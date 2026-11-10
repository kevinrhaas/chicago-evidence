#!/usr/bin/env python3
"""Read-only GitHub monitoring plus authorized local Git object-cache materialization."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import base64,datetime,hashlib,json,os,subprocess,sys,time,traceback
OUT=Path(__file__).resolve().parent;REPO=Path('/tmp/chicago-west-wicket-20261109');REMOTE='kevinrhaas/chicago';RUN=42758213227;SOURCE='b9c767997c452740c6b690cf2d280d7f75c8c9d5';BRANCH='steward/bake-'+str(RUN);BIND='27e6ea7f369349e2769dd42eb81e0fe0402892d2f6208a090ef467b2c8d29553';ENV=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def git(*args,stdin=None,check=True):return subprocess.run(['git',*args],cwd=REPO,env=ENV,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check)
def api(path,allow404=False):
 p=subprocess.run(['gh','api','repos/'+REMOTE+'/'+path],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
 if p.returncode:
  if allow404 and b'404'in p.stderr:return None
  raise RuntimeError('API read failed '+path+': '+p.stderr.decode()[-1200:])
 return json.loads(p.stdout)
def unchanged():
 assert git('rev-parse','HEAD').stdout.decode().strip()==SOURCE,'Root HEAD changed'
 assert not git('status','--porcelain').stdout,'Root tracked/untracked worktree state changed'
state={'status':'MONITORING','run_id':RUN,'expected_source':SOURCE,'expected_retained_branch':BRANCH,'observations':[],'claim_limit':'API GET only; local writes confined to external receipts and authorized Git object/ref cache. No checkout/HEAD/tracked-source change, retry dispatch or GitHub mutation.'}
try:
 unchanged();last=None
 while True:
  with ThreadPoolExecutor(max_workers=3)as pool:
   fs=[pool.submit(api,p,*a)for p,a in [('actions/runs/'+str(RUN),()),('actions/runs/'+str(RUN)+'/jobs?per_page=100',()),('git/ref/heads/'+BRANCH,(True,))]]
   run,jobs,ref=[f.result()for f in fs]
  assert run['head_sha']==SOURCE,'Wrong workflow source SHA';bake=next((x for x in jobs['jobs']if x['name']=='bake'),None)
  if bake:assert 'ubuntu-26.04'in bake.get('labels',[]),'Wrong pinned native runner image label'
  observation={'utc':now(),'run_status':run['status'],'run_conclusion':run['conclusion'],'bake_status':bake.get('status')if bake else None,'bake_conclusion':bake.get('conclusion')if bake else None,'current_steps':[s['name']for s in (bake or{}).get('steps',[])if s['status']=='in_progress'],'retained_present':ref is not None};state['observations'].append(observation);state.update(last_run=run,last_jobs=jobs,last_ref=ref);save('B-NATIVE-GITHUB-PROVENANCE.json',state)
  fingerprint=(observation['bake_status'],observation['bake_conclusion'],tuple(observation['current_steps']),observation['retained_present'])
  if fingerprint!=last:print(json.dumps(observation),flush=True);last=fingerprint
  if bake and bake['status']=='completed':
   if bake['conclusion']!='success':raise RuntimeError('Actual native bake failed: '+str(bake['conclusion']))
   if ref is not None:break
  if run['status']=='completed'and run['conclusion']not in ['success',None]:raise RuntimeError('Run ended before successful retained native '+str(run['conclusion']))
  time.sleep(30)
 retained=ref['object']['sha'];commit=api('git/commits/'+retained);assert [x['sha']for x in commit['parents']]==[SOURCE],'API raw native parent mismatch';state.update(status='AUTHENTIC_BAKE_SUCCESS_RETAINED_PARENT_EXACT',retained_sha=retained,retained_commit=commit,actual_raw_parents=[SOURCE]);save('B-NATIVE-GITHUB-PROVENANCE.json',state)
 fetch=git('fetch','--depth=2','--filter=blob:none','--no-tags','origin','refs/heads/'+BRANCH+':refs/remotes/origin/'+BRANCH);(OUT/'RETAINED-FETCH.log').write_bytes(fetch.stdout+fetch.stderr)
 assert git('rev-parse','refs/remotes/origin/'+BRANCH).stdout.decode().strip()==retained
 rawcommit=git('cat-file','-p',retained).stdout;parents=[l.split()[1]for l in rawcommit.decode().split('\n\n',1)[0].splitlines()if l.startswith('parent ')];assert parents==[SOURCE],'Local raw native parent mismatch'
 rawdiff=git('diff','--raw','--no-renames','--no-abbrev','--no-ext-diff',SOURCE,retained).stdout;(OUT/'RETAINED-RAW-DIFF.txt').write_bytes(rawdiff);changes=[]
 for line in rawdiff.decode().splitlines():
  header,path=line.split('\t',1);oldmode,newmode,oldoid,newoid,status=header[1:].split();changes.append({'path':path,'old_mode':oldmode,'new_mode':newmode,'old_git_blob':oldoid,'new_git_blob':newoid,'status':status})
 materialized=[]
 for row in changes:
  oid=row['new_git_blob']
  if oid=='0'*40:continue
  present=git('cat-file','-e',oid+'^{blob}',check=False).returncode==0
  if present:materialized.append({**row,'already_present':True});continue
  data=api('git/blobs/'+oid);assert data['sha']==oid and data['encoding']=='base64';raw=base64.b64decode(data['content']);assert len(raw)==data['size'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,'GitHub blob SHA1 verification failed';written=git('hash-object','-w','--stdin',stdin=raw).stdout.decode().strip();assert written==oid
  materialized.append({**row,'already_present':False,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'Git_blob_SHA1_verified':True})
 unchanged();save('B-RETAINED-OBJECTS-READY.json',{'status':'ALL_CHANGED_NEW_BLOBS_PRESENT_AND_RAW_PARENT_EXACT','source':SOURCE,'retained_sha':retained,'run_id':RUN,'raw_parent':SOURCE,'changed_path_count':len(changes),'missing_new_blobs_fetched':sum(not x['already_present']for x in materialized),'materialized_blobs':materialized,'Root_HEAD_and_worktree_unchanged':True});print(json.dumps({'phase':'OBJECTS_READY','retained_sha':retained,'changed_paths':len(changes),'API_blobs_fetched':sum(not x['already_present']for x in materialized)}),flush=True)
 with (OUT/'POST-NATIVE-AUDIT.log').open('wb')as log:
  audited=subprocess.run([sys.executable,str(OUT/'audit-retained.py'),retained,'--run-id',str(RUN),'--binding-sha256',BIND],env=ENV,stdout=log,stderr=subprocess.STDOUT)
 unchanged();assert audited.returncode==0,'Strict audit rejected retained native; inspect POST-NATIVE-AUDIT.log/FAIL receipt'
 result=json.load(open(OUT/'POST-NATIVE-AUDIT.json'));receipt={'status':result['status'],'retained_sha':retained,'source':SOURCE,'run_id':RUN,'actual_raw_parents':parents,'audit_sha256':hashlib.sha256((OUT/'POST-NATIVE-AUDIT.json').read_bytes()).hexdigest(),'counts':result['counts'],'Root_HEAD_and_worktree_unchanged':True};save('B-NATIVE-RESULT.json',receipt);print(json.dumps(receipt),flush=True)
except Exception as e:
 failure={'status':'MONITOR_OR_MATERIALIZATION_OR_AUDIT_FAILURE','error_type':type(e).__name__,'error':str(e),'utc':now(),'traceback':traceback.format_exc(),'claim_limit':'No native acceptance; retain this failure and diagnose exact evidence without weakening checks or retrying the native.'};save('B-MONITOR-FAIL.json',failure);print(json.dumps(failure),flush=True);sys.exit(1)
