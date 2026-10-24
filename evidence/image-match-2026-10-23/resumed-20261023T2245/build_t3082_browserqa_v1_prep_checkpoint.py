from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-browser-qa-v1-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='18863fdce13c17419e4a1e691904facacb6b729da37630ace74731f7508b1ef8'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==14
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==863093
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-browser-photo-QAv1-PREPARED-UNRUN',mod.author_manifest(root,manifest),'Exact14 closed external QApreparation files plus manifest. Fourfuture appcasesTremont/Cobweb mobile/desktop strict popup/InspectPeople reasonflags/newheading,source/Photoscredits and priorgeometry/contact/network/error guards;unchangedexactnoticechecker bindsapprovedNEW14messages/old14IDs. Onefuture nativephoto_match sameprovisionalcamera16830ec/sourceb45d6068,onlyexternalmatchrecordmutable,noacceptance. Syntax/refusal/mobile-desktop/photo dryPASS,NOactualbrowser/publish/Blender/fullgate/capture. Gifford ownerapprovedcredit/rights preserved,no upgrade;originalT2385DIFFERS/open,flagunadopted. OlderQA/failuresunchanged,no live/future runsselected.')
