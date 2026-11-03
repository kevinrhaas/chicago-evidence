"""Exact staged-source diagnostic only; no checked-commit/delivery qualification."""
from pathlib import Path
import argparse,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys
P=Path(__file__).resolve().parent;RUNTIME=P.parents[1]
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
APP='c8f78fbe675db8d3ca1d6907b79aef13e46dd6e9'
FIELDS=['HEAD','MERGE_HEAD','TREE','APP','semantic_index_sha256']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=30)
def staged_source(repo,expected):
 assert set(expected)==set(FIELDS) and expected['APP']==APP
 for k in ['HEAD','MERGE_HEAD','TREE','APP']:assert re.fullmatch('[a-f0-9]{40}',expected[k])
 assert not git(repo,'ls-files','-u').strip() and not git(repo,'diff','--name-only').strip(),'No unmerged/unstaged tracked source permitted'
 assert not git(repo,'ls-files','--others','--exclude-standard').strip(),'Unexpected untracked source'
 assert git(repo,'rev-parse','HEAD').decode().strip()==expected['HEAD']
 assert git(repo,'rev-parse','MERGE_HEAD').decode().strip()==expected['MERGE_HEAD']
 assert git(repo,'rev-parse',expected['TREE']+'^{tree}').decode().strip()==expected['TREE']
 assert git(repo,'rev-parse',expected['TREE']+':chicago/4d').decode().strip()==expected['APP']
 raw=git(repo,'ls-files','--stage','-z');assert hashlib.sha256(raw).hexdigest()==expected['semantic_index_sha256']
 # Read the existing ROOT-approved tree object; never write-tree/update-index here.
 rows=[]
 for row in git(repo,'ls-tree','-r','-z',expected['TREE']).split(b'\0'):
  if row:
   info,path=row.split(b'\t',1);mode,kind,oid=info.split();rows.append((path,mode+b' '+oid+b' 0\t'+path+b'\0'))
 assert b''.join(record for path,record in sorted(rows))==raw,'Actual staged blob/mode map differs from approved TREE'
 return dict(expected)
