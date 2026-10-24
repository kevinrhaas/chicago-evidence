from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5112-stage14-watch/closed-H9-desktop14-actual-PASS');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='cf81336d33d847eadccda4b6c8899af5480b76c7d71441e861d3b7c501ab5908'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==7
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==135959
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix not in ['.pyc','.key','.p12','.pfx'];data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H9-EXACT5112-desktop14-PREMERGE-ACTUAL-Full-BUDGET-PASS',mod.author_manifest(root,manifest),'Exact7 closed PREMERGE currentH9desktop14 payloads plus originalmanifest. Exact5112/run40091268264/job120864261854,140PASS0FAIL/zeroerrors/fullSMOKEPASS. ACTUALcurrentFull1904 4164calls3943402triangles versusUNCHANGED7800/4600000,margin656598,budget12:44:20/jobdone12:44:23. Rawjoblog/run/source/inputbinderretained,NOnewPOST/rerun/edit/bypass. Mobilea6b20dseparateactualproof,combined2logclosurefutureseparate. Original35budgetFAIL/H8candidateproof/DAconditionalcoverage distinct;thisispremergecurrentbudgetPASSnotarchivistmerge/sourceacceptanceorblanketcurrent18coverage. No livewatch/canonicaltreeselected.')
