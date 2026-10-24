from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-dev6f-glessner-separate-get-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c048af1b3cbbd457d70771429f3c3265611d7681056b1fcec2ac82e5a44a1154'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==5
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==11914
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-pinned6f-Glessner-SEPARATE-GET-PASS-NOT-RECOVERED-INSPECTOR',mod.author_manifest(root,manifest),'Exact5 closed LIGHT separateGET files plus manifest. NEWserver/request,exactoriginalstatichandler/samepublishedpath,streamedGET200/44825956B/SHA256d1f66c6fc791034e6aa25e2dba2ad220a62592a0bff4bf9346a51b23c2876925. Sourceasset/mirror/handlerpre-postexact,serverclosed,nobrowser/sourcewrite/publish. Original8fbinspectoroverallFAIL/bodyunavailableunchangedUNRECOVERED;separateGETdoesNOTconvertoriginalPASS/nofullstage/hostedsmoke/readiness/imageacceptance. No livecontentselected.')
