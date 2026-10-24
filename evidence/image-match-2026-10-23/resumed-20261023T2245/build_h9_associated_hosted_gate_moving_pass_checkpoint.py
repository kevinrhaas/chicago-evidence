from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5112-stage14-watch/closed-H9-hosted-gate-and-moving-PASS');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='1d9118d59af8eb6c94eaaf33f4942c9892f156cacb768e5af0a491874111c027'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==11
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==2002343
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix not in ['.pyc','.key','.p12','.pfx'];data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H9-associated-hosted1064-moving32-PASS-SYNTHETIC3c3f',mod.author_manifest(root,manifest),'Exact11 closed actual H9-associated hostedgate/moving payloads plus original manifest. Rawgate1064checks384selftestsPASS,movingeveryframeceiling+32uploadreleasePASS. Actualcheckout3c3f/treee50fparentsH9+dev0c33,independenttwochangelogfold-onlycomparisonretained,NOTsamewholeH9tree3bffd. ExactH9mobilePASSa6b20dseparate,desktop14PENDING/no currentFullbudget/mergeapproval. OldFAIL/candidateproofsdistinct,GET-onlyrawcapture/noretryPOST/edits/bypassorlivewatchharvestingbyarchivist.')
