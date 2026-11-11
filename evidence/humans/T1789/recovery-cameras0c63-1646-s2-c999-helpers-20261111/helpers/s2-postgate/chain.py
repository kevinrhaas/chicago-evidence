"""Prepared only. ROOT runs a reviewed phase after all16 and ROOT ownership return."""
from pathlib import Path
import base64,hashlib,json,os,re,stat,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=Path('/dev/shm/chicago-t1789-charles-gate-20261110');APP=ROOT/'chicago/4d'
GATE=Path('/tmp/t1789-settler-s2-source-full-gate-prep-20261111')
BRANCH='steward/t1789-1812-loose-linen-seat-20261111'
OLD='3d2d9b356db02deed9d406422f754af4de7aa5f0'
INCOMING='900d9166e5adf7bcff84214c78fd5f0fdda634b9'
PRIMARY='9453fa44842225bdb9de2c687cf7dca2f8a8211d'
TREE='1dced78ea49426b9f4c4b9f52ef79db47f06facf'
FREEZE_SHA='97a2d891a72d62898170279ace4c2832fe76dd36e4719c84a3fd68e408f7133f'
BASE=Path('/tmp/t1789-settler-linen-source-full-gate-prep-20261111/FREEZE.json')
BASE_SHA='ec890f5f94ccc4493f7aa2660abb53cc138f553d40350c537d33cb0e02655528'
APPLY=Path('/tmp/ROOT-T1789-LTS-COMPACT-DEV-INTEGRATION-APPLY-20261111-02/APPLY-RECEIPT.json')
APPLY_SHA='1744df0e8e880c6ad65b49a7161a13b8cdc9707f3562207df9549aded4d015fb'
PROTECTED='refs/heads/steward/t1789-charles-woven-coat-20261110'
METADATA_ONLY={'chicago/4d/docs/ROADMAP.md','chicago/4d/docs/STATUS.md','chicago/4d/renderers/web/js/changelog.js'}
DELETED={'chicago/4d/changelog.d/T1789.json'}
ENV=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
READ_ENV=dict(ENV);READ_ENV.pop('GIT_NO_LAZY_FETCH',None)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args,env=ENV):return subprocess.check_output(['git','-C',str(ROOT),*args],env=env).decode().strip()
def save(path,body):
    assert not path.exists(),str(path)
    path.write_text(json.dumps(body,indent=2)+'\n')
def prior(phase,name):
    closed=json.loads((P/phase/'CLOSED.json').read_text());assert closed['accepted']
    path=P/phase/(name+'-RECEIPT.json');assert sha(path)==closed['receipt_SHA256']
    return json.loads(path.read_text())
def remote_head(branch,absent=False):
    rows=git('ls-remote','origin','refs/heads/'+branch,env=READ_ENV).splitlines()
    if not rows:
        assert absent,'required remote ref missing';return None
    assert len(rows)==1 and rows[0].split()[1]=='refs/heads/'+branch
    return rows[0].split()[0]
def ancestor(a,b):
    r=subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',a,b],env=ENV)
    assert r.returncode in (0,1);return r.returncode==0

