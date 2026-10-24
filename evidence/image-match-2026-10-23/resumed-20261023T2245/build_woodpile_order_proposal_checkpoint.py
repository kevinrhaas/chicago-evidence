from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-woodpile-native-proposal');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='183116da4adbef5c24477b7e11c250843d00566940597ff6a81364a06e8dc902'
author=json.loads(manifest.read_text());assert len(author['files'])==11 and sum(r['bytes'] for r in author['files'])==1102562
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-native202-woodpile-order-3path-proposal-UNAPPLIED',mod.author_manifest(root,manifest),'Exact11 closed proposal files plus manifest,3authored paths only. UNAPPLIED at capture: native manifest202 adds bare woodpile writer step180 after outbuildings and before keptground; inventory manifest preserves historical measurement and one ordering assertion. README binds dependency/report-only-field analysis. No native execution/test/canonical edit by proposal; root actual adoption/check/61-step ordered tail belongs separately. No browser/fullgate/readiness/image-match claim.')
