#!/usr/bin/env python3
"""Reconcile the exact current hosted source gate; never dispatch or write ROOT."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

rid=int(sys.argv[1])
metap=Path(f'/tmp/t3654-support-{rid}-meta.json')
meta=json.loads(metap.read_text())
ledgerp=Path('/tmp/t3654-legacy-coverage-ledger.json')
ledger=json.loads(ledgerp.read_text())
summaryp=Path('/tmp/t3654-source-gate-summary.json')
summary=json.loads(summaryp.read_text())
assert summary['run_id']==rid
assert meta['headSha']==summary['source_commit']==ledger['source_task_commit']
assert meta['headBranch']=='steward/t3654-1871-city-baseline'
source=next(x for x in ledger['supporting_ci'] if x['run_id']==rid and x['name']=='source-gate')
assert source['head_sha']==meta['headSha']
parts=[]
aggregate=None
for job in meta['jobs']:
    match=re.fullmatch(r'gate part (\d)/8',job['name'])
    if job['name']=='gate':
        aggregate={'job_id':job['databaseId'],'status':job['status'],'conclusion':job['conclusion']}
    if not match:
        continue
    n=int(match.group(1))
    row={'part':f'{n}/8','ordinal':n,'job_id':job['databaseId'],'status':job['status'],'conclusion':job['conclusion'],'verified_pass':False}
    logp=Path(f'/tmp/t3654-support-{rid}-job{job["databaseId"]}.log')
    if logp.exists():
        lines=[re.sub(r'\x1b\[[0-9;]*m','',re.sub(r'^\d{4}-\d\d-\d\dT[\d:.]+Z\s','',s)) for s in logp.read_text(encoding='utf-8-sig').splitlines()]
        body='\n'.join(lines)
        passes=re.findall(r'^CHECK PASS — part (\d)/8: (\d+) steps, none red\.$',body,re.M)
        fails=re.findall(r'^CHECK FAIL — part (\d)/8: (\d+) of (\d+) steps failed:',body,re.M)
        row.update(log=str(logp),log_sha256=hashlib.sha256(logp.read_bytes()).hexdigest())
        if job['status']=='completed' and job['conclusion']=='success':
            assert len(passes)==1 and int(passes[0][0])==n and not fails, f'No exact successful log for part{n}'
            row.update(verified_pass=True,steps=int(passes[0][1]))
        elif fails:
            row['failure_summaries']=fails
    parts.append(row)
assert len(parts)==8 and sorted(x['ordinal'] for x in parts)==list(range(1,9))
parts.sort(key=lambda x:x['ordinal'])
source_complete=bool(all(x['verified_pass'] for x in parts) and aggregate and aggregate['status']=='completed' and aggregate['conclusion']=='success' and meta['status']=='completed' and meta['conclusion']=='success')
hold=ledger.get('dispatch_hold')
complete=bool(source_complete and not hold)
summary.update(complete=complete,source_jobs_complete=source_complete,dispatch_hold=hold,parts=parts,aggregate=aggregate,metadata=str(metap),metadata_sha256=hashlib.sha256(metap.read_bytes()).hexdigest(),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),verified_parts=sum(x['verified_pass'] for x in parts),reason=hold or ('All eight exact-head part logs and aggregate succeeded.' if complete else 'Full current source coverage is incomplete; fresh legacy dispatch remains blocked.'))
temporary=summaryp.with_suffix('.tmp');temporary.write_text(json.dumps(summary,indent=2)+'\n');temporary.replace(summaryp)
source.update(status=meta['status'],conclusion=meta['conclusion'],metadata=str(metap),completed_jobs=[x for x in parts if x['status']=='completed'])
temporary=ledgerp.with_suffix('.tmp');temporary.write_text(json.dumps(ledger,indent=2)+'\n');temporary.replace(ledgerp)
print(json.dumps({'run_id':rid,'head':meta['headSha'],'complete':complete,'verified_parts':summary['verified_parts'],'parts':[{k:x.get(k) for k in ['part','status','conclusion','verified_pass','steps']} for x in parts],'aggregate':aggregate},indent=2))
