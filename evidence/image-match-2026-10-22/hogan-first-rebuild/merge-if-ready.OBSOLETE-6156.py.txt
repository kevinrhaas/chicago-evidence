import json,subprocess,datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root=Path('/tmp/t2377-model');plan=json.loads((root/'smoke-runs.json').read_text());repo=plan['repository'];head=plan['head'];number=plan['pr']
assert repo=='kevinrhaas/chicago' and number==1229 and head=='6156a0367a2379f0d986b88c7c8236c4ebec0e55'
assert len(plan['runs'])==6 and not plan.get('pending_dispatch')
for v in ['mobile','desktop']:assert sorted(p for r in plan['runs'] if r['viewport']==v for p in r['parts'])==list(range(1,16))
def get(p):return json.loads(subprocess.check_output(['gh','api',p],text=True))
pr=get(f'repos/{repo}/pulls/{number}');assert pr['head']['sha']==head and pr['base']['ref']=='dev'
if pr['merged']:
 print(json.dumps({'merged':True,'merge_commit_sha':pr['merge_commit_sha'],'already_merged':True}));raise SystemExit(0)
assert pr['state']=='open'
with ThreadPoolExecutor(max_workers=6) as pool:runs=list(pool.map(lambda r:get(f"repos/{repo}/actions/runs/{r['id']}"),plan['runs']))
for r in runs:assert r['head_sha']==head and r['workflow_id']==plan['workflow_id'] and r['event']=='workflow_dispatch'
checks=get(f'repos/{repo}/commits/{head}/check-runs?filter=latest&per_page=100')['check_runs'];statuses=get(f'repos/{repo}/commits/{head}/status')['statuses']
ready=(pr.get('mergeable') is True and pr.get('mergeable_state')=='clean' and all(r['status']=='completed' and r['conclusion']=='success' for r in runs) and any(c['name']=='gate' and c['status']=='completed' and c['conclusion']=='success' for c in checks) and all(c['status']=='completed' and c['conclusion'] in ['success','skipped','neutral'] for c in checks) and all(s['state']=='success' for s in statuses))
snapshot={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ready':ready,'pr':number,'head':head,'mergeable_state':pr.get('mergeable_state'),'runs':[{k:r[k] for k in ['id','status','conclusion','html_url','head_sha']} for r in runs],'checks':[{k:c[k] for k in ['name','status','conclusion']} for c in checks]};(root/'github-readiness.json').write_text(json.dumps(snapshot,indent=2)+'\n');print(json.dumps(snapshot),flush=True)
if not ready:raise SystemExit(0)
# The user explicitly authorized PRs and merging to dev. This source head, every required
# smoke partition at both viewports, and the current CI gate must still match at merge.
assert get(f'repos/{repo}/pulls/{number}')['head']['sha']==head
payload={'sha':head,'merge_method':'squash','commit_title':"T-2377: Hogan's pictured openings and ridge chimney (#1229)",'commit_message':'First geometry increment. T-2377 remains open; the reviewed provisional comparison still differs.'}
r=subprocess.run(['gh','api','-X','PUT',f'repos/{repo}/pulls/{number}/merge','--input','-'],input=json.dumps(payload),text=True,capture_output=True,check=True);receipt=json.loads(r.stdout);(root/'github-merge-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt));assert receipt.get('merged') is True
