from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
S = lambda b: hashlib.sha256(b).hexdigest()
r = Path('/workspace/PR1286-closed-partial6-exactcefcbf-PASS')
p = r / 'MANIFEST.json'
assert S(p.read_bytes()) == 'b68ed84cb3e70ee523f36df87f009eca9bbf622875af9bbee2cff45f520f9014'
rows = json.loads(p.read_text())['files']
assert len(rows) == 18 and sum(z['bytes'] for z in rows) == 446376
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and S(b) == z['sha256']
partial_note = ('Exact18 closed files plus original manifest. Six exactcefcbf actual raw smoke PASS groups: desktop5/8, '
    'mobile1-2/3-4/5/8; zeroerrors/zeroFAILcounts/nativefooter/checkout/env/job proof. Twelve jobs RUNNING20:25:50 '
    'and hosted gate pending. No full18/currentFullbudget/merge/image-match acceptance, caps unchanged/no oldrun reuse. '
    'GET live observers remain outside selection and unduplicated.')
receipt = W / 'STORAGE-EXTENDED-SPARSE-CACHE-110-20261024.json'
x = json.loads(receipt.read_text())
assert x['status'] == 'PASS_SPARSE_DEMATERIALIZED_ALL285_COMMITTED_PAYLOADS_RETAINED'
assert len(x['files']) == 110 and x['bytes_per_duplicate_set'] == 182165276
assert x['free_workspace_after'] == 2232578048 and x['reclaimed_allocated_bytes'] == 364240896
storage_entries = [(q, q.name, S(q.read_bytes())) for q in [receipt,
    W / 'extend_verified_archive_sparse_cache_110.py', W / 'STORAGE-ARCHIVE-OMISSIONS.json']]
storage_note = ('Owned-only bounded sparse dematerialization of110 newer already committed/independently remote-verified '
    'tar payload pairs, under existing parent own-cache policy and explicit fort coordinator window. Each pair validated '
    'local SHA256/size, HEAD/index blob, prior immutable remote receipt and ancestor. All110 Git blobs reread SHA256 after; '
    'Git object-file inventory/config/refs/HEAD/stage entries exact, cleanstatus, only sparse skip bits. Reclaimed364240896B, '
    'workspacefree2232578048B, fort >=2GiB startup unblocked. All285 archive payloads remain committed+GitHub; no rawsource/'
    'heldGLB/manifests/receipts/history/object deletion, no fetch/lazyfetch. Restore any tar via Git show or immutable URL. '
    'This is storage proof, not project source/native/model validation.')
summary = []
for name, entries, note in [
    ('PR1286-EXACT-CEFcbf-PARTIAL6-ACTUAL-PASS-12-PENDING', m.author_manifest(r,p), partial_note),
    ('ARCHIVIST-VERIFIED110-DUPLICATE-TAR-SPARSE-EVICTION-ALL285-GIT-RETAINED', storage_entries, storage_note)]:
    with contextlib.redirect_stdout(io.StringIO()):
        row = m.archive(name, entries, note)
    summary.append({'name': name, 'bytes': row['bytes'], 'readback': 'PASS'})
p = W / 'write_index.py'
s = p.read_text(); needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- PR1286 partial-six actual results preserve 18 closed files plus manifest: desktop5/8 and mobile1–2/3–4/5/8 '
    'each pass on exact cefcbf source, with raw checkout/environment/job bindings, complete native footer, zero failed '
    'counts and zero errors. **Twelve jobs remained running at20:25:50 and the hosted gate was pending.** This is not '
    'full18 coverage, a current Full-budget verdict, merge approval or an accepted picture match. Native caps stay unchanged '
    'and no old runs are inherited; the live GET observers are untouched.\n'
    '- A bounded archive-cache receipt records only the archivist\'s 110 newer duplicate tar payload pairs. Each was '
    'checked against current HEAD/index bytes and its prior independent immutable remote readback before sparse omission '
    'and redundant local-cache removal; all110 committed blobs were read and SHA256-checked afterward. Git object-file '
    'inventory, config, refs, HEAD and stage entries remain exact and status stays clean; only sparse skip bits change. '
    'This freed364,240,896B and left2,232,578,048B on workspace, allowing the fort owner\'s2GiB gate startup guard. '
    '**All285 previous archive payloads remain in Git and on GitHub**, with source packets, held GLBs, manifests and '
    'receipts intact. No Git object, history or source cleanup, fetch or lazy fetch occurred. Restore tars through '
    'their committed Git blobs or immutable URLs; future new archives still materialize normally.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archives': summary, 'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
