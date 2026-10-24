from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-daaf-official82-checkpoint-20261024T0107');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c49c9dfac84717a8793122ae2c15f5bfce2f24c01735d6eff7da4a941ba93b48'
author=json.loads(manifest.read_text());assert len(author['files'])==395
for rel,row in author['files'].items():
 p=root/rel;assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-daaf-ACTUAL-official82-redo-PASS-NATIVE-GATES-PENDING',mod.author_manifest(root,manifest),'Exact395 closed files plus manifest. Actual pinned official82master+82web producer exit0PASS:6master deltas=five intended visible plus exact prior-controlled9a0Kinzie UV-only; only5web changed and77byteexact. Hogan4guards,1797unrelated asset byte hashes and registry rows exact;82native input docs/recipes exact. Actual506stack/443buildinggate PASS including Cobweb5.05m head. All82masters/webGLBs,records,generators,22source snapshot, manifests,written list,logs/receipts and branchadoption included. Captured BEFORE native202manifest extension; remaining ordered native tail,full preflight and published browser QA PENDING; no code PR yet. Earlier82stale checkpoint remains historical, no current readiness/image-match claim and no live outputs selected.')
