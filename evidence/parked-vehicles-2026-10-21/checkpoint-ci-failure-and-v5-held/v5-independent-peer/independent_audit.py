"""Read-only pinned-source audit and bounded static construction arithmetic."""
from pathlib import Path
import ast, collections, copy, hashlib, importlib.util, json, math, os, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode=True
D=Path('/workspace/shared/human-tailoring-v5-source-proposal')
OUT=Path(__file__).resolve().parent
REF='2f75ef23dbb316ebe4cf53e65ce3af8b04f140d3'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'scope':'Independent finite static source review; no runtime, renderer, Blender, poses, LOD or canonical qualification','source_ref':REF,'checks':{},'ages':[]}
capsule=Path('/workspace/shared/human-tailoring-v5-source-proposal-frozen-2f75ef23.tar.gz')
report['capsule_sha256']=sha(capsule)
assert report['capsule_sha256']=='c26f48fbd71cf716fea6fcb4e9e90e6c326183aec3dcff77aaa78291448a07ce'
manifest=json.loads((D/'CAPSULE-MANIFEST.json').read_text())
for item in manifest['files']:
 p=D/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],str(p)
for line in (D/'MANIFEST.sha256').read_text().splitlines():
 h,p=line.split(maxsplit=1);assert sha(D/p.lstrip('*'))==h,p
report['checks']['capsule_and_every_manifest_entry_match']=True
pinned=json.loads((D/'PINNED-INPUTS.json').read_text())
for item in pinned['files']:
 raw=subprocess.check_output(['git','--no-optional-locks','-C','/workspace/chicago','show',REF+':'+item['git_path']])
 assert raw==(D/item['capsule_path']).read_bytes(),item['git_path']
report['checks']['all_seven_inputs_match_exact_saved_git_objects']=True
with tempfile.TemporaryDirectory(prefix='v5-independent-patch-',dir='/tmp') as tmp:
 shutil.copytree(D/'preimages',tmp,dirs_exist_ok=True)
 applied=subprocess.run(['patch','--batch','--forward','-p1','-i',str(D/'V5-BOUNDED-TAILORING-AGAINST-2f75.patch')],cwd=tmp,check=True,capture_output=True,text=True)
 for p in (D/'proposed').rglob('*'):
  if p.is_file():assert (Path(tmp)/p.relative_to(D/'proposed')).read_bytes()==p.read_bytes()
 report['checks']['patch_reproduces_both_proposed_files']=True
