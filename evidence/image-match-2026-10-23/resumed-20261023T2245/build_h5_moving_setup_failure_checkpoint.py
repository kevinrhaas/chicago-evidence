from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-H5-replacements-watch/closed-H5-moving-frames-setup-failure');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='cb71fa0a231c266f50e52a80255639e45cf773ad21b095a376fb371ef4f237cc'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==7
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==27289
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H5-movingframes-ACTUAL-SETUP-FAIL-BEFORE-MEASUREMENTS',mod.author_manifest(root,manifest),'Exact7 closed H5movingframe setupfailurefiles plus manifest. Actualjob120806725950Ubuntu26/Playwright1.56.1incompatibilitybeforemeasurements;merge262bc859bindsH5+29ea. Source4dH4=H5treebc25faexactbutfailedresultNOTrelabeled. CapturedH5replacements/automaticwholesmokepending,separatemovingworkflowrunner/installlocationsretained. No retry/source/job/lap/merge mutationbyobserver/archivist;no fullcoverage/waiver/approvalandnoliveharvesting.')
