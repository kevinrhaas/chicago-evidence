from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-final5d9-native-QA-closed-20261024T0650');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='98e01a6a28aa8972ce5f14017809dcd3096d8a17af03d5c6633c3e8da152ffcc'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==137
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==30021377
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-final5d9-ACTUAL-native13-four-appcases-photo-DIFFERS-GATE-PENDING',mod.author_manifest(root,manifest),'Exact137 closed final5d9 milestonepayloads plus manifest. Exactmigration/native13phasesPASS,fouractualappcases,oneactualphotorender/directmanualDIFFERSreview;failedV2/repairedV3retained,ownedcurrentsource/native delta included. Livefullpreflightexcluded/PENDING;UNCOMMITTED/PR/hostedsmokespending. OriginalT2385open/DIFFERS,flagresearchunadopted,rights unchanged,noimageacceptance/currentwholegate/readinessinheritance. Allselectedsourcepayloadsfrozen,no live tree/oldheldcache/fullmirror read.')
