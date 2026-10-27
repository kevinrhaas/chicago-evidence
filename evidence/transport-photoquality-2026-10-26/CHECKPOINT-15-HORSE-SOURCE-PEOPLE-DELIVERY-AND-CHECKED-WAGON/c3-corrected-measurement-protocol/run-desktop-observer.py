#!/usr/bin/env python3
"""Launch only after root's heavy-slot GO with fresh reviewed bindings. No producer."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
OBSERVER = HERE / 'observe-desktop.mjs'
OBSERVER_SHA256 = '703311147daebbb2792f8ab069101ae2a05cf82917614ff456e2cc0c891e71dc'
SUPERVISOR = '/workspace/.cloud-setup/transport-supervise.py'

def digest(file):
    h = hashlib.sha256()
    with Path(file).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def safe_name(name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('Unsafe binding path: ' + str(name))
    return p.as_posix()

def write(file, value):
    Path(file).write_text(json.dumps(value, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['worker', 'source-binding', 'source-sha256', 'mirror-root', 'mirror-manifest',
                 'mirror-sha256', 'runtime-manifest', 'runtime-sha256', 'out', 'prefix', 'scratch']:
        parser.add_argument('--' + name, required=True)
    a = parser.parse_args()
    repo, mirror = Path(a.worker).resolve(), Path(a.mirror_root).resolve()
    out, prefix, scratch = Path(a.out).absolute(), Path(a.prefix).absolute(), Path(a.scratch).absolute()
    receipt = Path(str(prefix) + '.driver.json')
    if out.exists() or scratch.exists() or receipt.exists():
        raise ValueError('Output, TMPDIR and driver receipt must be fresh')
    for suffix in ['.log', '.result.json', '.cleanup.json', '.pause.json']:
        if Path(str(prefix) + suffix).exists():
            raise ValueError('Supervisor prefix must be fresh')
    if scratch.parent != Path('/workspace') or len(str(scratch)) > 30:
        raise ValueError('Mandatory short direct /workspace/<name> owned TMPDIR')
    if any(out == p or p in out.parents for p in [repo, mirror]):
        raise ValueError('Observer outputs must be outside source and mirror')
    if shutil.disk_usage('/tmp').free < (256 + 24) * 1048576:
        raise ValueError('Need256MiB /tmp reserve plus24MiB desktop observer output allowance')
    if digest(OBSERVER) != OBSERVER_SHA256:
        raise AssertionError('Frozen desktop-only observer changed')
    bindings = [(Path(a.source_binding).resolve(), a.source_sha256.lower()),
                (Path(a.mirror_manifest).resolve(), a.mirror_sha256.lower()),
                (Path(a.runtime_manifest).resolve(), a.runtime_sha256.lower())]
    for file, expected in bindings:
        if digest(file) != expected:
            raise AssertionError('Reviewed binding SHA mismatch: ' + str(file))
    source = json.loads(bindings[0][0].read_text())
    published = json.loads(bindings[1][0].read_text())
    if not source.get('paths') or not isinstance(published, list) or not published:
        raise ValueError('Nonempty source binding and complete mirror manifest required')
    for rows in [source['paths'], published]:
        names = [safe_name(row['path']) for row in rows]
        if len(set(names)) != len(names):
            raise ValueError('Duplicate binding paths')
    env = dict(os.environ)
    env.pop('GIT_NO_LAZY_FETCH', None)
    inspect_env = {**env, 'GIT_NO_LAZY_FETCH': '1', 'GIT_OPTIONAL_LOCKS': '0'}
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=repo, env=inspect_env)
    def verify_rows(root, rows):
        for row in rows:
            file = root / safe_name(row['path'])
            if row.get('absent'):
                if file.exists() or file.is_symlink():
                    raise AssertionError('Pinned absent path reappeared: ' + str(file))
            elif not file.is_file() or digest(file) != row['sha256'] or ('bytes' in row and file.stat().st_size != row['bytes']):
                raise AssertionError('Bound file mismatch: ' + str(file))
    def guard():
        for file, expected in bindings:
            if digest(file) != expected:
                raise AssertionError('Binding changed during observation')
        if git('rev-parse', 'HEAD').decode().strip() != source['HEAD']:
            raise AssertionError('Bound HEAD changed')
        # Compare the existing index to the bound tree without writing an index/tree.
        subprocess.run(['git', 'diff', '--cached', '--quiet', source['TREE'], '--'], cwd=repo,
                       env=inspect_env, check=True)
        if git('rev-parse', source['TREE'] + ':chicago/4d').decode().strip() != source['APP']:
            raise AssertionError('Bound APP does not match bound TREE')
        changed = {p.decode() for p in git('diff', '--name-only', '-z', 'HEAD', '--').split(b'\0') if p}
        names = {row['path'] for row in source['paths']}
        if not changed <= names:
            raise AssertionError('Unbound changed tracked paths: ' + repr(sorted(changed - names)))
        verify_rows(repo, source['paths'])
        if {p.relative_to(mirror).as_posix() for p in mirror.rglob('*') if p.is_file()} != {r['path'] for r in published}:
            raise AssertionError('Complete mirror file set changed')
        verify_rows(mirror, published)
        return {'HEAD': source['HEAD'], 'TREE': source['TREE'], 'APP': source['APP'],
                'source_paths': len(source['paths']), 'mirror_files': len(published),
                'binding_sha256': [expected for _, expected in bindings],
                'status_sha256': hashlib.sha256(git('status', '--porcelain=v1', '-z')).hexdigest(),
                'all_bound_files_exact': True}
    result = {'scope': 'Desktop only actual native lifecycle; no source edits, memory reading or broad/fullgate acceptance',
              'state': 'PREPARING', 'observer_sha256': OBSERVER_SHA256, 'browser_launch_attempted': False,
              'scratch': str(scratch), 'out': str(out), 'prefix': str(prefix)}
    start = time.monotonic()
    try:
        result['before'] = guard()
        scratch.mkdir(exist_ok=False)
        write(scratch / 'OWNED-BY-DESKTOP-OBSERVER.json', {'out': str(out), 'prefix': str(prefix)})
        env['TMPDIR'] = str(scratch)
        command = [sys.executable, SUPERVISOR, '--prefix', str(prefix), '--cwd', str(repo / 'chicago/4d'),
                   '--timeout', '1800', '--', 'node', str(OBSERVER), '--app-root', str(repo / 'chicago/4d'),
                   '--published-root', str(mirror), '--out', str(out), '--runtime-manifest', str(bindings[2][0])]
        result.update(command=command, state='RUNNING', browser_launch_attempted=True)
        write(receipt, result)
        native = subprocess.run(command, env=env)
        closed = json.loads(Path(str(prefix) + '.result.json').read_text())
        cleanup = json.loads(Path(str(prefix) + '.cleanup.json').read_text())
        result.update(supervisor_process_returncode=native.returncode, supervisor=closed, cleanup=cleanup)
        result['after'] = guard()
        result['before_after_exact'] = result['after'] == result['before']
        observer = json.loads((out / 'ACTUAL-RESULT.json').read_text()) if (out / 'ACTUAL-RESULT.json').exists() else None
        result['observer_status'] = observer.get('status') if observer else 'MISSING_OR_INCOMPLETE'
        result['observer_result_sha256'] = digest(out / 'ACTUAL-RESULT.json') if observer else None
        complete = (closed['returncode'] == 0 and not closed['timed_out'] and cleanup['cleanup_complete']
                    and not cleanup['remaining_owned_children'] and result['before_after_exact']
                    and observer and observer.get('status') == 'PASS' and len(observer['rows']) == 1
                    and observer['rows'][0].get('profile') == 'desktop')
        result['state'] = 'PASS' if complete else 'NONPASS'
        rc = 0 if complete else (closed['returncode'] or 70)
    except Exception as error:
        result.update(state='NONPASS', error=repr(error))
        try:
            result['after_error'] = guard()
        except Exception as guard_error:
            result['after_error_guard_failure'] = repr(guard_error)
        rc = 70 if result['browser_launch_attempted'] else 2
    result['seconds'] = time.monotonic() - start
    result['app_or_ticket_acceptance'] = False
    write(receipt, result)
    print(json.dumps(result))
    return rc

if __name__ == '__main__':
    raise SystemExit(main())
