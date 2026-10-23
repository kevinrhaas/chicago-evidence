"""Bound fresh hosted smoke dispatches to one already-pushed Hogan SHA."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CHECKOUT = Path('/tmp/hogan-pr1229-integration')
REPO = 'kevinrhaas/chicago'
BRANCH = 'steward/t2377-hogan-picture-match'
WORKFLOW = 'chicago-4d-smoke.yml'
PLAN = ROOT / 'FINAL-HEAD-SMOKE-PLAN.json'
head = sys.argv[1]
assert len(head) == 40 and all(c in '0123456789abcdef' for c in head)


def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], text=True))


def listing():
    return api(f'repos/{REPO}/actions/workflows/{WORKFLOW}/runs?branch={BRANCH}&event=workflow_dispatch&per_page=100')['workflow_runs']


def remote_head():
    return api(f'repos/{REPO}/git/ref/heads/{BRANCH}')['object']['sha']


assert api(f'repos/{REPO}/pulls/1229')['head']['sha'] == head
assert remote_head() == head
assert subprocess.check_output(['git', '-C', str(CHECKOUT), 'rev-parse', 'HEAD'], text=True).strip() == head
if PLAN.exists():
    plan = json.loads(PLAN.read_text())
    assert plan['head'] == head
    assert not plan.get('pending_dispatch'), 'Inspect pending receipt/API runs before repeating any dispatch.'
else:
    contract_paths = ['.github/workflows/chicago-4d-smoke.yml', 'chicago/4d/tools/smoke_renderer.mjs']
    plan = {
        'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'repository': REPO, 'pr': 1229, 'branch': BRANCH, 'head': head,
        'workflow_file': WORKFLOW, 'workflow_id': 365585058,
        'status': 'PENDING_RESULTS', 'runs': [],
        'scope': 'Fresh current-head all15parts at mobile390x780 and desktop1280x800. Historical tested5eae proofs remain historical after real Wheeler dev geometry. No gate/assertion/workflow/timeout changes. Dispatch is not a pass or merge authorization.',
        'contract_sha256': {p: hashlib.sha256((CHECKOUT / p).read_bytes()).hexdigest() for p in contract_paths},
    }


def save():
    PLAN.write_text(json.dumps(plan, indent=2) + '\n')


jobs = [('desktop', '13'), ('mobile', '13')] + [(v, s) for s in ['1-4', '5-8', '9-12', '14-15'] for v in ['mobile', 'desktop']]
for viewport, stage in jobs:
    if any(r['viewport'] == viewport and r['stage'] == stage for r in plan['runs']):
        continue
    assert remote_head() == head, 'Source branch advanced; stop mixed-head dispatch.'
    before = {r['id'] for r in listing()}
    request = {'ref': BRANCH, 'inputs': {'viewport': viewport, 'stage': stage}}
    plan['pending_dispatch'] = {'viewport': viewport, 'stage': stage, 'before_ids': sorted(before), 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    save()
    subprocess.run(['gh', 'api', '-X', 'POST', f'repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches', '--input', '-'], input=json.dumps(request), text=True, capture_output=True, check=True)
    matches = []
    for _ in range(20):
        matches = [r for r in listing() if r['id'] not in before and r['head_sha'] == head]
        if matches:
            break
        time.sleep(2)
    assert len(matches) == 1, f'Ambiguous dispatch receipt: {len(matches)}. Pending receipt remains on disk.'
    run = matches[0]
    parts = [13] if stage == '13' else list(range(int(stage.split('-')[0]), int(stage.split('-')[1]) + 1))
    row = {'viewport': viewport, 'stage': stage, 'parts': parts, 'id': run['id'], 'url': run['html_url'], 'head': run['head_sha'], 'request': request}
    plan['runs'].append(row)
    plan.pop('pending_dispatch')
    save()
    print(json.dumps(row), flush=True)

assert len(plan['runs']) == 10
for viewport in ['mobile', 'desktop']:
    assert sorted(p for r in plan['runs'] if r['viewport'] == viewport for p in r['parts']) == list(range(1, 16))
plan['dispatch_complete'] = True
save()
print('All ten exact-head jobs dispatched. Results and merge readiness remain unverified.', flush=True)
