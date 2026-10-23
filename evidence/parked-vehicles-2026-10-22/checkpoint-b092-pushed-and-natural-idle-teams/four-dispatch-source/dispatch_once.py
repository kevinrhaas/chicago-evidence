import subprocess,json,pathlib,sys,datetime,time,re
sha=sys.argv[1];assert re.fullmatch(r'[0-9a-f]{40}',sha)
repo='kevinrhaas/chicago';branch='steward/1835-workwear-repair-20261021';target='59da1aaacc9af6bc07d362339ebee6ee62ed2d5c'
out=pathlib.Path('/workspace/shared/ROOT-1175-'+sha[:9]+'-FINAL4-ONCE');out.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def api(route,*args):
 r=subprocess.run(['gh','api',route,*args],capture_output=True,text=True)
 if r.returncode:raise RuntimeError('GitHub request failed: '+r.stderr[:500])
 return json.loads(r.stdout) if r.stdout.strip() else None
r={'source_head':sha,'source_branch':branch,'expected_target':target,'scope':'Fresh published parts14 and15 in both viewports for inspected1904/changelog-only DEV integration. Earlier-source results retain their original source labels. No rerun/cancel or whole-gate claim.','started':now(),'dispatches':[],'runs':[],'no_retry':True}
p=out/'receipt.json'
def save():p.write_text(json.dumps(r,indent=2)+'\n')
save()
try:
 pr=api('repos/'+repo+'/pulls/1175');dev=api('repos/'+repo+'/git/ref/heads/dev');assert pr['head']['sha']==sha and pr['base']['ref']=='dev' and dev['object']['sha']==target and pr['state']=='open'
 r['initial_pr']= {k:pr.get(k) for k in ['number','state','draft','mergeable','mergeable_state','merge_commit_sha']};r['initial_actual_dev']=dev['object']['sha'];save()
 for viewport,stage in [('desktop','14'),('mobile','14'),('desktop','15'),('mobile','15')]:
  assert api('repos/'+repo+'/git/ref/heads/'+branch)['object']['sha']==sha
  payload=out/('payload-'+viewport+'-'+stage+'.json');payload.write_text(json.dumps({'ref':branch,'inputs':{'viewport':viewport,'stage':stage}}))
  row={'viewport':viewport,'stage':stage,'attempted_at':now(),'post_attempted':True,'post_succeeded':False};r['dispatches'].append(row);save()
  api('repos/'+repo+'/actions/workflows/chicago-4d-smoke.yml/dispatches','--method','POST','--input',str(payload));row['post_succeeded']=True;save()
 for trial in range(6):
  inventory=api('repos/'+repo+'/actions/workflows/chicago-4d-smoke.yml/runs?per_page=100&page=1')
  (out/('inventory-'+str(trial)+'.json')).write_text(json.dumps(inventory))
  found=[x for x in inventory['workflow_runs'] if x['head_sha']==sha and x['head_branch']==branch and x['event']=='workflow_dispatch']
  r['runs']=[{k:x.get(k) for k in ['id','head_sha','head_branch','path','event','run_attempt','created_at','html_url']} for x in found];save()
  if len(found)==4:break
  time.sleep(5)
 assert len(r['runs'])==4,'Four dispatches accepted but discovery incomplete; do not redispatch'
 r['dispatch_complete']=True;r['ended']=now();save();print(json.dumps({'source':sha,'accepted':len(r['dispatches']),'discovered':len(r['runs']),'receipt':str(p)}))
except BaseException as e:
 r['error']=str(e);r['ended']=now();save();raise
