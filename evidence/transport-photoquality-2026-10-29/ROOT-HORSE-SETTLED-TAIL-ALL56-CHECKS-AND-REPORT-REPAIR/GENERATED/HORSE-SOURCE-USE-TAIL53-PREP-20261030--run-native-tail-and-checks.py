#!/usr/bin/env python3
"""Root-owned H native tail53 and all affected output checks; source protocol only."""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,math,os,re,shutil,sys,time,subprocess
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
BASE=Path('/tmp/HORSE-FULL-GATE-RETRY02-PREP-20261030/run-guarded-whole-gate.py')
BASE_SHA='4935cd9e22dab49b7b60233f2e7633801b7af091abd9eecc63fa875b05c666d4'
R=Path('/tmp/chicago-horse-20261029');A=R/'chicago/4d';MANIFEST=A/'tools/derived_manifest.json'
OLD='ddb77c3191c6fbf28953b8b96f2477bf91f088cb';TREE='9e3d17f39e5cec9be13d155eb8a273816e55195c';APP='11da9f86196ed4e3ebbcd694f1868487141a1246';INDEX='277c26af03ece19bf0d26e3a37494cafe592be8f4bb769c5fd096ef908a58ed4'
CERT=A/'data/transport/parked/standing-horse-planted/quiet-head-neck-v6-qualification-summary.json';CERT_SHA='badca71fb2ab7596be9447adaf01b3d035d5a59c7b844bc27b500d0a004d78a6'
REPORT='chicago/4d/docs/measurements/source_use_coverage.md';MF_REL='chicago/4d/tools/derived_manifest.json'
E={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_TERMINAL_PROMPT':'0','GIT_OPTIONAL_LOCKS':'0'}
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);assert p.is_file()and not p.is_symlink(),p;b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false',*args],cwd=R,env={**E,'GIT_NO_LAZY_FETCH':'1'})
def clean_graph_sourceuse_resolves(m):
 m=json.loads(json.dumps(m));matches=[s for s in m['steps'] if s['command']==['python3','tools/compile_source_use.py']];assert len(matches)==1;matches[0]['resolves']='NATIVE_SOURCE_USE_COMPILER_OWNS_THIS_ENUMERATION_T3131';return m
