"""Commit, verify and normally push only the exact source whose native gate passed."""
from pathlib import Path
import argparse, fcntl, hashlib, importlib.util, json, os, subprocess, sys

HERE=Path(__file__).resolve().parent
R=Path('/workspace/chicago-transport-current-20261103'); A=R/'chicago/4d'
OLD='ae762df51dad3bd48e7d5307e0bda3cd0ce05e31'
BASE='92bee8bdb89a900a840bcd94e760bb8f21c757c2'
TREE='ef566b993dd2bfe76eea419c750aa01e7acec263'
APP='99e764a8c61273784b35fac32e4690683c9f078f'
SEM='e51bf322c173b94ce9e04d70e47c0b67c65c20964de9003dcc96b49ef01dc2e6'
BRANCH='steward/t3088-horse-photoquality-20261026'
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--gate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def load(p):return json.loads(Path(p).read_text())
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*cmd):return subprocess.check_output(['git','-C',str(R),*cmd],env=env,timeout=60)
def val(*cmd):return git(*cmd).decode().strip()
def api():return json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/pulls/1649'],env=env,timeout=30))
def staged():
    assert not git('ls-files','-u').strip() and not git('diff','--name-only').strip()
    return dict(HEAD=val('rev-parse','HEAD'),MERGE_HEAD=val('rev-parse','MERGE_HEAD'),
        TREE=val('write-tree'),APP=val('rev-parse',TREE+':chicago/4d'),
        semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
def committed(head):
    assert val('rev-parse','HEAD')==head and val('rev-parse','HEAD^{tree}')==TREE
    assert val('show','-s','--format=%P','HEAD').split()==[OLD,BASE]
    assert not git('status','--porcelain','--untracked-files=no').strip()
    assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==SEM
    assert subprocess.run(['git','-C',str(R),'rev-parse','--verify','-q','MERGE_HEAD'],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==1
    return dict(HEAD=head,TREE=TREE,APP=APP,semantic_index_sha256=SEM)
gate=load(args.gate)
assert gate['status']=='PASS_ALL_FOUR_NATIVE_PREFLIGHT_PARTS_SAME_SOURCE'
assert len(gate['ledger'])==4 and gate['owned_TMPDIR_cleanup_complete']
for row in gate['ledger']:
    assert row['result']['returncode']==0 and not row['result']['timed_out']
    assert row['result']['requested_timeout_seconds']==row['result']['effective_timeout_seconds']==600
    assert row['result']['timeout_override_reason'] is None
    assert row['cleanup']['cleanup_complete'] and not row['cleanup']['remaining_owned_children']
    assert row['resources']['accepted'] and row['source_before']==row['source_after']
    assert row['source_before']==gate['source_before'] and row['native_footer_counts']
expected=dict(HEAD=OLD,MERGE_HEAD=BASE,TREE=TREE,APP=APP,semantic_index_sha256=SEM)
assert all(gate['source_before'][k]==v for k,v in expected.items())
assert staged()==expected and val('remote','get-url','origin')=='https://github.com/kevinrhaas/chicago.git'
assert val('symbolic-ref','HEAD')=='refs/heads/'+BRANCH
assert not args.out.exists();args.out.mkdir(parents=True)
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('delivery_guard',HERE/'resource_guard.py')
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
pins={str(p):digest(p)for p in [Path(__file__),SUP,HERE/'resource_guard.py',HERE/'RESTORED-RUNTIME-BASELINE.json',args.gate]}
rows=[];error=None;head=None;published=False
checks=[('HEAD-changelog-entry',['node','tools/check-changelog-entry.mjs',BASE,'HEAD']),
    ('HEAD-ID-collisions',['node','tools/resolve_id_collisions.mjs','--base',BASE,'--check']),
    ('HEAD-changelog-contract',['node','tools/check-changelog.mjs']),
    ('HEAD-pending-entry',['node','tools/changelog-entries.mjs','--check']),
    ('HEAD-changelog-history',['node','tools/changelog-history.mjs','--base',BASE])]
def run(label,cmd,cwd=A,cap=120,expected_code=0):
    assert all(digest(p)==h for p,h in pins.items())
    before=guard.snapshot();assert guard.check(before)['accepted'];prefix=args.out/label
    with Path(str(prefix)+'.stdout').open('xb')as f:
        q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(cwd),
            '--timeout',str(cap),'--',*cmd],env=env,stdout=f,stderr=subprocess.STDOUT)
    r=load(str(prefix)+'.result.json');c=load(str(prefix)+'.cleanup.json');resources=guard.pair(before,guard.snapshot())
    row=dict(label=label,result=r,cleanup=c,resources=resources,log=str(prefix)+'.log',log_sha256=digest(str(prefix)+'.log'))
    rows.append(row);save(args.out/'LEDGER.json',rows)
    assert q.returncode==r['returncode']==expected_code and not r['timed_out'],label
    assert r['requested_timeout_seconds']==r['effective_timeout_seconds']==cap and r['timeout_override_reason'] is None
    assert c['cleanup_complete'] and not c['remaining_owned_children'] and resources['accepted']
    return Path(str(prefix)+'.log').read_text(errors='replace')
