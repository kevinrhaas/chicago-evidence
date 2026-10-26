#!/usr/bin/env python3
"""One native 1904 memory gate; run only after the parent grants its heavy slot.

Source binding: {HEAD,TREE,APP,paths:[{path,sha256,bytes?}]}.
Source paths may pin a deleted file with {path,absent:true}.
Mirror manifest: [{path,sha256,bytes?}], covering every published file.
Both input JSON files require their separately reviewed SHA256 arguments.
Use separate fresh out/prefix/short scratch paths for mobile and desktop.
Native spawn memory emits JSON, not PNG. Its PNG option belongs to walk captures;
this wrapper deliberately does not change the measurement route to obtain images.
"""
import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

SUPERVISOR = Path('/workspace/.cloud-setup/transport-supervise.py')
METRIC_PATHS = ['chicago/4d/tools/measure_memory.mjs', 'chicago/4d/tools/memory_ceilings.json']
OLD_DESKTOP_GOAL_BYTES = 1125 * 1024 * 1024

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')

def relative_name(name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('Unsafe manifest path: ' + str(name))
    return p.as_posix()

def read_native_reference(git, accepted_base=None):
    """Read immutable committed native bytes; omitted base retains HEAD behavior."""
    if accepted_base is not None and not re.fullmatch(r'[0-9a-fA-F]{40}', accepted_base):
        raise ValueError('Accepted base must be an immutable full 40-hex commit SHA')
    selected = accepted_base.lower() if accepted_base is not None else 'HEAD'
    commit = git('rev-parse', '--verify', selected + '^{commit}').decode().strip()
    if accepted_base is not None and commit != selected:
        raise AssertionError('Accepted base did not resolve to its exact commit')
    rows, payloads = {}, {}
    for name in METRIC_PATHS:
        data = git('show', commit + ':' + name)
        rows[name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                      'git_blob': git('rev-parse', commit + ':' + name).decode().strip()}
        payloads[name] = data
    caps = json.loads(payloads[METRIC_PATHS[1]])['ceilings']['1904']
    limits = {viewport: caps[viewport]['total_bytes'] for viewport in ['mobile', 'desktop']}
    if not all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in limits.values()):
        raise ValueError('Native committed 1904 ceilings must be positive integer bytes')
    record = {'mode': 'explicit_accepted_base' if accepted_base is not None else 'HEAD_default',
              'commit': commit, 'files': rows, 'native_1904_ceilings_bytes': limits}
    return record, payloads


def verify_native_reference(repo, git, reference, accepted_base=None):
    current_reference, payloads = read_native_reference(git, accepted_base)
    if current_reference != reference:
        raise AssertionError('Native committed reference changed')
    for name, row in reference['files'].items():
        if digest(Path(repo) / name) != row['sha256']:
            raise AssertionError('Native metric/ceiling differs from selected committed reference: ' + name)
    return {name: row['sha256'] for name, row in reference['files'].items()}


