from pathlib import Path
import hashlib, importlib.util, json
WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
root = Path('/tmp/log82-official-checkpoint-20261023T2335')
manifest = root / 'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == '9d7f6ca4ba4e1b1873a68d1e629ce9b02cf6325fe007688763b47292929dcb0c'
author = json.loads(manifest.read_text()); assert len(author['files']) == 650
assert sum(row['bytes'] for row in author['files']) == 26567474
for row in author['files']:
    path = root / row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
    assert path.suffix != '.pyc'
    payload = path.read_bytes()
    assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], path
mod.archive('T3081-official82-master-and-web-bake-NATIVE-FULLGATES-PENDING', mod.author_manifest(root, manifest), 'Exact650 closed files plus verbatim author manifest: actual official82 masters and web outputs,195 generator/record bindings,18 authored changes, native produced manifests/logs, UV actual old/new controls and before18 stamps. Official generation exited0:76 master byteexact,5 intended visible changes,1 reviewed Kinzie stable UV-only delta;77 web byteexact and only5 changed. Hogan4 guards exact. Native consumers, published browser QA and full gates remain pending. No canonical adoption, code readiness or original image-match verdict; no live worktree selected.')
