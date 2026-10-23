from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
ROOT = Path('/tmp/T3081-published-qa-20261023')
MANIFEST = ROOT / 'MANIFEST.json'
EXPECTED = '157c19c04f654ab8a3c30c7cc6bae94913ddeeb47aa438e2b14f4b6efe84f5d3'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == EXPECTED
author = json.loads(MANIFEST.read_text())
assert author['status'] == 'FROZEN_PREPARED_NOT_BROWSER_EXECUTED' and len(author['files']) == 19
for row in author['files']:
    path = ROOT / row['path']
    assert path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__', 'node_modules', '.git', 'runs'] for part in path.parts)
    assert not path.name.endswith('.match.json')
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], path
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.archive(
    'T3081-five-model-published-QA-PREPARED-NO-BROWSER', mod.author_manifest(ROOT, MANIFEST),
    'T3081 QA preparation only:19 exact files plus manifest. Syntax/drymode only, no browser executed or current output. Future published mobile/desktop models, Photos/Sources, contact/entrance QA helper; exact five authoredrecord metadata, five original provisionalcameras plus portable path-only copies/sourceimages retained. No new solves, acceptedmatches, canonicalwrites or actual publishedQA. Future runs and newly generated portable matchfiles excluded.'
)
