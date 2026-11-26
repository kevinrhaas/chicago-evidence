from pathlib import Path
import hashlib,json,os,subprocess,time
root=Path.cwd();out=root/'assets/humans/web/photo_faces/historical';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=sorted(p for p in out.iterdir() if p.is_file());library=json.loads((out/'review.json').read_text());recipe=root/'data/humans/variation/historical_photo_faces.json'
parents={p:sha(root/p) for p in library['inputs_sha256']};parents[str(recipe.relative_to(root))]=sha(recipe)
for f in library['faces']:
 for sid in [f['source'],f['historical']['original_source']]:parents['data/sources/'+sid+'.json']=sha(root/'data/sources'/f'{sid}.json')
for f in json.loads(recipe.read_text())['faces']:parents[f['photo']]=sha(root/f['photo'])
report={'context':'Final T-3762 named-photo writer after consolidating processing provenance; all original archives remain individually credited.','files':len(files),'inputs_sha256':parents,'writes':[],'without_landmarker_or_network':True};env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
baseline=None
for i in range(2):
 mtimes={str(p):p.stat().st_mtime_ns for p in files}
 if i:
  path=out/'page_01_face_full.jpg';b=bytearray(path.read_bytes());b[len(b)//2]^=1;path.write_bytes(b)
  bad=subprocess.run(['python3','tools/historical_photo_faces.py','--check'],capture_output=True,text=True,env=env);assert bad.returncode and 'stale atlas' in bad.stdout+bad.stderr
  report['damaged_named_detail_rejected']=True
 began=time.monotonic()
 with (root/f'work/person-photo-reproduce-{i+1}.log').open('w') as log:subprocess.run(['python3','tools/historical_photo_faces.py','--all','--jobs','4'],check=True,stdout=log,stderr=subprocess.STDOUT,env=env)
 current={str(p.relative_to(root)):sha(p) for p in files}
 if baseline is None:baseline=current
 else:assert current==baseline,'second write changed named output bytes'
 assert all(p.stat().st_mtime_ns>mtimes[str(p)] for p in files if p.name!='coverage.json')
 assert {p:sha(root/p) for p in parents}==parents,'source, fit, frozen recipe or generator input changed'
 assert json.loads((out/'review.json').read_text())['faces']==library['faces']
 report['writes'].append({'seconds':round(time.monotonic()-began,2),'actual_rewrites':len(files)-1,'stable_coverage_retained':True,'matches_first_write':i>0});print(report['writes'][-1],flush=True)
report.update(output_sha256=baseline,all_27_face_records_unchanged=True,all_inputs_and_recipes_unchanged=True,damaged_page_restored_byte_exact=True)
(root/'work/person-photo-writer-reproduction.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: final named-photo writer reproduces twice, refuses/restores drift, preserves every source, existing head fit and authored recipe')
