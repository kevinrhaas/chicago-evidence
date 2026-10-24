from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/PR1286-closed-watchers-start-20261024')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '027236c0fffa803164685a2682956a7abe0f51de81c2ed94eae378d9c531ab9f'
rows = json.loads(p.read_text())['files']
assert len(rows) == 9 and sum(z['bytes'] for z in rows) == 81919
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'PR1286-BOTH-GET-WATCHERS-STARTED-ZERO-SMOKE-RESULTS'
note = ('Exact nine closed files plus original manifest. Workspace-only GET full18 observer PID2041948/session70776 '
        '300s cadence, initial18exact bound and ZERO actual smoke results. Ordinaryv2 PID2042920/session32309 '
        'source tree/parents verified. Old local WAITING GET loop2040970 terminated143/cache preserved, only correcting '
        'ordinary completion selection; intentional conditional SKIPPED is never PASS, staged jobs separate. '
        'V2 observer code/transition/initial snapshots preserved. No remote CI cancel/source/native assertion/cap edits. '
        'Sole18dispatch3b6218 frozen; live watchers not harvested, started again or duplicated by archivist.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- PR1286 watcher-start evidence preserves nine closed files plus manifest: the workspace GET-only full18 '
            'observer starts with all 18 exact-head bindings and **zero actual smoke results**. The separate ordinary v2 '
            'observer verifies source tree and parents. Its predecessor local WAITING loop was terminated with exit143 '
            'and its cache retained to correct completion selection: intentional conditional SKIPPED checks are never '
            'counted as PASS, and staged results stay separate. Observer v2 code, transition receipt and first snapshots '
            'are saved. No remote CI cancellation, source, native assertion or cap change occurred. The sole dispatch '
            'receipt remains frozen; no live observer is duplicated or harvested by this archive.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
