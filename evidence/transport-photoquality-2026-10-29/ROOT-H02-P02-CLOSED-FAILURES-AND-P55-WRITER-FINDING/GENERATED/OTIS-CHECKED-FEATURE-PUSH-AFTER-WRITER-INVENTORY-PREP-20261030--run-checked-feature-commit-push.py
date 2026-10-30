#!/usr/bin/env python3
"""Prepared only. Root must read actual full PASS and explicitly start this procedure."""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,os,re,subprocess,time

R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';P=Path(__file__).resolve().parent
OLD='9400c662b24909598fa6afdea2df4d3b89e7f25d'
TREE='bed69364051ee11b8684c9a02793d40e9b870a4f';APP='a6b4c60ac78d108eacb394d86a218a82438eff77'
INDEX_SHA='f464d4d9f5eb9c272828db6c7f62db089bedf69be0e371c05c63ab36d116bb30'
BRANCH='steward/t1790-natural-human-idle-20261029';REF='refs/heads/'+BRANCH
SOURCE_GUARD=Path('/tmp/OTIS-SOURCE55-AFTER-ACTUAL-WRITER-INVENTORY-20261030-01.json')
GUARD_SHA='21416d4fe7197bdbeeb9424ca0dc78d6f869a15f6b8fa05b4fc7ec5b97227f89'
GATE_WRAPPER=Path('/tmp/OTIS-WHOLE-GATE-AFTER-WRITER-INVENTORY-PREP-20261030/run-guarded-whole-gate.py')
POLICY=Path('/workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/PINNED-EC16-INTAKE-PRESERVED/OWNED-WAGON-BOUND-REPAIR-20261029/resource_admission_v10.py')
POLICY_SHA='eebdd83e057f31bc44f76e0b85acf037f28e4d06807c1070346e4e2802b6d65d'
E={**os.environ,'GIT_TERMINAL_PROMPT':'0','C4D_GATE_REQUIRE_BASE':'1','PYTHONDONTWRITEBYTECODE':'1'}
E.pop('GIT_NO_LAZY_FETCH',None) # Native readers retain normal permitted promisor fetching.
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);assert p.is_file() and not p.is_symlink(),p;b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def rawgit(*args):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false',*args],cwd=R,env=E)
def git(*args):return rawgit(*args).decode().strip()

def current_source(expected_head,gate_index):
    assert git('branch','--show-current')==BRANCH and git('rev-parse','HEAD')==expected_head
    for name in ['MERGE_HEAD','CHERRY_PICK_HEAD','REBASE_HEAD','REVERT_HEAD','rebase-merge','rebase-apply']:
        marker=Path(git('rev-parse','--git-path',name));marker=marker if marker.is_absolute() else R/marker
        assert not marker.exists(),('Unexpected in-progress Git operation',name)
    assert rawgit('ls-files','--stage','-z')==gate_index and sha(gate_index)==INDEX_SHA
    assert git('rev-parse',TREE+':chicago/4d')==APP
    assert not rawgit('diff','--name-only','-z','--')
    assert not rawgit('ls-files','--others','--exclude-standard','-z')
    if expected_head!=OLD:
        assert git('rev-parse','HEAD^{tree}')==TREE and git('rev-parse','HEAD:chicago/4d')==APP
        assert not rawgit('diff','--cached','--name-only','-z','--')
    assert pin(SOURCE_GUARD)['sha256']==GUARD_SHA
    frozen=load(SOURCE_GUARD);assert len(frozen['source_files'])==55
    assert sum(row['path'].endswith('.glb') for row in frozen['source_files'])==16
    for row in frozen['source_files']:
        item=pin(A/row['path']);assert item['bytes']==row['bytes'] and item['sha256']==row['sha256'],row['path']
    for row in load(P/'CURRENT-PINS.json')['tools']:assert pin(row['path'])==row
    return dict(head=expected_head,tree=TREE,app_tree=APP,semantic_index_sha256=INDEX_SHA,source_files=55,human_GLB_files=16)

