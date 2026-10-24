from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-first9-smokes');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='adf01eab30236f2dcbfb34c9968f9c3dfd171bce4bcbca792a72ff6b4d7feb56'
author=json.loads(manifest.read_text());assert len(author['files'])==13 and sum(r['bytes'] for r in author['files'])==553580
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-first9of18-hosted-smokes-PASS-COVERAGE-PENDING',mod.author_manifest(root,manifest),'Exact13 closed hosted read-only files plus manifest. First9of18 actual smoke jobs bind exact6bf checkout/correct viewport/stage/SMOKEPASS/zero pageerrors,445checks0failed; nine raw logs,line evidence,original dispatch and02:12snapshot preserved. Other9jobs running at capture, full18coverage PENDING and no finalapproval. No new job/writer/heavy/merge/lap mutation by audit/archivist; no live monitor outputs selected.')
