from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-gate-and-first3-smokes');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='0121c550d7a941a9339dbfac1221329fa7cdc6c07c045d2ebac6d680d965a191'
author=json.loads(manifest.read_text());assert len(author['files'])==7 and sum(r['bytes'] for r in author['files'])==2025187
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-hosted1060-PASS-first3of18-mobile-smokes-PARTIAL',mod.author_manifest(root,manifest),'Exact7 closed read-only hosted proof files plus manifest. Actual1060/383 gatePASS binds mergeca5a27aa2=6bf+026ace. Mobile stage15,9-12,8 jobs checkout exact6bf, SMOKEPASS34/69/21 with zero page errors. Snapshot only3of18PASS,12running/3queued, not wholecoverage/finalapproval. No job dispatch/writer/heavy/merge/lap mutation by monitoring/archivist; no live job outputs selected.')