def qualified_gate():
    assert sha(GATE/'FREEZE.json')==FREEZE_SHA and sha(BASE)==BASE_SHA and sha(APPLY)==APPLY_SHA
    d=json.loads((GATE/'FREEZE.json').read_text());old=json.loads(BASE.read_text())
    assert d['head']==OLD and d['incoming_dev']==INCOMING and d['branch']==BRANCH and d['index_tree']==TREE
    assert d['root']==str(ROOT) and d['protected_ref']==PROTECTED and d['protected_ref_head']==PRIMARY
    assert d['frozen_file_count']==len(d['rows'])==301 and len(d['expected_staged_paths'])==7 and d['parts']==16
    assert d['baseline302_SHA256']==BASE_SHA and d['baseline_preserved_except_explicit_staged_paths'] and d['old_native8_and_current_fixture_byte_exact']
    assert d['native_asset_adoption'] is False and d['no_new_native_changelog_entry']
    assert d['apply_receipt']==str(APPLY) and d['apply_receipt_SHA256']==APPLY_SHA
    assert set(d['deleted_paths'])==DELETED
    assert sha(Path(d['wrapper']))==d['wrapper_SHA256']
    assert json.loads((GATE/'READY.json').read_text())['freeze_SHA256']==FREEZE_SHA
    f=json.loads((GATE/'FREEZE-CLOSED.json').read_text());assert f['accepted'] and f['freeze_SHA256']==FREEZE_SHA
    assert f['result']['returncode']==0 and not f['result']['timed_out'] and f['result']['requested_timeout_seconds']==f['result']['effective_timeout_seconds']==120 and f['result']['timeout_override_reason'] is None
    assert f['cleanup']['cleanup_complete'] and not f['cleanup']['remaining_owned_children'] and f['resources']['accepted']
    by={r['file']:r for r in d['rows']};before={r['file']:r for r in old['rows']}
    assert len(by)==301 and len(before)==302 and set(by)==set(before)-DELETED
    changed=set(d['expected_staged_paths']);assert DELETED<=changed
    assert d['deleted_old_entry']==before[next(iter(DELETED))]
    for name in set(before)-changed:
        assert all(by[name][k]==before[name][k] for k in ('bytes','sha256','Git_mode','Git_blob_OID')),name
    native={f'chicago/4d/assets/humans/{web}settler_1812.lod{lod}.glb' for web in ('','web/') for lod in range(4)}
    protected=native|{'chicago/4d/data/humans/fixture.measure.json'}
    assert protected<=set(d['protected_native_and_fixture_paths']) and not protected&changed
    for name in protected:
        assert all(by[name][k]==before[name][k] for k in ('bytes','sha256','Git_mode','Git_blob_OID')),name
    a=json.loads((GATE/'AGGREGATE.json').read_text())
    assert a['status']=='ALL16_S2_MERGED_SOURCE_GATE_PARTS_PASS_NOT_NATIVE_QUALIFICATION'
    assert a['head']==OLD and a['incoming_dev']==INCOMING and a['branch']==BRANCH and a['index_tree']==TREE and a['freeze_SHA256']==FREEZE_SHA
    assert a['protected_primary_ref']==PROTECTED and a['protected_primary_head']==PRIMARY and a['native8_fixture_unchanged']
    assert set(a['deleted_paths'])==DELETED and len(a['parts'])==a['partition_count']==16 and a['frozen_files']==301 and a['prior_S8_gate_claims_reused'] is False
    total=0
    for i in range(1,17):
        path=GATE/f'part{i}.CLOSED.json';c=json.loads(path.read_text());part=a['parts'][i-1]
        assert part['part']==i and sha(path)==part['CLOSED_SHA256']
        assert c['accepted'] and c['part']==i and c['freeze_SHA256']==FREEZE_SHA
        r,k,g=c['result'],c['cleanup'],c['resources']
        assert r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==600 and r['timeout_override_reason'] is None
        assert k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
        log=GATE/f'part{i}.log';assert sha(log)==c['log_SHA256']
        assert log.read_text(errors='replace').count('S2_SOURCE_VERIFIED '+FREEZE_SHA+' native8_fixture_primary_ref_unchanged parts16')==2
        assert len(c['actual_final_markers'])==1
        match=re.fullmatch(r'CHECK PASS — part '+str(i)+r'/16: (\d+) steps, none red\.',c['actual_final_markers'][0]);assert match
        assert int(match.group(1))==part['steps'];total+=part['steps']
    assert total==a['sum_part_executions']
    return d,a


def verify_worktree(d,head,committed):
    assert Path.cwd()==APP and git('branch','--show-current')==BRANCH and git('rev-parse','HEAD')==head
    assert git('rev-parse','--verify',PROTECTED)==PRIMARY,'protected primary local ref moved'
    merge=Path(git('rev-parse','--absolute-git-dir'))/'MERGE_HEAD'
    if committed:assert not merge.exists()
    else:assert merge.read_text().strip()==INCOMING,'normal reviewed merge must still be pending'
    assert git('ls-files','-u')=='' and git('diff','--name-only')=='' and git('write-tree')==TREE
    if committed:
        assert git('status','--porcelain=v1','--untracked-files=no')=='' and git('rev-parse','HEAD^{tree}')==TREE
    else:assert sorted(git('diff','--cached','--name-only').splitlines())==d['expected_staged_paths']
    for name in d['deleted_paths']:
        assert not (ROOT/name).exists() and not (ROOT/name).is_symlink(),name
    for row in d['rows']:
        p=ROOT/row['file'];info=p.lstat();assert stat.S_ISREG(info.st_mode) and not p.is_symlink()
        assert info.st_size==row['bytes'] and sha(p)==row['sha256'],row['file']
        assert ('100755' if info.st_mode&stat.S_IXUSR else '100644')==row['Git_mode'],row['file']


