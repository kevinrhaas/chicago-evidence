"""Dispatch the authorized final matrix; preserve earlier smoke receipts verbatim."""
import datetime
import json
from pathlib import Path
import re
import subprocess
import sys
import time

manifest = Path('/workspace/audio-1812/ci-smoke-merged.json')
expected = sys.argv[1] if len(sys.argv) == 2 else ''
if not re.fullmatch('[0-9a-f]{40}', expected):
    sys.exit('Supply the reviewed pushed full merge SHA.')
repo, branch, workflow = 'kevinrhaas/chicago', 'steward/1812-seasonal-audio', 'chicago-4d-smoke.yml'

def gh(*args, body=None):
    result = subprocess.run(['gh', *args], input=None if body is None else json.dumps(body),
                            text=True, capture_output=True, check=True, timeout=45)
    return json.loads(result.stdout) if result.stdout.strip() else None

def head():
    return gh('api', f'repos/{repo}/git/ref/heads/{branch}')['object']['sha']

def runs():
    return gh('api', f'repos/{repo}/actions/workflows/{workflow}/runs?branch={branch}&event=workflow_dispatch&per_page=100')['workflow_runs']

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

if head() != expected:
    sys.exit('Remote branch is not the reviewed merge SHA; nothing dispatched.')
if manifest.exists():
    state = json.loads(manifest.read_text())
    if any(state.get(k) != v for k, v in [('repository',repo),('branch',branch),('workflow',workflow),('head_sha',expected)]):
        sys.exit('Existing merged manifest is bound to another revision; refusing overwrite.')
else:
    state = {'repository':repo, 'branch':branch, 'workflow':workflow, 'head_sha':expected,
             'created_at':stamp(), 'purpose':'fresh published smoke after merging DEV; no inherited verdicts',
             'runs':[{'viewport':viewport, 'stage':stage} for stage in ['13','8','14','15','1-2','3-4','5','6-7','9-12']
                     for viewport in ['mobile','desktop']]}

def save():
    temporary = manifest.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2) + '\n')
    temporary.replace(manifest)

save()
for row in state['runs']:
    if row.get('run_id'):
        if row.get('head_sha') != expected:
            sys.exit('Existing row has wrong SHA; inspect without redispatching.')
        continue
    if row.get('dispatch_started'):
        sys.exit('Dispatch lacks run ID; inspect accepted request before any retry to avoid duplicates.')
    if head() != expected:
        sys.exit('Remote head changed; refusing mixed-revision coverage.')
    before = {run['id'] for run in runs()}
    row['dispatch_started'] = stamp()
    row['requested_ref'] = branch
    row['expected_head_sha'] = expected
    save()
    gh('api', '--method', 'POST', f'repos/{repo}/actions/workflows/{workflow}/dispatches', '--input', '-',
       body={'ref':branch, 'inputs':{'viewport':row['viewport'], 'stage':row['stage']}})
    deadline = time.monotonic() + 55
    while time.monotonic() < deadline:
        fresh = [run for run in runs() if run['id'] not in before]
        if len(fresh) > 1:
            row['ambiguous_candidate_ids'] = [run['id'] for run in fresh]
            save()
            sys.exit('Concurrent dispatch ambiguity; inspect inputs before assigning coverage.')
        if fresh:
            run = fresh[0]
            row.update(run_id=run['id'], url=run['html_url'], head_sha=run['head_sha'],
                       head_branch=run['head_branch'], status=run['status'], conclusion=run.get('conclusion'),
                       run_attempt=run.get('run_attempt'), observed_at=stamp())
            save()
            if run['head_sha'] != expected or run['head_branch'] != branch:
                sys.exit('Accepted run differs from selected SHA/ref; recorded honestly, no further dispatch.')
            print(f"{row['viewport']} {row['stage']}: {row['url']} @ {run['head_sha']}", flush=True)
            break
        time.sleep(2)
    else:
        sys.exit('Accepted dispatch not visible yet; inspect before retry.')
    if head() != expected:
        sys.exit('Remote head moved after dispatch; recorded runs retain original tested SHA.')
state['dispatch_completed_at'] = stamp()
save()
print(f"Recorded {len(state['runs'])} fresh runs pinned to {expected}; verdicts pending.", flush=True)
