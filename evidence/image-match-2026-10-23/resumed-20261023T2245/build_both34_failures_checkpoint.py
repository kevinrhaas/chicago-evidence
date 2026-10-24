from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-both34-failures');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='d93b1a84ac087ef61d015b933c28bdb57e012361e38a1e6e347f6b72a29f453a'
author=json.loads(manifest.read_text());assert len(author['files'])==8 and sum(r['bytes'] for r in author['files'])==158657
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-both-mobile-desktop34-ACTUAL-FAIL-WOLF-bbox',mod.author_manifest(root,manifest),'Exact8 closed read-only actual failure files plus manifest. Mobile137PASS1FAIL,desktop134PASS1FAIL:both sameWolfwholeboundingbox11m versus2.6mwall. Rawbothlogs/jobs and exact6bfexecution bindings/diagnosis hypothesis retained,not repair or acceptance. At02:28 snapshot11success2failure5running,fullcoverage PENDING. No reruns/assertion changes/writers/heavy/merge/lap mutation by monitor/archivist.')
