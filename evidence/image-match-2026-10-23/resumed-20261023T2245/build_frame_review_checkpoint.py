from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/frame1239-resumed-readonly-20261023/closed-review')
MANIFEST = ROOT / 'MANIFEST.json'
EXPECTED = 'b7f17d99f1fcaad9298a0c28f289818b13e7c7dc54512edf1394652437fb6f7c'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
data = json.loads(MANIFEST.read_text())
assert len(data['files']) == 11
for row in data['files']:
    path = ROOT / row['path']
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256']
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'PR1239-resumed-readonly-integrity-NO-APPROVAL', mod.author_manifest(ROOT, MANIFEST),
    'Closed read-only PR1239 audit of a219:87 guarded originalframe/source/lodging paths unchanged, original rights174 entries preserved, Photosfixture acquisition fix leaves assertions unchanged. Documented source-index budget extension measured separately. LatestCI and liveowner pending at author snapshot; not merge/browser/image acceptance.'
)
