from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-ready-for-preflight-02-checkpoint');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c3a5ef879a692fca166e614d8fb43325c3f2e20a25af81522577fb0b051d9abc'
author=json.loads(manifest.read_text());assert len(author['files'])==99
for rel,row in author['files'].items():
 p=root/rel;assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-current-native61step-PASS-BEFORE-fullpreflight02',mod.author_manifest(root,manifest),'Exact99 closed current root recovery files plus manifest: all current source/assets/native deltas, binary/index patches, complete native61step2lap PASS receipts, final focused checks, dev026 ancestry/fold resolution and pending preflight runner.82 fresh input/recipe docs,Hogan4,original22cards/ledger/orderbook exact; native202 and0of3515doorway obstructions. Explicitly BEFORE fullpreflight02, not wholegate PASS. Running /workspace/T3081-daaf-preflight-02 is excluded entirely; no live tree read/browser/readiness/image-match claim. Final site proof belongs to separate closed packet.')
