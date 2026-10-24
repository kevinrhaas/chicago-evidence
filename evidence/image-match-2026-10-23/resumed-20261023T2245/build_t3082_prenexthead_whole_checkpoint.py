from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-pre-nexthead-whole-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='fc80fd04948b5193778257d38597d25daf9b949bdb619e263c387048c7dad5b0'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==76
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==17457919
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-PRE-NEXTHEAD-WHOLE-recovery-NATIVE-PASS-BROWSER-GATES-PENDING',mod.author_manifest(root,manifest),'Exact76 closed futuremigration recovery files plus manifest. Wholeownedsource/docs/native5outputs/wording/oneentry,46genuineframeexports/registries/full diff/oldrefs,actualproducerbindings/nativereceipts. Current6bf native13phasePASS,browser/fullgatesPENDING;future root target not yet public atcapture,no mutable root read/migration/claim/merge/heavy. Heldcache/fullmirror excluded,inherited82logsalreadycommitted6bfwithpriorproofs. OriginalT2385DIFFERS/open,rightsunchanged,flagunadopted. Recovery requires remoteproof beforefutureclearing,no futurehead/gateinheritance/acceptance.')
