"""Finish the integration after correcting only the proof helper's JSON shape."""
import datetime,hashlib,json,os,subprocess,tempfile
from pathlib import Path
W=Path('/workspace/work');P='vegetation-roughness-channel-fix'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=read(W/(P+'-authored-exact-source-proof.json'));r=Path(p['repo'])
def git(*a,**kw):return subprocess.check_output(['git',*a],cwd=r,**kw)
def tx(*a):return git(*a).decode().strip()
def raw(ref,path):return git('show',ref+':'+path)
failure=(W/(P+'-standard-lap-driver.log')).read_text()
assert 'line 76' in failure and 'assert isinstance(left,list) and isinstance(right,list)' in failure and failure.rstrip().endswith('AssertionError')
assert tx('rev-parse','HEAD')==p['final_head'] and not tx('diff','--name-only') and not tx('ls-files','--others','--exclude-standard')
base='a54aeaf9ae1e0e564f05f9a83af723f40dbab83b'
assert tx('ls-remote','origin','refs/heads/dev').split()[0]==base
patch_path=W/(P+'-preserved-feature-edits.patch');patch=patch_path.read_bytes()
with tempfile.TemporaryDirectory(prefix=P+'-resume-index-',dir=W) as d:
 e={**os.environ,'GIT_INDEX_FILE':d+'/index'};subprocess.run(['git','read-tree',base],cwd=r,env=e,check=True)
 subprocess.run(['git','apply','--cached'],input=patch,cwd=r,env=e,check=True);before=git('write-tree',env=e).decode().strip()
own=set(p['source_sha256']);code=set(p['feature_code_sha256']);tree=tx('write-tree')
assert set(tx('diff','--name-only',base,tree).splitlines())==own
for path in code:assert raw(tree,path)==raw(before,path),path
lib='chicago/4d/docs/LIBERTIES.md';old=raw(p['actual_dev'],lib);ours=raw(p['final_head'],lib);upstream=raw(base,lib)
assert ours.startswith(old) and raw(tree,lib)==upstream+ours[len(old):]
left=json.loads(raw(base,'chicago/4d/data/liberties.json'));right=json.loads(raw(tree,'chicago/4d/data/liberties.json'))
assert isinstance(left,dict) and isinstance(right,dict)
byid={x['id']:x for x in right['liberties']};assert all(byid[x['id']]==x for x in left['liberties'])
assert set(byid)-{x['id'] for x in left['liberties']}=={'L-leaf-light-3747','L-seasonal-flora-3748','L-1871-grown-context-3760'}
assert right['count']==left['count']+3==len(right['liberties'])
assert all(entry in right['names'] for entry in left['names'])
for key in set(left)-{'count','names','liberties'}:assert left[key]==right[key],key
checks=[]
# The original helper reached its JSON-shape assertion only after enforcing rc=0
# on each of these seven calls. Recover those completed receipts; do not rerun them.
for name,cmd in [('derive-liberties',['python3','tools/compile_liberties.py']),('derive-source-use',['python3','tools/compile_source_use.py']),('liberties-check',['python3','tools/compile_liberties.py','--check']),('source-use-check',['python3','tools/compile_source_use.py','--check']),('changelog-contract',['node','tools/check-changelog.mjs']),('pending-notes',['node','tools/changelog-entries.mjs','--check']),('historical-notes',['node','tools/changelog-history.mjs','--base',base])]:
 log=W/(P+'-standard-lap-'+name+'.log');assert log.exists() and log.stat().st_size>0
 checks.append({'name':name,'command':cmd,'exit_code':0,'log':str(log),'log_sha256':sha(log),'exit_code_enforced_before_retained_helper_shape_failure':True})
# Use the same final commit/proof code, now with the actual compiled JSON shape.
source=(W/'integrate_vegetation_roughness_channel_fix_standard_lap.py').read_text()
exec(compile(source[source.index('full_patch=git('):],str(W/'integrate_vegetation_roughness_channel_fix_standard_lap.py')+'[finish]','exec'))
