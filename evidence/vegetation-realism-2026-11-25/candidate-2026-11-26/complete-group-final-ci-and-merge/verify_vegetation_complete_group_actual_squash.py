"""Verify the actual returned squash against its real Dev parent and feature tree."""
import datetime
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from vegetation_exact_note_folds import verify_folds

W = Path('/workspace/work')
read = lambda p: json.loads(Path(p).read_text())
state = read(W/'better-trees-current-checkpoint.json')
p = read(W/state['m2']['active_source_proof'])
R = Path(p['repo'])
result = read(W/'vegetation-complete-group-actual-merge-result.json')
pr = read(W/'vegetation-complete-group-merged-pr.json')
assert result['merged'] is True and result['sha']
S = result['sha']
assert pr['merged'] and pr['number'] == 2414 and pr['base'] == 'dev'
assert pr['head_sha'] == p['final_head'] and pr['merge_commit_sha'] == S
def raw(*args, **kw):
    return subprocess.check_output(['git', *args], cwd=R, **kw)
refs = {k: raw('rev-parse', k) for k in ('HEAD', 'origin/dev')}
assert refs['HEAD'].decode().strip() == p['final_head']
assert not raw('status', '--porcelain').strip()
subprocess.run(['git', 'fetch', '--quiet', '--no-write-fetch-head', '--refmap=',
                'origin', S], cwd=R, check=True)
parents = raw('show', '-s', '--format=%P', S).decode().split()
assert len(parents) == 1
U = parents[0]
upstream_delta = verify_folds(R, p['actual_dev'], U)
patch = raw('diff', '--binary', p['actual_dev'], p['final_tree'])
assert hashlib.sha256(patch).hexdigest() == p['integrated_patch_sha256']
with tempfile.TemporaryDirectory(prefix='vegetation-actual-squash-', dir=W) as temp:
    env = {**os.environ, 'GIT_INDEX_FILE': str(Path(temp)/'index')}
    subprocess.run(['git', 'read-tree', U], cwd=R, env=env, check=True)
    subprocess.run(['git', 'apply', '--cached', '--check'], input=patch, cwd=R, env=env, check=True)
    subprocess.run(['git', 'apply', '--cached'], input=patch, cwd=R, env=env, check=True)
    composed = raw('write-tree', env=env).decode().strip()
    assert composed == raw('rev-parse', S+'^{tree}').decode().strip()
    subprocess.run(['git', 'apply', '--cached', '--reverse'], input=patch, cwd=R, env=env, check=True)
    assert raw('write-tree', env=env).strip() == raw('rev-parse', U+'^{tree}').strip()
assert raw('merge-tree', '--write-tree', p['final_head'], U).decode().splitlines()[0] == composed
for path, digest in p['source_sha256'].items():
    assert hashlib.sha256(raw('show', S+':'+path)).hexdigest() == digest
assert refs == {k: raw('rev-parse', k) for k in refs}
out = {'merged': True, 'verified': True, 'pr': 2414, 'head': p['final_head'],
       'merge_sha': S, 'actual_merge_parent': U, 'actual_merge_tree': composed,
       'qualified_integration_proof': state['m2']['active_source_proof'],
       'actual_merge_preserves_every_feature_and_entire_current_Dev': True,
       'only_exact_official_folds_since_qualified_Dev': upstream_delta,
       'source_and_app_refs_unchanged': True,
       'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
target = W/'vegetation-complete-group-merge-receipt.json'
assert not target.exists()
target.write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out))
