from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-published-qa-v2-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='4c9fb34a1e021d67beb2d8fef0c00a983f99f1d9ae7b9e70903269fa875d563c'
author=json.loads(manifest.read_text());assert len(author['files'])==11
assert sum(r['bytes'] for r in author['files'])==49296
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-published-QA-v2-LIGHT-PREPARED-NO-BROWSER',mod.author_manifest(root,manifest),'Exact11 closed LIGHT files plus manifest. QA v2 fixes linked-credit DOM counting and encodes explicit root decision that Cobweb Photos stays empty: Wau-Bun source is a book, panorama subject join unresolved, credited Sources and uncertainty retained. Syntax/dry/native-pure-data/staging only, zero browser/publish/Blender/fetch/full gate. Ten published cases and five source pairs remain not-executed batches; runtime bare PNG preserved. Original frozen19 unchanged/reverified. Staging-check and future run outputs excluded; no accepted match or actual QA claim.')
