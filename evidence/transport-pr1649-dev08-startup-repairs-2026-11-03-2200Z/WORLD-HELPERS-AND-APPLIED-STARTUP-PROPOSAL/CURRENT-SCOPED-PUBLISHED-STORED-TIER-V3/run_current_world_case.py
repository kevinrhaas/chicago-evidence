"""One fresh published feature scope. Root GO only; no app/source/site writes."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
P=Path(__file__).resolve().parent;RUNTIME=P.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
p=argparse.ArgumentParser();p.add_argument('--binding',type=Path,required=True);p.add_argument('--year',choices=['1835','1904'],required=True);p.add_argument('--viewport',choices=['desktop','mobile'],required=True);p.add_argument('--scope',choices=['A','B','C'],required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();b=load(a.binding)
assert b['ROOT_EXPLICIT_WORLD_SCOPE_GO']is True and not b['template_only'];R=Path(b['repo']);A=R/'chicago/4d';site=R/'site/4d';O=a.out;assert not O.exists()
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=30)
def source():
 assert not git('status','--porcelain','--untracked-files=no').strip() and not git('ls-files','-u').strip()
 assert subprocess.run(['git','-C',str(R),'rev-parse','--verify','-q','MERGE_HEAD'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
 s=dict(HEAD=git('rev-parse','HEAD').decode().strip(),TREE=git('rev-parse','HEAD^{tree}').decode().strip(),APP=git('rev-parse','HEAD:chicago/4d').decode().strip(),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
 assert all(s[k]==v for k,v in b['source'].items()) and all(k in b['source']for k in ['HEAD','TREE','APP']);return s
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
SUP=Path('/workspace/.cloud-setup/transport-supervise.py');G=RUNTIME/'resource_guard.py';BASE=RUNTIME/'RESTORED-RUNTIME-BASELINE.json'
for f in [SUP,G,BASE]:assert sha(f)==b['guard_pins'][str(f)],'Current epoch/supervisor bytes differ'
spec=importlib.util.spec_from_file_location('current_world_guard',G);guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
before=source();receipt=b['checked_source_receipt'];assert sha(receipt['path'])==receipt['sha256'];checked=load(receipt['path'])[receipt['source_key']];assert all(checked[k]==before[k]for k in ['HEAD','TREE','APP'])
# Native publish must stamp this actual committed HEAD before the probe; no publish is run here.
assert load(site/'build.json')['version']==before['HEAD'][:10],'Publish the actual checked HEAD first'
resource_before=guard.snapshot();assert guard.check(resource_before)['accepted'];O.mkdir(parents=True)
pins={str(p):sha(p)for p in (A/'renderers/web/js').rglob('*.js')}
for folder in ['data/transport','assets/humans']:
 for f in (A/folder).rglob('*'):
  if f.is_file()and f.suffix in ['.json','.glb']:pins[str(f)]=sha(f)
for rel in ['renderers/web/index.html','renderers/web/css/walk.css','data/humans/fixture.measure.json','data/sidecars/'+a.year+'/index.json','data/sidecars/'+a.year+'/people.json','data/liberties.json','renderers/web/transport/driven/horse-current26-inplace-full.glb','renderers/web/transport/wagon-driver/wagon-w01.glb','renderers/web/transport/parked-brougham/brougham-near.glb']:
 f=A/rel;pins[str(f)]=sha(f)
helpers={f.name:sha(f)for f in P.iterdir()if f.suffix in ['.py','.cjs']}
cfg=dict(template_only=False,root_explicit_world_interaction_GO=True,root=str(site),output=str(O/'frames'),scene=a.year,tree='published',touch=a.viewport=='mobile',scope=a.scope,check_light=a.scope=='C',recheck_whole_route=a.scope=='A',actual_route_probe=str(P/'probe-native-world-route.cjs'),actual_source_HEAD_or_staged_TREE=before,actual_source_pins=pins,boot_ready_ms=240000,mount_ready_ms=300000,native_phase_seconds=600,native_image_sharpness='Low (1)', native_stored_boot_detail='balanced'if a.viewport=='mobile'else'full', native_profile_change_from_V2='Persist requested visitor tier before boot; original setDetail and Light retirement assertions retained',high_sharpness_performance_or_photo_acceptance=False,harness_pins=helpers)
save(O/'ROOT-BOUND-WORLD-CONFIG.json',cfg);save(O/'SOURCE-BEFORE.json',before)
env=dict(os.environ,PW_EXECUTABLE='/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell',PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103',PYTHONDONTWRITEBYTECODE='1');prefix=O/'world';result={};cleanup={};report={};error=None
try:
 q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','600','--','node',str(P/'observe-one-world-case.cjs'),str(O/'ROOT-BOUND-WORLD-CONFIG.json')],env=env,stdout=(O/'world.stdout').open('xb'),stderr=subprocess.STDOUT)
 result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');rp=O/'frames/WORLD-CASE-RESULT.json';report=load(rp)if rp.exists()else{}
 passed=q.returncode==result['returncode']==0 and not result['timed_out'] and result['requested_timeout_seconds']==result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')=='ACTUAL_WORLD_INTERACTION_SCOPE_PASS'and report.get('probe',{}).get('scope')==a.scope
except BaseException as ex:passed=False;error=repr(ex)
after=source();resources=guard.pair(resource_before,guard.snapshot());passed=passed and before==after and resources['accepted']and all(sha(P/name)==digest for name,digest in helpers.items())
closed=dict(status='ACTUAL_CURRENT_PUBLISHED_WORLD_SCOPE_PASS'if passed else'ACTUAL_CURRENT_PUBLISHED_WORLD_SCOPE_NONPASS',scene=a.year,viewport=a.viewport,scope=a.scope,predicate_ids=report.get('probe',{}).get('predicate_ids',[]),source_before=before,source_after=after,checked_source_receipt=receipt,guards=b['guard_pins'],result=result,cleanup=cleanup,resources=resources,harness_pins=helpers,native_report=str(O/'frames/WORLD-CASE-RESULT.json'),failure=error,all_cases_or_full_smoke_or_photo_PASS=False)
save(O/'CLOSED.json',closed);print(json.dumps({'status':closed['status'],'receipt':str(O/'CLOSED.json')}));raise SystemExit(0 if passed else 1)
