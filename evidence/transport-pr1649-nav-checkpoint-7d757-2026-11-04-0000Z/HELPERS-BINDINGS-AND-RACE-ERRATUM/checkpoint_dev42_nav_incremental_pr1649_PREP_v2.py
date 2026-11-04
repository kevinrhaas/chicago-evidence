"""Owner-requested incremental FEATURE branch checkpoint; full preflight stays pending.

This never merges DEV. It keeps actual targeted/publication proofs and the prior-source negatives,
commits their exact staged tree, runs actual-commit QA, and normally pushes.
"""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys,time
P=Path(__file__).resolve().parent;R=Path('/workspace/chicago-transport-current-20261103');A=R/'chicago/4d'
SUP=Path('/workspace/.cloud-setup/transport-supervise.py');BRANCH='steward/t3088-horse-photoquality-20261026'
ap=argparse.ArgumentParser();ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--message',type=Path,required=True);args=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*cmd):return subprocess.check_output(['git','-C',str(R),*cmd],env=env,timeout=45)
def val(*cmd):return git(*cmd).decode().strip()
def api():return json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/pulls/1649?incremental_checkpoint_readback='+str(time.time_ns())],env=env,timeout=40))
b=load(args.binding);expected=b['source'];OLD=expected['HEAD'];BASE=expected['MERGE_HEAD'];TREE=expected['TREE'];APP=expected['APP'];SEM=expected['semantic_index_sha256']
assert b['template_only']is False
assert b['policy']=='OWNER_AUTHORIZED_INCREMENTAL_FEATURE_BRANCH_CHECKPOINT'
assert b['full_native_preflight_and_CI_required_before_DEV_merge']is True
assert b['user_authorization_quotes']==['commit to GitHub periodically','you don’t have to make things perfect before pushing and committing a ticket to dev, you can make incremental progress']
assert OLD=='d0671d821ba861a171fbd3394b22e4ed496dceda'and BASE=='42b9c601d51d8a93cde2706e1773f0bd00fadfbe'
assert TREE=='9c4550f9f49dd33a9b4d5262b92cf25a234f5ed2'and APP=='92a63744fe38744fe1df5c7a501ad754ed2c5fc7'and SEM=='bfef2cf0ed3a65070053d3cac9989f78150dec2ca5f55b565e7695e28210548f'
assert b['native_tail_fixedpoint_PASS_claimed']is False
assert b['current_source_world_interaction_status']=='PENDING'
assert b['full_actual_published_interactions_required_before_DEV_merge']is True
assert sha(SUP)=='a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
assert sha(P/'resource_guard.py')=='ac68e89608a6828d71d0933a4e3403ca09585a8f362551e28582e33ea4a73a3c'
assert sha(P/'RESTORED-RUNTIME-BASELINE.json')=='3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
def native(row,cap=None):
 x=row['result'];c=row['cleanup'];assert x['returncode']==0 and not x['timed_out']and x['timeout_override_reason']is None
 assert x['requested_timeout_seconds']==x['effective_timeout_seconds']
 if cap is not None:assert x['effective_timeout_seconds']==cap
 assert c['cleanup_complete']and not c['remaining_owned_children']and row['resources']['accepted']
proofs={}
for key in ['targeted_owner_receipt','publication_receipt','patch_adoption_receipt','patch_manifest_receipt','fix_manifest_receipt','retained_native_tail_negative','retained_prior_source_world_negative']:
 ref=b[key];assert sha(ref['path'])==ref['sha256'];proofs[key]=load(ref['path'])
