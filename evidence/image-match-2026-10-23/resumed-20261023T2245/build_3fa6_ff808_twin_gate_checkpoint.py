from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-3fa6-ff808-twin-gate');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='607813c75ef426633d68d25c2261e0dced76756faf304b2d616b5d4f46d5f89b'
author=json.loads(manifest.read_text());assert len(author['files'])==4 and sum(r['bytes'] for r in author['files'])==1834934
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1256-3fa6-ff808-twin-hosted1060-PASS-HISTORICAL',mod.author_manifest(root,manifest),'Exact4 closed read-only files plus manifest. Actual hosted job120716837616/run40042580102 completed00:21:50 with1060PASS/383 self-tests; exact merge381b93dbb binds3fa6 intoff808, matching root current base at capture. Historical versus current330c+2f25; owner40044007439 still live00:42. No approval, mutation or new job. Outside-packet admission refusal record not selected, no live owner files archived.')
