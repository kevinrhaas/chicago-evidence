# Read-only source guard for the staged W candidate; no Git writes or truncation.
from pathlib import Path
import subprocess,json,hashlib
r=Path('/tmp/chicago-wagon-20261029');p=Path(__file__).resolve().parent
b=json.loads((p/'SEALED-STAGED-FIVE-PATH-CANDIDATE.json').read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=r)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert git('rev-parse','HEAD').decode().strip()==b['HEAD']
assert git('rev-parse',b['TREE']+':chicago/4d').decode().strip()==b['APP']
assert not (r/'.git/MERGE_HEAD').exists()
assert git('ls-files','--stage','-z')==(p/'STAGED-COMPLETE-INDEX.z').read_bytes()
assert not git('diff','--name-only').strip()
assert not git('ls-files','--others','--exclude-standard').strip()
for row in b['paths']+b['protected_checked_paths']:
 f=r/row['path'];assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],row['path']
assert sha(p/'observe-native-railway-lifecycle.mjs')==b['observer_sha256']
print(json.dumps({'source_freeze':'PASS','HEAD':b['HEAD'],'TREE':b['TREE'],'APP':b['APP'],'source_paths':len(b['paths'])+len(b['protected_checked_paths']),'complete_index_exact':True}))
