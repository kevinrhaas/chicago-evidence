"""One GET-only PR/CI snapshot. Never dispatches, retries, cancels, or merges."""
import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = 'kevinrhaas/chicago'
FRAME = '.github/workflows/chicago-4d-frame-time.yml'
NATIVE = {'.github/workflows/chicago-4d-check.yml', FRAME,
          '.github/workflows/chicago-4d-moving-frames.yml',
          '.github/workflows/chicago-4d-humans.yml',
          '.github/workflows/chicago-4d-bake.yml'}
MATRIX = {'still-frame (desktop)', 'still-frame (mobile)', 'memory (1835, self-test)'} | {
    f'memory ({year}, {viewport})' for year in ['1812', '1835', '1904']
    for viewport in ['desktop', 'mobile']}
SUCCESS = MATRIX | {'gate', 'moving-frames', 'upload-release', 'humans', 'warranted', 'report'}
SKIP = {'bake', 'smoke', 'open-pr', 'publish-bundle', 'fresh-consumer', 'teamster-studies', 'dress-study'}


def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()


def get(endpoint):
    result = subprocess.run(['gh', 'api', f'repos/{REPO}/{endpoint}'], capture_output=True, timeout=45)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace').strip())
    return json.loads(result.stdout)


def sha256(raw): return hashlib.sha256(raw).hexdigest()


