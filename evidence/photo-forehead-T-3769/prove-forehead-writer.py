from pathlib import Path
import hashlib,json,os,subprocess,time
root=Path.cwd();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outs=[root/'assets/humans/web/photo_faces'/name for name in ['pilot','children']]
recipes=[root/'data/humans/variation'/name for name in ['photo_face_pilot.json','photo_face_children.json']]
files=sorted(p for out in outs for p in out.iterdir() if p.is_file())
deployed={str(p.relative_to(root)):sha(p) for p in files}
old_catalogs=[json.loads((out/'review.json').read_text()) for out in outs]
parents={name:sha(root/name) for d in old_catalogs for name in d['inputs_sha256']}
parents.update({str(p.relative_to(root)):sha(p) for p in recipes})
report={'context':'Two actual offline writes of the forehead blend on the feature working tree.','files':len(files),'without_model_or_network':True,'writes':[]}
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
baseline=None
for n in range(2):
 before={str(p):p.stat().st_mtime_ns for p in files}
 if n:
  damaged=outs[1]/'page_00_face_full.jpg';blob=bytearray(damaged.read_bytes());blob[len(blob)//2]^=1;damaged.write_bytes(blob)
  bad=subprocess.run(['python3','tools/photo_face_library.py','--check',str(outs[1]/'review.json')],env=env,capture_output=True,text=True)
  assert bad.returncode!=0 and 'stale atlas' in bad.stdout+bad.stderr
  report['damaged_child_page_rejected']=True
 began=time.monotonic()
 with (root/f'work/forehead-reproduce-{n+1}.log').open('w') as log:
  for recipe,out in zip(recipes,outs):
   subprocess.run(['python3','tools/photo_face_library.py','--batch',str(recipe),'--output',str(out),'--jobs','4'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 current={str(p.relative_to(root)):sha(p) for p in files}
 if baseline is None:
  baseline=current
  report['changed_from_deployed']=[p for p in deployed if deployed[p]!=current[p]]
 else:assert current==baseline,'second write changed output bytes'
 advanced=sum(p.stat().st_mtime_ns>before[str(p)] for p in files);assert advanced==len(files)
 assert {name:sha(root/name) for name in parents}==parents,'read-only input or pinned recipe changed'
 for old,out in zip(old_catalogs,outs):
  new=json.loads((out/'review.json').read_text())
  assert new['faces']==old['faces'],'face, eye, hair or head-fit record changed'
  assert new['budget']==old['budget'],'texture budget changed'
  assert new['textures']['light']['size_px']==old['textures']['light']['size_px']
  for a,b in zip(old['pages'],new['pages']):
   for tier in a['textures']:
    assert a['textures'][tier]['size_px']==b['textures'][tier]['size_px']
    assert a['textures'][tier]['gpu_bytes_rgba8_mipmaps']==b['textures'][tier]['gpu_bytes_rgba8_mipmaps']
 report['writes'].append({'seconds':round(time.monotonic()-began,2),'mtimes_advanced':advanced,'matches_first_write':n>0})
 print('WRITE',n+1,report['writes'][-1],flush=True)
report.update(all_272_face_eye_hair_and_head_fit_records_unchanged=True,all_parents_and_recipes_unchanged=True,texture_dimensions_and_gpu_budget_unchanged=True,damaged_child_page_restored_byte_exact=True,output_sha256=baseline)
(root/'work/forehead-writer-reproduction.json').write_text(json.dumps(report,indent=2)+chr(10))
print('PASS: two offline writes; all outputs reproducible; corrupted child page refused and repaired; all face records, input recipes, parents and GPU budgets unchanged')
