# SPDX-License-Identifier: GPL-3.0-or-later
"""Coachman-only reconstructed layering; no anatomy, clip or runtime changes.

The source construction is NOT a posed-cloth certificate. Native exported
coat/breeches triangle crossings over complete idle/walk cycles remain required.
"""
import math


def _need(test, message):
    if not test:
        raise ValueError('coachman layers: ' + message)


def _sub(a, b):
    return [x-y for x, y in zip(a, b)]


def _dot(a, b):
    return math.fsum(x*y for x, y in zip(a, b))


def closest_triangle(point, a, b, c):
    """Closest actual triangle point and barycentrics, including edge regions."""
    ab, ac, ap = _sub(b, a), _sub(c, a), _sub(point, a)
    _need(_dot(ab, ab)*_dot(ac, ac)-_dot(ab, ac)**2 > 1e-20,
          'degenerate correspondence triangle')
    d1, d2 = _dot(ab, ap), _dot(ac, ap)
    if d1 <= 0 and d2 <= 0:
        bary = (1., 0., 0.)
    else:
        bp = _sub(point, b); d3, d4 = _dot(ab, bp), _dot(ac, bp)
        if d3 >= 0 and d4 <= d3:
            bary = (0., 1., 0.)
        else:
            vc = d1*d4-d3*d2
            if vc <= 0 and d1 >= 0 and d3 <= 0:
                v = d1/(d1-d3); bary = (1-v, v, 0.)
            else:
                cp = _sub(point, c); d5, d6 = _dot(ab, cp), _dot(ac, cp)
                if d6 >= 0 and d5 <= d6:
                    bary = (0., 0., 1.)
                else:
                    vb = d5*d2-d1*d6
                    if vb <= 0 and d2 >= 0 and d6 <= 0:
                        w = d2/(d2-d6); bary = (1-w, 0., w)
                    else:
                        va = d3*d6-d5*d4
                        if va <= 0 and d4-d3 >= 0 and d5-d6 >= 0:
                            w = (d4-d3)/((d4-d3)+(d5-d6)); bary = (0., 1-w, w)
                        else:
                            total = va+vb+vc
                            _need(total > 1e-20, 'degenerate correspondence triangle')
                            v, w = vb/total, vc/total; bary = (1-v-w, v, w)
    return [math.fsum(w*p[k] for w, p in zip(bary, (a, b, c))) for k in range(3)], bary


def surface_skin(mesh, point, band_m, maximum_distance_m):
    """Sample emitted clothing triangles, never an invented leg-weight formula."""
    best = None
    for face_id, face in enumerate(mesh['triangles']):
        tri = [mesh['positions_m'][i] for i in face]
        if max(p[1] for p in tri) < point[1]-band_m or min(p[1] for p in tri) > point[1]+band_m:
            continue
        q, bary = closest_triangle(point, *tri)
        distance = math.dist(point, q)
        if best is None or distance < best[0]:
            mapping = {}
            for weight, i in zip(bary, face):
                for bone, value in mesh['weights'][i].items():
                    mapping[bone] = mapping.get(bone, 0.) + max(0., weight)*value
            best = distance, mapping, face_id
    _need(best is not None and best[0] <= maximum_distance_m, 'clothing correspondence absent or too distant')
    return best


def bounded_skin(mapping, maximum_discard):
    _need(all(math.isfinite(v) and v >= 0 for v in mapping.values()), 'invalid interpolated skin')
    items = sorted(((k, v) for k, v in mapping.items() if v > 0), key=lambda x: (-x[1], x[0]))
    total = math.fsum(v for _, v in items)
    _need(total > 0, 'empty skin')
    discarded = math.fsum(v for _, v in items[4:])/total
    _need(discarded <= maximum_discard, 'clothing correspondence discards excessive skin mass')
    kept = math.fsum(v for _, v in items[:4])
    return {k: v/kept for k, v in items[:4]}, discarded


