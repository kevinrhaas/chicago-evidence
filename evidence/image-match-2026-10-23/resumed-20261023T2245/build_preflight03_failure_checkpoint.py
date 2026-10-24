from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-preflight03-failed-before-latest-dev');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='5c7d29cedd56eef0233d1ce23af760543501ca1ed1e7a0c7c92ec2733e8e42f5'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==14
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-fullpreflight03-ACTUAL-FAIL1-contractreader-exit1',mod.author_manifest(root,manifest),'Exact14 closed failed-preflight03 files plus manifest before normal latestdev merge retry. Actual1of1060 datasetFAIL with4contractreader errors:local meshpositionaliasp(count/getX/getY/getZ) confusedasplacement;sourceunchanged,durableexit1,changelog/IDsPASS. Wholebinarysourcepatch and own5path/docs-onlypatches retained,no codecommit. Localrenamev3proposal pending,validator unchanged. This failinggate is not approval;future normalabort8e/latestdevmerge requires its ownsourceguards/currentgate. No live output selected.')
