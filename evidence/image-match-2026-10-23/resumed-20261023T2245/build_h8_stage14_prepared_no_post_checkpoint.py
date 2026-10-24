from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-H8-stage14-prepared/closed-prepared-no-POST');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b8058b9348a6857a54e7e461929d12c04db811687dccfd997ae66dd9f489f9e3'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==10
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==21344
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H8-stage14-controller-PREPARED-NO-POST-NO-HEAD',mod.author_manifest(root,manifest),'Exact10 closed controller/dispatch readiness payloads plus original manifest. No H8hash yet,NO POST/runbinding/watcherexecution. Two exactnative stage14 payloads require parent finalhash+authorization, exclusivePOST sentinels and separateGETonly2run watcher withALLchecks. Fresh09:59GET-onlylease sees ownf83expiry10:48:34,notstale,reclaimNOTARMED;explicitparentfollowupAFTERexpiryrequired. Readiness only,neverCI/PASS/sourceapproval. No operational/CI/source mutation byarchivist,earlieractualDAresultsseparate,nolivecanonicalwatchoutputsselected.')
