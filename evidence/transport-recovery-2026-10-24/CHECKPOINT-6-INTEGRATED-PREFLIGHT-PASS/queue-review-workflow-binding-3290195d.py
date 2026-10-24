#!/usr/bin/env python3
"""Audit frozen source commit and distinguish PR, outgoing push and DEV push filters."""
import datetime,hashlib,json,pathlib,re,subprocess
import yaml
R=pathlib.Path('/workspace/chicago')
O=pathlib.Path('/workspace/.cloud-setup/logs/transport-recovery')
H='3290195d40cbacf5cbfd0c76f14119d6712aa30c'
B='29ea317f30ea110c4477e84a8d34b55f9fc50e55'
P='8c45c899f696eb87da9f818828bed36668bdfa2b'
BR='steward/t3083-t3086-t3087-transport-recovery-20261024'
def run(*args,timeout=30):
 p=subprocess.run(['git','-C',str(R),*args],capture_output=True,text=True,timeout=timeout)
 return {'command':['git',*args],'exit_status':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def git(*args):
 r=run(*args)
 if r['exit_status']:raise RuntimeError(r)
 return r['stdout']
def pattern(p):
 s='';i=0
 while i<len(p):
  if p[i:i+2]=='**':s+='.*';i+=2
  elif p[i]=='*':s+='[^/]*';i+=1
  elif p[i]=='?':s+='[^/]';i+=1
  else:s+=re.escape(p[i]);i+=1
 return '^'+s+'$'
def match(p,globs):
 state=False
 for g in globs:
  neg=g.startswith('!')
  if re.fullmatch(pattern(g[1:] if neg else g),p):state=not neg
 return state
pr=git('diff','--name-only',B+'...'+H).splitlines()
push=git('diff','--name-only',P,H).splitlines()
assert len(pr)==59 and len(push)==20
assert git('merge-base',B,H).strip()==B
mtree=run('merge-tree','--write-tree','--messages',B,H)
assert mtree['exit_status']==0
T=git('rev-parse',H+'^{tree}').strip()
assert mtree['stdout'].splitlines()[0]==T=='bac89999d2afd653e632c52d15b2f50336688deb'
remote=run('ls-remote','origin','refs/heads/'+BR)
remote_h=remote['stdout'].split()[0] if remote['exit_status']==0 and remote['stdout'].split() else None
ids={'chicago-4d-check.yml':365585053,'chicago-4d-moving-frames.yml':374947050,'chicago-4d-pr-stuck.yml':365616743,'chicago-4d-humans.yml':380427937}
scenarios=[('PR into dev','pull_request','dev',pr,'actual source B...H'),('planned branch push from prior source P','push',BR,push,'P..H; actual event before SHA must be collected'),('ordinary DEV merge with same resulting tree','push','dev',pr,'B..merged-tree delta; actual squash SHA unknown')]
rows=[]
for f in git('ls-tree','-r','--name-only',H,'.github/workflows/').splitlines():
 raw=git('show',H+':'+f)
 d=yaml.load(raw,Loader=yaml.BaseLoader)
 on=d.get('on') or {}
 row={'path':f,'name':d.get('name'),'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'git_blob':git('rev-parse',H+':'+f).strip(),'documented_workflow_id':ids.get(f.rsplit('/',1)[-1]),'job_keys':list(d.get('jobs',{})),'complete_event_and_filter_configuration':on,'scenario_evaluations':[]}
 for label,event,branch,paths,why in scenarios:
  e={'scenario':label,'event':event,'branch':branch,'path_set':why,'candidate_changed_path_count':len(paths)}
  if event not in on:e.update(expected_trigger=False,reason='event absent')
  else:
   cfg=on[event] or {}
   branch_ok=(not cfg.get('branches') or match(branch,cfg['branches'])) and not (cfg.get('branches-ignore') and match(branch,cfg['branches-ignore']))
   hit=[p for p in paths if match(p,cfg['paths'])] if cfg.get('paths') else paths
   if cfg.get('paths-ignore'):hit=[p for p in hit if not match(p,cfg['paths-ignore'])]
   e.update(expected_trigger=bool(branch_ok and hit),branch_filter_matches=bool(branch_ok),path_filter_matches=len(hit),matching_paths=hit if cfg.get('paths') or cfg.get('paths-ignore') else 'unfiltered')
  row['scenario_evaluations'].append(e)
 rows.append(row)
bake=next(x for x in rows if x['path'].endswith('/chicago-4d-bake.yml'))
bake_owned=[p for p in pr if match(p,bake['complete_event_and_filter_configuration']['push']['paths'])]
assert not bake_owned
receipt={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':H,'tree':T,'reviewed_dev_base':B,'actual_commit_parents':git('show','-s','--format=%P',H).strip().split(),'merge_base':B,'tracked_status_at_audit':git('status','--porcelain','--untracked-files=no'),'prior_pushed_source':P,'remote_ref_observation':remote,'remote_head_at_observation':remote_h,'planned_push_from_P_applicable_to_observed_remote':remote_h==P,'actual_PR_changed_paths':pr,'planned_branch_push_changed_paths':push,'actual_executed_merge_tree_command_and_result':mtree,'workflow_inventory':rows,'bake_branch_ownership_screen':{'workflow_changed_since_previous_source':'.github/workflows/chicago-4d-bake.yml' in push,'expected_push_path_matches':[p for p in push if match(p,bake['complete_event_and_filter_configuration']['push']['paths'])],'owned_PR_bake_paths':bake_owned,'expected_screen_result':'warranted q emits bake=0 if current readable origin/dev is reviewed B; downstream conditional bake/smoke jobs skip. This is a source prediction, not an actual Actions result.','actual_screen_executed_locally':False,'incoming_checkout_change':'warranted actions/checkout@v4 now has fetch-depth:0 and filter:blob:none; this is included in this H workflow hash.'},'actual_new_run_ids':[],'server_protection_rules_read':False,'network_status':'api.github.com still destination-policy blocked per root; only ordinary read-only native git ls-remote used here. No API writes, PR dispatch, rerun or merge attempted.','prior_receipt_limitation':'Old 8c45-vs29ea receipt is preserved unchanged. It evaluated branch push filters on PR-owned paths. This receipt separates each event path set; notably incoming bake workflow/generators trigger normal bake warranted on P..H push.','local_validation':'Root reports canonical derived tail passed59steps, one unchanged lap214.547s. Root reports fresh full preflight running; this audit neither executes nor declares its outcome.','exact_head_collection_plan':['Reverify actual final PR base/head and complete files. These predictions apply only to H/tree T and reviewed B; DEV/head movement needs fresh binding.','Collect normal gate PR workflow365585053, moving-frames PR374947050, report branch push365616743. Workflow identities come from WORKPLAN-PEOPLE-TRANSPORT.md:42, not discovered run IDs.','Also collect actual normal content-build push run on H caused by incoming paths; verify warranted succeeded and actual downstream result. No workflow ID is invented for bake.','Match source push checkout H; for PR synthetic merge Q verify actual parents[B,H] and expected tree T. Save actual raw workflow/run/job/check/status/log receipts and latest attempts.','Unknown, missing, pending, cancelled or unreadable is not green. Path-filter N/A is no new check, not a fabricated success. Collect any other actual head check as well.','Require complete final-tree preflight and published smoke both viewports, current normal green checks, ordinary SHA-pinned squash into DEV on current clean mergeability; no admin, bypass, dispatch or invented metadata.','Recheck PR head/base/draft/hold and lap lock before ordinary merge, then verify resulting DEV source tree/public asset hashes. Close only shipping children; no broad photographic/native-world completion or production promotion.']}
path=O/'queue-review-workflow-binding-3290195d-vs-29ea317f.json'
path.write_text(json.dumps(receipt,indent=2)+'\n')
print(path)
print('head',H,'tree',T,'base',B,'PR_paths',len(pr),'planned_push_paths',len(push),'remote',remote_h)
for row in rows:
 if any(e['expected_trigger'] for e in row['scenario_evaluations']):
  print(row['name'],[(e['scenario'],e['expected_trigger'],e.get('path_filter_matches')) for e in row['scenario_evaluations']])
print('merge-tree command exit',mtree['exit_status'],'result',mtree['stdout'].strip())
print('No new run IDs discovered. No heavy tests performed.')
