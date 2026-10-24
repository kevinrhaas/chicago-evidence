from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head-da65119-watch/closed-final18-DA-staged-smokes');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='f5545c78becee1b2177d127a8a07bb7bb65070669c88d7dbfc140960c2bd9422'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==45
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1251514
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-da65119-FINAL18-ACTUAL-staged-SMOKE-PASS-EXACT-HEAD',mod.author_manifest(root,manifest),'Exact45 closed FINAL DA staged-smoke payloads plus original manifest. All18 exactda65119logs/jobs cover all15parts across both viewports, zeroerrors/completebodies;829desktop+836mobile checksPASS/zeroFAIL. Lastdesktop13actual160/0finished09:48/body130m56s. Hosted1063/383+movingabf3 separate;DAhumanFAILd0e63 and laterH7strictPASS/sourceparityb18 remain distinct,NEVERrelabeled. Parent-reportednewpinned38e7dev3assets/globalCLdata change still owes native/fullgate/fresh1904validation,NO currentdev/newhead/mergeapproval. Observer stoppedcleanly,no18reruns/cancel/dispatchbywatcher/archivist;old partialtimepointsimmutable,noliveoutputsselected.')
