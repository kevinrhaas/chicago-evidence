from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-own-lap-f83-expiry-guard/closed-armed-waiting-snapshot');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='022bb1c5f17e8bd7d54edffe38979172abd6ab1aa570263b7a8080c4c25d63c1'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==8
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==17643
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-own-f83-lease-ARMED-WAITING-ZERO-CAS-SNAPSHOT',mod.author_manifest(root,manifest),'Exact8 closed operational readiness payloads plus original manifest. RootexplicitPREPARE+ARMauthorization,freshexactownf83owner/emptytree/zeroParents/date07:48:34,nativeHELDexit3/toolcf3strict3hours. Correctprimaryapp/workspace/primary-human-runner-compat/chicago/4d,NOToldforttmp. FrozenPID1501330/session7438/45sGETguard metadata only;earliestONEnormalCAS10:48:35requires sameown/openPR/nativeSTALE. ZERO CASatcapture,no stage14POST/force/release/manualtime/retry. Liveguard excluded,DONOTduplicate;futureoutcome needsseparatefinalreceipt. NoCI/source/mergeapproval oroperationalactionbyarchivist.')
