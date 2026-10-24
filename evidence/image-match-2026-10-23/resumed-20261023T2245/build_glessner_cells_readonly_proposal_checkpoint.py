from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-full-glessner-cells-proposal-school-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8e405c7dd4e5e147e28d9b57fbe23ead517da135d8aa1ca0084e60b06202be35'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==6
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==20155
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-Full-Glessner-cells4to2-READONLY-UNAPPLIED-PROPOSAL',mod.author_manifest(root,manifest),'Exact6 closed readonly proposal files plus manifest. UNAPPLIEDonefieldexistingFullopaqueGlessnercells4to2candidate,no canonical/workflow/asset/quality/cap edits.6tiny nativekernel fixtures preserveexacttriangles/attributes/conservativebounds. GLBJSONheader/source metadataonly,nobinarydecode/duplicatescan/browser/bake/gate. No actualsavings/latestspawnverdict; spherecullingcaveat and owed baseline/candidate normalmeasurements explicit. No heavy/livework selected.')
