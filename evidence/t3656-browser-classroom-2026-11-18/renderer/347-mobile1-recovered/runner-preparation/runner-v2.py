#!/usr/bin/env python3
"""Durable, pinned mobile stages 1–12 only. Never publishes, edits source, or retries."""
import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

SCHEMA = 1
STAGES = list(range(1, 13))
GUARDS = {
    'suite_completion': 'mobile 390x780: the suite body ran to completion',
    'page_errors': 'mobile 390x780: zero page errors',
    'vendor_decoder': 'vendor: meshopt decoder loads and reports supported',
    'vendor_import': 'vendor: meshopt import raises no page error',
}
CHILD = None
STOP_SIGNAL = None

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def durable_json(path, value):
    path = Path(path)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('w') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def event(out, kind, **payload):
    with (out / 'events.ndjson').open('a') as f:
        f.write(json.dumps({'utc': now(), 'kind': kind, **payload}, sort_keys=True) + '\n')
        f.flush()
        os.fsync(f.fileno())

def git(repo, *args):
    return subprocess.check_output(['git', *args], cwd=repo, text=True, timeout=45).strip()

def required_equal(label, actual, expected):
    if actual != expected:
        raise RuntimeError(f'{label} mismatch: expected {expected!r}; observed {actual!r}')

def load_config(path):
    cfg = json.loads(Path(path).read_text())
    for key in ['expected_head', 'expected_tree']:
        if not re.fullmatch('[0-9a-f]{40}', cfg.get(key, '')):
            raise ValueError(f'{key} requires a final approved 40-character Git SHA')
    for key in ['expected_harness_sha256', 'expected_main_sha256']:
        if not re.fullmatch('[0-9a-f]{64}', cfg.get(key, '')):
            raise ValueError(f'{key} requires the final SHA256')
    if not cfg.get('expected_build', {}).get('built_utc') or not cfg['expected_build'].get('version'):
        raise ValueError('Exact final expected_build.version and built_utc are required')
    for key in ['repo', 'app', 'mirror', 'node', 'chromium', 'bc_directory']:
        if not Path(cfg[key]).is_absolute():
            raise ValueError(f'{key} must be absolute')
    stages = cfg.get('stages', STAGES)
    if (not isinstance(stages, list) or not stages or
            any(type(n) is not int or n not in STAGES for n in stages) or
            stages != list(range(stages[0], stages[-1] + 1))):
        raise ValueError('Requested stages must be one explicit contiguous subset of mobile1–12')
    return cfg

def provenance(cfg):
    repo, app, mirror = map(Path, [cfg['repo'], cfg['app'], cfg['mirror']])
    head, tree = git(repo, 'rev-parse', 'HEAD', 'HEAD^{tree}').splitlines()
    required_equal('HEAD', head, cfg['expected_head'])
    required_equal('Git tree', tree, cfg['expected_tree'])
    dirty = git(repo, 'status', '--porcelain=v1', '--untracked-files=normal')
    if dirty:
        raise RuntimeError('Primary worktree is dirty; refusing a mixed candidate')
    refs = {name: git(repo, 'rev-parse', name) for name in cfg.get('frozen_refs', {})}
    required_equal('Explicit frozen refs', refs, cfg.get('frozen_refs', {}))
    harness = file_sha(app / 'tools/smoke_renderer.mjs')
    source_main = file_sha(app / 'renderers/web/js/main.js')
    mirror_main = file_sha(mirror / 'walk/js/main.js')
    required_equal('Harness SHA256', harness, cfg['expected_harness_sha256'])
    required_equal('Source main SHA256', source_main, cfg['expected_main_sha256'])
    required_equal('Published main SHA256', mirror_main, source_main)
    build = json.loads((mirror / 'build.json').read_text())
    for key, val in cfg['expected_build'].items():
        required_equal(f'Published build {key}', build.get(key), val)
    return {'checked_utc': now(), 'head': head, 'git_tree': tree,
            'source_app_git_tree': git(repo, 'rev-parse', f'HEAD:{app.relative_to(repo)}'),
            'worktree_clean': True, 'frozen_refs': refs, 'harness_sha256': harness,
            'source_main_sha256': source_main, 'published_main_sha256': mirror_main,
            'publication_build': build,
            'operator_supplied_smoke_tree_hash': cfg.get('smoke_tree_hash'),
            'smoke_tree_note': 'Operator descriptor; independently checked Git trees and hashes are separate fields.'}

