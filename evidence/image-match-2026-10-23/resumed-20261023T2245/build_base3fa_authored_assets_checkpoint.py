from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-base3fa-authored-assets-checkpoint-20261024T0025');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='26b2d65cb0dbd804dd2f3ce20abac9c521e65c23a4b82064e37bf860fd195329'
author=json.loads(manifest.read_text());assert len(author['files'])==69
for rel,row in author['files'].items():
    path=root/rel
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-base3fa-authored-assets-recovery-NATIVE-STALE-PREFLIGHT-CANCELLED',mod.author_manifest(root,manifest),'Exact69 closed files plus verbatim manifest: all18 actual graft source files, corrected exact-phase consumer/STATUS,11 actual asset deltas, native82 rows, transfer script/receipt, guarded migration and cancellation reasons/logs. First native60-step2-lap tail completed, but later model build left2SC metadata stale. Preflight CANCELLED143, not PASS. New compile_scene/native tail still running at capture and EXCLUDED; native outputs not claimed current. Recovery requires correct model-before-scene order and native/fullgate validation. No live tree or current readiness/browser/image-match claim.')
