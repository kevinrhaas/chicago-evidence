# SPDX-License-Identifier: GPL-3.0-or-later
"""Original empty coach upholstery and bounded finish reconstruction (T-3084).

The 1893 colour lithograph supplies dark green coachwork, black running gear and
bright fine lining. It does not identify pigments, varnish optics, upholstery or
hidden cabin joinery. No source pixels or external geometry are embedded.
"""
import copy
import math


def finished_materials(materials, recipe):
    """Retain the accepted lamp materials; give cabin glass its own material."""
    result = copy.deepcopy(materials)
    if len(result) != 7:
        raise ValueError('V19 requires the explicit recessed quarter material')
    if recipe.get('schema') != 1 or recipe.get('grade') != 'reconstructed':
        raise ValueError('Explicit reconstructed coach finish recipe required')
    for index, key in [(0, 'green_coachwork'), (1, 'black_coachwork'), (2, 'dark_upholstery')]:
        material = copy.deepcopy(recipe[key])
        pbr = material['pbrMetallicRoughness']
        values = pbr['baseColorFactor'] + [pbr['metallicFactor'], pbr['roughnessFactor']]
        if not all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1 for v in values):
            raise ValueError('Finite bounded coach finish coefficients required')
        result[index] = material
    glass = copy.deepcopy(recipe['cabin_glass'])
    transmission = glass.get('extensions', {}).get('KHR_materials_transmission', {}).get('transmissionFactor')
    if transmission != .98 or glass['pbrMetallicRoughness']['baseColorFactor'][3] != 1:
        raise ValueError('Explicit thin physical cabin glass required')
    result.append(glass)
    if result[3:7] != materials[3:7]:
        raise ValueError('Accepted lamp/iron/glass and unidentified quarter finishes changed')
    return result


def rounded_pad(center, size, axis=1, samples=32):
    """A closed soft rectangular cushion INSIDE its stated original box.

    Four superelliptic rings make a rounded edge without adding tufting, buttons
    or a historical upholstery pattern the occupied catalogue cannot show.
    """
    if axis not in (1, 2) or samples < 16 or samples % 4:
        raise ValueError('A cushion uses an up/depth axis and complete quadrant samples')
    if any(not math.isfinite(v) or v <= 0 for v in size):
        raise ValueError('Finite positive cushion envelope required')
    across = [i for i in range(3) if i != axis]
    vertices = []
    for offset, scale in [(-.5, .88), (-.23, 1.), (.23, 1.), (.5, .88)]:
        for i in range(samples):
            angle = math.tau * i / samples
            point = list(center)
            point[axis] += offset * size[axis]
            for coordinate, component in zip(across, (math.cos(angle), math.sin(angle))):
                point[coordinate] += math.copysign(abs(component) ** .36, component) * size[coordinate] * scale / 2
            vertices.append(point)
    # Explicit outward winding, independent of which axis holds the rings.
    faces = [list(reversed(range(samples))), list(range(3 * samples, 4 * samples))]
    for ring in range(3):
        for i in range(samples):
            j = (i + 1) % samples
            faces.append([ring * samples + i, ring * samples + j,
                          (ring + 1) * samples + j, (ring + 1) * samples + i])
    if axis == 1:
        faces = [list(reversed(face)) for face in faces]
    return vertices, faces


