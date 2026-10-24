from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-prestack-current-whole-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='2eea1db76fe56525d06cb1c8c15aac23e87461d22ccb79dea2bf8c38bd6861e1'
author=json.loads(manifest.read_text());assert len(author['files'])==68 and sum(r['bytes'] for r in author['files'])==14894171
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-PRESTACK-WHOLE-OWNED-STATE-UNCOMMITTED-NATIVE-GATES-PENDING',mod.author_manifest(root,manifest),'Exact68 closed whole-owned-state files plus manifest before stack migration: full raw dirty docs/source/fixtures, staged/unstaged/HEAD patches and fold deletion,current native registries,46actual frame exports,binding/semantic proof. daaf+026 merge UNCOMMITTED; future stack onto committed pushed6bf/T3081PR1260 requires this recovery proof first. OriginalT2385 open/DIFFERS,rights unchanged,flag research unadopted; native/fullgates pending. No live tree/held cache read; no current readiness or accepted image-match claim.')
