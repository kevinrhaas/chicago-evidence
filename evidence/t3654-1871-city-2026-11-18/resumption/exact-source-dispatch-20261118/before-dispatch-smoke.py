#!/usr/bin/env python3
"""Dispatch existing smoke groups against an exact pushed commit or explicit checkpoint."""
import datetime
import json
from pathlib import Path
import re
import subprocess
import sys
import time

REPO = 'kevinrhaas/chicago'
BRANCH = 'steward/t3654-1871-city-baseline'
ROOT = '/workspace/chicago'
LEDGER = Path('/tmp/t3654-legacy-coverage-ledger.json')

def run(args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()

def gh(*args):
    return run(['/usr/bin/gh', *args])

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(doc):
    temporary = LEDGER.with_suffix('.next.json')
    temporary.write_text(json.dumps(doc, indent=2) + '\n')
    temporary.replace(LEDGER)

def runs():
    return json.loads(gh('run', 'list', '--repo', REPO, '--workflow',
                        'chicago-4d-smoke.yml', '--branch', BRANCH,
                        '--event', 'workflow_dispatch', '--limit', '30',
                        '--json', 'databaseId,headSha,status,conclusion,createdAt,url'))

def main():
    sha = sys.argv[1] if len(sys.argv) in (2, 3) else ''
    checkpoint = len(sys.argv) == 3 and sys.argv[2] == '--validate-checkpoint'
    if len(sys.argv) == 3 and not checkpoint:
        raise SystemExit('Unknown mode.')
    if not re.fullmatch(r'[a-f0-9]{40}', sha):
        raise SystemExit('Pass the exact pushed task commit SHA.')
    if not json.loads(Path('/tmp/t3654-source-gate-summary.json').read_text()).get('complete'):
        if not checkpoint:
            raise SystemExit('Source gate coverage is not complete; nothing dispatched.')
        record = json.loads(run(['git', 'show', f'{sha}:chicago/4d/docs/measurements/t-3654-validation-checkpoint.json']))
        if record.get('state') != 'implementation_checkpoint_validation_pending':
            raise SystemExit('Commit does not declare its pending checkpoint validation.')
        print('Validating the explicitly requested GitHub checkpoint; local full source coverage remains pending.', flush=True)
    if run(['git', 'rev-parse', 'HEAD']) != sha:
        raise SystemExit('Local HEAD differs from the requested frozen commit.')
    remote_sha = gh('api', f'repos/{REPO}/git/ref/heads/{BRANCH}', '--jq', '.object.sha')
    if remote_sha != sha:
        raise SystemExit('Remote branch differs from the requested frozen commit.')
    doc = json.loads(LEDGER.read_text())
    held = doc.get('source_task_commit')
    if held not in ('pending_commit_after_source_gates', sha):
        raise SystemExit('Ledger belongs to another commit.')
    doc['source_task_commit'] = sha
    save(doc)
    for group in doc['ci_plan']:
        if group.get('run_id'):
            if group.get('head_sha') != sha:
                raise SystemExit('Existing run belongs to another commit.')
            continue
        if group['status'] != 'pending_dispatch':
            raise SystemExit('An unassigned dispatch needs reconciliation before retrying.')
        before = {row['databaseId'] for row in runs()}
        group.update(status='dispatching', dispatch_started_at=stamp(),
                     dispatch_prior_ids=sorted(before))
        save(doc)
        gh('workflow', 'run', 'chicago-4d-smoke.yml', '--repo', REPO,
           '--ref', BRANCH, '-f', f"viewport={group['viewport']}",
           '-f', f"stage={group['stage']}")
        deadline = time.monotonic() + 40
        while True:
            fresh = [row for row in runs() if row['databaseId'] not in before]
            if len(fresh) > 1:
                raise SystemExit('Multiple new runs need manual reconciliation; no next dispatch.')
            if fresh:
                row = fresh[0]
                if row['headSha'] != sha:
                    raise SystemExit('Dispatched run SHA differs; no next dispatch.')
                group.update(run_id=row['databaseId'], head_sha=row['headSha'],
                             status=row['status'], conclusion=row['conclusion'],
                             created_at=row['createdAt'], url=row['url'])
                save(doc)
                print(f"{group['viewport']} {group['stage']}: {row['databaseId']} {row['status']}", flush=True)
                break
            if time.monotonic() >= deadline:
                raise SystemExit('Run not yet listed; reconcile recorded dispatch before retrying.')
            time.sleep(2)

if __name__ == '__main__':
    main()
