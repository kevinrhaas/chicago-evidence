#!/usr/bin/env python3
"""Read-only monitor: no dispatch, retry, workflow/repository/PR mutation."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import time

spec=importlib.util.spec_from_file_location('v','/workspace/shared/validate_transport_split_smoke_c02.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def now():return datetime.now(timezone.utc).isoformat()
def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def inspect_terminal(meta,out,sha):
    r={'run_id':meta['id'],'attempt':meta['run_attempt'],'head_sha':meta['head_sha'],
       'status':meta['status'],'conclusion':meta['conclusion'],'html_url':meta['html_url'],
       'event':meta['event'],'path':meta['path'],'run_attempt':meta['run_attempt'],
       'accepted':False,'collected_utc':now()}
    try:
        text=v.gh('run','view',str(meta['id']),'--repo','kevinrhaas/chicago','--attempt',str(meta['run_attempt']),'--log')
        p=out/f'{meta["id"]}-attempt-{meta["run_attempt"]}.log';p.write_text(text);r['log_path']=str(p)
        lines=v.normalize(text)
        views=[re.fullmatch(r'NOT THE FULL GATE — viewports filtered to "(mobile|desktop)"',x) for x in lines]
        views=[x[1] for x in views if x]
        stages=[re.fullmatch(r'NOT THE FULL GATE — stages filtered to "([0-9-]+)" of 15',x) for x in lines]
        stages=[x[1] for x in stages if x]
        r['failure_lines']=[x for x in lines if re.match(r'^  FAIL\s+',x)]
        r['observed_pass_lines']=sum(bool(re.match(r'^  pass\s+',x)) for x in lines)
        r['audit_lines']=[x for x in lines if re.match(r'^\d+ staged-section',x)]
        r['summary_lines']=[x for x in lines if re.fullmatch(r'\d+ passed, \d+ failed',x)]
        v.require(len(views)==1 and len(stages)==1,'actual viewport/stage headers unavailable or ambiguous; no order-based pairing allowed')
        r.update(viewport=views[0],stage=stages[0],parts=v.parts(stages[0]))
        parsed=v.parse_log(text,r['viewport'],r['stage']);r.update(parsed)
        v.require(meta['head_sha']==sha,'run head mismatch')
        v.require(meta['path'].split('@')[0]=='.github/workflows/chicago-4d-smoke.yml','workflow path mismatch')
        v.require(meta['event']=='workflow_dispatch','event mismatch')
        v.require(meta['status']=='completed' and meta['conclusion']=='success','workflow conclusion is not success')
        r['accepted']=True
    except Exception as e:r['error']=str(e)
    return r

def main():
    a=argparse.ArgumentParser();a.add_argument('dispatch',type=Path);a.add_argument('--out',type=Path,required=True);args=a.parse_args()
    d=json.loads(args.dispatch.read_text());sha=d['sha'];repo=d['repository'];ids={x['id'] for x in d['discovered_runs']}
    v.require(len(ids)==18,'expected18actualrunIDs');out=args.out.resolve();v.require(not out.exists(),'fresh evidence directory required');out.mkdir(parents=True)
    save(out/'dispatch.json',d);records={};source_evidence={};source_error=None
    try:source_evidence=v.frozen_sources(repo,sha)
    except Exception as e:source_error=str(e)
    save(out/'frozen-source-audit.json',{'sha':sha,'evidence':source_evidence,'error':source_error})
    print(json.dumps({'kind':'frozen_source_audit','passed':not source_error,'error':source_error}),flush=True)
    while True:
        start=time.monotonic()
        try:
            data=v.api(f'repos/{repo}/actions/workflows/chicago-4d-smoke.yml/runs?head_sha={sha}&event=workflow_dispatch&per_page=100')
            selected={x['id']:x for x in data['workflow_runs'] if x['id'] in ids}
            checks=v.api(f'repos/{repo}/commits/{sha}/check-runs?per_page=100')
            pr=v.api(f'repos/{repo}/pulls/1041')
            snap={'at':now(),'sha':sha,'pr_head':pr['head']['sha'],'pr_draft':pr['draft'],
                  'run_status':dict(Counter(x['status'] for x in selected.values())),
                  'conclusions':dict(Counter(x['conclusion'] or 'pending' for x in selected.values())),
                  'found_selected_runs':len(selected),'missing_run_ids':sorted(ids-set(selected)),
                  'head_mismatches':[x['id'] for x in selected.values() if x['head_sha']!=sha],
                  'checks':[{k:x.get(k) for k in ['name','status','conclusion','html_url']} for x in checks['check_runs']]}
            with (out/'snapshots.jsonl').open('a') as f:f.write(json.dumps(snap)+'\n')
            save(out/'latest.json',snap)
            for run_id,meta in selected.items():
                if meta['status']!='completed' or str(run_id) in records:continue
                record=inspect_terminal(meta,out,sha);records[str(run_id)]=record;save(out/'partial-records.json',list(records.values()))
                print(json.dumps({'kind':'terminal','run_id':run_id,'conclusion':record['conclusion'],'accepted_leg':record['accepted'],
                                  'viewport':record.get('viewport'),'stage':record.get('stage'),'error':record.get('error'),
                                  'failures':record.get('failure_lines',[]),'summary':record.get('summary_lines',[])}),flush=True)
            print(json.dumps({'kind':'snapshot','at':snap['at'],'found':len(selected),'run_status':snap['run_status'],
                              'conclusions':snap['conclusions'],'paired_records':sum('viewport'in x for x in records.values()),
                              'accepted_legs':sum(x['accepted'] for x in records.values()),'pr_head_matches':snap['pr_head']==sha,
                              'check_failures':[x for x in snap['checks'] if x['conclusion'] not in [None,'success','skipped','neutral']],
                              'gate':[x for x in snap['checks'] if x['name']=='gate']}),flush=True)
            if len(records)==18:
                rows=list(records.values())
                m={'repository':repo,'sha':sha,'workflow':'.github/workflows/chicago-4d-smoke.yml','always_on_assertions':v.GUARDS,
                   'runs':[{k:r[k] for k in ['run_id','attempt','viewport','stage']} for r in rows if 'viewport'in r]}
                try:
                    v.manifest_check(m);save(out/'manifest.json',m)
                    receipt=v.aggregate(m,rows,source_evidence,source_error)
                except Exception as e:
                    receipt={'sha':sha,'coverage_proof_passed':False,'workflow_successes_at_sha':sum(r['conclusion']=='success' and r['head_sha']==sha for r in rows),
                             'claim':'coverage not proven','errors':['manifest pairing: '+str(e)],'runs':rows,'source_evidence':source_evidence}
                receipt['independent_pr_checks']=snap['checks'];receipt['pr_head_matches']=snap['pr_head']==sha
                save(out/'aggregate.json',receipt)
                print(json.dumps({'kind':'final','coverage_proof_passed':receipt['coverage_proof_passed'],
                                  'workflow_successes_at_sha':receipt['workflow_successes_at_sha'],'errors':receipt.get('errors',[]),
                                  'receipt':str(out/'aggregate.json')}),flush=True)
                return 0 if receipt['coverage_proof_passed'] else 1
        except Exception as e:
            print(json.dumps({'kind':'poll_error','at':now(),'error':str(e)}),flush=True)
        time.sleep(max(1,60-(time.monotonic()-start)))

if __name__=='__main__':raise SystemExit(main())
