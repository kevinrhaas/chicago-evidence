#!/usr/bin/env python3
"""Run four fresh native preflight parts against one pinned staged source.

Prepared helper only: execution requires ROOT's explicit launch. Does not commit,
push, change application files, update tracking refs, or reinterpret old results.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent
SUPERVISOR = Path('/workspace/.cloud-setup/transport-supervise.py')
OWNER_LOCK = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
BASELINE_SHA = '3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
SUPERVISOR_SHA = 'a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, value): Path(p).write_text(json.dumps(value, indent=2) + '\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text())

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--baseSHA', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve(); app = repo / 'chicago/4d'; out = Path(args.out).resolve()
    assert re.fullmatch('[0-9a-f]{40}', args.baseSHA), 'A full reviewed base SHA is required'
    assert not out.exists(), 'Use a fresh output directory; preserve previous runs'
    assert repo.is_dir() and (app / 'tools/preflight.sh').is_file()
    assert sys.version_info[:2] == (3, 11)
    assert subprocess.check_output(['node', '--version'], timeout=5).decode().startswith('v22.')
    assert digest(HERE / 'RESTORED-RUNTIME-BASELINE.json') == BASELINE_SHA
    assert digest(SUPERVISOR) == SUPERVISOR_SHA
    guard_spec = importlib.util.spec_from_file_location('current_resource_guard', HERE / 'resource_guard.py')
    guard = importlib.util.module_from_spec(guard_spec); guard_spec.loader.exec_module(guard)
    lock = OWNER_LOCK.open('a+'); fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1', CHECK_JOBS='4',
               C4D_GATE_REQUIRE_READERS='1', C4D_GATE_REQUIRE_BASE='1')
    for key in ['CHICAGO_TICKETS_DIR', 'CHECK_PART', 'BASE', 'CHECK_TIMINGS']:
        env.pop(key, None)
    def git(*cmd):
        return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
                                        '-C', str(repo), *cmd], env=env, timeout=60)
    def val(*cmd): return git(*cmd).decode().strip()
    assert val('rev-parse', args.baseSHA + '^{commit}') == args.baseSHA
    private_base = 'refs/transport/preflight-reviewed-base-' + args.baseSHA
    existing = subprocess.run(['git', '-C', str(repo), 'rev-parse', '--verify', '-q', private_base],
                              env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    if existing.returncode == 1:
        git('update-ref', private_base, args.baseSHA, '0' * 40)
    else:
        assert existing.returncode == 0 and existing.stdout.strip() == args.baseSHA
    # The native preflight's fetch of this private ref may print its documented
    # cached-ref notice. It cannot advance origin/dev or the exact private base.
    env.update(BASE=private_base, C4D_RULINGS_BASE=private_base)
    def source():
        assert not git('ls-files', '-u').strip(), 'Resolve authored/generated conflicts first'
        assert not git('diff', '--name-only').strip(), 'Stage the exact intended source first'
        assert val('rev-parse', private_base) == args.baseSHA
        mh = subprocess.run(['git', '-C', str(repo), 'rev-parse', '--verify', '-q', 'MERGE_HEAD'],
                            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        assert mh.returncode in (0, 1)
        tree = val('write-tree')
        return dict(HEAD=val('rev-parse', 'HEAD'), MERGE_HEAD=mh.stdout.strip() if mh.returncode == 0 else None,
                    TREE=tree, APP=val('rev-parse', tree + ':chicago/4d'),
                    semantic_index_sha256=hashlib.sha256(git('ls-files', '--stage', '-z')).hexdigest(),
                    private_base_ref=private_base, reviewed_base_SHA=args.baseSHA)
    original = source()
    text = (app / 'tools/check.sh').read_text()
    declarations = re.findall(r'(?m)^[ \t]*(?:(every_part)\s+)?(step|selftest)\s+', text)
    assert declarations, 'Native step declarations must be readable'
    expected = {str(k): dict(selected_steps=0, selftests=0, elsewhere_steps=0) for k in range(1, 5)}
    for ordinal, (every, kind) in enumerate(declarations, 1):
        for k in range(1, 5):
            row = expected[str(k)]
            if every or (ordinal - 1) % 4 + 1 == k:
                row['selected_steps'] += 1; row['selftests'] += int(kind == 'selftest')
            else:
                row['elsewhere_steps'] += 1
    distinct = len(declarations)
    selftests = sum(kind == 'selftest' for _, kind in declarations)
    overlaps = 3 * sum(bool(every) for every, _ in declarations)
    selftest_overlaps = 3 * sum(bool(every) and kind == 'selftest' for every, kind in declarations)
    out.mkdir(parents=True)
    pins = {str(p): digest(p) for p in [Path(__file__), SUPERVISOR, HERE / 'resource_guard.py',
            HERE / 'RESTORED-RUNTIME-BASELINE.json', app / 'tools/preflight.sh',
            app / 'tools/check.sh', app / 'tools/check_harness.sh']}
    state = dict(status='RUNNING_NOT_PASS', created_utc=utc(), source_before=original,
                 native_distinct_steps=distinct, native_selftests=selftests,
                 every_part_execution_overlap=overlaps, expected_parts=expected,
                 execution_pins=pins, original_cap_per_part_seconds=600, ledger=[])
    save(out / 'STATE.json', state)
    save(out / 'SOURCE-BEFORE.json', original)
    def footer(body, part):
        body = ANSI.sub('', body)
        f = re.findall(r'^CHECK PASS[^\n]*part ' + str(part) + r'/4:\s*(\d+) steps, none red\.$', body, re.M)
        other = re.findall(r'^  This is part ' + str(part) + r' of 4; the other (\d+) steps are in the other parts\.', body, re.M)
        st = re.findall(r'^  (\d+) of them are self-tests that prove a gate by breaking it;', body, re.M)
        assert len(f) == len(other) == len(st) == 1 and not re.search(r'^CHECK FAIL', body, re.M)
        assert 'green only when every part is: tools/check.sh --part 1/4 through --part 4/4.' in body
        got = dict(selected_steps=int(f[0]), selftests=int(st[0]), elsewhere_steps=int(other[0]))
        assert got == expected[str(part)], (got, expected[str(part)])
        return got
    scratch = out / 'native-tmp'; scratch.mkdir(mode=0o700)
    env['TMPDIR'] = str(scratch)
    failure = None
    in_flight = False
    try:
        for part in range(1, 5):
            assert source() == original
            assert all(digest(p) == sha for p, sha in pins.items())
            before = guard.snapshot(); assert guard.check(before)['accepted']
            env['CHECK_PART'] = str(part) + '/4'
            prefix = out / ('native-preflight-part-' + str(part))
            logs = [Path('/tmp/preflight-' + name + '.log') for name in ['check', 'cl', 'ids']]
            prior = {str(p): (p.stat().st_mtime_ns, p.stat().st_ctime_ns) if p.exists() else None for p in logs}
            state.update(active_part=part, active_command=['bash', 'tools/preflight.sh'])
            save(out / 'STATE.json', state)
            in_flight = True
            with Path(str(prefix) + '.supervisor.stdout').open('xb', buffering=0) as output:
                q = subprocess.run([sys.executable, str(SUPERVISOR), '--prefix', str(prefix), '--cwd',
                                    str(app), '--timeout', '600', '--', 'bash', 'tools/preflight.sh'],
                                   env=env, stdout=output, stderr=subprocess.STDOUT)
            result = load(str(prefix) + '.result.json'); cleanup = load(str(prefix) + '.cleanup.json')
            in_flight = not (cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'])
            after = guard.snapshot(); resources = guard.pair(before, after)
            copied = []
            for p in logs:
                if p.exists():
                    stamp = (p.stat().st_mtime_ns, p.stat().st_ctime_ns)
                    fresh = prior[str(p)] is None or prior[str(p)] != stamp
                    target = out / ('part-' + str(part) + '-' + p.name)
                    shutil.copy2(p, target)
                    copied.append(dict(native_path=str(p), path=str(target), fresh=fresh,
                                       bytes=target.stat().st_size, sha256=digest(target)))
                else:
                    copied.append(dict(native_path=str(p), path=None, fresh=False, missing=True))
            try: after_source = source(); source_error = None
            except BaseException as error: after_source = None; source_error = repr(error)
            row = dict(part=part, command=['bash', 'tools/preflight.sh'], CHECK_PART=env['CHECK_PART'],
                       result=result, cleanup=cleanup, resources=resources,
                       resource_before=before, resource_after=after, source_before=original,
                       source_after=after_source, source_error=source_error,
                       copied_native_logs=copied, supervisor_log=str(prefix) + '.log',
                       supervisor_log_sha256=digest(str(prefix) + '.log'))
            state['ledger'].append(row); save(out / 'STATE.json', state)
            assert q.returncode == result['returncode'] == 0 and not result['timed_out']
            assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 600
            assert result['timeout_override_reason'] is None
            assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
            assert resources['accepted'] and after_source == original
            assert len(copied) == 3 and all(p['fresh'] for p in copied)
            native_body = (out / ('part-' + str(part) + '-preflight-check.log')).read_text(errors='replace')
            row['native_footer_counts'] = footer(native_body, part)
            preflight_body = ANSI.sub('', Path(str(prefix) + '.log').read_text(errors='replace'))
            assert len(re.findall(r'^PREFLIGHT PASS\b', preflight_body, re.M)) == 1
            assert not re.search(r'^PREFLIGHT FAIL\b', preflight_body, re.M)
            save(out / 'STATE.json', state)
        assert len(state['ledger']) == 4
        assert sum(r['native_footer_counts']['selected_steps'] for r in state['ledger']) - overlaps == distinct
        assert sum(r['native_footer_counts']['selftests'] for r in state['ledger']) - selftest_overlaps == selftests
        assert source() == original and all(digest(p) == sha for p, sha in pins.items())
        state.update(status='PASS_ALL_FOUR_NATIVE_PREFLIGHT_PARTS_SAME_SOURCE', source_after=source(),
                     total_native_part_seconds=sum(r['result']['seconds'] for r in state['ledger']))
    except BaseException as error:
        failure = error
        state.update(status='NONPASS_NO_AUTOMATIC_RETRY', error=repr(error))
    finally:
        state['closed_utc'] = utc()
        # Preserve all native/raw diagnostics. Remove only this helper's isolated
        # native scratch after its supervised children have been cleaned up.
        safe_cleanup = not in_flight and all(r['cleanup']['cleanup_complete'] and not r['cleanup']['remaining_owned_children']
                           for r in state['ledger'])
        if safe_cleanup and scratch.exists(): shutil.rmtree(scratch)
        state['owned_TMPDIR_cleanup_complete'] = not scratch.exists()
        if not state['owned_TMPDIR_cleanup_complete']:
            state['status'] = 'NONPASS_OWNED_NATIVE_SCRATCH_RETAINED'
        save(out / 'STATE.json', state); save(out / 'CLOSED.json', state)
    print(json.dumps(dict(status=state['status'], receipt=str(out / 'CLOSED.json')), flush=True))
    if failure is not None: raise failure
    return 0 if state['status'].startswith('PASS_') else 1

if __name__ == '__main__':
    raise SystemExit(main())
