from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-own-lap-expiry-reclaim/closed-reclaim-receipt-v2');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='bfc18232a5fe938f93ca4a6f352ff12ff97053794af32a991ffa966907388cdd'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==8
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==21943
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-own-lap-normal-expiry-reclaim-OPERATIONAL-RECEIPT',mod.author_manifest(root,manifest),'Exact8 closed operational receipt files plus manifest. Rootexplicitlyauthorized normalexpired ownmarker4a988ee6reclaim;nativeSTALEexit0/independentoldSHAreadthenONE normal lap1260exit0. Newmarkerc9ad654ec0375de3ff48928bf99f266739916917committed04:48:31/expires07:48:31UTC,independentREST/nativeHELDexit3verified. HEAD460622/index/toolhashesunchanged. Noforce/release/manualtimestamp/retry/sourcewrite/smoke/heavy/cancel/merge. Datedoperationalstate only,futureownership requires freshread;no gate/readiness/imageacceptance.')
