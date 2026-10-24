from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-H9-final-native-preflight-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='6d035f678b51f20096bb3e8c5ef354fc5dce2a2aa6bc7406afd1f90ba4b1b9b9'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==35
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==7615650
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix not in ['.pyc','.key','.p12','.pfx'];data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-PUBLIC-H9-EXACT5112-native10-fullgate1064-PASS-HOSTED14-PENDING',mod.author_manifest(root,manifest),'Exact35 closed priority H9actualnative/fullgate payloads plus original manifest. Public5112aadaa97cdf3d42d057b3d4a29219f173666c/whole3bffd906EXACTtested1064checks384selftestsPASS,includesincoming30cca1736/Glessnercross. All105recipesfresh,105records210assetsexactH8,all26populationsame,allotherregistryrows incomingexact. Native10PASS;actualcanonicalnewtestisolation measured,32/0harness36/0selftest/auditPASS. Publiccode/PRbodyupdated,hosted14runs40091268264/40091276811DISPATCHED_NOT_RESULTS. Prior3955624shadowproofH8datasetNOTcurrent30FullPASS;localPhotosFAIL36NSSEROFS/independent35strictGETPASS bothpreserved. No freshhosted/currentbudget/merge/imageapproval orlivewatchsourceharvesting.')
