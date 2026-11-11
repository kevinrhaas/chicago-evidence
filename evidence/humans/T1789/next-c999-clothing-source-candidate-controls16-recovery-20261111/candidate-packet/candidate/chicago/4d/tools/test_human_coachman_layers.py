# SPDX-License-Identifier: GPL-3.0-or-later
"""Tiny synthetic controls only; never constructs/exports a human or claims fit."""
import copy
import ast
import json
import math
from pathlib import Path
import unittest
from human_coachman_layers import closest_triangle, surface_skin, bounded_skin, layered_skirt
from human_workwear_fit import _slab_points
from human_period_wardrobe import finish_edges


def tube(radius, low, high, segments=16):
    positions = [[radius*math.sin(2*math.pi*k/segments), y,
                  radius*math.cos(2*math.pi*k/segments)] for y in (high, low) for k in range(segments)]
    triangles = []
    for k in range(segments):
        n = (k+1) % segments
        triangles.extend([[k, n, segments+n], [k, segments+n, segments+k]])
    return dict(positions_m=positions, triangles=triangles,
                weights=[{'pelvis': 1.} for _ in positions])


class SourceControls(unittest.TestCase):
    def test_recipe_exactly_declares_source_tailoring(self):
        root = Path(__file__).resolve().parents[1]
        tree = ast.parse((root/'tools/human_coachman_1904.py').read_text())
        value = next(node.value for node in tree.body if isinstance(node, ast.Assign)
                     and any(isinstance(target, ast.Name) and target.id == 'TAILORING' for target in node.targets))
        # Evaluate only the literal dict declarations; never import/build a human.
        self.assertTrue(all(isinstance(node, (ast.Dict, ast.Call, ast.Name, ast.Load,
            ast.keyword, ast.Constant)) for node in ast.walk(value)))
        self.assertTrue(all(isinstance(node.func, ast.Name) and node.func.id == 'dict'
                            for node in ast.walk(value) if isinstance(node, ast.Call)))
        tailoring = eval(compile(ast.Expression(value), '<tailoring-data-only>', 'eval'), {'__builtins__': {}, 'dict': dict})
        recipe = json.loads((root/'data/humans/recipes/coachman_livery_1904.json').read_text())
        self.assertEqual(recipe['coachman_components']['tailoring'], tailoring)
        self.assertEqual(recipe['colors_linear_rgba']['garment_outer__livery_coat_green_1904'], [.014, .026, .019, 1])

    def test_closest_surface_interior_and_edge(self):
        triangle = ([0., 0., 0.], [1., 0., 0.], [0., 1., 0.])
        point, bary = closest_triangle([.25, .25, 1.], *triangle)
        self.assertEqual(point, [.25, .25, 0.]); self.assertEqual(bary, (.5, .25, .25))
        self.assertEqual(closest_triangle([2., 0., 1.], *triangle)[0], [1., 0., 0.])
        with self.assertRaisesRegex(ValueError, 'degenerate'):
            closest_triangle([0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0])

    def test_correspondence_and_distance_refusal(self):
        mesh = dict(positions_m=[[0, 0, 0], [1, 0, 0], [0, 1, 0]], triangles=[[0, 1, 2]],
                    weights=[{'pelvis': 1.}, {'thigh_l': 1.}, {'pelvis': 1.}])
        before = copy.deepcopy(mesh)
        distance, weights, face = surface_skin(mesh, [.5, 0, .02], .04, .15)
        self.assertAlmostEqual(distance, .02); self.assertEqual(face, 0)
        self.assertEqual(weights, {'pelvis': .5, 'thigh_l': .5}); self.assertEqual(mesh, before)
        with self.assertRaisesRegex(ValueError, 'absent or too distant'):
            surface_skin(mesh, [.5, 0, 1.], .04, .15)

    def test_skin_mass_is_not_silently_discarded(self):
        with self.assertRaisesRegex(ValueError, 'excessive skin mass'):
            bounded_skin({str(i): 1/6 for i in range(6)}, .025)
        weights, discarded = bounded_skin({'pelvis': 2., 'thigh_l': 2.}, .025)
        self.assertEqual(weights, {'pelvis': .5, 'thigh_l': .5}); self.assertEqual(discarded, 0)

    def test_matching_barycentric_weights_are_not_posed_correspondence_proof(self):
        # Identity pelvis and a 90-degree thigh rotation: LBS is bilinear in
        # bind position and weights. Its two interpolations do not commute.
        bind = [.5, 0., 0.]
        rotated = [-bind[1], bind[0], bind[2]]
        lbs_of_interpolated = [(a+b)/2 for a, b in zip(bind, rotated)]
        interpolated_posed_triangle = [0., .5, 0.]
        self.assertGreater(math.dist(lbs_of_interpolated, interpolated_posed_triangle), .3)

    def test_closed_fixture_topology_and_honest_receipt(self):
        body = {'meshes': [tube(.07, .4, 1.2)]}
        breeches, coat = tube(.1, .4, 1.2), tube(.15, 1., 1.2)
        inputs = copy.deepcopy((body, breeches, coat))
        tailoring = dict(segments=16, rows=5, hem_y=.5, ease=.036,
            front_closure='single_closed_ring_v1', seam_skin_blend_m=.08,
            skin_y_band_m=.04, maximum_skin_distance_m=.15, maximum_discarded_skin_mass=.025)
        result = layered_skirt(body, breeches, coat, 1., tailoring, _slab_points, finish_edges)
        self.assertEqual((body, breeches, coat), inputs)
        # Every ring closes through the last/first angular columns. No two
        # coincident front endpoints or coplanar overlapping front sheets.
        self.assertIn([15, 0, 16], result['triangles'])
        outer = result['positions_m'][:16*5]
        self.assertEqual(len({tuple(p) for p in outer}), len(outer))
        self.assertEqual(len(result['corner_uvs']), len(result['triangles']))
        self.assertEqual(result['receipt']['physical_edge_return']['thickness_m'], .0018)
        self.assertIs(result['receipt']['physical_edge_return']['fit_accepted'], False)
        for key in ['posed_triangle_clearance_accepted', 'standing_triangle_clearance_accepted', 'front_coverage_accepted']:
            self.assertIs(result['receipt'][key], False)
        self.assertIs(result['receipt']['native_export_and_weave_rebinding_required'], True)


if __name__ == '__main__':
    unittest.main()