def fresh_dev():
    gitdir=Path(git('rev-parse','--absolute-git-dir'));assert (gitdir/'objects').stat().st_dev==ROOT.stat().st_dev
    subprocess.run(['git','-C',str(ROOT),'fetch','--no-tags','--filter=blob:none','origin','refs/heads/dev:refs/remotes/origin/dev'],env=READ_ENV,check=True)
    value=git('rev-parse','origin/dev');assert remote_head('dev')==value,'DEV moved during fetch; retain failure and review'
    return value

def pr_questions(dev,head):
    base=git('merge-base','origin/dev',head)
    subprocess.run(['node','tools/check-changelog-entry.mjs',base,head],cwd=APP,env=READ_ENV,check=True)
    subprocess.run(['node','tools/resolve_id_collisions.mjs','--base','origin/dev','--check'],cwd=APP,env=READ_ENV,check=True)
    assert remote_head('dev')==dev,'DEV advanced during questions; no current-base PASS claimed'
    return dict(fresh_DEV=dev,merge_base=base,changelog_question=True,ID_collision_question=True,
        source_includes_fresh_DEV=ancestor(dev,head),DEV_includes_primary_parent=ancestor(PRIMARY,dev),merge_ready=False)

def commit_phase(d,a):
    out=P/'COMMIT';verify_worktree(d,OLD,False)
    assert remote_head(BRANCH)==OLD,'owned remote feature changed; STOP'
    observed=remote_head('dev');git('diff','--cached','--check')
    message=out/'COMMIT-MESSAGE.txt';assert not message.exists()
    message.write_text('Repair pinned linen capture and integrate current DEV\n\nNormal merge preserves reviewed source parent and DEV history.\nRequire the canonical Blender 4.5.3 LTS header and retain bounded observed diagnostics.\nWrite compact posterior observer JSON without removing fields or increasing caps.\nAll sixteen local source parts passed this exact tree; active human GLBs and fixture bytes are unchanged.\nThe first capture failure is retained; fresh canonical capture/native fit remain pending.\n\nChangelog: none — source-only capture guard and observer serialization fixes unblock the pending 1812 linen seat authoring; no human assets, measurements or rendered garment change. The existing primary entry is already folded on DEV.\n')
    subprocess.run(['git','-C',str(ROOT),'commit','--file',str(message)],env=ENV,check=True)
    head=git('rev-parse','HEAD')
    save(out/'LOCAL-HEAD-CHECKPOINT.json',dict(head=head,parents_expected=[OLD,INCOMING],tree_expected=TREE,push=False))
    assert git('show','-s','--format=%P','HEAD').split()==[OLD,INCOMING]
    assert git('rev-parse','HEAD^{tree}')==TREE and git('rev-parse','HEAD:chicago/4d')==git('rev-parse',TREE+':chicago/4d')
    assert sorted(git('diff','--name-only',OLD,head).splitlines())==d['expected_staged_paths']
    verify_worktree(d,head,True)
    save(out/'COMMIT-RECEIPT.json',dict(status='NORMAL_TWO_PARENT_SOURCE_S2_MERGE_COMMIT_NOT_PUSHED',head=head,parents=[OLD,INCOMING],tree=TREE,
        APP_tree=git('rev-parse','HEAD:chicago/4d'),freeze_SHA256=FREEZE_SHA,aggregate_SHA256=sha(GATE/'AGGREGATE.json'),all16_source_parts_pass=True,
        frozen301_preserved=True,native8_fixture_unchanged=True,deleted_paths=d['deleted_paths'],protected_primary_ref=PROTECTED,protected_primary_head=PRIMARY,
        remote_feature_before_commit=OLD,remote_DEV_observed=observed,DEV_advanced_since_gate=observed!=INCOMING,source_only=True,native_qualification='PENDING',push=False,DEV_merge=False,merge_ready=False))


