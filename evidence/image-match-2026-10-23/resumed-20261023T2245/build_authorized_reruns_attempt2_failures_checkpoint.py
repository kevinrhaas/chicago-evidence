from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5d9d4464-watch/closed-authorized-reruns-and-attempt2-failures');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='de687cd85d01e55aabead1b98f46b39ec3412cb143970ecc9b18db373c176eae'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==14
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==154144
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H4-one-authorized-rerun-each-ATTEMPT2-SETUP-FAIL',mod.author_manifest(root,manifest),'Exact14 closed rerun/failure/recoverypayloads plus manifest. ExactlyONErootauthorizedPOST201perfailedrunafteroriginalprooffrozen. Attempt2jobs120804563764/120804571055bothactualUbuntu26.04.1/image26samePlaywright1.56.1installFAIL,smokebodyNEVERSTARTED. Exactworkflowlines39/60-61retained,nofurtherretry/code/assertionchange. LocalENOSPCcapturefragments preserved;GETonlyobserverrestartedafterpublisherrelocation,noPOSTrepeated. SetupfailureproofNOTfullsmokePASS/currentapproval/imageacceptance,nolivejobselection.')
