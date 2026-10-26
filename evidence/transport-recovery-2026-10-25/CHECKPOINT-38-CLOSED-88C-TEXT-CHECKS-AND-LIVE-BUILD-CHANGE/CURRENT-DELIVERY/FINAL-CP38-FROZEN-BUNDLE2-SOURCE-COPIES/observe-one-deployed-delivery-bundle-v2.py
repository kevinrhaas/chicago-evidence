#!/usr/bin/env python3
"""One snapshot followed immediately by independent UI observations; no retry loop."""
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
B=Path('/workspace/.cloud-setup/logs/transport-recovery')
O=B/'current-deployed-final-observation-bundle2'
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
Y=B/'current-dev-external-merge-yard-observer-preparation-v5/observe-current-dev-external-merge-yard-v5.mjs'
N=B/'20261025T2225-CURRENT-DEV-FOLDED-NOTES-PREPARATION-v5/observe-current-dev-folded-notes-v5.mjs'
G=B/'20261025T2225-CURRENT-DEV-FOLDED-NOTES-PREPARATION-v3/prepare-pinned-deployed-notes-inputs.py'
assert not O.exists();O.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def state(phase,**fields):
 p=O/'STATE.tmp';p.write_text(json.dumps({'phase':phase,'observed_unix':time.time(),**fields},indent=2)+'\n');p.replace(O/'STATE.json');print(phase,flush=True)
def run(cmd):subprocess.run(cmd,cwd='/workspace',check=True)
def observe(prefix,command,cap):
 assert os.access('/home/agent/.pki/nssdb/cert9.db',os.W_OK),'Current-turn NSS permission required; never disable TLS'
 rc=subprocess.call([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd','/workspace','--timeout',str(cap),'--',*command],cwd='/workspace')
 r,c=read(str(prefix)+'.result.json'),read(str(prefix)+'.cleanup.json')
 assert c['cleanup_complete'] and c['remaining_owned_children']==[],'Owned browser cleanup incomplete; no second browser permitted'
 return {'prefix':str(prefix),'returncode':rc,'actual_command_returncode':r['returncode'],'timed_out':r['timed_out'],'cleanup_complete':True}
try:
 assert sha(Y)=='3884e24b6a19f86c161562abe90055e29b7203775532dbf0e463035def78e5f6'
 assert sha(N)=='b94229dfa419dee1e27330f08f65700abd2eb3e95bbeac22a066279ed404dd0a'
 assert sha(G)=='1d4305678b52934c935502e39af3b9410e0efb7e4eb90028fc288a76863f47af'
 state('SNAPSHOTTING: actual official deployed D and native selected bytes, no browser yet')
 run([sys.executable,'/workspace/.cloud-setup/observe-current-deployed-selected-http.py','--out',str(O/'HTTP')])
 H=O/'HTTP/RESULT.json';h=read(H);assert h['result']=='PASS';D=h['current_dev'];I=O/'HTTP/YARD-INPUT-BINDING.json';R=O/'HTTP/REVIEW-ANNOTATIONS-INPUT-BINDING.json'
 run([sys.executable,str(G),'--deployed-head',D,'--http-receipt',str(H),'--http-receipt-sha256',sha(H),'--review-contract',str(R),'--review-contract-sha256',sha(R),'--out',str(O/'NOTES-INPUTS')])
 NI=O/'NOTES-INPUTS/INPUT-BINDING.json'
 common={'deployed_head':D,'http_receipt':str(H),'http_receipt_sha256':sha(H),'yard_output':str(O/'yard-output'),'notes_output':str(O/'notes-output')}
 state('RUNNING: targeted yard, explicit Balanced choice at both widths; all original errors/pose/bytes guards retained',**common)
 yard=observe(O/'yard',['node',str(Y),'--execute-read-only-current-dev-yard','--expected-deployed-head',D,'--current-http-receipt',str(H),'--current-http-receipt-sha256',sha(H),'--yard-input-binding',str(I),'--yard-input-binding-sha256',sha(I),'--review-annotation-contract',str(R),'--review-annotation-contract-sha256',sha(R),'--out',str(O/'yard-output')],3600)
 state('RUNNING: native Balanced notes after actual yard cleanup; all original source/text/error guards retained',yard=yard,**common)
 notes=observe(O/'notes',['node',str(N),'--execute-current-dev-notes-observation','--expected-deployed-head',D,'--input-binding',str(NI),'--input-binding-sha256',sha(NI),'--review-contract',str(R),'--review-contract-sha256',sha(R),'--out',str(O/'notes-output')],5400)
 ok=all(x['returncode']==0 and x['actual_command_returncode']==0 and not x['timed_out'] for x in [yard,notes])
 state('PASS: both targeted observers actually closed0/cleanup0; ROOT visual review and public evidence still required' if ok else 'CLOSED WITH NONPASS: actual outcomes retained; no automatic retry or historical qualification transfer',yard=yard,notes=notes,**common)
 if not ok:raise SystemExit(1)
except BaseException as e:
 if not isinstance(e,SystemExit):state('STOPPED: actual error retained; no automatic retry',error=str(e))
 raise