def mirror_inventory(root, hash_content):
    """Hash all contents at cohort boundaries; stat every file between stages."""
    rows = []
    for path in sorted(Path(root).rglob('*')):
        if path.is_symlink():
            raise RuntimeError(f'Unexpected mirror symlink requires explicit review: {path}')
        if not path.is_file():
            continue
        st = path.stat()
        row = {'path': path.relative_to(root).as_posix(), 'size': st.st_size,
               'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns,
               'inode': st.st_ino, 'device': st.st_dev}
        if hash_content:
            row['sha256'] = file_sha(path)
        rows.append(row)
    if not rows:
        raise RuntimeError('Published mirror is empty')
    return rows

def metadata(rows):
    return [{k: v for k, v in row.items() if k != 'sha256'} for row in rows]

def mirror_checks(cfg, baseline, full=False):
    rows = mirror_inventory(Path(cfg['mirror']), full)
    required_equal('Frozen mirror file inventory/stat digest', sha(canonical(metadata(rows))),
                   sha(canonical(metadata(baseline))))
    if full:
        required_equal('Frozen mirror full-content digest', sha(canonical(rows)), sha(canonical(baseline)))
    return {'checked_utc': now(), 'files': len(rows), 'bytes': sum(r['size'] for r in rows),
            'metadata_sha256': sha(canonical(metadata(rows))),
            'full_content_checked': full,
            'inventory_sha256': sha(canonical(rows)) if full else None}

def active_renderers():
    found = []
    for p in Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name) == os.getpid():
            continue
        try:
            stat = (p / 'stat').read_text().rsplit(')', 1)[1].split()
            if stat[0] == 'Z':
                continue
            comm = (p / 'comm').read_text().strip()
            args = (p / 'cmdline').read_bytes().split(b'\0')
            smoke = any(a.endswith(b'/smoke_renderer.mjs') or a == b'tools/smoke_renderer.mjs' for a in args)
            if comm in ['chromium', 'chrome', 'headless_shell'] or smoke:
                found.append({'pid': int(p.name), 'comm': comm, 'state': stat[0]})
        except (OSError, IndexError):
            pass
    return found

def assert_quiet():
    active = active_renderers()
    if active:
        raise RuntimeError(f'Active local renderer; no unowned process will be killed: {active}')
    return {'utc': now(), 'active_local_renderers': []}

