from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-published-qa-v3-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='1476173078bfdacf6643d51aba2daaf80b2936cd25f557bdc98773f17f5909de'
author=json.loads(manifest.read_text());assert len(author['files'])==8 and sum(r['bytes'] for r in author['files'])==37736
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-published-QA-v3-Cobweb-fixture-PREPARED-NO-BROWSER',mod.author_manifest(root,manifest),'Exact8 closed LIGHT files plus manifest. PREPARED_NOT_BROWSER_EXECUTED: single Cobweb authored-record fixture hash updated for adopted reconstructed5.05m head; source/claim metadata only, no actual asset measurement. Harness/staging/preservation modules byte-identicalv2, run sequence points v3 fixture; other4records and doorway/camera/sourcecredits/assertions unchanged. Syntax/all5guarded dry only. No browser/publish/Blender/fetch/fullgate/inflightasset read/canonical write; v1/v2 untouched; future actual runs excluded.')
