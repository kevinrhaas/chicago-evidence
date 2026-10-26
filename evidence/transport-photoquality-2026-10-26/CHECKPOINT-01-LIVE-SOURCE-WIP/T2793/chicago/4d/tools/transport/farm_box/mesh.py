# SPDX-License-Identifier: GPL-3.0-or-later
"""Original metre-scale surfaces for the versioned farm-box master.

The mesh is authored in each exported articulation frame. Normals and grain UVs
are carried by the actual surface, rather than another renderer-side model.
"""
from collections import defaultdict
import json
import math
import struct


def unit(v):
    length = math.sqrt(math.fsum(x * x for x in v))
    if length <= 1e-14:
        raise ValueError("Degenerate surface normal")
    return tuple(x / length for x in v)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


class Mesh:
    def __init__(self):
        self.nodes = []
        self.parts = []
        self.batches = defaultdict(lambda: [[], [], []])

    def node(self, name, parent=None, translation=(0, 0, 0)):
        if any(n["name"] == name for n in self.nodes):
            raise ValueError("Duplicate frame " + name)
        result = len(self.nodes)
        self.nodes.append({"name": name, "translation": list(translation)})
        if parent is not None:
            self.nodes[parent].setdefault("children", []).append(result)
        return result

    def surface(self, name, frame, material, vertices, faces, uvs=None, normals=None):
        """Triangulate convex planar faces; emit real per-triangle flat normals."""
        positions, directions, texture = self.batches[(frame, material)]
        start = len(positions) // 3
        used = []
        for face in faces:
            for k in range(1, len(face)-1):
                ids = (face[0], face[k], face[k+1])
                points = [vertices[i] for i in ids]
                normal = unit(cross(sub(points[1], points[0]), sub(points[2], points[0])))
                for i, point in zip(ids, points):
                    if not all(math.isfinite(v) for v in point):
                        raise ValueError("Nonfinite geometry " + name)
                    positions.extend(point)
                    directions.extend(normals[i] if normals else normal)
                    texture.extend(uvs[i] if uvs else (point[2]/2.24, point[1]/.14))
                    used.append(point)
        self.parts.append({"name": name, "frame": self.nodes[frame]["name"],
                           "material": material, "first_vertex_in_batch": start,
                           "vertex_count": len(used),
                           "min_m": [min(p[k] for p in used) for k in range(3)],
                           "max_m": [max(p[k] for p in used) for k in range(3)]})

    def box(self, name, frame, size, centre, material, grain_axis=2, phase=0, cut_material=4):
        half = [x/2 for x in size]
        vertices = [[centre[k]+s[k]*half[k] for k in range(3)]
                    for s in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
                              (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
        faces = [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]
        # Each face owns its grain projection; edge/cut treatment can be assigned
        # separately without distorting the long-grain scale on adjacent faces.
        for number, face in enumerate(faces):
            spans = [max(vertices[i][k] for i in face)-min(vertices[i][k] for i in face) for k in range(3)]
            if spans[grain_axis] == 0:
                a, b = [k for k in range(3) if spans[k] > 0]
                uv = [((p[a]-centre[a])/size[a]+.5, (p[b]-centre[b])/size[b]+.5) for p in vertices]
                face_material = cut_material if material in (0, 1) else material
            else:
                other = max((k for k in range(3) if k != grain_axis), key=lambda k: spans[k])
                uv = [(p[grain_axis]/2.24+phase, p[other]/.14) for p in vertices]
                face_material = material
            self.surface(f"{name}.face{number}", frame, face_material, vertices, [face], uv)

    def lathe_x(self, name, frame, profile, centre, material, sides, phase=0):
        """Closed radial profile about the wheel axle, with smooth ring normals.

        Profile order is clockwise in the axial/radial section. A repeated first
        point is optional; the closing segment is emitted exactly once.
        """
        if profile[-1] == profile[0]:
            profile = profile[:-1]
        if sides < 8 or len(profile) < 3 or any(r <= 0 for _, r in profile):
            raise ValueError("Invalid revolved section")
        profile_distance = 0
        for section in range(len(profile)):
            ax, radius = profile[section]
            bx, next_radius = profile[(section+1) % len(profile)]
            if ax == bx and radius == next_radius:
                raise ValueError("Zero-length revolved section")
            slope = unit((radius-next_radius, bx-ax, 0))
            vertices, normals, uv, faces = [], [], [], []
            segment_length = math.hypot(bx-ax, next_radius-radius)
            for row, (x, r) in enumerate([(ax, radius), (bx, next_radius)]):
                for j in range(sides+1):
                    angle = math.tau*j/sides
                    c, s = math.cos(angle), math.sin(angle)
                    vertices.append((centre[0]+x, centre[1]+r*c, centre[2]+r*s))
                    normals.append((slope[0], slope[1]*c, slope[1]*s))
                    uv.append((angle*radius/2.24+phase, (profile_distance+row*segment_length)/.14))
            for j in range(sides):
                faces.append((j, j+1, sides+1+j+1, sides+1+j))
            self.surface(f"{name}.section{section}", frame, material,
                         vertices, faces, uv, normals)
            profile_distance += segment_length

    def disc_x(self, name, frame, radius, x, centre, material, sides, outward):
        vertices = [(centre[0]+x, centre[1], centre[2])]
        for j in range(sides):
            a = math.tau*j/sides
            vertices.append((centre[0]+x, centre[1]+radius*math.cos(a), centre[2]+radius*math.sin(a)))
        faces = [(0, j+1, (j+1) % sides+1) for j in range(sides)]
        if outward < 0:
            faces = [tuple(reversed(face)) for face in faces]
        uv = [(.5+(p[1]-centre[1])/(2*radius), .5+(p[2]-centre[2])/(2*radius)) for p in vertices]
        self.surface(name, frame, material, vertices, faces, uv)

    def glb(self, materials, images, extras):
        payload = bytearray()
        views, accessors, meshes = [], [], []

        def append(raw, target=None):
            payload.extend(b"\0" * (-len(payload) % 4))
            view = {"buffer": 0, "byteOffset": len(payload), "byteLength": len(raw)}
            if target is not None:
                view["target"] = target
            views.append(view)
            payload.extend(raw)
            return len(views)-1

        def attribute(values, width):
            raw = struct.pack("<"+"f"*len(values), *values)
            view = append(raw, 34962)
            accessors.append({"bufferView": view, "componentType": 5126,
                              "count": len(values)//width, "type": f"VEC{width}",
                              "min": [min(values[k::width]) for k in range(width)],
                              "max": [max(values[k::width]) for k in range(width)]})
            return len(accessors)-1

        nodes = json.loads(json.dumps(self.nodes))
        for (frame, material), (positions, normals, uv) in self.batches.items():
            mesh = {"name": nodes[frame]["name"]+"_"+materials[material]["name"],
                    "primitives": [{"attributes": {"POSITION": attribute(positions, 3),
                                                    "NORMAL": attribute(normals, 3),
                                                    "TEXCOORD_0": attribute(uv, 2)},
                                    "material": material}]}
            meshes.append(mesh)
            nodes[frame].setdefault("children", []).append(len(nodes))
            nodes.append({"name": mesh["name"], "mesh": len(meshes)-1})
        embedded = [{"bufferView": append(raw), "mimeType": "image/png"} for raw in images]
        payload.extend(b"\0" * (-len(payload) % 4))
        document = {"asset": {"version": "2.0", "generator": "Original Chicago farm-box master",
                              "copyright": "GPL-3.0-or-later geometry; credited CC0 optical material analogy"},
                    "scene": 0, "scenes": [{"nodes": [0]}], "nodes": nodes,
                    "meshes": meshes, "materials": materials, "accessors": accessors,
                    "bufferViews": views, "buffers": [{"byteLength": len(payload)}],
                    "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}],
                    "textures": [{"source": i, "sampler": 0} for i in range(len(images))],
                    "images": embedded, "extras": extras}
        encoded = json.dumps(document, separators=(",", ":"), allow_nan=False).encode()
        encoded += b" " * (-len(encoded) % 4)
        return (struct.pack("<III", 0x46546c67, 2, 28+len(encoded)+len(payload))
                + struct.pack("<II", len(encoded), 0x4e4f534a)+encoded
                + struct.pack("<II", len(payload), 0x004e4942)+payload)
