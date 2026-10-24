#!/usr/bin/env python3
"""ROOT quiet-window execution only. Native owners, own clone, no manual derived JSON."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

REPO=Path('/workspace/chicago-smoke-infra-t3121')
APP=REPO/'chicago/4d'
OUT=Path('/workspace/.cloud-setup/logs/transport-recovery/PR1278-a729-plus-PINNED-70b-intake-preparation')
HEAD='a729a4e0dc39ec2b6c9236ac310387799433c0bc'
PIN='70bcc4366a455a15f1e54e3edfce50c046c0ddce'
OWNER='codex-api-diagnosis-PR1278-renewed-20261024T2137Z'
CONFLICTS=['chicago/4d/assets/manifest.json','chicago/4d/data/jaunts/prairie-built-so-far.json','chicago/4d/data/sidecars/1812/sources/uses.json','chicago/4d/data/sidecars/1835/sources/index.json','chicago/4d/data/sidecars/1904/jaunts/catalog.json','chicago/4d/data/sidecars/1904/jaunts/prairie-built-so-far.json','chicago/4d/data/sidecars/1904/sources/uses.json','chicago/4d/docs/measurements/source_use_coverage.md']
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
assert 'CHICAGO_TICKETS_DIR' not in os.environ
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,data):
    p=OUT/name
    assert not p.exists(), 'Preserve first attempt; no automatic rerun'
    p.write_text(json.dumps(data,indent=2)+'\n')
def git(*a):
    p=subprocess.run(['git',*a],cwd=REPO,env=ENV,capture_output=True,timeout=120)
    assert p.returncode==0,p.stderr.decode()
    return p.stdout
def gs(*a): return git(*a).decode().strip()
def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def snapshot(name):
    stages=git('ls-files','--stage','-z')
    grouped={}
    for row in stages.split(b'\0'):
        if not row:continue
        meta,raw=row.split(b'\t',1);mode,blob,stage=meta.decode().split()
        grouped.setdefault(raw.decode(),[]).append({'mode':mode,'blob':blob,'stage':int(stage)})
    entries=[]
    for rel,stage_entries in sorted(grouped.items()):
        p=REPO/rel
        if not p.exists() and not p.is_symlink():
            entries.append({'path':rel,'missing':True,'index_stages':stage_entries})
            continue
        data=os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
        entries.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'index_stages':stage_entries})
    untracked=gs('ls-files','--others','--exclude-standard').splitlines()
    value={'observed_utc':utc(),'HEAD':gs('rev-parse','HEAD'),'MERGE_HEAD':gs('rev-parse','MERGE_HEAD'),'source_files':len(entries),'index_stage_listing_sha256':hashlib.sha256(stages).hexdigest(),'entries':entries,'untracked_source':untracked}
    write(name,value)
    return value
def native_stage(number,command,timeout,allow_stale=False):
    path=OUT/f'OWNER1-{number}.log'
    assert not path.exists()
    started=time.monotonic();rc=None;timed_out=False
    with path.open('xb') as f:
        try:rc=subprocess.run(command,cwd=APP,env=ENV,stdout=f,stderr=subprocess.STDOUT,timeout=timeout).returncode
        except subprocess.TimeoutExpired:timed_out=True;rc=124
    record={'command':command,'returncode':rc,'seconds':time.monotonic()-started,'timed_out':timed_out,'log':str(path),'log_sha256':digest(path)}
    write(f'OWNER1-{number}.result.json',record)
    if allow_stale and rc==1 and not timed_out:return False
    assert rc==0 and not timed_out,'Native owner failed; preserve all output and stop without rerun'
    return True

if sys.argv[1:]==['--snapshot-final-only']:
    # The outer wrapper calls this only AFTER its supervisor completed cleanup,
    # including on failed/timed-out owners. It invokes no owner or publisher.
    if (OUT/'OWNER1-source-before.json').exists() and not (OUT/'OWNER1-source-after.json').exists():
        snapshot('OWNER1-source-after-FAILED-OR-INTERRUPTED.json')
    sys.exit(0)

if sys.argv[1:] in [['--preflight-before'],['--preflight-after']]:
    assert os.environ.get('BASE')==PIN,'Pinned preflight requires explicit existing BASE override'
    candidate=json.loads((OUT/'OWNER1-RESOLVED-CANDIDATE-BINDING.json').read_text())
    assert gs('rev-parse','HEAD')==HEAD and gs('rev-parse','MERGE_HEAD')==PIN
    phase='before' if sys.argv[1]=='--preflight-before' else 'after'
    if phase=='before':
        assert gs('write-tree')==candidate['candidate_tree'] and not gs('diff','--name-only')
        p=subprocess.run(['gh','api','repos/kevinrhaas/chicago/pulls/1278'],cwd=REPO,env=ENV,capture_output=True,text=True,timeout=60)
        assert p.returncode==0
        pr=json.loads(p.stdout);assert pr['head']['sha']==HEAD and pr['draft'] is True and pr['state']=='open'
        assert gs('ls-remote','--exit-code','origin','refs/heads/steward/t3107-kimball-habs1-south-stacks').split()[0]==HEAD
        p=subprocess.run(['node','tools/ticket.mjs','lap','1278','--status'],cwd=APP,env=ENV,capture_output=True,text=True,timeout=60)
        assert p.returncode==3 and OWNER in p.stdout
        write('PREFLIGHT1-PINNED-BASE-PROVENANCE.json',{'observed_utc':utc(),'BASE':PIN,'candidate_tree':candidate['candidate_tree'],'candidate_APP':candidate['APP_tree'],'local_origin_dev_metadata':gs('rev-parse','origin/dev'),'native_DEV_metadata':gs('ls-remote','--exit-code','origin','refs/heads/dev').split()[0],'scope':'Explicit pinned70b source gate; never silently follows a newer actualDEV source. Documented BASE override; no assertion edits.','owned_lease':p.stdout.strip()})
    value=snapshot('PREFLIGHT1-source-'+phase+'.json')
    assert not value['untracked_source']
    if phase=='after':
        prior=json.loads((OUT/'PREFLIGHT1-source-before.json').read_text())
        assert prior['entries']==value['entries'],'Source/index changed during preflight; preserve and stop'
        assert gs('write-tree')==candidate['candidate_tree'] and not gs('diff','--name-only')
    sys.exit(0)

write('OWNER1-RUNNING.json',{'started_utc':utc(),'worker_pid':os.getpid(),'worker_process_group':os.getpgrp(),'HEAD':HEAD,'MERGE_HEAD':PIN,'state':'Owner phase started; no result yet'})
assert gs('rev-parse','HEAD')==HEAD and gs('rev-parse','MERGE_HEAD')==PIN
assert gs('diff','--name-only','--diff-filter=U').splitlines()==CONFLICTS
assert (APP/'tickets').resolve().is_relative_to(REPO) and (REPO/'site/4d').resolve().is_relative_to(REPO)
remote=gs('ls-remote','--exit-code','origin','refs/heads/steward/t3107-kimball-habs1-south-stacks').split()[0]
assert remote==HEAD,'Remote head moved; stop'
p=subprocess.run(['gh','api','repos/kevinrhaas/chicago/pulls/1278'],cwd=REPO,env=ENV,capture_output=True,text=True,timeout=60)
assert p.returncode==0
pr=json.loads(p.stdout);assert pr['head']['sha']==HEAD and pr['draft'] is True and pr['state']=='open'
p=subprocess.run(['node','tools/ticket.mjs','lap','1278','--status'],cwd=APP,env=ENV,capture_output=True,text=True,timeout=60)
assert p.returncode==3 and OWNER in p.stdout,'Own lease not positively held'
before=snapshot('OWNER1-source-before.json')
assert not before['untracked_source'],'Unexpected untracked source before owner'
# Delete only exactly identified old ignored generated outputs. Their old archived
# bytes remain reachable in HEAD; the new archive is incoming PIN's committed input.
archive='chicago/4d/docs/RESEARCH/glessner-v4-recovery/'
old=json.loads(git('show',HEAD+':'+archive+'manifest.json'))
new=json.loads(git('show',PIN+':'+archive+'manifest.json'))
assert len(old['files'])==len(new['files'])==3 and set(old['files'])==set(new['files'])
assert (APP/'docs/RESEARCH/glessner-v4-recovery/manifest.json').read_bytes()==git('show',PIN+':'+archive+'manifest.json')
for part in old['parts']:git('cat-file','-e',HEAD+':'+archive+part['name'])
retired=[]
for rel,expected in old['files'].items():
    path=APP/rel
    assert path.resolve().is_relative_to(APP) and not path.is_symlink()
    assert not gs('ls-files','--',str(path.relative_to(REPO)))
    assert path.stat().st_size==expected['bytes'] and digest(path)==expected['sha256']
    assert expected!=new['files'][rel]
    retired.append({'path':str(path),'verified_old':expected,'incoming_expected':new['files'][rel]})
write('OWNER1-verified-generated-retirement-before-delete.json',{'observed_utc':utc(),'old_archive_commit':HEAD,'new_archive_commit':PIN,'files':retired,'old_archive_parts_reachable':True})
for item in retired:Path(item['path']).unlink()
native_stage('01-normal-materialize',['python3','tools/recover_glessner_v4.py','--materialize'],120)
for rel,expected in new['files'].items():
    path=APP/rel
    assert path.stat().st_size==expected['bytes'] and digest(path)==expected['sha256']
write('OWNER1-new-materialized-three-hashes-PASS.json',{'observed_utc':utc(),'archive_pin':PIN,'files':new['files'],'actual_all_exact':True})

# The clean textual merge preserved both parents'753 entry objects but its scalar
# count stayed752. Preserve the actual native failure before the documented fix.
initial_lib=native_stage('02-liberties-initial-CHECK',['python3','tools/compile_liberties.py','--check'],120,allow_stale=True)
if not initial_lib:
    initial_log=(OUT/'OWNER1-02-liberties-initial-CHECK.log').read_text()
    assert 'does not match docs/LIBERTIES.md' in initial_log,'Unexpected checker failure; stop'
    native_stage('03-liberties-native-owner',['python3','tools/compile_liberties.py'],120)
    native_stage('04-liberties-final-CHECK',['python3','tools/compile_liberties.py','--check'],120)



# Resolve the registry ONLY through its own exact-byte re-emission protocol.
assert digest(APP/'generators/archetypes/k01_frontage.py')=='a7975204a73cbf74126928d28f2de3dfca762632c13189d7879b13ce148f2d5e'
native_stage('05-canonical-asset-registry',['python3','tools/merge_asset_registry.py','--resolve','chicago/4d/assets/manifest.json'],600)
git('add','--','chicago/4d/assets/manifest.json')
manifest=json.loads((APP/'tools/derived_manifest.json').read_text())
derived_conflicts=[p for p in CONFLICTS if p!='chicago/4d/assets/manifest.json']
owners={p:next(i for i,s in enumerate(manifest['steps']) if p in s.get('resolves',[])) for p in derived_conflicts}
assert min(owners.values())==147
second={tuple(s['command']) for s in manifest['second_pass']}
assert all(i<147 for i,s in enumerate(manifest['steps']) if tuple(s['command']) in second)
assert gs('diff','--name-only','--diff-filter=U').splitlines()==derived_conflicts
native_stage('06-canonical-resolve-tail148-202',['node','tools/rederive.mjs','--resolve'],900)
assert not gs('diff','--name-only','--diff-filter=U')
after=snapshot('OWNER1-source-after.json')
assert not after['untracked_source'],'Native owner left new untracked source; review before preflight'
a={x['path']:x for x in before['entries']};b={x['path']:x for x in after['entries']}
changed=[p for p in sorted(set(a)|set(b)) if p not in a or p not in b or a[p].get('sha256')!=b[p].get('sha256')]
allowed={p for s in manifest['steps'][147:] for p in s.get('resolves',[])} | {'chicago/4d/assets/manifest.json','chicago/4d/data/liberties.json'}
unexpected=[p for p in changed if p not in allowed]
write('OWNER1-output-delta-review.json',{'observed_utc':utc(),'changed_paths':changed,'unexpected_outside_tail_ownership':unexpected,'allowed_tail_resolves_count':len(allowed),'no_hand_derived_JSON':True})
assert not unexpected,'Unexpected authored/protected source write: preserve and stop before preflight'
protected=json.loads((OUT/'PIN70b-PROTECTED-MERGED-INPUTS.json').read_text())['files']
for rel,record in protected.items():
    if rel!='chicago/4d/data/liberties.json':assert digest(REPO/rel)==record['sha256']
# The native library refresh must retain every accepted and own object, not just count.
old_lib=json.loads(git('show',HEAD+':chicago/4d/data/liberties.json'))
new_lib=json.loads(git('show',PIN+':chicago/4d/data/liberties.json'))
merged_lib=json.loads((APP/'data/liberties.json').read_text())
records={x['id']:x for x in merged_lib['liberties']}
for parent in [old_lib,new_lib]:
    assert all(records.get(x['id'])==x for x in parent['liberties'])
assert set(records)=={x['id'] for x in old_lib['liberties']}|{x['id'] for x in new_lib['liberties']}
assert merged_lib['count']==len(records)==753
assert merged_lib['names']==old_lib['names']==new_lib['names']
assert not gs('diff','--name-only'),'Canonical resolver left unstaged source changes; review before preflight'
tree=gs('write-tree')
write('OWNER1-RESOLVED-CANDIDATE-BINDING.json',{'observed_utc':utc(),'HEAD':HEAD,'MERGE_HEAD':PIN,'candidate_tree':tree,'APP_tree':gs('rev-parse',tree+':chicago/4d'),'changed_owner_paths':changed,'protected_exact':True,'all_conflicts_resolved_by_native_owner':True,'full_preflight':'PENDING: separately supervised after review','commit_push_ready_merge':False})
print(json.dumps({'canonical_owner_phase':'PASS','candidate_tree':tree,'APP_tree':gs('rev-parse',tree+':chicago/4d'),'changed_paths':changed,'normal_full_preflight':'PENDING'}))
