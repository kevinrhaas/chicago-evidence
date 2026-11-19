#!/usr/bin/env python3
"""Dispatch existing smoke groups only after verified complete exact-tree source coverage."""
import datetime
import hashlib
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
COVERAGE_VERIFIER = Path('/tmp/t3654-pre-browser-source-coverage-reviewed.py')
COVERAGE_PROOF = Path('/tmp/t3654-pre-browser-source-coverage.json')
COVERAGE_BINDINGS = Path('/tmp/t3654-pre-browser-bindings-6409-hosted-2-5-6.json')
COVERAGE_VERIFIER_SHA256 = '0b204f89658f4c35cb1124caf4685b037ead6048dc7dd94fd0e518dda4ab621b'
COVERAGE_BINDINGS_SHA256 = '5ae8a0ca71140cb95984bb83f5d40ab102d5a6dcd3f2625d428b588b9a352b08'
DECLARATIONS = Path(ROOT) / 'chicago/4d/tools/check.sh'

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

def require_complete_prebrowser(proof, sha):
    """This is source assertion coverage for browser sequencing, never hosted green."""
    rid = proof.get('hosted_run_id')
    if (proof.get('schema') != 't3654-pre-browser-source-coverage-v1'
            or proof.get('source_commit') != sha
            or proof.get('repository') != REPO or proof.get('pull_request') != 2198
            or type(rid) is not int or rid <= 0
            or proof.get('hosted_run_url') != f'https://github.com/{REPO}/actions/runs/{rid}'
            or not re.fullmatch(r'[a-f0-9]{40}', proof.get('source_tree', ''))
            or not re.fullmatch(r'[a-f0-9]{40}', proof.get('included_dev_base', ''))):
        raise SystemExit('Pre-browser source proof identity is invalid.')
    if (proof.get('source_check_coverage_complete') is not True
            or proof.get('ready_for_browser_queue') is not True
            or proof.get('hosted_gate_required_before_merge') is not True
            or proof.get('live_dispatch_checks_required') is not True
            or proof.get('declared_steps') != 1379
            or proof.get('covered_ordinals') != list(range(1, 1380))
            or proof.get('missing_ordinals') != []
            or proof.get('declaration_sha256') != hashlib.sha256(DECLARATIONS.read_bytes()).hexdigest()):
        raise SystemExit('Pre-browser source proof is incomplete or declarations changed.')
    if (proof.get('verifier_sha256') != COVERAGE_VERIFIER_SHA256
            or proof.get('bindings') != {'path': str(COVERAGE_BINDINGS), 'sha256': COVERAGE_BINDINGS_SHA256}):
        raise SystemExit('Pre-browser source proof was not made by the reviewed verifier and bindings.')
    excluded = proof.get('excluded_hosted_timeout_job_ids')
    if (not isinstance(excluded, list) or len(excluded) != len(set(excluded))
            or any(type(j) is not int for j in excluded)
            or excluded != []):
        raise SystemExit('Pre-browser source proof contains an unknown timeout exclusion.')
    return rid

def authorize_source(sha):
    summary = json.loads(SOURCE_SUMMARY.read_text())
    if summary.get('complete') is True:
        return 'hosted', summary, require_complete_source(summary, sha)
    if (summary.get('source_commit') != sha or summary.get('repository') != REPO
            or summary.get('pull_request') != 2198):
        raise SystemExit('Current hosted source record belongs to another tree or repository.')
    # Re-run the strict raw-artifact verifier. A saved ready boolean is insufficient.
    if not COVERAGE_VERIFIER.is_file() or not COVERAGE_BINDINGS.is_file():
        raise SystemExit('Complete source proof is unavailable; nothing dispatched.')
    if (hashlib.sha256(COVERAGE_VERIFIER.read_bytes()).hexdigest() != COVERAGE_VERIFIER_SHA256
            or hashlib.sha256(COVERAGE_BINDINGS.read_bytes()).hexdigest() != COVERAGE_BINDINGS_SHA256):
        raise SystemExit('The reviewed pre-browser verifier or explicit bindings changed.')
    try:
        run([sys.executable, str(COVERAGE_VERIFIER), '--bindings', str(COVERAGE_BINDINGS), '--require-complete'])
    except subprocess.CalledProcessError as exc:
        raise SystemExit('Pre-browser source verification is incomplete; nothing dispatched.\n'
                         + (exc.output or '')) from exc
    proof = json.loads(COVERAGE_PROOF.read_text())
    rid = require_complete_prebrowser(proof, sha)
    if (rid != summary.get('run_id')
            or proof['included_dev_base'] != summary.get('included_dev_base')):
        raise SystemExit('Pre-browser proof and current hosted source record disagree.')
    return 'pre-browser', proof, rid

