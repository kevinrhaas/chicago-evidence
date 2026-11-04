"""Run the repository's unchanged CI-gated PR refresh for ONLY1693, outside ROOT.

This is the existing automated integration path: refresh, normal feature push,
then CI; it never merges DEV. A normal push and native lap checks retain their
original race/refusal behavior. No force, timeout increase or guard patch.
"""
from pathlib import Path
import datetime, fcntl, hashlib, importlib.util, json, os, subprocess, sys, time

B = Path('/workspace/.cloud-setup/transport-current-20261103')
R = Path('/workspace/chicago-transport-current-20261103')
O = B / 'actual-driver1693-official-owner-reviewed-refresh-03'
W = Path('/tmp/chicago-pr1693-official-refresh-20261104')
BRANCH = 'steward/t2804-independent-driver-looking-20261104'
OLD = '27d52718290a2708f70ca536c6b796a83a936601'
SUP = '/workspace/.cloud-setup/transport-supervise.py'

def save(name, value):
    (O / name).write_text(json.dumps(value, indent=2) + '\n')

def git(repo, *args):
    return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
                                    '-C', str(repo), *args], timeout=45)

def source():
    return dict(HEAD=git(R, 'rev-parse', 'HEAD').decode().strip(),
                TREE=git(R, 'write-tree').decode().strip(),
                index_sha256=hashlib.sha256(git(R, 'ls-files', '--stage', '-z')).hexdigest(),
                status=git(R, 'status', '--porcelain').decode())

def api(endpoint):
    endpoint += ('&' if '?' in endpoint else '?') + 'isolated_refresh=' + str(time.time_ns())
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/kevinrhaas/chicago/' + endpoint], timeout=40))