def prepare_guard(binding):
 assert not binding['template_only'] and binding['mode']=='STAGED_DIAGNOSTIC_NOT_DELIVERY_ACCEPTANCE'
 for f in [SUP,RUNTIME/'resource_guard.py',RUNTIME/'RESTORED-RUNTIME-BASELINE.json']:assert sha(f)==binding['guard_pins'][str(f)]
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('current_staged_world_guard',RUNTIME/'resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
 return lock,guard
def valid_native(row,cap=None):
 r=row['result'];c=row['cleanup'];assert r['returncode']==0 and not r['timed_out'] and r['timeout_override_reason']is None
 assert r['requested_timeout_seconds']==r['effective_timeout_seconds']
 if cap is not None:assert r['effective_timeout_seconds']==cap
 assert c['cleanup_complete']and not c['remaining_owned_children']and row['resources']['accepted']
def targeted_owner(binding,repo,source):
 ref=binding['targeted_owner_receipt'];assert sha(ref['path'])==ref['sha256'];o=load(ref['path'])
 assert o['status']=='TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT'and o['resources']['accepted']
 old=o['source_after'];assert old['APP']==APP==source['APP']and old['HEAD']==source['HEAD']and old['MERGE_HEAD']==source['MERGE_HEAD']
 assert git(repo,'rev-parse',old['TREE']+':chicago/4d').decode().strip()==APP
 delta=git(repo,'diff','--name-only','--no-renames',old['TREE'],source['TREE']).decode().splitlines()
 assert all(p.startswith('.github/workflows/')for p in delta),'Only explicit workflow delta allowed after identicalAPP owner proof'
 for rel,pin in o['fix_pins'].items():
  if rel.startswith('chicago/4d/'):assert sha(repo/rel)==pin
 for row in o['ledger']:valid_native(row)
 return dict(path=ref['path'],sha256=ref['sha256'],source_after=old,APP_byte_identical=True,workflow_only_delta=delta,not_full_preflight=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--binding',type=Path,required=True);p.add_argument('--year',choices=['1835','1904'],required=True);p.add_argument('--viewport',choices=['desktop','mobile'],required=True);p.add_argument('--scope',choices=['A','B','C'],required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();b=load(a.binding)
 assert b['ROOT_EXPLICIT_STAGED_WORLD_SCOPE_GO']is True;R=Path(b['repo']);A=R/'chicago/4d';site=R/'site/4d';O=a.out;assert not O.exists();lock,guard=prepare_guard(b)
 before=staged_source(R,b['source']);owner=targeted_owner(b,R,before)
 pr=b['publication_receipt'];assert sha(pr['path'])==pr['sha256'];pub=load(pr['path']);assert pub['status']=='ACTUAL_STAGED_NATIVE_PUBLICATION_PASS'
 assert all(pub['source_before'][k]==pub['source_after'][k]==before[k]for k in FIELDS)and len(pub['ledger'])==2
 for row,cmd,cap in zip(pub['ledger'],[['bash','tools/publish.sh'],['node','tools/check_published.mjs']],[180,120]):valid_native(row,cap);assert row['result']['command']==cmd
 stamp=load(site/'build.json')['version'];assert stamp==before['HEAD'][:10],'Native publisher stamps oldHEAD; it is not the staged-source identity'
 rb=guard.snapshot();assert guard.check(rb)['accepted'];O.mkdir(parents=True)
 pins={str(p):sha(p)for p in (A/'renderers/web/js').rglob('*.js')}
 for folder in ['data/transport','assets/humans']:
  for f in (A/folder).rglob('*'):
   if f.is_file()and f.suffix in['.json','.glb']:pins[str(f)]=sha(f)
 for rel in ['renderers/web/index.html','renderers/web/css/walk.css','data/humans/fixture.measure.json','data/sidecars/'+a.year+'/index.json','data/sidecars/'+a.year+'/people.json','data/liberties.json','renderers/web/transport/driven/horse-current26-inplace-full.glb','renderers/web/transport/wagon-driver/wagon-w01.glb','renderers/web/transport/parked-brougham/brougham-near.glb']:pins[str(A/rel)]=sha(A/rel)
 helpers={f.name:sha(f)for f in P.iterdir()if f.suffix in['.py','.cjs']}
 cfg=dict(template_only=False,root_explicit_world_interaction_GO=True,root=str(site),output=str(O/'frames'),scene=a.year,tree='published',touch=a.viewport=='mobile',scope=a.scope,check_light=a.scope=='C',recheck_whole_route=a.scope=='A',actual_route_probe=str(P/'probe-native-world-route.cjs'),actual_source_HEAD_or_staged_TREE=before,actual_source_pins=pins,boot_ready_ms=240000,mount_ready_ms=300000,native_phase_seconds=600,native_image_sharpness='Low (1)',native_stored_boot_detail='balanced'if a.viewport=='mobile'else'full',harness_pins=helpers,diagnostic_mode=b['mode'],native_build_stamp_is_old_HEAD_only=stamp,delivery_acceptance=False)
 save(O/'ROOT-BOUND-WORLD-CONFIG.json',cfg);save(O/'SOURCE-BEFORE.json',before)
 env=dict(os.environ,PW_EXECUTABLE='/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell',PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103',PYTHONDONTWRITEBYTECODE='1');prefix=O/'world';result={};cleanup={};report={};error=None
 try:
  q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','600','--','node',str(P/'observe-one-world-case.cjs'),str(O/'ROOT-BOUND-WORLD-CONFIG.json')],env=env,stdout=(O/'world.stdout').open('xb'),stderr=subprocess.STDOUT)
  result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');rp=O/'frames/WORLD-CASE-RESULT.json';report=load(rp)if rp.exists()else{}
  passed=q.returncode==result['returncode']==0 and not result['timed_out']and result['requested_timeout_seconds']==result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')=='ACTUAL_WORLD_INTERACTION_SCOPE_PASS'and report.get('probe',{}).get('scope')==a.scope
 except BaseException as ex:passed=False;error=repr(ex)
 after=staged_source(R,b['source']);resources=guard.pair(rb,guard.snapshot());passed=passed and before==after and resources['accepted']and all(sha(P/name)==digest for name,digest in helpers.items())
 closed=dict(status='ACTUAL_STAGED_PUBLISHED_SCOPE_PASS'if passed else'ACTUAL_STAGED_PUBLISHED_SCOPE_NONPASS',mode=b['mode'],scene=a.year,viewport=a.viewport,scope=a.scope,predicate_ids=report.get('probe',{}).get('predicate_ids',[]),source_before=before,source_after=after,targeted_owner_APP_bridge=owner,publication_receipt=pr,native_build_stamp_old_HEAD_only=stamp,harness_pins=helpers,result=result,cleanup=cleanup,resources=resources,native_report=str(O/'frames/WORLD-CASE-RESULT.json'),failure=error,full_all4_commit_CI_DEV_delivery_or_photo_qualification=False)
 save(O/'CLOSED.json',closed);print(json.dumps({'status':closed['status'],'receipt':str(O/'CLOSED.json')}));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
