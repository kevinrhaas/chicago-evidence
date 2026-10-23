import json,subprocess,time,datetime
from pathlib import Path
repo='kevinrhaas/chicago';branch='steward/t2377-hogan-picture-match';head='6156a0367a2379f0d986b88c7c8236c4ebec0e55';workflow='chicago-4d-smoke.yml';path=Path('/tmp/t2377-model/smoke-runs.json')
def get(p):return json.loads(subprocess.check_output(['gh','api',p],text=True))
def listing():return get(f'repos/{repo}/actions/workflows/{workflow}/runs?branch={branch}&event=workflow_dispatch&per_page=30')['workflow_runs']
assert not path.exists(),'Existing dispatch plan: inspect before redispatching'
plan={'repository':repo,'pr':1229,'branch':branch,'head':head,'workflow_id':365585058,'scope':'All15parts at both viewports; exact partition1-12/13/14-15','runs':[]}
def save():path.write_text(json.dumps(plan,indent=2)+'\n')
for viewport in ['mobile','desktop']:
 for stage in ['1-12','13','14-15']:
  assert get(f'repos/{repo}/git/ref/heads/{branch}')['object']['sha']==head
  before={r['id'] for r in listing()};payload={'ref':branch,'inputs':{'viewport':viewport,'stage':stage}};plan['pending_dispatch']={'viewport':viewport,'stage':stage,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};save()
  subprocess.run(['gh','api','-X','POST',f'repos/{repo}/actions/workflows/{workflow}/dispatches','--input','-'],input=json.dumps(payload),text=True,capture_output=True,check=True)
  for attempt in range(15):
   matches=[r for r in listing() if r['id'] not in before and r['head_sha']==head]
   if matches:break
   time.sleep(2)
  assert len(matches)==1,f'Ambiguous dispatch receipt: {len(matches)}'
  r=matches[0];entry={'viewport':viewport,'stage':stage,'parts':list(range(1,13)) if stage=='1-12' else [13] if stage=='13' else [14,15],'id':r['id'],'url':r['html_url'],'head':r['head_sha']};plan['runs'].append(entry);plan.pop('pending_dispatch',None);save();print(json.dumps(entry),flush=True)
for viewport in ['mobile','desktop']:
 parts=[p for r in plan['runs'] if r['viewport']==viewport for p in r['parts']];assert sorted(parts)==list(range(1,16))
print('Dispatched all15parts for bothviewports; no merge until all6runs andCI pass.',flush=True)
