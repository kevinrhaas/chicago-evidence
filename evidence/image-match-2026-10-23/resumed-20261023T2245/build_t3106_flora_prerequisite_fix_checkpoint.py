from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3106-flora-prerequisite-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='397dc580fc47c71bf8f95385b94179b4fdbfc9ba65917ebc6ce90ab9a890855e'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==43
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==3941857
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3106-scoped-flora-prerequisite-ACTUAL-one-mobile-PASS-NOT-FULLGATE',mod.author_manifest(root,manifest),'Exact43 closed floraprerequisitepayloads plus manifest. Actualscopedsource/datafixinisolatedutilitybranch/ONEnativepublishedmobile1812LightcasePASS:all10declaredstems/zerofloraproblems/1583of2100trees/north1113.108m. Source-nativeCPU/sixfocusedchecksPASS. Originalfort/read-onlybaselineFAIL/helper-optionstrictfailuresretained,distinctfrom2d0f. Runtime3/authored6/full7patches/exactsourcehashesincluded. Rootreview/canonicaltransplantPENDING,nocodepush/PR/merge/fullgate/imageacceptance,no livefolderselected.')
