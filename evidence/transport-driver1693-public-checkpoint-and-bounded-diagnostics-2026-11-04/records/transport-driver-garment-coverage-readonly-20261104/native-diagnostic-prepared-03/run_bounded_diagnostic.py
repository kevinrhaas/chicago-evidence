#!/usr/bin/env python3
"""ROOT-only, committed-source, one 120-second native CPU diagnostic window."""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys

P = Path(__file__).resolve().parent
RUNTIME = Path('/workspace/.cloud-setup/transport-current-20261103')
SUP = Path('/workspace/.cloud-setup/transport-supervise.py')
LOCK = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def save(p, value): Path(p).write_text(json.dumps(value, indent=2) + '\n')
def reference(ref):
    assert set(ref) == {'path', 'sha256'}
    assert re.fullmatch('[a-f0-9]{64}', ref['sha256'])
    assert sha(ref['path']) == ref['sha256']
    return load(ref['path'])

def public_source_bridge(cfg, source, git):
    """Bounded transitive admission of the actual positive driver checkpoint.

    The delivery owner has already qualified the reviewed fixture-only native
    source bridge. Preserve that scope and its immutable receipts; do not redo
    the whole gate or pretend historical parts ran on the final source.
    """
    bridge = reference(cfg['public_source_bridge'])
    assert bridge['schema'] == 'ROOT_ACTUAL_POSITIVE_DRIVER_FEATURE_SOURCE_BRIDGE_V3'
    assert bridge['status'] == 'ROOT_BOUND_POSITIVE_ACTUAL_NORMAL_FEATURE_PUSH_CHECKPOINT'
    assert bridge['ROOT_EXPLICIT_POSITIVE_SOURCE_BRIDGE'] is True
    assert set(source) == {'HEAD', 'TREE', 'semantic_index_sha256'}
    assert bridge['source'] == source
    checkpoint = reference(bridge['actual_checkpoint_receipt'])
    assert checkpoint['status'] == bridge['actual_checkpoint_status_exact'] == 'ACTUAL_DRIVER_BRIDGED_COVERAGE_COMMIT_QA_PUBLICATION_FEATURE_PUSH_READY_PR_PASS_CI_PENDING'
    assert all(checkpoint['source'][k] == v for k, v in source.items())
    assert checkpoint['error'] is None and checkpoint['source_error'] is None and checkpoint['resources']['accepted']
    assert checkpoint['normal_push_attempted'] and checkpoint['Git_remote_readback_verified'] and checkpoint['API_remote_readback_verified']
    assert checkpoint['ready_PR_verified'] and checkpoint['PR_number'] > 0
    assert bridge['ROOT_verified_actual_normal_feature_push'] is True
    assert bridge['ROOT_verified_actual_native_full_gate'] is True
    assert bridge['ROOT_verified_actual_committed_HEAD_QA'] is True
    assert bridge['source_commit_bridge'] == checkpoint['source_commit_bridge']
    committed_bridge = reference(checkpoint['source_commit_bridge'])
    assert committed_bridge['status'] == 'ACTUAL_REVIEWED_BRIDGED_NATIVE_COVERAGE_COMMITTED_HEAD_QA_PUBLICATION_PASS'
    assert committed_bridge['staged_source'] == checkpoint['source_before']
    assert committed_bridge['committed_source'] == checkpoint['source']
    assert committed_bridge['committed_source']['APP'] == git('rev-parse', source['HEAD']+':chicago/4d').decode().strip()
    assert committed_bridge['parents'] == checkpoint['parents'] == git('show', '-s', '--format=%P', source['HEAD']).decode().split()
    for key in ['TREE', 'APP', 'semantic_index_sha256']:
        assert committed_bridge['staged_source'][key] == committed_bridge['committed_source'][key]
    assert committed_bridge['all_five_actual_HEAD_QA_PASS'] and committed_bridge['actual_HEAD_whitespace_PASS']
    assert committed_bridge['native_build_stamp'] == source['HEAD'][:10]
    assert committed_bridge['native_publication_caps'] == [180, 120]
    assert checkpoint['all_four_same_TREE'] is committed_bridge['all_four_same_TREE'] is False
    assert checkpoint['reviewed_fixture_only_source_bridge'] == committed_bridge['reviewed_fixture_only_source_bridge']
    gate_ref = checkpoint['full_fourpart_receipt']
    assert gate_ref == committed_bridge['full_fourpart_receipt'] == bridge['actual_native_full_gate_receipt']
    native_gate = reference(gate_ref)
    assert native_gate['status'] == 'FULL_NATIVE_COVERAGE_PASS_WITH_REVIEWED_FIXTURE_ONLY_SOURCE_BRIDGE'
    assert native_gate['all_four_same_TREE'] is False
    # High-level reference/source guard only. The actual positive delivery
    # checkpoint validated the gate's individual caps, mixed sources, catalog,
    # causal single-test review and retained negatives. They are not replayed.
    assert native_gate['source_before'] == native_gate['source_after'] == committed_bridge['staged_source']
    assert native_gate['error'] is None and native_gate['source_error'] is None and native_gate['resources']['accepted']
    causal_refs = {key: committed_bridge[key] for key in ['broader_causal_review', 'current_1904_fixture_receipt',
        'source_bridge_generic_ordinal_erratum', 'correct_full_command_catalog']}
    scoped_receipts = {}
    for key, ref in causal_refs.items():
        doc = reference(ref); scoped_receipts[key] = dict(reference=ref, recorded_status=doc.get('status'),
            scope='Referenced transitively by the positive delivery source bridge; not a new diagnostic, whole-gate or visual PASS.')
    branch = bridge['public_feature_branch']
    assert re.fullmatch(r'steward/[A-Za-z0-9._/-]+', branch)
    assert git('rev-parse', '--abbrev-ref', 'HEAD').decode().strip() == branch
    push = reference(bridge['actual_normal_push_result_receipt'])
    cleanup = reference(bridge['actual_normal_push_cleanup_receipt'])
    command = push['command']
    assert command[:2] == ['git', 'push']
    args = [x for x in command[2:] if x not in ['-u', '--set-upstream']]
    assert len(args) == 2 and args[0] == 'origin'
    assert args[1] in [branch, 'HEAD', 'HEAD:'+branch, 'HEAD:refs/heads/'+branch]
    assert push['returncode'] == 0 and not push['timed_out']
    assert 0 < push['requested_timeout_seconds'] == push['effective_timeout_seconds'] <= 120
    assert push['timeout_override_reason'] is None
    assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
    push_rows = [row for row in checkpoint['ledger'] if row.get('result', {}).get('command') == command]
    assert len(push_rows) == 1
    assert push_rows[0]['result'] == push and push_rows[0]['cleanup'] == cleanup and push_rows[0]['resources']['accepted']
    # Read-only remote proof happens freshly for this execution. No push, fetch,
    # credential inspection, proxy changes, force option or retry is performed.
    remote = git('ls-remote', '--exit-code', 'origin', 'refs/heads/'+branch).decode().strip()
    assert remote.splitlines() == [source['HEAD']+'\trefs/heads/'+branch]
    refs = [cfg['public_source_bridge'], bridge['actual_checkpoint_receipt'], checkpoint['source_commit_bridge'], gate_ref,
        bridge['actual_normal_push_result_receipt'], bridge['actual_normal_push_cleanup_receipt'], *causal_refs.values()]
    return dict(bridge=cfg['public_source_bridge'], actual_checkpoint_receipt=bridge['actual_checkpoint_receipt'],
        immutable_source_commit_bridge=checkpoint['source_commit_bridge'], actual_native_full_gate_receipt=gate_ref,
        admission_kind='BOUNDED_TRANSITIVE_ACTUAL_POSITIVE_FEATURE_CHECKPOINT_NO_WHOLE_GATE_REPLAY',
        admitted_receipt_pins={ref['path']: ref['sha256'] for ref in refs}, scoped_causal_receipts=scoped_receipts,
        prior_source=committed_bridge['prior_source'], actual_staged_source=committed_bridge['staged_source'], actual_committed_source=checkpoint['source'],
        all_four_same_TREE=False, historical_parts_relabelled_as_final_source=False,
        public_feature_branch=branch, fresh_git_remote_readback=remote,
        fresh_git_remote_readback_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        normal_push_result_receipt=bridge['actual_normal_push_result_receipt'],
        normal_push_cleanup_receipt=bridge['actual_normal_push_cleanup_receipt'])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    cfg = load(args.binding); binding_sha256 = sha(args.binding)
    assert cfg['template_only'] is False and cfg['ROOT_EXPLICIT_GARMENT_DIAGNOSTIC_GO'] is True
    assert cfg['protocol'] == 'NATIVE_SEATED_COVERAGE_DIAGNOSTIC_V1_NOT_ACCEPTANCE'
    assert cfg['native_cap_seconds'] == 120
    assert cfg['candidate_generation_enabled'] is False
    repo = Path(cfg['repo']).resolve(); app = Path(cfg['app']).resolve(); out = args.out.resolve()
    assert app == repo/'chicago/4d', 'APP must be the actual project under the bound repository.'
    assert out != repo and repo not in out.parents, 'Output must be outside the repository, before any mkdir/write.'
    assert not out.exists(), 'Use a fresh external output directory.'
    assert sys.version_info[:2] == (3, 11), 'Use the existing transport activation.'
    assert subprocess.check_output(['node', '--version'], timeout=5).decode().startswith('v22.')
    for file, digest in cfg['input_pins'].items(): assert sha(file) == digest, file
    assert sha(__file__) == cfg['runner_sha256']
    lock = LOCK.open('a+')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    spec = importlib.util.spec_from_file_location('garment_diagnostic_guard', RUNTIME/'resource_guard.py')
    guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', UV_THREADPOOL_SIZE='1')
    # Strict no-lazy metadata inspection must not leak into a native command or
    # its own partial-clone fixtures. Preserve all inherited proxy settings.
    env.pop('GIT_NO_LAZY_FETCH', None)
    git_env = dict(env, GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1')
    for key in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        assert env.get(key) == '1', 'Source transport-activate.sh first.'
    def git(*argv):
        return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', '-C', str(repo), *argv], env=git_env, timeout=30)
    def source():
        merge_path = Path(git('rev-parse', '--git-path', 'MERGE_HEAD').decode().strip())
        if not merge_path.is_absolute(): merge_path = repo/merge_path
        assert not merge_path.exists(), 'An in-progress merge is not a clean committed source.'
        assert not git('status', '--porcelain').strip(), 'Only a clean committed receiving source is admitted.'
        return dict(HEAD=git('rev-parse', 'HEAD').decode().strip(),
                    TREE=git('rev-parse', 'HEAD^{tree}').decode().strip(),
                    semantic_index_sha256=hashlib.sha256(git('ls-files', '--stage', '-z')).hexdigest())
    before = source()
    assert before == cfg['source'], 'ROOT must bind the actual new public committed driver source, not the old A3 stage.'
    public_bridge = public_source_bridge(cfg, before, git)
    baseline = guard.snapshot(); assert guard.check(baseline)['accepted']
    out.mkdir(parents=True, exist_ok=False)
    save(out/'SOURCE-BEFORE.json', before); save(out/'RESOURCES-BEFORE.json', baseline)
    prefix = out/'native-owner'; result = {}; cleanup = {}; report = {}; error = None; passed = False
    try:
        with (out/'native.stdout').open('xb') as log:
            q = subprocess.run([sys.executable, str(SUP), '--prefix', str(prefix), '--cwd', str(P),
                '--timeout', '120', '--', 'node', str(P/'diagnose_native_coverage.mjs'),
                str(args.binding.resolve()), str(out/'native')], env=env, stdout=log, stderr=subprocess.STDOUT)
        result = load(str(prefix)+'.result.json'); cleanup = load(str(prefix)+'.cleanup.json')
        report_file = out/'native/RESULT.json'
        if report_file.exists(): report = load(report_file)
        passed = (q.returncode == result['returncode'] == 0 and not result['timed_out']
            and result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 120
            and result['timeout_override_reason'] is None and cleanup['cleanup_complete']
            and not cleanup['remaining_owned_children']
            and report.get('status') == 'NATIVE_FINITE_COVERAGE_DIAGNOSTIC_COMPLETE_NOT_GARMENT_ACCEPTANCE')
    except BaseException as ex:
        error = repr(ex)
    after = None; source_error = None
    try:
        after = source(); assert after == before
        for file, digest in cfg['input_pins'].items(): assert sha(file) == digest, file
        for path, digest in public_bridge['admitted_receipt_pins'].items(): assert sha(path) == digest
        assert sha(args.binding) == binding_sha256 == report.get('config_sha256', binding_sha256)
    except BaseException as ex:
        source_error = repr(ex); passed = False
    resources = guard.pair(baseline, guard.snapshot()); passed = passed and resources['accepted']
    closed = dict(status='BOUNDED_NATIVE_GARMENT_DIAGNOSTIC_COMPLETE_NOT_FIX_OR_COVERAGE_PASS' if passed else 'BOUNDED_NATIVE_GARMENT_DIAGNOSTIC_NONPASS',
        source_before=before, source_after=after, config_sha256=sha(args.binding),
        public_source_bridge=public_bridge, native_child_GIT_NO_LAZY_FETCH_removed='GIT_NO_LAZY_FETCH' not in env,
        result=result, cleanup=cleanup, resources=resources, error=error, source_error=source_error,
        native_report=str(out/'native/RESULT.json'), candidate_generation=False, asset_bytes_changed=False,
        original_native_motion_and_physical_controls_replaced=False, original_quality_or_world_budgets_changed=False,
        garment_gait_photo_or_whole_ticket_acceptance=False)
    save(out/'CLOSED.json', closed)
    print(json.dumps(dict(status=closed['status'], receipt=str(out/'CLOSED.json'))))
    raise SystemExit(0 if passed else 1)

if __name__ == '__main__':
    main()
