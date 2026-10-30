import argparse,datetime,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent; R=Path('/tmp/chicago-wagon-20261029'); A=R/'chicago/4d'; L=O.parent.parent
SUP='/workspace/.cloud-setup/transport-supervise.py'; BIND=O/'bind-checked-followup-published-source.py'
POLICY_PATH=O/'resource_admission_v10.py';POLICY_SHA256='eebdd83e057f31bc44f76e0b85acf037f28e4d06807c1070346e4e2802b6d65d'
assert hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest()==POLICY_SHA256
spec=importlib.util.spec_from_file_location('reviewed_resource10',POLICY_PATH);policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
BASELINE_PATH=policy.BASELINE_PATH;BASELINE_SHA256=policy.BASELINE_SHA256;BASELINE_EVENTS=policy.trusted_baseline()['events_baseline']
p=argparse.ArgumentParser();p.add_argument('--desktop3-reconciliation',required=True);p.add_argument('--desktop3-reconciliation-sha256',required=True);args=p.parse_args()
assert re.fullmatch('[0-9a-f]{64}',args.desktop3_reconciliation_sha256),'ActualreviewedreconciliationSHAisrequired; no placeholder'
RECON_PATH=Path(args.desktop3_reconciliation);assert hashlib.sha256(RECON_PATH.read_bytes()).hexdigest()==args.desktop3_reconciliation_sha256
recon=json.loads(RECON_PATH.read_bytes());assert recon['schema']=='explicit-native-pass-resource10-source-current-reconciliation-v1'and recon['result'].startswith('PASS')
assert recon['policy_code']=={'path':str(POLICY_PATH),'sha256':POLICY_SHA256}and recon['trusted_initial_baseline_sha256']==BASELINE_SHA256
assert recon['original_fixed_counter_resource_verdict_preserved_NONPASS']is True and recon['new_browser_or_native_test_run_performed']is False and recon['original_artifacts_rewritten']is False and recon['whole_published_gate_PASS']is False
assert recon['current_postclosure_resource_check']['accepted']and recon['original_before_healthy_under_resource10']['accepted']and recon['original_event_transition_under_resource10']['accepted']
plan=json.loads((O/'ACTUAL-NEWHEAD-NATIVE-SMOKE-PLAN-SUMMARY.json').read_bytes());receipt=json.loads((O/'ACTUAL-NORMAL-CHECKED-FOLLOWUP-PUSH.json').read_bytes());assert(plan['HEAD'],plan['TREE'],plan['APP'])==(receipt['HEAD'],receipt['TREE'],receipt['APP'])
bridge=json.loads((O/'TARGETED-TO-COMMITTED-PUBLISH-COVERAGE-BRIDGE.json').read_bytes());assert bridge['result'].startswith('PASS')and bridge['committed_HEAD']==plan['HEAD']and(bridge['TREE'],bridge['APP'])==(plan['TREE'],plan['APP'])
# Both first-profile groups have actually closed and been rebound, before this
# controller is started. Never assume an existing unclosed transcript is a PASS.
for v in ['MOBILE','DESKTOP']:
 d=json.loads((Path('/tmp')/f'WAGON-OWNBOUND-PUBLISHED-{v}-STAGE1-01/ACTUAL-PARTIAL-VERDICT.json').read_bytes())
 assert d['result'].startswith('PASS') and d['cleanup_complete'] and d['remaining_owned_children']==0
 assert d['HEAD']==plan['HEAD']
