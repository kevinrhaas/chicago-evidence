from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-dev60-105recipe-210asset-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='a75e46fbcc8ed9442f5a4f99626f36b55ba9a8bfd2952caa97ac5a15ba7dc8c3'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==4
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==717804
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-dev60-bounded-drift-WHEELER-plus984-NOT-CAMERA-RESULT',mod.author_manifest(root,manifest),'Exact4 closed read-only drift/count files plus manifest.105ownrecords/registryrecipes+210existingGLBsexact67-to60;2390dependenciesonlyK01params/shapedgable/changelogchanged,allsharedlog/frame/renderer/smoke/nativewriter/check/isolationexact. ActualWheeler20027to21011(+984)master/web,new60blobhashverified. Prior100arithmeticmarginwouldovershoot884 IFsinglevisiblecontribution,NOTactualcameraFAIL/PASS orbudgetwaiver. No fetch/source/job/lap/merge mutation/heavy/gate;currentheadvalidation stillrequired.')
