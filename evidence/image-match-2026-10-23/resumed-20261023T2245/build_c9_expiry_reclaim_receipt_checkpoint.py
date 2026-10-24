from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-own-lap-c9-expiry-guard/closed-final-receipt');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='7ee8a11326b6ae69c9c1afc789cf5cb591fe89926416d20e4de426526fd4e266'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==6
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==26066
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-own-c9-expiry-ONE-normal-CAS-f83-OPERATIONAL-PROOF',mod.author_manifest(root,manifest),'Exact6 closed normalownlapreclaimpayloads plus manifest. Exactownc9positivelySTALEafter07:48:32,ONEnormalCASexit0,newf83eef4a32a34ce0b3ccb68c859b310a87e82fe3timestamp07:48:34/expiry10:48:34. Independentowner-ref-time/HELDexit3/HEAD-index-toolequalityverified. Noforce/release/manualtime/retry/sourceCIchange;operationalproofONLY/futureownershiprequiresfreshread,no currentgate/merge/imageacceptance. No livewatchoutputsselectedandnooperationalactionbyarchivist.')
