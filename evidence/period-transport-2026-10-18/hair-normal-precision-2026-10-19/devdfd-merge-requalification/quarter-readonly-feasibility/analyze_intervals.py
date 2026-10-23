# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only existing rest arrays; analytic intervals, NO candidate evaluation."""
from pathlib import Path
import sys,json,hashlib,math
sys.path.insert(0,'/workspace/shared/horse-neck-complete-scope-capture-owned-source-next')
from glb_data import parse,read
SOURCE=Path('/workspace/shared/horse-ear-root-exporter-source-reviewed-next/export-trial1/equine_ear_root_candidate.glb')
WANT='26027c225b0c2f3c6ed72543cb2e80238196a86815b7bb910744cbc65cb23ed3'
raw=SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=WANT:raise ValueError('Exact parent pin mismatch')
d,b=parse(raw);m=d['meshes'][0];p=m['primitives'][0]
if m['name']!='skinned_equine_coat'or p['material']!=0:raise ValueError('Source coat identity')
a=read(d,b,p['attributes']['POSITION']).astype(float);rows=[]
for i in range(24):
 O=a[192+i];Q=a[216+i];H=a[1049+i];u=Q-O;v=H-Q;dot=float(u@v);den=float(v@v)
 if not math.isfinite(dot)or den<=0:raise ValueError('Degenerate analytic input')
 upper=2*dot/den
 rows.append({'sample':i,'source_indices':{'old_neck_band':192+i,'neck_portal':216+i,'head_band':1049+i,'head_source_portal':i,'head_source_band':24+i},'O':O.tolist(),'Q':Q.tolist(),'H':H.tolist(),'dot_QminusO_HminusQ_m2':dot,'head_column_squared_m2':den,'lambda_upper_from_original_movement_guard':upper,'positive_feasible':upper>0,'interval_with_explicit_half_bound':{'lower_exclusive':0,'upper_inclusive':min(.5,upper)}if upper>0 else None,'quarter_satisfies_interval':upper>=.25})
report={'status':'READ-ONLY analytic feasibility; no newcandidate positions computed','input_glb_sha256':WANT,'formula':'|Q-lambda*(H-Q)-O|^2 <= |Q-O|^2; lambda>0 gives lambda <=2dot(Q-O,H-Q)/|H-Q|^2','rows':rows,'columns_without_any_positive_lambda':[r['sample']for r in rows if not r['positive_feasible']],'quarter_infeasible_columns':[r['sample']for r in rows if not r['quarter_satisfies_interval']],'all24_positive_solution_exists':all(r['positive_feasible']for r in rows),'no_candidate_or_lambda_sweep':True}
Path(__file__).with_name('analytic-intervals.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'upper_bounds':[r['lambda_upper_from_original_movement_guard']for r in rows],'no_positive':report['columns_without_any_positive_lambda'],'quarter_fail':report['quarter_infeasible_columns']},indent=2))
