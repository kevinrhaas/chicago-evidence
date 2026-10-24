from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-aabb-v2-actual-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='f7c9a2ae0b50f194dd65c5d529bb6172f4083647866a4f7d13045ce2c7272b2c'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==46
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==9192233
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-AABB-v2-ACTUAL-primary-spawn-PASS-LEFT-APPLIED',mod.author_manifest(root,manifest),'Exact46 closed actualAABBv2payloads plus manifest,includingverbatimfrozen981eproposal18+manifest andimmutablec297baselinehashrefs. PrimaryspawnPASS4589658triangles versus4600000cap,margin10342;raw5097calls/319,cumulativeboxRejected106.43focusedchecks+5directPNGpairs;exactapprovedtwo-pathLEFTAPPLIED/allprocessesclosedCLEAR. BaselinethreesupplementaltriangleFAIL/rawpeopleERR_ABORTED-nativepolicyretained;pixelnonidentity/twohigher singlesubmit timings explicit,nohardwareperformanceverdict. No fullstage/fullgate/imageacceptance,future rootpreflight05 excluded. Originalrejected2m/baselineevidenceunchanged.')
