from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-330c-owner-handoff-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='7199ec273f569d7b4c8dfe2602fbeccdcb4a54ddc3adc1a959b12b7574cddd1b'
author=json.loads(manifest.read_text());assert len(author['files'])==9
assert sum(r['bytes'] for r in author['files'])==1999971
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1256-330c-readonly-owner-handoff-NO-TAKEOVER-OR-APPROVAL',mod.author_manifest(root,manifest),'Exact9 closed read-only files plus manifest.87 a219 guards exact;330c only changelog fold, newdev2f25 no owned87/log/lodging population delta. Owner completed00:17:38 success; no lap1239/1256 observed00:19, future acquisition must re-read. Actual3fa6 hosted1060PASS raw transcript job120716733333 binds merge8874634a8=3fa6 into9f and is explicitly historical versus current330c+2f. No takeover, approval, writer or new job.')
