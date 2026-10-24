from pathlib import Path
import contextlib, hashlib, importlib.util, io, json

W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/T3122-T3123-T3124-integration-20261024/claim-renewal')
p = r / 'MANIFEST.json'
expected = '462edc79259970a9d2c530b0f159f2e852f2060b06aef197c8e9860ec8bbc89e'
assert hashlib.sha256(p.read_bytes()).hexdigest() == expected
rows = json.loads(p.read_text())['files']
assert len(rows) == 3
for x in rows:
    rel = Path(x['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == x['bytes'] and hashlib.sha256(b).hexdigest() == x['sha256']
name = 'T3122-T3123-T3124-NORMAL-OWN-RELEASE-RECLAIM-RENEWAL-OPERATIONAL-ONLY'
note = ('Exact three closed operational payloads plus original manifest. Initial normal claim refuses live claims; '
        'own normal release 9b93a28d followed by three-of-three normal same-actor claim '
        'd7f61a194995daeda46c3ee0f326b12abe3ee00a with exact remote main readback. '
        'Claimed 2026-10-24T19:14:50Z, expires 22:14:50Z. No force, rival override, done, code, native, '
        'app or cache write; inactive Fort SITE absent. Dated operational receipt only; future ownership '
        'requires fresh native checks. No live clone harvest or source/model validation implied.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- A closed operational receipt preserves the normal renewal of the owner\'s T3122/T3123/T3124 claims. '
            'The first normal claim refused existing live claims; the owner then normally released its own claims '
            '(9b93a28d) and reclaimed all three with the same actor (d7f61a194995daeda46c3ee0f326b12abe3ee00a), '
            'with exact remote readback. The dated claim runs from 19:14:50 to 22:14:50 UTC on 2026-10-24. '
            'No force, rival override, completion, source, native, app or cache write occurred; inactive Fort SITE '
            'was absent. This is an operational record, not source or model validation, and future ownership '
            'must be checked again. Only the three listed closed files and original manifest are archived.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
