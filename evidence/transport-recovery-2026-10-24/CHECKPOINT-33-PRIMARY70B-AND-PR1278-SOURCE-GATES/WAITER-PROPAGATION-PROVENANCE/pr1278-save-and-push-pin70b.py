#!/usr/bin/env python3
"""Wait for root's closed publication, then gate and FF-deliver only owned PR1278."""
from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, time

REPO=Path('/workspace/chicago-smoke-infra-t3121')
APP=REPO/'chicago/4d'
LOG=Path('/workspace/.cloud-setup/logs/transport-recovery')
PREP=LOG/'PR1278-a729-plus-PINNED-70b-intake-preparation'
WORKER=PREP/'canonical-owner-worker.py'
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
STATE=LOG/'PR1278-PIN70b-save-and-push-driver-state.json'
PREF=LOG/'PR1278-PIN70b-normal-full-PREFLIGHT1'
ROOTSTATE=LOG/'70b-save-and-publish-driver-state.json'
ROOTPUB=LOG/'70b-transport-ui-committed-head-publish'
HEAD='a729a4e0dc39ec2b6c9236ac310387799433c0bc'
BASE='70bcc4366a455a15f1e54e3edfce50c046c0ddce'
TREE='fc8a2552adbd7d4e01bd38b7daa8fd097e3553b7'
APP_TREE='c7a8af69710fcba95872e3810999077e254dd036'
REF='steward/t3107-kimball-habs1-south-stacks'
OWNER='codex-api-diagnosis-PR1278-renewed-20261024T2137Z'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',BASE=BASE,C4D_GATE_REQUIRE_READERS='1')
assert 'CHICAGO_TICKETS_DIR' not in ENV
assert not STATE.exists(),'Preserve first continuation outcome; do not launch twice'

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(Path(p).read_text())
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,value):
    p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(p)
def phase(name,**fields):
    save(STATE,{'phase':name,'observed_utc':utc(),**fields})
    try:os.write(1,(name+'\n').encode())
    except BrokenPipeError:pass
def run(command,cwd=REPO,timeout=120):
    return subprocess.run(command,cwd=cwd,env=ENV,capture_output=True,text=True,timeout=timeout)
def git(*args):
    p=run(['git',*args]);assert p.returncode==0,p.stderr
    return p.stdout.strip()
def api(path):
    p=run(['gh','api','repos/kevinrhaas/chicago/'+path]);assert p.returncode==0,'Ordinary API read failed; stop without bypass'
    return json.loads(p.stdout)
def closed(prefix):
    r,c=read(str(prefix)+'.result.json'),read(str(prefix)+'.cleanup.json')
    assert r['returncode']==0 and not r['timed_out'],str(prefix)
    assert c['cleanup_complete'] and not c['remaining_owned_children'],str(prefix)
    return r,c
def candidate():
    assert git('rev-parse','HEAD')==HEAD and git('rev-parse','MERGE_HEAD')==BASE
    assert git('write-tree')==TREE and git('rev-parse',TREE+':chicago/4d')==APP_TREE
    assert not git('diff','--name-only') and not git('ls-files','--others','--exclude-standard')
def remote_guards():
    assert git('remote','get-url','origin')=='https://github.com/kevinrhaas/chicago.git'
    p=api('pulls/1278')
    assert p['state']=='open' and p['draft'] is True and p['head']['sha']==HEAD and p['head']['ref']==REF
    assert p['head']['repo']['full_name']=='kevinrhaas/chicago' and p['base']['ref']=='dev'
    assert not any(x['name'].lower()=='hold' for x in p['labels'])
    assert git('ls-remote','--exit-code','origin','refs/heads/'+REF).split()[0]==HEAD,'Remote moved; preserve it and stop'
    status=run(['node','tools/ticket.mjs','lap','1278','--status'],APP)
    assert status.returncode==3 and OWNER in status.stdout,'Own lease not positively held'
    return {'observed_utc':utc(),'PR_head':p['head']['sha'],'PR_draft':p['draft'],'API_base':p['base']['sha'],'lease':status.stdout.strip()}
