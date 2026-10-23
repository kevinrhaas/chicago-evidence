#!/usr/bin/env python3
"""Bounded GET-only observer. Metadata never proves stage coverage or merge readiness."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

REPO = 'kevinrhaas/chicago'
SMOKE = 'chicago-4d-smoke.yml'
CANONICAL = 'chicago-4d-humans.yml'
RANGES = ['1-2', '3-4', '5', '6-7', '8', '9-12', '13', '14', '15']
POLL_SECONDS = 60
MAX_SECONDS = 90 * 60
API_TIMEOUT_SECONDS = 45


def require(condition, message):
    if not condition:
        raise ValueError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def load_dispatches(smoke_path, canonical_path):
    smoke = json.loads(smoke_path.read_text())
    canonical = json.loads(canonical_path.read_text())
    sha = smoke.get('sha', '')
    require(re.fullmatch('[0-9a-f]{40}', sha), 'Full lowercase frozen SHA required')
    for record, workflow in [(smoke, SMOKE), (canonical, CANONICAL)]:
        require(record.get('repository') == REPO, 'Unexpected repository')
        require(record.get('sha') == sha, 'Dispatch SHA mismatch')
        require(record.get('workflow') == workflow, 'Unexpected workflow')
        require(record.get('branch') == smoke.get('branch') and bool(smoke.get('branch')), 'Dispatch branch mismatch')
        require(record.get('remote_head_after') == sha, 'Completed exact-head dispatch discovery required')
    dispatched = smoke.get('dispatches', [])
    grid = Counter((x.get('viewport'), x.get('stage')) for x in dispatched)
    require(grid == Counter((v, s) for v in ['mobile', 'desktop'] for s in RANGES), 'Exactly 18 requested grid cells required')
    require(all(x.get('post_succeeded') is True for x in dispatched), 'Incomplete smoke dispatch receipt')
    require(canonical.get('post_succeeded') is True and canonical.get('inputs', {}).get('build_teamsters') is True,
            'Canonical dispatch must explicitly request resident masters')
    runs = smoke.get('discovered_runs', [])
    human = canonical.get('runs', [])
    require(len(runs) == 18 and len(human) == 1, 'Exactly 18 discovered smoke runs and one canonical run required')
    expected = {}
    for record, workflow in [(x, SMOKE) for x in runs] + [(human[0], CANONICAL)]:
        run_id = record.get('id')
        require(type(run_id) is int and run_id > 0 and run_id not in expected, 'Duplicate/invalid discovered run ID')
        require(record.get('head_sha') == sha, 'Discovered run SHA mismatch')
        attempt = record.get('run_attempt', 1)
        require(type(attempt) is int and attempt > 0, 'Invalid explicit/default first run attempt')
        expected[run_id] = {'workflow': workflow, 'attempt': attempt}
    return smoke, canonical, sha, expected


# Only these JSON metadata routes can be issued. Never content/log/archive/artifact routes.
def allowed_endpoint(endpoint):
    prefix = rf'repos/{re.escape(REPO)}/'
    routes = [
        r'actions/workflows/chicago-4d-smoke\.yml/runs\?head_sha=[0-9a-f]{40}&event=workflow_dispatch&per_page=100',
        r'actions/runs/[1-9][0-9]*',
        r'actions/runs/[1-9][0-9]*/attempts/[1-9][0-9]*/jobs\?per_page=100',
        r'commits/[0-9a-f]{40}/check-runs\?per_page=100',
        r'pulls/[1-9][0-9]*',
    ]
    return any(re.fullmatch(prefix + route, endpoint) for route in routes)


class MetadataAPI:
    def __init__(self, deadline, out):
        self.deadline = deadline
        self.out = out
        self.count = 0

    def get(self, endpoint):
        require(allowed_endpoint(endpoint), 'Refused non-metadata endpoint')
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('90-minute observer wall reached before GET')
        self.count += 1
        timeout = min(API_TIMEOUT_SECONDS, remaining)
        with (self.out / 'metadata-requests.jsonl').open('a') as file:
            file.write(json.dumps({'at': now(), 'method': 'GET', 'endpoint': endpoint, 'timeout_seconds': timeout}) + '\n')
        # Any subprocess/JSON/API failure is fatal: no retry or fallback host.
        result = subprocess.run(['gh', 'api', '--hostname', 'github.com', '--method', 'GET', endpoint],
                                capture_output=True, text=True, timeout=timeout)
        if result.returncode:
            raise RuntimeError('Metadata GET failed; no retry: ' + (result.stderr.strip() or str(result.returncode)))
        return json.loads(result.stdout)


def run_meta(meta):
    fields = ['id', 'head_sha', 'head_branch', 'status', 'conclusion', 'run_attempt', 'event', 'path',
              'workflow_id', 'check_suite_id', 'created_at', 'updated_at', 'html_url', 'name', 'display_title']
    return {key: meta.get(key) for key in fields}


def validate_meta(meta, run_id, expected, sha, branch):
    require(meta.get('id') == run_id, 'Run ID mismatch')
    require(meta.get('head_sha') == sha and meta.get('head_branch') == branch, 'Observed run head/branch mismatch')
    require(meta.get('event') == 'workflow_dispatch', 'Observed run event mismatch')
    require((meta.get('path') or '').split('@')[0] == '.github/workflows/' + expected['workflow'], 'Workflow path mismatch')
    require(meta.get('run_attempt') == expected['attempt'], 'Run attempt changed; reconcile instead of silently accepting rerun')


def terminal_jobs(api, run_id, meta, expected, sha):
    attempt = expected['attempt']
    body = api.get(f'repos/{REPO}/actions/runs/{run_id}/attempts/{attempt}/jobs?per_page=100')
    jobs = body.get('jobs', [])
    require(type(body.get('total_count')) is int, 'Job list has no total_count')
    require(body['total_count'] == len(jobs), 'Terminal jobs truncated; no pagination/download fallback')
    required = {'smoke'} if expected['workflow'] == SMOKE else {'humans', 'teamster-studies'}
    rows = []
    for job in jobs:
        require(job.get('run_id') == run_id, 'Terminal job run mismatch')
        if 'head_sha' in job:
            require(job['head_sha'] == sha, 'Terminal job head mismatch')
        if 'run_attempt' in job:
            require(job['run_attempt'] == attempt, 'Terminal job attempt mismatch')
        row = {k: job.get(k) for k in ['id', 'name', 'run_id', 'head_sha', 'run_attempt', 'status', 'conclusion', 'html_url', 'started_at', 'completed_at']}
        row['steps'] = [{k: s.get(k) for k in ['name', 'number', 'status', 'conclusion']} for s in job.get('steps', [])]
        rows.append(row)
    names = Counter(x.get('name') for x in jobs)
    required_ok = all(names[name] == 1 and any(x['name'] == name and x['status'] == 'completed' and x['conclusion'] == 'success' for x in rows) for name in required)
    return {'run_id': run_id, 'attempt': attempt, 'head_sha': sha, 'collected_utc': now(), 'required_job_names': sorted(required),
            'required_jobs_completed_success': required_ok, 'jobs': rows, 'scope': 'Job/step metadata only; no logs or artifact inspection'}


def summary(snapshot, expected, jobs):
    runs = snapshot['runs']
    terminal = len(runs) == len(expected) and all(x['status'] == 'completed' for x in runs)
    workflows_success = terminal and all(x['conclusion'] == 'success' for x in runs)
    jobs_ok = terminal and all(jobs.get(str(x['id']), {}).get('required_jobs_completed_success') is True for x in runs)
    return {'all_19_selected_runs_terminal': terminal, 'all_19_selected_workflows_success': workflows_success,
            'all_selected_required_jobs_success': jobs_ok,
            'selected_metadata_success_only': workflows_success and jobs_ok and snapshot['pr_head_matches'],
            'coverage_proof_passed': False, 'coverage': 'UNPROVEN: no actual stage/viewport logs or assertion union inspected',
            'merge_qualified': False, 'artifact_content_inspected': False,
            'not_claimed': ['actual 18-cell run pairing', 'stage-union completeness', 'canonical artifact content/visual quality', 'all current checks green', 'merge readiness']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('smoke_dispatch', type=Path)
    parser.add_argument('--canonical', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--pr', type=int, default=1041)
    parser.add_argument('--max-seconds', type=int, default=MAX_SECONDS)
    args = parser.parse_args()
    require(0 < args.max_seconds <= MAX_SECONDS and args.pr > 0, 'Positive PR and at most 90-minute wall required')
    smoke, canonical, sha, expected = load_dispatches(args.smoke_dispatch, args.canonical)
    out = args.out.resolve()
    require(out.is_relative_to(Path('/workspace/shared').resolve()), 'Explicit outside shared evidence directory required')
    out.mkdir(parents=True, exist_ok=False)
    save(out / 'dispatch.json', smoke); save(out / 'canonical-dispatch.json', canonical)
    started = time.monotonic(); deadline = started + args.max_seconds
    api = MetadataAPI(deadline, out)
    jobs, attempted_jobs = {}, set()
    receipt = {'repository': REPO, 'sha': sha, 'branch': smoke['branch'], 'pr': args.pr, 'started_utc': now(),
               'limits': {'wall_seconds': args.max_seconds, 'poll_seconds': POLL_SECONDS, 'subprocess_timeout_seconds': API_TIMEOUT_SECONDS},
               'policy': 'GET-only whitelisted metadata; no logs/artifacts/downloads/POST/retries; any API failure stops',
               'coverage_proof_passed': False, 'coverage': 'UNPROVEN', 'merge_qualified': False, 'expected_runs': {str(k): v for k, v in expected.items()}}
    save(out / 'observer.json', receipt)
    final_exit = 1
    try:
        while time.monotonic() < deadline:
            cycle_started = time.monotonic()
            listing = api.get(f'repos/{REPO}/actions/workflows/{SMOKE}/runs?head_sha={sha}&event=workflow_dispatch&per_page=100')
            smoke_ids = {i for i, x in expected.items() if x['workflow'] == SMOKE}
            selected = {m['id']: m for m in listing.get('workflow_runs', []) if m.get('id') in smoke_ids}
            canonical_id = next(i for i, x in expected.items() if x['workflow'] == CANONICAL)
            selected[canonical_id] = api.get(f'repos/{REPO}/actions/runs/{canonical_id}')
            for run_id, meta in selected.items():
                validate_meta(meta, run_id, expected[run_id], sha, smoke['branch'])
            checks = api.get(f'repos/{REPO}/commits/{sha}/check-runs?per_page=100')
            pr = api.get(f'repos/{REPO}/pulls/{args.pr}')
            snapshot = {'at': now(), 'sha': sha, 'pr_head': pr['head']['sha'], 'pr_head_matches': pr['head']['sha'] == sha,
                        'pr_draft': pr.get('draft'), 'missing_run_ids': sorted(set(expected) - set(selected)),
                        'runs': [run_meta(m) for _, m in sorted(selected.items())],
                        'checks_total_count': checks.get('total_count'),
                        'check_list_truncated': checks.get('total_count', 0) != len(checks.get('check_runs', [])),
                        'check_runs': [{k: x.get(k) for k in ['id', 'name', 'head_sha', 'status', 'conclusion', 'html_url']} for x in checks.get('check_runs', [])]}
            with (out / 'snapshots.jsonl').open('a') as file:
                file.write(json.dumps(snapshot) + '\n')
            save(out / 'latest.json', snapshot)
            require(snapshot['pr_head_matches'], 'PR head changed; no stale-head qualification')
            for run_id, meta in sorted(selected.items()):
                if meta['status'] != 'completed' or run_id in attempted_jobs:
                    continue
                attempted_jobs.add(run_id)
                save(out / 'terminal-jobs-attempted.json', sorted(attempted_jobs))
                record = terminal_jobs(api, run_id, meta, expected[run_id], sha)
                jobs[str(run_id)] = record
                save(out / 'terminal-jobs.json', jobs)
                print(json.dumps({'kind': 'terminal_metadata', 'run': run_meta(meta), 'required_jobs_success': record['required_jobs_completed_success'],
                                  'coverage': 'UNPROVEN', 'merge_qualified': False}), flush=True)
            status = summary(snapshot, expected, jobs)
            receipt.update(status, latest_snapshot=snapshot, terminal_jobs=jobs, metadata_requests=api.count)
            save(out / 'observer.json', receipt)
            print(json.dumps({'kind': 'metadata_snapshot', 'at': snapshot['at'], 'statuses': dict(Counter(x['status'] for x in snapshot['runs'])),
                              'conclusions': dict(Counter(x['conclusion'] or 'pending' for x in snapshot['runs'])), 'missing_run_ids': snapshot['missing_run_ids'],
                              **status}), flush=True)
            if status['all_19_selected_runs_terminal']:
                receipt['stop_reason'] = 'all selected workflow runs terminal; metadata only'
                final_exit = 0 if status['selected_metadata_success_only'] else 1
                break
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(remaining, max(0, POLL_SECONDS - (time.monotonic() - cycle_started))))
        else:
            receipt['stop_reason'] = 'bounded wall expired; unfinished evidence stays unproven'
    except Exception as error:
        receipt.update(stop_reason='metadata error/refusal; stopped without retry', error=str(error))
        print(json.dumps({'kind': 'metadata_stop_no_retry', 'error': str(error), 'coverage': 'UNPROVEN', 'merge_qualified': False}), flush=True)
    finally:
        receipt.update(finished_utc=now(), elapsed_seconds=time.monotonic()-started, metadata_requests=api.count,
                       coverage_proof_passed=False, coverage='UNPROVEN', merge_qualified=False,
                       observer_exit_code=final_exit)
        save(out / 'observer.json', receipt)
    return final_exit


if __name__ == '__main__':
    raise SystemExit(main())
