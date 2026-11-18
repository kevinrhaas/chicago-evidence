"""After root's quiet-window grant, verify a completed official snapshot against Git.

This script does not publish or copy a tree. Do not run it against a live publisher.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--root', default='/workspace/chicago-classroom-final-published')
parser.add_argument('--commit', default='45b35a2c7d910ec1e73f5a60489b1b22c4aff278')
parser.add_argument('--out', default='/tmp/t3656-resource-renderer-manifest.json')
args = parser.parse_args()
root, output = Path(args.root).resolve(), Path(args.out).resolve()
assert root != Path('/workspace/chicago-classroom-published'), 'Preserve the pre-repair frozen build'
assert output != Path('/tmp/t3656-renderer-manifest.json'), 'Preserve the pre-repair manifest'
repo = '/workspace/chicago'
def git(*arguments):
    return subprocess.check_output(['git', '-C', repo, *arguments])
commit = git('rev-parse', args.commit + '^{commit}').decode().strip()
build = json.loads((root / 'build.json').read_text())
assert build['version'] == commit[:9], (build['version'], commit)
digest = lambda data: hashlib.sha256(data).hexdigest()
paths = git('ls-tree', '-r', '--name-only', commit, '--',
            'chicago/4d/renderers/web/js', 'chicago/4d/renderers/web/css').decode().splitlines()
files, source_files = {}, {}
for source in paths:
    if not source.endswith(('.js', '.css')):
        continue
    relative = source.removeprefix('chicago/4d/renderers/web/')
    # publish.sh moves the changelog to the fleet path and emits a small re-export.
    published = relative if relative == 'js/changelog.js' else 'walk/' + relative
    expected = digest(git('show', commit + ':' + source))
    actual = digest((root / published).read_bytes())
    assert actual == expected, f'Published file does not match Git commit: {published}'
    files[published] = actual
    source_files[published] = {'source': source, 'sha256': expected}
for relative in ['build.json', 'walk/index.html', 'walk/js/changelog.js', '1835/index.html']:
    files[relative] = digest((root / relative).read_bytes())
manifest = {
    'created': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'commit': commit, 'root': str(root), 'publication_build': build,
    'node': '/tmp/chicago-check-runtime/node_modules/node/bin/node',
    'chromium': '/usr/bin/chromium',
    'scope': 'Completed official published snapshot; authored JS/CSS independently matched to immutable Git commit. Generated entry pages and changelog re-export hashed separately.',
    'files': files, 'git_source_files': source_files,
}
output.write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Verified {len(source_files)} authored JS/CSS files against {commit}; wrote {output}')
