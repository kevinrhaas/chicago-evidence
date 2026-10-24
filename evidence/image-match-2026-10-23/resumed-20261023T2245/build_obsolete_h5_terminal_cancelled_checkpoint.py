from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-H5-replacements-watch/closed-obsolete-automatic-push-cancelled');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='3f87216eec01a18396e2c87bd73fc40663459ee7737d57f24a610494665fca9d'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==5
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==159816
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-obsolete-H5-auto-smoke-TERMINAL-CANCELLED-PARTIAL-LOG',mod.author_manifest(root,manifest),'Exact5 closed terminalfollowuppayloads plus manifest. ActualobsoleteH5pushrun40071825677CANCELLED07:42:32,exactH5partialrawlog145952Bretained,nofinalassertioncounts/SMOKEPASS. Supersededbyda65119reasonbound,distinctfromreplacementPASS/runtimeFAIL. EarlieronePOST202accepted/in_progressreceiptremainsfrozenhistorical;thisisread-onlyterminalfollowupnotnewcancel/retry/dispatch. No currentheadcoverage/approval/imageacceptance,noliveoutputsselected.')
