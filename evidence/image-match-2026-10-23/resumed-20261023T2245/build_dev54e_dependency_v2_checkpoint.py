from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-dev54e-105recipe-210asset-review-v2');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='6ce57107aa58cb61e947885a1a507064af89d19951c8901ebe5051b79765f065'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==4
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==742992
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-dev54e-105recipe210asset-bounded-review-NOT-CAMERA-PASS',mod.author_manifest(root,manifest),'Exact4 closed read-only dependency/count files plus manifest.105record/recipe/masterwebregistryrows and210existingGLBblobsexact8e-to54,1911dependenciesguarded;onlyK01params/wallgable,changelog,incomingcheck/isolation/newK01test differ. Root addsNOcheck/isolationregistrations,explicitcorrectionofearlierunpublishedabb48speculation. ActualnewColeman+44/FirstPresby+86master/webtriangles(+130combined),new54blobhashesverified;NOTnewcameraPASS/freshgate/waiver. No fetch/source/job/lap/merge mutation or heavy work.')
