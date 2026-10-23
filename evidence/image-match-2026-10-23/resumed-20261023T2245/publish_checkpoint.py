from datetime import datetime, timezone
from pathlib import Path
import base64
import hashlib
import json
import shutil
import subprocess

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

assert not run(['git', 'status', '--porcelain']).stdout
run(['git', 'pull', '--ff-only', '--quiet', 'origin', 'main'])
DEST.mkdir(parents=True, exist_ok=True)
selected = [WORK / name for name in ['ARCHIVES.json', 'RECOVERY.md', 'PR-SNAPSHOT.json', 'SCHOOL-SELECTION.json']]
selected += sorted(WORK.glob('*.py'))
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
run(['git', 'add', '--', str(REL)])
changed = run(['git', 'diff', '--cached', '--name-only']).stdout.splitlines()
assert changed and all(p.startswith(str(REL) + '/') for p in changed)
run(['git', 'commit', '-q', '-m', 'Checkpoint resumed school and Tremont actual comparisons with open image gates'])
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
receipt = {'published_at': datetime.now(timezone.utc).isoformat(), 'repository': 'kevinrhaas/chicago-evidence', 'commit': head, 'observed_remote_main': remote, 'push': push_log, 'files': copied, 'remote_readback': []}
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
