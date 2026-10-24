from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/PR1286-closed-fresh-ordinary-gate-PASS')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '7c05ebfbc0484b3a1c00d141631ef10a066a2a6fee67d69bce03d2ec17c89f62'
rows = json.loads(p.read_text())['files']
assert len(rows) == 15 and sum(z['bytes'] for z in rows) == 2095677
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'PR1286-FRESH-HOSTED1065-384-REPORT-WARRANTED-PASS-TREE-EXACT'
note = ('Exact15 closed files plus manifest. Actual hostedgate1065steps/384selftests CHECKPASS plus report/warranted '
        'PASS rawlogs/metadata. Synthetic274f3972 parents305+cef has ENTIREcfb2a9c5 tree identical publiccef; public soleparent '
        '305 independentlyGET bound. Moving/humans ABSENT noPASS inference, conditional SKIPPED remainsSKIPPED. Separate '
        'staged18 has11actualPASS/7RUNNING last20:30; no fullcoverage/currentFullbudget/merge/image-match approval. Nativecaps '
        'unchanged, no oldrun reuse or overcap waiver. WorkspaceGET-only observer, no source/native/browser/lease/CI changes.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py';s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- PR1286 fresh ordinary evidence now records actual hosted **1065-step/384-self-test CHECKPASS**, plus '
    'actual report and warranted-check passes, retaining15 closed files plus manifest with raw logs and metadata. '
    'Gate checkout274f3972dc1f2fd148266d4ce61989f062ca9189 has parents305+cef and an entire tree '
    'cfb2a9c590b3b257fc845f35e07eb0d4208a40e7 identical to publiccef; the public source soleparent305 is independently '
    'bound. Moving/humans checks are **absent, not inferred passes**, and intentional conditional SKIPPED remains '
    'SKIPPED. The separate staged matrix had11 actual passes and7 running at its last20:30 snapshot. No full18 '
    'coverage, current Full-budget verdict, merge or picture-match approval follows; native caps remain unchanged '
    'and the earlier far-pose failure receives no waiver. Live GET-only watchers remain untouched.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
    'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
