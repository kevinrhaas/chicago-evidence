#!/usr/bin/env python3
"""Root-authorized narrow cancellation of nine superseded 6409 smoke runs."""
import datetime,hashlib,json,subprocess
from pathlib import Path
REPO='kevinrhaas/chicago'
HEAD='6409dda1222e1284e111ab0efde1c471f3284d60'
BRANCH='steward/t3654-1871-city-baseline'
IDS=[44435658605,44435679854,44435694950,44435709855,44435726551,44435741457,44435756130,44435771674,44435788373]
ROOT=Path('/tmp/t3654-6409-smoke-supersession')
ROOT.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,data):
 p=ROOT/name
 assert not p.exists(),p
 p.write_text(json.dumps(data,indent=2)+'\n')
def api(rid):
 p=subprocess.run(['gh','api',f'repos/{REPO}/actions/runs/{rid}'],capture_output=True,text=True,check=True)
 return json.loads(p.stdout)
save('authorization.json',{'recorded_at':now(),'source':'Root explicit task message','authorized_ids':IDS,'head':HEAD,'branch':BRANCH,'reason':'Integrate dev21f609 because PR2198 conflicts and changed data/assets require fresh30 browser cells. Preserve completed6409 mobile1–12 as dated evidence; cancel only these unfinished obsolete smoke runs.','force_cancel_authorized':False})
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
  receipt={'run_id':rid,'at':now(),'action':'ordinary_cancel','exit_code':p.returncode,'accepted':p.returncode==0 and '202 Accepted' in p.stdout,'reason':'Superseded by required upstream integration; not a test failure'}
  save(f'{rid}-receipt.json',receipt);receipts.append(receipt)
  if not receipt['accepted']:
   print(json.dumps(receipt),flush=True);raise SystemExit('Cancellation refused; stop before next run')
  after=api(rid);save(f'{rid}-after.json',after);print(json.dumps({'run_id':rid,'accepted':True,'status':after['status'],'conclusion':after['conclusion']}),flush=True)
  continue
 save(f'{rid}-receipt.json',receipt);receipts.append(receipt);print(json.dumps(receipt),flush=True)
save('batch-result.json',{'at':now(),'head':HEAD,'receipts':receipts,'accepted_cancellations':sum(r.get('accepted',False) for r in receipts),'untouched_completed_runs':[44435608683,44435626669,44435642854]})
