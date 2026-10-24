from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-full-preflight04-public4606-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='3285cc6b85452cf4deaf53a6285a9016ed3c0693cb81b25b859498f9f91de60f'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==19
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-fullpreflight04-ACTUAL1061-PASS-public4606-DEV60-PENDING',mod.author_manifest(root,manifest),'Exact19 closed testedsource/fullgate files plus manifest. Actual1061checks/383selftestsPASSexit0,scientificreadersrequired,sourceunchanged;normalpublicmergecommit460622123de7ec66c22c0d080309664ede498f50,FFpush/freshPRheadbinding/postcommitCL-IDchecksPASS. Onlytwo resultdocumentationparagraphs addedaftergate. TransientcachedoldPRresponse retained with authoritativefreshbinding. Latestdev60reconciliation/completeupdatedheadsmokesPENDING atcapture;no futuremerge/currentheadinheritance/readiness/imageacceptance. Ongoingdev60merge/livegateoutputs excluded,oldfailurepacketsunchanged.')
