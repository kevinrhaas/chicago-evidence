from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-cobweb-stack-head-proposal');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='7a147bf9931ce11c672fe8141cbb42d3ef73831301c1630b6d816f3c50ecd682'
author=json.loads(manifest.read_text());assert len(author['files'])==107 and sum(r['bytes'] for r in author['files'])==7714099
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-COBWEB-stack-head-CPU-proposal-UNAPPLIED-NO-EXPORT',mod.author_manifest(root,manifest),'Exact107 closed proposal files plus manifest,5authored paths. UNAPPLIED at capture: existing head control shifts only64chimney Z vertices to5.05m heads, global roof clearance0.524429m and0.067229m margin; pure CPU82 default/other81 exact. No new actual export, Blender/native/heavy/fullgate/browser run or accepted historical geometry claim. Root actual application and required official82 redo on laterdaaf base remain separate; no live canonical files selected.')
