#!/usr/bin/env python3
"""One explicitly opted-in canonical resident dispatch at an exact remote head."""
import datetime
import json
from pathlib import Path
import re
import subprocess
import sys
import time

if len(sys.argv) != 2 or not re.fullmatch(r'[0-9a-f]{40}', sys.argv[1]):
    raise SystemExit('pass the full committed and pushed SHA')
sha = sys.argv[1]
repo = 'kevinrhaas/chicago'
branch = 'steward/period-transport-2793'
workflow = 'chicago-4d-humans.yml'
out = Path('/workspace/shared') / ('human-probe-dispatch-' + sha[:9] + '.json')
if out.exists():
    raise SystemExit('dispatch receipt exists; reconcile without another POST')

def api(endpoint, body=None):
    args = ['gh', 'api', endpoint]
    if body is not None:
        args += ['--method', 'POST', '--input', '-']
    result = subprocess.run(args, input=None if body is None else json.dumps(body),
                            text=True, capture_output=True, check=True, timeout=60)
    return json.loads(result.stdout) if result.stdout.strip() else None

def head():
    return api(f'repos/{repo}/git/ref/heads/{branch}')['object']['sha']

def runs():
    return api(f'repos/{repo}/actions/workflows/{workflow}/runs?event=workflow_dispatch&per_page=100')['workflow_runs']

if head() != sha:
    raise SystemExit('remote branch head differs; no dispatch')
before = {row['id'] for row in runs()}
receipt = {'repository': repo, 'branch': branch, 'sha': sha, 'workflow': workflow,
           'inputs': {'build_teamsters': True}, 'before_run_ids': sorted(before),
           'requested_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'post_succeeded': False, 'coverage': 'UNPROVEN until terminal canonical jobs'}

def save():
    out.write_text(json.dumps(receipt, indent=2) + '\n')

save()
api(f'repos/{repo}/actions/workflows/{workflow}/dispatches',
    {'ref': branch, 'inputs': {'build_teamsters': 'true'}})
receipt['post_succeeded'] = True
save()
for attempt in range(10):
    found = [row for row in runs() if row['id'] not in before and row['head_sha'] == sha
             and row['head_branch'] == branch]
    receipt['runs'] = [{key: row[key] for key in ['id', 'head_sha', 'status', 'conclusion', 'html_url']}
                       for row in found]
    save()
    if len(found) == 1:
        break
    if len(found) > 1:
        raise SystemExit('multiple matching runs; reconcile without redispatching')
    time.sleep(3)
receipt['remote_head_after'] = head()
save()
if receipt['remote_head_after'] != sha or len(receipt.get('runs', [])) != 1:
    raise SystemExit('incomplete dispatch discovery; reconcile saved receipt without another POST')
print(json.dumps({'receipt': str(out), 'sha': sha, 'run': receipt['runs'][0]}))
