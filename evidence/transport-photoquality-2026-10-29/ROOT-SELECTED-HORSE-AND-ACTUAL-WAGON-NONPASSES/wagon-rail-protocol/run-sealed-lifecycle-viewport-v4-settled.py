# Outside-app full source/index/mirror guards around the approved native observer adapter.
from pathlib import Path
import subprocess,sys,json,hashlib,time
b=Path(__file__).resolve().parent.parent;p=b/'MEMORY-FOLLOWUP-PREP';m=Path('/tmp/chicago-wagon-20261029/site/4d')
assert len(sys.argv)==3 and sys.argv[1] in ('desktop','mobile')
vp,name=sys.argv[1:];out=b/name;assert not out.exists()
expected=json.loads((b/'RAIL-CANDIDATE-FULL-MIRROR-BEFORE-BROWSER-01.json').read_text())
def guard():
 subprocess.run([sys.executable,str(p/'check-staged-source-freeze.py')],check=True)
 rows=[{'path':f.relative_to(m).as_posix(),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(m.rglob('*')) if f.is_file()]
 assert rows==expected,'Full published mirror changed'
 return len(rows)
assert guard()==5630
start=time.monotonic();rc=1
try:
 rc=subprocess.run([sys.executable,str(p/'run-owned-lifecycle-viewport-v4-settled.py'),vp,str(out)],cwd='/tmp/chicago-wagon-20261029/chicago/4d').returncode
finally:
 count=guard()
 (b/(name+'-GUARD-CLOSED.json')).write_text(json.dumps({'viewport':vp,'returncode':rc,'seconds':time.monotonic()-start,'source_paths':53,'complete_semantic_index_exact':True,'published_mirror_files':count,'full_mirror_before_after_exact':True,'observer_sha256':hashlib.sha256((p/'observe-native-railway-lifecycle-v4-settled.mjs').read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256((p/'run-native-railway-lifecycle-v4-settled.cjs').read_bytes()).hexdigest()},indent=2)+'\n')
sys.exit(rc)
