from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T3041-whistler-identity-20261024');manifest=root/'RECEIPTS.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='68e375bb280ae5767e3a7774d134fe5d9722a0b691b21a1a04229bd96be0d731'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==9
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3041-Whistler-front-identities-LIGHT-PROPOSED-UNAPPLIED',mod.author_manifest(root,manifest),'Exact9 closed LIGHT source-identity files plus verifiedRECEIPTS.json manifest. Fivewhole-front pictured-ruling proposals justified from actualuncroppedWhistler sheet/crops andQuaife notes;other25gradesunchanged. Historical numberingerrata retainedseparately,no record/geometry reassignment. Proposed native rulings UNAPPLIED;no canonical adoption/camera/render/heavy work or image-match acceptance. No live rootpreflight03/QAcontentselected.')
