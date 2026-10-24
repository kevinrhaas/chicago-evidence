from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-H8-stage14-prepared/closed-HOLD-after-budget-failure');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='ed4951819374b722c4d361e9b4305a1df68cc434c0e3a49be9aaee7dff98aab2'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==11
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==22947
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H8-AUTHORITATIVE-HOLD-failed35f0-NO-POST',mod.author_manifest(root,manifest),'Exact11 closed operational HOLD payloads plus original manifest. ParentexplicitlyFORBIDSstage14dispatchoncheckpoint35f0c564cafterparent-reportedactual1904Full4666158>4600000;separatefullgate1063/383PASSnotbudgetwaiver. ActivecontrollerenforcesCONFIGhold/explicitlaterrepairedheadauthorizationandrejectsfailedprefix. NO POST/operationsentinel/binding/watcherexists,leaseunarmed. Earlierb805preparedsnapshotremainsdatedpre-HOLDreadiness;thislaterHOLDguidesrecoveryuntilparentauthorizesrepairednewhead. Numberscontextnotnewobservermeasurement,nomutation/CIclaimbyarchivist.')
