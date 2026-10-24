from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T3041-front-shape-refinement-20261024');manifest=root/'PROPOSAL-SHA256.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8ee377b840a2465624e182559715be14a4d563fb7f08c50b74d2bafea99b7339'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==28 and sum(r['bytes'] for r in rows)==363898
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3041-front-shape-refinement-PROPOSAL-UNAPPLIED-UNRENDERED',mod.author_manifest(root,manifest),'Exact28 frozen frontshapeproposal payloads plus verifiedPROPOSAL-SHA256manifest. Sixfileoverlay44160B/SHA9bdba9b711bac0d1d0c72df502241ebcd52d86f65d29d1076ca2df9c7afb65c4,separatefivegradepatch,CPU25default/20overlaynontarget/API/schemaPASS. UNAPPLIED/UNRENDEREDatclosure,no native/fullacceptance;originalT3041/T2387open/differs. FutureREALadoptiononnewbranchfrompublicda65119separate/livecanonicaltreeEXCLUDED,no camerareassignment/imageacceptance orborrowedactualproof. Oldpacketsunchanged.')
