#!/usr/bin/env python3
"""ROOT-admitted delivery of an already resolved and fully gated merge.

Preparation is inert. Execution needs a separately reviewed binding with ROOT GO,
the completed four-part receipt hash, exact source and execution pins, and a fresh
output directory. One ordinary merge commit and one normal existing-feature push;
no PR creation/edit, ticket transition, CI dispatch/rerun, DEV merge or force push.
"""
from pathlib import Path
import argparse
import datetime
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

RUNTIME = Path('/workspace/.cloud-setup/transport-current-20261103')
REPO = Path('/workspace/chicago-transport-current-20261103')
APP = REPO / 'chicago/4d'
SUP = Path('/workspace/.cloud-setup/transport-supervise.py')
LOCK = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
BRANCH = 'steward/t2804-independent-driver-looking-20261104'
OLD_HEAD = 'edfc3edc60cf00a8cf2376419d0df8fc3cd8b0a3'
BASE = 'b622c89794f3c52086421b6208ef3eb2876a0528'
SOURCE = dict(HEAD=OLD_HEAD, TREE='f2d0bc74730766d3309a8b23900e39c112e1fffe',
              APP='956ba4adc9ed9d855d18c197d26e208e8f6cb2d0',
              semantic_index_sha256='f1ce756b9a58dd4e4d00b06ec90ac3db5f9ae693dd129bbb4c497561cc0e6257')
