#!/usr/bin/env python3
"""API-authenticated native audit; Git object/ref writes only, never a checkout/adoption."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import base64,datetime,hashlib,json,os,subprocess,sys,traceback
OUT=Path(__file__).resolve().parent;REPO=Path('/tmp/chicago-west-wicket-20261109');SOURCE_REPO=Path('/tmp/nov10-kinzie-completion');REMOTE='kevinrhaas/chicago';RUN=42818215260;JOB=129840484223;SOURCE='6b11594bbd1d1a4e9fdd864878359ccf1c54edfc';BRANCH='steward/bake-'+str(RUN);BIND='e9f0beae765610a9b5f11734e35a8440e44bd7b306aee080ef5a8e8c4f68cc22';ENV=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def save(n,j):(OUT/n).write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args,repo=REPO,stdin=None,check=True):return subprocess.run(['git',*args],cwd=repo,env=ENV,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check)
def api(p):
 r=subprocess.run(['gh','api','repos/'+REMOTE+'/'+p],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,check=True);return json.loads(r.stdout)
b=json.loads((OUT/'BEFORE-BINDING.json').read_bytes());root_before=json.loads((OUT/'ROOT-BEFORE-READONLY-AUDIT.json').read_bytes())
def unchanged():
 assert git('rev-parse','HEAD',repo=SOURCE_REPO).stdout.decode().strip()==SOURCE,'Frozen SOURCE HEAD changed'
 assert not git('status','--porcelain',repo=SOURCE_REPO).stdout,'Frozen SOURCE worktree changed'
 assert git('rev-parse','HEAD').stdout.decode().strip()==root_before['Root_HEAD'],'Root QA HEAD changed'
 assert git('status','--porcelain').stdout.decode()==root_before['Root_status'],'Root QA worktree changed'
 for n,h in b['manifest_sha256'].items():assert sha((Path(b['actual_readonly_asset_root'])/n).read_bytes())==h,'Root physical native registry changed'
try:
 unchanged();assert sha((OUT/'BEFORE-BINDING.json').read_bytes())==BIND
 with ThreadPoolExecutor(max_workers=3)as p:
  tasks=[p.submit(api,x)for x in['actions/runs/'+str(RUN),'actions/jobs/'+str(JOB),'git/ref/heads/'+BRANCH]];run,job,ref=[x.result()for x in tasks]
 assert run['head_sha']==SOURCE and run['event']=='workflow_dispatch','Unexpected workflow source/event';assert job['name']=='bake'and job['status']=='completed'and job['conclusion']=='success'and 'ubuntu-26.04'in job['labels'],'Unqualified actual bake job'
 retained=ref['object']['sha'];commit=api('git/commits/'+retained);assert [p['sha']for p in commit['parents']]==[SOURCE],'API raw retained parent mismatch'
 log=(OUT/'ACTUAL-BAKE-JOB.log').read_text();assert '4.5.3'in log and b['pin']['version']=='4.5.3','Pinned Blender job evidence absent'
 save('AUTHENTIC-NATIVE-PROVENANCE.json',{'status':'ACTUAL_BAKE_SUCCESS_API_PARENT_EXACT','run':run,'bake_job':job,'retained_ref':ref,'retained_commit':commit,'source':SOURCE,'retained':retained,'runner_label':'ubuntu-26.04','blender_pin':b['pin'],'bake_log_sha256':sha((OUT/'ACTUAL-BAKE-JOB.log').read_bytes()),'claim_limit':'Bake success only; full source gates/smokes remain separately measured.'})
 f=git('fetch','--depth=2','--filter=blob:none','--no-tags','origin','refs/heads/'+BRANCH+':refs/remotes/origin/'+BRANCH);(OUT/'ACTUAL-RETAINED-FETCH.log').write_bytes(f.stdout+f.stderr)
 assert git('rev-parse','refs/remotes/origin/'+BRANCH).stdout.decode().strip()==retained
 raw=git('cat-file','-p',retained).stdout;parents=[r.split()[1]for r in raw.decode().split('\n\n',1)[0].splitlines()if r.startswith('parent ')];assert parents==[SOURCE],'Local raw retained parent mismatch'
 rawdiff=git('diff','--raw','--no-renames','--no-abbrev','--no-ext-diff',SOURCE,retained).stdout;(OUT/'ACTUAL-RETAINED-RAW-DIFF.txt').write_bytes(rawdiff);changes=[]
 for row in rawdiff.decode().splitlines():
  meta,path=row.split('\t',1);om,nm,old,new,status=meta[1:].split();changes.append({'path':path,'old_git_blob':old,'new_git_blob':new,'status':status})
 existing=set(git('cat-file','--batch-all-objects','--batch-check=%(objectname)').stdout.decode().splitlines());materialized=[]
 # Frozen SOURCE code/records/asset-input bytes come from OWN SOURCE plus
 # explicit authenticated canonical asset aliases, never current Root code.
 paths=list(b['source_files']);tree=git('ls-tree','-r','-z',SOURCE,'--',*paths,repo=SOURCE_REPO).stdout;oids={}
 for row in tree.split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);oids[path.decode()]=meta.split()[2].decode()
 for path,receipt in b['source_files'].items():
  oid=oids[path]
  if oid in existing:continue
  alias=b['SOURCE_git_authenticated_asset_input_overlay'].get(path);actual=Path(alias['actual_read_path'])if alias else SOURCE_REPO/path;content=actual.read_bytes();assert sha(content)==receipt['sha256'];assert hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()==oid
  assert git('hash-object','-w','--stdin',stdin=content).stdout.decode().strip()==oid;existing.add(oid);materialized.append({'git_blob':oid,'path':path,'source':'frozen_SOURCE_own_or_Git_authenticated_asset_alias','sha256':sha(content),'bytes':len(content)})
 missing={r['new_git_blob']for r in changes if r['new_git_blob']!='0'*40 and r['new_git_blob']not in existing}
 def fetch_blob(oid):
  j=api('git/blobs/'+oid);assert j['sha']==oid and j['encoding']=='base64';raw=base64.b64decode(j['content']);assert len(raw)==j['size']and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid;return oid,raw
 with ThreadPoolExecutor(max_workers=3)as pool:
  for oid,content in pool.map(fetch_blob,sorted(missing)):
   assert git('hash-object','-w','--stdin',stdin=content).stdout.decode().strip()==oid;materialized.append({'git_blob':oid,'source':'API_verified_native_blob','sha256':sha(content),'bytes':len(content)})
 unchanged();save('ACTUAL-OBJECTS-MATERIALIZED.json',{'status':'OBJECTS_READY_NOT_ADOPTED','source':SOURCE,'retained':retained,'raw_parents':parents,'run':RUN,'changes':changes,'materialized':materialized,'Root_HEAD_and_physical_native_registries_unchanged':True});print('Objects ready',retained,len(changes),'changed paths',len(materialized),'new immutable blobs',flush=True)
 with (OUT/'ACTUAL-POST-NATIVE-AUDIT.log').open('wb')as f:
  p=subprocess.run([sys.executable,str(OUT/'audit-retained.py'),retained,'--repo',str(REPO),'--binding',str(OUT/'BEFORE-BINDING.json'),'--binding-sha256',BIND,'--run-id',str(RUN)],env=ENV,stdout=f,stderr=subprocess.STDOUT)
 unchanged();assert p.returncode==0,'Strict native audit rejected retained outputs; inspect failure receipt/log'
 r=json.loads((OUT/'POST-NATIVE-AUDIT.json').read_bytes());save('ACTUAL-NATIVE-AUDIT-RESULT.json',{'status':r['status'],'retained':retained,'source':SOURCE,'run':RUN,'audit_sha256':sha((OUT/'POST-NATIVE-AUDIT.json').read_bytes()),'counts':r['counts'],'raw_parents':parents,'Root_HEAD_and_worktree_unchanged':True,'Root_native_registries_unchanged':True});print(json.dumps(json.loads((OUT/'ACTUAL-NATIVE-AUDIT-RESULT.json').read_bytes()),indent=2),flush=True)
except Exception as e:
 j={'status':'FAIL_AUTH_MATERIALIZATION_OR_NATIVE_AUDIT','error':str(e),'traceback':traceback.format_exc(),'source':SOURCE,'run':RUN,'claim_limit':'No adoption or native acceptance; preserve literal failure and diagnose without broad waivers.'};save('ACTUAL-AUDIT-FAIL.json',j);print(json.dumps(j,indent=2),flush=True);sys.exit(1)
