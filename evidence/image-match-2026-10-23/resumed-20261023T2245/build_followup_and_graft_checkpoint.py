from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
packages = [
    (
        Path('/tmp/chicago-next-model/T-2385-followup-plan-a219-20261023'),
        'CLOSED-MANIFEST.json',
        'ceeea69571b12318fce6bf07d17c364bd2ed310246057074c425418f289f2e10',
        13,
        'TREMONT-a219-23master-followup-LIGHT-UNAPPLIED-UNBAKED',
        'Exact13 closed LIGHT files plus manifest: a219 23-master inventory, prior CPU-parity binding, authored integration/build plan and draftdocs/changelog. UNAPPLIED/UNBAKED, no new browser/fullgate, originalT2385 open/DIFFERS and flagposeunadopted. Frozen sourceevidence unchanged; no rights upgrade or code PR.'
    ),
    (
        Path('/tmp/log82-graft-prep-20261023T2340'),
        'MANIFEST.json',
        'fcce162c55f53e5f26140cabac25e1256a6e9a2cbb3a7e8a4d87f7e7afe451bc',
        25,
        'T3081-guarded-graft-helper-PREPARED-NOT-APPLIED',
        'Exact25 closed helper/overlay/report/fixture files plus manifest;45LIGHT checks, actual disposablegraft and preimage/HEAD/index/no-partial-write guards. NOcanonical graft or official/native/browser/fullgate. Supports explicit futurecommit or resolveduncommittedmerge; base5f18files bind authoredb9ad snapshot. Root liveSTATUS newwording intentionally refused. Only prepared helper, no liveworktree or newly baked outputs.'
    ),
]
for root, filename, expected, count, name, note in packages:
    manifest = root / filename
    assert hashlib.sha256(manifest.read_bytes()).hexdigest() == expected
    author = json.loads(manifest.read_text())
    assert len(author['files']) == count
    for row in author['files']:
        path = root / row['path']
        assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
        assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
        assert path.suffix != '.pyc'
        payload = path.read_bytes()
        assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], path
    mod.archive(name, mod.author_manifest(root, manifest), note)
