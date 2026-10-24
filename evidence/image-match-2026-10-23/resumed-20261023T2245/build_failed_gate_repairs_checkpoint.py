from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-after-failed-gate-checkpoint-20261024T0058');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='d89c83fb963a16664a51d204973d55fbf942cb1d2d61b217ed81e4f599622fd8'
author=json.loads(manifest.read_text());assert len(author['files'])==100
for rel,row in author['files'].items():
 p=root/rel;assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-first-fullgate-FAIL7-focused-repairs-PASS-82ASSETS-STALE',mod.author_manifest(root,manifest),'Exact100 closed current-state recovery files plus manifest: tracked/untracked authored state and binary/index patches, complete first fullgate FAIL7/1060 logs with original process exit unavailable after restart, focused four repairs PASS, actual native woodpile/placement build checks with before files, adopted Cobweb five-path metadata/head patch and CPU proof. CURRENT generator changed but all82 actual export/recipe redo remains owed and old recipes STALE. No code commit/PR/readiness/fullgate PASS/browser/image-match claim. Earlier unadopted Cobweb proposal retained as separate timepoint. No live folder selected.')
