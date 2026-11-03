"""Prepared only: unchanged full native human fixture, both viewports/all24 GLBs."""
from pathlib import Path
import fcntl, hashlib, importlib.util, json, os, subprocess, sys

D = Path(__file__).resolve().parent
R = Path('/workspace/chicago-driver-motion-20261103')
APP = R/'chicago/4d'
OUT = D/sys.argv[1]
OUT.mkdir(exist_ok=False)
lock = open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock', 'a+')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
spec = importlib.util.spec_from_file_location('guard', '/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
sha = lambda raw: hashlib.sha256(raw).hexdigest()
def save(name, value): (OUT/name).write_text(json.dumps(value, indent=2)+'\n')
def git(*args): return subprocess.check_output(['git', '-C', str(R), *args], timeout=20)
files = sorted(str(p.relative_to(APP)) for folder in ['assets/humans', 'assets/humans/web'] for p in (APP/folder).glob('*.glb'))
assert len(files) == 24
recipe = json.loads((APP/'data/humans/animations/seated-driver-look-v2.json').read_text())
native = json.loads((D/'native-02/models/RESULT.json').read_text())
assert native['passed'] and len(recipe['parents']) == 8
for row in recipe['parents']:
    assert sha((APP/row['file']).read_bytes()) == native['candidate_sha256_before'][row['file']]
critical = ['tools/human_fixture.mjs', 'tools/human_fixture.html', 'data/humans/contract.json',
            'renderers/web/js/scene-loader.js', 'renderers/web/vendor/three-0.185.1/three.module.js',
            'renderers/web/vendor/three-0.185.1/three.core.js',
            'renderers/web/vendor/three-0.185.1/addons/loaders/GLTFLoader.js',
            'renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js']
changed = git('diff', '--name-only', 'HEAD').decode().splitlines()
new = git('ls-files', '--others', '--exclude-standard').decode().splitlines()
paths = set(files + critical + [str(Path(p).relative_to('chicago/4d')) for p in changed + new if p.startswith('chicago/4d/')])
paths.discard('data/humans/fixture.measure.json')
def pins(): return {p: sha((APP/p).read_bytes()) for p in sorted(paths)}
before = pins()
index = sha(git('ls-files', '--stage', '-z'))
browser = '/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell'
assert subprocess.check_output([browser, '--version'], timeout=5).decode().strip() == 'Chromium 141.0.7390.37'
save('SOURCE-BEFORE.json', dict(head=git('rev-parse', 'HEAD').decode().strip(), pins=before, semantic_index_sha256=index, files=files))
save('MEASURE-BEFORE.json', json.loads((APP/'data/humans/fixture.measure.json').read_text()))
env = dict(os.environ, PW_EXECUTABLE=browser, PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103')
env.pop('CHICAGO_TICKETS_DIR', None)
ledger = []
error = None
try:
    for label, command, cap in [('write-full-native-fixture', ['node', 'tools/human_fixture.mjs', '--write'], 600),
                                ('check-current-fixture-hashes', ['node', 'tools/human_fixture.mjs', '--check'], 120)]:
        assert pins() == before and sha(git('ls-files', '--stage', '-z')) == index
        resources_before = g.snapshot(); assert g.check(resources_before)['accepted']
        prefix = OUT/label
        q = subprocess.run([sys.executable, '/workspace/.cloud-setup/transport-supervise.py', '--prefix', str(prefix), '--cwd', str(APP), '--timeout', str(cap), '--', *command], env=env, stdout=(OUT/(label+'.stdout')).open('xb'), stderr=subprocess.STDOUT)
        result = json.loads(Path(str(prefix)+'.result.json').read_text())
        cleanup = json.loads(Path(str(prefix)+'.cleanup.json').read_text())
        resources = g.pair(resources_before, g.snapshot())
        row = dict(label=label, result=result, cleanup=cleanup, resources=resources)
        ledger.append(row); save('LEDGER.json', ledger)
        assert q.returncode == result['returncode'] == 0 and not result['timed_out']
        assert result['effective_timeout_seconds'] == result['requested_timeout_seconds'] == cap
        assert result['timeout_override_reason'] is None and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
        assert pins() == before and sha(git('ls-files', '--stage', '-z')) == index
    measure = json.loads((APP/'data/humans/fixture.measure.json').read_text())
    assert len(measure['files']) == 24
    assert {row['file'] for row in measure['files']} == set(files)
    assert measure['viewports'] == dict(desktop=dict(width=1280,height=800),mobile=dict(width=390,height=780))
    for row in measure['files']:
        assert row['sha256'] == sha((APP/row['file']).read_bytes()) and all(v['ok'] for v in row['verdicts'])
        if row['file'] in {p['file'] for p in recipe['parents']}:
            assert 'sit_drive_look_v2' in row['clips'] and row['clips']['sit_drive_look_v2']['duration_s'] == 8
    save('ACTUAL-MEASURE.json', measure)
except BaseException as exception:
    error = repr(exception)
after = pins()
save('CLOSED.json', dict(passed=error is None and len(ledger)==2, ledger=ledger, error=error,
                       source_pins_before=before, source_pins_after=after,
                       same_source_except_native_measure=before==after,
                       actual_native_600s_cap=True, original_per_viewport_readiness_seconds=120,
                       no_selective_or_unsupported_flags=True, no_scene_photo_or_full_gate_claim=True))
print(json.dumps(dict(passed=error is None, output=str(OUT), error=error)))
raise SystemExit(0 if error is None else 1)
