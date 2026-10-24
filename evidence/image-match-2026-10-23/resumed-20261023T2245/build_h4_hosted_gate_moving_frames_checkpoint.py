from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5d9d4464-watch/closed-hosted-gate-and-moving-frames');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8bd5c86e938b499fdfeefa8ace5fb29ce0a0e3a3f923688913c895fc5d3ea1da'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==5
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1952061
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H4-ACTUAL-hosted1062-and-movingframes-PASS-SMOKES-PARTIAL',mod.author_manifest(root,manifest),'Exact5 closed actualhostedproofpayloads plus manifest. Rawbothjobscheckoutmerge857db5fad0e354248c9eca7ce37a1929ef5b2a49=exact5dH4head+29eadev. Gate1062checks/383selftestsPASSwithT3081changelog,movingframesPASS. Separatesmokespartial/setupfailed1-2notexercised,NO fullcoverage/waiver/approval orborrowedlocal/oldheadproof. Captureresumedafterspace restored,nolivejob/canonicaltreeselected;no mutations/dispatch/heavybyarchivist.')
