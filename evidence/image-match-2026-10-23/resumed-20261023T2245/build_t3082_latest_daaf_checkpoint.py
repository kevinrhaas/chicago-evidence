from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-latest-daaf-prep-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='1826984e62411b54e6442116688dab16fbd39cf1da92664b6fbe71547d278ce7'
author=json.loads(manifest.read_text());assert len(author['files'])==24 and sum(r['bytes'] for r in author['files'])==6844909
for row in author['files']:
 p=root/row['path'];assert len(Path(row['path']).parts)==1;assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-latest-daaf-actual-migration-UNCOMMITTED-GATES-PENDING',mod.author_manifest(root,manifest),'Exact24 closed top-level migration files plus manifest, candidate disposable fixture EXCLUDED explicitly. Full incoming raw documents/history, own suffixes,4preimages,23native candidate input proof/docs, actual migration receipt/recomputed23hashes,46genuine export transfer hashes/protected rows, actual registry transfer results and final diff/entry/status. v3HEAD full daaf276c4d3310f050dc96bbb67e8cfe80078388 UNCOMMITTED; downstream/native/fullgates/PR pending. Earlier actual exports independently remote0cfce6af/b279. Failed extraction and tuple-versus-JSON preparation diagnostics retained; no production recipe mismatch. Original T2385 open/claimed/DIFFERS, rights unchanged, flag research unadopted. No live tree/candidate/held cache selected.')
