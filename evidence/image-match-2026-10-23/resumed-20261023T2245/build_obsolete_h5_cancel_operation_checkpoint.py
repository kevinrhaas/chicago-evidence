from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-obsolete-H5-auto-cancel/closed-operation');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='69c6093eb10cbb58743e9ee55008c69dd8bb314a2888b7408dc9d3408c1c6b24'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==6 and sum(r['bytes'] for r in rows)==35445
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-obsolete-H5-auto-smoke-ONE-CANCEL-ACCEPTED-NOT-TERMINAL',mod.author_manifest(root,manifest),'Exact6 closed operationalcancelproofpayloads plus manifest. ONEnormalauthorizedCANCELobsoleteH5automaticpushsmoke40071825677only;freshhead6024/eventpush/pathchecked,metadata/jobs/runninglogGETpreservedBEFOREPOST. OneAPI202accepted,immediatereadbackstillin_progress,NOTterminalcancelclaim. No oldH4desktop13/newda651cancel/retry/dispatch. Separateda651watcheractive/oldresultshistorical,nocurrentsmokegate/approval. Archiverperformsnomutationandselectsnolivewatchoutputs.')