def native_log(job, attempt, folder):
    path = folder / f"job-{job['id']}-attempt-{attempt}.log"
    if not path.exists():
        result = subprocess.run(['gh', 'api', f"repos/{REPO}/actions/jobs/{job['id']}/logs"],
                                capture_output=True, timeout=45)
        if result.returncode: return {'unknown': result.stderr.decode(errors='replace').strip()}
        path.write_bytes(result.stdout)
    raw = path.read_bytes()
    content = re.sub(r'\x1b\[[0-9;]*m', '', raw.decode('utf-8-sig', errors='replace'))
    # Bind the native checkout before setup, not a git fixture later in check.sh.
    checkout = content.split('##[group]Run actions/setup', 1)[0]
    resolved_ref_shas = re.findall(r'(?m)^.*?Z ([0-9a-f]{40})\s*$', checkout)
    checkout_succeeded = any(step.get('name') == 'Run actions/checkout@v4'
        and step.get('status') == 'completed' and step.get('conclusion') == 'success'
        for step in job.get('steps', []))
    commits = re.findall(r'\[command\][^\n]*git log -1 --format=%H\r?\n[^\n]*?Z ([0-9a-f]{40})\s*(?:\r?\n|$)', checkout) if checkout_succeeded else []
    lines = [line for line in content.splitlines() if 'self-test |' not in line and re.search(
        r'CHECK (?:PASS|FAIL).*steps|PASS — every moving frame|PASS upload release:|'
        r'(?<![a-z])ok /(?:1812|1835|1904)/|memory over its ceiling|self-test (?:ok|FAILED) —|'
        r'every tier under its ceiling|THE CEILING IS BROKEN|warning title=still-frame ceiling|'
        r'(?i:human[^\n]{0,60}(?:PASS|FAIL)|(?:PASS|FAIL)[^\n]{0,60}human)', line)]
    return {'path': str(path), 'bytes': len(raw), 'sha256': sha256(raw),
            'actual_checkout_sha': commits[-1] if commits else None, 'native_lines': lines,
            'checkout_step_succeeded': checkout_succeeded, 'target_ref_resolution_shas': resolved_ref_shas}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sha', required=True, help='Actual checked public COMMIT SHA, not candidate TREE')
    parser.add_argument('--expected-tree')
    parser.add_argument('--pr', type=int, default=1649)
    parser.add_argument('--logs', action='store_true', help='Cache terminal native job logs and checkout bindings')
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('snapshots'))
    parser.add_argument('--log-cache', type=Path, help='Shared cache for the SAME pinned source/job IDs across immutable snapshot folders')
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.sha): parser.error('--sha must be a complete commit SHA')
    folder = args.out / args.sha
    folder.mkdir(parents=True, exist_ok=True)
    log_folder = args.log_cache or (folder / 'native-logs')
    log_folder.mkdir(exist_ok=True)
    endpoints = {'pr': f'pulls/{args.pr}', 'dev': 'git/ref/heads/dev',
                 'pinned_commit': f'git/commits/{args.sha}',
                 'checks': f'commits/{args.sha}/check-runs?per_page=100&filter=latest',
                 'runs': f'actions/runs?head_sha={args.sha}&per_page=100',
                 'status': f'commits/{args.sha}/status?per_page=100',
                 'reviews': f'pulls/{args.pr}/reviews?per_page=100'}
    result = {'opened_utc': utc(), 'GET_only': True, 'expected_public_commit': args.sha,
              'expected_tree': args.expected_tree, 'observations': {}, 'errors': {}}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending = {name: pool.submit(get, endpoint) for name, endpoint in endpoints.items()}
        for name, future in pending.items():
            try: result['observations'][name] = future.result()
            except Exception as error: result['errors'][name] = str(error)
    observed = result['observations']
    pr = observed.get('pr', {})
    commit = observed.get('pinned_commit', {})
    result['pinned_tree_matches'] = bool(commit) and (not args.expected_tree or commit['tree']['sha'] == args.expected_tree)
    result['public_pr_head_matches'] = pr.get('head', {}).get('sha') == args.sha
    if pr.get('merge_commit_sha') and pr.get('mergeable') and not pr.get('merged'):
        try: result['actual_github_merge_commit'] = get(f"git/commits/{pr['merge_commit_sha']}")
        except Exception as error: result['errors']['synthetic_merge'] = str(error)
    runs = observed.get('runs', {}).get('workflow_runs', [])
    result['run_jobs'] = []
    result['frame_runs'] = []
    for run in runs:
        if run.get('head_sha') != args.sha:
            result['errors'][f"run-{run['id']}"] = 'Run source differs from requested pinned commit'
            continue
        if run['path'] == FRAME: result['frame_runs'].append({key: run.get(key) for key in ['id', 'head_sha', 'status', 'conclusion', 'event', 'run_attempt']})
        try: jobs = get(f"actions/runs/{run['id']}/attempts/{run['run_attempt']}/jobs?per_page=100")
        except Exception as error:
            result['errors'][f"jobs-{run['id']}"] = str(error)
            continue
        if jobs['total_count'] != len(jobs['jobs']): result['errors'][f"jobs-{run['id']}"] = 'Job pagination incomplete'
        row = {'run': {key: run.get(key) for key in ['id', 'path', 'head_sha', 'status', 'conclusion', 'event', 'run_attempt']}, 'jobs': jobs['jobs']}
        for job in row['jobs']:
            if job.get('head_sha') != args.sha: result['errors'][f"job-{job['id']}"] = 'Job source differs from pinned commit'
            if args.logs and run['path'] in NATIVE and job['status'] == 'completed' and job['conclusion'] != 'skipped':
                job['saved_native_log'] = native_log(job, run['run_attempt'], log_folder)
        result['run_jobs'].append(row)
    checks = observed.get('checks', {}).get('check_runs', [])
    result['check_counts'] = dict(collections.Counter(f"{item['status']}/{item.get('conclusion')}" for item in checks))
    by_name = {item['name']: item for item in checks}
    result['missing_or_not_success'] = sorted(name for name in SUCCESS if by_name.get(name, {}).get('conclusion') != 'success')
    result['missing_or_not_expected_skip'] = sorted(name for name in SKIP if by_name.get(name, {}).get('conclusion') != 'skipped')
    result['unexpected_check_names'] = sorted(set(by_name) - SUCCESS - SKIP)
    result['duplicate_check_names'] = [name for name, count in collections.Counter(item['name'] for item in checks).items() if count > 1]
    result['terminal_nonpass'] = [{key: item.get(key) for key in ['id', 'name', 'status', 'conclusion', 'details_url']} for item in checks
                                if item['status'] == 'completed' and item['conclusion'] not in ['success', 'skipped']]
    result['metadata_state'] = 'EXPECTED_15_SUCCESS_7_SKIP' if not any(result[key] for key in [
        'missing_or_not_success', 'missing_or_not_expected_skip', 'unexpected_check_names',
        'duplicate_check_names', 'terminal_nonpass', 'errors']) else 'PENDING_OR_ROOT_REVIEW'
    frames = result['frame_runs']
    result['matrix_action'] = ('ROOT_RECONCILE_SOURCE_OR_GET_ERROR_NO_DISPATCH'
        if 'runs' in result['errors'] or not result['pinned_tree_matches'] or not result['public_pr_head_matches']
        else 'NEEDED_ONE_DISPATCH_AFTER_ROOT_SOURCE_RECONCILE' if not frames else 'RUN_EXISTS_NO_DUPLICATE_DISPATCH')
    checkout_shas = {job['saved_native_log'].get('actual_checkout_sha') for row in result['run_jobs'] for job in row['jobs'] if 'saved_native_log' in job} - {None}
    result['actual_native_checkout_commits'] = {}
    for checkout_sha in checkout_shas:
        try: result['actual_native_checkout_commits'][checkout_sha] = get(f'git/commits/{checkout_sha}')
        except Exception as error: result['errors'][f'checkout-{checkout_sha}'] = str(error)
    try: result['pr_after'] = get(f'pulls/{args.pr}')
    except Exception as error: result['errors']['pr_after'] = str(error)
    result['public_pr_head_stayed_fixed'] = result.get('pr_after', {}).get('head', {}).get('sha') == args.sha
    if not result['public_pr_head_stayed_fixed']: result['matrix_action'] = 'ROOT_RECONCILE_SOURCE_OR_GET_ERROR_NO_DISPATCH'
    if result['errors']: result['metadata_state'] = 'UNKNOWN_GET_ERROR_ROOT_REVIEW'
    result['closed_utc'] = utc()
    result['limits'] = ['Metadata counts are not native footer/source/review/lock qualification or merge authorization.',
                        'Different warranted decisions/job expansion require review; skipped never means a native pass.',
                        'Pinned source evidence stays pinned if DEV or the public PR head later moves.',
                        'No POST, dispatch, retry, cancellation, claim, push, or merge is implemented.']
    target = folder / (datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'snapshot': str(target), 'snapshot_sha256': sha256(target.read_bytes()),
                      **{key: result[key] for key in ['pinned_tree_matches', 'public_pr_head_matches', 'public_pr_head_stayed_fixed', 'check_counts', 'metadata_state', 'matrix_action', 'missing_or_not_success', 'missing_or_not_expected_skip', 'terminal_nonpass']},
                      'errors': result['errors']}))
    return 2 if result['errors'] else 0


if __name__ == '__main__': raise SystemExit(main())
