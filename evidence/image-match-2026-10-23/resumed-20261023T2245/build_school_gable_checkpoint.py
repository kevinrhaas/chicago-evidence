from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/chicago-next-model/T-2372-front-gable-next-20261023')
MANIFEST = ROOT / 'ARTIFACTS.json'
EXPECTED = '6e76ae74c3f6e0a4f2013840032fabc11e1c111fba4ed4ce463e93d91edbe36a'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
data = json.loads(MANIFEST.read_text())
assert data['status'] == 'CLOSED_ACTUAL_DIFFERS_UNADOPTED' and len(data['files']) == 680
assert len(data['excluded_runtime_caches']) == 35
for row in data['files']:
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
    'SCHOOL-front-gable-courses-one-ACTUAL-DIFFERS', mod.author_manifest(ROOT, MANIFEST),
    'School T2372 follow-up: exact680 noncache closed files plus originalmanifest. One actual official export/same-camera capture adds horizontal front-gable log courses, masterfe73a03a,528triangles. Direct source/full/detail review DIFFERS; visible improvement remains UNADOPTED. Stable4-file proposal/libertyCover, actual barePNG doorbaseline, raw/snapshot and receipts retained. Historical81 default/51positional checks are not a substitute for current82-family canonical integration.35 runtimepyc and external runtime symlinks excluded by author; no rights upgrade or canonical write.'
)
