from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
paths = [W/'STORAGE-EXTENDED-SPARSE-CACHE-M1-20261024.json', W/'extend_verified_archive_sparse_cache_M1.py']
x = json.loads(paths[0].read_text())
assert x['status'] == 'PASS_SPARSE_DEMATERIALIZED_ALL286_COMMITTED_PAYLOADS_RETAINED'
assert len(x['files']) == 1 and x['bytes_per_duplicate_set'] == 17864254
assert x['free_workspace_after'] == 2194563072
entries = [(p,p.name,hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
name = 'ARCHIVIST-ONE-M-TAR-PAIR-SPARSE-286-COMMITTED-PAYLOADS-RETAINED'
note = ('Bounded own-cache readiness receipt and exact executed script only. Fort coordinator requested only the new '
    'M25/native17,864,254B tar pair archived9281; currentHEAD/index/local/prior independentHTTPS proof checked, committed '
    'Gitblob reread SHA256 after. Reclaimed35,725,312B/free2,194,563,072B; object-file inventory/config/refs/HEAD/stages exact, '
    'cleanstatus/only sparse skip bits. All286 omitted archive payloads remain Git+GitHub recoverable; source/rawpacket/'
    'heldGLB/receipts untouched. No fetch/lazyfetch or native/model/gate proof. Normal future archives still materialize.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name,entries,note)
p=W/'write_index.py';s=p.read_text();needle='- Further producer/integration work is ongoing.'
assert s.count(needle)==1
addition=('- A later targeted storage follow-up dematerializes **only the newly verified actual-M tar pair** '
    '(17,864,254B each), after current HEAD/index/local-byte and independent9281 HTTPS proof checks. Its committed '
    'blob passes SHA256 readback after eviction. The receipt records35,725,312B reclaimed and2,194,563,072B free, '
    'with Git object-file inventory/config/refs/HEAD/stage entries exact and clean status; only sparse skip bits change. '
    'All286 omitted payloads remain in Git and on GitHub; source packets, held GLBs and receipts are untouched. '
    'This fort-coordinated cache action adds startup margin only and implies no native/model/fullgate result.\n')
p.write_text(s.replace(needle,addition+needle))
print(json.dumps({'archive':name,'bytes':row['bytes'],'readback':'PASS','inventory_count':len(json.loads((W/'ARCHIVES.json').read_text()))}))
