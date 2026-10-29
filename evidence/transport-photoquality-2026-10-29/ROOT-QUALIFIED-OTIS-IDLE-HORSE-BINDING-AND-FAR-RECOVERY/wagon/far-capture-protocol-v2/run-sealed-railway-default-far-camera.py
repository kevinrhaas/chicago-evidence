# Outside-app full source/index/mirror guards around the approved native observer adapter.
from pathlib import Path
import subprocess,sys,json,hashlib,time
b=Path(__file__).resolve().parent.parent;p=b/'CONTEXT-FIX-DEFAULT-FAR-CAPTURE-PREP-V2';m=Path('/tmp/chicago-wagon-20261029/site/4d')
assert len(sys.argv)==3 and sys.argv[1] in ('desktop','mobile')
pins=json.loads((p/'MANIFEST.json').read_text())
for row in pins['payloads']+pins['external_pins']:
 f=Path(row['path']) if Path(row['path']).is_absolute() else p/row['path']
 assert f.stat().st_size==row['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],row['path']
vp,name=sys.argv[1:];out=b/name;assert not out.exists()
expected=json.loads((b/'RAIL-CONTEXT-FIX-FULL-MIRROR-BEFORE-BROWSER-01.json').read_text())
def guard():
 subprocess.run([sys.executable,str(b/'CONTEXT-RESTORE-FIX-PREP-20261029/check-staged-source-freeze.py')],check=True)
 rows=[{'path':f.relative_to(m).as_posix(),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(m.rglob('*')) if f.is_file()]
 assert rows==expected,'Full published mirror changed'
 return len(rows)
assert guard()==5630
start=time.monotonic();rc=1
try:
 rc=subprocess.run([sys.executable,str(p/'run-owned-railway-default-far-camera.py'),vp,str(out)],cwd='/tmp/chicago-wagon-20261029/chicago/4d').returncode
finally:
 count=guard()
 (b/(name+'-GUARD-CLOSED.json')).write_text(json.dumps({'viewport':vp,'returncode':rc,'seconds':time.monotonic()-start,'source_paths':53,'complete_semantic_index_exact':True,'published_mirror_files':count,'full_mirror_before_after_exact':True,'observer_sha256':hashlib.sha256((p/'observe-native-railway-default-far-camera.mjs').read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256((p/'run-native-railway-default-far-camera.cjs').read_bytes()).hexdigest()},indent=2)+'\n')
sys.exit(rc)
