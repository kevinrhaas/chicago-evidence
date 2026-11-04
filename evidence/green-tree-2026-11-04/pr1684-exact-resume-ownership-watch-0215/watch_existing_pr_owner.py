from pathlib import Path
import subprocess,json,time,datetime,re
P=Path(__file__).resolve().parent;RID=41759074130;URL=f'https://github.com/kevinrhaas/polecat-platform/actions/runs/{RID}'
def api(repo,path,missing=False):
 for retry in range(3):
  q=subprocess.run(['bash','-c','source /workspace/shared/resume-chicago-env.sh\nexec gh api -H "Cache-Control: no-cache" "$1"','gt-pr-owner-watch','repos/kevinrhaas/'+repo+'/'+path],capture_output=True,timeout=45)
  if q.returncode==0:return json.loads(q.stdout)
  if missing and b'HTTP 404'in q.stderr:return None
  print(json.dumps({'read_error':q.stderr.decode(),'path':path,'retry':retry,'not_native_failure':True}),flush=True)
  if retry<2:time.sleep(2)
 raise RuntimeError(q.stderr.decode())
for i in range(6):
 run=api('polecat-platform',f'actions/runs/{RID}');jobs=api('polecat-platform',f'actions/runs/{RID}/jobs');j=next(x for x in jobs['jobs']if x['name']=='targeted-chicago');assert j['labels']==['ubuntu-26.04'];ref=api('chicago','git/ref/heads/lap/pr-1684',missing=True);commit=None;owner=None
 if ref:
  commit=api('chicago','git/commits/'+ref['object']['sha']);m=re.search(r'(?m)^run: (.+)$',commit['message']);owner=m.group(1).strip()if m else None
 row={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':run,'jobs':jobs,'lap_ref':ref,'lap_commit':commit,'lap_run_url':owner,'our_exact_pr_lap':owner==URL,'foreign_lap_present':ref is not None and owner!=URL,'read_only_no_takeover':True};(P/'OWNER-WATCH-LATEST.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps({'at':row['at'],'run_status':run['status'],'native_job':j['status'],'runner':j['runner_name'],'active':[s['name']for s in j['steps']if s['status']=='in_progress'],'lap_present':ref is not None,'lap_run_url':owner,'our_exact_pr_lap':row['our_exact_pr_lap'],'foreign_lap':row['foreign_lap_present']}),flush=True)
 if row['our_exact_pr_lap']:
  assert j['status']=='in_progress'and j['runner_name'];(P/'ACTUAL-EXACT-PR-LAP-PROOF.json').write_text(json.dumps(row,indent=2)+'\n');break
 if row['foreign_lap_present']or run['status']=='completed':break
 if i<5:time.sleep(20)
(P/'OWNER-WATCH-CLOSED.json').write_text(json.dumps({'read_only':True,'last':row,'snapshots':i+1,'scope':'No claim/PRlap exists unless actual proof file says so; no dispatch or job mutation'},indent=2)+'\n')
