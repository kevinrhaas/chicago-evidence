from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-daaf-final-site-audit');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='5fce54111f7875aef4a98dbfa8ca1b73c9bf8062c8282f10795a66852f1ec6db'
author=json.loads(manifest.read_text());assert len(author['files'])==19 and sum(r['bytes'] for r in author['files'])==507407
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-daaf026ace-FRESH70-input-bounded-site-audit',mod.author_manifest(root,manifest),'Exact19 closed fresh bounded site files plus manifest, depending on d083 frozen input snapshot:70inputs remeasured,68reused exact and2changed copies(newhead parameter source,three Wolf woodpile centres). Current zero body/both-door-zone hits among3515points/segments,653entries,both native aprons and allwater disjoint; snapshot replay exact. Parent native61step/202/two-lap logs bound. No fullgate,3D/app/browser/historical-setback/readiness/image-match claim. Live preflight released after capture and entirely excluded; no canonical/native/heavy writes by audit/archivist.')