rows=[r for r in plan['groups'] if r['stage']!='1'and not(r['viewport']=='mobile'and r['stage']=='2-3')];assert len(rows)==25;completed=[]
prior=json.loads((O/'REMAINING-NATIVE-PUBLISHED-GROUPS-STOPPED10-DESKTOP4-TIMEOUT-20261030.json').read_bytes())
assert prior['status']=='STOPPED at first actual NONPASS' and len(prior['completed'])==10
assert prior['HEAD']==plan['HEAD']
passed_prior=[x for x in prior['completed']if x['result'].startswith('PASS')];failed_prior=prior['prior_actual_NONPASS']+[x for x in prior['completed']if not x['result'].startswith('PASS')];resource_prior=prior['prior_original_resource_NONPASS']
assert len(resource_prior)==1 and(resource_prior[0]['viewport'],resource_prior[0]['stage'])==('desktop','3')and resource_prior[0]['native_assertions_complete_PASS']is True and resource_prior[0]['resource_event_admission_before_after_PASS']is False
assert [(x['viewport'],x['stage'])for x in passed_prior]==[('mobile','4'),('mobile','5'),('mobile','6'),('mobile','7'),('mobile','8'),('mobile','9'),('mobile','10-11'),('mobile','12'),('mobile','15')]
assert [(x['viewport'],x['stage'])for x in failed_prior]==[('mobile','13'),('mobile','14'),('desktop','2'),('desktop','4')]and all(x['timed_out']for x in failed_prior)
admit=O/'RESUME11-ACTUAL-ADMISSION';admit.mkdir(exist_ok=False)
with(admit/'CURRENT-BINDING.log').open('wb')as f:subprocess.run([sys.executable,str(BIND),'before',str(admit)],cwd=A,stdout=f,stderr=subprocess.STDOUT,check=True)
current_binding=json.loads((admit/'SOURCE-AND-MIRROR-BEFORE.json').read_bytes())
completed=[]
for saved in passed_prior:
 v=saved['viewport'];stage=saved['stage'];attempt='02'if stage in ['4','8','12']else'01'
 out=Path('/tmp')/f'WAGON-OWNBOUND-PUBLISHED-{v.upper()}-STAGE{stage}-{attempt}';prefix=L/f'rail-owned-wagon-bound-published-{v}-{stage}-{attempt}'
 actual=json.loads((out/'ACTUAL-PARTIAL-VERDICT.json').read_bytes());result=json.loads(Path(str(prefix)+'.result.json').read_bytes());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_bytes())
 assert actual==saved and actual['result'].startswith('PASS') and actual['failed_checks']==0
 assert (actual['HEAD'],actual['TREE'],actual['APP'])==(plan['HEAD'],plan['TREE'],plan['APP'])
 assert result['returncode']==0 and not result['timed_out'] and result['requested_timeout_seconds']==600 and result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None
 assert result['command']==['node','tools/smoke_renderer.mjs','--published']and result['cwd']==str(A)
 assert cleanup['cleanup_complete'] and cleanup['remaining_owned_children']==[]
 assert json.loads((out/'SOURCE-AND-MIRROR-BEFORE.json').read_bytes())==json.loads((out/'SOURCE-AND-MIRROR-AFTER.json').read_bytes())==current_binding
 transcript=Path(str(prefix)+'.log').read_text(errors='replace');summary=re.search(r'(\d+) passed, (\d+) failed',transcript)
 assert 'SMOKE PASS'in transcript and summary and (int(summary[1]),int(summary[2]))==(actual['passed_checks'],0)
 if 'resource_event_admission_before_after_PASS'in actual:
  assert actual['native_assertions_complete_PASS']and actual['resource_event_admission_before_after_PASS']and actual['memory_events_baseline_sha256']==BASELINE_SHA256
  past_resource=json.loads((out/'ACTUAL-CLOSED-MEMORY-EVENTS.json').read_bytes());past_before=json.loads((out/'ACTUAL-LAUNCH-RESOURCES.json').read_bytes())
  assert past_resource['accepted']and past_resource['baseline_sha256']==BASELINE_SHA256 and past_resource['actual_memory_events']==past_resource['baseline_memory_events']==BASELINE_EVENTS and past_before['memory_events']==BASELINE_EVENTS
 completed.append(actual)
