from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/tmp/T3122-neutral-stone-alias-final-peer-review')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == 'dfd8a6c3e6cfa665b0c09119baa281d2690d862b96a6e8e5fc7b5a586c373ad4'
rows = json.loads(p.read_text())['files']
assert len(rows) == 2
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'T3122-NEUTRAL-STONE-ALIAS-FINAL-SOURCE-REVIEW-EXPORTS-PENDING'
note = ('Exact two closed files plus original manifest. Final source span APPROVE for producer '
        'a0bcd0e9223d4ba2b1a9fd3a67fe1959ee3035846ff0c03a99bc11e0324ba538: both new shaft helpers use '
        'resolved wall RGBA/roughness exact equality before neutral alias, preserving named stone/.93 fallback for '
        'different white/whitewash descriptors. Helper resides in already-hashed producer. Four paint-test assertions '
        'source-reviewed; owner-reported PASS NOT rerun by reviewer. No geometry/tone/normal logic change, no canonical '
        'reviewer writes. Genuine25/web/native results PENDING at closure; no export proof borrowed. Earlier fe215 '
        'preimplementation review remains a distinct immutable timepoint.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- A later, separate neutral-stone alias review approves the **final source span only**, pinned to producer '
            'a0bcd0e9223d4ba2b1a9fd3a67fe1959ee3035846ff0c03a99bc11e0324ba538. Both new shaft helpers call the '
            'resolved wall RGBA/roughness equality helper: exact descriptors alias, while white/whitewash cases retain '
            'the named stone/.93 fallback. This helper is already inside the hashed producer, without a new freshness '
            'dependency. The reviewer inspected four paint-test assertions and records the owner-reported passes, '
            'but did not rerun those tests. Geometry, tone and normal logic remain outside this change. **Genuine25 '
            'exports, web derivatives and native results were pending at closure**; this is not actual export proof. '
            'The earlier fe215 preimplementation review remains an immutable, distinct timepoint.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
