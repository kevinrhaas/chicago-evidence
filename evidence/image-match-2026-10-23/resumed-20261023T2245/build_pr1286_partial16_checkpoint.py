from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/PR1286-closed-partial16-exactcefcbf-PASS')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '12378d85a70c7a3195d21e4357fbbdcc614d9e66ab317d7fbcc378d4d4bb9b90'
rows = json.loads(p.read_text())['files']
assert len(rows) == 37 and sum(z['bytes'] for z in rows) == 1114654
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'PR1286-EXACT-CEFcbf-PARTIAL16-ACTUAL-PASS-DESKTOP13-14-PENDING'
note = ('Exact37 closed files plus original manifest. Sixteen exactcefcbf actual raw smoke PASS groups: allnine mobile '
        'groups/all15parts plus desktopseven. Complete checkout/env/nativefooter/nonempty zeroFAIL counts/zeroerrors/'
        'run+jobSUCCESS proof. Onlydesktop13+14RUNNING20:40:50; no full18/currentFull1904budget/merge/image-match approval. '
        'Ordinary1065/384+report+warranted proof separately7c05/d70; moving/humans absent, SKIPPED notPASS. Preliminary14 '
        'capture refused localcountguard when liveobserver advanced16 beforefreeze; empty14folder has no closedmanifest '
        'and is NOT CI failure. No rawproofmutation/old1282-83 reuse/cap waiver/observer duplication or source/CI actions.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py';s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- PR1286 partial16 preserves37 closed files plus manifest: all nine mobile groups covering parts1–15 '
    'and seven desktop groups pass on exactcefcbf source, with raw checkout/environment, complete native footers, '
    'nonempty zero-failed counts, zero errors and both run/job success bindings. **Only desktop13 and14 remain running '
    'at20:40:50**, so full18, current Full1904 budget, merge and picture-match acceptance are not claimed. The source-bound '
    'ordinary1065/384+report+warranted passes remain separate; moving/humans are absent and conditional SKIPPED is not '
    'PASS. An earlier attempted14-result freeze was locally refused by its count guard because the observer had advanced '
    'to16: that empty folder has no closed manifest and is not a CI failure or changed raw proof. No old1282/1283 results '
    'are inherited, no caps are waived, and live observers/source/CI remain untouched.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
    'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
