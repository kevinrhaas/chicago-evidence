"""Owner-requested incremental FEATURE branch checkpoint; full preflight stays pending.

This never merges DEV. It keeps the real targeted/publication/world receipts,
commits their exact staged tree, runs actual-commit QA, and normally pushes.
"""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
P=Path(__file__).resolve().parent;R=Path('/workspace/chicago-transport-current-20261103');A=R/'chicago/4d'
SUP=Path('/workspace/.cloud-setup/transport-supervise.py');BRANCH='steward/t3088-horse-photoquality-20261026'
ap=argparse.ArgumentParser();ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--message',type=Path,required=True);args=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*cmd):return subprocess.check_output(['git','-C',str(R),*cmd],env=env,timeout=45)
def val(*cmd):return git(*cmd).decode().strip()
def api():return json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/pulls/1649'],env=env,timeout=40))
b=load(args.binding);expected=b['source'];OLD=expected['HEAD'];BASE=expected['MERGE_HEAD'];TREE=expected['TREE'];APP=expected['APP'];SEM=expected['semantic_index_sha256']
assert b['policy']=='OWNER_AUTHORIZED_INCREMENTAL_FEATURE_BRANCH_CHECKPOINT'
assert b['full_native_preflight_and_CI_required_before_DEV_merge']is True
assert b['user_authorization_quotes']==['commit to GitHub periodically','you don’t have to make things perfect before pushing and committing a ticket to dev, you can make incremental progress']
assert OLD=='5439723317fbb6491e837911243f2f62fb35065b'and BASE=='08d3f3d7c85545013eaca18a9d256fe63a8e17e0'
assert sha(SUP)=='a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
assert sha(P/'RESTORED-RUNTIME-BASELINE.json')=='3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
def native(row,cap=None):
 x=row['result'];c=row['cleanup'];assert x['returncode']==0 and not x['timed_out']and x['timeout_override_reason']is None
 assert x['requested_timeout_seconds']==x['effective_timeout_seconds']
 if cap is not None:assert x['effective_timeout_seconds']==cap
 assert c['cleanup_complete']and not c['remaining_owned_children']and row['resources']['accepted']
proofs={}
for key in ['targeted_owner_receipt','publication_receipt','world_receipt']:
 ref=b[key];assert sha(ref['path'])==ref['sha256'];proofs[key]=load(ref['path'])
owners=proofs['targeted_owner_receipt'];assert owners['status']=='TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT'and owners['source_after']==expected and owners['resources']['accepted']
for row in owners['ledger']:native(row)
pub=proofs['publication_receipt'];assert pub['status']=='ACTUAL_STAGED_NATIVE_PUBLICATION_PASS'and pub['source_before']==pub['source_after']==expected and pub['resources']['accepted']and len(pub['ledger'])==2
for row,cap in zip(pub['ledger'],[180,120]):native(row,cap)
world=proofs['world_receipt'];assert world['source_before']==world['source_after']==expected and world['resources']['accepted']
assert world['scene']=='1904'and world['viewport']=='mobile'and world['scope']=='C'
world_scope_passed=world['status']=='ACTUAL_STAGED_PUBLISHED_SCOPE_PASS'
if world_scope_passed:
 native(world,600)
 assert {'P13_posed_proxy_unified_pick','P14_visible_scene_person_record','P15_trusted_Find_handler_and_close','P16_Light_restore_and_PNG'}<=set(world['predicate_ids'])