def layered_skirt(body, breeches, coat, waist, tailoring, slab_points, finish_edges):
    """Loft outside BOTH source layers with one connected closed front.

    The gentleman's open-front constructor and its clearance test are untouched.
    Keep the inherited >4mm sampled radial construction constraint, including
    the front. It is NOT actual triangle clearance or a posed-cloth proof.
    """
    t = tailoring
    segs, rows, hem = t['segments'], t['rows'], t['hem_y']
    _need(segs >= 8 and rows >= 3, 'insufficient skirt sampling')
    _need(t['front_closure'] == 'single_closed_ring_v1', 'undeclared front topology')
    top = waist + .006
    levels = [top+(hem-top)*i/(rows-1) for i in range(rows)]
    angles = [2*math.pi*k/segs for k in range(segs)]
    directions = [(math.sin(a), math.cos(a)) for a in angles]
    tris = [[mesh['positions_m'][i] for i in face]
            for mesh in [*body['meshes'], breeches] for face in mesh['triangles']
            if min(mesh['positions_m'][i][1] for i in face) <= top+.02
            and max(mesh['positions_m'][i][1] for i in face) >= hem-.02]
    supports = []
    for i, _ in enumerate(levels):
        points = slab_points(tris, levels[min(rows-1, i+1)]-.004, levels[max(0, i-1)]+.004)
        _need(len(points) >= 3, 'empty body/breeches envelope band')
        supports.append([max(nx*p[0]+nz*p[2] for p in points)+t['ease'] for nx, nz in directions])
    widest = max(range(rows), key=lambda i: sum(supports[i]))
    for i in range(widest+1, rows):
        supports[i] = [max(a, .995*b) for a, b in zip(supports[i], supports[i-1])]
    for i, support in enumerate(supports):
        supports[i] = [max(support[k], (support[(k-1) % segs]+2*support[k]+support[(k+1) % segs])/4)
                       for k in range(segs)]
    coat_section = []
    for face in coat['triangles']:
        tri = [coat['positions_m'][i] for i in face]
        coat_section.extend(slab_points([tri], top+.008, top+.008))
    _need(coat_section, 'actual bodice seam section missing')
    out = dict(name='livery_coat_skirt', material='garment_outer__livery_coat_green_1904',
               positions_m=[], triangles=[], uvs=[], weights=[], corner_uvs=[])
    maximum_distance = maximum_discard = 0.
    for i, y in enumerate(levels):
        fraction = i/(rows-1)
        blend = min(1., max(0., (top-y)/t['seam_skin_blend_m']))
        blend = blend*blend*(3-2*blend)
        for k, (nx, nz) in enumerate(directions):
            radius = supports[i][k]+(.006+.014*max(0., nz))*fraction**1.4
            seam_radius = max(nx*p[0]+nz*p[2] for p in coat_section)-.0015
            if i == 0:
                radius = min(radius, seam_radius)
            point = [nx*radius, y, nz*radius]
            distance, lower, _ = surface_skin(breeches, point, t['skin_y_band_m'], t['maximum_skin_distance_m'])
            maximum_distance = max(maximum_distance, distance)
            if blend < 1:
                _, upper, _ = surface_skin(coat, [nx*seam_radius, top+.008, nz*seam_radius],
                                           t['skin_y_band_m'], t['maximum_skin_distance_m'])
                mapping = {bone: (1-blend)*upper.get(bone, 0.)+blend*lower.get(bone, 0.)
                           for bone in upper.keys() | lower.keys()}
            else:
                mapping = lower
            weights, discarded = bounded_skin(mapping, t['maximum_discarded_skin_mass'])
            maximum_discard = max(maximum_discard, discarded)
            out['positions_m'].append(point); out['uvs'].append([k/segs, fraction]); out['weights'].append(weights)
    for i in range(rows-1):
        for k in range(segs):
            next_k = (k+1) % segs
            a, b = i*segs+k, i*segs+next_k
            c, d = (i+1)*segs+next_k, (i+1)*segs+k
            uv = [[k/segs, i/(rows-1)], [(k+1)/segs, i/(rows-1)],
                  [(k+1)/segs, (i+1)/(rows-1)], [k/segs, (i+1)/(rows-1)]]
            for face, corners in (([a, b, c], [uv[0], uv[1], uv[2]]),
                                  ([a, c, d], [uv[0], uv[2], uv[3]])):
                out['triangles'].append(face); out['corner_uvs'].append(corners)
    worst = math.inf
    for i in range(rows-1):
        for point in slab_points(tris, levels[i+1], levels[i]):
            angle = math.atan2(point[0], point[2]) % (2*math.pi)
            k = min(segs-1, max(0, int(angle/(2*math.pi)*segs)))
            fraction = (point[1]-levels[i])/(levels[i+1]-levels[i])
            radius = math.fsum(w*math.hypot(*[out['positions_m'][j*segs+k][a] for a in (0, 2)])
                               for w, j in ((1-fraction, i), (fraction, i+1)))
            worst = min(worst, radius-math.hypot(point[0], point[2]))
    _need(worst > .004, 'sampled radial layered-envelope construction constraint is <=4mm')
    out = finish_edges(out, .0018)
    out.setdefault('receipt', {}).update(dict(garment='coachman-only layered closed-front livery skirt',
        construction_revision='coachman-layering-source-v1', hem_y_m=hem, top_y_m=top,
        minimum_sampled_radial_envelope_clearance_m=worst, front_closure=t['front_closure'],
        skinning='nearest emitted breeches triangle, blended to actual bodice at waist',
        maximum_skin_correspondence_distance_m=maximum_distance, maximum_discarded_skin_mass=maximum_discard,
        body_and_breeches_unchanged=True, posed_triangle_clearance_accepted=False,
        standing_triangle_clearance_accepted=False, front_coverage_accepted=False,
        native_export_and_weave_rebinding_required=True))
    return out
