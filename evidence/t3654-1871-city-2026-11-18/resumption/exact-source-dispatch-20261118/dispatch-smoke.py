#!/usr/bin/env python3
"""Dispatch existing smoke groups only after the exact pushed commit's full source gate."""
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
SOURCE_SUMMARY = Path('/tmp/t3654-source-gate-summary.json')

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

def require_complete_source(summary, sha):
    """Reject stale, partial, or differently identified source proof before any mutation."""
    if summary.get('complete') is not True or summary.get('source_jobs_complete') is not True:
        raise SystemExit('Source gate coverage is not complete; nothing dispatched.')
    if summary.get('source_commit') != sha:
        raise SystemExit('Source gate proof belongs to another commit; nothing dispatched.')
    rid = summary.get('run_id')
    if (summary.get('schema') != 't3654-hosted-source-gate-v1'
            or summary.get('repository') != REPO
            or summary.get('pull_request') != 2198
            or type(rid) is not int or rid <= 0
            or not re.fullmatch(r'[a-f0-9]{40}', summary.get('included_dev_base', ''))
            or summary.get('url') != f'https://github.com/{REPO}/actions/runs/{rid}'):
        raise SystemExit('Source gate repository, pull request, or run identity is invalid.')
    parts = summary.get('parts', [])
    expected = {f'{n}/8' for n in range(1, 9)}
    if (len(parts) != 8 or {p.get('part') for p in parts} != expected
            or any(p.get('verified_pass') is not True
                   or p.get('status') != 'completed'
                   or p.get('conclusion') != 'success'
                   or type(p.get('job_id')) is not int
                   for p in parts)
            or len({p['job_id'] for p in parts}) != 8):
        raise SystemExit('Source gate lacks eight distinct verified successful part jobs.')
    aggregate = summary.get('aggregate') or {}
    if (aggregate.get('status') != 'completed'
            or aggregate.get('conclusion') != 'success'
            or type(aggregate.get('job_id')) is not int
            or summary.get('dispatch_hold')):
        raise SystemExit('Source aggregate is incomplete or dispatch remains held.')
    return rid

def main():
    sha = sys.argv[1] if len(sys.argv) == 2 else ''
    if not re.fullmatch(r'[a-f0-9]{40}', sha):
        raise SystemExit('Pass only the exact pushed task commit SHA; no bypass mode exists.')
    summary = json.loads(SOURCE_SUMMARY.read_text())
    source_run = require_complete_source(summary, sha)
    if run(['git', 'rev-parse', 'HEAD']) != sha:
        raise SystemExit('Local HEAD differs from the requested frozen commit.')
    if run(['git', 'status', '--porcelain', '--untracked-files=no']):
        raise SystemExit('Tracked checkout changes remain; nothing dispatched.')
    remote_sha = gh('api', f'repos/{REPO}/git/ref/heads/{BRANCH}', '--jq', '.object.sha')
    if remote_sha != sha:
        raise SystemExit('Remote branch differs from the requested frozen commit.')
    remote_base = gh('api', f'repos/{REPO}/git/ref/heads/dev', '--jq', '.object.sha')
    if remote_base != summary['included_dev_base']:
        raise SystemExit('The dev base has advanced beyond the verified source proof.')
    live = json.loads(gh('run', 'view', str(source_run), '--repo', REPO,
                         '--json', 'headSha,headBranch,status,conclusion,url,jobs'))
    expected_jobs = {p['job_id'] for p in summary['parts']} | {summary['aggregate']['job_id']}
    live_jobs = {j['databaseId'] for j in live['jobs']
                 if j['status'] == 'completed' and j['conclusion'] == 'success'}
    if (live.get('headSha') != sha or live.get('headBranch') != BRANCH
            or live.get('status') != 'completed' or live.get('conclusion') != 'success'
            or live.get('url') != summary['url'] or not expected_jobs <= live_jobs):
        raise SystemExit('Live GitHub source run does not match the complete exact-head proof.')
    doc = json.loads(LEDGER.read_text())
    held = doc.get('source_task_commit')
    if held != sha:
        raise SystemExit('Ledger belongs to another commit.')
    if doc.get('dispatch_hold'):
        raise SystemExit('The coverage ledger still holds dispatch.')
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