try:
    p=api();assert p['state']=='open' and p['head']['sha']==OLD and not p['draft'] and p['base']['ref']=='dev'
    assert all(x['name']!='hold' for x in p['labels'])
    held=run('own-lap-status',['node','tools/ticket.mjs','lap','1649','--status'],expected_code=3)
    assert 'held lap/pr-1649' in held and 'Codex root checking transport loops and interactions PR1649 before ordinary DEV merge' in held
    assert staged()==expected
    run('normal-merge-commit',['git','commit','-F',str(HERE/'REVIEWABLE-COMMIT-MESSAGE.txt')],cwd=R)
    head=val('rev-parse','HEAD');source=committed(head);save(args.out/'ACTUAL-COMMITTED-SOURCE.json',source)
    for label,cmd in checks:run(label,cmd);committed(head)
    run('HEAD-whitespace',['git','show','--check','--format=oneline','HEAD'],cwd=R)
    p=api();assert p['head']['sha']==OLD and p['state']=='open' and not p['draft']
    remote=val('ls-remote','origin','refs/heads/'+BRANCH).split();assert remote==[OLD,'refs/heads/'+BRANCH]
    run('normal-original-PR-push',['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=R)
    committed(head)
    remote=val('ls-remote','origin','refs/heads/'+BRANCH).split();assert remote==[head,'refs/heads/'+BRANCH]
    p=api();assert p['head']['sha']==head and not p['draft'] and p['base']['ref']=='dev'
    published=True;save(args.out/'PUBLIC-PR-READBACK.json',p)
except BaseException as e:error=repr(e)
try: final_source=committed(head)if head else staged();source_error=None
except BaseException as e:final_source=None;source_error=repr(e)
if source_error and error is None:error='Final source closure: '+source_error
closed=dict(status='ACTUAL_CHECKED_COMMIT_QA_NORMAL_PUSH_PASS'if published and error is None else'CHECKED_DELIVERY_NONPASS',
    source=final_source,source_error=source_error,parents=[OLD,BASE],gate_receipt=str(args.gate),gate_sha256=digest(args.gate),
    exact_tested_TREE_committed=head is not None,all_five_HEAD_QA_PASS=all(x[0]in {r['label']for r in rows if r['result']['returncode']==0}for x in checks)if head else False,
    normal_push_verified=published,PR=1649,DEV_merged=False,ledger=rows,error=error,execution_pins=pins)
save(args.out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],HEAD=head,receipt=str(args.out/'CLOSED.json'),error=error)),flush=True)
raise SystemExit(0 if published and error is None else 1)
