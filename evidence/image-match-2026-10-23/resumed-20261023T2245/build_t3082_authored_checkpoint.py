from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T-3082-authored-integration-96ca-20261023')
manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='f499de07fbe97caabd449549007127b7e5ffccbaaadd82e4ba87d0176e734e6f'
author=json.loads(manifest.read_text());assert len(author['files'])==19
assert sum(r['bytes'] for r in author['files'])==152151
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-TREMONT-96ca-authored-integration-UNCOMMITTED-UNBAKED',mod.author_manifest(root,manifest),'Exact19 closed authored files plus manifest, including authored-only patch, separate incoming e5ed fold patch, actual T3082 entry/ticket, raw documentation prefix guards,23 no-bpy recipe documentation/stale plan, protected Hogan/Glessner/native flag/source bytes, read-only Glessner proof and reversible old-cache move receipt. New steward/t3082-tremont-quarter-roof at96ca remains UNCOMMITTED/UNBAKED at capture; no new native browser/fullgate/PR. Original T2385 open/claimed/DIFFERS, flag research unadopted and no rights upgrade. Live code tree and held old258999416B committed792 cache GLBs excluded.')