def preflight_phase(d,a):
    c=prior('COMMIT','COMMIT');verify_worktree(d,c['head'],True)
    questions=pr_questions(fresh_dev(),c['head']);verify_worktree(d,c['head'],True)
    save(P/'PREFLIGHT'/'PREFLIGHT-RECEIPT.json',dict(status='BOTH_ACTUAL_COMMITTED_S2_PR_EVENT_QUESTIONS_PASS',head=c['head'],tree=TREE,
        **questions,all16_source_parts_pass_exact_tree=True,source_files_written=False,bare_fullgate_rerun=False,push=False,DEV_merge=False,native_qualification='PENDING'))
    (P/'DRAFT-PR-BODY-READY.md').write_text('Prepares looser linen trousers for the reconstructed 1812 settler, artifact-only canonical capture and native posterior/pose observation. Active GLBs and fixture measurements remain unchanged; visible fit is pending canonical bake and native review.\n\nThe first capture stopped before geometry because its version guard omitted the canonical LTS suffix. This revision requires the exact observed Blender 4.5.3 LTS header, retains all archive/owner/codec pins, and preserves that failure. The observer writes compact JSON with identical parsed content and unchanged caps.\n\nThis is partial T1789 work. Primary #1928 has merged; this normal two-parent source merge includes DEV `'+INCOMING+'`. Current integration status is recorded by the actual preflight receipt and is not assumed merge-ready. T1789 stays open.\n\nValidation: all sixteen source partitions passed frozen tree `'+TREE+'` (freeze `'+FREEZE_SHA+'`, '+str(a['sum_part_executions'])+' actual step executions). Both committed-head PR-event questions passed against fresh DEV `'+questions['fresh_DEV']+'`. Actual source head: `'+c['head']+'`.\n\nFresh request H2, canonical parent capture, native fixture measurements, rear/pose/LOD fit and photographic review remain pending. No new asset admission or production promotion is claimed.\n')


def push_phase(d,a):
    c=prior('COMMIT','COMMIT');p=prior('PREFLIGHT','PREFLIGHT');assert p['head']==c['head'] and p['changelog_question'] and p['ID_collision_question']
    verify_worktree(d,c['head'],True);assert ancestor(OLD,c['head'])
    dev=fresh_dev();questions=p if dev==p['fresh_DEV'] else pr_questions(dev,c['head'])
    assert remote_head(BRANCH)==OLD,'remote feature advanced; STOP, no force/overwrite'
    save(P/'PUSH'/'LOCAL-HEAD-CHECKPOINT.json',dict(head=c['head'],parents=[OLD,INCOMING],tree=TREE,branch=BRANCH,remote_expected=OLD,before_push=True))
    hooks=subprocess.run(['git','-C',str(ROOT),'config','--path','--get','core.hooksPath'],env=ENV,capture_output=True,text=True)
    assert hooks.returncode in (0,1)
    if hooks.returncode==0:
        hp=Path(hooks.stdout.strip());hp=hp if hp.is_absolute() else ROOT/hp
    else:
        hp=Path(git('rev-parse','--git-common-dir'));hp=(hp if hp.is_absolute() else ROOT/hp)/'hooks'
    original=hp/'pre-push';original_path=str(original.resolve()) if original.is_file() and os.access(original,os.X_OK) else ''
    env=dict(READ_ENV,T1789_EXPECTED_SOURCE_HEAD=c['head'],T1789_EXPECTED_REF='refs/heads/'+BRANCH,T1789_EXPECTED_OLD_HEAD=OLD,T1789_ORIGINAL_PRE_PUSH=original_path)
    attempt=dict(head=c['head'],destination='refs/heads/'+BRANCH,advertised_remote_must_equal=OLD,remote_expected=OLD,fresh_DEV=dev,force=False,original_pre_push=original_path)
    save(P/'PUSH'/'PUSH-ATTEMPT.json',attempt)
    result=subprocess.run(['git','-C',str(ROOT),'-c','core.hooksPath='+str(P/'PUSH/hooks'),'push','origin','HEAD:refs/heads/'+BRANCH],env=env,check=False)
    if result.returncode:
        save(P/'PUSH'/'PUSH-FAILED.json',dict(**attempt,returncode=result.returncode,local_head_preserved=git('rev-parse','HEAD'),automatic_retry=False))
        raise SystemExit(result.returncode)
    advertised=json.loads((P/'PUSH'/'ADVERTISED-EXPECTED-OLD.json').read_text());assert advertised['remote_oid']==OLD and advertised['head']==c['head']
    assert remote_head(BRANCH)==c['head'];verify_worktree(d,c['head'],True)
    save(P/'PUSH'/'PUSH-RECEIPT.json',dict(status='NORMAL_OWN_FEATURE_FAST_FORWARD_S2_PUSH_VERIFIED',head=c['head'],parents=[OLD,INCOMING],tree=TREE,
        branch=BRANCH,remote_expected_before=OLD,advertised_remote_oid=OLD,fresh_DEV_before_push=dev,preflight=questions,
        remote_DEV_after_push=remote_head('dev'),force=False,DEV_push_or_merge=False,merge_ready=False,production=False,native_qualification='PENDING'))


