from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-next-head-watch/closed-controller-readiness');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='58a4b36eb53ae52ba6cc01bf9796518e3b91a700566df3dea3f4f46cd8d74603'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==2
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==9995
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-next-head-18run-readonly-controller-PREPARED-NOT-INVOKED',mod.author_manifest(root,manifest),'Exact2 closed prepared watcher files plus manifest. Parameterizedexacthead/18runreadonlycontroller requiresactualacceptedreceiptbindingsbeforeGETs,preservesfailedrawlogs,separatesmetadatafromtranscriptsuccess. ASTsyntaxvalidationonly,no newheadinvocation/poll/dispatch/result atcapture. Awaitsfutureactualbinding,no gate/currenthead/readiness/imageacceptance andno livejobselection.')
