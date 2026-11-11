"""Small source controls; no native asset, body preparation or visual acceptance."""
import copy
import math
import unittest
from unittest.mock import patch

from human_collar_rim import fair_stock_top_rim


class RimControls(unittest.TestCase):
    def test_uniform_band_and_declared_style_anchors_remain_exact(self):
        old = [1.55]*40
        out, receipt = fair_stock_top_rim(old, [1.5]*40, [0, 10, 20, 30], .004)
        self.assertEqual(out, old)
        self.assertEqual(receipt['maximum_top_lowering_m'], 0)
        self.assertFalse(receipt['native_fit_accepted'])

    def test_side_jaw_sample_kink_is_faired_below_unchanged_front_and_back(self):
        old = [1.55]*40
        old[13] -= .003
        protected = [i for i in range(40) if min(i, 40-i) <= 8] + [20]
        snapshot = list(old)
        out, receipt = fair_stock_top_rim(old, [1.5]*40, protected, .004)
        self.assertEqual(old, snapshot)
        self.assertTrue(all(out[i] == old[i] for i in protected))
        self.assertTrue(all(0 <= a-b <= .004+1e-12 for a, b in zip(old, out)))
        # A sharp one-sample dip becomes a broader linen edge, without raising
        # its jaw-limited low point or altering the protected front silhouette.
        self.assertLess(out[12], old[12])
        self.assertLess(out[14], old[14])
        before = abs(old[12]-2*old[13]+old[14])
        after = abs(out[12]-2*out[13]+out[14])
        self.assertLess(after, before)
        self.assertGreater(receipt['maximum_top_lowering_m'], 0)

    def test_arc_fairing_is_rotation_equivariant_and_does_not_invert_a_short_band(self):
        old = [1.55+.001*math.sin(i*.9) for i in range(40)]
        bottoms = [p-.006 for p in old]
        anchors = [0, 7, 20, 33]
        out, _ = fair_stock_top_rim(old, bottoms, anchors, .004)
        shift = 9
        rotate = lambda row: row[-shift:]+row[:-shift]
        moved, _ = fair_stock_top_rim(rotate(old), rotate(bottoms), [(i+shift)%40 for i in anchors], .004)
        for actual, expected in zip(moved, rotate(out)):
            self.assertAlmostEqual(actual, expected, places=12)
        self.assertTrue(all(a-b <= .0015+1e-12 for a, b in zip(old, out)))

    def test_unknown_or_unbounded_inputs_are_refused(self):
        for tops, bottoms, anchors, allowance in [
            ([1.]*11, [0.]*11, [0, 5], .004),
            ([1.]*40, [0.]*39, [0, 20], .004),
            ([float('nan')]*40, [0.]*40, [0, 20], .004),
            ([1.]*40, [1.]*40, [0, 20], .004),
            ([1.]*40, [0.]*40, [0], .004),
            ([1.]*40, [0.]*40, [0, 40], .004),
            ([1.]*40, [0.]*40, [0, 20], .02),
        ]:
            with self.subTest(allowance=allowance, count=len(tops)):
                with self.assertRaises(ValueError):
                    fair_stock_top_rim(tops, bottoms, anchors, allowance)

    def test_actual_stock_constructor_preserves_body_rig_and_nonshape_channels(self):
        # Existing source owner, synthetic neck only: no MakeHuman construction.
        import human_merchant_1835 as owner
        positions = [[.055*math.sin(2*math.pi*k/40), 1.44+j*.005,
                      .045*math.cos(2*math.pi*k/40)] for j in range(29) for k in range(40)]
        # One jaw sample produces an actual owner clamp kink at the side.
        positions.append([.075, 1.535, 0.])
        body = {'meshes':[{'positions_m':positions,
            'weights':[{'neck_01':1.}]*(len(positions)-1)+[{'head':1.}]}]}
        bones = {'neck_01':{'head_m':[0., 1.5, 0.]}}
        before = copy.deepcopy((body, bones))
        with patch.object(owner, 'fair_stock_top_rim', side_effect=lambda t, b, a, m:(list(t), {'control':'unfaired'})):
            original, original_frame = owner.stock(body, bones)
        actual, frame = owner.stock(body, bones)
        self.assertEqual((body, bones), before)
        for key in ('triangles', 'weights', 'uvs', 'material', 'name'):
            self.assertEqual(actual[key], original[key], key)
        first_return = min(actual['flat_face_indices'])
        self.assertEqual(actual['corner_uvs'][:first_return], original['corner_uvs'][:first_return])
        # The canonical edge finisher recomputes its bounded return texels for
        # the changed edge length; no frozen outer cloth corners are repacked.
        self.assertTrue(all(math.isfinite(value) for face in actual['corner_uvs'][first_return:]
                            for uv in face for value in uv))
        self.assertEqual(frame[0], original_frame[0])
        self.assertEqual(frame[2], original_frame[2])
        receipt = actual['receipt']['top_rim_fairing']
        self.assertTrue(receipt['original_style_anchor_heights_preserved'])
        self.assertFalse(receipt['actual_posed_clearance_accepted'])
        self.assertGreater(receipt['maximum_top_lowering_m'], 0)
        self.assertIn('physical_edge_return', actual['receipt'])


if __name__ == '__main__':
    unittest.main()