assert b['targeted_owner_receipt']==dict(path=str(P/'actual-dev42-rail-targeted-and-reports-01/CLOSED.json'),sha256='d850c38e6a7cd28d099ad1340cc664fe04ea301ac479b190604c542ad1ec8dc2')
assert Path(b['publication_receipt']['path'])==P/'actual-staged-dev42-rail-publication-01/CLOSED.json'
assert b['patch_adoption_receipt']==dict(path=str(P/'ROOT-RAIL-PRELOAD-ADOPTION.json'),sha256='e7a1926edff0a5c391788731b352f8f5076e84d91e662260bcf5ad249f0c02f1')
assert Path(b['patch_manifest_receipt']['path'])==P/'rail-code-preload-dev42-01/PREPARED-MANIFEST.json'
assert b['fix_manifest_receipt']==dict(path=str(P/'DEV42-ALL-THIRTEEN-RAIL-FIXES.json'),sha256='60b970b134062724451d5a6b3dcfccb4c7bacd19b5f8b8a273edb62a2251bf29')
assert b['retained_native_tail_negative']==dict(path=str(P/'actual-dev42-native-report-tail-01/CLOSED.json'),sha256='ceda5106b6d2d45ba02b5e0e567083f6e4cff32771bd3c6f056e93e72eb9269a')
assert b['retained_prior_source_world_negative']==dict(path=str(P/'actual-staged-dev42-v8-world-1904-mobile-C-01/CLOSED.json'),sha256='4fbe224bb289f5c8a652b0d29f9cf3bbdbc5f01b64925c9a8b13a5d6aab9cc72')
adoption=proofs['patch_adoption_receipt'];manifest=proofs['patch_manifest_receipt'];patch=Path(adoption['patch'])
assert patch==P/'rail-code-preload-dev42-01/PREPARED-PRELOAD-5-PATH.patch'
assert adoption['patch_sha256']==sha(patch)=='bbfc38348aa8e81c06b703aae87c2e0c37a00d7f095b135d0bd1087067db5c29'
assert manifest['patch']==dict(path=str(patch),sha256=adoption['patch_sha256'])
assert adoption['TREE_before']=='1bc5eec70ab7b415e24d1a2e09bdef1f8b86aee8'and adoption['TREE_after']==TREE and adoption['APP_after']==APP and adoption['semantic_index_sha256']==SEM
patch_paths={'chicago/4d/renderers/web/js/nav-rail.js','chicago/4d/renderers/web/js/navigator.js','chicago/4d/renderers/web/js/main.js','chicago/4d/tools/test_navigator.mjs','chicago/4d/tools/test_driven_assembly.mjs'}
assert set(manifest['base_pins'])==set(manifest['candidate_pins'])==patch_paths
assert set(val('diff','--name-only','--no-renames',adoption['TREE_before'],TREE).splitlines())==patch_paths
for path,h in manifest['base_pins'].items():assert hashlib.sha256(git('show',adoption['TREE_before']+':'+path)).hexdigest()==h
for path,h in manifest['candidate_pins'].items():assert sha(R/path)==h and hashlib.sha256(git('show',TREE+':'+path)).hexdigest()==h
owners=proofs['targeted_owner_receipt'];assert owners['status']=='TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT'and owners['source_after']==expected and owners['resources']['accepted']
assert owners['native_tail_fixedpoint_PASS_claimed']is False and owners['retained_native_tail_negative']==b['retained_native_tail_negative']
assert owners['fix_pins']==proofs['fix_manifest_receipt']['files']and len(owners['fix_pins'])==13
assert all(sha(R/path)==h for path,h in owners['fix_pins'].items())
owner_names=['workflow-shell-syntax','workflow-native-shape','transport-loop','driven-assembly','main-source-syntax','navigator','bake-warranted-self-test','check-liberties','check-source-use']
assert [row['name']for row in owners['ledger']]==owner_names
for row,cap in zip(owners['ledger'],[5,5,5,5,5,5,120,120,120]):native(row,cap)
negative=proofs['retained_native_tail_negative'];assert negative['status']=='NATIVE_REPORT_TAIL_NONPASS_NO_AUTOMATIC_RETRY'
tail=negative['ledger'][-1];tx=tail['result'];tc=tail['cleanup']
assert tail['name']=='native-affected-tail'and tx['returncode']==124 and tx['timed_out']and tx['requested_timeout_seconds']==tx['effective_timeout_seconds']==600 and tx['timeout_override_reason']is None
assert tc['cleanup_complete']and not tc['remaining_owned_children']and tail['resources']['accepted']
prior_world=proofs['retained_prior_source_world_negative']
assert prior_world['status']=='ACTUAL_STAGED_PUBLISHED_SCOPE_NONPASS'and prior_world['scope']=='C'and prior_world['scene']=='1904'and prior_world['viewport']=='mobile'
assert prior_world['source_before']==prior_world['source_after']and prior_world['source_after']['APP']=='f770bfe6f8df03cf257b7c73cbc9138b2a2d5a8e'and prior_world['source_after']['TREE']==adoption['TREE_before']
assert prior_world['source_after']['APP']!=APP
wx=prior_world['result'];wc=prior_world['cleanup']
assert wx['returncode']==1 and not wx['timed_out']and wx['requested_timeout_seconds']==wx['effective_timeout_seconds']==600 and wx['timeout_override_reason']is None
assert wc['cleanup_complete']and not wc['remaining_owned_children']and prior_world['resources']['accepted']
# The old source's failure is retained as a failure. This helper does not inspect
# a new-world status or infer its outcome from timing, fixtures, or an older APP.
pub=proofs['publication_receipt'];assert pub['status']=='ACTUAL_STAGED_NATIVE_PUBLICATION_PASS'and pub['source_before']==pub['source_after']==expected and pub['resources']['accepted']and len(pub['ledger'])==2
assert pub['full_all4_commit_CI_DEV_delivery_or_photo_qualification']is False
assert pub['targeted_owner_APP_bridge']['path']==b['targeted_owner_receipt']['path']and pub['targeted_owner_APP_bridge']['sha256']==b['targeted_owner_receipt']['sha256']and pub['targeted_owner_APP_bridge']['source_after']==expected
assert pub['native_build_stamp_old_HEAD_only']==OLD[:10]
for row,cmd,cap in zip(pub['ledger'],[['bash','tools/publish.sh'],['node','tools/check_published.mjs']],[180,120]):native(row,cap);assert row['result']['command']==cmd

