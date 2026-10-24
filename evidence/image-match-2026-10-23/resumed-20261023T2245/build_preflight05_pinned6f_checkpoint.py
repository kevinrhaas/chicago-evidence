from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/workspace/T3081-preflight05-pinned6f-closed','a4e748fc37c458e688f28201b21d0577416d4194c148beaaadd3bf8f5d353a05',25,7529371,'T3081-pinned6f-fullpreflight05-ACTUAL1062-PASS-NOT-SMOKES','Exact25 closed fullpreflight05 files plus manifest. Actual1062checks/383selftestsPASS,scientificreadersrequired/sourceunchanged,native9phasesPASS,105records/210assets exact. Wholeownedbinary/sourcepatchagainstpublicincoming6f/exactstagedtreebinding included;duplicateincoming120MBGlessnerpackage excluded. FullpreflightproofNOThostedsmokeacceptance;finalcanonicalarrivalrunsseparate/liveexcluded. No currentarrival/hostedsmoke/readiness/imageacceptance andno furthercleanup.'),('/tmp/PR1260-dev6f-arrival-only-prepared-20261024','a5f3f4ab840aecfff18b55bf00529892c3d401c1e5599881dc055bed595482dd',3,18068,'PR1260-pinned6f-conditional-arrival-helper-PREPARED-ONLY','Exact3 closed preparedhelper files plus manifest. Syntax/dryonly,conditionalonparentgate05PASS+unchangedtrue+closedprocesses. Exactnativearrivalwithno4stands/nopublish/sourcechanges,strictnativecaps+3HTTPbodyhashes. Livewaiter/actualarrivaloutputsseparate/unselected,no actualresult/hostedsmoke/readiness/imageacceptanceclaim.')]
for directory,expected,count,total,name,note in packets:
 root=Path(directory);manifest=root/'MANIFEST.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==count
 if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
 assert sum(r['bytes'] for r in rows)==total
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 mod.archive(name,mod.author_manifest(root,manifest),note)
