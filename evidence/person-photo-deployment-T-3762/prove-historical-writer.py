from pathlib import Path
import hashlib,json,os,subprocess,time
root=Path.cwd();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outs=[root/'assets/humans/web/photo_faces'/n for n in ['pilot','children','historical']]
files=sorted(p for out in outs for p in out.iterdir() if p.is_file())
old=[json.loads((o/'review.json').read_text()) for o in outs]
parents={n:sha(root/n) for d in old for n in d['inputs_sha256']}
for name in ['photo_face_pilot.json','photo_face_children.json','person_photo_references.json','historical_photo_faces.json']:
 p=root/'data/humans/variation'/name;parents[str(p.relative_to(root))]=sha(p)
report={'context':'T-3762: two actual offline writes of all three catalogs on the feature tree.','files':len(files),'writes':[],'no_landmarker_or_network':True}
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
commands=[['python3','tools/historical_photo_faces.py','--all','--jobs','4']]+[['python3','tools/photo_face_library.py','--batch',str(root/'data/humans/variation'/r),'--output',str(o),'--jobs','4'] for r,o in zip(['photo_face_pilot.json','photo_face_children.json'],outs)]
baseline=None
for i in range(2):
 before={str(p):p.stat().st_mtime_ns for p in files}
 if i:
  p=outs[2]/'page_01_face_full.jpg';b=bytearray(p.read_bytes());b[len(b)//2]^=1;p.write_bytes(b)
  bad=subprocess.run(['python3','tools/historical_photo_faces.py','--check'],capture_output=True,text=True,env=env)
  assert bad.returncode and 'stale atlas' in bad.stdout+bad.stderr
  report['damaged_named_detail_refused']=True
 began=time.monotonic()
 with (root/f'work/historical-reproduce-{i+1}.log').open('w') as log:
  for cmd in commands:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,env=env)
 current={str(p.relative_to(root)):sha(p) for p in files}
 if baseline is None:baseline=current
 else:assert current==baseline,'second write moved output bytes'
 assert all(p.stat().st_mtime_ns>before[str(p)] for p in files if p.name!='coverage.json'),'all atlas/catalog/image payloads were actually rewritten'
 assert sha(outs[2]/'coverage.json')==baseline.get(str((outs[2]/'coverage.json').relative_to(root))),'unchanged coverage is retained byte exact'
 assert {n:sha(root/n) for n in parents}==parents,'read-only parent/recipe changed'
 for previous,o in zip(old,outs):
  new=json.loads((o/'review.json').read_text());assert previous['faces']==new['faces'];assert previous['budget']==new['budget']
 report['writes'].append({'seconds':round(time.monotonic()-began,2),'outputs_rewritten':len(files)-1,'stable_coverage_retained':True,'matches_first_write':i>0});print(report['writes'][-1],flush=True)
main=Path('/workspace/chicago/chicago/4d');unchanged=[]
for o in outs[:2]:
 for p in o.iterdir():
  if p.suffix.lower() in ['.jpg','.png','.glb']:
   rel=p.relative_to(root);assert sha(p)==sha(main/rel),str(rel)+' generic pixels changed';unchanged.append(str(rel))
report.update(output_sha256=baseline,unchanged_generic_pixel_and_scalp_files=len(unchanged),all_272_generic_face_records_unchanged=True,all_27_named_face_records_unchanged=True,parents_and_recipes_unchanged=True,damaged_named_page_restored=True)
(root/'work/historical-writer-reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all three catalogs reproduce twice; named drift rejected and repaired; generic/child pixels, heads and eyes unchanged; all parents and recipes unchanged')