def historical_desktop_comparison(total_bytes):
    return {'scope': 'READ_ONLY_SUPPLEMENTAL_OLD_GOAL_NOT_NATIVE_GATE',
            'old_1125_mib_goal_bytes': OLD_DESKTOP_GOAL_BYTES,
            'actual_total_bytes': total_bytes,
            'actual_strictly_below_old_goal': total_bytes < OLD_DESKTOP_GOAL_BYTES,
            'remaining_bytes_to_old_goal': OLD_DESKTOP_GOAL_BYTES - total_bytes,
            'changes_native_gate_or_result': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', required=True)
    ap.add_argument('--accepted-base', help='Explicit immutable 40-hex commit for unchanged native metric/caps; omitted means HEAD as before')
    ap.add_argument('--source-binding', required=True)
    ap.add_argument('--expected-source-binding-sha256', required=True)
    ap.add_argument('--mirror-root', required=True)
    ap.add_argument('--mirror-manifest', required=True)
    ap.add_argument('--expected-mirror-manifest-sha256', required=True)
    ap.add_argument('--viewport', choices=['mobile', 'desktop'], required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--prefix', required=True)
    ap.add_argument('--scratch', required=True, help='Fresh short owned /workspace/<name> directory')
    ap.add_argument('--timeout', type=float, default=240)
    a = ap.parse_args()
    repo = Path(a.worker).resolve()
    mirror = Path(a.mirror_root).resolve()
    out = Path(a.out).absolute()
    prefix = Path(a.prefix).absolute()
    scratch = Path(a.scratch).absolute()
    if not (repo / '.git').exists() or not (repo / 'chicago/4d').is_dir():
        raise ValueError('Worker is not an existing Chicago checkout')
    if out.exists() or scratch.exists():
        raise ValueError('Output and scratch must both be fresh paths')
    if scratch.parent != Path('/workspace') or len(str(scratch)) > 30:
        raise ValueError('Use a short, direct child of /workspace for browser TMPDIR')
    if len(str(scratch / 'playwright_chromiumdev_profile-XXXXXX/SingletonSocket').encode()) >= 100:
        raise ValueError('Browser scratch risks Chromium Unix socket limit')
    if not 0 < a.timeout <= 1200:
        raise ValueError('Timeout must be positive and bounded at 1200s')
    for suffix in ['.log', '.result.json', '.cleanup.json', '.pause.json']:
        if Path(str(prefix) + suffix).exists():
            raise ValueError('Supervisor prefix already exists')
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    # This flag is solely for our inspections, never the native child.
    env.pop('GIT_NO_LAZY_FETCH', None)
    env.pop('CHICAGO_TICKETS_DIR', None)
    inspect_env = {**env, 'GIT_NO_LAZY_FETCH': '1', 'GIT_OPTIONAL_LOCKS': '0'}

    def git(*args):
        return subprocess.check_output(['git', *args], cwd=repo, env=inspect_env)

    source_path = Path(a.source_binding).resolve()
    mirror_path = Path(a.mirror_manifest).resolve()
    expected_source_hash = a.expected_source_binding_sha256.lower()
    expected_mirror_hash = a.expected_mirror_manifest_sha256.lower()
    if digest(source_path) != expected_source_hash or digest(mirror_path) != expected_mirror_hash:
        write(out / 'ACTUAL-RESULT.json', {'state': 'BINDING_INPUT_MISMATCH', 'browser_launched': False})
        return 2
    source = json.loads(source_path.read_text())
    published = json.loads(mirror_path.read_text())
    if not isinstance(published, list) or not published or not source.get('paths'):
        raise ValueError('Nonempty source paths and complete mirror manifest are required')
    source_names = [relative_name(row['path']) for row in source['paths']]
    mirror_names = [relative_name(row['path']) for row in published]
    if any(row.get('absent') for row in published):
        raise ValueError('Mirror manifest must list existing files only')
    if len(set(source_names)) != len(source_names) or len(set(mirror_names)) != len(mirror_names):
        raise ValueError('Duplicate manifest path')

    def verify_rows(root, rows):
        for row in rows:
            p = root / relative_name(row['path'])
            if row.get('absent'):
                if p.exists() or p.is_symlink():
                    raise AssertionError('Pinned deletion reappeared: ' + str(p))
                continue
            if not p.is_file() or digest(p) != row['sha256']:
                raise AssertionError('File hash mismatch: ' + str(p))
            if 'bytes' in row and p.stat().st_size != row['bytes']:
                raise AssertionError('File size mismatch: ' + str(p))

    def snapshot():
        if digest(source_path) != expected_source_hash or digest(mirror_path) != expected_mirror_hash:
            raise AssertionError('Binding JSON changed')
        head = git('rev-parse', 'HEAD').decode().strip()
        tree = git('write-tree').decode().strip()
        app = git('rev-parse', tree + ':chicago/4d').decode().strip()
        if (head, tree, app) != (source['HEAD'], source['TREE'], source['APP']):
            raise AssertionError('Pinned HEAD/index TREE/APP mismatch')
        # Any authored/derived working change must be explicitly pinned, including
        # staged merge outputs; source binding can also name committed files.
        changed = {x.decode() for x in git('diff', '--name-only', '-z', 'HEAD', '--').split(b'\0') if x}
        if not changed <= set(source_names):
            raise AssertionError('Changed tracked paths absent from binding: ' + repr(sorted(changed - set(source_names))))
        verify_rows(repo, source['paths'])
        actual = {p.relative_to(mirror).as_posix() for p in mirror.rglob('*') if p.is_file()}
        if actual != set(mirror_names):
            raise AssertionError('Published mirror file set changed')
        verify_rows(mirror, published)
        metric = verify_native_reference(repo, git, native_reference, a.accepted_base)
        if digest(reference_file) != reference_sha256:
            raise AssertionError('Saved native reference receipt changed')
        for name, row in native_reference['files'].items():
            if digest(reference_root / name) != row['sha256']:
                raise AssertionError('Saved immutable native reference bytes changed: ' + name)
        status = git('status', '--porcelain=v1', '-z')
        return {'HEAD': head, 'TREE': tree, 'APP': app,
                'git_status_sha256': hashlib.sha256(status).hexdigest(),
                'source_binding_sha256': expected_source_hash, 'pinned_source_paths': len(source_names),
                'mirror_manifest_sha256': expected_mirror_hash, 'mirror_files': len(mirror_names),
                'mirror_root': str(mirror), 'build': json.loads((mirror / 'build.json').read_text()),
                'native_metric_and_ceiling_sha256': metric, 'native_reference': native_reference,
                'native_reference_receipt_sha256': reference_sha256, 'source_and_mirror_exact': True}

    command = ['node', 'tools/measure_memory.mjs', '--gate', '--no-snapshot', '--year', '1904',
               '--only', a.viewport, '--root', str(mirror), '--json', str(out / 'READING.json')]
    launch = [sys.executable, str(SUPERVISOR), '--prefix', str(prefix), '--cwd', str(repo / 'chicago/4d'),
              '--timeout', str(a.timeout), '--', *command]
    start = time.monotonic()
    result = {'scope': 'Native pinned published 1904 memory gate, one viewport; no metric edits or heap snapshots',
              'viewport': a.viewport, 'native_command': command, 'supervisor_command': launch,
              'scratch': str(scratch), 'out': str(out), 'prefix': str(prefix),
              'browser_launch_attempted': False, 'state': 'PREPARING',
              'native_spawn_png_support': False, 'PNG_note': 'Native PNGs require a different --walk --captures route; none requested.'}
    try:
        native_reference, native_payloads = read_native_reference(git, a.accepted_base)
        reference_root = out / 'IMMUTABLE-NATIVE-REFERENCE'
        reference_root.mkdir(exist_ok=False)
        for name, data in native_payloads.items():
            saved = reference_root / name
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_bytes(data)
        reference_file = out / 'NATIVE-REFERENCE.json'
        write(reference_file, native_reference)
        reference_sha256 = digest(reference_file)
        result['native_reference'] = native_reference
        result['native_reference_receipt_sha256'] = reference_sha256
        before = snapshot()
        write(out / 'BEFORE.json', before)
        scratch.mkdir(exist_ok=False)
        write(scratch / 'OWNED-BY-MEMORY-RUN.json', {'out': str(out), 'prefix': str(prefix),
                                                  'created_utc': datetime.now(timezone.utc).isoformat()})
        env['TMPDIR'] = str(scratch)
        write(out / 'COMMAND.json', {**result, 'TMPDIR': str(scratch),
                                    'PW_EXECUTABLE': env.get('PW_EXECUTABLE'),
                                    'normal_TLS_and_native_browser_flags': True})
        result['browser_launch_attempted'] = True
        native = subprocess.run(launch, cwd=repo / 'chicago/4d', env=env, capture_output=True, text=True)
        (out / 'SUPERVISOR.stdout').write_text(native.stdout)
        (out / 'SUPERVISOR.stderr').write_text(native.stderr)
        result['supervisor_process_returncode'] = native.returncode
        closed = json.loads(Path(str(prefix) + '.result.json').read_text())
        cleanup = json.loads(Path(str(prefix) + '.cleanup.json').read_text())
        write(out / 'NATIVE-SUPERVISOR-RESULT.json', closed)
        write(out / 'NATIVE-CLEANUP.json', cleanup)
        result.update(native_returncode=closed['returncode'], native_seconds=closed['seconds'],
                      timed_out=closed['timed_out'], cleanup_complete=cleanup['cleanup_complete'],
                      remaining_owned_children=cleanup['remaining_owned_children'])
        after = snapshot()
        write(out / 'AFTER.json', after)
        result['before_after_exact'] = after == before
        reading = json.loads((out / 'READING.json').read_text()) if (out / 'READING.json').is_file() else None
        rows = reading.get('rows', []) if reading else []
        result['reading_written'] = reading is not None
        result['valid_single_1904_viewport_reading'] = (len(rows) == 1 and rows[0].get('year') == '1904'
                                                       and rows[0].get('viewport') == a.viewport
                                                       and isinstance(rows[0].get('totals', {}).get('total'), (int, float))
                                                       and not isinstance(rows[0]['totals']['total'], bool)
                                                       and math.isfinite(rows[0]['totals']['total'])
                                                       and rows[0]['totals']['total'] >= 0)
        if result['valid_single_1904_viewport_reading']:
            result['actual_totals_bytes'] = rows[0]['totals']
            result['actual_page_errors'] = rows[0].get('errors', [])
            result['actual_native_ceiling_bytes'] = native_reference['native_1904_ceilings_bytes'][a.viewport]
            if a.viewport == 'desktop':
                result['historical_1125_mib_comparison'] = historical_desktop_comparison(rows[0]['totals']['total'])
        intact = result['before_after_exact'] and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
        complete = intact and not closed['timed_out'] and result['valid_single_1904_viewport_reading']
        result['state'] = 'PASS' if complete and closed['returncode'] == 0 else 'NONPASS'
        result['app_or_ticket_acceptance'] = False
        rc = closed['returncode'] if complete else 70
    except Exception as error:
        result.update(state='NONPASS', error=repr(error), app_or_ticket_acceptance=False)
        try:
            write(out / 'AFTER-ERROR.json', snapshot())
        except Exception as after_error:
            result['after_snapshot_error'] = repr(after_error)
        rc = 70 if result['browser_launch_attempted'] else 2
    result['wrapper_seconds'] = time.monotonic() - start
    write(out / 'ACTUAL-RESULT.json', result)
    print(json.dumps(result))
    return rc

if __name__ == '__main__':
    raise SystemExit(main())
