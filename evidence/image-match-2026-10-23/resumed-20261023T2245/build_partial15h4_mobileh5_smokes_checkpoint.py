from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5d9d4464-watch/closed-partial-15H4-plus-mobileH5');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c2ae3600d48b1cdf9fce1fd59c8913a6ac1e050c3e31393326d43acbcc4b3bf1'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==43
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1106883
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-mixed-H4-15PASS-H5mobile12-PASS-PARTIAL-SOURCE-PARITY',mod.author_manifest(root,manifest),'Exact43 closed partialmixedsourcehostedproofpayloads plus manifest.15H4groupsverifiedPASS+H5mobile1-2actualUbuntu24.04.5PASS194/0,identical4dtreebc25fa. OldtwoH4setupFAILremainFAILED;H4desktop13/H5desktop1-2PENDING. Raw15PASS/2FAILH4logs/jobs+H5mobilelog/job/sourceparityretained. Desktop14actualCI4590174trianglesunderunchanged4600000limit. PARTIALnot18of18H4PASS/finalapproval/currentconsolidatedsourcevalidation;nolivejobsoroldresultsrelabeled,noarchivistmutation.')
