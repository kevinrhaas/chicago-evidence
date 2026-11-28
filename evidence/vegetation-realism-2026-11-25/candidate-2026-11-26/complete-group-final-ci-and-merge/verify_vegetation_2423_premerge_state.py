"""Final read-only source, green-CI, ownership and live-merge checks."""
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from vegetation_github_api_read import read as api
from vegetation_note_fold_composition import qualify_composition
from vegetation_pr_merge_native import qualify as qualify_native

W = Path('/workspace/work')
P = 'vegetation-dev-2423'
read = lambda p: json.loads(Path(p).read_text())
p = read(W/(P+'-final-integration-proof.json'))
r = read(W/(P+'-merge-readiness.json'))
cp = read(W/'better-trees-current-checkpoint.json')
repo = Path(p['repo'])
allow_draft = sys.argv[1:] == ['--before-ready']
assert not sys.argv[1:] or allow_draft
assert r['merge_candidate_ready'] and r['ci_green']
now = datetime.datetime.now(datetime.timezone.utc)
assert 0 <= (now-datetime.datetime.fromisoformat(r['time_utc'])).total_seconds() < 180
assert r['head'] == p['final_head']
def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo, text=True).strip()
assert git('rev-parse', 'HEAD') == p['final_head']
assert not git('status', '--porcelain')
assert git('ls-remote', 'origin', 'refs/heads/steward/t3747-t3748-t3760-better-trees').split()[0] == p['final_head']
for path, digest in p['source_sha256'].items():
    assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest
composition = qualify_composition('m2-dev2423', p)
native = qualify_native(P, composition)
assert native['complete']
pr = api('repos/kevinrhaas/chicago/pulls/2414')
assert pr['state'] == 'open' and not pr['merged']
assert pr['head']['sha'] == p['final_head'] and pr['base']['ref'] == 'dev'
assert pr['mergeable'] is True
assert 'hold' not in [x['name'] for x in pr['labels']]
if not allow_draft:
    assert not pr['draft'] and pr['mergeable_state'] == 'clean', pr['mergeable_state']
reviews = api('repos/kevinrhaas/chicago/pulls/2414/reviews?per_page=100')
assert len(reviews) < 100
latest = {}
for review in reviews:
    if review['state'] in ('APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'):
        latest[review['user']['login']] = review['state']
assert 'CHANGES_REQUESTED' not in latest.values(), latest
lap = git('ls-remote', 'origin', 'refs/heads/lap/pr-2414').split()[0]
assert lap == cp['process']['m2_lap_sha']
env = {**os.environ, 'PATH': str(W/'node22/bin')+':'+os.environ['PATH'],
       'NODE_PATH': str(W/'node22/lib/node_modules'),
       'CHICAGO_TICKETS_DIR': str(W/'better-trees-seasons-integration/chicago/4d/tickets')}
env.pop('GH_TOKEN', None)
env.pop('GITHUB_TOKEN', None)
lock = subprocess.run(['node', 'tools/ticket.mjs', 'lap', '2414', '--status'],
    cwd=repo/'chicago/4d', env=env, capture_output=True, text=True)
assert lock.returncode == 3 and 'Better Trees season pass ' in lock.stdout
for ticket in ('T-3747', 'T-3748', 'T-3760'):
    files = list(Path(env['CHICAGO_TICKETS_DIR']).rglob(ticket+'-*.md'))
    assert len(files) == 1
    text = files[0].read_text()
    assert '\nstate: review\n' in text and '\npr: 2414\n' in text
out = {'complete': True, 'pr': 2414, 'head': p['final_head'],
       'before_ready': allow_draft, 'draft': pr['draft'],
       'mergeable_state': pr['mergeable_state'], 'owned_lap': lap,
       'live_dev_composition': composition, 'actual_combined_PR_native': native,
       'review_states': latest, 'time_utc': now.isoformat(),
       'unresolved_inline_threads_must_be_read_fresh_with_GitHub_connector': True}
target = W/(P+('-before-ready-state.json' if allow_draft else '-final-premerge-state.json'))
target.write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('actual_combined_PR_native', 'live_dev_composition')}))
