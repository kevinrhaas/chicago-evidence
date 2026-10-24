from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5112-stage14-watch/closed-H9-mobile14-actual-PASS');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='a6b20dfc0f430c8ee00414d8c132236db1c774f5abeee61471ca0b6e8d0ba2f6'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==7
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==108068
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix not in ['.pyc','.key','.p12','.pfx'];data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H9-EXACT5112-mobile14-ACTUAL-PASS-Desktop-PENDING',mod.author_manifest(root,manifest),'Exact7 closed actualH9mobile14 payloads plus original manifest. Exact5112/mobile14/run40091276811/job120864286492,140PASS0FAIL/zeroerrors/fullSMOKEPASS. Actualcurrentdata1904spawn1714calls711234triangles versusUNCHANGED7800calls1270000triangles. NativeT2645GlessnerPhotos-tabcasePASS isNOTextra35PhotosUIproof;localNSSEROFSFAILdistinct,noTLSbypass. Desktop14stillPENDING,NO currentH9Fullbudget/fullcoverage/mergeapproval orH8prototypeinheritance. Rawlogs/inputs/jobs/source preserved,no livewatch/source/CI actionsbyarchivist.')