GATE_DIR = RUNTIME / 'actual-driver1693-dev-b622-fourpart-v2-01'
GATE_RUNNER = RUNTIME / 'dev-b622-integration-01/run_native_fourpart_resolved_merge.py'
GATE_BINDING = RUNTIME / 'dev-b622-integration-01/ROOT-EXACT-RESOLVED-MERGE-NATIVE-V2-GO.json'
REFERENCE = Path('/workspace/.cloud-setup/transport-driver-motion-20261103/driver-delivery-prepared-v3/deliver_driver_v6_v3.py')
EXPECTED_PARTS = {
    '1': dict(selected_steps=292, selftests=91, elsewhere_steps=865),
    '2': dict(selected_steps=291, selftests=104, elsewhere_steps=866),
    '3': dict(selected_steps=291, selftests=99, elsewhere_steps=866),
    '4': dict(selected_steps=292, selftests=107, elsewhere_steps=865),
}
REQUIRED_ENV = dict(CHECK_JOBS='4', C4D_GATE_REQUIRE_READERS='1',
                    C4D_GATE_REQUIRE_BASE='1', C4D_RULINGS_BASE=BASE)
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    if not __debug__:
        raise RuntimeError('Assertion checks must remain enabled; optimized Python execution refused')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    binding = load(args.binding)
    binding_hash = sha(args.binding)
    assert binding['template_only'] is False
    assert binding['ROOT_EXPLICIT_INTEGRATION_DELIVERY_GO'] is True, 'ROOT review and explicit GO required'
    assert binding['status'] == 'PREPARED_EXACT_RESOLVED_MERGE_DELIVERY_NOT_EXECUTED'
    assert binding['repo'] == str(REPO) and binding['branch'] == BRANCH
    assert binding['source'] == SOURCE and binding['expected_parents'] == [OLD_HEAD, BASE]
    assert binding['base'] == BASE and binding['existing_PR'] == 1693
    assert binding['normal_commit_budget'] == binding['normal_feature_push_budget'] == 1
    assert binding['PR_create_budget'] == binding['PR_edit_budget'] == 0
    assert binding['ticket_write_budget'] == binding['CI_dispatch_or_rerun_budget'] == 0
    assert binding['DEV_merge_budget'] == 0
    assert type(binding['require_remote_dev_exact_reviewed_base']) is bool
    assert binding['reference_helper'] == dict(path=str(REFERENCE), sha256=sha(REFERENCE))
    assert binding['reference_helper']['sha256'] == 'd43a79dabfd32bcbaa7af6b33b2dbd092a2c6e03d30f9a86e554f21db14b3af5'
    out = args.out.resolve()
    assert not out.exists() and not out.is_relative_to(REPO), 'Fresh outside-repository evidence path required'
    assert sys.version_info[:2] == (3, 11)
    assert subprocess.check_output(['node', '--version'], timeout=5).decode().startswith('v22.')

    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1', **REQUIRED_ENV)
    for key in ['GIT_NO_LAZY_FETCH', 'CHICAGO_TICKETS_DIR', 'CHECK_PART', 'BASE', 'CHECK_TIMINGS']:
        env.pop(key, None)
    for key in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']:
        assert env.get(key) == '1', 'Source transport-activate.sh before execution'
    metadata_env = dict(env, GIT_NO_LAZY_FETCH='1')

    def git(*argv, timeout=40):
        return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
                                        '-C', str(REPO), *argv], env=metadata_env, timeout=timeout)

    def val(*argv, timeout=40):
        return git(*argv, timeout=timeout).decode().strip()

    def api(endpoint, timeout=20):
        separator = '&' if '?' in endpoint else '?'
        endpoint += separator + 'integration_readback=' + str(time.time_ns())
        return json.loads(subprocess.check_output(['gh', 'api', endpoint], env=env, timeout=timeout))

    def pins():
        assert sha(args.binding) == binding_hash and sha(__file__) == binding['runner_sha256']
        for path, digest in binding['execution_pins'].items():
            assert sha(path) == digest, path
        for path, digest in binding['source_pins'].items():
            assert sha(REPO / path) == digest, path
        for ref in binding['additional_proofs'].values():
            assert set(ref) == {'path', 'sha256'} and sha(ref['path']) == ref['sha256']
        for path, digest in binding['retained_raw_proof_pins'].items():
            assert sha(path) == digest, path
        assert sha(binding['commit_message_path']) == binding['commit_message_sha256']
        proof = binding['full_fourpart']
        assert proof['path'] == str(GATE_DIR / 'CLOSED.json') and proof['sha256']
        assert sha(proof['path']) == proof['sha256'], 'Completed gate receipt must be independently pinned'

    # The active gate owns this same lock. Never overlap it, and never wait forever.
    lock = LOCK.open('a+')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    pins()
    spec = importlib.util.spec_from_file_location('resolved_merge_delivery_resources', RUNTIME / 'resource_guard.py')
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)

    def merge_head():
        result = subprocess.run(['git', '-C', str(REPO), 'rev-parse', '--verify', '-q', 'MERGE_HEAD'],
                                env=metadata_env, capture_output=True, timeout=10)
        assert result.returncode in (0, 1)
        return result.stdout.decode().strip() if result.returncode == 0 else None

    def source(head, staged):
        pins()
        assert val('branch', '--show-current') == BRANCH
        assert not git('ls-files', '-u').strip(), 'Unresolved source refused'
        assert not git('diff', '--name-only').strip(), 'Tracked working-tree edits refused'
        assert not git('ls-files', '--others', '--exclude-standard').strip(), 'Untracked source refused'
        assert merge_head() == (BASE if staged else None)
        tree = val('write-tree')
        actual = dict(HEAD=val('rev-parse', 'HEAD'), TREE=tree,
                      APP=val('rev-parse', tree + ':chicago/4d'),
                      semantic_index_sha256=hashlib.sha256(git('ls-files', '--stage', '-z')).hexdigest())
        assert actual == dict(SOURCE, HEAD=head), 'Actual source no longer matches the fully gated tree'
        changed = val('diff', '--cached', '--name-only', 'HEAD').splitlines()
        assert changed == (binding['expected_staged_paths'] if staged else [])
        if not staged:
            assert val('show', '-s', '--format=%P', 'HEAD').split() == [OLD_HEAD, BASE]
        return actual

    origin = val('remote', 'get-url', 'origin')
    assert origin in ['https://github.com/kevinrhaas/chicago.git', 'https://github.com/kevinrhaas/chicago', 'git@github.com:kevinrhaas/chicago.git']
    assert val('rev-parse', BASE + '^{commit}') == BASE
    assert val('rev-parse', OLD_HEAD + '^{commit}') == OLD_HEAD
    before = source(OLD_HEAD, True)
    gate = load(binding['full_fourpart']['path'])
    assert gate['status'] == 'PASS_ALL_FOUR_NATIVE_CHECK_PARTS_SAME_STAGED_SOURCE'
    assert gate['source_before'] == gate['source_after'] == SOURCE
    assert gate['branch'] == BRANCH and gate['expected_MERGE_HEAD'] == BASE
    assert gate['error'] is None and gate['source_error'] is None
    assert gate['resources']['accepted'] and gate['owned_TMPDIR_cleanup_complete']
    assert not (GATE_DIR / 'native-tmp').exists(), 'Owned gate scratch not fully cleaned'
    assert gate['native_distinct_steps'] == 1157 and gate['native_selftests'] == 401
    assert gate['original_cap_per_part_seconds'] == 600
    assert gate['required_environment'] == REQUIRED_ENV
    assert gate['native_GIT_NO_LAZY_FETCH_absent'] is True and gate['metadata_git_GIT_NO_LAZY_FETCH'] == '1'
    assert gate['expected_parts'] == EXPECTED_PARTS and gate['every_part_execution_overlap'] == 9
    assert gate['binding_path'] == str(GATE_BINDING)
    assert sha(GATE_BINDING) == gate['binding_sha256'] == binding['gate_binding_sha256']
    gb = load(GATE_BINDING)
    assert gb['ROOT_EXPLICIT_CURRENT_FOURPART_GO'] is True and gb['template_only'] is False
    assert gb['source'] == SOURCE and gb['expected_MERGE_HEAD'] == gb['reviewed_base_SHA'] == BASE
    assert sha(GATE_RUNNER) == gb['runner_sha256'] == gate['runner_sha256'] == binding['gate_runner_sha256']
    assert gate['execution_pins'] == gb['execution_pins']
    for path, digest in gate['execution_pins'].items():
        assert sha(path) == digest
    declarations = re.findall(r'(?m)^[ \t]*(?:(every_part)\s+)?(step|selftest)\s+', (APP / 'tools/check.sh').read_text())
    assert len(declarations) == 1157 and sum(kind == 'selftest' for _, kind in declarations) == 401
    assert sum(bool(every) for every, _ in declarations) == 3
    assert [row['part'] for row in gate['ledger']] == [1, 2, 3, 4]
    for row in gate['ledger']:
        part = row['part']
        result, cleanup = row['result'], row['cleanup']
        assert row['source_before'] == row['source_after'] == SOURCE and row['source_error'] is None
        assert row['command'] == result['command'] == ['./tools/check.sh', '--part', f'{part}/4']
        assert result['returncode'] == 0 and not result['timed_out']
        assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 600
        assert result['timeout_override_reason'] is None
        assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and row['resources']['accepted']
        assert guard.pair(row['resource_before'], row['resource_after']) == row['resources']
        assert sha(row['log']) == row['log_sha256']
        body = ANSI.sub('', Path(row['log']).read_text(errors='replace'))
        expected = EXPECTED_PARTS[str(part)]
        assert row['native_footer_counts'] == expected
        assert len(re.findall(r'^CHECK PASS[^\n]*part ' + str(part) + r'/4:\s*' + str(expected['selected_steps']) + r' steps, none red\.$', body, re.M)) == 1
        assert not re.search(r'^CHECK FAIL', body, re.M)
        assert f"  {expected['selftests']} of them are self-tests that prove a gate by breaking it;" in body
        assert f"  This is part {part} of 4; the other {expected['elsewhere_steps']} steps are in the other parts." in body
        assert 'green only when every part is: tools/check.sh --part 1/4 through --part 4/4.' in body
    assert sum(r['native_footer_counts']['selected_steps'] for r in gate['ledger']) - 9 == 1157
    assert sum(r['native_footer_counts']['selftests'] for r in gate['ledger']) == 401
    assert abs(gate['total_native_part_seconds'] - sum(r['result']['seconds'] for r in gate['ledger'])) < 1e-6

    # Preserve the failed original gate and actual canonical repairs. These are
    # provenance only; none of the old part's positives substitutes for V2's four.
    proofs = {key: load(ref['path']) for key, ref in binding['additional_proofs'].items()}
    negative = proofs['prior_failed_fourpart']
    assert negative['status'] == 'NONPASS_NO_AUTOMATIC_RETRY' and len(negative['ledger']) == 1
    assert negative['source_before'] == negative['source_after'] and negative['source_error'] is None
    assert negative['source_before']['TREE'] == '708fcd2d5fcf7393dbb71732948c8642b868e967'
    assert negative['ledger'][0]['part'] == 1 and negative['ledger'][0]['result']['returncode'] == 1
    assert negative['resources']['accepted'] and negative['owned_TMPDIR_cleanup_complete']
    assert gb['preserved_prior_native_negative'] == binding['additional_proofs']['prior_failed_fourpart']
    scalar = proofs['exact_two_scalar_repair_audit']
    assert scalar['status'] == 'EXACT_TWO_CANONICAL_COUNT_SCALAR_REPAIRS_NOT_FULL_GATE'
    assert scalar['new_source'] == SOURCE and scalar['all_other_bytes_exact'] is True
    assert scalar['changed_paths'] == ['chicago/4d/data/liberties.json', 'chicago/4d/docs/measurements/source_use_coverage.md']
    assert scalar['full_fourparts_must_execute_fresh'] is True and scalar['no_failed_part_reuse'] is True
    for path, digest in scalar['new_blob_sha256'].items():
        assert sha(REPO / path) == digest

    def repaired_native(row, command, returncode):
        result, cleanup = row['result'], row['cleanup']
        assert result['command'] == command and result['returncode'] == returncode and not result['timed_out']
        assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 120
        assert result['timeout_override_reason'] is None
        assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']

    liberty_repair = proofs['canonical_liberties_producer']
    assert liberty_repair['status'] == 'NATIVE_LIBERTIES_PRODUCER_COMPLETE_REVIEW_PENDING'
    repaired_native(liberty_repair, ['python3', 'tools/compile_liberties.py'], 0)
    assert liberty_repair['resources']['accepted'] and liberty_repair['changed'] == ['chicago/4d/data/liberties.json']
    assert liberty_repair['after_sha256'] == scalar['new_blob_sha256']['chicago/4d/data/liberties.json']
    checks = proofs['preserved_derived_input_checks']
    assert checks['status'] == 'NONPASS' and checks['source_before'] == checks['source_after']
    assert checks['resources']['accepted'] and [row['name'] for row in checks['rows']] == ['liberties', 'source-use']
    repaired_native(checks['rows'][0], ['python3', 'tools/compile_liberties.py', '--check'], 0)
    repaired_native(checks['rows'][1], ['python3', 'tools/compile_source_use.py', '--check'], 1)
    source_repair = proofs['canonical_source_use_producer_and_check']
    assert source_repair['status'] == 'NATIVE_SOURCE_USE_PRODUCER_AND_CHECK_PASS_REVIEW_PENDING'
    assert source_repair['resources']['accepted'] and [row['label'] for row in source_repair['rows']] == ['derive', 'check']
    repaired_native(source_repair['rows'][0], ['python3', 'tools/compile_source_use.py'], 0)
    repaired_native(source_repair['rows'][1], ['python3', 'tools/compile_source_use.py', '--check'], 0)

    start = guard.snapshot()
    assert guard.check(start)['accepted']
    out.mkdir(parents=True)
    scratch = out / 'delivery-tmp'
    scratch.mkdir(mode=0o700)
    env['TMPDIR'] = str(scratch)
    rows = []
    dev_observations = []
    head = None
    final = None
    error = source_error = None
    commit_attempted = push_attempted = False
    git_verified = api_verified = pr_verified = False
    commit_supervision_error = push_supervision_error = None
    in_flight = False
    state = dict(status='ACTIVE_INTEGRATION_DELIVERY_NOT_CI_OR_DEV_PASS', started_utc=utc(),
                 source_before=before, parents=[OLD_HEAD, BASE], ledger=rows,
                 exact_qualified_integration_base=BASE, remote_dev_observations=dev_observations,
                 require_remote_dev_exact_reviewed_base=binding['require_remote_dev_exact_reviewed_base'])

    def run(label, command, cap=120, cwd=APP, require_zero=True):
        nonlocal in_flight
        pins()
        snap = guard.snapshot()
        assert guard.check(snap)['accepted']
        prefix = out / label
        save(out / 'STATE.json', state | dict(active=label))
        in_flight = True
        with Path(str(prefix) + '.stdout').open('xb') as stdout:
            completed = subprocess.run([sys.executable, str(SUP), '--prefix', str(prefix), '--cwd', str(cwd),
                                        '--timeout', str(cap), '--', *command], env=env, stdout=stdout, stderr=subprocess.STDOUT)
        result = load(str(prefix) + '.result.json')
        cleanup = load(str(prefix) + '.cleanup.json')
        in_flight = not (cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'])
        resources = guard.pair(snap, guard.snapshot())
        row = dict(label=label, result=result, cleanup=cleanup, resources=resources,
                   resource_before=snap, log=str(prefix) + '.log', log_sha256=sha(str(prefix) + '.log'))
        rows.append(row)
        save(out / 'LEDGER.json', rows)
        assert completed.returncode == result['returncode']
        assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == cap
        assert result['timeout_override_reason'] is None
        assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
        if require_zero:
            assert result['returncode'] == 0 and not result['timed_out']
        return row

    def branchremote(timeout=20):
        return val('ls-remote', '--heads', 'origin', 'refs/heads/' + BRANCH, timeout=timeout).split()

    def admission(label, expected_head):
        # All metadata reads precede the single mutation. None edits PR ownership.
        pr = api('repos/kevinrhaas/chicago/pulls/1693')
        remote = branchremote()
        ref = api('repos/kevinrhaas/chicago/git/ref/heads/' + BRANCH)
        dev = api('repos/kevinrhaas/chicago/git/ref/heads/dev')
        observed = dict(utc=utc(), admission=label, actual_remote_DEV=dev['object']['sha'],
                        exact_qualified_integration_base=BASE,
                        remote_DEV_equals_qualified_base=dev['object']['sha'] == BASE,
                        later_DEV_tree_requalified=False)
        dev_observations.append(observed)
        save(out / (label + '.json'), dict(utc=utc(), pr=pr, Git_remote=remote, feature_ref=ref,
                                          dev_ref=dev, qualification=observed))
        assert pr['number'] == 1693 and pr['state'] == 'open' and pr['merged'] is False and not pr['draft']
        assert pr['base']['ref'] == 'dev' and pr['head']['ref'] == BRANCH and pr['head']['sha'] == expected_head
        assert pr['head']['repo']['full_name'] == 'kevinrhaas/chicago'
        assert remote == [expected_head, 'refs/heads/' + BRANCH] and ref['object']['sha'] == expected_head
        if binding['require_remote_dev_exact_reviewed_base']:
            assert dev['object']['sha'] == BASE, 'DEV advanced again; ROOT must review the new base'
        return pr

    def reconcile_push():
        nonlocal git_verified, api_verified, pr_verified
        deadline = time.monotonic() + 150
        for attempt in range(6):
            for kind in ['git', 'api', 'pr']:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    timeout = max(0.1, min(20, remaining))
                    if kind == 'git':
                        value = branchremote(timeout=timeout)
                        git_verified = value == [head, 'refs/heads/' + BRANCH]
                    elif kind == 'api':
                        value = api('repos/kevinrhaas/chicago/git/ref/heads/' + BRANCH, timeout=timeout)
                        api_verified = value['object']['sha'] == head
                    else:
                        value = api('repos/kevinrhaas/chicago/pulls/1693', timeout=timeout)
                        pr_verified = (value['number'] == 1693 and value['state'] == 'open' and value['merged'] is False
                                       and value['head']['sha'] == head and value['head']['ref'] == BRANCH and value['base']['ref'] == 'dev')
                    save(out / f'PUSH-READBACK-{attempt}-{kind}.json', dict(utc=utc(), value=value))
                except BaseException as exc:
                    save(out / f'PUSH-READBACK-{attempt}-{kind}-ERROR.json', dict(utc=utc(), error=repr(exc)))
            if git_verified and api_verified and pr_verified:
                return
            if time.monotonic() >= deadline:
                break
            time.sleep(min(3, max(0, deadline - time.monotonic())))

    try:
        admission('ADMISSION-BEFORE-COMMIT', OLD_HEAD)
        assert source(OLD_HEAD, True) == before
        commit_attempted = True
        save(out / 'COMMIT-INTENT.json', dict(utc=utc(), command=['git', 'commit', '-F', binding['commit_message_path']],
                                             parents=[OLD_HEAD, BASE], tree=SOURCE['TREE'], automatic_retry=False))
        try:
            run('ordinary-resolved-MERGE-commit-ONCE', ['git', 'commit', '-F', binding['commit_message_path']], cwd=REPO)
        except BaseException as exc:
            # Never repeat commit after an uncertain wrapper outcome. Preserve actual state.
            commit_supervision_error = repr(exc)
            save(out / 'COMMIT-READBACK.json', dict(utc=utc(), HEAD=val('rev-parse', 'HEAD'), MERGE_HEAD=merge_head(),
                                                   parents=val('show', '-s', '--format=%P', 'HEAD').split(), error=commit_supervision_error))
            raise
        head = val('rev-parse', 'HEAD')
        assert head not in [OLD_HEAD, BASE]
        final = source(head, False)
        checks = [
            ('entry', ['node', 'tools/check-changelog-entry.mjs', BASE, 'HEAD']),
            ('identifiers', ['node', 'tools/resolve_id_collisions.mjs', '--base', BASE, '--check']),
            ('changelog', ['node', 'tools/check-changelog.mjs']),
            ('pending-entry', ['node', 'tools/changelog-entries.mjs', '--check']),
            ('history', ['node', 'tools/changelog-history.mjs', '--base', BASE]),
        ]
        for label, command in checks:
            run('actual-HEAD-' + label, command)
            assert source(head, False) == final
        run('actual-HEAD-whitespace', ['git', 'show', '--check', '--format=oneline', 'HEAD'], cwd=REPO)
        run('actual-HEAD-base-diff-whitespace', ['git', 'diff', '--check', BASE, 'HEAD'], cwd=REPO)
        assert source(head, False) == final
        run('actual-HEAD-native-publish', ['bash', 'tools/publish.sh'], 180)
        assert source(head, False) == final
        run('actual-HEAD-published-check', ['node', 'tools/check_published.mjs'], 120)
        assert source(head, False) == final
        stamp = load(REPO / 'site/4d/build.json')['version']
        assert stamp == head[:10]
        bridge = dict(status='EXACT_SAME_TREE_NATIVE_FOURPART_MERGE_COMMIT_HEAD_QA_PUBLICATION_PASS',
                      staged_source=SOURCE, committed_source=final, parents=[OLD_HEAD, BASE],
                      exact_qualified_integration_base=BASE, remote_dev_observations=dev_observations,
                      latest_DEV_acceptance_claimed=False, later_DEV_tree_requalified=False,
                      all_four_same_TREE=True, full_fourpart_receipt=binding['full_fourpart'],
                      retained_negative_and_canonical_repair_proofs=binding['additional_proofs'],
                      all_five_actual_HEAD_QA_PASS=True, whitespace_PASS=True, native_build_stamp=stamp,
                      native_publication_caps=[180, 120], native_distinct_steps=1157, native_selftests=401,
                      CI_PASS_claimed=False, DEV_merged=False, ledger=rows)
        save(out / 'SOURCE-COMMIT-BRIDGE.json', bridge)
        admission('ADMISSION-BEFORE-PUSH', OLD_HEAD)
        save(out / 'SOURCE-COMMIT-BRIDGE.json', bridge)
        assert source(head, False) == final
        push_attempted = True
        save(out / 'PUSH-INTENT.json', dict(utc=utc(), old_remote=OLD_HEAD, new_remote=head,
                                           command=['git', 'push', 'origin', 'HEAD:refs/heads/' + BRANCH],
                                           mutation_budget=1, automatic_retry=False))
        try:
            run('normal-existing-feature-push-ONCE', ['git', 'push', 'origin', 'HEAD:refs/heads/' + BRANCH],
                cwd=REPO, require_zero=False)
        except BaseException as exc:
            push_supervision_error = repr(exc)
            save(out / 'PUSH-SUPERVISION-ERROR.json', dict(utc=utc(), error=push_supervision_error))
        # Even when mutation transport or supervision is uncertain, GET-reconcile once;
        # no path ever repeats the push command, creates a PR or edits the existing PR.
        reconcile_push()
        assert git_verified and api_verified and pr_verified, 'Push outcome unverified; no automatic retry'
        public = api('repos/kevinrhaas/chicago/git/commits/' + head)
        save(out / 'PUBLIC-COMMIT.json', public)
        assert public['tree']['sha'] == SOURCE['TREE'] and [p['sha'] for p in public['parents']] == [OLD_HEAD, BASE]
        assert source(head, False) == final
        assert push_supervision_error is None, 'Remote reconciled, but supervision/resource proof failed; ROOT review required'
    except BaseException as exc:
        error = repr(exc)
    finally:
        try:
            actual_head = val('rev-parse', 'HEAD')
            actual = source(actual_head, actual_head == OLD_HEAD)
        except BaseException as exc:
            actual = None
            source_error = repr(exc)
        resources = guard.pair(start, guard.snapshot())
        safe_cleanup = not in_flight and all(row['cleanup']['cleanup_complete'] and not row['cleanup']['remaining_owned_children'] for row in rows)
        if safe_cleanup and scratch.exists():
            shutil.rmtree(scratch)
        scratch_clean = not scratch.exists()
        success = bool(head and git_verified and api_verified and pr_verified and error is None
                       and source_error is None and resources['accepted'] and scratch_clean)
        closed = dict(status='EXACT_DRIVER_MERGE_COMMIT_QA_PUBLICATION_EXISTING_PR_PUSH_PASS_CI_PENDING' if success
                      else 'INTEGRATION_DELIVERY_NONPASS_OR_UNCERTAIN_NO_AUTOMATIC_MUTATION_RETRY',
                      source_before=before, source=actual, parents=[OLD_HEAD, BASE], full_fourpart_receipt=binding['full_fourpart'],
                      retained_negative_and_canonical_repair_proofs=binding['additional_proofs'],
                      exact_qualified_integration_base=BASE, remote_dev_observations=dev_observations,
                      require_remote_dev_exact_reviewed_base=binding['require_remote_dev_exact_reviewed_base'],
                      latest_DEV_acceptance_claimed=False, later_DEV_tree_requalified=False,
                      source_commit_bridge=dict(path=str(out / 'SOURCE-COMMIT-BRIDGE.json'), sha256=sha(out / 'SOURCE-COMMIT-BRIDGE.json'))
                          if (out / 'SOURCE-COMMIT-BRIDGE.json').exists() else None,
                      ordinary_merge_commit_attempted=commit_attempted, normal_feature_push_attempted=push_attempted,
                      Git_remote_readback_verified=git_verified, API_remote_readback_verified=api_verified,
                      existing_PR_number=1693, existing_PR_head_verified=pr_verified,
                      ledger=rows, resources=resources, owned_TMPDIR_cleanup_complete=scratch_clean,
                      error=error, source_error=source_error, commit_supervision_error=commit_supervision_error,
                      push_supervision_error=push_supervision_error, binding_path=str(args.binding), binding_sha256=binding_hash,
                      execution_pins=binding['execution_pins'], runner_sha256=sha(__file__),
                      native_GIT_NO_LAZY_FETCH_absent='GIT_NO_LAZY_FETCH' not in env,
                      metadata_git_GIT_NO_LAZY_FETCH=metadata_env['GIT_NO_LAZY_FETCH'],
                      all_four_same_TREE=True, closed_utc=utc(), CI_PASS_claimed=False, DEV_merged=False,
                      production_promoted=False, PR_created_or_edited=False, ticket_state_changes_performed=False,
                      existing_own_lap_untouched=True, CI_dispatches_or_reruns_performed=False)
        save(out / 'CLOSED.json', closed)
        print(json.dumps(dict(status=closed['status'], HEAD=head, PR=1693, error=error, receipt=str(out / 'CLOSED.json'))), flush=True)
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
