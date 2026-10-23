from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
packages = [
    (
        Path('/tmp/chicago-next-model/T-2386-roof-relief-next-20261023'),
        'FINAL-HANDOFF-SHA256.json',
        'd52545aa4d76141429aa227ec9767673050dc3509578690bf1b9d53a24c8da9f',
        716,
        'WOLF-roof-relief-ACTUAL-DIFFERS-NOT-RECOMMENDED',
        'Wolf Point T2386: exact716 final closed files plus author manifest. Original405 historical prepared/unrun set retained separately from new306 actual run and final handoff. Actual roof-relief comparison DIFFERS; approximately40k triangles, NOT RECOMMENDED and UNADOPTED. No extra trial after grant or canonical application. Shared current82 integration must use the guarded baseline without this expensive experimental roof; no image match or rights promotion.'
    ),
    (
        Path('/tmp/log81-adoption-20261023T2250'),
        'MANIFEST.json',
        '443eeb5056015345e4dc497d78977afbd59385646de7037f62fa6e706ae5ce6b',
        154,
        'LOG82-baseline12KW-guarded-plan-UNBAKED',
        'T3081 engineering baseline12KW: exact154 closed files plus manifest at dev5f15. Five visible log-model improvements/current82-master scope, default/Hogan/source/Covers/provenance guards and authored patches. No official family bake, browser, whole gate, canonical write or image acceptance by this plan. Experimental Wolf roof relief excluded. This archive is the frozen plan, not the root live integration worktree.'
    ),
]
for root, filename, expected, count, name, note in packages:
    manifest = root / filename
    assert hashlib.sha256(manifest.read_bytes()).hexdigest() == expected
    author = json.loads(manifest.read_text())
    assert len(author['files']) == count
    for row in author['files']:
        path = root / row['path']
        assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
        assert not any(part in ['__pycache__', 'node_modules', '.git'] for part in path.parts)
        assert path.suffix != '.pyc'
        payload = path.read_bytes()
        assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], path
    receipt = mod.archive(name, mod.author_manifest(root, manifest), note)
    assert receipt['bytes'] < 50_000_000
print('Two closed exact archives built, full tar readback PASS; no live roots selected.')
