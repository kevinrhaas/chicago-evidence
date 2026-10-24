from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-fixture-tmpdir-fix-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='f8d8ad4bc31ac7b47cc4942745a1aa01266509416ad73960ab1c72f0588f0de9'
author=json.loads(manifest.read_text());assert len(author['files'])==7 and sum(r['bytes'] for r in author['files'])==6254
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-fixture-tmpdir-prerequisite-focused10tests-PASS',mod.author_manifest(root,manifest),'Exact7 closed files plus manifest. Root-authorized4 TemporaryDirectory dir=/tmp argument edits in only2 fixture suites, exactdaaf preimages and unchanged production helper guard hashes. Focused suites4+6tests PASS under workspace TMPDIR with exact patch/log/exit receipts. No heavy/native/fullgate/publish/codecommit or current readiness claim; no live tree selected.')
