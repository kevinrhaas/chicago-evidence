from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/chicago-next-model/T-2385-flag-pose-next-20261023T2255')
MANIFEST = ROOT / 'CLOSED-MANIFEST.json'
EXPECTED = '2c1e64b3183ce5770a2dc807546a791b77dce093211ab82ab66906ee6907490b'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
author = json.loads(MANIFEST.read_text())
assert len(author['files']) == 351 and author['total_bytes'] == 34039131
entries = []
for row in author['files']:
    path, dst = Path(row['path']), Path(row['archive_path'])
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    assert not dst.is_absolute() and '..' not in dst.parts
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    assert path.suffix != '.pyc'
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], path
    entries.append((path, str(dst), row['sha256']))
entries.append((MANIFEST, 'AUTHOR-CLOSED-MANIFEST.json', EXPECTED))
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'TREMONT-one-ACTUAL-pictorial-flag-pose-DIFFERS-with-preserved-failure', entries,
    'Tremont T2385: exact351 closed input/actual/review files plus manifest. One successful native/GPU pose capture after preserved initialsignedzero harnessfailure and explicitly granted numeric-only normalization retry; both original and corrected runners/inputs/failure retained. GlobalWIND_FROM225 remains unchanged; singleflag pictorialTO105.6 override and quarterroof held, all other guards/readbacks pass. Direct source/native image review DIFFERS, unadopted; no historical wind/rights/PD claim or canonical/production/test assertion edit.'
)
