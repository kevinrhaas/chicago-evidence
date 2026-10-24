from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1239-live-owner-watch-20261023/closed-96ca-review')
manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='7cb42998257b054871b6429bed6f2180928de5a7f3f1b1b2e4b496eaa3e96496'
author=json.loads(manifest.read_text());assert len(author['files'])==6
assert sum(r['bytes'] for r in author['files'])==538643
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1239-96ca-readonly-guards-CHECKS-PENDING-NO-APPROVAL',mod.author_manifest(root,manifest),'Exact6 closed read-only files plus manifest. PR1239 head96ca preserves87 a219 guards and exact V2 tools; LIBERTIES full hash d872bfe51b324e72bd47b8682ee5363d943edbce119fb3849a7fef4ed5a33079 is exact a219 prefix plus2849B Glessner append. 17ac-to-dev-e5 delta is T3024 changelog fold only. Current96ca checks pending at capture; earlier20455 hosted PASS remains historical. No writers, lap changes, heavy jobs or approval.')
