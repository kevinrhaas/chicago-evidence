#!/usr/bin/env python3
"""Stage immutable exact-6409 proofs from authorized completed real attempts.

No source edit, canonical gate mutation, exception creation, or dispatch.
The root explicitly authorized fresh local parts 6, 16, 8, 7, 15, 3, 11, 4 and 12 of 16.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

TMP=Path('/tmp')
VERIFIER=TMP/'t3654-pre-browser-source-coverage-strict-reviewed.py'
VERIFIER_SHA='accc8728fb6e35995f52b910c5bad86a1a1b8617dbe74cf7e5409800591a1b07'
INITIAL=TMP/'t3654-pre-browser-bindings-6409-hosted-2-5-6.json'
INITIAL_SHA='5ae8a0ca71140cb95984bb83f5d40ab102d5a6dcd3f2625d428b588b9a352b08'
assert hashlib.sha256(VERIFIER.read_bytes()).hexdigest()==VERIFIER_SHA
assert hashlib.sha256(INITIAL.read_bytes()).hexdigest()==INITIAL_SHA
b=json.loads(INITIAL.read_text())
b['local_receipt_globs']=['t3654-source-fallback-*.receipt.json','t3654-6409-source-*.receipt.json']
seed=TMP/'t3654-pre-browser-bindings-6409-discovery-seed.json'
seed_bytes=(json.dumps(b,indent=2)+'\n').encode()
if seed.exists():assert seed.read_bytes()==seed_bytes
else:seed.write_bytes(seed_bytes)
spec=importlib.util.spec_from_file_location('reviewed_auditor',VERIFIER)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);v.configure(seed)
assert (v.HEAD,v.BASE,v.TREE,v.RUN)==('6409dda1222e1284e111ab0efde1c471f3284d60','c676aa2f4ad6ee8cff0521da6ba8add70d55949c','eeaaefef97d3275b048f308c57c3df5514dbb028',44421763389)
assert not b['qualified_local_exits'] and not b['excluded_hosted_timeouts']
rows=v.declarations((v.APP/'tools/check.sh').read_text())
assert len(rows)==v.COUNT and v.digest(v.APP/'tools/check.sh')==v.DECL_SHA
raw=(TMP/'t3654-source-gate-summary.json').read_bytes();idx=json.loads(raw)
assert (idx['source_commit'],idx['included_dev_base'],idx['run_id'],idx['repository'],idx['pull_request'])==(v.HEAD,v.BASE,v.RUN,v.REPO,v.PR)
parts={x['job_id']:x for x in idx['parts']};assert len(parts)==len(idx['parts'])
assert all(x.get('status')!='completed' or x.get('conclusion')=='success' for x in parts.values()), 'Current source failure/cancellation; no exception is authorized'
hosted=[];hosted_labels=[]
for x in sorted(parts.values(),key=lambda x:int(x['part'].split('/')[0])):
    if x.get('status')!='completed' or x.get('conclusion')!='success' or x.get('verified_pass') is not True:
        continue
    k,n=map(int,x['part'].split('/'));assert n==v.PART_COUNT
    p=TMP/f't3654-support-{v.RUN}-part{k}-complete-meta.json'
    item=v.verify_hosted(p,rows,parts);assert item['job_id']==x['job_id']
    hosted.append(v.bound(p));hosted_labels.append(k)
assert hosted
local=[];local_labels=[]
for p in sorted(TMP.glob('t3654-6409-source-*.receipt.json')):
    # No fixture directories or aliases can enter this automatic admission scope.
    assert p.parent==TMP and p.resolve().parent==TMP.resolve()
    item,why=v.verify_local(p,rows,b['harness_sha256'])
    if item is None:continue
    d=v.read_json(p)
    assert d['part'] in ('3/16','4/16','6/16','7/16','8/16','11/16','12/16','15/16','16/16'), 'Current local part is outside the root-authorized admission set'
    assert d.get('process_receipt'), 'No alternate exit is authorized for this source'
    process=v.read_json(d['process_receipt']);assert process['head']==v.HEAD
    assert d['part'] not in local_labels,'Duplicate current local part needs explicit review'
    local.append(v.bound(p));local_labels.append(d['part'])
assert '6/16' in local_labels
sha=hashlib.sha256(raw).hexdigest();ip=TMP/f't3654-pre-browser-hosted-index-{sha[:16]}.json'
if ip.exists():assert ip.read_bytes()==raw
else:ip.write_bytes(raw)
b['hosted_evidence_index']=v.bound(ip);b['accepted_hosted_metadata']=hosted;b['accepted_local_receipts']=local
hl='-'.join(map(str,hosted_labels));ll='-'.join(x.replace('/','of') for x in sorted(local_labels,key=lambda x:int(x.split('/')[0])))
label=f'h{hl}-l{ll}-strict';p=TMP/f't3654-pre-browser-bindings-6409-{label}.json'
if p.exists():
    old=json.loads(p.read_text())
    assert old['accepted_hosted_metadata']==hosted and old['accepted_local_receipts']==local and old['local_receipt_globs']==b['local_receipt_globs']
else:p.write_text(json.dumps(b,indent=2)+'\n')
print(json.dumps({'new_immutable_binding':v.bound(p),'accepted_hosted_parts':hosted_labels,'accepted_local_parts':local_labels,'automatic_dispatch':False},indent=2),flush=True)
run=subprocess.run([sys.executable,str(VERIFIER),'--bindings',str(p),'--require-complete'])
if run.returncode not in (0,1):sys.exit(run.returncode)
proof=Path(b['output']);d=json.loads(proof.read_text());assert d['bindings']==v.bound(p) and d['source_commit']==v.HEAD
f=TMP/f't3654-pre-browser-source-coverage-6409-{label}-frozen.json'
if f.exists():
    previous=json.loads(f.read_text());assert previous['covered_ordinals']==d['covered_ordinals'] and previous['bindings']==d['bindings']
else:f.write_bytes(proof.read_bytes())
pointer={'scope':'Convenience pointer only, never queue or merge authorization; reverify raw inputs and live state.','source_commit':v.HEAD,'verifier':v.bound(VERIFIER),'binding':v.bound(p),'frozen_proof':v.bound(f),'covered_declarations':len(d['covered_ordinals']),'missing_declarations':len(d['missing_ordinals']),'automatic_dispatch':False}
(TMP/'t3654-pre-browser-latest-6409.json').write_text(json.dumps(pointer,indent=2)+'\n')
print(json.dumps({**pointer,'ready_for_browser_queue':d['ready_for_browser_queue'],'require_complete_exit':run.returncode},indent=2))
sys.exit(run.returncode)
