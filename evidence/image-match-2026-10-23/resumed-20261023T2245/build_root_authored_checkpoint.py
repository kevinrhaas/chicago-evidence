from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/log82-authored-checkpoint-20261023T2324')
MANIFEST = ROOT / 'MANIFEST.json'
EXPECTED = 'b9ad8b12f72c054d056ef3be19d5d273a9281cc1bbb585c322f2b2f2b60f818b'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
author = json.loads(MANIFEST.read_text())
assert len(author['files']) == 20 and author['status'] == 'closed authored-only recovery checkpoint'
for row in author['files']:
    path = ROOT / row['path']
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], path
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'T3081-root-authored-only-UNCOMMITTED-UNBAKED', mod.author_manifest(ROOT, MANIFEST),
    'Root T3081 authored-only recovery: exact20 selected files plus originalmanifest, base5f15,18authored files plus patch/README. UNCOMMITTED and UNBAKED at snapshot; native consumers/fullgates pending, PR1239V2 dependency before population writers. Changelog kind validated but no shipping/readiness claim. Not a liveworktree grab, official82 bake, browser proof, accepted image match or code PR.'
)
