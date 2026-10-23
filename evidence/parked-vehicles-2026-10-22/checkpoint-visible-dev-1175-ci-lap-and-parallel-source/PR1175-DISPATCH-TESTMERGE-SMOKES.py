import sys,json,subprocess,pathlib,datetime,re,time
repo='kevinrhaas/chicago'
branch,sha,head,base=sys.argv[1:5]
assert all(re.fullmatch('[0-9a-f]{40}',x) for x in (sha,head,base))
assert branch.startswith('steward/pr1175-verify-')
out=pathlib.Path('/workspace/shared/PR1175-TESTMERGE-'+sha[:10]+'-SMOKES')
out.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
n=0
def api(route,method='GET',payload=None):
 global n
 n+=1
 stem=out/f'{n:03d}'
 cmd=['gh','api','repos/'+repo+'/'+route,'--method',method]
 if payload is not None:
  p=stem.with_suffix('.request.json');p.write_text(json.dumps(payload,indent=2)+'\n');cmd+=['--input',str(p)]
 r=subprocess.run(cmd,capture_output=True,text=True)
 stem.with_suffix('.stdout').write_text(r.stdout)
 stem.with_suffix('.stderr').write_text(r.stderr)
 if r.returncode:raise RuntimeError(f'GitHub {method} failed; inspect {stem}')
 return json.loads(r.stdout) if r.stdout.strip() else None
cells=[('desktop','13'),('desktop','14'),('mobile','14'),('desktop','1-2'),('mobile','1-2')]+[(v,s) for v in ('desktop','mobile') for s in ('3-4','5','6-7','8','9-12','15')]+[('mobile','13')]
assert len(cells)==18
for v in ('desktop','mobile'):
 seen=[]
 for cv,st in cells:
  if cv!=v:continue
  for part in st.split(','):
   ab=part.split('-');seen.extend(range(int(ab[0]),int(ab[-1])+1))
 assert sorted(seen)==list(range(1,16))
receipt={'repository':repo,'pr':1175,'verification_ref':branch,'test_merge_sha':sha,'source_head':head,'target_base':base,'scope':'One immutable complete published smoke batch on the actual GitHub PR test-merge snapshot. Historical person proofs keep original labels. No rerun, assertion changes or whole-gate PASS until every actual leg succeeds.','started':now(),'dispatches':[],'runs':[],'automatic_retry':False}
p=out/'RECEIPT.json'
def save():p.write_text(json.dumps(receipt,indent=2)+'\n')
save()
try:
 pr=api('pulls/1175');assert pr['state']=='open' and pr['head']['sha']==head and pr['base']['ref']=='dev' and pr['base']['sha']==base and pr['auto_merge'] is None
 assert pr['merge_commit_sha']==sha
 assert api('git/ref/heads/dev')['object']['sha']==base
 commit=api('git/commits/'+sha)
 assert [x['sha'] for x in commit['parents']]==[base,head]
 receipt['test_merge_tree']=commit['tree']['sha'];receipt['test_merge_parents']=[x['sha'] for x in commit['parents']];save()
 assert api('git/ref/heads/'+branch)['object']['sha']==sha
 before=api('actions/workflows/chicago-4d-smoke.yml/runs?per_page=100')
 assert not [x for x in before['workflow_runs'] if x['head_branch']==branch and x['head_sha']==sha and x['event']=='workflow_dispatch'],'Existing batch: do not duplicate'
 for viewport,stage in cells:
  assert api('git/ref/heads/'+branch)['object']['sha']==sha
  row={'viewport':viewport,'stage':stage,'post_attempted':True,'post_succeeded':False,'at':now()};receipt['dispatches'].append(row);save()
  api('actions/workflows/chicago-4d-smoke.yml/dispatches','POST',{'ref':branch,'inputs':{'viewport':viewport,'stage':stage}})
  row['post_succeeded']=True;save()
 for trial in range(4):
  inv=api('actions/workflows/chicago-4d-smoke.yml/runs?per_page=100')
  found=[x for x in inv['workflow_runs'] if x['head_branch']==branch and x['head_sha']==sha and x['event']=='workflow_dispatch']
  receipt['runs']=[{k:x.get(k) for k in ('id','head_sha','head_branch','event','run_attempt','path','status','conclusion','created_at','html_url')} for x in found];save()
  if len(found)==18:break
  if trial<3:time.sleep(5)
 assert len(found)==18,'Accepted dispatches not fully discovered: inspect inventory; do not redispatch'
 receipt['dispatch_complete']=True;receipt['ended']=now();save()
 print(json.dumps({'accepted':18,'discovered':len(found),'receipt':str(p)}))
except BaseException as e:
 receipt['error']=str(e);receipt['ended']=now();save();raise
