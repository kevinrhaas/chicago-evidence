#!/usr/bin/env python3
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import time

s=importlib.util.spec_from_file_location('v','/workspace/shared/validate_transport_split_smoke.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
a=argparse.ArgumentParser();a.add_argument('run_id',type=int);a.add_argument('sha');a.add_argument('--out',type=Path,required=True);args=a.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
while True:
 start=time.monotonic()
 try:
  m=v.api(f'repos/kevinrhaas/chicago/actions/runs/{args.run_id}');r={k:m.get(k) for k in ['id','head_sha','status','conclusion','html_url','run_attempt','created_at','updated_at']};r['expected_sha']=args.sha;r['head_matches']=m['head_sha']==args.sha
  (out/'latest.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'kind':'human_ci',**r}),flush=True)
  if m['status']=='completed':
   jobs=v.api(f'repos/kevinrhaas/chicago/actions/runs/{args.run_id}/jobs');(out/'jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
   try:
    text=v.gh('run','view',str(args.run_id),'--repo','kevinrhaas/chicago','--attempt',str(m['run_attempt']),'--log');(out/f'{args.run_id}.log').write_text(text);r['log_collected']=True
    lines=v.normalize(text);receipts=[];skip=0;decoder=json.JSONDecoder()
    for i,line in enumerate(lines):
     if i<skip or not line.lstrip().startswith('{'):continue
     raw='\n'.join(lines[i:i+10000]);offset=len(raw)-len(raw.lstrip());raw=raw.lstrip()
     try:d,end=decoder.raw_decode(raw)
     except json.JSONDecodeError:continue
     if isinstance(d,dict):receipts.append(d);skip=i+raw[:end].count('\n')+1
    (out/'structured-log-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    codes=Counter();issues=[x for x in receipts if 'issue_code_counts'in x]
    for x in issues:codes.update(x['issue_code_counts'])
    r['structured_receipt_count']=len(receipts);r['issue_receipt_count']=len(issues);r['issue_code_totals']=dict(codes);r['any_issue_receipt_truncated']=any(x.get('truncated') for x in issues)
    r['errors']=[x for x in lines if '##[error]'in x or 'page.evaluate: Error:'in x]
   except Exception as e:r['log_error']=str(e)
   (out/'terminal.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'kind':'human_terminal',**r}),flush=True);break
 except Exception as e:print(json.dumps({'kind':'human_poll_error','error':str(e)}),flush=True)
 time.sleep(max(1,60-(time.monotonic()-start)))
