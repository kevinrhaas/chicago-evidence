from pathlib import Path
import fcntl, hashlib, importlib.util, json, os, shutil, subprocess, sys

ROOT = Path('/tmp/chicago-queue-refresh-20261109')
APP = ROOT / 'chicago/4d'
TASK = Path('/workspace/.cloud-setup/queue-refresh-20261109')
PROBE = TASK / 'human-cloth-browser-probe.mjs'
OUT = Path(sys.argv[1])
assert not OUT.exists()
assert hashlib.sha256(PROBE.read_bytes()).hexdigest() == '38477f7a4d0cd64767cc7a458508132146a8285db3c2bbfb888dcfeafb24ca5f'
lock = open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock', 'a+')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
spec = importlib.util.spec_from_file_location('guard', '/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0',
           PW_EXECUTABLE='/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell')
for key in ['GIT_NO_LAZY_FETCH', 'CHECK_PART', 'CHICAGO_TICKETS_DIR']:
    env.pop(key, None)
def save(path, value): path.write_text(json.dumps(value, indent=2)+'\n')
def git(*args): return subprocess.check_output(['git', '-C', str(ROOT), *args], env=env).decode().strip()
def source():
    assert not git('status', '--porcelain'), 'Committed source must remain clean'
    result = {'HEAD': git('rev-parse', 'HEAD'), 'TREE': git('rev-parse', 'HEAD^{tree}')}
    assert result == {'HEAD': 'a64f26fa2fc3e05dd39cd8e55df5384646786d7b', 'TREE': '0c2fe214e0c41f127282f82b04b3754279baf526'}
    return result
original = source(); initial = guard.snapshot(); assert guard.check(initial)['accepted']
OUT.mkdir(); scratch = OUT / 'owned-tmp'; scratch.mkdir(); env['TMPDIR'] = str(scratch)
state = {'status': 'RUNNING_NOT_PASS', 'source': original, 'scope': 'Actual HumanActor in controlled studio; no whole-town or photographic acceptance', 'cells': []}
save(OUT/'STATE.json', state)
cells = [('source','desktop',False), ('source','desktop',True), ('source','phone',False),
         ('published','desktop',False), ('published','phone',False), ('published','phone',True)]
try:
    for mode, viewport, baseline in cells:
        assert source() == original
        before = guard.snapshot(); assert guard.check(before)['accepted']
        name = mode+'-'+viewport+('-baseline' if baseline else '-current')
        command = ['node', str(PROBE), '--mode', mode, '--viewport', viewport, '--out', str(OUT/name)]
        if baseline: command.append('--baseline')
        prefix = OUT/(name+'-supervisor')
        result = subprocess.run([sys.executable, '/workspace/.cloud-setup/transport-supervise.py', '--prefix', str(prefix), '--cwd', str(APP), '--timeout', '600', '--', *command], env=env)
        receipt = json.loads(Path(str(prefix)+'.result.json').read_text())
        cleanup = json.loads(Path(str(prefix)+'.cleanup.json').read_text())
        resources = guard.pair(before, guard.snapshot())
        row = {'name': name, 'result': receipt, 'cleanup': cleanup, 'resources': resources, 'source_after': source()}
        state['cells'].append(row); save(OUT/'STATE.json', state)
        assert result.returncode == receipt['returncode'] == 0 and not receipt['timed_out']
        assert receipt['requested_timeout_seconds'] == receipt['effective_timeout_seconds'] == 600 and receipt['timeout_override_reason'] is None
        assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
        proof = json.loads((OUT/name/'receipt.json').read_text())
        assert not proof['errors'] and len(proof['records']) == 2 and len(proof['images']) == 4
        assert row['source_after'] == original
        print(json.dumps({'cell': name, 'passed': True, 'seconds': round(receipt['seconds'],3)}), flush=True)
    state['status'] = 'PASS_SIX_ACTUAL_LOADER_STUDIO_CELLS_NOT_PHOTOGRAPHIC_ACCEPTANCE'
except BaseException as error:
    state['status'] = 'NONPASS_NO_AUTOMATIC_RETRY'; state['error'] = repr(error)
finally:
    state['resources'] = guard.pair(initial, guard.snapshot())
    if not state['resources']['accepted']: state['status'] = 'NONPASS_RESOURCE_GUARD'
    if all(row['cleanup']['cleanup_complete'] for row in state['cells']): shutil.rmtree(scratch)
    state['owned_tmp_removed'] = not scratch.exists()
    save(OUT/'CLOSED.json', state); save(OUT/'STATE.json', state)
print(json.dumps({'status': state['status'], 'receipt': str(OUT/'CLOSED.json')}), flush=True)
sys.exit(0 if state['status'].startswith('PASS_') else 1)
