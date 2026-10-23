from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/log82-applied-review-20261023T2320')
MANIFEST = ROOT / 'MANIFEST.json'
EXPECTED = 'b67a21b927330d09b761161485921e4ccae325853ee060a8c4eff703e45b60dc'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
author = json.loads(MANIFEST.read_text())
assert author['status'] == 'CLOSED_READONLY_APPLIED_REVIEW' and len(author['files']) == 12
for row in author['files']:
    path = ROOT / row['path']
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256']
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'T3081-readonly-applied82-default-and-source-guards-NO-APPROVAL', mod.author_manifest(ROOT, MANIFEST),
    'Closed bounded root-application audit:12 exact files plus manifest.82 legacy raw geometry/material/confidence exact with12new controls disabled; enabled school528tri raw parity, Hogan/Ouilmette byteguards and rawLIBERTIES prefix+append pass. Native manifest --check only reports201steps/415resolvablefiles, not native execution. Official82 generation/native consumers/published/fullgates pending. current symlink/caches excluded; not liveworktree, original image acceptance or merge approval. Later rootSTATUS wording fix belongs to next source checkpoint.'
)