def remote_phase(d,a):
    c=prior('COMMIT','COMMIT');p=prior('PUSH','PUSH');assert p['head']==c['head']
    verify_worktree(d,c['head'],True);assert remote_head(BRANCH)==c['head']
    calls=[];cache={}
    def get(endpoint,limit=1048576):
        response=subprocess.run(['gh','api','--hostname','github.com','--method','GET','repos/kevinrhaas/chicago/'+endpoint],env=READ_ENV,capture_output=True,timeout=20)
        assert response.returncode==0,response.stderr.decode(errors='replace')[:300]
        raw=response.stdout;assert len(raw)<=limit,'bounded GitHub response exceeded'
        calls.append(dict(endpoint=endpoint,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
        return json.loads(raw)
    commit=get('git/commits/'+c['head']);assert commit['sha']==c['head'] and commit['tree']['sha']==TREE
    assert [r['sha'] for r in commit['parents']]==[OLD,INCOMING]
    def directory(oid):
        if oid not in cache:
            tree=get('git/trees/'+oid);assert tree['sha']==oid and not tree.get('truncated')
            assert len({r['path'] for r in tree['tree']})==len(tree['tree'])
            cache[oid]={r['path']:r for r in tree['tree']}
        return cache[oid]
    def entry_for(name):
        oid=TREE;parts=name.split('/')
        for part in parts[:-1]:
            entry=directory(oid).get(part)
            if entry is None:return None
            assert entry['type']=='tree';oid=entry['sha']
        return directory(oid).get(parts[-1])
    rows={r['file']:r for r in d['rows']};verified=[];deleted=[]
    for name in d['expected_staged_paths']:
        entry=entry_for(name)
        if name in DELETED:
            assert entry is None,'folded old entry must be absent remotely';deleted.append(name);continue
        row=rows[name]
        assert entry and entry['type']=='blob' and entry['sha']==row['Git_blob_OID'] and entry['mode']==row['Git_mode'] and entry['size']==row['bytes'],name
        result=dict(file=name,Git_blob_OID=entry['sha'],Git_mode=entry['mode'],bytes=entry['size'],local_SHA256=row['sha256'],remote_body_verified=False)
        if name not in METADATA_ONLY:
            assert row['bytes']<=65536,'only three bounded changed source bodies may download'
            body=get('git/blobs/'+entry['sha'],131072);assert body['encoding']=='base64';raw=base64.b64decode(body['content'],validate=False)
            assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
            assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==entry['sha']
            result['remote_body_verified']=True
        verified.append(result)
    assert len(verified)==6 and sum(r['remote_body_verified'] for r in verified)==3 and set(deleted)==DELETED
    assert {r['file'] for r in verified if not r['remote_body_verified']}==METADATA_ONLY
    assert remote_head(BRANCH)==c['head'];verify_worktree(d,c['head'],True)
    observed=remote_head('dev')
    save(P/'REMOTE-VERIFY'/'REMOTE-RECEIPT.json',dict(status='EXACT_S2_TWO_PARENTS_TREE_SIX_ENTRIES_THREE_BODIES_ONE_DELETION_VERIFIED',head=c['head'],parents=[OLD,INCOMING],tree=TREE,
        freeze_SHA256=FREEZE_SHA,all301_local_frozen_SHA256_bytes_modes_preserved=True,remote_changed_entries=verified,remote_deleted_paths=deleted,API_GETs=calls,
        large_docs_changelog_or_assets_downloaded=False,all301_remote_raw_bodies_claimed=False,protected_primary_ref=PROTECTED,protected_primary_head=PRIMARY,
        remote_DEV_observed=observed,DEV_advanced_since_preflight=observed!=p['fresh_DEV_before_push'],source_only=True,merge_ready=False,
        source_request_H2=None,native_qualification='PENDING',DEV_merge=False,production=False))

if __name__=='__main__':
    phase=sys.argv[1];assert phase in ('COMMIT','PREFLIGHT','PUSH','REMOTE-VERIFY')
    d,a=qualified_gate()
    {'COMMIT':commit_phase,'PREFLIGHT':preflight_phase,'PUSH':push_phase,'REMOTE-VERIFY':remote_phase}[phase](d,a)