def coach_front_wrap(profile, width, rows=28, columns=20):
    """Close the lower cabin with a continuous source-outline-following nose.

    The former small flat closure covered only the upper front. This original
    thin shell follows the existing side outline down to its lowest point;
    20mm transverse crown and15mm thickness are reconstructed construction.
    """
    low, high = min(y for z, y in profile), max(y for z, y in profile)
    levels = sorted({round(y, 10) for y in
                     [low, high] + [low + (high - low) * i / rows for i in range(1, rows)] +
                     [y for z, y in profile]})
    vertices = []
    for inner in (False, True):
        for y in levels:
            hits = [z0 + (z1 - z0) * (y - y0) / (y1 - y0)
                    for (z0, y0), (z1, y1) in zip(profile, profile[1:] + profile[:1])
                    if y0 != y1 and min(y0, y1) - 1e-12 <= y <= max(y0, y1) + 1e-12]
            if not hits:
                raise ValueError('Missing front outline bearing')
            half = width(y)
            for ix in range(columns + 1):
                fraction = -1 + 2 * ix / columns
                vertices.append([fraction * half, y,
                                 max(hits) + .020 * (1 - fraction * fraction) - (.015 if inner else 0.)])
    stride = columns + 1
    count = len(levels) * stride
    faces = []
    for iy in range(len(levels) - 1):
        for ix in range(columns):
            i = iy * stride + ix
            faces.extend([[i, i + 1, i + stride + 1, i + stride],
                          [count + i + stride, count + i + stride + 1, count + i + 1, count + i]])
    boundary = list(range(stride)) + [i * stride + columns for i in range(1, len(levels))]
    boundary += list(range(count - 2, count - stride - 1, -1))
    boundary += [i * stride for i in range(len(levels) - 2, 0, -1)]
    faces.extend([[i, count + i, count + j, j] for i, j in zip(boundary, boundary[1:] + boundary[:1])])
    return vertices, faces


def curved_coach_panel(profile, side, width, thickness, triangulate, segments=8):
    """Subdivide the ORIGINAL outline triangles before rolling the coach belly.

    A concave side outline can have several intervals at the same height. Retain
    that outline and its holes instead of filling its horizontal envelope. Every
    old triangle gets a conforming barycentric grid; coincident edge vertices are
    shared so the reconstructed curved face also has continuous smooth normals.
    """
    if side not in (-1, 1) or segments < 2 or thickness <= 0:
        raise ValueError('Bounded sampled coach panel required')
    points = []
    lookup = {}
    def point(z, y):
        key = (round(float(z), 12), round(float(y), 12))
        if key not in lookup:
            lookup[key] = len(points)
            points.append(key)
        return lookup[key]
    triangles = []
    for tri in triangulate(profile):
        a, b, c = [profile[k] for k in tri]
        def grid(i, j):
            u, v = i / segments, j / segments
            return point(a[0] + u * (b[0] - a[0]) + v * (c[0] - a[0]),
                         a[1] + u * (b[1] - a[1]) + v * (c[1] - a[1]))
        for i in range(segments):
            for j in range(segments - i):
                triangles.append([grid(i, j), grid(i + 1, j), grid(i, j + 1)])
                if i + j < segments - 1:
                    triangles.append([grid(i + 1, j), grid(i + 1, j + 1), grid(i, j + 1)])
    # The original profile is CCW(z,y), whose normal is -X. Normalize here;
    # do not let the caller's original clockwise ordering invert the skin.
    count = len(points)
    vertices = []
    for inner in (False, True):
        for z, y in points:
            t = max(0., min(1., (1.26 - y) / .91))
            roll = .018 * 4 * t * (1 - t)
            x = side * (width(y) + (0. if inner else thickness + roll))
            vertices.append([x, y, z])
    faces = [list(reversed(tri)) for tri in triangles]
    faces += [[count + i for i in tri] for tri in triangles]
    area = sum(a[0] * b[1] - b[0] * a[1]
               for a, b in zip(profile, profile[1:] + profile[:1]))
    order = list(range(len(profile)))
    if area < 0:
        order.reverse()
    for ai, bi in zip(order, order[1:] + order[:1]):
        a, b = profile[ai], profile[bi]
        edge = [point(a[0] + (b[0] - a[0]) * i / segments,
                      a[1] + (b[1] - a[1]) * i / segments) for i in range(segments + 1)]
        for i, j in zip(edge, edge[1:]):
            faces.append([i, j, count + j, count + i])
    if len(points) != count:
        raise ValueError('A sampled outline edge is absent from its cap triangulation')
    if side < 0:
        faces = [list(reversed(face)) for face in faces]
    return vertices, faces
