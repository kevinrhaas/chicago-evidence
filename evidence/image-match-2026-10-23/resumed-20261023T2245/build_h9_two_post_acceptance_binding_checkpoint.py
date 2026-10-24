from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-H9-stage14-prepared/closed-H9-two-POST-acceptance-binding');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b28195a55846f515e505c2fab9e90e7b889de0dcd4bac32d45cf325de016b876'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==16
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==118696
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix not in ['.pyc','.key','.p12','.pfx'];data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H9-EXACT5112-TWO-POST-204-ACCEPTED-NOT-RESULTS',mod.author_manifest(root,manifest),'Exact16 closed H9dispatch/acceptancebinding payloads plus original manifest. ParentexplicitFINAL2POSTSNOWauthorization,HTTP204each;unchangednativedesktop14run40091268264/mobile14run40091276811. Independentlyboundhead5112aadaa97cdf3d42d057b3d4a29219f173666c/fulltree3bffd906/parents35f0+30ccareadback. Own1d653live,noreclaim. DISPATCHED_NOT_RESULTS ONLY:priorcandidateH8shadowPASS3955624/DA18/H7strictNOT H9acceptance. FrozenGETonlywatcherPID1590193/session7527bothinprogressmetadata,livewatcherexcluded/DONOTduplicate. No rerun/cancel/timeout/assertion/tierchange/TLSbypassorCIoperationbyarchivist;actualresultsowedseparate.')
