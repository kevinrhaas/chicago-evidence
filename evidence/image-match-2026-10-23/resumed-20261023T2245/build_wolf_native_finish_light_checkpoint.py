from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T-2386-native-roof-finish-next-20261023')
manifest=root/'ARTIFACTS.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='2765f0b2108923881dd79aa73be544a170546c0d04d8f75468d2d8dbfd32865b'
author=json.loads(manifest.read_text());assert len(author['files'])==223
assert sum(r['bytes'] for r in author['files'])==5916698
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('WOLF-future-native-roof-finish-LIGHT-UNRENDERED-UNADOPTED',mod.author_manifest(root,manifest),'Exact223 frozen LIGHT files plus author manifest: future data-only darkened stock finish and native-relief binding study, current82 pure geometry/default/material guards and frozen prior actual-before comparison inputs. No new render, official/native/heavy run, T3081 scope growth or canonical change. UNRENDERED/UNADOPTED; prior approximately40k-triangle roof experiment remains rejected. No original image-match acceptance.')