def main():
    assert not O.exists() and W.is_dir() and (W / '.git').is_dir(), 'Existing owned isolated checkout and fresh evidence required'
    initial = source()
    assert initial['HEAD'] == OLD and initial['status'] == ''
    lock = open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock', 'a+')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    spec = importlib.util.spec_from_file_location('isolated_refresh_guard', B / 'resource_guard.py')
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    rb = guard.snapshot()
    assert guard.check(rb)['accepted']
    O.mkdir()
    assert W.is_dir()
    scratch = O / 'native-tmp'
    scratch.mkdir(mode=0o700)
    env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
               CHECK_JOBS='4', LAP_ONLY='1693', LAP_BASE='dev')
    for name in ['GIT_NO_LAZY_FETCH', 'CHICAGO_TICKETS_DIR', 'CHECK_PART', 'BASE',
                 'CHECK_TIMINGS', 'C4D_RULINGS_BASE', 'C4D_GATE_REQUIRE_BASE', 'C4D_GATE_REQUIRE_READERS']:
        env.pop(name, None)
    rows = []
    error = None
    public = None
    in_flight = False

    def run(label, command, cap, cwd=W):
        nonlocal in_flight
        before = guard.snapshot()
        assert guard.check(before)['accepted']
        assert source() == initial, 'ROOT source changed; no further service work'
        prefix = O / label
        save('STATE.json', dict(status='ACTIVE_OFFICIAL_SINGLE_PR_REFRESH_NOT_DEV_MERGE', active=label,
                                source_before=initial, ledger=rows))
        in_flight = True
        with (O / (label + '-owner.stdout')).open('xb') as stream:
            q = subprocess.run([sys.executable, SUP, '--prefix', str(prefix), '--cwd', str(cwd),
                                '--timeout', str(cap), '--', *command], env=env,
                               stdout=stream, stderr=subprocess.STDOUT)
        result = json.loads(Path(str(prefix) + '.result.json').read_text())
        cleanup = json.loads(Path(str(prefix) + '.cleanup.json').read_text())
        resources = guard.pair(before, guard.snapshot())
        row = dict(label=label, result=result, cleanup=cleanup, resources=resources,
                   log=str(prefix) + '.log')
        rows.append(row)
        save('LEDGER.json', rows)
        in_flight = not (cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'])
        assert q.returncode == result['returncode'] == 0 and not result['timed_out']
        assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == cap
        assert result['timeout_override_reason'] is None
        assert not in_flight and resources['accepted']
        assert source() == initial
        return row

    try:
        pr = api('pulls/1693')
        save('PR-BEFORE.json', pr)
        assert pr['state'] == 'open' and not pr['draft'] and not pr['merged']
        if pr['head']['sha'] != OLD:
            public = pr
            raise RuntimeError('Another official refresh already changed public HEAD; reconcile it, do not duplicate')
        assert not git(W, 'status', '--porcelain').strip(), 'Isolated checkout has unexpected source edits'
        run('02-fetch-current-public-inputs', ['git', '-c', 'gc.auto=0', 'fetch', '--filter=blob:none',
             '--no-recurse-submodules', 'origin', '+refs/heads/dev:refs/remotes/origin/dev',
             '+refs/heads/' + BRANCH + ':refs/remotes/origin/' + BRANCH], 120)
        run('03-checkout-current-dev', ['git', 'checkout', '--detach', 'origin/dev'], 120)
        proof_path = Path('/workspace/.cloud-setup/transport-driver1693-owner-content-resolution-20261104/RESOLUTION-PROOF.json')
        assert hashlib.sha256(proof_path.read_bytes()).hexdigest() == '46f557adad69e862a8b0f6ae0a19ceb65cf846379526f0a40e8f9a2a1fd160a4'
        proof = json.loads(proof_path.read_text())
        for item in proof['files']:
            path = item['repo_path']
            for ref, label in [('origin/dev', 'THEIRS'), ('origin/' + BRANCH, 'OURS'), (proof['source_commits']['base'], 'BASE')]:
                assert hashlib.sha256(git(W, 'show', ref + ':' + path)).hexdigest() == item['preimages'][label]['sha256'], 'Fixed reviewed preimage changed: ' + path + ' ' + label
        driver = B / 'fixed_reviewed_pr1693_content_driver.py'
        command = sys.executable + ' ' + str(driver) + ' %O %A %B %P'
        subprocess.run(['git', '-C', str(W), 'config', 'merge.root-reviewed-pr1693.driver', command], check=True, env=env, timeout=10)
        attributes = W / '.git/info/attributes'
        prior_attributes = attributes.read_bytes() if attributes.exists() else b''
        (O / 'INFO-ATTRIBUTES-BEFORE.bin').write_bytes(prior_attributes)
        added = b'\nchicago/4d/docs/STATUS.md merge=root-reviewed-pr1693\nchicago/4d/tools/step_isolation.json merge=root-reviewed-pr1693\n'
        owner_attributes = O / 'OWNER-REVIEWED-ATTRIBUTES'
        owner_attributes.write_bytes(added)
        subprocess.run(['git', '-C', str(W), 'config', 'core.attributesFile', str(owner_attributes)], check=True, env=env, timeout=10)
        selected = git(W, 'check-attr', 'merge', '--', 'chicago/4d/docs/STATUS.md', 'chicago/4d/tools/step_isolation.json').decode()
        assert selected.count(': merge: root-reviewed-pr1693') == 2, selected
        (O / 'ACTUAL-OWNER-ATTRIBUTE-SELECTION.txt').write_text(selected)
        save('OWNER-REVIEWED-RESOLUTION-ADMISSION.json', dict(proof_path=str(proof_path), proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(), driver_path=str(driver), driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(), fixed_paths=[item['repo_path'] for item in proof['files']], only_fixed_reviewed_inputs_accepted=True, upstream_bytes_preserved=True, permanent_repo_attributes_or_script_changed=False))
        script = W / '.github/steward/pr-lap.sh'
        script_bytes = script.read_bytes()
        assert script_bytes == git(W, 'show', 'origin/dev:.github/steward/pr-lap.sh'), 'Official script changed'
        save('SERVICE-INPUTS.json', dict(current_DEV=git(W, 'rev-parse', 'origin/dev').decode().strip(), prior_feature=git(W, 'rev-parse', 'origin/' + BRANCH).decode().strip(), official_script_sha256=hashlib.sha256(script_bytes).hexdigest(), script_unmodified=True, only_PR=1693, policy='Owner-reviewed fixed content resolutions supplied to unchanged automated refresh; CI gates public result before DEV merge'))
        run('04-UNCHANGED-OFFICIAL-PR1693-REFRESH', ['bash', '.github/steward/pr-lap.sh',
                                                 '--repo', 'kevinrhaas/chicago'], 600)
        public = api('pulls/1693')
        save('PR-AFTER.json', public)
        save('DEV-AFTER.json', api('git/ref/heads/dev'))
        assert public['head']['sha'] != OLD, 'Official service made no public update; inspect exact native refusal'
        compare = api('compare/' + OLD + '...' + public['head']['sha'])
        save('PUBLIC-NORMAL-DESCENDANT.json', compare)
        assert compare['status'] == 'ahead' and compare['merge_base_commit']['sha'] == OLD
    except BaseException as exc:
        error = repr(exc)
    finally:
        after = source()
        resources = guard.pair(rb, guard.snapshot())
        clean = not in_flight and all(row['cleanup']['cleanup_complete'] and
                    not row['cleanup']['remaining_owned_children'] for row in rows)
        # Retain owned checkout and scratch for review; no unowned deletion or process signalling.
        ok = error is None and resources['accepted'] and after == initial and clean
        closed = dict(status='OFFICIAL_SINGLE_PR_REFRESH_PUBLIC_NORMAL_DESCENDANT_VERIFIED_CI_PENDING'
                      if ok else 'OFFICIAL_ISOLATED_REFRESH_NONPASS_REVIEW_NO_AUTOMATIC_RETRY',
                      error=error, source_before=initial, source_after=after, resources=resources,
                      ledger=rows, owned_descendants_cleanup_complete=clean,
                      owned_checkout_retained=str(W), owned_scratch_retained=str(scratch),
                      public_head=public['head']['sha'] if public else None,
                      DEV_merge_performed=False, force_push=False, script_modified=False,
                      local_whole_gate_retargeted=False, fresh_public_CI_required_before_DEV_merge=True,
                      closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        save('CLOSED.json', closed)
        print(json.dumps({k: closed[k] for k in ['status', 'error', 'public_head']}), flush=True)
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
