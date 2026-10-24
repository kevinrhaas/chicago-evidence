from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T-3082-official23-prep-3fa-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='ac365d2bdeda7a93368cc5739b1cd9f3473d5ccb3ce5a90db065ec42eb6308e6'
author=json.loads(manifest.read_text());assert len(author['files'])==18
assert sum(r['bytes'] for r in author['files'])==803124
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-3fa-official23-migration-PREPARED-UNCOMMITTED-UNBAKED',mod.author_manifest(root,manifest),'Exact18 closed latest-base migration/preparation files plus manifest: standard guarded migration receipt, latest authored/fold patches and entry, actual current CPU default parity, syntax/dry-passed split official23 runner, copied immutable actual1106+25 input binding and old manifests. HEAD3fa/MERGE_HEADff808 remains UNCOMMITTED/UNBAKED at capture. Heavy grant not consumed; no producer/browser/gate. Original T2385 open/claimed/DIFFERS, flag research unadopted, rights unchanged. Live tree, binding future run outputs and held GLBs excluded.')
