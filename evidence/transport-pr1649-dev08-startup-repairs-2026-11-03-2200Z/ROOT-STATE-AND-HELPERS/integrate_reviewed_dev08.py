"""Normal, uncommitted integration of the reviewed DEV08 source; never commits/pushes."""
from pathlib import Path
import datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
P=Path(__file__).resolve().parent
R=Path('/workspace/chicago-transport-current-20261103')
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
INCOMING='08d3f3d7c85545013eaca18a9d256fe63a8e17e0'
HEAD='5439723317fbb6491e837911243f2f62fb35065b'
O=P/'actual-dev08-normal-integration-01'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false','-C',str(R),*a],timeout=30)
assert not O.exists()
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert not git('status','--porcelain','--untracked-files=no').strip()
assert not git('ls-files','-u').strip()
assert subprocess.run(['git','-C',str(R),'rev-parse','--verify','-q','MERGE_HEAD'],stdout=subprocess.DEVNULL).returncode==1
assert digest(SUP)=='a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
assert digest(P/'RESTORED-RUNTIME-BASELINE.json')=='3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('guard',P/'resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
before=guard.snapshot();assert guard.check(before)['accepted'];O.mkdir()
state={'status':'ACTIVE_UNCOMMITTED_INTEGRATION_NOT_GATE_PASS','opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HEAD':HEAD,'incoming':INCOMING,'before_TREE':git('rev-parse','HEAD^{tree}').decode().strip(),'before_semantic_index_sha256':hashlib.sha256(git('ls-files','--stage','-z')).hexdigest(),'ledger':[]}
save(O/'STATE.json',state)
def run(label,args,expected):
 prefix=O/label
 with Path(str(prefix)+'.stdout').open('xb')as f:
  q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(R),'--timeout','120','--',*args],stdout=f,stderr=subprocess.STDOUT)
 result=json.loads(Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text())
 state['ledger'].append(dict(label=label,result=result,cleanup=cleanup));save(O/'STATE.json',state)
 assert q.returncode==result['returncode'] and q.returncode in expected
 assert not result['timed_out'] and result['requested_timeout_seconds']==result['effective_timeout_seconds']==120 and result['timeout_override_reason']is None
 assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']
try:
 run('fetch-dev08',['git','-c','gc.auto=0','-c','maintenance.auto=false','fetch','origin','dev'],{0})
 assert git('rev-parse','refs/remotes/origin/dev').decode().strip()==INCOMING,'DEV advanced; review it before merging'
 run('merge-dev08',['git','-c','gc.auto=0','-c','maintenance.auto=false','merge','--no-commit','--no-ff',INCOMING],{0,1})
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 assert git('rev-parse','MERGE_HEAD').decode().strip()==INCOMING
 state.update(status='NORMAL_DEV08_INTEGRATION_PENDING_RESOLUTION_OWNERS_AND_GATE',unmerged=git('ls-files','-u').decode(),tracked_status=git('status','--porcelain','--untracked-files=no').decode())
except BaseException as e:
 state.update(status='INTEGRATION_NONPASS_NO_AUTOMATIC_RETRY',error=repr(e));raise
finally:
 state.update(closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),resources=guard.pair(before,guard.snapshot()),HEAD_after=git('rev-parse','HEAD').decode().strip())
 save(O/'STATE.json',state);save(O/'CLOSED.json',state)
print(json.dumps({'status':state['status'],'receipt':str(O/'CLOSED.json')}),flush=True)