def supervised(prefix,cap,command):
    assert not any(Path(str(prefix)+s).exists() for s in ['.log','.result.json','.cleanup.json'])
    return subprocess.run(['python3',str(SUP),'--prefix',str(prefix),'--cwd',str(APP),'--timeout',str(cap),'--',*command],env=ENV).returncode

try:
    phase('WAITING: root driver final PASS plus actual primary publication0/cleanup0; no own heavy job launched')
    started=time.monotonic()
    while True:
        assert time.monotonic()-started<3600,'Root handoff wait expired; inspect closed proof, no automatic retry'
        try:root_state=read(ROOTSTATE)
        except (FileNotFoundError,json.JSONDecodeError):root_state={}
        label=root_state.get('phase','')
        assert not label.startswith('STOPPED:'),'Root continuation stopped; preserve failure and do not launch own gate'
        if label.startswith('PASS:') and all(Path(str(ROOTPUB)+s).exists() for s in ['.result.json','.cleanup.json']):
            root_pub_result,root_pub_cleanup=closed(ROOTPUB)
            assert root_state['publish_prefix']==str(ROOTPUB)
            root_binding=read(root_state['binding'])
            assert root_binding['incoming_dev']==BASE and root_binding['tree']=='9fa9511eabff9a0e42da32410edf09a8e3608889'
            assert root_binding['head']==root_state['head']
            assert root_pub_result['cwd']=='/workspace/chicago/chicago/4d' and root_pub_result['command']==['bash','tools/publish.sh']
            save(PREP/'PREFLIGHT1-ROOT-QUIET-HANDOFF-VERIFIED.json',{'observed_utc':utc(),'root_driver_final':root_state,'root_binding_sha256':digest(root_state['binding']),'root_publish_result':root_pub_result,'root_publish_cleanup_sha256':digest(str(ROOTPUB)+'.cleanup.json'),'own_heavy_job_not_yet_started':True})
            break
        time.sleep(2)
    candidate();before_commit_guards=remote_guards()
    phase('RUNNING: own explicit pinned70b normal full preflight; root publication and finalPASS verified',prefix=str(PREF),tree=TREE)
    p=run(['python3',str(WORKER),'--preflight-before']);assert p.returncode==0,p.stderr
    began=time.time()
    rc=supervised(PREF,1800,['env','BASE='+BASE,'bash','tools/preflight.sh'])
    after=run(['python3',str(WORKER),'--preflight-after'])
    copies=[]
    for short in ['check','cl','ids']:
        source=Path('/tmp/preflight-'+short+'.log')
        if source.exists() and source.stat().st_mtime>=began-1:
            dest=Path(str(PREF)+'-'+short+'-FINAL.log');assert not dest.exists();shutil.copyfile(source,dest)
            copies.append({'file':str(dest),'bytes':dest.stat().st_size,'sha256':digest(dest)})
    save(PREP/'PREFLIGHT1-ACTUAL-RETURN-AND-CLOSED-TMP-LOGS.json',{'observed_utc':utc(),'supervisor_command_exit':rc,'after_snapshot_exit':after.returncode,'after_snapshot_stderr':after.stderr,'unique_closed_logs':copies})
    assert rc==0 and after.returncode==0,'Own preflight or source stability failed; no commit/push'
    result,cleanup=closed(PREF)
    assert result['command']==['env','BASE='+BASE,'bash','tools/preflight.sh']
    plain=re.sub(r'\x1b\[[0-9;]*m','',Path(str(PREF)+'-check-FINAL.log').read_text())
    footer=re.findall(r'CHECK PASS\s+—\s+(\d+) steps, none red\.',plain)
    tests=re.findall(r'(\d+) of them are self-tests',plain)
    assert footer and tests and 'PREFLIGHT PASS' in Path(str(PREF)+'.log').read_text()
    steps,selftests=int(footer[-1]),int(tests[-1])
    candidate();before_commit_guards=remote_guards()
    hook_config=run(['git','config','--get','core.hooksPath'])
    assert hook_config.returncode in [0,1]
    hooks=Path(hook_config.stdout.strip()) if hook_config.returncode==0 else Path(git('rev-parse','--git-path','hooks'))
    if not hooks.is_absolute():hooks=REPO/hooks
    assert not [n for n in ['pre-commit','prepare-commit-msg','commit-msg','post-commit','pre-push'] if (hooks/n).is_file() and os.access(hooks/n,os.X_OK)],'Unexpected executable hook; stop before unreviewed job'
    msg=PREP/'EXACT-VALIDATED-MERGE-COMMIT-message.txt';assert not msg.exists()
    msg.write_text('T-3107: integrate accepted Prairie kit changes and refresh shared records\n\nPreserve both stone-stack material and accepted front-pier stack geometry.\nCanonical registry re-emission kept all33master GLBs byte-identical;\nliberties and the shared derived tail were rebuilt by their native owners.\n\nExact source tree '+TREE+' passed pinned70b full preflight: '+str(steps)+'steps, '+str(selftests)+'self-tests.\n')
    p=run(['git','commit','--file',str(msg)]);assert p.returncode==0,p.stderr
    new=git('rev-parse','HEAD');assert git('rev-parse','HEAD^{tree}')==TREE
    parents=git('show','-s','--format=%P','HEAD').split();assert parents==[HEAD,BASE]
    assert not git('status','--porcelain')
    exact=LOG/'PR1278-PIN70b-exact-new-HEAD-questions1'
    command=['bash','-c','set -e; node tools/check-changelog-entry.mjs '+BASE+' HEAD; node tools/resolve_id_collisions.mjs --base '+BASE+' --check']
    assert supervised(exact,120,command)==0;closed(exact)
    binding={'created_utc':utc(),'head':new,'tree':TREE,'app_subtree':APP_TREE,'parents':parents,'incoming_pin':BASE,'preflight_prefix':str(PREF),'actual_preflight_command':result['command'],'preflight_seconds':result['seconds'],'preflight_returncode':0,'steps':steps,'self_tests':selftests,'cleanup_complete':True,'remaining_children':0,'exact_HEAD_questions_prefix':str(exact),'owner_source_review_sha256':digest(PREP/'OWNER1-CLOSED-CANDIDATE-SOURCE-REVIEW.json'),'state':'Actual exact pinned70b source committed; normal FF push pending, renderer pending. No DEV merge.'}
    save(PREP/'EXACT-VALIDATED-COMMITTED-HEAD-BINDING.json',binding)
    phase('EXACT VALIDATED SOURCE COMMITTED: normal FF push pending; no browser/publisher',head=new,tree=TREE)
    guard=remote_guards()
    p=run(['git','push','origin','HEAD:refs/heads/'+REF],timeout=180)
    push={'observed_utc':utc(),'before_push_guard':guard,'command':['git','push','origin','HEAD:refs/heads/'+REF],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'new_head':new,'tree':TREE}
    save(PREP/'NORMAL-FF-PUSH-ACTUAL.json',push);assert p.returncode==0,'Ordinary push failed; preserve remote advance, no force or automatic retry'
    assert git('ls-remote','--exit-code','origin','refs/heads/'+REF).split()[0]==new
    current=api('pulls/1278')
    save(PREP/'NORMAL-FF-PUSH-NATIVE-AND-API-OBSERVATION.json',{'observed_utc':utc(),'native_remote_head':new,'API_head':current['head']['sha'],'API_base':current['base']['sha'],'draft':current['draft'],'state':current['state'],'immediate_API_propagation_may_lag':current['head']['sha']!=new,'no_push_retry':True})
    assert current['draft'] is True and current['state']=='open'
    phase('PASS: own exact pinned preflight/mergecommit/head-questions/normalFFpush CLOSED; DRAFT, renderer and fresh CI pending',head=new,tree=TREE,binding=str(PREP/'EXACT-VALIDATED-COMMITTED-HEAD-BINDING.json'))
except BaseException as error:
    phase('STOPPED: preserve actual failure; no automatic rerun/reset/force/READY/merge',error=str(error))
    raise
