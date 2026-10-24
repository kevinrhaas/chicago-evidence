from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-native-6bf-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='599d0d510b18a715821f0dd5210f6ab08db98f9e82c624fddcda4766905263df'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==69
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==10222333
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-6bf-ACTUAL-NATIVE-ONLY-61step2lap-PASS-GATES-PENDING',mod.author_manifest(root,manifest),'Exact69 closed native-only files plus manifest.13durable actual publish/stalecheck/derivation/focused phases exit0,normal202manifest61step tailsettled2laps finalunchanged. Correct3Glessner members materialized/hashed;oldheldGLBs excluded.105records/210GLBs/authoredsource,22cards/fullledger/orderbook/lodging/policy/constants/clauses/outliers exact. Only5native deltas:liberties,Tremont,source-sidecar/index,coverage;fullsnapshots+patchselected. Normal expiredsame-ownerCASrefresh5a8a93502:45:25,no force. Heavyclear02:50:25,schoolownsnextbrowser. NOactualbrowser/fullgate/codecommit/PR or imageacceptance;originalT2385DIFFERS/open,rightsunchanged,flagunadopted. No livetree/fullmirror/heldoldassets read.')
