"""Qualify the People-tab fix and verify existing native reports, without committing.

No data/liberty inputs changed: native --check confirms their fresh expected
outputs without repeating the already successful writers.
"""
from pathlib import Path
import fcntl,hashlib,importlib.util,json,os,subprocess,sys,datetime
P=Path(__file__).resolve().parent;R=Path('/workspace/chicago-transport-current-20261103');A=R/'chicago/4d'
O=P/'actual-dev08-startup-targeted-and-owners-03';SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
HEAD='5439723317fbb6491e837911243f2f62fb35065b';BASE='08d3f3d7c85545013eaca18a9d256fe63a8e17e0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git','-C',str(R),*a],timeout=30)
assert not O.exists()
assert git('rev-parse','HEAD').decode().strip()==HEAD and git('rev-parse','MERGE_HEAD').decode().strip()==BASE
assert not git('ls-files','-u').strip()
assert sha(SUP)=='a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
assert sha(P/'RESTORED-RUNTIME-BASELINE.json')=='3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('guard',P/'resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
before=guard.snapshot();assert guard.check(before)['accepted'];O.mkdir()
fixes=json.loads((P/'DEV08-ALL-ELEVEN-FINAL-FIXES.json').read_text())['files']
assert all(sha(R/p)==h for p,h in fixes.items())
git('add','--',*fixes)
assert not git('diff','--name-only').strip()
original_index=git('write-tree').decode().strip()
allowed={'chicago/4d/data/liberties.json','chicago/4d/docs/measurements/source_use_coverage.md'}
body=(R/'.github/workflows/chicago-4d-bake.yml').read_text();q=body.index('      - id: q\n');start=body.index('        run: |\n',q)+len('        run: |\n');lines=[]
for line in body[start:].splitlines():
 if line and not line.startswith('          '):break
 lines.append(line[10:]if line else '')
script=O/'actual-warranted-q.sh';script.write_text('\n'.join(lines)+'\n');assert 'sparse-checkout' in script.read_text()
state={'status':'ACTIVE_TARGETED_AND_OWNERS_NOT_FULL_GATE','HEAD':HEAD,'MERGE_HEAD':BASE,'TREE_before_native_owners':original_index,'fix_pins':fixes,'ledger':[],'opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};save(O/'STATE.json',state)
def source_stable():
 assert git('rev-parse','HEAD').decode().strip()==HEAD and git('rev-parse','MERGE_HEAD').decode().strip()==BASE
 assert all(sha(R/p)==h for p,h in fixes.items())
 assert set(git('diff','--name-only').decode().splitlines())<=allowed
def run(name,cmd,cap):
 source_stable();prefix=O/name;snap=guard.snapshot();assert guard.check(snap)['accepted']
 with Path(str(prefix)+'.stdout').open('xb')as f:
  q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(A),'--timeout',str(cap),'--',*cmd],stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 result=json.loads(Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text());resources=guard.pair(snap,guard.snapshot())
 row=dict(name=name,command=cmd,result=result,cleanup=cleanup,resources=resources);state['ledger'].append(row);save(O/'STATE.json',state)
 assert q.returncode==result['returncode']==0 and not result['timed_out']
 assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==cap and result['timeout_override_reason']is None
 assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted'];source_stable()
try:
 run('workflow-shell-syntax',['bash','-n',str(script)],5)
 run('workflow-native-shape',['python3','-c',"import sys;sys.path.insert(0,'tools');import bake_warranted as b;assert not b.workflow_shape_changed(base='"+BASE+"')"],5)
 run('transport-loop',['node','tools/test_transport_loop.mjs'],5)
 run('driven-assembly',['node','tools/test_driven_assembly.mjs'],5)
 run('main-source-syntax',['node','--check','renderers/web/js/main.js'],5)
 run('navigator',['node','tools/test_navigator.mjs'],5)
 run('bake-warranted-self-test',['python3','tools/bake_warranted.py','--self-test'],120)
 run('check-liberties',['python3','tools/compile_liberties.py','--check'],120)
 run('check-source-use',['python3','tools/compile_source_use.py','--check'],120)
 git('add','--',*sorted(allowed));assert not git('diff','--name-only').strip()
 tree=git('write-tree').decode().strip()
 state.update(status='TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT',source_after={'HEAD':HEAD,'MERGE_HEAD':BASE,'TREE':tree,'APP':git('rev-parse',tree+':chicago/4d').decode().strip(),'semantic_index_sha256':hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()})
except BaseException as e:
 state.update(status='TARGETED_OR_OWNERS_NONPASS_NO_AUTOMATIC_RETRY',error=repr(e));raise
finally:
 state.update(closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),resources=guard.pair(before,guard.snapshot()));save(O/'STATE.json',state);save(O/'CLOSED.json',state)
print(json.dumps({'status':state['status'],'receipt':str(O/'CLOSED.json')}),flush=True)
