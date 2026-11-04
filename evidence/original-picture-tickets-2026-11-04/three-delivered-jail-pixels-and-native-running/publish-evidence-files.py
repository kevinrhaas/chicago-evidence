"""Publish explicitly named recovery files to chicago-evidence, with exact readback."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument('--manifest', type=Path, required=True)
args = parser.parse_args()
spec = json.loads(args.manifest.read_bytes())
assert spec['prefix'].startswith('evidence/') and spec['prefix'].endswith('/')
assert '..' not in spec['prefix']
receipt_path = Path(spec['receipt'])
assert not receipt_path.exists(), 'Closed publication receipt already exists'
repo = 'repos/kevinrhaas/chicago-evidence/'

def api(path, body=None, method=None):
    command = ['gh', 'api', repo + path]
    if body is not None:
        # Use an explicit method and file body: implicit-method piped requests
        # produced EOF errors in this cloud CLI, while this form succeeded.
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.json') as request:
            json.dump(body, request)
            request.flush()
            result = subprocess.run(
                command + ['--method', method or 'POST', '--input', request.name],
                capture_output=True,
            )
    else:
        if method:
            command += ['--method', method]
        result = subprocess.run(command, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode())
    return json.loads(result.stdout)

files = {name: Path(source).read_bytes() for name, source in spec['files'].items()}
assert files
assert all(not name.startswith('/') and '..' not in name.split('/') for name in files)
blobs = {}
for name, data in files.items():
    expected = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    row = api('git/blobs', {'encoding': 'base64', 'content': base64.b64encode(data).decode()})
    assert row['sha'] == expected
    blobs[name] = expected
for attempt in range(5):
    parent = api('git/ref/heads/main')['object']['sha']
    base_tree = api('git/commits/' + parent)['tree']['sha']
    tree = api('git/trees', {'base_tree': base_tree, 'tree': [{'path': spec['prefix'] + name, 'mode': '100644', 'type': 'blob', 'sha': oid} for name, oid in blobs.items()]})
    commit = api('git/commits', {'message': spec['message'], 'tree': tree['sha'], 'parents': [parent]})
    try:
        api('git/refs/heads/main', {'sha': commit['sha'], 'force': False}, 'PATCH')
        break
    except RuntimeError as error:
        if '422' not in str(error) and '409' not in str(error):
            raise
else:
    raise RuntimeError('Concurrent evidence updates; no forced update attempted')
for name, data in files.items():
    assert base64.b64decode(api('git/blobs/' + blobs[name])['content']) == data
    row = api('contents/' + quote(spec['prefix'] + name, safe='/') + '?ref=' + commit['sha'])
    assert row['sha'] == blobs[name]
receipt = {'commit': commit['sha'], 'parent': parent, 'prefix': spec['prefix'], 'normal_fast_forward': True, 'all_blob_and_commit_path_readbacks_exact': True, 'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': blobs[name], 'url': 'https://github.com/kevinrhaas/chicago-evidence/blob/' + commit['sha'] + '/' + spec['prefix'] + name} for name, data in files.items()}}
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'commit': commit['sha'], 'files': len(files), 'readbacks': 'PASS'}))
