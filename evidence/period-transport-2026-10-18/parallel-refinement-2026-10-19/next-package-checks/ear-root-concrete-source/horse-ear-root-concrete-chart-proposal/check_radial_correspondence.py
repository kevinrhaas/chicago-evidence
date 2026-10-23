# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import json,numpy as np
P=Path(__file__).parent;r=json.loads((P/'CONCRETE-CHART.json').read_text());rows=[]
for row in r['rows']:
 focus=np.array(row['projection_focus_actual_ring1_centroid_m']);leaf=np.array([q['leaf_point_local_m']for q in row['original_18_projected_points']]);ratios=[];errors=[];gaps=[]
 for q in row['conforming_loop']:
  if 'ear_boundary_corner'in q:target=leaf[q['ear_boundary_corner']]
  else:
   i=q['ear_edge'];t=q['ear_edge_fraction'];target=(1-t)*leaf[i]+t*leaf[(i+1)%18]
  cut=np.array(q['position_local_m']);rho=(cut[1]-focus[1])/(target[1]-focus[1]);err=float(np.linalg.norm(cut-(focus+rho*(target-focus))));assert 0<rho<1 and err<1e-12;ratios.append(float(rho));errors.append(err);gaps.append(float(target[1]-cut[1]))
 rows.append({'side':row['side'],'all22knots_radial_ordered':True,'rho_min':min(ratios),'rho_max':max(ratios),'radial_reconstruction_max_error_m':max(errors),'minimum_leaf_to_cut_Y_span_over_all22knots_m':min(gaps)})
(P/'RADIAL-CHECKS.json').write_text(json.dumps({'source_only':True,'rows':rows,'scope':'Actual22cut knots correspond to original18edge leaf loop; proves endpoint radial ordering, not triangulated or posed embedding.'},indent=2)+'\n');print(rows)
