from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-dev38-1904-probe-v2-observer-20261024');manifest=root/'PREPARED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='98e8c6aface8ecfb0c9e64b9798ddeea775d6c6e1837ae0015c5449f4bba11d4'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==11
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==56203
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-dev38-1904-observer-v2-PREPARED-UNRUN-native-LOD-CORRECTION',mod.author_manifest(root,manifest),'Exact11 closed observerV2 preparation payloads plus original manifest. PREPARED_UNRUN fixes actualV1mobileLODobserver only: nativeGlessnerLight/Balanced chosenURL/declaredLOD/assetDetail binds actualselected streamedSHA-bytes/requestfinished,never fakeFull. Photosrowcredits/nativecaps/image/error predicatesunchanged. Closeddiagofactual001:3955624budgetPASSbutwholeQAFAIL36TLSCertrequests/35brokenlazy+1fullimage;all4exactcredits true. Prior missingCAnickname inference explicitlyRETRACTED,rootprovedcurrentCAtrustalias;NOglobalNSSimport/source/browser/bind changes. PureLODnegativeguards/syntax/dryPASS,NOactualnew8cards/fresh14/mergeproof,oldattempt/helperunchanged. __pycache__ omittedbyoriginalselection,noliveoutputsselected.')
