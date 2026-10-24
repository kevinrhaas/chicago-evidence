from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-cells-ab-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c297a0fcff6e013f854160e6f7538374732a84d6cf0b5091ce699f26aceeda36'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==66
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==22313902
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-ACTUAL-Full-Glessner-cells-AB-2m-REJECTED-4m-RESTORED',mod.author_manifest(root,manifest),'Exact66 closed actualA/B payloads plus manifest,includingverbatimoriginal8e405proposal. Actual2mspawn4601506stillover4600000by1506,REJECTED. Exact4mcanonical/mirror94a263restored/normalpublish+readonlyPASS,allprocessesstoppedCLEAR. Threeobserveronlyfailedattempts/nativepeopleERR_ABORTEDclassificationunderexistingsmoke,eightfinalobserverauditsexact,originalthreesupplementaltriangleoverrunsretained. No cap/quality/asset/tolerancewaiver orimageacceptance/fullstagePASS;future root fixseparate,no livefolder selected.')
