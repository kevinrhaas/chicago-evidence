# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepared bounded source-surface controls; never native/LOD/walking acceptance."""
import copy
import math
import unittest
from human_apron_layering import conforming_bib, skirt_patch


def front_z(mesh, x, y, only_outer=False):
    found = []
    for fi, face in enumerate(mesh['triangles']):
        if only_outer and mesh['source_triangle_indices'][fi] < 0:
            continue
        a, b, c = [mesh['positions_m'][i] for i in face]
        det = (b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(det) < 1e-14:
            continue
        u = ((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/det
        v = ((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/det
        if min(u, v, 1-u-v) >= -1e-10:
            found.append(u*a[2]+v*b[2]+(1-u-v)*c[2])
    return max(found) if found else None


class ApronLayerSupport(unittest.TestCase):
    def test_real_support_diagonal_prevents_old_independent_grid_bridge(self):
        # A raised diagonal between source vertices1/3; the opposite grid diagonal
        # between0/2 cuts below the actual underlay at the center. This is an
        # adversarial surface control, not an assertion about a historical body.
        support = dict(name='test_bodice', positions_m=[[-.2,.1,0],[.2,.1,0],[.2,.4,0],[-.2,.4,.08]],
                       triangles=[[0,1,3],[1,2,3]], weights=[{'pelvis':1.}]*4)
        before = copy.deepcopy(support)
        panel = conforming_bib(support, {'spine_02':{'head_m':[0,0,-.1]}}, .088,
                               top=.312, half_width=(.2,.2), offset=.007)
        old_grid = dict(positions_m=[[x,y,z+.007]for x,y,z in support['positions_m']], triangles=[[0,1,2],[0,2,3]])
        self.assertLess(front_z(old_grid,0,.25), front_z(support,0,.25))
        self.assertAlmostEqual(front_z(panel,0,.25,True)-front_z(support,0,.25), .007)
        self.assertEqual(support,before)
        for fi, face in enumerate(panel['triangles']):
            source = panel['source_triangle_indices'][fi]
            if source < 0:
                continue
            for index in face:
                self.assertLessEqual(set(panel['source_basis'][index]),set(support['triangles'][source]))
        self.assertFalse(panel['receipt']['apron_layer_support']['walking_turning_seated_native_LOD_or_photo_accepted'])

    def test_lower_apron_preserves_source_Y_exact_weights_and_actual_faces(self):
        segments, rows = 48, 4
        skirt = dict(name='test_skirt', positions_m=[], weights=[], triangles=[])
        for row in range(rows):
            for col in range(segments):
                a = 2*math.pi*col/segments
                skirt['positions_m'].append([.2*math.sin(a),1-row*.1,.2*math.cos(a)])
                skirt['weights'].append({'pelvis':.7,'thigh_l':.3}if col<segments//2 else {'pelvis':1.})
        for row in range(rows-1):
            for col in range(segments):
                a=row*segments+col;b=row*segments+(col+1)%segments;c=b+segments;d=a+segments
                skirt['triangles'] += [[a,c,b],[a,d,c]]
        before=copy.deepcopy(skirt)
        apron=skirt_patch(skirt,rows=rows,segments=segments,columns_each_side=6,last_row_from_hem=1,
                          offset=.008,name='test_apron',material='garment_outer__test')
        for index,basis in enumerate(apron['source_basis'][:3*13]):
            source=next(iter(basis));p=apron['positions_m'][index];q=skirt['positions_m'][source]
            self.assertEqual(p[1],q[1]);self.assertEqual(apron['weights'][index],skirt['weights'][source])
            self.assertAlmostEqual(math.hypot(p[0],p[2])-math.hypot(q[0],q[2]),.008)
        self.assertEqual(skirt,before)
        self.assertTrue(all(i>=0 for i in apron['source_triangle_indices'][:2*2*12]))


if __name__=='__main__':
    unittest.main()
