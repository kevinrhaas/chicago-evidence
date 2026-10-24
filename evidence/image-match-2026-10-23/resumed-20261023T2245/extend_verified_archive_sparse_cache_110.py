from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess

W = Path(__file__).resolve().parent
R = (W / 'remote-evidence').resolve()
REL = 'evidence/image-match-2026-10-23/resumed-20261023T2245'
ENV = {**os.environ, 'GIT_NO_LAZY_FETCH': '1', 'GIT_OPTIONAL_LOCKS': '0'}
S = lambda b: hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R, env=ENV)
def free():
    v = os.statvfs('/workspace')
    return v.f_bavail * v.f_frsize
def object_files():
    root = R / '.git/objects'
    return {str(p.relative_to(root)): [p.stat().st_size, p.stat().st_mtime_ns, p.stat().st_ino]
            for p in root.rglob('*') if p.is_file()}

assert not git('status', '--porcelain')
head = git('rev-parse', 'HEAD').decode().strip()
assert head == 'acbfbd89e5d543bf169b683d67de9f5a8c703dfd'
stages = git('ls-files', '--stage'); refs = git('show-ref')
config_before = S((R / '.git/config').read_bytes())
objects_before = object_files()
free0 = free()
ledger = json.loads((W / 'STORAGE-ARCHIVE-OMISSIONS.json').read_text())
old_names = {z['name'] for z in ledger['files']}
assert len(old_names) == 175
proofs = {}
for p in sorted((W / 'publications').glob('*.json')):
    rec = json.loads(p.read_text())
    for proof in rec.get('remote_readback', []):
        if proof['status'] == 'PASS':
            proofs[proof['path']] = (p, rec, proof)
selected = []
for row in json.loads((W / 'ARCHIVES.json').read_text()):
    src = Path(row['archive'])
    if not src.is_file():
        continue
    assert src.name not in old_names and not src.is_symlink()
    path = REL + '/archives/' + src.name
    dst = R / path
    assert dst.is_file() and not dst.is_symlink()
    assert src.resolve().parent == Path('/workspace/T3081-emergency-archive-hold')
    b = src.read_bytes()
    assert len(b) == row['bytes'] and S(b) == row['sha256'] and dst.read_bytes() == b
    indexed = git('ls-files', '--stage', '--', path).decode().split()
    blob = git('rev-parse', head + ':' + path).decode().strip()
    assert indexed[:3] == ['100644', blob, '0']
    assert git('cat-file', 'blob', blob) == b
    p, rec, proof = proofs[path]
    assert proof['git_blob'] == blob and proof['sha256'] == row['sha256'] and proof['bytes'] == row['bytes']
    assert git('merge-base', '--is-ancestor', rec['commit'], head) == b''
    selected.append({'name': src.name, 'local_archive_path': str(src), 'worktree_path': str(dst),
        'git_path': path, 'sha256': row['sha256'], 'bytes': row['bytes'], 'git_blob': blob,
        'verified_committed_at': head, 'local_mode': oct(stat.S_IMODE(src.stat().st_mode)),
        'working_mode': oct(stat.S_IMODE(dst.stat().st_mode)),
        'independent_remote_readback': {'published_commit': rec['commit'], 'published_at': rec['published_at'],
            'receipt_file': str(p), 'receipt_sha256': S(p.read_bytes()), **proof},
        'restore_url': 'https://github.com/kevinrhaas/chicago-evidence/blob/' + head + '/' + path,
        'restoration': 'git show HEAD:<git_path> > chosen-output; remove exact sparse exclusion and reapply for working copy'})
assert len(selected) == 110 and sum(z['bytes'] for z in selected) == 182165276
receipt = {'at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PREVERIFIED_PENDING_EVICTION',
    'authorization': 'Existing parent own-cache reversible sparse policy, plus explicit fort coordinator window for these exact110 duplicate tars to unblock >=2GiB native gate startup. No Git object/history/source/heldGLB deletion.',
    'head': head, 'stage_entries_sha256': S(stages), 'refs_sha256': S(refs),
    'config_sha256': config_before, 'status_before': 'clean', 'free_workspace_before': free0,
    'files': selected, 'bytes_per_duplicate_set': 182165276, 'sets': 2,
    'no_fetch_or_lazy_fetch': True, 'no_git_object_or_source_cleanup': True}
out = W / 'STORAGE-EXTENDED-SPARSE-CACHE-110-20261024.json'
assert not out.exists()
out.write_text(json.dumps(receipt, indent=2) + '\n')
sparse = R / '.git/info/sparse-checkout'
before = sparse.read_text()
receipt['sparse_before_sha256'] = S(before.encode())
ledger['files'] += selected
ledger.update({'status': 'AUTHORIZED_EXACT285_REMOTE_VERIFIED_ARCHIVE_TAR_OMISSIONS',
    'count': 285, 'extended_at': receipt['at_utc'],
    'scope': 'Original175 and110 additional exact HEAD/index/local/cache/prior independent remote-readback verified tars may be absent. All285 committed Git objects/index entries/refs/source packets/manifests/receipts retained; restore via Git blob or immutable remote URL. New archives materialize normally.'})
(W / 'STORAGE-ARCHIVE-OMISSIONS.json').write_text(json.dumps(ledger, indent=2) + '\n')
after = before + ''.join('!/' + z['git_path'] + '\n' for z in selected)
sparse.write_text(after)
subprocess.run(['git', 'sparse-checkout', 'reapply'], cwd=R, env=ENV, check=True)
assert not git('status', '--porcelain') and git('ls-files', '--stage') == stages
assert git('show-ref') == refs and git('rev-parse', 'HEAD').decode().strip() == head
for z in selected:
    assert not Path(z['worktree_path']).exists()
    src = Path(z['local_archive_path'])
    assert S(src.read_bytes()) == z['sha256']
    src.unlink()
    assert S(git('cat-file', 'blob', z['git_blob'])) == z['sha256']
assert not git('status', '--porcelain') and git('ls-files', '--stage') == stages
assert git('show-ref') == refs and git('rev-parse', 'HEAD').decode().strip() == head
assert S((R / '.git/config').read_bytes()) == config_before
assert object_files() == objects_before
receipt.update({'status': 'PASS_SPARSE_DEMATERIALIZED_ALL285_COMMITTED_PAYLOADS_RETAINED',
    'sparse_after_sha256': S(after.encode()), 'head_after': head, 'status_after': 'clean',
    'free_workspace_after': free(), 'reclaimed_allocated_bytes': free() - free0,
    'index_skip_worktree_bits_only_changed': True, 'all_new110_committed_blobs_full_sha256_after_eviction': True,
    'git_object_file_inventory_exact': True, 'config_refs_stage_entries_head_exact': True})
out.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'files'}, indent=2))