def changed_files():
 rows=[]
 for raw in git('diff','--name-only','-z','--').split(b'\0'):
  if not raw:continue
  rel=os.fsdecode(raw);p=R/rel;assert p.is_relative_to(R)
  rows.append(dict(path=rel,deleted=True)if not p.exists()else dict(path=rel,deleted=False,mode=oct(p.stat().st_mode&0o777),bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
 return rows
def protected_source(before,initial_index):
 assert git('rev-parse','HEAD').decode().strip()==OLD and git('branch','--show-current').decode().strip()=='steward/t3088-horse-photoquality-20261026'
 assert git('ls-files','--stage','-z')==initial_index and sha(initial_index)==INDEX
 assert not git('ls-files','--others','--exclude-standard','-z')
 for row in before['source_files']:
  if row['path'] in {REPORT,MF_REL}:continue
  actual=pin(R/row['path']);assert(actual['bytes'],actual['sha256'])==(row['bytes'],row['sha256']),row['path']
 assert pin(CERT)['sha256']==CERT_SHA
 spec=importlib.util.spec_from_file_location('actual_horse_tail_canonical_guard',A/'tools/transport/horse_quiet_head_neck_idle_v6/canonical_guard.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);actual_code=module.code_pins();assert len(actual_code)==63 and actual_code==load(CERT)['actual_code_pins']
 changes=changed_files()
 for row in changes:
  rel=row['path'];assert not(rel.startswith('chicago/4d/assets/')or rel.startswith('chicago/4d/renderers/')),'Native metadata tail may not modify models/renderers'
  assert not(rel.startswith('chicago/4d/tools/')and rel!=MF_REL),'Native metadata tail may not modify tools except legitimate source-use ownership enumeration'
 return dict(head=OLD,staged_tree=TREE,staged_app_tree=APP,semantic_index_sha256=INDEX,source117_protected_except_declared_report_and_native_sourceuse_resolves=True,all63_qualifier_code_pins_exact=True,finite_certificate_exact=True,unstaged_changes=changes)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root-owned-tail-go',required=True,action='store_true');ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();start=time.monotonic();deadline=start+1200;out=args.out.resolve();assert out.is_relative_to(Path('/tmp'))and not out.is_relative_to(R)and not out.exists();out.mkdir(mode=0o700);scratch=None;before=None;initial_index=None;before_resources=None;pair=None;errors=[];tail=None;checks=None;changed_after_tail=None;phase=[];attempted_prefixes=[];state=dict(at=now(),status='ACTUAL_NATIVE_TAIL_AND_ALL_AFFECTED_CHECKS_PENDING',source_or_index_staged=False,feature_commit_push=False,full_check_sh_PASS_claimed=False,overall_cap_seconds=1200,tail_cap_seconds=600,verification_cap_seconds=600,closure_reserve_seconds=30)
 save(out/'ACTUAL-SOURCE-USE-TAIL-CLOSED.json',state)
 assert pin(BASE)['sha256']==BASE_SHA;spec=importlib.util.spec_from_file_location('reviewed_fullgate_helpers',BASE);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
 cfg=load(P/'PINS.json')
 for row in cfg['files']:assert pin(row['path'])==row,row['path']
 assert pin(base.SUP)['sha256']==base.SUP_SHA and pin(base.POLICY)['sha256']==base.POLICY_SHA
 policy=base.policy();manifest_before=load(MANIFEST);assert pin(MANIFEST)==cfg['manifest_before'];assert manifest_before['after_the_pass']['max_laps']==3
 sourceuse=next(i for i,s in enumerate(manifest_before['steps'])if s['command']==['python3','tools/compile_source_use.py']);assert sourceuse==151 and len(manifest_before['steps'][sourceuse:])==53
 c=load('/tmp/HORSE-ACTUAL-FULL-GATE-SHM-20261030-02/ACTUAL-WHOLE-GATE-CLOSED.json');assert c['worker']=='H'and c['status']=='NONPASS_FULL_NATIVE_CHECK_SH_OR_SOURCE_RESOURCE_CLOSURE'and c['tree']==TREE and c['app_tree']==APP and c['source_index_unchanged']and c['errors']==[] and c['native_cleanup']['cleanup_complete']and c['native_cleanup']['remaining_owned_children']==[]
 try:
  before_resources=policy.snapshot();assert policy.check_snapshot(before_resources)['accepted'];assert not base.active_owners();save(out/'RESOURCES-BEFORE.json',before_resources)
  before,initial_index=base.source_snapshot(base.CONFIG['H']);assert sha(initial_index)==INDEX;save(out/'SOURCE-BEFORE.json',before);(out/'COMPLETE-INDEX-BEFORE.z').write_bytes(initial_index);(out/'ORIGINAL-derived_manifest.json').write_bytes(MANIFEST.read_bytes())
  scratch=base.owned_scratch('h-source-use-tail');admission=base.filesystem_state(scratch);admission.update(base.copy_demand(base.CONFIG['H']));assert admission['block_bytes']==4096 and admission['available_bytes']>=admission['mandatory_native_synthesis_copy_bytes']+admission['scratch_reserve_bytes'];save(out/'ACTUAL-SHM-ADMISSION.json',admission);save(out/'ACTUAL-SAMEEXEC-SHM-PROBE.json',base.scratch_probe(scratch))
  env={**E,'TMPDIR':str(scratch),'C4D_GATE_REQUIRE_READERS':'1','C4D_GATE_REQUIRE_BASE':'1','CHECK_JOBS':'4','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'};env.pop('GIT_NO_LAZY_FETCH',None)
  def owned(label,cmd,cap):
   prefix=out/label;argv=[sys.executable,str(base.SUP),'--prefix',str(prefix),'--cwd',str(A),'--timeout',str(cap),'--',*cmd];attempted_prefixes.append(prefix);save(out/'ACTUAL-ATTEMPTED-NATIVE-PHASES.json',dict(prefixes=[str(p)for p in attempted_prefixes]));rc=subprocess.run(argv,cwd=A,env=env).returncode;result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');phase.append(dict(label=label,command=cmd,cap_seconds=cap,result=result,cleanup=cleanup));assert result['command']==cmd and result['cwd']==str(A)and result['requested_timeout_seconds']==result['effective_timeout_seconds']==cap and result['timeout_override_reason']is None;assert cleanup['cleanup_complete']and cleanup['remaining_owned_children']==[];assert rc==result['returncode']==0 and not result['timed_out'],label;return result
  assert deadline-time.monotonic()-30>=600,'Native tail600 must fit within remaining1170 work window before launch'
  tail=owned('native-tail',['node','tools/rederive.mjs','--tail','tools/compile_source_use.py'],600)
  text=(out/'native-tail.log').read_text(errors='replace');settled=re.findall(r'derived layer rebuilt from step (\d+) — (\d+) step\(s\) in manifest order, (\d+) lap\(s\), and the last one moved nothing; no second pass',text);assert len(settled)==1 and settled[0][:2]==('152','53')and 1<=int(settled[0][2])<=3 and 'WARNING:'not in text,'Actual native tail must settle; its warning/RC0 is insufficient'
  manifest_after=load(MANIFEST);assert clean_graph_sourceuse_resolves(manifest_before)==clean_graph_sourceuse_resolves(manifest_after),'Only native source-use resolves enumeration may change in the declared graph'
  after_tail=protected_source(before,initial_index);changed_after_tail=after_tail['unstaged_changes'];declared=set().union(*(set(s.get('resolves',[]))for s in manifest_after['steps'][sourceuse:]))|{MF_REL};assert all(row['path']in declared for row in changed_after_tail),'Tail changed an output outside its declared ownership; retain actuals for review'
  save(out/'SOURCE-AFTER-NATIVE-TAIL.json',after_tail);save(out/'NATIVE-SETTLEMENT.json',dict(start_step=152,steps=53,actual_laps=int(settled[0][2]),max_laps=3,actual_last_lap_moved_nothing=True,native_warning_accepted=False,manifest_before=cfg['manifest_before'],manifest_after=pin(MANIFEST)))
  for row in cfg['files']:assert pin(row['path'])==row,row['path']
  remaining=math.floor(deadline-time.monotonic()-30);assert remaining>0,'Actual verification must leave original30s closure reserve';verify_cap=min(600,remaining)
  checks=owned('native-affected-checks',[sys.executable,str(P/'run-affected-native-checks.py'),'--commands',str(P/'NATIVE-AFFECTED-CHECKS.json'),'--commands-sha',cfg['commands_sha256'],'--out',str(out/'affected-checks')],verify_cap)
  verify=load(out/'affected-checks/ACTUAL-ALL-AFFECTED-CHECKS.json');assert verify['status']=='ACTUAL_ALL_56_NATIVE_OWNER_AND_UPSTREAM_CHECKS_PASS'and len(verify['commands'])==56 and all(row['returncode']==0 for row in verify['commands'])
  assert protected_source(before,initial_index)['unstaged_changes']==changed_after_tail,'Affected output checks must leave all actual derived outputs unchanged';assert clean_graph_sourceuse_resolves(manifest_before)==clean_graph_sourceuse_resolves(load(MANIFEST))
 except BaseException as error:errors.append(repr(error))
 finally:
  if before is not None:
   try:state['source_after']=protected_source(before,initial_index);save(out/'SOURCE-AFTER.json',state['source_after'])
   except BaseException as error:errors.append('SOURCE: '+repr(error))
  if scratch is not None:
   try:
    observed_cleanup=[]
    for prefix in attempted_prefixes:
     path=Path(str(prefix)+'.cleanup.json');value=load(path)if path.is_file()else None;observed_cleanup.append(dict(prefix=str(prefix),actual_cleanup=pin(path)if value is not None else None,complete_zero=(value is not None and value.get('cleanup_complete')is True and value.get('remaining_owned_children')==[])))
    all_owned_closed=all(row['complete_zero']for row in observed_cleanup);save(out/'ACTUAL-NATIVE-CLEANUP-BEFORE-SHM-REMOVAL.json',dict(native_attempted=bool(attempted_prefixes),phases=observed_cleanup,all_attempted_phases_actually_closed_zero=all_owned_closed))
    assert all_owned_closed,'Actual owned cleanup absent/incomplete: retain this owned scratch and do not remove files that native descendants may still use'
    assert scratch.parent==base.OWNED and not scratch.is_symlink();save(out/'SHM-BEFORE-OWNED-CLEANUP.json',base.filesystem_state(scratch));shutil.rmtree(scratch);assert not scratch.exists();state['owned_SHM_scratch_removed']=True;save(out/'SHM-AFTER-OWNED-CLEANUP.json',base.filesystem_state(base.OWNED))
   except BaseException as error:errors.append('OWNED_SCRATCH: '+repr(error))
  if before_resources is not None:
   try:
    after_resources=policy.snapshot();pair=policy.check_pair(before_resources,after_resources);owners=base.active_owners();save(out/'RESOURCES-AFTER.json',dict(snapshot=after_resources,pair=pair,active_owners=owners));assert pair['accepted']and not owners;state['resource10_pair']=pair
   except BaseException as error:errors.append('RESOURCE10: '+repr(error))
  try:
   for row in cfg['files']:assert pin(row['path'])==row,row['path']
   assert time.monotonic()<=deadline,'Actual entire controller exceeded original1200 envelope'
  except BaseException as error:errors.append('CODE_OR_TOTAL_BOUND: '+repr(error))
 passed=not errors and tail is not None and checks is not None and pair is not None and pair['accepted']and state.get('owned_SHM_scratch_removed')is True
 state.update(at=now(),status='ACTUAL_NATIVE_TAIL53_SETTLED_ALL56_AFFECTED_CHECKS_PASS_SOURCE_INDEX_RESOURCE_CLOSED'if passed else'NONPASS_NATIVE_OWNER_TAIL_OR_AFFECTED_CHECKS_OR_SOURCE_RESOURCE_CLOSURE',seconds=time.monotonic()-start,phases=phase,errors=errors,actual_derived_changes=changed_after_tail,new_source_staging_and_full03='PENDING_ROOT_ACTUAL_SCOPE_REVIEW',feature_commit_push=False,full_check_sh_PASS_claimed=False)
 save(out/'ACTUAL-SOURCE-USE-TAIL-CLOSED.json',state);print(json.dumps({'status':state['status'],'seconds':state['seconds'],'errors':errors,'changed_paths':[x['path']for x in changed_after_tail or []]}));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