skipped={(x['viewport'],x['stage'])for x in completed};assert len(skipped)==9
# Reconciliation is a NEW explicit acceptance, never a rewritten original verdict.
assert(recon['HEAD'],recon['TREE'],recon['APP'])==(plan['HEAD'],plan['TREE'],plan['APP'])and(recon['viewport'],recon['stage'])==('desktop','3')and recon['native_checks']==107 and recon['native_failed_checks']==0
fresh_binding=Path(recon['fresh_source_binding']['path']);assert hashlib.sha256(fresh_binding.read_bytes()).hexdigest()==recon['fresh_source_binding']['sha256']and json.loads(fresh_binding.read_bytes())==current_binding
original_manifest=Path(recon['original_artifact_manifest']['path']);assert recon['original_artifact_manifest']['sha256']=='722d3b14eeba315f3302e014f53212717a3c35d3986430cf374056d730adb3da'and hashlib.sha256(original_manifest.read_bytes()).hexdigest()==recon['original_artifact_manifest']['sha256']
for record in json.loads(original_manifest.read_bytes())['records']:
 path=Path(record['path']);assert path.is_file()and not path.is_symlink()and path.stat().st_size==record['bytes']and hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
assert json.loads(Path(recon['original_verdict']['path']).read_bytes())==resource_prior[0]
reconciled_keys={('desktop','3')};reconciled=[dict(viewport='desktop',stage='3',acceptance='Explicitresource10current-source/postclosurehealthyreconciliation; originalresourceNONPASSpreserved',receipt_path=str(RECON_PATH),receipt_sha256=args.desktop3_reconciliation_sha256,original_verdict=resource_prior[0])]
(admit/'ACTUAL-VALIDATED-CLOSED-GROUPS.json').write_text(json.dumps(dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),HEAD=plan['HEAD'],completed=completed,reconciled_existing_native_PASS=reconciled,remaining_groups=15,source_index_fullmirror_exact=True),indent=2)+'\n')
# Both actualtimeouts remain immutable UNQUALIFIED evidence; never completedPASS.
for failed in failed_prior:
 failed_out=Path('/tmp')/f"WAGON-OWNBOUND-PUBLISHED-{failed['viewport'].upper()}-STAGE{failed['stage']}-01";failed_prefix=L/f"rail-owned-wagon-bound-published-{failed['viewport']}-{failed['stage']}-01"
 assert json.loads((failed_out/'ACTUAL-PARTIAL-VERDICT.json').read_bytes())==failed
 failed_result=json.loads(Path(str(failed_prefix)+'.result.json').read_bytes());failed_cleanup=json.loads(Path(str(failed_prefix)+'.cleanup.json').read_bytes())
 assert failed_result['returncode']==124 and failed_result['timed_out'] and failed_result['requested_timeout_seconds']==600 and failed_result['effective_timeout_seconds']==600 and failed_result['timeout_override_reason']is None
 assert failed_cleanup['cleanup_complete'] and failed_cleanup['remaining_owned_children']==[]
 assert json.loads((failed_out/'SOURCE-AND-MIRROR-BEFORE.json').read_bytes())==json.loads((failed_out/'SOURCE-AND-MIRROR-AFTER.json').read_bytes())==current_binding
deferred={(v,s)for v in ['mobile','desktop']for s in ['13','14']}|{('desktop','2'),('desktop','4')}
deferred_ledger=[dict(viewport=v,stage=s,status='DEFERRED UNQUALIFIED; no PASS coverage',reason='Actualoriginal600timeouts:mobile13/14anddesktop2/4. Desktop13/14UNRUN. Existingnativehasnowithin-partselector; pendingindependentruntime/fullassertionsolution.',this_slot_actual_NONPASS=(v=='mobile'or s in ['2','4']),supporting_actual_failure_verdict=(str(Path('/tmp')/f"WAGON-OWNBOUND-PUBLISHED-{v.upper()}-STAGE{s}-01/ACTUAL-PARTIAL-VERDICT.json")if(v=='mobile'or s in ['2','4'])else None))for v,s in sorted(deferred)]
(admit/'ACTUAL-DEFERRED-UNQUALIFIED-LEDGER.json').write_text(json.dumps(dict(HEAD=plan['HEAD'],deferred=deferred_ledger,actual_pending_total=15,runnable_commands=9,whole_gate='PENDING'),indent=2)+'\n')
(O/'EXTERNAL-CONTROLLER-11.pid').write_text(str(os.getpid())+'\n')

