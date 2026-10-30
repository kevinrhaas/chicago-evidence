import datetime
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

S = Path(__file__).resolve().parent
(S / 'PAYLOAD').mkdir(exist_ok=False)
(S / 'GENERATED').mkdir(exist_ok=False)
files, copies, evidence = [], [], {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze(path, label):
    path = Path(path)
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    target = S / 'GENERATED' / label
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    assert target.read_bytes() == raw
    copies.append(dict(captured_from=str(path), snapshot=str(target), bytes=len(raw), sha256=sha(target)))
    files.append(target)
    return target


configs = {
    'H': dict(repo='/tmp/chicago-horse-20261029',
        old_tree='4278fa10062c3593ea2cf65f7bf41a4bee7d39b0', old_app='bfc9fcdd77e694e9deb3f5d514d0f45b8fb559cf',
        new_tree='9e3d17f39e5cec9be13d155eb8a273816e55195c', new_app='11da9f86196ed4e3ebbcd694f1868487141a1246',
        repair='/tmp/HORSE-FULL-GATE-REPAIR-LIGHT-20261030-01', patch='EXACT-4278-TO-THREE-REPAIRS.patch',
        index='COMPLETE-REPAIRED-SEMANTIC-INDEX.z', paths=3,
        measurement='/tmp/HORSE-ACTUAL-INCREMENTAL-ISOLATION-REPAIR-20261030-01',
        prep='/tmp/HORSE-INCREMENTAL-ISOLATION-REPAIR-PREP-20261030',
        prefix='/workspace/.cloud-setup/logs/transport-recovery/horse-two-native-incremental-isolation-measurements-20261030-01', count=2),
    'P': dict(repo='/tmp/chicago-transport-resume-20261029',
        old_tree='eee92b422b653b68593fbfeab11c3c4b37122247', old_app='44d9d0908178710474c4003e1631dcb8f01f8f84',
        new_tree='222273b4b2e118885887ebb94f7778b70029ddbd', new_app='3fc00238e7435a9ee5566e38b8d05d0618ee6355',
        repair='/tmp/OTIS-ACTUAL-INCREMENTAL-ISOLATION-REPAIR-20261030-01', patch='ONE-LEDGER-SOURCE-REPAIR.patch',
        index='COMPLETE-INDEX-AFTER-STAGING.z', paths=1,
        measurement='/tmp/OTIS-ACTUAL-INCREMENTAL-ISOLATION-REPAIR-20261030-01',
        prep='/tmp/OTIS-INCREMENTAL-ISOLATION-REPAIR-PREP-20261030',
        prefix='/workspace/.cloud-setup/logs/transport-recovery/otis-four-native-incremental-isolation-measurements-20261030-01', count=4),
}
base_env = {**os.environ, 'GIT_NO_LAZY_FETCH': '1', 'GIT_TERMINAL_PROMPT': '0'}
for worker, cfg in configs.items():
    repo = Path(cfg['repo'])
    repair = Path(cfg['repair'])
    measure = Path(cfg['measurement'])
    files.extend(p for p in repair.rglob('*') if p.is_file())
    if measure != repair:
        files.extend(p for p in measure.rglob('*') if p.is_file())
    result = json.loads(Path(cfg['prefix'] + '.result.json').read_bytes())
    cleanup = json.loads(Path(cfg['prefix'] + '.cleanup.json').read_bytes())
    actual = json.loads((measure / 'ACTUAL-INCREMENTAL-ISOLATION-REPAIR.json').read_bytes())
    assert result['returncode'] == 0 and not result['timed_out']
    assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 120
    assert cleanup['cleanup_complete'] and cleanup['remaining_owned_children'] == []
    assert len(actual['commands']) == cfg['count'] and actual['all_preexisting_rows_unchanged']
    for row in actual['commands']:
        assert row['native_measurer_returncode'] == row['actual_declared_returncode'] == 0 and not row['timed_out']
        assert row['measured_row'] == {'wrote': [], 'wrote_ignored': []}
        original, preserved = Path(row['original_probe']['path']), Path(row['preserved_probe']['path'])
        assert preserved.is_file() and sha(preserved) == row['preserved_probe']['sha256'] == row['original_probe']['sha256']
        if original.exists():
            assert original.read_bytes() == preserved.read_bytes()
            files.append(original)
    files.extend(Path(cfg['prefix'] + suffix) for suffix in ['.log', '.result.json', '.cleanup.json'])
    for p in sorted(Path(cfg['prep']).rglob('*')):
        if p.is_file():
            freeze(p, worker + '-EXECUTION-PREP/' + str(p.relative_to(cfg['prep'])))

    def git(*args, env=base_env):
        return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', *args], cwd=repo, env=env)

    before_index = git('ls-files', '--stage', '-z')
    assert before_index == (repair / cfg['index']).read_bytes()
    changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', cfg['old_tree'], cfg['new_tree']).decode().splitlines()
    assert len(changed) == cfg['paths']
    if worker == 'P':
        assert changed == ['chicago/4d/tools/step_isolation.json']
    for rel in changed:
        expected = git('show', cfg['new_tree'] + ':' + rel)
        assert (repo / rel).read_bytes() == expected
        freeze(repo / rel, worker + '-REPAIRED-SOURCE/' + rel)

    # All reconstruction writes go to private packet files and a private object store.
    objects = Path(git('rev-parse', '--git-path', 'objects').decode().strip())
    if not objects.is_absolute():
        objects = repo / objects
    private_objects = S / 'GENERATED' / (worker + '-PRIVATE-OBJECTS')
    private_objects.mkdir()
    private_index = S / 'GENERATED' / (worker + '-PRIVATE-APPLICABILITY.index')
    private_env = {**base_env, 'GIT_INDEX_FILE': str(private_index), 'GIT_OBJECT_DIRECTORY': str(private_objects),
                   'GIT_ALTERNATE_OBJECT_DIRECTORIES': str(objects.resolve())}
    git('read-tree', cfg['old_tree'], env=private_env)
    git('apply', '--cached', '--check', '--binary', str(repair / cfg['patch']), env=private_env)
    git('apply', '--cached', '--binary', str(repair / cfg['patch']), env=private_env)
    reconstructed = git('write-tree', env=private_env).decode().strip()
    assert reconstructed == cfg['new_tree']
    assert git('rev-parse', reconstructed + ':chicago/4d', env=private_env).decode().strip() == cfg['new_app']
    reconstructed_index = git('ls-files', '--stage', '-z', env=private_env)
    assert reconstructed_index == before_index == git('ls-files', '--stage', '-z')
    report = S / 'GENERATED' / (worker + '-ACTUAL-PRIVATE-RECONSTRUCTION.json')
    report.write_text(json.dumps(dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        result='PASS exact oldTREE+patch reconstructs newTREE/APP and complete semantic index',
        old_tree=cfg['old_tree'], new_tree=reconstructed, old_app=cfg['old_app'], new_app=cfg['new_app'],
        exact_changed_paths=changed, patch=str(repair / cfg['patch']), patch_sha256=sha(repair / cfg['patch']),
        private_index=str(private_index), private_object_directory=str(private_objects),
        semantic_index_sha256=hashlib.sha256(reconstructed_index).hexdigest(),
        primary_semantic_index_unchanged=True, primary_git_objects_or_source_written=False), indent=2) + '\n')
    files.append(report)
    evidence[worker] = dict(old_tree=cfg['old_tree'], new_tree=cfg['new_tree'], old_app=cfg['old_app'], new_app=cfg['new_app'],
        exact_changed_paths=changed, actual_measurement=result, actual_cleanup=cleanup,
        measured_tools=[r['tool'] for r in actual['commands']], all_preexisting_rows_unchanged=True,
        exact_patch_reconstruction=True, new_full_gate_PASS=False)

