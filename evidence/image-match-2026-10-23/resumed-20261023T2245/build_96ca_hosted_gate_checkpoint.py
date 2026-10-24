from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-96ca-hosted-gate')
manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='a93aca466794f427c014cc498e0c4e1495b2f58720e2ceebeee3866bf80c6ca5'
author=json.loads(manifest.read_text());assert len(author['files'])==4
assert sum(r['bytes'] for r in author['files'])==1837916
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1239-96ca-e5-actual-hosted1060-PASS-NO-FINAL-APPROVAL',mod.author_manifest(root,manifest),'Exact4 closed read-only files plus manifest: actual hosted job120710578230/run40040620666 raw transcript and bound proof,1060PASS,383 self-tests,T3055 changelog. Exact checkout merge1266bb91e4fcbddb9b6ff90d4e212df0ec4ea4b5 binds96ca into actual deve5. Snapshot still has moving-frames pending, draft/open PR and live owner. This updates historical earlier20455 proof only for its explicitly bound current stack; no new job, writer, native/browser execution or final approval by archivist/reviewer.')
