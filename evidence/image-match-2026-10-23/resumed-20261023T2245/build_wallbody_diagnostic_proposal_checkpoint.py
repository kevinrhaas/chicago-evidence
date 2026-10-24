from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-wall-body-diagnostic-proposal');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='173903eb6009b8cde6448323798c57fb34ab5f61513c1d1333d3dcbcfe8f5fdf'
author=json.loads(manifest.read_text());assert len(author['files'])==24 and sum(r['bytes'] for r in author['files'])==3102261
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-wall-body-diagnostic-3path-PROPOSAL-UNAPPLIED',mod.author_manifest(root,manifest),'Exact24 closed proposal files plus manifest. UNAPPLIED3path stored-position read-only body diagnostic,CPUactualGLB+18controlsPASS;actual browser/native/fullgate UNRUN. Originalfullbounds11.022m versusbody5.4016m,unchangedwalllimit9.76. Small source geometry-section bounds are diagnostic measurementcaps,not produced asset/model geometry. Provenance/limits/frozen inputs retained;parent may later adopt afterdev8e. No canonical/liveQA/model/asset edits or gate acceptance by proposal/archivist.')
