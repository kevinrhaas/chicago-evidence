from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/chicago-next-model/T-2385-deep-roof-proposal-20261023T2250')
MANIFEST = ROOT / 'CLOSED-MANIFEST.json'
EXPECTED = '8c7c13d449ef1011d8cb3228ad411e2402ed1cbe13bdba8df3aa042cf4759acc'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
author = json.loads(MANIFEST.read_text())
assert len(author['files']) == 14 and author['base_working_commit'] == '792598d88056dbc768bb5062258a803c6a62524b'
entries = []
for row in author['files']:
    path, dst = Path(row['path']), Path(row['archive_path'])
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    assert not dst.is_absolute() and '..' not in dst.parts
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    assert path.suffix != '.pyc'
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256']
    entries.append((path, str(dst), row['sha256']))
entries.append((MANIFEST, 'AUTHOR-CLOSED-MANIFEST.json', EXPECTED))
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'TREMONT-quarter-roof-stock-UNAPPLIED-producer-proposal', entries,
    'Tremont T2385: exact14 closed proposal files plus manifest; four guarded existing-file proposals, patch/liberty/readme/16CPU and24phase raw-parity/schema proof. Geometry/confidence/nonroof API preserved; only target roof stock linearRGBx0.25 intended. UNAPPLIED: official23-family rebake/fullgates/native adoption not run. Recover from recorded792 base plus guarded patch; execution-support trees intentionally excluded. Not another actual capture or historical pigment claim; original image still differs.'
)