def current_mirror(expected):
    root=R/'site/4d';rows=[];assert root.is_dir() and not root.is_symlink()
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink()
        if p.is_file():
            item=pin(p);rows.append(dict(path=str(p.relative_to(root)),bytes=item['bytes'],sha256=item['sha256']))
    assert rows==expected['files'];assert len(rows)==expected['files_count'] and sum(x['bytes'] for x in rows)==expected['bytes']
    return dict(files=len(rows),bytes=expected['bytes'],exact_actual_full_gate_published_mirror=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root-go-after-actual-full-pass',required=True,action='store_true')
    parser.add_argument('--gate-out',required=True,type=Path)
    parser.add_argument('--gate-wrapper-sha',required=True)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args();out=args.out.resolve();assert out.is_relative_to(Path('/tmp')) and not out.is_relative_to(R) and not out.exists()
    assert args.gate_out.resolve()==Path('/tmp/OTIS-ACTUAL-FULL-GATE-SHM-20261030-03')
    assert re.fullmatch('[0-9a-f]{64}',args.gate_wrapper_sha)
    out.mkdir(mode=0o700);state=dict(at=now(),state='VALIDATING_ACTUAL_FULL_GATE_BEFORE_COMMIT',commands=[],commit='UNRUN',push='UNRUN',DEV_merge='UNRUN',whole_ticket_or_photo_completion=False)
    def save(): (out/'ACTUAL-CHECKED-FEATURE-DELIVERY.json').write_text(json.dumps(state,indent=2)+'\n')
    def command(label,argv,cwd=R,timeout=60):
        started=time.monotonic()
        try:p=subprocess.run(argv,cwd=cwd,env=E,capture_output=True,timeout=timeout)
        except subprocess.TimeoutExpired as error:
            log=out/(label+'.log');log.write_bytes((error.stdout or b'')+(error.stderr or b''));state['commands'].append(dict(label=label,command=argv,cwd=str(cwd),returncode=None,timed_out=True,seconds=time.monotonic()-started,log=pin(log)));save();raise
        log=out/(label+'.log');log.write_bytes(p.stdout+p.stderr);row=dict(label=label,command=argv,cwd=str(cwd),returncode=p.returncode,seconds=time.monotonic()-started,log=pin(log));state['commands'].append(row);save();assert p.returncode==0,(label,p.returncode);return p.stdout.decode().strip()
    def remote(label,ref):
        text=command(label,['git','ls-remote','--exit-code','origin',ref]);parts=text.split();assert len(parts)==2 and parts[1]==ref;return parts[0]
    save()
    try:
        g=args.gate_out;closed=load(g/'ACTUAL-WHOLE-GATE-CLOSED.json');result=load(g/'native-check.result.json');cleanup=load(g/'native-check.cleanup.json');pins=load(g/'WRAPPER-CODE-PINS.json')
        assert pins['wrapper']==pin(GATE_WRAPPER) and pins['wrapper']['sha256']==args.gate_wrapper_sha
        assert pins['shared_resource10']==pin(POLICY) and pins['shared_resource10']['sha256']==POLICY_SHA
        assert pins['native_timeout_seconds']==1200
        assert closed['status']=='ACTUAL_FULL_NATIVE_CHECK_SH_PASS_SOURCE_AND_RESOURCE10_EXACT' and closed['worker']=='P'
        assert (closed['head'],closed['tree'],closed['app_tree'])==(OLD,TREE,APP)
        assert closed['native_result']==result and closed['native_cleanup']==cleanup and closed['source_index_unchanged'] is True and closed['errors']==[]
        assert result['returncode']==0 and result['timed_out'] is False and result['requested_timeout_seconds']==result['effective_timeout_seconds']==1200 and result['timeout_override_reason'] is None
        assert result['command']==['bash','tools/check.sh'] and result['cwd']==str(A) and cleanup['cleanup_complete'] is True and cleanup['remaining_owned_children']==[]
        plain=re.sub(r'\x1b\[[0-9;]*m','',(g/'native-check.log').read_text(errors='replace'));summaries=re.findall(r'^CHECK (PASS|FAIL) — (.+)$',plain,re.M)
        assert summaries and summaries[-1][0]=='PASS' and list(summaries[-1])==closed['final_native_summary']
        assert closed['native_environment_explicit']['C4D_GATE_REQUIRE_READERS']=='1' and closed['native_environment_explicit']['C4D_GATE_REQUIRE_BASE']=='1' and closed['native_environment_explicit']['CHECK_JOBS']=='4'
        before=load(g/'SOURCE-BEFORE.json');after=load(g/'SOURCE-AFTER.json');assert before==after and before['head']==OLD and before['tree']==TREE and before['app_tree']==APP
        gate_index=(g/'COMPLETE-INDEX-BEFORE.z').read_bytes();assert before['semantic_index_sha256']==sha(gate_index)==INDEX_SHA and before['semantic_index_entries']==18052 and len(before['source_files'])==55 and sum(row['path'].endswith('.glb') for row in before['source_files'])==16
        assert pin(POLICY)['sha256']==POLICY_SHA
        spec=importlib.util.spec_from_file_location('P_checked_resource10',POLICY);policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
        rb=load(g/'RESOURCES-BEFORE.json');ra=load(g/'RESOURCES-AFTER.json');pair=policy.check_pair(rb['snapshot'],ra['snapshot']);assert pair['accepted'] and pair==ra['pair_assessment']==closed['shared_resource10_pair'] and rb['active_owners']==ra['active_owners']==[]
        state['actual_full_gate']=dict(closed=pin(g/'ACTUAL-WHOLE-GATE-CLOSED.json'),native_result=pin(g/'native-check.result.json'),native_cleanup=pin(g/'native-check.cleanup.json'),native_log=pin(g/'native-check.log'),original_HEAD=OLD,original_TREE=TREE,original_APP=APP,original_seconds=result['seconds'],retargeted=False)
        state['source_before']=current_source(OLD,gate_index);state['mirror_before']=current_mirror(load(g/'MIRROR-AFTER.json'))
        assert git('remote','get-url','--push','origin')=='https://github.com/kevinrhaas/chicago.git'
        assert git('config','--get','branch.'+BRANCH+'.remote')=='origin'
        assert remote('REMOTE-FEATURE-BEFORE-COMMIT',REF)==OLD,'Another writer changed the feature ref; stop, no force'
        command('REFRESH-NORMAL-DEV-BASE',['git','-c','gc.auto=0','-c','maintenance.auto=false','fetch','--filter=blob:none','origin','dev'])
        dev=git('rev-parse','origin/dev');assert remote('REMOTE-DEV-BASE-BOUND','refs/heads/dev')==dev
        mergebase=git('merge-base',dev,'HEAD');assert re.fullmatch('[0-9a-f]{40}',mergebase)
        state.update(current_DEV_ref=dev,actual_merge_base_before_commit=mergebase);save()
        state['source_before_commit']=current_source(OLD,gate_index)
        staged_paths=rawgit('diff','--cached','--name-only','-z','--').split(b'\0');assert all(x.startswith(b'chicago/4d/') for x in staged_paths if x)
        command('ACTUAL-STAGED-WHITESPACE',['git','diff','--cached','--check'])
        command('NORMAL-FEATURE-COMMIT',['git','-c','gc.auto=0','-c','maintenance.auto=false','commit','--file',str(P/'COMMIT-MESSAGE.txt')],timeout=60)
        head=git('rev-parse','HEAD');state.update(commit='CREATED_REQUIRED_HEAD_CHECKS_PENDING',HEAD=head);save()
        assert git('show','-s','--format=%P','HEAD')==OLD and git('merge-base',dev,'HEAD')==mergebase
        state['source_after_commit']=current_source(head,gate_index)
        checks=[('real-newHEAD-changelog-entry',['node','tools/check-changelog-entry.mjs',mergebase,head]),('real-newHEAD-ID-collision',['node','tools/resolve_id_collisions.mjs','--base',dev,'--check']),('real-newHEAD-changelog-contract',['node','tools/check-changelog.mjs']),('real-newHEAD-pending-entries',['node','tools/changelog-entries.mjs','--check']),('real-newHEAD-pinned-history',['node','tools/changelog-history.mjs','--base',dev])]
        for label,argv in checks:command(label,argv,cwd=A)
        command('ACTUAL-COMMITTED-WHITESPACE',['git','diff','--check',OLD,head])
        state['source_after_checks']=current_source(head,gate_index);state['mirror_after_checks']=current_mirror(load(g/'MIRROR-AFTER.json'))
        assert remote('REMOTE-FEATURE-BEFORE-PUSH',REF)==OLD,'Another writer changed the feature ref; retain local commit and stop'
        assert remote('REMOTE-DEV-BEFORE-PUSH','refs/heads/dev')==dev,'DEV advanced during HEAD checks; preserve commit, refresh base and recheck before push'
        state.update(commit='PASS_CHECKED_NEW_HEAD',state='ACTUAL_FIVE_NEW_HEAD_CHECKS_PASS_NORMAL_PUSH_PENDING',preflight_questions=dict(actual_check_sh_same_TREE_pass=True,actual_new_HEAD_merge_base_changelog_entry_pass=True,actual_new_HEAD_current_DEV_ID_check_pass=True,preflight_shell_script_itself_executed_by_this_procedure=False));save()
        command('ACTUAL-NORMAL-FEATURE-PUSH',['git','-c','gc.auto=0','-c','maintenance.auto=false','push','origin',head+':'+REF],timeout=120)
        state['push']='NORMAL_PUSH_RETURNED_ZERO';save()
        remote_head=remote('REMOTE-FEATURE-AFTER-PUSH',REF);assert remote_head==head,'Remote advanced after actual push; preserve truthful push result and stop'
        state['source_after_push']=current_source(head,gate_index);state['mirror_after_push']=current_mirror(load(g/'MIRROR-AFTER.json'))
        state.update(at=now(),state='PASS_ACTUAL_CHECKED_FEATURE_COMMIT_AND_NORMAL_PUSH',push='PASS_REMOTE_EXACT',remote_HEAD=remote_head,clean=True,actual_newHEAD_republished=False,required_published_both_profile_smoke='SEPARATE_PENDING',current_GitHub_CI='NOT_READ_BY_THIS_PROCEDURE',DEV_merge='UNRUN',P6_full_world='NONPASS_ORIGINAL600_TIMEOUT_600.1310998959816_SECONDS',P6_near_native8='PASS_COMPLETED_NEAR_SECTION_ONLY_MID_CARD_PHONE_PENDING',broad_T1790='OPEN_NOT_COMPLETED')
        save();print(json.dumps({k:v for k,v in state.items() if k!='commands'}));return 0
    except BaseException as error:
        state.update(at=now(),state='STOPPED_OR_NONPASS_ORIGINALS_RETAINED',error=repr(error));save();raise

if __name__=='__main__':raise SystemExit(main())
