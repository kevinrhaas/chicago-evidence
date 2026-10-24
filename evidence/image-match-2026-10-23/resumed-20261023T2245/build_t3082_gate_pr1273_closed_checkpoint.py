from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-gate-PR1273-closed-20261024T0704');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='4caa982d20ffff544f71652d5345dae6c79d441637ad9198d3b5544b44cac9a5'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==24
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1808135
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-ACTUAL1062-PASS-code9f95-DRAFT-PR1273-HOSTED-PENDING',mod.author_manifest(root,manifest),'Exact24 closed compactgate/PRpayloads plus manifest. Full1062checks/383selftestsPASSwithinitialENOSPCandstandardnativesolitaryretryhonestlyretained. H5workflowonlyFF/all20sourcebyteguards,rawprefix-safe resultdocs,codecommit9f95f8ee/normalpushDRAFT1273+ownlivelap/T3082REVIEWe678remoteproof/cleanworktree. Hostedfullsmokes,parent/devmergePENDING;originalT2385openDIFFERS/rightsunchanged/flagresearchunadopted. No futurehostedacceptance/merge/imageacceptance,nolivecontentselected;earliermilestonegatependingtimepointimmutable.')