S=O/'REMAINING-NATIVE-PUBLISHED-GROUPS-ACTUAL-STATE.json'
def save(status,**kw):
 passed_count=sum(x['result'].startswith('PASS')for x in completed)+len(reconciled_keys)
 data=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),HEAD=plan['HEAD'],status=status,completed=completed,reconciled_existing_native_PASS=reconciled,prior_original_resource_NONPASS=resource_prior,remaining_groups=len(rows)-passed_count,remaining_runnable_groups=len(rows)-len(deferred)-passed_count,deferred_unqualified=deferred_ledger,prior_actual_NONPASS=failed_prior,whole_gate='PENDING: BOTHstage13and14partsANDdesktop2and4UNQUALIFIED untilactualfullassertionPASS plus everyotherrequiredgroup',**kw)
 S.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data),flush=True)
try:
 for row in rows:
  if(row['viewport'],row['stage'])in skipped or(row['viewport'],row['stage'])in reconciled_keys or(row['viewport'],row['stage'])in deferred:continue
  pause=Path('/workspace/.cloud-setup/transport-browser-resource-pause.json')
  if pause.exists():
   save('WAITING root pause before preparing next native group; no browser/native launched',active=row,pause_file=str(pause))
   while pause.exists():time.sleep(.25)
  v=row['viewport'];stage=row['stage'];attempt='02'if v=='mobile'and stage in ['4','8','12']else'01';out=Path('/tmp')/f'WAGON-OWNBOUND-PUBLISHED-{v.upper()}-STAGE{stage}-{attempt}';prefix=L/f'rail-owned-wagon-bound-published-{v}-{stage}-{attempt}'
  assert not out.exists() and not Path(str(prefix)+'.log').exists(),f'Existing actual group must be reviewed, never overwritten: {out}'
  save('PREPARING next native group',active=row,prefix=str(prefix),output=str(out))
  out.mkdir();(out/'PNGS').mkdir()
  with (out/'STANDING-RECORD.log').open('wb')as f:subprocess.run(['node','tools/dev-smoke-state.mjs','ask','--viewport',v,'--stage',stage],cwd=A,stdout=f,stderr=subprocess.STDOUT,check=True)
  with(out/'BINDING-BEFORE.log').open('wb')as f:subprocess.run([sys.executable,str(BIND),'before',str(out)],cwd=A,stdout=f,stderr=subprocess.STDOUT,check=True)
  resource=policy.snapshot();admission=policy.check_snapshot(resource)
  (out/'ACTUAL-LAUNCH-RESOURCES.json').write_text(json.dumps(resource,indent=2)+'\n')
  (out/'ACTUAL-RESOURCE-ADMISSION-BEFORE.json').write_text(json.dumps(admission,indent=2)+'\n')
  assert admission['accepted'],'Resource10launchfloor/nonmaxcounter/keyset/monotonicinitialguardfailed; no browserlaunched'
  assert not Path('/workspace/.cloud-setup/transport-browser-resource-pause.json').exists(),'Root browser pause active; no browser launched'
  tmp=Path('/tmp')/f'wg-bound-{v[0]}{stage.replace("-", "_")}-r{attempt}';tmp.mkdir(mode=0o700,exist_ok=False)
  env={**os.environ,'TMPDIR':str(tmp),'SMOKE_VIEWPORT':v,'SMOKE_STAGE':stage,'SMOKE_TIMING':'1','SMOKE_SHOTS':str(out/'PNGS')}
  save('RUNNING actual native group',active=row,prefix=str(prefix),output=str(out))
  rc=subprocess.run([sys.executable,SUP,'--prefix',str(prefix),'--cwd',str(A),'--timeout','600','--','node','tools/smoke_renderer.mjs','--published'],cwd=A,env=env).returncode
  result=json.loads(Path(str(prefix)+'.result.json').read_bytes());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_bytes())
  with(out/'BINDING-AFTER.log').open('wb')as f:subprocess.run([sys.executable,str(BIND),'after',str(out)],cwd=A,stdout=f,stderr=subprocess.STDOUT,check=True)
  transcript=Path(str(prefix)+'.log').read_text(errors='replace');summary=re.search(r'(\d+) passed, (\d+) failed',transcript)
  passed=rc==0 and result['returncode']==0 and not result['timed_out'] and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']and 'SMOKE PASS'in transcript and summary is not None and int(summary[2])==0
  native_passed=passed
  resource_after=policy.snapshot();resource_pair=policy.check_pair(resource,resource_after)
  (out/'ACTUAL-CLOSED-RESOURCES.json').write_text(json.dumps(resource_after,indent=2)+'\n')
  (out/'ACTUAL-RESOURCE-PAIR-VERDICT.json').write_text(json.dumps(resource_pair,indent=2)+'\n')
  post_resource=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_memory_events=resource_after['memory_events'],before_memory_events=resource['memory_events'],trusted_initial_baseline_events=BASELINE_EVENTS,baseline_path=str(BASELINE_PATH),baseline_sha256=BASELINE_SHA256,policy_code_sha256=POLICY_SHA256,max_counter_policy='INFORMATIONALmonotonic;allnonmax0;resourceshealthyBOTHends',event_transition=resource_pair['events'],accepted=resource_pair['accepted'],native_assertions_complete_PASS=native_passed)
  (out/'ACTUAL-CLOSED-MEMORY-EVENTS.json').write_text(json.dumps(post_resource,indent=2)+'\n')
  passed=native_passed and resource_pair['accepted']
  verdict=dict(native_assertions_complete_PASS=native_passed,resource_event_admission_before_after_PASS=resource_pair['accepted'],resource_admission_policy_version='resource10',resource_policy_sha256=POLICY_SHA256,resource_complete_before_after_PASS=resource_pair['accepted'],memory_events_baseline_sha256=BASELINE_SHA256,HEAD=plan['HEAD'],TREE=plan['TREE'],APP=plan['APP'],passed_checks=int(summary[1])if summary else None,failed_checks=int(summary[2])if summary else None,result='PASS native partial group only'if passed else'NONPASS actual native partial group',viewport=v,stage=stage,seconds=result['seconds'],timed_out=result['timed_out'],cleanup_complete=cleanup['cleanup_complete'],remaining_owned_children=len(cleanup['remaining_owned_children']),source_index_fullmirror_unchanged=True,whole_published_gate='PENDING until all required groups pass')
  (out/'ACTUAL-PARTIAL-VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n');completed.append(verdict)
  if not passed:save('STOPPED at first actual NONPASS',active=row,prefix=str(prefix));raise SystemExit(1)
  save('CLOSED PASS partial group; preparing next',last=row)
 save('ALL9 remaining RUNNABLEgroups closedPASS; BOTHstage13and14partsANDdesktop2and4remainUNQUALIFIED',whole_gate_candidates='PENDING: phone13and14plusdesktop2and4actual600NONPASS;desktop13and14UNRUN;nowholepublishedgate/CI/mergeclaim')
except BaseException as err:
 if not isinstance(err,SystemExit):save('STOPPED exception/resource/source issue; inspect actuals before resuming',error=repr(err))
 raise
