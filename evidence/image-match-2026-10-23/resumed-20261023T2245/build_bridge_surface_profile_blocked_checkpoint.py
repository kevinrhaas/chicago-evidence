from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T-2375-native-surface-profile');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='20125984f22fd5b70cc98db09b516acb4e20de4d84aba127244e3b0808ec97cc'
author=json.loads(manifest.read_text());rows=author if isinstance(author,list) else author['files'];assert len(rows)==52
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T2375-native-surface-profile-PROPOSAL-FULL-ADOPTION-BLOCKED',mod.author_manifest(root,manifest),'Exact52 frozen source proposal files plus manifest. FULLADOPTIONBLOCKED byactuallegacyfallback/whole-yardextentcounterexample;coherentsampler/nativecamera-travel controls only. No canonical/nativepage/bake/fullgate/imageacceptance. Futurev2blockerrepair is separate/live andexcluded. Rootlatest67native04live alsoexcluded;no borrowingfocusedcontractPASSor futurefullgateproof.')
