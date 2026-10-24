from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-H7-humans-watch/closed-H7-strict-humans-PASS');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b18a55fde9c9ede284531992011d6406b534b171b2ae4e8f9cbeb578a9514414'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==12
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==134559
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H7-ACTUAL-original-eight-human-fixtures-STRICT-PASS',mod.author_manifest(root,manifest),'Exact 12 closed H7 strict human proof payloads plus original manifest. Actual run 40081409169/job120835576800 checks exact18f7 on Ubuntu24.04.5: all8 ORIGINAL fixture files byte-reproduce,16GLBs open in both viewports,46actor checks per viewport and finalOK. IndependentGit proof whole4d tree66a68bd7 DA-to-H7 EXACT;only outside4d human runner pin changed. OriginalDA humansFAIL preserved;no cause inferred,retry,fixture/assertion refresh or asset replacement. Observer GET-only. DA staged17of18/desktop13 pending,no fullcoverage or mergeapproval. No live outputs selected.')