else:
 # A reversible feature-branch save is expressly allowed while tests continue.
 # Keep the failed scope negative; do not use its snapshot as a passing gate.
 assert b['allow_saved_partial_world_evidence']is True
 assert world['status']=='ACTUAL_STAGED_PUBLISHED_SCOPE_NONPASS'
 wr=world['result'];wc=world['cleanup']
 assert wr['returncode']==1 and not wr['timed_out']and wr['requested_timeout_seconds']==wr['effective_timeout_seconds']==600 and wr['timeout_override_reason']is None
 assert wc['cleanup_complete']and not wc['remaining_owned_children']
 report=load(world['native_report']);a=report['failureAPI']
 assert report['status']=='ACTUAL_WORLD_INTERACTION_SCOPE_NONPASS'and not report['missing']and not report['pageErrors']
 assert a['ready']is True and a['error']is None and not a['problems']
 person='pa1904_otis_f_r_c1900_hans_johnson'
 assert len(a['town'])==1 and a['town'][0]['visible']and a['humans']==1
 assert a['navigator']['app']=='inspect'and a['navigator']['level']>0 and a['navigator']['link']['person']==person
 cards=[c for c in a['cards']if c['dataset'].get('personId')==person]
 assert len(cards)==1 and cards[0]['name']=='Hans Johnson'and cards[0]['census']and not cards[0]['waiting']
 assert cards[0]['rect']['width']>0 and cards[0]['rect']['height']>0

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
assert not args.out.exists()and args.message.is_file();args.out.mkdir(parents=True)
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('checkpoint_guard',P/'resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
pins={str(p):sha(p)for p in[Path(__file__),args.binding,args.message,SUP,P/'resource_guard.py',P/'RESTORED-RUNTIME-BASELINE.json',*[Path(b[k]['path'])for k in proofs]]}
rows=[];error=None;head=None;pushed=False
def run(label,cmd,cwd=A,expected_code=0):
 assert all(sha(p)==h for p,h in pins.items());before=guard.snapshot();assert guard.check(before)['accepted'];prefix=args.out/label
 with Path(str(prefix)+'.stdout').open('xb')as f:q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(cwd),'--timeout','120','--',*cmd],env=env,stdout=f,stderr=subprocess.STDOUT)
 result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=guard.pair(before,guard.snapshot());row=dict(label=label,result=result,cleanup=cleanup,resources=resources,log_sha256=sha(str(prefix)+'.log'));rows.append(row);save(args.out/'LEDGER.json',rows)
 assert q.returncode==result['returncode']==expected_code and not result['timed_out']and result['requested_timeout_seconds']==result['effective_timeout_seconds']==120 and result['timeout_override_reason']is None
 assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted']
 return Path(str(prefix)+'.log').read_text(errors='replace')
try:
 pr=api();assert pr['state']=='open'and pr['head']['sha']==OLD and pr['base']['ref']=='dev'
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
 committed(head);assert val('ls-remote','origin','refs/heads/'+BRANCH).split()==[head,'refs/heads/'+BRANCH]
 pr=api();assert pr['head']['sha']==head and pr['state']=='open'and pr['base']['ref']=='dev';save(args.out/'PUBLIC-PR-READBACK.json',pr);pushed=True
except BaseException as ex:error=repr(ex)
try:final=committed(head)if head else staged();source_error=None
except BaseException as ex:final=None;source_error=repr(ex)
closed=dict(status='OWNER_INCREMENTAL_CHECKPOINT_NORMAL_PUSH_PASS_FULL_PREFLIGHT_PENDING'if pushed and error is None and source_error is None else'INCREMENTAL_CHECKPOINT_NONPASS_NO_AUTOMATIC_RETRY',source=final,source_error=source_error,source_before_commit=expected,parents=[OLD,BASE],exact_tested_staged_TREE_committed=head is not None,world_receipt=b['world_receipt'],targeted_owner_receipt=b['targeted_owner_receipt'],publication_receipt=b['publication_receipt'],normal_push_verified=pushed,full_native_preflight_pending=True,world_interaction_scope_passed=world_scope_passed,world_negative_preserved=not world_scope_passed,CI_green_claimed=False,DEV_merged=False,owner_authorization_quotes=b['user_authorization_quotes'],ledger=rows,error=error,execution_pins=pins)
save(args.out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],HEAD=head,error=error,receipt=str(args.out/'CLOSED.json'))),flush=True)
raise SystemExit(0 if pushed and error is None and source_error is None else 1)