extra = [
    '/tmp/horse-quiet-head-neck-v6-full-gate-repair-source-freeze-20261030-01.json',
    '/tmp/HORSE-INCREMENTAL-ISOLATION-INDEPENDENT-SOURCE-REVIEW-20261030-01.json',
    '/tmp/HORSE-BEFORE-FULL-GATE-REPAIR-20261030-01/MANIFEST.json',
    '/tmp/OTIS-SOURCE54-AFTER-ACTUAL-ISOLATION-MEASUREMENT-20261030-01.json',
    '/tmp/OTIS-SOURCE54-CANONICAL-MIRROR-RESTORED-GUARD-20261030-01.json',
]
for path in extra:
    freeze(Path(path), 'GUARDS-AND-REVIEW/' + Path(path).name)
restore = Path('/tmp/OTIS-ACTUAL-NATIVE-PUBLISH-RESTORE-AFTER-ISOLATION-20261030-01')
files.extend(p for p in restore.rglob('*') if p.is_file())
restore_result = json.loads((restore / 'native-publish.result.json').read_bytes())
restore_cleanup = json.loads((restore / 'native-publish.cleanup.json').read_bytes())
assert restore_result['returncode'] == 0 and not restore_result['timed_out']
assert restore_cleanup['cleanup_complete'] and restore_cleanup['remaining_owned_children'] == []
copy_map = S / 'GENERATED' / 'FROZEN-CODE-SOURCE-GUARD-COPY-MAP.json'
copy_map.write_text(json.dumps(copies, indent=2) + '\n')
files.extend([copy_map, Path(__file__)])

