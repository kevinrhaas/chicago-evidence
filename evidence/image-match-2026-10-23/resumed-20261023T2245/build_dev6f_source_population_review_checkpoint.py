from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-dev6f-pinned-source-population-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='f8b7f484461495d17e6006c8f6d1cccfa93b5c4302c37d66609afd0507035d91'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==6
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1044305
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-pinned-dev6f-source-population-bounded-review',mod.author_manifest(root,manifest),'Exact6 closed pinned6f read-only review files plus manifest.105ownrecords/registryrecipes+210existingassetsexact60to6f,2436populationinputsexact;threeincomingstructuresform-only,ZERO nonform/layoutdiffs. Source dependencies/newGlessner20part-threeGLBrecoverycontractretained. Rootreportedrematerialize/checkPASSexplicitlynotexecutedbyreviewer. No writes/claims/heavy/gate/CIdispatch;futureCIawaitsnewheadbinding,notcurrentapproval/readiness/imageacceptance. No live mutable root selection.')
