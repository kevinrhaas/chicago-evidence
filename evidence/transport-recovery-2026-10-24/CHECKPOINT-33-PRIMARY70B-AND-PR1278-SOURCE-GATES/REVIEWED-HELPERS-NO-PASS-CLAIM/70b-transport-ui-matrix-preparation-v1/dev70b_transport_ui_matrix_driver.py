#!/usr/bin/env python3
"""NEW matrix only. Never imports/resumes previous results. Root launches explicitly."""
import argparse,fcntl,os,subprocess,sys,time,traceback
from pathlib import Path
from dev70b_transport_ui_matrix_common import *
def main():
 p=argparse.ArgumentParser();p.add_argument('--head',required=True);p.add_argument('--out',required=True);p.add_argument('--preflight-prefix',required=True);p.add_argument('--publish-prefix',required=True);p.add_argument('--focused-prefix',required=True);p.add_argument('--focused-output',required=True);p.add_argument('--execute-fresh-matrix',action='store_true');a=p.parse_args()
 need(a.execute_fresh_matrix,'Prepared only: root must explicitly request fresh execution')
 out=Path(a.out).resolve();need(out.parent==LOG and out.name.startswith('70b-transport-ui-matrix-'),'Use a fresh 70b-transport-ui-matrix-* directory under transport-recovery');need(not out.exists(),'Preserve existing attempt; use a new output directory')
 config={'head':a.head,'preflight_prefix':a.preflight_prefix,'publish_prefix':a.publish_prefix,'focused_prefix':a.focused_prefix,'focused_output':a.focused_output}
 need(not busy_processes(),'An existing browser/smoke/continuation is active; inspect it rather than launch a duplicate')
 lock_path=Path('/workspace/.cloud-setup/abb1-transport-ui-matrix.active.lock');lock=lock_path.open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 # All prerequisites/source guards precede the first browser. No helper publishes or derives.
 prereq=prerequisites(config);snapshot,published=source_snapshot(a.head,prereq['focused']['published_manifest_digest'])
 focused_manifest=read(Path(config['focused_output'])/'PUBLISHED-MANIFEST-AFTER.json');need(sorted(focused_manifest,key=lambda r:r['path'])==published,'Current published bytes differ from completed focused proof')
 out.mkdir();state={'status':'running','fresh_results_only':True,'zero_inherited_results':True,'config':config,'tree':TREE,'app_subtree':APP_TREE,'accepted_base':BASE,'planned_legs':[list(x) for x in LEGS],'completed':[],'prerequisites':prereq,'initial_source':snapshot,'started_unix':time.time(),'tool_hashes':{p.name:digest(p) for p in [Path(__file__),Path(__file__).with_name('dev70b_transport_ui_matrix_common.py'),Path(__file__).with_name('dev70b_transport_ui_matrix_verify.py'),SUPERVISOR]}}
 save(out/'PUBLISHED-MANIFEST-BEFORE.json',published);mh=value_hash(published);save(out/'MATRIX-STATE.json',state)
 try:
  for viewport,stage in LEGS:
   pause=Path('/workspace/.cloud-setup/transport-browser-resource-pause.json')
   if pause.exists():
    state['resource_pause']={'state':'waiting before source check and before supervisor launch','since_unix':time.time(),'browser_launched':False};save(out/'MATRIX-STATE.json',state)
    print('Waiting for owned browser resource pause to be released; no browser launched',flush=True)
    while pause.exists():time.sleep(.25)
    state.pop('resource_pause',None);save(out/'MATRIX-STATE.json',state)
   need(not busy_processes(),'Another browser/smoke/continuation became active')
   for name,want in state['tool_hashes'].items():
    file=SUPERVISOR if name==SUPERVISOR.name else Path(__file__).with_name(name);need(digest(file)==want,'Reviewed helper/supervisor changed during run')
   before,_=source_snapshot(a.head,mh);prefix=out/f'70b-transport-ui-matrix-{viewport}-{stage}';need(not any(prefix.parent.glob(prefix.name+'.*')),'Leg prefix exists; do not reuse receipts')
   save(str(prefix)+'.binding.before.json',before);state['active']={'viewport':viewport,'stage':stage,'prefix':str(prefix),'timeout_seconds':timeout_for(viewport,stage),'timeout_reason':timeout_reason(viewport,stage),'launch_requested':True,'browser_launch_state':'Delegated to supervisor; actual process/log receipts determine launch'};save(out/'MATRIX-STATE.json',state)
   print(f'Starting fresh {viewport} part{stage}; bound{timeout_for(viewport,stage)}s',flush=True)
   env={k:v for k,v in os.environ.items() if not k.startswith('SMOKE_')};env['GIT_OPTIONAL_LOCKS']='0';env.pop('CHICAGO_TICKETS_DIR',None)
   outer=subprocess.call([sys.executable,str(SUPERVISOR),'--prefix',str(prefix),'--cwd',str(APP),'--timeout',str(timeout_for(viewport,stage)),'--',*child_command(viewport,stage)],env=env)
   # Save every actual outcome before rejecting it; never turn a timeout into a pass.
   record={'viewport':viewport,'stage':stage,'prefix':str(prefix),'outer_returncode':outer,'proof':None};state['completed'].append(record);state.pop('active',None);save(out/'MATRIX-STATE.json',state)
   need(outer==0,'Supervisor returned failure; actual receipts retained')
   proof=validate_leg(prefix,viewport,stage);after,_=source_snapshot(a.head,mh);save(str(prefix)+'.binding.after.json',after)
   record['proof']=proof;record['binding_hashes']={s:digest(str(prefix)+s) for s in ['.binding.before.json','.binding.after.json']};save(out/'MATRIX-STATE.json',state)
   need(not busy_processes(),'Browser/smoke survived cleanup or another run started')
   print(f'Completed {viewport} {stage}: {proof["passed"]}passed, {proof["staged_checks"]}staged; {proof["command_seconds"]:.3f}s; within600={proof["fits_foreground_budget"]}',flush=True)
  final,published_after=source_snapshot(a.head,mh);save(out/'PUBLISHED-MANIFEST-AFTER.json',published_after);state.update(status='all24completed_pending_final_verification',final_source=final);save(out/'MATRIX-STATE.json',state)
  verified=verify_complete(out,a.head);save(out/'FINAL-24-LEG-VERIFICATION.json',verified);state.update(status='PASS: fresh all15parts/bothviewports, final verification complete',finished_unix=time.time(),verification_sha256=digest(out/'FINAL-24-LEG-VERIFICATION.json'));save(out/'MATRIX-STATE.json',state)
  print('PASS: fresh24legs/source/manifests/cleanup verified. This does not claim that >600s commands fit the600s foreground budget.',flush=True);return 0
 except BaseException as e:
  state.update(status='STOPPED: actual failure/interruption retained; no automatic retries or inherited resumption',error=str(e),finished_unix=time.time());save(out/'MATRIX-STATE.json',state);raise
 finally:fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
if __name__=='__main__':raise SystemExit(main())
