from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-parent-landed-86acc-proof');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='1ec457e5dcc8e3676548361ebaf2620da64949f3804f0c3e7e7ec108839bb913'
author=json.loads(manifest.read_text());assert len(author['files'])==6 and sum(r['bytes'] for r in author['files'])==1887813
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1256-LANDED-86acc-parent-hosted1060-PASS-NO-T3081-APPROVAL',mod.author_manifest(root,manifest),'Exact6 closed parent-landed proof files plus manifest. PR1256 merged01:14:15 squash86acc7914fcbc44dd0e85cd1ada853a6d5d5868c; actual hosted job120730355529/run40046820691 PASS1060/383 at exactmerge200fd6fd2=daaf into2f25, movingframes/reportPASS. Owner completed01:14:48 success.87 a219 guards exact on both86acc squash/currentdev026ace; only2file T3055 fold afterward. Read-only proof of parent landing, not T3081/T3082 validation/adoption or image-match approval; no source/lap/job mutation.')
