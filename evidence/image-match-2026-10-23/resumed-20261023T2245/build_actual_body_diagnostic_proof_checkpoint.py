from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-body-diagnostic-live-proof');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='a3422a8406ae0326f56105603b441b39e0fc233e6aa6051464d05dfc130f7329'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==28
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==5199031
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-ACTUAL-body-diagnostic-PASS-optional1904-PROBE-FAIL-ABORT',mod.author_manifest(root,manifest),'Exact28 closed focused actual proof files plus manifest. Mobile/desktop storedquantized/CDP full/body proofsPASS(11.022312/5.401596m),19clonedcontrols each,exact14notices,zeropage/request/CDP/cleanup errors. Independent v1controls18/v2controls38 rerun reports,adopted3sourcehashes/snapshots/actualsamples retained. OPTIONAL1904probe actual5113calls/4599770triangles withinunchanged4600000by230,BUT overallFAIL/orchestratorexit1 retained due one unfilteredpeople.jsonERR_ABORTED;page/HTTP/cleanup0. No filtering/rerun/source edits,unknownaborttiming explained;3PNGs viewed. NOTfullstage3-4/14PASS/fullgate/imageacceptance. Live rootpreflight03 wholly excluded.')
