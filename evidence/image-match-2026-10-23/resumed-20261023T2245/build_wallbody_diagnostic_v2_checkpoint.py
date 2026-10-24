from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-wall-body-diagnostic-proposal-v2');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='57cfda0dce707763ab67f091b7b5e4a99052c6f964c264a04da1f376963fdeba'
author=json.loads(manifest.read_text());assert len(author['files'])==25 and sum(r['bytes'] for r in author['files'])==3108008
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-wall-body-diagnostic-v2-PROPOSAL-UNAPPLIED-38CPU',mod.author_manifest(root,manifest),'Exact25 closed v2 proposal files plus manifest,v1immutable. Independent callerfilter finding retained:declaredsign withmissingwall could be dropped;v2twoauthoredlines requirefinitepositivewall ORdeclaredAppendage.38CPUcontrolsPASS includingrealcandidatepredicate missing,string2.6,false,NaN,Infinity. Same3pathbodydiagnostic UNAPPLIED;noheavy/canonical/liveQA/actualbrowser/native/fullgate. No actualbrowser proof borrowed from earliermodel QA;parent adoption separatelyowned. Measurementcaps remain diagnostic,not assetproduction geometry.')
