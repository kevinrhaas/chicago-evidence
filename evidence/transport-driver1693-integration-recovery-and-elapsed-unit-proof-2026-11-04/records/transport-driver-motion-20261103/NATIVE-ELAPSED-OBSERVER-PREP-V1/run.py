#!/usr/bin/env python3
"""False-GO prepared native observer. Original lock/guard/600s supervision only."""
import argparse, fcntl, hashlib, importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path

D = Path(__file__).resolve().parent
BASE = D.parent / 'REAL-LOOK-RENDERED-FIXTURE-V1'
SUP = Path('/workspace/.cloud-setup/transport-supervise.py')
GUARD = Path('/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
LOCK = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
def save(p, value): Path(p).write_text(json.dumps(value, indent=2) + '\n')
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec); spec.loader.exec_module(out); return out

def main():
    parser = argparse.ArgumentParser(description='ROOT-bound actual native configured transport pace observer; prepared-only false GO by default')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--go', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    go = load(args.go); manifest = load(D/'MANIFEST.json')
    assert go['approved'] is True, 'False GO: Root has not authorized this native observer'
    assert go['policy'] == 'ROOT_AUTHORIZED_NATIVE_CONFIGURED_TRANSPORT_PACE_OBSERVER'
    assert go['manifest_sha256'] == sha(D/'MANIFEST.json')
    assert go['canonical_gate_owner_released'] is True
    assert go['candidate_applied_and_reviewed'] is True
    assert go['source']['HEAD'] != 'ROOT_BIND_POST_MERGE_AND_PATCH_HEAD'
    root = args.root.resolve(); app = root/'chicago/4d'; out = args.out.resolve()
    assert not out.is_relative_to(root), 'Observer output must stay outside APP'
    for path, digest in manifest['fixture_pins'].items(): assert sha(D/path) == digest, path
    for path, digest in manifest['external_helper_pins'].items(): assert sha(path) == digest, path
    assert go['asset_pins'] == manifest['unchanged_asset_pins']
    for path, digest in go['asset_pins'].items(): assert sha(app/path) == digest, path
    assert set(go['runtime_pins']) == set(manifest['required_runtime_paths'])
    for path, digest in go['runtime_pins'].items(): assert sha(app/path) == digest, path
    # Reuse the already-reviewed staged TREE/APP/index/HEAD verifier unchanged.
    admission = module('original_driver_fixture', BASE/'run.py')
    before = admission.source(root, go['source'])
    lock = LOCK.open('a+'); fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    guard = module('native_transport_guard', GUARD)
    resources_before = guard.snapshot(); assert guard.check(resources_before)['accepted']
    out.mkdir(exist_ok=False); save(out/'SOURCE-BEFORE.json', before)
    scratch = out/'native-tmp'; scratch.mkdir(mode=0o700)
    config = dict(go, browser=manifest['browser'], cases=manifest['cases'])
    save(out/'CONFIG.json', config)
    prefix = out/'native-elapsed'; result = cleanup = resources = report = after = None; error = None
    try:
        assert subprocess.check_output([manifest['browser'], '--version'], timeout=5).decode().strip() == 'Chromium 141.0.7390.37'
        env = dict(os.environ, PW_EXECUTABLE=manifest['browser'],
            PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103', TMPDIR=str(scratch))
        env.pop('CHICAGO_TICKETS_DIR', None)
        with (out/'SUPERVISOR.stdout').open('xb') as stdout:
            completed = subprocess.run([sys.executable, str(SUP), '--prefix', str(prefix), '--cwd', str(app),
                '--timeout', '600', '--', 'node', str(D/'run_browser.cjs'), str(app), str(out/'browser'), str(out/'CONFIG.json')],
                env=env, stdout=stdout, stderr=subprocess.STDOUT)
        result = load(str(prefix)+'.result.json'); cleanup = load(str(prefix)+'.cleanup.json')
        resources = guard.pair(resources_before, guard.snapshot()); report = load(out/'browser/REPORT.json')
        assert completed.returncode == result['returncode'] == 0 and not result['timed_out']
        assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 600
        assert result['timeout_override_reason'] is None
        assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
        assert report['passed'] and report['browser_closed'] and report['server_closed']
        assert len(report['runs']) == 2
        for row in report['runs']:
            assert row['passed'] and row['viewport_elapsed_seconds'] <= 120 and row['browser_closed']
            assert row['cleanup']['passed'] and len(row['PNG_pairs']) == 3
            assert row['actual']['passed'] and len(row['actual']['windows']) == 3 and len(row['actual']['controls']) == 8
        after = admission.source(root, go['source']); assert before == after
        for path, digest in go['asset_pins'].items(): assert sha(app/path) == digest, path
        for path, digest in go['runtime_pins'].items(): assert sha(app/path) == digest, path
    except BaseException as exception:
        error = repr(exception)
    try: after = admission.source(root, go['source'])
    except BaseException as exception: error = (error+'; ' if error else '') + 'source_after: ' + repr(exception)
    if resources is None: resources = guard.pair(resources_before, guard.snapshot())
    if not resources['accepted']: error = (error+'; ' if error else '') + 'native resource guard rejected'
    if cleanup and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']:
        shutil.rmtree(scratch)
    if scratch.exists(): error = (error+'; ' if error else '') + 'owned native TMPDIR retained'
    save(out/'CLOSED.json', dict(status='NATIVE_CONFIGURED_TRANSPORT_PACE_OBSERVER_PASS' if error is None else 'NONPASS_NO_AUTOMATIC_RETRY',
        error=error, source_before=before, source_after=after, result=result, cleanup=cleanup, resources=resources,
        report=report, manifest_sha256=sha(D/'MANIFEST.json'), ROOT_GO_sha256=sha(args.go),
        owned_TMPDIR_cleanup_complete=not scratch.exists(),
        human_visual_review_required=True, natural_stride_acceptance=False, photographic_acceptance=False,
        consumer_FPS_acceptance=False, equal_origin_wheel_or_horse_claim=False))
    print(json.dumps(dict(passed=error is None, out=str(out), error=error)))
    return 0 if error is None else 1

if __name__ == '__main__': raise SystemExit(main())
