from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-dev-ancestry-merge-026ace-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8c64f73689623d6142aef1238b57f02f22f21e4233c5ae024a9b43bc7760a524'
author=json.loads(manifest.read_text());assert len(author['files'])==5 and sum(r['bytes'] for r in author['files'])==19124
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-dev026ace-ancestry-merge-UNCOMMITTED-EXPORTS-EXACT',mod.author_manifest(root,manifest),'Exact5 closed files plus manifest: normal uncommitted026ace dev ancestry merge into daaf topic,59hash proof retains14owned deltas and46actual exports. Scope guard caught squash-history retained T3055 pending file; exact title/kind/items already folded once proved, only intended incoming deletion applied; final2 staged fold paths exact. No native/fullgate/publish/heavy/codecommit or readiness claim; no live tree selected.')
