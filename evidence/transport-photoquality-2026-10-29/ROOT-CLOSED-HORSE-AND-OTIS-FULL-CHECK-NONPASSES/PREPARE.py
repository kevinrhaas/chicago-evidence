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
files = []
attempts = {}
for worker, name in [('H', 'HORSE-ACTUAL-FULL-GATE-SHM-20261030-01'), ('P', 'OTIS-ACTUAL-FULL-GATE-SHM-20261030-01')]:
    d = Path('/tmp') / name
    result = json.loads((d / 'native-check.result.json').read_bytes())
    cleanup = json.loads((d / 'native-check.cleanup.json').read_bytes())
    closed = json.loads((d / 'ACTUAL-WHOLE-GATE-CLOSED.json').read_bytes())
    assert cleanup['cleanup_complete'] and cleanup['remaining_owned_children'] == []
    assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 1200
    assert not result['timed_out'] and result['timeout_override_reason'] is None
    assert result['returncode'] == (1 if worker == 'H' else 130)
    assert closed['source_index_unchanged'] and closed['shared_resource10_pair']['accepted']
    assert json.loads((d / 'SOURCE-BEFORE.json').read_bytes()) == json.loads((d / 'SOURCE-AFTER.json').read_bytes())
    files.extend(p for p in d.rglob('*') if p.is_file())
    attempts[worker] = dict(attempt=str(d), actual_native=result, actual_cleanup=cleanup,
        closed_status=closed['status'], source_index_unchanged=True, resource10_pair_accepted=True,
        final_native_summary=closed['final_native_summary'], actual_wrapper_errors=closed['errors'],
        mirror_before_after_equality_claimed=False, mirror_after_record_available=(d / 'MIRROR-AFTER.json').exists(),
        complete_native_PASS=False)

files.extend([
    Path('/tmp/OTIS-FULL-GATE-PREEMPTIVE-STATIC-DEFECT-20261030-01.json'),
    Path('/tmp/OTIS-ACTUAL-FULL-GATE-SHM-20261030-01-EARLY-STOP-REASON.json'),
    Path('/tmp/TRANSPORT-WHOLE-GATE-SHM-INDEPENDENT-SOURCE-REVIEW-20261030-01.json'),
])
captured = []
for p in sorted(Path('/tmp/TRANSPORT-WHOLE-GATE-SHM-PREP-20261030').iterdir()):
    if p.is_file():
        raw = p.read_bytes()
        target = S / 'GENERATED' / ('CLOSED-EXECUTION-PREP-' + p.name)
        target.write_bytes(raw)
        assert target.read_bytes() == raw
        captured.append(dict(captured_from=str(p), snapshot=str(target), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
        files.append(target)
assert next(x['sha256'] for x in captured if x['captured_from'].endswith('/run-guarded-whole-gate.py')) == '48d63aea46fba701170523ea096f7d6dee9028101595ae9ee3675a31f2e24310'

o = Path('/workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/PINNED-EC16-INTAKE-PRESERVED/OWNED-WAGON-BOUND-REPAIR-20261029')
files.extend([o / 'resource_admission_v10.py', o.parent.parent.parent / 'ROOT-READONLY-MEMORY-EVENT-BASELINE-20261030-0235.json'])
scope = S / 'GENERATED' / 'CLOSED-ATTEMPT-SCOPE.json'
scope.write_text(json.dumps(dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    state='H completed1109 steps with2errors. P intentionallySIGINT after static4missingisolationrows during incompletepublish; partialmirror NOTHEALTHY.',
    attempts=attempts, execution_prep_snapshots=captured, P_mirror_healthy=False,
    P_missing_MIRROR_AFTER_preserved=True, P_early_stop='Owned SIGINT before original1200 cap; no timeout',
    H_native_fullgate_PASS=False, P_native_fullgate_PASS=False,
    active_global_or_retry_logs_included=False, source_assets_included=False,
    original_failures_rewritten=False, source_feature_commit_push='Not established by this packet', DEV_merge=False), indent=2) + '\n')
files.extend([scope, Path(__file__)])

pub = json.loads(Path('/tmp/WAGON-W4-PUBLIC330A-REFERENCE-INDEX-20261030.json').read_bytes())
public_by_sha = {r['original_sha256']: r for r in pub['manifest']['files']}
repo = Path('/tmp/root-transport-evidence-publisher-20261030')
env = {**os.environ, 'GIT_NO_LAZY_FETCH': '1'}
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
            cache[key] = subprocess.check_output(['git', 'show', key], cwd=repo, env=env)
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

manifest = dict(schema='closed-H-P-original1200-full-gate-nonpass-evidence-v1',
    created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    state='Both NONPASS; H2of1109FAIL and Pintentionalnative130/partialmirror. No assets or active/retry logs.',
    attempts=attempts, file_count=len(rows), new_unique_payload_count=len(unique),
    encoded_payload_bytes=sum(r['encoded_bytes'] for r in rows if r['storage'] == 'new-encoded-payload'),
    original_bytes=sum(r['original_bytes'] for r in rows), public_reference_count=sum(r['storage'] == 'already-public-byte-exact-reference' for r in rows),
    files=rows, preservation='All originals retained. Frozen execution-prep copies retain captured_from paths. Ppartialmirror NOTHEALTHY; missing afterrecord not invented. No Git/source/index/kernel/counter mutation.')
path = S / 'ENCODED-PAYLOAD-MANIFEST.json'
path.write_text(json.dumps(manifest, indent=2) + '\n')
(S / 'README.md').write_text('''# Closed full-gate failures before source repairs

H completed its original1200-second tools/check.sh attempt in841.397650825s with2of1109stepsfailed. Cleanup reachedzeroownedchildren; oldsource116/fullindex and resource10closure stayedhealthy. Requiredpublish rebuilt itsmirror; before/aftermirror equality is notclaimed.

P was deliberately interrupted byownedSIGINT afterastaticaudit provedfournewsteps lackisolationrows. Native130/103.8238s isinterrupted, notPASSortimeout. Source/indexstayedunchanged andresourcepairwasaccepted. Publishwasinterrupted: theactualwrapperreportedSOURCE/MIRRORAssertionError, finalsummaryisabsent andMIRROR-AFTERwasnotcreated. Its partialmirror is NOTHEALTHY. No missingafterrecord is synthesized.

Bothattempts remainNONPASS. Actualtranscripts, timings, supervisors/cleanup, source/index/mirrorguards, resources, SHMNode/Pythonprobes, scratchadmission/cleanup, andPstaticdefect/earlystopreason areincluded. Executionpreparation inputs arefrozenbytecopies withoriginalpaths/SHA beforefuturerepairs. Noassets, active/global/retrylogs orfeaturepush/DEVmergeclaim areincluded. Originalsremain; rootissoleGitwriter. Gzipmtime0level1, byteexactaliases andindependentlyverifiedpublicreferences only.
''')
print(json.dumps(dict(prepared=str(S), manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), records=len(rows),
    unique_payloads=len(unique), encoded_bytes=manifest['encoded_payload_bytes'], original_bytes=manifest['original_bytes'],
    public_references=manifest['public_reference_count'], status='READY immutable failures; no Git writes; active retries excluded'), indent=2))
