from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-base3fa-site-final');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='3c64c4734f5cfd71076ecf2184a75c6208af793b1a45d1b666fd0068e1fb2dba'
author=json.loads(manifest.read_text());assert len(author['files'])==4 and sum(r['bytes'] for r in author['files'])==33201
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-base3fa-final70-input-BOUNDED-SITE-EQUIVALENCE',mod.author_manifest(root,manifest),'Exact4 closed final compact files plus manifest after root fresh model and tail67528 exit0. All70 current native source/data inputs EXACT frozen settled d083 audit, corrected metadata61.5/62; inherits only its bounded2D653door/site proof. Binds actual3fa/ff808/index and final56step2lap tail; dependencies d083 plus intermediate b957, whose stale-metadata timepoint stays NOT_FINAL_FRESHNESS. No new bake/browser/fullgate/readiness/image-match claim or canonical writes by audit/archivist.')
