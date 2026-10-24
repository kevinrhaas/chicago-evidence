from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-H8-dev38-gate-budget-fail-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='dd6fbc8badf5f6f9d32b6b6772eb7424065946da8d15599e4f57283d9a6d09c6'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==38
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==8958854
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H8-PUBLIC35f0-native-fullgate-PASS-ACTUAL-BUDGET-FAIL-BLOCKS-MERGE',mod.author_manifest(root,manifest),'Exact38 closed priority publicsource/native/gate/budget payloads plus original manifest. Real pushed H8public35f0c564cc25303d3f5641812d532dd9d2166b64 whole-tree9c53 exacttestedsource,full1063/383PASS and10nativephasesPASS. Actual1904Full4666158triangles exceeds unchanged4600000 by66158:FAIL BLOCKS MERGE. Allapp/site originalbindingpostguardnewfilePASS preserved separately, originalFAIL neverrewritten. Stage14 dispatch HOLD authoritative for this failed checkpoint. Parent proposes one reviewed futureOBBactualcandidate,NOTapplied/measuredbythispacket;no repair/CI/mergeapproval or oldDAresultinheritance. No livecanonical/watch outputs selected.')