def parse_log(text, stage, mirror, exit_code):
    lines = text.splitlines()
    checks = []
    issues = []
    for number, line in enumerate(lines, 1):
        m = re.fullmatch(r'\s*(pass|FAIL)\s+\[(\d+):([0-5]\d)\]\s+(.*)', line)
        if m:
            checks.append({'line': number, 'outcome': m[1], 'seconds': int(m[2])*60+int(m[3]),
                           'text': m[4], 'raw': line})
        elif re.match(r'^\s*(pass|FAIL)\s+', line):
            issues.append(f'Malformed or untimed check at line {number}')
    summaries = [(i, re.fullmatch(r'(\d+) passed, (\d+) failed', line)) for i, line in enumerate(lines)]
    summaries = [(i, m) for i, m in summaries if m]
    sections = [(i, re.fullmatch(r'(\d+) staged-section check\(s\) \(stage (\d+) of 15\), (\d+) always-on check\(s\)', line)) for i, line in enumerate(lines)]
    sections = [(i, m) for i, m in sections if m]
    runtimes = [(i, re.match(r'^(\d+) m (\d+) s for stage (\d+) at (mobile|desktop)\b', line)) for i, line in enumerate(lines)]
    runtimes = [(i, m) for i, m in runtimes if m]
    verdicts = [(i, line) for i, line in enumerate(lines) if line in ['SMOKE PASS', 'SMOKE FAIL']]
    nonempty = [i for i, line in enumerate(lines) if line.strip()]
    served = [line for line in lines if line.startswith('serving ')]
    if len(served) != 1 or not re.fullmatch(re.escape(f'serving {mirror}') + r' on \d+ — PUBLISHED mirror \(compressed assets, visitor layout\)', served[0] if served else ''):
        issues.append('Wrong or non-unique published-mirror header')
    if lines.count('NOT THE FULL GATE — viewports filtered to "mobile"') != 1:
        issues.append('Missing/non-unique mobile-only header')
    if lines.count(f'NOT THE FULL GATE — stages filtered to "{stage}" of 15') != 1:
        issues.append('Missing/non-unique exact single-stage header')
    if sum(line.startswith('NOT THE FULL GATE — stages filtered') for line in lines) != 1:
        issues.append('Grouped or concatenated stage headers')
    if not (len(summaries) == len(sections) == len(runtimes) == len(verdicts) == 1):
        issues.append('Incomplete or non-unique final footer')
    summary = counts = runtime = None
    if len(summaries) == len(sections) == len(runtimes) == len(verdicts) == 1:
        si, s = summaries[0]; ci, c = sections[0]; ti, t = runtimes[0]; vi, verdict = verdicts[0]
        summary = {'passed': int(s[1]), 'failed': int(s[2])}
        counts = {'staged': int(c[1]), 'stage': int(c[2]), 'always_on': int(c[3])}
        runtime = {'seconds': int(t[1])*60+int(t[2]), 'stage': int(t[3]), 'viewport': t[4]}
        if not (si < ci < ti < vi == nonempty[-1]) or verdict != 'SMOKE PASS':
            issues.append('Wrong footer order or terminal PASS')
        if counts['stage'] != stage or runtime['stage'] != stage or runtime['viewport'] != 'mobile':
            issues.append('Wrong final stage/viewport')
        if counts['always_on'] != 13 or counts['staged'] <= 0:
            issues.append('Missing selected body or wrong always-on count')
        if summary != {'passed': sum(c['outcome'] == 'pass' for c in checks), 'failed': sum(c['outcome'] == 'FAIL' for c in checks)}:
            issues.append('Observed timed checks disagree with footer')
        if summary['failed'] or summary['passed'] != counts['staged'] + counts['always_on']:
            issues.append('Failed checks or inconsistent check totals')
        if any(c['line'] > si for c in checks):
            issues.append('Check after final summary')
    guards = {key: [c for c in checks if c['text'] == name] for key, name in GUARDS.items()}
    for key, matches in guards.items():
        if len(matches) != 1 or matches[0]['outcome'] != 'pass':
            issues.append(f'Missing, duplicate or failed mandatory guard: {key}')
    if exit_code != 0:
        issues.append(f'No successful durable process exit: {exit_code!r}')
    return {'passed': not issues, 'issues': issues, 'summary': summary, 'section_counts': counts,
            'runtime': runtime, 'required_guards': guards,
            'observed_checks': len(checks), 'failed_checks': [c for c in checks if c['outcome'] == 'FAIL'],
            'last_check': checks[-1] if checks else None,
            'last_nonempty_line': lines[nonempty[-1]] if nonempty else None}

