from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/T3126-runtime/closed-cefcbf-public-gate-control-handoff-20261024T202119Z')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == 'a4218e675f9af6e31828d64699b09a9b867623ed1deded228bfa01013d8c461e'
rows = json.loads(p.read_text())['files']
assert len(rows) == 84 and sum(z['bytes'] for z in rows) == 15329890
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    assert not any(z in ['.git', '__pycache__', 'node_modules'] for z in rel.parts)
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'PR1286-PUBLIC-CEFcbf-LOCAL1065-PASS-FAR-CONTROL-BOTH-FAIL-CACHE-HANDOFF'
note = ('Exact84 closed payloads plus manifest. Public/frozen clean sourcecefcbf155/treecfb2a9c5 one normal commit on305 '
        'equals tested tree. Actual required-reader preflight1065/384/626s exit0 and separate committed-head CL/IDs PASS. '
        'Interrupted doc-startup gate has NO VERDICT; stale unowned global CL/IDs copies not accepted. Own doc suffix fixed '
        'without altering incoming raw prefixes. Completed previous/current WEB geometry-only far controls BOTH over unchanged '
        '3470000 cap:3483153 vs3494017,delta10864,calls5781 each. Only target HTTP geometry differs; camera/state/detail/sidecar/'
        'animation/published5383 hashes bound. Mobile actual signature-range supplement; source comparison directly owner-reviewed '
        'DIFFERS/original2375OPEN. T3126REVIEW, finite own lap/status3 and wrapper correction explicit. REAL cache transfer maps '
        'and receipt only,5577objects/5383files exact incl inode, no live cache payload/read. Closed18dispatch bindings included '
        'but all actual raw-log/ordinary CI outcomes PENDING at closure; no merge approval, universal budget PASS or picture match.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
assert row['bytes'] < 50000000
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- PR1286 final local source/control handoff preserves 84 closed payloads plus manifest. Public clean source '
            'cefcbf15534f8cfa0b592faf4e4d7287109f0822, tree cfb2a9c590b3b257fc845f35e07eb0d4208a40e7, is one '
            'normal commit on305 and exactly equals the final tested tree. The actual required-reader preflight passes '
            '**1065 steps/384 self-tests, exit0,626s**, with separate actual committed-head changelog/ID receipts. The '
            'interrupted doc-startup attempt has **NO VERDICT**; its stale unowned global CL/ID copies are not results '
            'of that run. The own ASCII doc suffix was repaired while preserving incoming raw prefixes. The completed '
            'geometry-only far-pose control is explicit: previous WEB 3,483,153 versus current 3,494,017 triangles, both '
            'over the unchanged3,470,000 cap; delta10,864 with5,781 calls each. Target HTTP geometry alone differs; '
            'camera, state, detail, sidecar, held animation and all5,383 published file hashes are bound. This is not '
            'a whole-Abb-app or universal budget pass. The mobile visible full-citation supplement is actual; the '
            'official source comparison was directly owner-reviewed DIFFERS and original T2375 remains OPEN. T3126 is '
            'REVIEW, not DONE, with a dated finite own lap and explicit native HELD/status3 wrapper correction. The '
            'guarded real-cache handoff stores only maps/receipts: all5,577 objects/5,383 files preserve SHA/inode/dev/'
            'mode/owner/mtime through the owner transfer, with no live cache payload/read in this archive. Closed18 '
            'dispatch bindings are included, but **actual raw-log and ordinary CI outcomes remain pending at closure**. '
            'Expected-head merge delegation is conditional on those independent results and fresh base safety; this '
            'packet grants no merge approval or picture-match acceptance.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