def require_live_source(live, authority, kind, sha):
    url = authority['url'] if kind == 'hosted' else authority['hosted_run_url']
    if (live.get('headSha') != sha or live.get('headBranch') != BRANCH
            or live.get('url') != url):
        raise SystemExit('Live GitHub source run identity differs from the verified proof.')
    if kind == 'hosted':
        expected = {p['job_id'] for p in authority['parts']} | {authority['aggregate']['job_id']}
        passed = {j['databaseId'] for j in live['jobs']
                  if j['status'] == 'completed' and j['conclusion'] == 'success'}
        if (live.get('status') != 'completed' or live.get('conclusion') != 'success'
                or not expected <= passed):
            raise SystemExit('Live GitHub source run does not match complete hosted proof.')
        return
    allowed = set(authority['excluded_hosted_timeout_job_ids'])
    parts = [j for j in live['jobs'] if re.fullmatch(r'gate part [1-8]/8', j['name'])]
    if (len(parts) != 8 or {j['name'] for j in parts} != {f'gate part {n}/8' for n in range(1, 9)}
            or len({j['databaseId'] for j in parts}) != 8
            or any(j['status'] not in ('queued', 'in_progress', 'completed')
                   or j['conclusion'] == 'skipped' for j in parts)
            or any(j['name'] != 'gate' and j not in parts for j in live['jobs'])):
        raise SystemExit('Live source job inventory is incomplete or unexpectedly skipped.')
    failed_parts = [j for j in live['jobs'] if j['name'] != 'gate'
                    and j['conclusion'] not in (None, '', 'success', 'skipped')]
    if any(j['databaseId'] not in allowed or j['conclusion'] != 'failure' for j in failed_parts):
        raise SystemExit('A new hosted source failure or cancellation needs review before dispatch.')
    for job in live['jobs']:
        if job['name'] == 'gate' and job['conclusion'] not in (None, '', 'success'):
            # Current6409 has no permitted source failures or timeout exclusions.
            # A failed aggregate cannot authorize browser sequencing.
            if job['conclusion'] != 'failure' or not failed_parts:
                raise SystemExit('Hosted aggregate has an unexplained failure or cancellation.')
    if live.get('conclusion') not in (None, '', 'success', 'failure'):
        raise SystemExit('The live hosted source run was cancelled or otherwise invalidated.')

def main():
    sha = sys.argv[1] if len(sys.argv) == 2 else ''
    if not re.fullmatch(r'[a-f0-9]{40}', sha):
        raise SystemExit('Pass only the exact pushed task commit SHA; no bypass mode exists.')
    kind, authority, source_run = authorize_source(sha)
    if run(['git', 'rev-parse', 'HEAD']) != sha:
        raise SystemExit('Local HEAD differs from the requested frozen commit.')
    if run(['git', 'status', '--porcelain', '--untracked-files=no']):
        raise SystemExit('Tracked checkout changes remain; nothing dispatched.')
    if kind == 'pre-browser' and run(['git', 'rev-parse', 'HEAD^{tree}']) != authority['source_tree']:
        raise SystemExit('Local committed tree differs from the verified coverage union.')
    remote_sha = gh('api', f'repos/{REPO}/git/ref/heads/{BRANCH}', '--jq', '.object.sha')
    if remote_sha != sha:
        raise SystemExit('Remote branch differs from the requested frozen commit.')
    remote_base = gh('api', f'repos/{REPO}/git/ref/heads/dev', '--jq', '.object.sha')
    if remote_base != authority['included_dev_base']:
        raise SystemExit('The dev base has advanced beyond the verified source proof.')
    live = json.loads(gh('run', 'view', str(source_run), '--repo', REPO,
                         '--json', 'headSha,headBranch,status,conclusion,url,jobs'))
    require_live_source(live, authority, kind, sha)
    doc = json.loads(LEDGER.read_text())
    held = doc.get('source_task_commit')
    if held != sha:
        raise SystemExit('Ledger belongs to another commit.')
    if doc.get('dispatch_hold'):
        raise SystemExit('The coverage ledger still holds dispatch.')
    proof_path = SOURCE_SUMMARY if kind == 'hosted' else COVERAGE_PROOF
    doc['source_dispatch_authorization'] = {
        'kind': kind, 'source_commit': sha, 'proof': str(proof_path),
        'proof_sha256': hashlib.sha256(proof_path.read_bytes()).hexdigest(),
        'checked_at': stamp(), 'hosted_gate_required_before_merge': True,
    }
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
