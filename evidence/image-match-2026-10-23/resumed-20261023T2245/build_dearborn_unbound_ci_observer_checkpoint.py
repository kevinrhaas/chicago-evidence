from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/T3126-unbound-CI-observer-prepared')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '571ae778c0a46b7c1595fd8c3a77df22a7a07d13cbd29bae7858fe1550672922'
x = json.loads(p.read_text())
assert x['status'] == 'UNBOUND_UNRUN' and len(x['files']) == 6
assert sum(z['bytes'] for z in x['files']) == 30022
for z in x['files']:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'T3126-CI-OBSERVERS-PREPARED-UNBOUND-UNRUN-NO-DISPATCH'
note = ('Exact six closed files plus original manifest. Workspace-only prepared staged/ordinary observers, AST parse only. '
        'Captured actual incoming305 workflow f0f6c6f5 retains manual viewport/stage/native--published/Ubuntu24/150m inputs; '
        'dev-only push workflow-edit automatic trigger preserved. All18 planned legs have null run IDs and accepted=false. '
        'No final PR/public source SHA/tree/API/POST/process/native/test/render/install; no observers started or dispatch. '
        'No old1282/1283 results reused; FAR Fly budget context is not PASS or waiver. Original Dearborn OPEN/DIFFERS.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- T3126 CI observer preparation is saved as **UNBOUND and UNRUN**: six closed files plus manifest, with '
            'workspace-only staged and ordinary observers checked by AST parsing only. The captured incoming305 workflow '
            'retains its manual viewport/stage/native --published inputs, Ubuntu24 runner and 150-minute limit; the dev-only '
            'push workflow-edit trigger is preserved. All 18 planned legs have null job IDs and accepted=false. No final PR, '
            'public source hash, tree, API request, POST, observer process, native run, test, render or install is claimed. '
            'No prior PR1282/1283 results are inherited, and the earlier FAR Fly budget failure is neither a pass nor a waiver. '
            'Original T2375 remains OPEN/DIFFERS.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