def stop_handler(signum, _frame):
    global STOP_SIGNAL
    STOP_SIGNAL = signum
    if CHILD is not None and CHILD.poll() is None:
        try:
            os.killpg(CHILD.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

def require_not_stopped():
    if STOP_SIGNAL:
        raise RuntimeError(f'Supervisor interrupted by signal {STOP_SIGNAL}')

def cleanup_owned_child():
    """Never kill an unowned renderer; reap our live timeout group on supervisor errors."""
    global CHILD
    if CHILD is None:
        return {'needed': False}
    child = CHILD
    receipt = {'needed': True, 'timeout_pid': child.pid, 'process_group': child.pid}
    def group_members():
        found = []
        for path in Path('/proc').iterdir():
            if not path.name.isdigit():
                continue
            try:
                fields = (path / 'stat').read_text().rsplit(')', 1)[1].split()
                if fields[0] != 'Z' and int(fields[2]) == child.pid:
                    found.append(int(path.name))
            except (OSError, ValueError, IndexError):
                pass
        return found
    def wait_group(seconds):
        deadline = time.monotonic() + seconds
        while group_members() and time.monotonic() < deadline:
            child.poll()
            time.sleep(0.1)
        return group_members()
    try:
        if group_members():
            try:
                os.killpg(child.pid, signal.SIGTERM)
                receipt['term_sent_utc'] = now()
            except ProcessLookupError:
                pass
            if wait_group(6):
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                    receipt['kill_sent_utc'] = now()
                except ProcessLookupError:
                    pass
                receipt['remaining_live_owned_pids'] = wait_group(5)
        receipt['exit_code'] = child.wait(timeout=1)
    except BaseException as exc:
        receipt['cleanup_error'] = f'{type(exc).__name__}: {exc}'
    finally:
        CHILD = None
    return receipt

def execute(cfg, out, resume):
    global CHILD
    requested_stages = cfg.get('stages', STAGES)
    out = Path(out).resolve()
    if not out.exists():
        out.mkdir(parents=True)
    lock = (out / 'supervisor.lock').open('a+')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    config_digest = sha(canonical(cfg))
    script_digest = file_sha(__file__)
    manifest_path = out / 'manifest.json'
    if manifest_path.exists():
        if not resume:
            raise RuntimeError('Existing cohort requires --resume; no files will be overwritten')
        manifest = json.loads(manifest_path.read_text())
        required_equal('Cohort configuration', manifest['config_sha256'], config_digest)
        required_equal('Supervisor script', manifest['runner_sha256'], script_digest)
        if manifest.get('status') not in ['running', 'completed']:
            raise RuntimeError('Prior failure/interruption requires review and a new cohort; automatic retry forbidden')
        baseline = json.loads((out / 'mirror-inventory.json').read_text())
        required_equal('Stored mirror inventory', sha(canonical(baseline)), manifest['mirror_inventory_sha256'])
        for row in manifest['stages']:
            if row['status'] != 'passed' or row.get('exit_code') != 0 or not row.get('ended_utc'):
                raise RuntimeError(f'Stage {row["stage"]} lacks a durable completed pass; no automatic retry')
            log = out / row['log']
            required_equal('Completed log digest', file_sha(log), row['log_sha256'])
            if not parse_log(log.read_text(errors='replace'), row['stage'], cfg['mirror'], row['exit_code'])['passed']:
                raise RuntimeError('Previously passed log no longer validates')
    else:
        if resume:
            raise RuntimeError('No existing manifest to resume')
        if any(p.name != 'supervisor.lock' for p in out.iterdir()):
            raise RuntimeError('New cohort directory must be empty')
        assert_quiet()
        pins = provenance(cfg)
        baseline = mirror_inventory(Path(cfg['mirror']), True)
        # No renderer starts until the complete baseline and manifest are durable.
        durable_json(out / 'mirror-inventory.json', baseline)
        durable_json(out / 'config.json', cfg)
        manifest = {'schema_version': SCHEMA, 'created_utc': now(), 'status': 'running',
                    'config_sha256': config_digest, 'runner_sha256': script_digest,
                    'scope': f'Fresh local mobile stages {requested_stages[0]}–{requested_stages[-1]} only; not the full renderer gate',
                    'requested_stages': requested_stages,
                    'timeout_seconds': 1200, 'kill_after_seconds': 5,
                    'provenance': pins, 'mirror_inventory_sha256': sha(canonical(baseline)),
                    'mirror_files': len(baseline), 'mirror_bytes': sum(r['size'] for r in baseline),
                    'node_version': subprocess.check_output([cfg['node'], '--version'], text=True).strip(),
                    'chromium_version': subprocess.check_output([cfg['chromium'], '--version'], text=True).strip(),
                    'node_binary_sha256': file_sha(cfg['node']), 'stages': []}
        if not manifest['node_version'].startswith('v22.'):
            raise RuntimeError('Node22 required')
        durable_json(manifest_path, manifest)
        event(out, 'cohort_created', head=cfg['expected_head'], manifest='manifest.json')
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)
    try:
        for stage in requested_stages:
            if any(r['stage'] == stage for r in manifest['stages']):
                continue
            require_not_stopped()
            quiet = assert_quiet()
            pins_before = provenance(cfg)
            mirror_before = mirror_checks(cfg, baseline)
            env = {k: v for k, v in os.environ.items() if not k.startswith('SMOKE_')}
            overrides = {'PATH': f'{Path(cfg["node"]).parent}:{cfg["bc_directory"]}:' + env.get('PATH', '/usr/bin:/bin'),
                         'PW_EXECUTABLE': cfg['chromium'], 'SMOKE_ROOT': cfg['mirror'],
                         'SMOKE_VIEWPORT': 'mobile', 'SMOKE_STAGE': str(stage), 'SMOKE_TIMING': '1'}
            env.update(overrides)
            command = ['/usr/bin/timeout', '--signal=TERM', '--kill-after=5s', '1200s',
                       cfg['node'], 'tools/smoke_renderer.mjs', '--published']
            row = {'stage': stage, 'viewport': 'mobile', 'attempt': 1, 'status': 'starting',
                   'started_utc': now(), 'log': f'mobile-{stage}.log', 'command_argv': command,
                   'cwd': cfg['app'], 'environment_overrides': overrides, 'quiet_before': quiet,
                   'provenance_before': pins_before, 'mirror_before': mirror_before,
                   'supervisor_pid': os.getpid()}
            manifest['stages'].append(row)
            durable_json(manifest_path, manifest)
            event(out, 'stage_start', stage=stage, receipt=row)
            started = time.monotonic()
            with (out / row['log']).open('xb', buffering=0) as log:
                require_not_stopped()
                CHILD = subprocess.Popen(command, cwd=cfg['app'], env=env, stdin=subprocess.DEVNULL,
                                         stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                # A signal can arrive during Popen before CHILD has been assigned.
                if STOP_SIGNAL:
                    stop_handler(STOP_SIGNAL, None)
                row.update({'status': 'running', 'timeout_pid': CHILD.pid, 'process_group': CHILD.pid})
                durable_json(manifest_path, manifest)
                event(out, 'stage_spawned', stage=stage, timeout_pid=CHILD.pid)
                code = CHILD.wait()
                os.fsync(log.fileno())
            row.update({'status': 'verifying', 'ended_utc': now(), 'exit_code': code,
                        'elapsed_seconds': round(time.monotonic()-started, 3), 'stop_signal': STOP_SIGNAL,
                        'log_sha256': file_sha(out / row['log'])})
            durable_json(manifest_path, manifest)
            event(out, 'stage_process_exit', stage=stage, exit_code=code, ended_utc=row['ended_utc'],
                  log_sha256=row['log_sha256'])
            result = parse_log((out / row['log']).read_text(errors='replace'), stage, cfg['mirror'], code)
            row['validation'] = result
            row['provenance_after'] = provenance(cfg)
            row['mirror_after'] = mirror_checks(cfg, baseline)
            # Browser teardown should have completed before the official process exits.
            row['quiet_after'] = assert_quiet()
            row['status'] = 'passed' if result['passed'] and not STOP_SIGNAL else 'failed'
            if code in [124, 137]:
                row['status'] = 'incomplete_capped_or_killed'
            durable_json(out / f'mobile-{stage}-receipt.json', row)
            durable_json(manifest_path, manifest)
            event(out, 'stage_validated', stage=stage, status=row['status'], exit_code=code,
                  summary=result['summary'], issues=result['issues'])
            print(json.dumps({'stage': stage, 'status': row['status'], 'exit_code': code,
                              'elapsed_seconds': row['elapsed_seconds'], 'summary': result['summary'],
                              'receipt': str(out / f'mobile-{stage}-receipt.json')}), flush=True)
            if row['status'] != 'passed':
                raise RuntimeError(f'Stage {stage} did not complete cleanly; stopped without retry')
            # Retain the owned PGID through post-run checks: an exited timeout leader
            # may still have a live descendant that exception cleanup must terminate.
            CHILD = None
        manifest['provenance_final'] = provenance(cfg)
        manifest['mirror_final'] = mirror_checks(cfg, baseline, full=True)
        manifest['quiet_final'] = assert_quiet()
        require_not_stopped()
        manifest['status'] = 'completed'
        manifest['ended_utc'] = now()
        manifest['totals'] = {
            'stages': len(manifest['stages']),
            'reported_passed': sum(r['validation']['summary']['passed'] for r in manifest['stages']),
            'staged_checks': sum(r['validation']['section_counts']['staged'] for r in manifest['stages']),
            'repeated_always_on_checks': sum(r['validation']['section_counts']['always_on'] for r in manifest['stages'])}
        durable_json(manifest_path, manifest)
        event(out, 'cohort_completed', totals=manifest['totals'])
        print(json.dumps({'status': 'completed', 'manifest': str(manifest_path), 'totals': manifest['totals']}), flush=True)
    except BaseException as exc:
        # Cleanup precedes evidence writes: an evidence I/O error must not strand a world.
        manifest['owned_child_cleanup'] = cleanup_owned_child()
        manifest['status'] = 'stopped'
        manifest['stopped_utc'] = now()
        manifest['stop_reason'] = f'{type(exc).__name__}: {exc}'
        durable_json(manifest_path, manifest)
        event(out, 'cohort_stopped', reason=manifest['stop_reason'])
        raise

def self_test():
    mirror = '/workspace/chicago/site/4d'
    fixture = Path('/tmp/t3656-b1-mobile-2.log').read_text()
    good = parse_log(fixture, 2, mirror, 0)
    assert good['passed'] and good['summary'] == {'passed': 115, 'failed': 0}
    assert good['section_counts'] == {'staged': 102, 'stage': 2, 'always_on': 13}
    assert good['runtime']['seconds'] == 238
    negatives = [fixture + fixture, fixture.replace('115 passed', '116 passed'),
                 fixture.replace('102 staged-section', '0 staged-section'),
                 fixture.replace('13 always-on', '12 always-on'),
                 fixture.replace('stages filtered to "2"', 'stages filtered to "1-2"'),
                 fixture.replace('SMOKE PASS', 'SMOKE FAIL'), fixture + '\nafter verdict\n',
                 fixture.replace('115 passed', '  FAIL  mobile 390x780: untimed failure\n115 passed'),
                 fixture.replace('115 passed', '  FAIL  [2:99] mobile 390x780: malformed time\n115 passed')]
    for key in GUARDS:
        line = good['required_guards'][key][0]['raw']
        negatives += [fixture.replace(line, ''), fixture.replace(line, line.replace('pass', 'FAIL', 1))]
    for marker in ['115 passed, 0 failed', '102 staged-section', '3 m 58 s for stage', 'SMOKE PASS']:
        negatives.append(fixture[:fixture.index(marker)])
    for text in negatives:
        assert not parse_log(text, 2, mirror, 0)['passed']
    for code in [None, 1, 124, 137, -15]:
        assert not parse_log(fixture, 2, mirror, code)['passed']
    assert not parse_log(fixture, 3, mirror, 0)['passed']
    assert not parse_log(fixture, 2, '/wrong/mirror', 0)['passed']
    assert not parse_log(fixture.replace('mobile', 'desktop'), 2, mirror, 0)['passed']
    # These are parser fixtures only; no browser process, config, cohort or evidence is created.
    print(json.dumps({'self_test': 'PASS', 'valid_real_log_fixture': 'b1 mobile2',
                      'negative_text_cases': len(negatives), 'negative_exit_cases': 5,
                      'browser_launched': False}), flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--config')
    parser.add_argument('--out')
    parser.add_argument('--execute', action='store_true', help='Launch only after root supplies final pins and explicit go')
    parser.add_argument('--resume', action='store_true', help='Continue only after durable passed stages; never retry an incomplete stage')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.execute or not args.config or not args.out:
        parser.error('Execution requires --execute --config FINAL.json --out NEW_COHORT_DIR')
    execute(load_config(args.config), args.out, args.resume)

if __name__ == '__main__':
    main()
