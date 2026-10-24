from datetime import datetime, timezone
from pathlib import Path
import base64
import hashlib
import json
import shutil
import subprocess
import sys

WORK = Path(__file__).resolve().parent
REPO = WORK / 'remote-evidence'
REL = Path('evidence/image-match-2026-10-23/resumed-20261023T2245')
DEST = REPO / REL
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def run(args, check=True):
    result = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {args[0]} {args[1]}\n{result.stderr}')
    return result

def verify_archive_availability():
    rows = json.loads((WORK / 'ARCHIVES.json').read_text())
    ledger_path = WORK / 'STORAGE-ARCHIVE-OMISSIONS.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {'files': []}
    allowed = {r['name']: r for r in ledger['files']}
    assert len(allowed) == len(ledger['files'])
    absent = []
    for row in rows:
        source = Path(row['archive'])
        if source.is_file():
            assert not source.is_symlink()
            assert source.stat().st_size == row['bytes'] and sha(source) == row['sha256'], source
            continue
        entry = allowed.get(source.name)
        assert entry is not None, 'Missing archive without remote-verification ledger: ' + str(source)
        assert entry['sha256'] == row['sha256'] and entry['bytes'] == row['bytes']
        proof = entry['independent_remote_readback']
        path = str(REL / 'archives' / source.name)
        assert entry['git_path'] == path and proof['path'] == path
        assert proof['status'] == 'PASS' and proof['sha256'] == row['sha256'] and proof['bytes'] == row['bytes']
        blob = run(['git', 'rev-parse', 'HEAD:' + path]).stdout.strip()
        assert blob == entry['git_blob'] == proof['git_blob']
        indexed = run(['git', 'ls-files', '--stage', '--', path]).stdout.split()
        assert indexed[:3] == ['100644', blob, '0'], 'Uncertain archive index: ' + path
        data = subprocess.check_output(['git', 'cat-file', 'blob', blob], cwd=REPO)
        assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
        absent.append({'path': path, 'git_blob': blob, 'bytes': row['bytes'], 'sha256': row['sha256'], 'status': 'COMMITTED_INDEX_BLOB_AND_PRIOR_REMOTE_READBACK_PASS'})
    return absent

assert not run(['git', 'status', '--porcelain']).stdout
absent = verify_archive_availability()
if '--check-storage' in sys.argv:
    print(json.dumps({'status': 'STORAGE_AVAILABILITY_PASS', 'verified_absent_archives': len(absent)}))
    raise SystemExit(0)
# Avoid automatic repack scratch while storage is constrained; normal refs/push behavior is unchanged.
run(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', 'pull', '--ff-only', '--quiet', 'origin', 'main'])
absent = verify_archive_availability()
DEST.mkdir(parents=True, exist_ok=True)
selected = [WORK / name for name in ['ARCHIVES.json', 'RECOVERY.md', 'PR-SNAPSHOT.json', 'SCHOOL-SELECTION.json']]
selected += sorted(WORK.glob('*.py'))
selected += sorted(WORK.glob('STORAGE-*.json'))
selected += sorted((WORK / 'archives').iterdir())
selected += sorted((WORK / 'publications').glob('*.json'))
if (WORK / 'TICKETS-POINTER-RECEIPT.json').exists():
    selected.append(WORK / 'TICKETS-POINTER-RECEIPT.json')
assert selected and all(p.is_file() and not p.is_symlink() for p in selected)
copied = []
for source in selected:
    rel = source.relative_to(WORK)
    destination = DEST / rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert sha(source) == sha(destination)
    copied.append({'path': str(REL / rel), 'bytes': source.stat().st_size, 'sha256': sha(source)})
run(['git', 'add', '--sparse', '--', str(REL)])
assert not run(['git', 'diff', '--cached', '--diff-filter=D', '--name-only', '--', str(REL / 'archives')]).stdout, 'Archive deletion forbidden'
changed = run(['git', 'diff', '--cached', '--name-only']).stdout.splitlines()
assert changed and all(p.startswith(str(REL) + '/') for p in changed)
run(['git', 'commit', '-q', '-m', 'Checkpoint resumed picture comparisons and guarded integration work'])
push_log = []
for attempt in range(3):
    result = run(['git', 'push', 'origin', 'HEAD:main'], check=False)
    push_log.append({'attempt': attempt + 1, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode == 0:
        break
    if 'fetch first' not in result.stderr and 'non-fast-forward' not in result.stderr and 'rejected' not in result.stderr:
        raise RuntimeError('Normal push failed; no force or authentication changes attempted.\n' + result.stderr)
    run(['git', 'pull', '--rebase', '--quiet', 'origin', 'main'])
else:
    raise RuntimeError('Three normal pushes raced with main; checkpoint commit remains local.')
head = run(['git', 'rev-parse', 'HEAD']).stdout.strip()
remote = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).stdout.strip().split()[0]
receipt = {'published_at': datetime.now(timezone.utc).isoformat(), 'repository': 'kevinrhaas/chicago-evidence', 'commit': head, 'observed_remote_main': remote, 'push': push_log, 'files': copied, 'verified_absent_archives': absent, 'remote_readback': []}
(WORK / 'LATEST-PUBLICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')

# Re-read the published index plus every archive through the GitHub blob API.
verify = [p for p in copied if p['path'] in changed and (p['path'].endswith('/RECOVERY.md') or p['path'].endswith('.tar.gz'))]
for row in verify:
    blob_sha = run(['git', 'rev-parse', head + ':' + row['path']]).stdout.strip()
    response = subprocess.check_output(['gh', 'api', 'repos/kevinrhaas/chicago-evidence/git/blobs/' + blob_sha], text=True)
    payload = json.loads(response)
    assert payload['encoding'] == 'base64'
    data = base64.b64decode(payload['content'])
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
    receipt['remote_readback'].append({'path': row['path'], 'git_blob': blob_sha, 'bytes': len(data), 'sha256': row['sha256'], 'status': 'PASS'})
(WORK / 'LATEST-PUBLICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
history = WORK / 'publications'
history.mkdir(exist_ok=True)
(history / (head + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
assert not run(['git', 'status', '--porcelain']).stdout
print(json.dumps({'commit': head, 'remote_main': remote, 'remote_readback_files': len(verify), 'status': 'PUBLISHED_AND_READBACK_PASS', 'index': f'https://github.com/kevinrhaas/chicago-evidence/blob/{head}/{REL}/RECOVERY.md'}, indent=2))
