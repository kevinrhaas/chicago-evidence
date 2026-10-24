from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-3fa6-supersession-review')
manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='36f6c31eb33abea96d61a74544c1a3ea8685fab1d85c27c2e74dbde9ea541429'
author=json.loads(manifest.read_text());assert len(author['files'])==6
assert sum(r['bytes'] for r in author['files'])==252985
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1256-3fa6-supersedes-closed1239-readonly-CHECKS-PENDING',mod.author_manifest(root,manifest),'Exact6 closed read-only files plus manifest: PR1239 closed unmerged in favor of non-draft1256 same new3fa6 branch;87 a219 guards exact. LIBERTIES preserves full96ca prefix plus2331B Kimball append, hashes bound in receipt; source9f21/PR1255/T3076, actualff808 delta changelog fold only. New current-head checks pending at00:02 capture; prior96ca proof historical. No writers, native/heavy/browser jobs, lap changes or approval.')
