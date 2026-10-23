from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
MANIFEST = Path('/tmp/chicago-next-model/T-2385-resume-light-20261023T2245/ACTUAL-CLOSED-MANIFEST.json')
EXPECTED = 'e61759cc60e1fb2eb7d055b241e4ffd17f9fd15c100a4122173c2e5e07024c5e'
sha = lambda b: hashlib.sha256(b).hexdigest()
assert sha(MANIFEST.read_bytes()) == EXPECTED
author = json.loads(MANIFEST.read_text())
assert len(author['files']) == 18 and author['file_count'] == 18
entries = []
for row in author['files']:
    path = Path(row['path'])
    dst = Path(row['archive_path'])
    assert path.is_absolute() and path.resolve().is_relative_to(Path('/tmp/chicago-next-model'))
    assert path.is_file() and not path.is_symlink()
    assert not dst.is_absolute() and '..' not in dst.parts
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    assert path.suffix != '.pyc'
    data = path.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], path
    assert path.read_bytes() == data
    entries.append((path, row['archive_path'], row['sha256']))
entries.append((MANIFEST, 'AUTHOR-ACTUAL-CLOSED-MANIFEST.json', EXPECTED))
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'TREMONT-three-ACTUAL-roof-GPU-trials-DIFFERS', entries,
    'Tremont T2385: three actual roof-only linearRGB factors0.5/0.25/0.125 completed with fixed source master/camera/native flag/wind/time/grade/light/exposure and actual GPU/readback guards. All images reviewed DIFFERS; factor0.25 preferred as bounded next candidate UNADOPTED. Exact18 closed files plus originalmanifest; shared328 native inputs remain in prior frozen archive. No canonical edit, historical pigment claim or image-match acceptance.'
)
print('TREMONT ARCHIVE CLOSED:18author files+manifest, all hashes/double-read/fulltarreadback PASS.')
