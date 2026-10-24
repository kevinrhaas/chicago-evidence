from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-dev67-native04-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='df728e933195e4e0953526fa30ee7e0bbf25a5217590fd6e8f8c5be489bd4905'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==20
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-dev67-ACTUAL-v3-native04-PASS-FULLPREFLIGHT-RUNNING',mod.author_manifest(root,manifest),'Exact20 closed current source/native files plus manifest. Normal67devmerge+exactv3source recovered bybinarypatchfrompublic6bf;native9phases/61writer2laps/alldatasetstaleness-sourceuse-closing-publishedchecksPASS.105records/210assets/all105inputs/26population-modelsguardsexact. Fullpreflight04RUNNING_NOT_RESULT,sourcepatchboundinitialdiffonly,no livegateoutputs. Actualv3browserNOTRUN(oldv2proofseparate/localrenameonly),newcompletehostedsmokespending,no codecommit. No currentfullgate/readiness/imageacceptance or borrowedbrowserproof.')
