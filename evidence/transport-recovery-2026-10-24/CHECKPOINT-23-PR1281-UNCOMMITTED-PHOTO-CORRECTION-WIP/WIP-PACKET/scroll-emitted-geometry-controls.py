#!/usr/bin/env python3
"""Bounded target proof: emit only Wheeler's balcony rail/panel, never a house/GLB."""
import copy,hashlib,json,math,pathlib,sys,time
START=time.monotonic();R=pathlib.Path('/workspace/chicago-resume-1281');A=R/'chicago/4d';O=pathlib.Path(__file__).parent
sys.path.insert(0,str(A/'generators'))
from archetypes import k08_bays as K8
from archetypes import k01_frontage_params as KP
record=json.loads((A/'data/structures/wheeler_house_1812_prairie.json').read_bytes())
params=KP.from_phase(record['phases'][0],record)
v=next(b['variant'] for b in params.bays if b['variant'].get('balcony',{}).get('panel'))
bay=K8.Bay(v,K8.load(),'full');flat=K8.strip('T3113-targeted-balcony-only')
actual=[];guard=K8._check_balcony_scroll_geometry
def capture(iron,panel,rails,clearance=.01):
 snapshot={'iron':copy.deepcopy(iron),'panel':copy.deepcopy(panel),'rails':copy.deepcopy(rails),'clearance':clearance}
 actual.append(snapshot);guard(iron,panel,rails,clearance)
K8._check_balcony_scroll_geometry=capture
try:
 i=v['balcony']['panel']['run'];bay._balcony(flat,bay.runs[i],0.0,K8.part(v,bay.data,'eaves')['overhang_m'],first=i==0,idx=i)
finally:K8._check_balcony_scroll_geometry=guard
assert len(actual)==2,'Both actual scrolls must have emitted and reached their guard'
checks=[]
for i,s in enumerate(actual):
 guard(s['iron'],s['panel'],s['rails'],s['clearance']);checks.append({'scroll':i,'case':'actual-emitted-candidate','accepted':True,'vertices':len(s['iron'])})
 # Mutate actual emitted snapshots; no placement/radius/clearance formula is reproduced.
 hi=[max(p[k] for p in s['panel']) for k in range(3)]
 top=max(p[1] for p in s['iron']);topmask=[abs(p[1]-top)<1e-9 for p in s['iron']]
 cases={
  'intersecting-body':[(p[0],p[1],hi[2]-.005) if p[1]<=hi[1] else p for p in s['iron']],
  'detached-tail':[(p[0],p[1],p[2]+.25) if is_top else p for p,is_top in zip(s['iron'],topmask)],
  'low-return-tail':[(p[0],hi[1]-.02,p[2]) if is_top else p for p,is_top in zip(s['iron'],topmask)],
 }
 for label,iron in cases.items():
  try:guard(iron,s['panel'],s['rails'],s['clearance'])
  except ValueError as e:checks.append({'scroll':i,'case':label,'rejected':True,'reason':str(e)})
  else:raise AssertionError(f'{label} corruption was accepted for scroll{i}')
# Compare actual emitted triangle cross products to stored per-vertex normals.
iron=flat.prims['iron'];min_dot=1.0;triangles=0
for offset in range(0,len(iron.idx),3):
 ids=iron.idx[offset:offset+3];a,b,c=[iron.pos[k] for k in ids];u=[b[k]-a[k] for k in range(3)];v_=[c[k]-a[k] for k in range(3)];cross=(u[1]*v_[2]-u[2]*v_[1],u[2]*v_[0]-u[0]*v_[2],u[0]*v_[1]-u[1]*v_[0]);length=math.sqrt(sum(x*x for x in cross));assert length>1e-12,'Degenerate emitted iron triangle';n=[x/length for x in cross]
 for k in ids:
  dot=sum(n[j]*iron.nrm[k][j] for j in range(3));min_dot=min(min_dot,dot);assert dot>.999999,'Emitted iron face normal differs from actual triangle'
 triangles+=1
result={'source_generator_sha256':hashlib.sha256((A/'generators/archetypes/k08_bays.py').read_bytes()).hexdigest(),'source_record_sha256':hashlib.sha256((A/'data/structures/wheeler_house_1812_prairie.json').read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-START,'scope':'Only actual normalized Wheeler balcony rail/panel in RAM; no house/GLB export, owner, render, gate or publish. Tests mutate emitted snapshots, not constructor arithmetic.','checks':checks,'iron_triangles_checked':triangles,'min_actual_normal_dot':min_dot,'full_photo_acceptance':False,'limitations':['Conservative panel-body bounding-box clearance and actual rectangular top-rail support; not full scene collision or global manifold proof.','All-house invariance, actual exports, current photo comparisons, full ordered derivation, smoke and normal CI remain pending.']}
(O/'scroll-emitted-geometry-controls-proof.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
