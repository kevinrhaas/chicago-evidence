from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-dev8e-body-adoption-checkpoint');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='eac36fa98f31bd871b382777c91c214d83897a4e30e03a057949ae6287fea3a2'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==17
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-dev8e-ACTUAL-v2-body-diagnostic-adoption-UNCOMMITTED-NOT-GATE',mod.author_manifest(root,manifest),'Exact17 closed source checkpoint files plus manifest. Actualnormaldev8e reconciliation and guardedv2 bodydiagnostic adopted,binarypatchfrom public6bf/stagedtree/mergeparent recorded. UNCOMMITTED_CHECKPOINT_NOT_A_GATE:actualbrowser/currentfullpreflight/smokesPENDING.105native recipes/210GLBs byteexact6bf. Originalv1/v2proposal and earlieractualfailures preserved separately;no asset/modelgeometry change,gateacceptance/readiness/image-match claim. No live folders selected.')
