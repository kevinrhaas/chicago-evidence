#!/usr/bin/env python3
"""Register completed, decoded CI evidence; never writes repository receipts."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

rid=int(sys.argv[1])
logp=Path(f'/tmp/t3654-ci-{rid}.log')
metap=Path(f'/tmp/t3654-ci-{rid}-meta.json')
meta=json.loads(metap.read_text())
ledgerp=Path('/tmp/t3654-legacy-coverage-ledger.json')
ledger=json.loads(ledgerp.read_text())
row=next(x for x in ledger['ci_plan'] if x['run_id']==rid)
assert meta['headSha']==row['head_sha'], 'Unexpected tested commit'
assert meta['status']=='completed', 'Job is not complete'
log=logp.read_text(encoding='utf-8-sig')
lines=[re.sub(r'^\d{4}-\d\d-\d\dT[\d:.]+Z\s','',s) for s in log.splitlines()]
body='\n'.join(lines)
viewport=re.search(r'^NOT THE FULL GATE — viewports filtered to "([^"]+)"',body,re.M)
stage=re.search(r'^NOT THE FULL GATE — stages filtered to "([^"]+)"',body,re.M)
if viewport: assert viewport.group(1)==row['viewport'], 'Wrong viewport'
if stage: assert stage.group(1)==row['stage'], 'Wrong stage range'
summary=re.search(r'^(\d+) passed, (\d+) failed$',body,re.M)
counts=re.search(r'^(\d+) staged-section check\(s\) \(stage ([^ ]+) of 15\), (\d+) always-on check\(s\)',body,re.M)
elapsed=re.search(r'^(\d+) m (\d+) s for stage ',body,re.M)
zero_errors=bool(re.search(r'^  pass  .*: zero page errors$',body,re.M))
published=bool(re.search(r'^serving .* — PUBLISHED mirror',body,re.M))
passed=int(summary.group(1)) if summary else None
failed=int(summary.group(2)) if summary else None
credit=bool(not row.get('superseded_reason') and meta['conclusion']=='success' and published and viewport and stage and summary and counts and zero_errors and failed==0 and re.search(r'^SMOKE PASS$',body,re.M))
sha=hashlib.sha256(logp.read_bytes()).hexdigest()
row.update(status=meta['status'],conclusion=meta['conclusion'],metadata_updated_at=meta['updatedAt'],logs_available=True,log=str(logp),log_sha256=sha,metadata=str(metap),target='published' if published else 'unverified',staged_checks=int(counts.group(1)) if counts else None,always_on_checks=int(counts.group(3)) if counts else None,page_errors=0 if zero_errors else None,passed=passed,failed=failed,harness_seconds=int(elapsed.group(1))*60+int(elapsed.group(2)) if elapsed else None,coverage_credit=credit,root_receipt_recorded=False,root_receipt_note='Held until a clean boundary with source-gate publisher/check processes.',failure_lines=[s.strip() for s in lines if re.match(r'^  FAIL ',s)][:12])
mp=Path('/tmp/t3654-verified-ci-logs.json');mapping=json.loads(mp.read_text()) if mp.exists() else {};mapping[str(rid)]={'path':str(logp),'sha256':sha};mt=mp.with_suffix('.tmp');mt.write_text(json.dumps(mapping,indent=2)+'\n');mt.replace(mp)
ledger['last_ci_poll_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();lt=ledgerp.with_suffix('.tmp');lt.write_text(json.dumps(ledger,indent=2)+'\n');lt.replace(ledgerp)
print(json.dumps({k:row.get(k) for k in ['run_id','viewport','stage','head_sha','conclusion','passed','failed','page_errors','staged_checks','always_on_checks','harness_seconds','coverage_credit','failure_lines']},indent=2))
print('Coverage cells:',sum(len(x['parts']) for x in ledger['ci_plan'] if x.get('coverage_credit')),'of30')
