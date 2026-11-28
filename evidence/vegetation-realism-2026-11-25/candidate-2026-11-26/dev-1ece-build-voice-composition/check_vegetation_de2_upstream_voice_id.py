"""Run the unchanged narration regression with one exact upstream build input."""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

W = Path('/workspace/work')
R = W/'better-trees-seasons-current'
A = R/'chicago/4d'
P = 'chicago/4d/data/narration/voices.json'
BASE = '976557fd7511aadb2b1dc3e9815ff9a88b295f92'
UP = '1ece2a1fd8c238b54e3b0cbbdf97fc64570dda51'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
old = git('show', BASE+':'+P)
new = git('show', UP+':'+P)
assert git('diff', '--name-only', BASE, UP).decode().splitlines() == [P]
assert old.count(b'"street:young_lady": "EXAVITQu4vr4xnSz7DtE"') == 1
assert old.replace(b'"street:young_lady": "EXAVITQu4vr4xnSz7DtE"',
                   b'"street:young_lady": "EXAVITQu4vr4xnSDxMaL"') == new
refs = {k: git('rev-parse', k) for k in ('HEAD', 'origin/dev')}
proof = json.loads((W/'vegetation-dev-de2-final-integration-proof.json').read_text())
assert refs['HEAD'].decode().strip() == proof['final_head']
assert not git('status', '--porcelain')
for path, h in proof['source_sha256'].items():
    assert sha(R/path) == h
dest = W/'vegetation-de2-voice-id-native-source'
assert not dest.exists()
shutil.copytree(A, dest, copy_function=os.link, symlinks=True,
               ignore=shutil.ignore_patterns('tickets', '__pycache__', 'node_modules', '.venv'))
voice = dest/'data/narration/voices.json'
private = voice.with_suffix('.private')
private.write_bytes(new)
private.replace(voice)
assert (A/'data/narration/voices.json').read_bytes() == old
assert not any((R/'site/4d'/x).exists() for x in
               ('data/narration/voices.json', 'data/voices.json', 'voices.json'))
log = W/'vegetation-dev-de2-upstream-voice-id-native.log'
env = {**os.environ, 'PATH': str(W/'node22/bin')+':'+os.environ['PATH'],
       'TMPDIR': str(W)}
env.pop('CHICAGO_TICKETS_DIR', None)
with log.open('w') as out:
    run = subprocess.run(['node', 'tools/test_narration.mjs'], cwd=dest, env=env,
                         stdout=out, stderr=subprocess.STDOUT, timeout=180)
assert run.returncode == 0
assert refs == {k: git('rev-parse', k) for k in refs}
assert not git('status', '--porcelain')
for path, h in proof['source_sha256'].items():
    assert sha(R/path) == h
assert (A/'data/narration/voices.json').read_bytes() == old
out = {'complete': True, 'base': BASE, 'upstream_voice_fix': UP,
       'head': proof['final_head'], 'path': P,
       'before_sha256': hashlib.sha256(old).hexdigest(),
       'after_sha256': hashlib.sha256(new).hexdigest(),
       'unchanged_test': 'tools/test_narration.mjs',
       'unchanged_test_sha256': sha(dest/'tools/test_narration.mjs'),
       'exit_code': 0, 'log': str(log), 'log_sha256': sha(log),
       'qualified_source_and_refs_unchanged': True,
       'runtime_renderers_assets_and_audio_files_unchanged': True,
       'build_voice_config_not_in_published_mirror': True,
       'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(W/'vegetation-dev-de2-upstream-voice-id-native.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out))
