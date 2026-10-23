# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import json,unittest,copy,math
P=Path(__file__).parent
s=json.loads(Path('/workspace/shared/horse-head-groove-coat-next/trial1/head-source-surface.json').read_text())
def validate(r):
 if r['input090_sha256']!='090be8fdc2516ee5b5c8f886026f441850cc208f17b6ede71fed9007ab80f12f':raise ValueError('wrong input')
 for row in r['rows']:
  if len(row['original_18_projected_points'])!=18 or len(row['conforming_loop'])!=row['conforming_piecewise_planar_cut_point_count']or len(row['extra_source_edge_crossings'])!=4:raise ValueError('wrong cut knots')
  for q in row['conforming_loop']:
   f=s['faces'][q['source_face']];bc=q['barycentric']
   if len(bc)!=3 or not all(math.isfinite(v)for v in bc)or min(bc)<-1e-9 or abs(sum(bc)-1)>1e-12:raise ValueError('bad barycentric')
   point=[sum(bc[k]*s['positions'][f[k]][j]for k in range(3))for j in range(3)]
   if max(abs(a-b)for a,b in zip(point,q['position_local_m']))>1e-12:raise ValueError('point not on claimed source face')
  if row['minimum_projected_leaf_to_skull_Y_gap_m']<=0:raise ValueError('no positive radial span')
 return True
class SourceMap(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads((P/'CONCRETE-CHART.json').read_text())
 def test_actual(self):self.assertTrue(validate(self.r))
 def test_falsely_18_conforming(self):
  r=copy.deepcopy(self.r);r['rows'][0]['conforming_piecewise_planar_cut_point_count']=18
  with self.assertRaises(ValueError):validate(r)
 def test_wrong_barycentric(self):
  r=copy.deepcopy(self.r);r['rows'][0]['conforming_loop'][0]['barycentric']=[1.1,-.1,0]
  with self.assertRaises(ValueError):validate(r)
 def test_wrong_source_face(self):
  r=copy.deepcopy(self.r);r['rows'][0]['conforming_loop'][0]['source_face']=80
  with self.assertRaises(ValueError):validate(r)
 def test_wrong_point(self):
  r=copy.deepcopy(self.r);r['rows'][0]['conforming_loop'][0]['position_local_m'][1]+=.001
  with self.assertRaises(ValueError):validate(r)
 def test_wrong_frozen_input(self):
  r=copy.deepcopy(self.r);r['input090_sha256']='0'*64
  with self.assertRaises(ValueError):validate(r)
if __name__=='__main__':unittest.main()