def staged():
 assert not git('ls-files','-u').strip()and not git('diff','--name-only').strip()
 assert not git('ls-files','--others','--exclude-standard').strip()
 tree=val('write-tree');return dict(HEAD=val('rev-parse','HEAD'),MERGE_HEAD=val('rev-parse','MERGE_HEAD'),TREE=tree,APP=val('rev-parse',tree+':chicago/4d'),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
def committed(head):
 assert val('rev-parse','HEAD')==head and val('rev-parse','HEAD^{tree}')==TREE and val('rev-parse','HEAD:chicago/4d')==APP
 assert val('show','-s','--format=%P','HEAD').split()==[OLD,BASE]
 assert not git('status','--porcelain','--untracked-files=no').strip()
 assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==SEM
 assert subprocess.run(['git','-C',str(R),'rev-parse','--verify','-q','MERGE_HEAD'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==1
 return dict(HEAD=head,TREE=TREE,APP=APP,semantic_index_sha256=SEM)
assert staged()==expected and val('symbolic-ref','HEAD')=='refs/heads/'+BRANCH
assert val('remote','get-url','origin')=='https://github.com/kevinrhaas/chicago.git'
assert not args.out.exists()and args.message.is_file()
assert 'Checkpoint: owner-requested incremental feature branch; full preflight pending'in args.message.read_text()
args.out.mkdir(parents=True)
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('checkpoint_guard',P/'resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
pins={str(p):sha(p)for p in[Path(__file__),args.binding,args.message,patch,SUP,P/'resource_guard.py',P/'RESTORED-RUNTIME-BASELINE.json',*[Path(b[k]['path'])for k in proofs]]}
rows=[];error=None;head=None;pushed=False;push_command_succeeded=False;Git_remote_readback_verified=False
qa_labels=['HEAD-entry','HEAD-identifiers','HEAD-changelog','HEAD-pending-entry','HEAD-history']
def run(label,cmd,cwd=A,expected_code=0):
 assert all(sha(p)==h for p,h in pins.items());before=guard.snapshot();assert guard.check(before)['accepted'];prefix=args.out/label
 with Path(str(prefix)+'.stdout').open('xb')as f:q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(cwd),'--timeout','120','--',*cmd],env=env,stdout=f,stderr=subprocess.STDOUT)
 result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=guard.pair(before,guard.snapshot());row=dict(label=label,result=result,cleanup=cleanup,resources=resources,log_sha256=sha(str(prefix)+'.log'));rows.append(row);save(args.out/'LEDGER.json',rows)
 assert q.returncode==result['returncode']==expected_code and not result['timed_out']and result['requested_timeout_seconds']==result['effective_timeout_seconds']==120 and result['timeout_override_reason']is None
 assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted']
 return Path(str(prefix)+'.log').read_text(errors='replace')
try:
 pr=api();assert pr['state']=='open'and pr['head']['sha']==OLD and pr['base']['ref']=='dev'and not pr['draft']and all(x['name']!='hold'for x in pr['labels'])
 held=run('own-lap-status',['node','tools/ticket.mjs','lap','1649','--status'],expected_code=3)
 assert 'held lap/pr-1649'in held and 'Codex root checking transport loops and interactions PR1649 before ordinary DEV merge'in held
 assert staged()==expected
 run('normal-checkpoint-commit',['git','commit','-F',str(args.message)],cwd=R)
 head=val('rev-parse','HEAD');save(args.out/'ACTUAL-COMMITTED-SOURCE.json',committed(head))
 checks=[('HEAD-entry',['node','tools/check-changelog-entry.mjs',BASE,'HEAD']),('HEAD-identifiers',['node','tools/resolve_id_collisions.mjs','--base',BASE,'--check']),('HEAD-changelog',['node','tools/check-changelog.mjs']),('HEAD-pending-entry',['node','tools/changelog-entries.mjs','--check']),('HEAD-history',['node','tools/changelog-history.mjs','--base',BASE])]
 for label,cmd in checks:run(label,cmd);committed(head)
 run('HEAD-whitespace',['git','show','--check','--format=oneline','HEAD'],cwd=R)
 assert api()['head']['sha']==OLD and val('ls-remote','origin','refs/heads/'+BRANCH).split()==[OLD,'refs/heads/'+BRANCH]
 run('normal-feature-branch-push',['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=R)
 push_command_succeeded=True
 committed(head);assert val('ls-remote','origin','refs/heads/'+BRANCH).split()==[head,'refs/heads/'+BRANCH]
 Git_remote_readback_verified=True
 pr=api();save(args.out/'PUBLIC-PR-READBACK.json',pr);assert pr['head']['sha']==head and pr['state']=='open'and pr['base']['ref']=='dev';pushed=True
except BaseException as ex:error=repr(ex)
try:final=committed(head)if head else staged();source_error=None
except BaseException as ex:final=None;source_error=repr(ex)
closed=dict(status='OWNER_INCREMENTAL_CHECKPOINT_NORMAL_PUSH_PASS_FULL_PREFLIGHT_PENDING'if pushed and error is None and source_error is None else'INCREMENTAL_CHECKPOINT_NONPASS_NO_AUTOMATIC_RETRY',source=final,source_error=source_error,source_before_commit=expected,parents=[OLD,BASE],exact_tested_staged_TREE_committed=head is not None,targeted_owner_receipt=b['targeted_owner_receipt'],publication_receipt=b['publication_receipt'],patch_adoption_receipt=b['patch_adoption_receipt'],patch_manifest_receipt=b['patch_manifest_receipt'],fix_manifest_receipt=b['fix_manifest_receipt'],all_five_HEAD_QA_PASS=all(any(r['label']==label and r['result']['returncode']==0 and not r['result']['timed_out']and r['cleanup']['cleanup_complete']and not r['cleanup']['remaining_owned_children']and r['resources']['accepted']for r in rows)for label in qa_labels),normal_push_verified=pushed,push_command_succeeded=push_command_succeeded,Git_remote_readback_verified=Git_remote_readback_verified,check_sh_PASS_claimed=False,full_native_preflight_pending=True,current_source_world_interaction_status='PENDING',world_interaction_scope_passed=False,prior_world_PASS_transferred=False,retained_prior_source_world_negative=b['retained_prior_source_world_negative'],CI_green_claimed=False,DEV_merged=False,native_tail_fixedpoint_PASS_claimed=False,retained_native_tail_negative=b['retained_native_tail_negative'],owner_authorization_quotes=b['user_authorization_quotes'],ledger=rows,error=error,execution_pins=pins)
save(args.out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],HEAD=head,error=error,receipt=str(args.out/'CLOSED.json'))),flush=True)
raise SystemExit(0 if pushed and error is None and source_error is None else 1)
