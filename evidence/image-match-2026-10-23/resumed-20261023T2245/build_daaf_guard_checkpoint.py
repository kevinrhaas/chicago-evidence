from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-daaf-guard-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b323f264f52f78efb8111bf25626b1dab693c43f2f12ef1683aca015038dd3a5'
author=json.loads(manifest.read_text());assert len(author['files'])==5 and sum(r['bytes'] for r in author['files'])==124207
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1256-daaf-readonly-guards-CURRENT-GATE-PENDING',mod.author_manifest(root,manifest),'Exact5 closed read-only files plus manifest.1256 head daaf/currentdev2f25;87owned guards exacta219 and no log/lodging input delta.313old LIBERTIES blocks retained with only intentional Glessner2203 revision plus one Coleman3077; all other body exact. Dated00:53 snapshot has liveowner/newgate pending, no approval/mutation. No new native/browser/heavy/gate job or canonical writes by audit/archivist.')
