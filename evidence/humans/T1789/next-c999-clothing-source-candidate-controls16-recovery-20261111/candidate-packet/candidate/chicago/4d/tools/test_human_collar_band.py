# SPDX-License-Identifier: GPL-3.0-or-later
"""Collar edge controls on an uneven source tessellation; no export/fit claim."""
import collections
import copy
import math
import unittest

from human_dress_components import collar_band


def uneven_neck():
    n = 12
    mesh = dict(name='source_bodice', material='plain', positions_m=[], triangles=[],
                uvs=[], corner_uvs=[], weights=[])
    for row in range(3):
        for k in range(n):
            theta = 2*math.pi*k/n
            y = (1.490, 1.509 + .006*math.sin(3*theta + .4), 1.535)[row]
            mesh['positions_m'].append([.055*math.sin(theta), y, .055*math.cos(theta)])
            mesh['uvs'].append([k/n, row/2])
            mesh['weights'].append({'neck_01': 1.})
    for row in range(2):
        for k in range(n):
            a = row*n+k; b = row*n+(k+1) % n
            mesh['triangles'].extend([[a, b, b+n], [a, b+n, a+n]])
    mesh['corner_uvs'] = [[list(mesh['uvs'][i]) for i in face] for face in mesh['triangles']]
    return mesh, {'neck_01': {'head_m': [0., 1.5, 0.]}}


def outer_lower_edges(mesh, below=1.522):
    # finish_edges marks its added cloth-return faces; measure the emitted outer shell.
    faces = mesh['triangles'][:min(mesh['flat_face_indices'])]
    counts = collections.Counter(tuple(sorted((a, b)))
        for face in faces for a, b in zip(face, face[1:]+face[:1]))
    return [(a, b) for (a, b), count in counts.items()
            if count == 1 and max(mesh['positions_m'][i][1] for i in (a, b)) < below]


class CollarBand(unittest.TestCase):
    def test_narrow_cook_band_survives_triangles_crossing_its_entire_height(self):
        source, bones = uneven_neck()
        for i, p in enumerate(source['positions_m']):
            if i >= 24:
                p[1] = 1.512
            elif i >= 12:
                p[1] = 1.509 + .0005*math.sin(i)
        collar = collar_band(source, bones, lift=.0022)
        edges = outer_lower_edges(collar, below=1.511)
        self.assertTrue(edges)
        for edge in edges:
            for i in edge:
                self.assertAlmostEqual(collar['positions_m'][i][1], 1.510, places=12)
        self.assertAlmostEqual(max(p[1] for p in collar['positions_m']), 1.512, places=12)

    def test_lower_rim_is_one_level_closed_ring_not_source_triangle_steps(self):
        source, bones = uneven_neck()
        original = copy.deepcopy(source)
        collar = collar_band(source, bones)
        self.assertEqual(source, original)
        edges = outer_lower_edges(collar)
        self.assertTrue(edges)
        graph = collections.defaultdict(set)
        for a, b in edges:
            graph[a].add(b); graph[b].add(a)
            for i in (a, b):
                self.assertAlmostEqual(collar['positions_m'][i][1], 1.510, places=12)
        self.assertTrue(all(len(neighbours) == 2 for neighbours in graph.values()))
        seen = set(); pending = [next(iter(graph))]
        while pending:
            i = pending.pop()
            if i not in seen:
                seen.add(i); pending.extend(graph[i]-seen)
        self.assertEqual(seen, set(graph))

    def test_uniform_neck_weights_keep_rim_coherent_under_rigid_neck_rotation(self):
        source, bones = uneven_neck()
        collar = collar_band(source, bones)
        angle = math.radians(70.)
        def posed(p):
            x, y, z = p
            return [math.cos(angle)*x + math.sin(angle)*z, y+.07,
                    -math.sin(angle)*x + math.cos(angle)*z]
        rim = {i for edge in outer_lower_edges(collar) for i in edge}
        self.assertTrue(rim)
        for i in rim:
            self.assertEqual(collar['weights'][i], {'neck_01': 1.})
            self.assertAlmostEqual(posed(collar['positions_m'][i])[1], 1.580, places=12)
        # This is the rigid-neck case only; variable skin weights need native posed proof.
        self.assertFalse(collar['receipt']['posed_support_accepted'])


if __name__ == '__main__':
    unittest.main()
