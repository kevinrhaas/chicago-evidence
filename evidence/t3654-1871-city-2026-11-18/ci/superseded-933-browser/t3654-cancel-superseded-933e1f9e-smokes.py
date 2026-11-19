#!/usr/bin/env python3
"""Root-authorized narrow cancellation of six superseded 933 smoke runs."""
import datetime,hashlib,json,subprocess
from pathlib import Path
REPO='kevinrhaas/chicago'
HEAD='933e1f9e00f378436bb2c9396b634696dc6f3138'
BRANCH='steward/t3654-1871-city-baseline'
IDS=[44444724593,44444739587,44444759609,44444773514,44444794793,44444815188]
ROOT=Path('/tmp/t3654-933e1f9e-smoke-supersession')
ROOT.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,data):
 p=ROOT/name
 assert not p.exists(),p
 p.write_text(json.dumps(data,indent=2)+'\n')
def api(rid):
 p=subprocess.run(['gh','api',f'repos/{REPO}/actions/runs/{rid}'],capture_output=True,text=True,check=True)
 return json.loads(p.stdout)
save('authorization.json',{'recorded_at':now(),'source':'Root explicit task message','authorized_ids':IDS,'head':HEAD,'branch':BRANCH,'reason':'Owner compiler repair updates only data/liberties.json count1184 to1185; staged runtime hash changed tosha256:f681e5412b836a8d. Root explicitly authorized retiring exactly these six unfinished933 smoke runs before the new clean/publication binding.','force_cancel_authorized':False})
receipts=[]
for rid in IDS:
 before=api(rid);save(f'{rid}-before.json',before)
 assert before['id']==rid and before['repository']['full_name']==REPO
 assert before['head_sha']==HEAD and before['head_branch']==BRANCH
 assert before['path']=='.github/workflows/chicago-4d-smoke.yml' and before['name']=='Chicago 4D — full smoke'
 assert before['event']=='workflow_dispatch'
 if before['status']=='completed':
  receipt={'run_id':rid,'at':now(),'action':'none','reason':'Already completed at live guard; not cancelled','conclusion':before['conclusion']}
 else:
  p=subprocess.run(['gh','api','-i','-X','POST',f'repos/{REPO}/actions/runs/{rid}/cancel'],capture_output=True,text=True)
  (ROOT/f'{rid}-cancel-response.txt').write_text(p.stdout+p.stderr)
  receipt={'run_id':rid,'at':now(),'action':'ordinary_cancel','exit_code':p.returncode,'accepted':p.returncode==0 and '202 Accepted' in p.stdout,'reason':'Superseded by confirmed derived-liberty count repair; no browser test failure observed'}
  save(f'{rid}-receipt.json',receipt);receipts.append(receipt)
  if not receipt['accepted']:
   print(json.dumps(receipt),flush=True);raise SystemExit('Cancellation refused; stop before next run')
  after=api(rid);save(f'{rid}-after.json',after);print(json.dumps({'run_id':rid,'accepted':True,'status':after['status'],'conclusion':after['conclusion']}),flush=True)
  continue
 save(f'{rid}-receipt.json',receipt);receipts.append(receipt);print(json.dumps(receipt),flush=True)
save('batch-result.json',{'at':now(),'head':HEAD,'receipts':receipts,'accepted_cancellations':sum(r.get('accepted',False) for r in receipts),'untouched_completed_runs':[]})
