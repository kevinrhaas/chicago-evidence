"""Run original driver checks, full human writer and genuine report owners."""
from pathlib import Path
import argparse, fcntl, hashlib, importlib.util, json, os, subprocess, sys

D = Path(__file__).resolve().parent
R = Path('/workspace/chicago-transport-current-20261103')
A = R / 'chicago/4d'
SUP = Path('/workspace/.cloud-setup/transport-supervise.py')

def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')

def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args], timeout=30)

def source():
    tree = git('write-tree').decode().strip()
    return dict(HEAD=git('rev-parse', 'HEAD').decode().strip(), TREE=tree,
                APP=git('rev-parse', tree + ':chicago/4d').decode().strip(),
                semantic_index_sha256=hashlib.sha256(git('ls-files', '--stage', '-z')).hexdigest())

def clean_worktree():
    assert not git('diff', '--name-only').strip(), 'Unexpected unstaged tracked changes'
    assert not git('ls-files', '--others', '--exclude-standard').strip(), 'Unexpected untracked source'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    assert not a.out.exists()
    assert git('symbolic-ref', '--short', 'HEAD').decode().strip() == 'steward/t2804-independent-driver-looking-20261104'
    assert git('rev-parse', 'HEAD').decode().strip() == 'a3a87cafe9321a2970a390cac77ae45be82680f5'
    clean_worktree()
    lock = open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock', 'a+')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert hashlib.sha256(SUP.read_bytes()).hexdigest() == 'a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
    spec = importlib.util.spec_from_file_location('driver_v6_guard', D / 'resource_guard.py')
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    initial = source()
    rb = guard.snapshot()
    assert guard.check(rb)['accepted']
    a.out.mkdir()
    save(a.out / 'SOURCE-BEFORE.json', initial)
    steps = [
        ('seated-reproduction', ['python3', 'tools/human_seated_look.py', '--check'], 5, []),
        ('standing-reproduction', ['python3', 'tools/human_natural_idle.py', '--check'], 5, []),
        ('protected-standing', ['python3', 'tools/test_human_natural_idle.py'], 5, []),
        ('driver-clock', ['node', 'tools/test_driven_assembly.mjs'], 5, []),
        ('human-contract', ['python3', 'tools/human_contract.py', '--check'], 5, []),
        ('main-syntax', ['node', '--check', 'renderers/web/js/main.js'], 5, []),
        ('human-fixture-write', ['node', 'tools/human_fixture.mjs', '--write'], 600,
         ['chicago/4d/data/humans/fixture.measure.json']),
        ('human-fixture-check', ['node', 'tools/human_fixture.mjs', '--check'], 120, []),
        ('liberties-owner', ['python3', 'tools/compile_liberties.py'], 120,
         ['chicago/4d/data/liberties.json']),
        ('source-use-owner', ['python3', 'tools/compile_source_use.py'], 120,
         ['chicago/4d/docs/measurements/source_use_coverage.md']),
        ('liberties-check', ['python3', 'tools/compile_liberties.py', '--check'], 120, []),
        ('source-use-check', ['python3', 'tools/compile_source_use.py', '--check'], 120, []),
        ('human-contract-after-fixture', ['python3', 'tools/human_contract.py', '--check'], 5, []),
    ]
    save(a.out / 'PLAN.json', dict(steps=steps, full_gate=False, all_24_human_GLBS=True,
         native_viewports=[[1280, 800], [390, 780]], original_caps=True))
    ledger = []
    error = None
    try:
        for name, command, cap, writes in steps:
            clean_worktree()
            before = source()
            sb = guard.snapshot()
            assert guard.check(sb)['accepted']
            save(a.out / 'ACTIVE.json', dict(label=name, command=command, cap=cap))
            prefix = a.out / name
            with (a.out / (name + '-owner.stdout')).open('xb') as out:
                q = subprocess.run([sys.executable, str(SUP), '--prefix', str(prefix),
                    '--cwd', str(A), '--timeout', str(cap), '--', *command],
                    stdout=out, stderr=subprocess.STDOUT,
                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                        PW_EXECUTABLE='/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell'))
            result = json.loads(Path(str(prefix) + '.result.json').read_text())
            cleanup = json.loads(Path(str(prefix) + '.cleanup.json').read_text())
            resources = guard.pair(sb, guard.snapshot())
            changed = git('diff', '--name-only').decode().splitlines()
            unknown = git('ls-files', '--others', '--exclude-standard').decode().splitlines()
            row = dict(label=name, result=result, cleanup=cleanup, resources=resources,
                       source_before=before, changed_paths=changed, unexpected_untracked=unknown,
                       log=str(prefix) + '.log',
                       log_sha256=hashlib.sha256(Path(str(prefix) + '.log').read_bytes()).hexdigest())
            ledger.append(row)
            save(a.out / 'LEDGER.json', ledger)
            assert q.returncode == result['returncode'] == 0 and not result['timed_out'], name
            assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == cap
            assert result['timeout_override_reason'] is None
            assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
            assert not unknown and set(changed) <= set(writes), (name, changed, unknown)
            assert source() == before, 'Command changed the staged source'
            if changed:
                subprocess.run(['git', '-C', str(R), 'add', '--', *changed], check=True, timeout=30)
            clean_worktree()
            row['source_after'] = source()
            row['genuine_owner_outputs_staged'] = changed
            save(a.out / 'LEDGER.json', ledger)
    except BaseException as ex:
        error = repr(ex)
    final = source()
    resources = guard.pair(rb, guard.snapshot())
    passed = error is None and len(ledger) == len(steps) and resources['accepted']
    save(a.out / 'CLOSED.json', dict(status='ACTUAL_DRIVER_V6_NATIVE_24_GLB_FIXTURE_AND_OWNERS_PASS_NOT_FULL_GATE' if passed else
        'ACTUAL_DRIVER_V6_QUALIFICATION_NONPASS', source_before=initial, source_after=final,
        ledger=ledger, resources=resources, error=error, full_native_gate=False,
        rendered_new_look_fixture_or_full_world_acceptance=False, committed_or_pushed=False))
    print(json.dumps(dict(passed=passed, error=error, receipt=str(a.out / 'CLOSED.json'))), flush=True)
    raise SystemExit(0 if passed else 1)

if __name__ == '__main__':
    main()
