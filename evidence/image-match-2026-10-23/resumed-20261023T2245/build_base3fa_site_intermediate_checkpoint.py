from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-base3fa-site-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b9571e3c860ce2f31bfd77a41febc64ef52136faf311b93b8b0ca5cc93b01a9e'
author=json.loads(manifest.read_text());assert len(author['files'])==11 and sum(r['bytes'] for r in author['files'])==145765
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-base3fa-compact-site-INTERMEDIATE-NOT-FINAL-FRESHNESS',mod.author_manifest(root,manifest),'Exact11 closed compact intermediate files plus manifest, depending on frozen d083 fixed653 audit. Actual00:20:36 snapshot on3fa+ff808 has sidecar lodging metadata84 while measured physical site findings remain exact. Root subsequently corrected model61.5 and reran normal scene tail; that future final70-input equivalence receipt is not included. NOT_FINAL_FRESHNESS, no current native/fullgate/browser/readiness claim, no canonical writes.')
