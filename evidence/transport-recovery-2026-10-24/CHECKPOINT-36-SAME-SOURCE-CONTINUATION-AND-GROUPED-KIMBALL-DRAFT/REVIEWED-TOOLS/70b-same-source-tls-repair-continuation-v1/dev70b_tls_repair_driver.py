#!/usr/bin/env python3
import argparse
import fcntl
import os
import subprocess
import sys
import time
from dev70b_tls_repair_common import *

p=argparse.ArgumentParser();p.add_argument('--execute-reviewed-continuation',action='store_true');p.add_argument('--tools-sha256',required=True);a=p.parse_args()
need(a.execute_reviewed_continuation,'Explicit ROOT execution required')
tools(a.tools_sha256);quiet();need(not RUN.exists(),'Preserve existing continuation; never automatically retry')
lock=Path('/workspace/.cloud-setup/abb1-transport-ui-matrix.active.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
original, prereq, before, sealed, initial=original_evidence(a.tools_sha256)
RUN.mkdir();save(RUN/'PUBLISHED-MANIFEST-BEFORE.json',before)
state={'schema':'chicago-h3-tls-repair-composite-state-v1','status':'RUNNING: explicit reviewed TLS environment repair continuation','head':HEAD,'tree':old.TREE,'app_subtree':old.APP_TREE,'accepted_base':old.BASE,'config':original['config'],'prerequisites':prereq,'root_authorization_sha256':AUTH_SHA,'tools_manifest_sha256':a.tools_sha256,'zero_cross_source_results':True,'reused_same_source_leg_count':7,'new_required_leg_count':17,'planned_legs':[list(x) for x in old.LEGS],'selected':sealed,'original_failed_attempt':{'viewport':'mobile','stage':'14','prefix':str(ORIGINAL/'70b-transport-ui-matrix-mobile-14'),'result':'NONPASS:139passed/1zero-page-errors TLSfailure','original_driver_returncode':1,'original_pipeline_returncode':1,'original_cleanup_complete':True,'selected_for_coverage':False},'initial_source':initial,'started_unix':time.time()}
save(RUN/'COMPOSITE-STATE.json',state)
try:
 for v, stage in old.LEGS[7:]:
  pause=Path('/workspace/.cloud-setup/transport-browser-resource-pause.json')
  while pause.exists():
   state['resource_pause']={'since_unix':time.time(),'browser_launched':False};save(RUN/'COMPOSITE-STATE.json',state);time.sleep(.25)
  state.pop('resource_pause',None);quiet();tools(a.tools_sha256)
  prior,_=source(value_hash(before));prefix=RUN/f'70b-tls-repair-{v}-{stage}'
  need(not any(RUN.glob(prefix.name+'.*')),'Never reuse an attempt prefix')
  save(str(prefix)+'.binding.before.json',prior);state['active']={'viewport':v,'stage':stage,'prefix':str(prefix),'timeout_seconds':old.timeout_for(v,stage)};save(RUN/'COMPOSITE-STATE.json',state)
  print(f'Starting new after reviewed TLS repair: {v} {stage}',flush=True)
  env={k:x for k,x in os.environ.items() if not k.startswith('SMOKE_')};env['GIT_OPTIONAL_LOCKS']='0';env.pop('CHICAGO_TICKETS_DIR',None)
  rc=subprocess.call([sys.executable,str(old.SUPERVISOR),'--prefix',str(prefix),'--cwd',str(old.APP),'--timeout',str(old.timeout_for(v,stage)),'--',*old.child_command(v,stage)],env=env)
  state['attempted_outcomes']=state.get('attempted_outcomes',[])+[{'viewport':v,'stage':stage,'prefix':str(prefix),'outer_returncode':rc}];save(RUN/'COMPOSITE-STATE.json',state)
  need(rc==0,'Actual new leg failed: STOP, preserve evidence, no retry')
  proof=old.validate_leg(prefix,v,stage);after,_=source(value_hash(before));save(str(prefix)+'.binding.after.json',after)
  state['selected'].append({'viewport':v,'stage':stage,'prefix':str(prefix),'outer_returncode':rc,'proof':proof,'binding_hashes':{s:digest(str(prefix)+s) for s in ['.binding.before.json','.binding.after.json']},'origin':'new-after-reviewed-TLS-environment-repair'});state.pop('active',None);save(RUN/'COMPOSITE-STATE.json',state);quiet()
  print(f'Closed {v} {stage}: {proof["passed"]}passed; {proof["command_seconds"]:.3f}s; within600={proof["fits_foreground_budget"]}',flush=True)
 final,after=source(value_hash(before));save(RUN/'PUBLISHED-MANIFEST-AFTER.json',after);state.update(status='All24 selected executions present; internal verification pending',final_source=final);save(RUN/'COMPOSITE-STATE.json',state)
 proof=verify_selected(RUN,a.tools_sha256);save(RUN/'INTERNAL-COMPOSITE-PROOF.json',proof);state.update(status='PASS: composite24 native leg executions; original attempt remains NONPASS; independent verification pending',internal_proof_sha256=digest(RUN/'INTERNAL-COMPOSITE-PROOF.json'),finished_unix=time.time());save(RUN/'COMPOSITE-STATE.json',state)
except BaseException as exc:
 state.update(status='STOPPED: actual new failure retained; no automatic retry',error=str(exc),finished_unix=time.time());save(RUN/'COMPOSITE-STATE.json',state);raise
finally:
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
