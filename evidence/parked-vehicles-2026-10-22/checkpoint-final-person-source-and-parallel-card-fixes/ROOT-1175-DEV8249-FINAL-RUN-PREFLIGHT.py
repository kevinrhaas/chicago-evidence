"""HELD until root releases the full-gate lane; no outer timeout or automatic retry."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, subprocess, sys

app = Path('/workspace/chicago/chicago/4d')
out = Path('/workspace/shared/ROOT-1175-DEV8249-FINAL-FULL-PREFLIGHT-20261022')
expected_tree = 'fc2a6cbc3870119a159d410ab273f8665e8e5c4f'
expected_head = 'fe9832a14921d385d1d53463403bdf3f39bc3f2b'
expected_merge = '824957fe47dd70fad729c3b117cb18b695d54b0b'
expected_branch = 'steward/1835-workwear-repair-20261021'
resolution = Path('/workspace/shared/ROOT-1175-DEV8249-FINAL-RESOLVED-TREE.json')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=app, text=True).strip()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-released', required=True, action='store_true')
    parser.parse_args()
    assert not out.exists(), 'One fresh execution only; preserve earlier failures'
    assert git('rev-parse', 'HEAD') == expected_head
    assert git('rev-parse', 'MERGE_HEAD') == expected_merge
    assert git('branch', '--show-current') == expected_branch
    assert git('write-tree') == expected_tree
    assert not git('diff', '--name-only')
    assert not git('diff', '--name-only', '--diff-filter=U')
    solved = json.loads(resolution.read_text())
    assert solved['head'] == expected_head and solved['merge_head'] == expected_merge
    assert solved['staged_tree'] == expected_tree and solved['resolver_exit'] == 0
    assert solved['last_lap_no_change'] and solved['unmerged_paths'] == solved['unstaged_paths'] == 0
    env = os.environ.copy()
    env.update({'PATH': '/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin:/workspace/shared/chicago-tools/usr/bin:' + env['PATH'],
                'CHECK_JOBS': '4', 'C4D_GATE_REQUIRE_READERS': '1',
                'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
    out.mkdir(exist_ok=False)
    record = {'started_utc': utc(), 'owner_pid': os.getpid(), 'head': expected_head,
              'merge_head': expected_merge, 'branch': expected_branch,
              'staged_tree_before': expected_tree, 'command': ['bash', 'tools/preflight.sh'],
              'check_jobs': 4, 'require_readers': True, 'math_threads': 1,
              'introduced_outer_timeout': False, 'automatic_retry': False,
              'resolution_receipt_sha256': hashlib.sha256(resolution.read_bytes()).hexdigest()}
    (out / 'START.json').write_text(json.dumps(record, indent=2) + '\n')
    with (out / 'FULL-PREFLIGHT.log').open('wb') as log:
        child = subprocess.Popen(['bash', 'tools/preflight.sh'], cwd=app, env=env,
                                 stdout=log, stderr=subprocess.STDOUT)
        record['repository_pid'] = child.pid
        (out / 'START.json').write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({'started': str(out), 'owner_pid': os.getpid(),
                          'repository_pid': child.pid, 'started_utc': record['started_utc']}), flush=True)
        rc = child.wait()
    # Capture global tool logs immediately, before any other gate can replace them.
    copies = []
    for name in ['preflight-check.log', 'preflight-cl.log', 'preflight-ids.log']:
        source = Path('/tmp') / name
        if source.is_file():
            shutil.copy2(source, out / name)
            copies.append({'name': name, 'bytes': (out / name).stat().st_size,
                           'sha256': hashlib.sha256((out / name).read_bytes()).hexdigest()})
    record.update({'finished_utc': utc(), 'preflight_exit': rc, 'global_log_copies': copies,
                   'staged_tree_after': git('write-tree'), 'head_after': git('rev-parse', 'HEAD'),
                   'merge_head_after': git('rev-parse', 'MERGE_HEAD'),
                   'unstaged_paths_after': git('diff', '--name-only').splitlines(),
                   'unmerged_paths_after': git('diff', '--name-only', '--diff-filter=U').splitlines()})
    record['exact_tree_unchanged'] = (record['staged_tree_after'] == expected_tree
        and record['head_after'] == expected_head and record['merge_head_after'] == expected_merge
        and not record['unstaged_paths_after'] and not record['unmerged_paths_after'])
    (out / 'EXIT.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2), flush=True)
    return rc if rc else (0 if record['exact_tree_unchanged'] else 3)

if __name__ == '__main__':
    sys.exit(main())
