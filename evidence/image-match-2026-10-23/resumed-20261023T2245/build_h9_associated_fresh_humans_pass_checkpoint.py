from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5112-stage14-watch/closed-H9-fresh-humans-PASS');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='9f6982fa9db28c1fef7c49f972369950a590a6e60ab52f3882b6e16362350b2d'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==8
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==118211
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix not in ['.pyc','.key','.p12','.pfx'];data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H9-associated-FRESH-human-fixtures-PASS-SYNTHETIC3c3f-NOT-H9-TREE',mod.author_manifest(root,manifest),'Exact8 closed H9-associated freshhuman proof payloads plus original manifest. All8ORIGINALfixturesbyte-reproduce,16GLBs bothviewports/46actorchecks each/finalOK onUbuntu24. ActualtestedPRmerge3c3fparentsH9+dev0c33/treee50f11dc,NOTpublicH9tree3bffd;independentAPIcompareonlyT3115entryfold+changelog.js changes,nohumanpathdelta. Rawsourceproof/logsretained. Two directlyexactH9stage14dispatches stillPENDING,NO currentH9budget/wholecoverage/mergeapproval/oldfailurerelabel. No livewatch/canonicalsource read,CIoperation orfixture/assertion refreshbyarchivist.')
