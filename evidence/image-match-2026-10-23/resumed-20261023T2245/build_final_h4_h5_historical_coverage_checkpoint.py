from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head5d9d4464-watch/closed-final16H4-plus2H5-source-equivalent-coverage');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='e1ddef54a8cc2251fafff6fb8088a17c4fd79cd276ea4f7006803a747819b0bf'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==59
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1432145
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-HISTORICAL-final16H4-plus2H5-source-equivalent-COVERAGE',mod.author_manifest(root,manifest),'Exact59 closed historicalcoveragepayloads plus manifest. OldH4desktop13actualPASS160/0zeroerrors08:25:58,finalH4matrix16PASS+2PRESERVEDUbuntu26setupFAIL(attempt1+2/oneauthorizedreruneachretained),NEVER18of18H4PASS. TwoH5replacements194/0withEXACTbc25identical4dtreecomplete15partsby2viewportsas16H4+2H5sourceequivalentcoverage. CanceledH5autono coverage;consolidatedda65119DIFFERENTruntimeNOINHERITANCE. Newda651observerseparate16PASS/desktop13+14pendingatcapture,no finalcurrentheadapproval. No mutations/livewatchorcanonicalsourceharvesting.')