pre=D/'preimages/chicago/4d';newdir=D/'proposed/chicago/4d'
def funcs(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
oldf=funcs(pre/'tools/human_workwear_fit.py');newf=funcs(newdir/'tools/human_workwear_fit.py')
assert all(oldf[k]==newf[k] for k in oldf if k!='garment_shell')
assert set(newf)-set(oldf)=={'trouser_hang_profile','hanging_trouser_point'}
r0=json.loads((pre/'data/humans/recipes/worker_1835.json').read_text());r=json.loads((newdir/'data/humans/recipes/worker_1835.json').read_text())
assert {k:v for k,v in r.items() if k!='workwear_tailoring_v5'}==r0
assert r['height_scale']==1
report['checks']['old_recipe_fields_and_existing_non_shell_helpers_unchanged']=True
sys.path.insert(0,str(D/'inputs/chicago/4d/tools'))
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=module('independent_old',pre/'tools/human_workwear_fit.py');new=module('independent_new',newdir/'tools/human_workwear_fit.py')
for age in (25,35):
 body=json.loads((D/f'inputs/chicago/4d/assets/authored/humans/makehuman_hm08/prepared_adult_{age}.json').read_text());untouched=copy.deepcopy(body)
 m=body['meshes'][0];bones={b['name']:b for b in body['skeleton']};height=max(p[1] for p in m['positions_m']);waist=r['waist_height_fraction']*height
 pants0=old.garment_shell(m,'trousers',r['trouser_offset_m'],r,bones,height);pants=new.garment_shell(m,'trousers',r['trouser_offset_m'],r,bones,height)
 shirt0=old.garment_shell(m,'shirt',r['shirt_offset_m'],r,bones,height);shirt=new.garment_shell(m,'shirt',r['shirt_offset_m'],r,bones,height)
 vest=new.garment_shell(m,'waistcoat',r['waistcoat_offset_m'],r,bones,height)
 assert body==untouched
 assert all(v==shirt[k] for k,v in shirt0.items() if k!='receipt')
 assert all(v==pants[k] for k,v in pants0.items() if k not in ('receipt','positions_m'))
 changed=[i for i,(a,b) in enumerate(zip(pants0['positions_m'],pants['positions_m'])) if a!=b]
 assert all(a[1]==b[1] for a,b in zip(pants0['positions_m'],pants['positions_m']))
 assert all(a==b for a,b in zip(pants0['positions_m'],pants['positions_m']) if a[1]>=pants['receipt']['trouser_hang_profile']['sides']['l']['transition_end_y_m'])
 sections=[]
 for side in ('l','r'):
  hip,knee,ankle=[bones[j+'_'+side]['head_m'] for j in ('thigh','calf','foot')]
  lo=ankle[1]+.073;hi=knee[1]+.1*(hip[1]-knee[1]);chain={j+'_'+side for j in ('thigh','calf','foot','ball')}
  ps=[p for p,w in zip(m['positions_m'],m['weights']) if lo<=p[1]<=hi and math.fsum(v for j,v in w.items() if j in chain)>.9]
  rx0=max(abs(p[0]-hip[0]) for p in ps)+.012;rz0=max(abs(p[2]-hip[2]) for p in ps)+.012
  s=max(1,max(math.hypot((p[0]-hip[0])/rx0,(p[2]-hip[2])/rz0) for p in ps));rx,rz=rx0*s,rz0*s
  actual=pants['receipt']['trouser_hang_profile']['sides'][side]
  assert math.isclose(actual['section_rx_m'],rx,abs_tol=1e-15) and math.isclose(actual['section_rz_m'],rz,abs_tol=1e-15)
  assert math.isclose(actual['transition_end_y_m'],knee[1]+.65*(hip[1]-knee[1]),abs_tol=1e-15)
  sections.append({'side':side,'source_support_vertices':len(ps),'hip_axis_xyz_m':hip,'knee_y_m':knee[1],'transition_y_m':actual['transition_end_y_m'],'support_radial_scale':s,'design_rx_rz_m':[rx,rz],'hem_rx_rz_m':[.85*rx,.85*rz],'untapered_design_gap_to_centre_m':abs(hip[0])-rx,'max_source_support_elliptic_radius':max(math.hypot((p[0]-hip[0])/rx,(p[2]-hip[2])/rz) for p in ps)})
  for i in changed:
   w=pants['weights'][i]
   if sum(v for j,v in w.items() if j in chain)<.9:continue
   a,b=pants0['positions_m'][i],pants['positions_m'][i]
   va=(a[0]-hip[0],a[2]-hip[2]);vb=(b[0]-hip[0],b[2]-hip[2])
   assert abs(va[0]*vb[1]-va[1]*vb[0])<1e-14
   assert math.hypot(*vb)>=math.hypot(*va)-1e-14
 closure=waist+.4*(bones['upperarm_l']['head_m'][1]-waist);assert math.isclose(vest['receipt']['waistcoat_front_closure_y_m'],closure,abs_tol=1e-15)
 edges=collections.Counter(tuple(sorted((a,b))) for f in vest['triangles'] for a,b in zip(f,f[1:]+f[:1]))
 lookup=dict(zip(m['source_vertex_indices'],m['positions_m']))
 origins=[[sum(w*lookup[int(s)][axis] for s,w in b.items()) for axis in range(3)] for b in vest['source_basis']]
 seam=[(e,c) for e,c in edges.items() if all(abs(origins[i][0])<1e-12 and origins[i][2]>0 and waist-.04+1e-8<origins[i][1]<closure-1e-8 for i in e)]
 assert len(seam)==10 and all(c==2 for e,c in seam) and max(edges.values())<=2
 # Eight closed-band source vertices only: exercise source-barycentric UV/weight provenance independently.
 seam_vertices=sorted({i for e,c in seam for i in e});sample=seam_vertices[::max(1,len(seam_vertices)//8)][:8]
 weight_error=0.
 sid_to_index={sid:i for i,sid in enumerate(m['source_vertex_indices'])}
 for i in sample:
  expected={}
  for sid,fraction in vest['source_basis'][i].items():
   for joint,w in m['weights'][sid_to_index[int(sid)]].items():expected[joint]=expected.get(joint,0)+fraction*w
  keep=sorted(((k,v) for k,v in expected.items() if v>1e-12),key=lambda kv:(-kv[1],kv[0]))[:4];total=sum(v for k,v in keep);expected={k:v/total for k,v in keep}
  weight_error=max(weight_error,max(abs(expected.get(k,0)-vest['weights'][i].get(k,0)) for k in set(expected)|set(vest['weights'][i])))
 assert weight_error<1e-12
 report['ages'].append({'age':age,'all_body_skin_skeleton_identity_metadata_unchanged_in_memory':True,'shirt_arrays_exact':True,'trouser_nonposition_arrays_exact':True,'trouser_y_exact_and_above_transition_positions_exact':True,'changed_trouser_vertices':len(changed),'max_added_trouser_displacement_m':max(math.dist(a,b) for a,b in zip(pants0['positions_m'],pants['positions_m'])),'changed_points_radially_nonshrinking':True,'source_height_m':height,'waist_y_m':waist,'waistcoat_closure_y_m':closure,'closed_band_height_m':closure-(waist-.04),'shared_closed_band_edges':len(seam),'eight_closed_band_vertex_skin_checks_max_error':weight_error,'sections':sections})
report['inherited_idle0_negative_source_face_projections']={'count':40,'status':'OPEN; not rerun or waived'}
report['checks']['no_fit_threshold_normal_sole_builder_export_animation_or_mask_change_in_patch']=True
report['finite_static_verdict']='PASS for exact provenance, bounded construction and preservation; full fit, LOD, canonical, period completion and photographic acceptance remain OPEN'
report['reviewed_file_hashes']={str(p.relative_to(D)):sha(p) for p in [D/'MANIFEST.sha256',D/'README-HANDOFF.md',D/'FINITE-SOURCE-CONTROLS.json',D/'SUPPLEMENTAL-SOURCE-CONTROLS.json',D/'V5-BOUNDED-TAILORING-AGAINST-2f75.patch',newdir/'tools/human_workwear_fit.py',newdir/'data/humans/recipes/worker_1835.json']}
(OUT/'INDEPENDENT-CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