pub = json.loads(Path('/tmp/WAGON-W4-PUBLIC330A-REFERENCE-INDEX-20261030.json').read_bytes())
public_by_sha = {r['original_sha256']: r for r in pub['manifest']['files']}
publication_repo = Path('/tmp/root-transport-evidence-publisher-20261030')
rows, unique, cache, seen = [], {}, {}, set()
for p in files:
    assert p.is_file() and not p.is_symlink(), str(p)
    if str(p) in seen:
        continue
    seen.add(str(p))
    raw = p.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest in public_by_sha:
        old = public_by_sha[digest]
        public_path = pub['public_prefix'] + '/' + old['payload_path']
        key = pub['public_commit'] + ':' + public_path
        if key not in cache:
            cache[key] = subprocess.check_output(['git', 'show', key], cwd=publication_repo, env=base_env)
        encoded = cache[key]
        assert len(encoded) == old['encoded_bytes'] and hashlib.sha256(encoded).hexdigest() == old['encoded_sha256']
        row = dict(original_path=str(p), original_bytes=len(raw), original_sha256=digest,
            storage='already-public-byte-exact-reference', public_commit=pub['public_commit'], public_path=public_path,
            payload_path=old['payload_path'], encoding=old['encoding'], encoded_bytes=old['encoded_bytes'], encoded_sha256=old['encoded_sha256'])
    elif digest in unique:
        old = unique[digest]
        encoded = (S / old['payload_path']).read_bytes()
        row = dict(original_path=str(p), original_bytes=len(raw), original_sha256=digest,
            storage='same-checkpoint-byte-exact-alias', payload_path=old['payload_path'], encoding=old['encoding'],
            encoded_bytes=old['encoded_bytes'], encoded_sha256=old['encoded_sha256'])
    else:
        encoded = gzip.compress(raw, compresslevel=1, mtime=0)
        payload = Path('PAYLOAD') / (digest + '-' + p.name + '.gz')
        (S / payload).write_bytes(encoded)
        row = dict(original_path=str(p), original_bytes=len(raw), original_sha256=digest,
            storage='new-encoded-payload', payload_path=str(payload), encoding='gzip-mtime0-level1',
            encoded_bytes=len(encoded), encoded_sha256=hashlib.sha256(encoded).hexdigest())
        unique[digest] = row
    assert len(encoded) == row['encoded_bytes'] and hashlib.sha256(encoded).hexdigest() == row['encoded_sha256']
    assert gzip.decompress(encoded) == raw
    rows.append(row)

manifest = dict(schema='H3-P1-exact-repairs-real-native-isolation-measurements-v1',
    created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    state='Exact stagedH3/P1 repairs and six actual native measurements; new full-gate/feature push/DEV acceptance not established',
    repairs=evidence, P_separate_canonical_publish_restore_result=restore_result,
    P_separate_canonical_publish_restore_cleanup=restore_cleanup,
    file_count=len(rows), new_unique_payload_count=len(unique),
    encoded_payload_bytes=sum(r['encoded_bytes'] for r in rows if r['storage'] == 'new-encoded-payload'),
    original_bytes=sum(r['original_bytes'] for r in rows), files=rows,
    preservation='Old source and failed gates remain. No assets/77MB snapshot copies or active full-gate logs. Private patch reconstruction changes only packet-local index/object files; primary source/index/Git objects unchanged.')
path = S / 'ENCODED-PAYLOAD-MANIFEST.json'
path.write_text(json.dumps(manifest, indent=2) + '\n')
(S / 'README.md').write_text('''# Exact H3/P1 repairs and actual native isolation measurements

H oldTREE4278fa10/APPbfc9fcdd becomes9e3d17f3/11da9f86 through exactlythree repairpaths. P oldTREEeee92b42/APP44d9d090 becomes222273b4/3fc00238 through onlytools/step_isolation.json. Both actual Gitbinarypatches reconstruct their entire targetTREE/APP and complete semanticindex using packet-private indices/objectdirectories; app/sharedGit state is unchanged. Repaired text files, readable maps, source117/source54 guards and completeindices areincluded. Assets and77MB oldcopies arenotduplicated.

Allsix native --tool measurements areactual: twoH commands closed in12.007s andfourP commands in2.323s underoriginal120-second caps, declaredandmeasurerreturncodeszero/cleanupzero. Their original/preservedrawprobes, logs, exactcommands, oldledgers and source/resourceclosure areincluded. Allpreexistingrows remain unchanged. Preparationcode andfuture-mutableguard inputs arefrozenbytes with originalpaths andSHA.

P's separate requiredcanonicalpublish restore actuallypassed in48.567s andits new source54/full5635mirror guard is preserved. This doesnotrewriteP's earlier interrupted partialmirror failure. Oldfailedfullgates remainpublic separately. Newfullretry/featurepush/DEVmerge/world-photoacceptance areNOTestablished bythispacket; active retrylogs areexcluded. RootissoleGitpublisher. Alloriginalsremain; gzipmtime0level1/exactaliases/verifiedpublicreferences only.
''')
print(json.dumps(dict(prepared=str(S), manifest_sha256=sha(path), records=len(rows), unique_payloads=len(unique),
    encoded_bytes=manifest['encoded_payload_bytes'], original_bytes=manifest['original_bytes'],
    exact_H3_P1_reconstruction=True, status='READY immutable recovery; no primary app/Git mutation or browser'), indent=2))
