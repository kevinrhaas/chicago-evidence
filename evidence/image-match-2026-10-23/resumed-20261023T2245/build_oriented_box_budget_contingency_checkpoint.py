from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-oriented-box-contingency');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='a778757060d26a4cc916a373b7d7c6f82a8ba39d349f1d75e2f7d8e8883df1d0'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==16
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==124122
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-oriented-box-budget-CONTINGENCY-UNAPPLIED-SAVING-UNMEASURED',mod.author_manifest(root,manifest),'Exact16 closed contingency payloads plus original manifest. UNAPPLIED one-path batch-frustum-box affine plane-support using same cachedlocalbox/fringe;47existing+6newCPU controlsPASS,including2000random/300grazing. No vertexcache/geometry/cap/camera/tier/material/pick change. Actual root newdevspawnFAIL4666158/66158over retained verbatim;candidate actual savingUNMEASURED/maybenone,NO fixclaim. Initialmissing-integration-fixture error retained before47PASS. Parent review/adoption/actualcandidate pending,noheavy/canonicalwritesbyproducer/archivist;no currentgate/browser/mergeapproval.')
