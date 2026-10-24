from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head-da65119-watch/closed-desktop14-actual-cap-PASS');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c3caa285f8c6151ef39c1e3c7281596d6a31d527693cf3f4e3f6f9651dcd9011'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==6
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==101945
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-da65119-desktop14-ACTUAL-CAP-PASS-17of18-PARTIAL',mod.author_manifest(root,manifest),'Exact6 closed actualconsolidateddesktop14payloads plus manifest. Raw140PASS0FAIL/exactda65119head-stage-viewport/zeroerrors. Actual1904spawn5097calls4591258triangles versusunchanged7800calls4600000triangles,margin8742. Matrix17of18stagedPASSonlydesktop13PENDINGatcapture,NO fullapproval/currentdevinheritance/oldfailurerelabel. AlloldH4H5failureshistoricalanddistinct,no livewatchharvesting/CI/source mutationbyarchivist.')
