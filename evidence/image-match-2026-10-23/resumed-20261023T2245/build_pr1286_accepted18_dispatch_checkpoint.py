from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/PR1286-headcefcbf-binding-and-dispatch')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '3b6218a484977601bf157241b05117bbe265cc2e164188c92d6fdf8a14f67a73'
x = json.loads(p.read_text())
assert x['status'] == 'CLOSED_DISPATCHED_NOT_RESULTS'
assert len(x['files']) == 27 and sum(z['bytes'] for z in x['files']) == 68524
for z in x['files']:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
binding = json.loads((r / 'INITIAL_BINDING.json').read_text())
d = json.loads((r / 'BOUND_DISPATCH.json').read_text())
head = 'cefcbf15534f8cfa0b592faf4e4d7287109f0822'
assert binding['head'] == d['head'] == head
assert binding['tree'] == 'cfb2a9c590b3b257fc845f35e07eb0d4208a40e7'
assert d['status'] == 'DISPATCHED_NOT_RESULTS' and len(d['runs']) == 18
assert len({z['id'] for z in d['runs']}) == 18
groups = {'1-2', '3-4', '5', '6-7', '8', '9-12', '13', '14', '15'}
assert {(z['viewport'], z['stage']) for z in d['runs']} == {(v, g) for v in ['desktop','mobile'] for g in groups}
for z in d['runs']:
    assert z['dispatch_accepted'] is True and z['observed_head'] == head
    payload = json.loads((r / (z['viewport'] + '-' + z['stage'] + '.json')).read_text())
    assert payload == {'ref': d['branch'], 'inputs': {'viewport': z['viewport'], 'stage': z['stage']}}
assert hashlib.sha256((r / 'PUBLIC_chicago-4d-smoke.yml').read_bytes()).hexdigest() == binding['workflow_sha256']
name = 'PR1286-CEFcbf-AUTHORIZED-18-ACCEPTED-DISPATCH-NOT-RESULTS'
note = ('Exact27 closed payloads plus original manifest. Sole authorized18 native workflow POSTs accepted once, '
        '18 unique IDs/exact cefcbf15534f8cfa0b592faf4e4d7287109f0822, nine groups times two viewports; '
        'finished20:10:36UTC/process0. Public treecfb2a9c590b3b257fc845f35e07eb0d4208a40e7/soleparent305dc4 '
        'and workflow f0f6c6f5 byte identity independently bound. Per-leg source check, payloads and durable sentinels '
        'preserved. DISPATCHED_NOT_RESULTS; no actual smoke/gate/budget PASS or old1282/1283 inheritance. '
        'Separate GET-only watchers active outside this selection, not duplicated. No source/native/browser/test/credential/'
        'assertion/cap changes, no image-match closure or merge approval.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py'
s = p.read_text()
old = '[1229, 1239, 1256, 1260, 1273, 1282, 1283]'
assert s.count(old) == 2
s = s.replace(old, '[1229, 1239, 1256, 1260, 1273, 1282, 1283, 1286]')
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- **PR1286 Dearborn is dispatched, not validated by these receipts.** The sole authorized dispatch closed '
            'at 20:10:36 UTC with exactly 18 accepted, unique native workflow runs: nine stage groups in each viewport, '
            'covering parts 1–15. Every run binds to public source cefcbf15534f8cfa0b592faf4e4d7287109f0822, '
            'tree cfb2a9c590b3b257fc845f35e07eb0d4208a40e7 and sole parent 305dc4e0663faf16870c11dab2ed49beb1df3b15. '
            'The public branch and unchanged incoming305 workflow (f0f6c6f5) are independently bound; per-leg source checks, '
            'payloads and durable POST sentinels are retained. **DISPATCHED_NOT_RESULTS: zero actual PASS results are '
            'inferred.** Separate GET-only staged/ordinary observers remain outside this closed selection and are not '
            'duplicated. No earlier PR1282/1283 results are inherited, and no source, native, browser, test, credential, '
            'assertion, cap, picture-match or merge action is performed by this checkpoint.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
