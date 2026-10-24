from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-dev6f-arrival-only-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8fb0286864eddb7e080b99f55bde24d176f19de8ce45e75267b752f7c13e6b51'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==14
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1165012
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-pinned6f-ACTUAL-arrival-CAP-PASS-OVERALL-FAIL-CDP-EVICTION',mod.author_manifest(root,manifest),'Exact14 closed actualpinned6farrival files plus manifest. NativecapPASS4590174triangles,margin9826;OVERALLFAILexit1retainedforadded44.8MBGlessnerresponse.bodyinspectorcacheeviction,notHTTP/loaderfailure. ActualKimball/ColemanbodyhashPASS,Glessneroriginalbodyunavailable. Independent109source+mirrorpre/postbindexactPASS,allprocessesclosed/rootCLEAR. Finalclosedgate05receiptcopiedonlyafterclosure. No rerun/publish/manualstands/futureH4sourceclaim or releasegatewaiver;failureandlimitsretained,nofullstage/hostedsmoke/readiness/imageacceptance. No livecontentselected.')
