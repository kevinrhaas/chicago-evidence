from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-claim-expiry-watch-20261024T0545');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='500840cda61a91bef827db1c7f59f3420229053e0f5b52bf8e31c059e7d0d305'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==7
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==12599
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-scheduled-own-expired-claim-CAS-OPERATIONAL-COMPLETE',mod.author_manifest(root,manifest),'Exact7 closed operational files plus manifest. Actualnativeexpirywait/freshEXACToriginalowner-at-runcheck,normalCASclaimexit005:45:30.526Z;noforce/manualtimestamp/changedholdertakeover. Independentremotepull/marker/ancestryreadbackPASS e22553d21bd9811943af17d1e1b71e70c44e2464,newexpiry08:45:30.526Z. Source/head/futuremigrationtargetunchangedNULL,noheavy/publish/PR. Datedoperationalproof,futureownershiprequiresfreshread;no source/gate/readiness/imageacceptance andno livefilesselected.')
