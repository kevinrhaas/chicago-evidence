from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-full18-old6bf-results');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='270ba53d2f13201924d6cfb0070c0a43cf2251ee72b0d1c4183fdb06534f9e61'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==59
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==3051058
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-old6bf-FULL18-COMPLETE-15PASS3FAIL-NOT-SMOKE-PASS',mod.author_manifest(root,manifest),'Exact59 closed final old6bf hosted files plus manifest. Bothviewport15parts coveredby18actual exact6bf jobs:15SUCCESS3FAIL,all18zero pageerrors. Failuresmobile3-4Wolf137/1,desktop3-4Wolf134/1,desktop14triangle139/1;15otherjobsPASSincludingdesktop13. Raw18logs/jobs/originalrequestJSONs/fullreceipt+hosted1060gate preserved. COMPLETE_EXECUTION_WITH_THREE_FAILURES_NOT_SMOKE_PASS: no inheritance,waiver,currentheadvalidation/finalapproval/imageacceptance. No job/source/lap/merge mutation bymonitor/archivist.')
