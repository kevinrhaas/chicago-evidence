from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/T3081-Wolf-lodging-readonly-risk')
MANIFEST = ROOT / 'MANIFEST.json'
EXPECTED = '83c9f511b2735bd8aed917b22b47211072377f848ab0a0bd1f7853248f626e1a'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
author = json.loads(MANIFEST.read_text())
assert author['status'] == 'CLOSED_IMMUTABLE_READONLY_STUDY' and len(author['files']) == 19
for row in author['files']:
    path = ROOT / row['path']
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    assert path.suffix != '.pyc'
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256']
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'WOLF-lodging-purefill-risk-and-PR1239-hosted1060-proof', mod.author_manifest(ROOT, MANIFEST),
    'Closed readonly risk/CI study:19 exact files plus manifest. Actual native purefills show olddev WolfL allocation churn (13retired/12new/2movedpeople/5movedseats), V2 preserves22households/157people/52seats/counters on tested inputs. Write-denial,24canonicalinput doublehash and unchanged book6c5e9e proof retained; no native writer, browser or new gate launched. Also actuala219 hosted1060PASS rawjoblog and merge20455(a219+dev5f15) binding, owner completed23:01:42. Root owns dependency/lap/merge; no approval for another target or original image match.'
)
