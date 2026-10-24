from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-mobile34-failure');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='df11e681053e55e54360c5c9e17d4e0dec0d11ec3e92b455278b3bf9583d2496'
author=json.loads(manifest.read_text());assert len(author['files'])==6 and sum(r['bytes'] for r in author['files'])==89466
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-mobile34-ACTUAL-FAIL-WOLF-bbox-FULLCOVERAGE-PENDING',mod.author_manifest(root,manifest),'Exact6 closed actual failure files plus manifest. Mobile3-4 run40051671920 exact6bf:137PASS1FAIL(Wolf boundingbox11m versus wall2.6m),zero pageerrors. Source-bound read-only hypothesis:signpolehead10.3+arm0.66=10.96 while meter measures wholeinstance with9.76limit; hypothesis not repair/acceptance. Snapshot11success1failure6running,fullcoverage PENDING. No assertion/source edits,job/merge/lap mutation or finalapproval by reviewer/archivist.')
