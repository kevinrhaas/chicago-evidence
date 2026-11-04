import datetime, hashlib, json, pathlib, re, subprocess, time

OUT = pathlib.Path(__file__).parent
HEAD = '27d52718290a2708f70ca536c6b796a83a936601'
PREFIX = 'repos/kevinrhaas/chicago/'
started = time.monotonic()
seen_logs = {int(path.name.split('-')[1]) for path in OUT.glob('job-*-receipt.json')}
seen_artifacts = {int(path.name.split('-')[1]) for path in OUT.glob('run-*-artifacts.json')}
last = None

def get(endpoint, path, binary=False):
    result = subprocess.run(['gh', 'api', PREFIX + endpoint], capture_output=True, timeout=50)
    path.write_bytes(result.stdout)
    if result.returncode:
        path.with_suffix(path.suffix + '.error.txt').write_bytes(result.stderr)
        raise RuntimeError(f'GET failed {endpoint}: rc={result.returncode}')
    if binary:
        return result.stdout
    return json.loads(result.stdout)

for iteration in range(40):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    snap = OUT / stamp
    snap.mkdir()
    try:
        pr = get('pulls/1693', snap / 'pr.json')
        if pr['head']['sha'] != HEAD:
            event = {'utc': stamp, 'status': 'PR_HEAD_CHANGED_DO_NOT_RETARGET_OLD_RUNS', 'watched_head': HEAD, 'actual_head': pr['head']['sha']}
            (OUT / 'HEAD-CHANGED.json').write_text(json.dumps(event, indent=2))
            print(json.dumps(event), flush=True)
            break
        dev = get('git/ref/heads/dev', snap / 'dev-ref.json')
        checks = get(f'commits/{HEAD}/check-runs?per_page=100', snap / 'checks.json')
        runs = get(f'actions/runs?head_sha={HEAD}&per_page=100', snap / 'runs.json')
        summary = {'utc': stamp, 'head': pr['head']['sha'], 'base': pr['base']['sha'],
                   'merge_commit_sha': pr.get('merge_commit_sha'), 'state': pr['state'],
                   'merged': pr['merged'], 'mergeable_state': pr['mergeable_state'],
                   'checks': [{k:c.get(k) for k in ('name','status','conclusion')} for c in checks['check_runs']],
                   'runs': [{k:r.get(k) for k in ('id','name','event','status','conclusion')} for r in runs['workflow_runs']],
                   'failed_steps': [], 'new_logs': [], 'current_DEV': dev['object']['sha'], 'merge_tree': None, 'feature_tree': 'f2d0bc74730766d3309a8b23900e39c112e1fffe', 'qualification': 'Local full4 qualifies featureTREEf2 against b622 only; remote PR workflows require an actual synthetic merge checkout.'}
        required = [f'gate part {k}/8' for k in range(1,9)] + ['gate','humans','moving-frames','upload-release']
        required += [f'still-frame ({v})' for v in ['desktop','mobile']] + [f'memory ({y}, {v})' for y in ['1812','1835','1904'] for v in ['desktop','mobile']] + ['memory (1835, self-test)']
        observed = {c['name']: c for c in checks['check_runs']}
        summary['missing_required_contexts'] = [name for name in required if name not in observed]
        merge = pr.get('merge_commit_sha')
        if merge:
            commit = get(f'git/commits/{merge}', snap / 'synthetic-merge.json')
            summary['merge_tree'] = commit['tree']['sha']
            summary['merge_parents'] = [p['sha'] for p in commit['parents']]
        for run in runs['workflow_runs']:
            rid = run['id']
            jobs = get(f'actions/runs/{rid}/jobs?per_page=100', snap / f'run-{rid}-jobs.json')
            for job in jobs['jobs']:
                failed_steps = [s for s in job.get('steps', []) if s.get('conclusion') in ('failure','timed_out','cancelled')]
                if failed_steps:
                    summary['failed_steps'].append({'job':job['name'], 'job_id':job['id'], 'steps':failed_steps})
                jid = job['id']
                if job['status'] == 'completed' and job.get('conclusion') != 'skipped' and jid not in seen_logs:
                    dest = OUT / f'job-{jid}.log'
                    try:
                        body = get(f'actions/jobs/{jid}/logs', dest, True)
                    except Exception as exc:
                        summary.setdefault('log_errors', []).append(str(exc))
                    else:
                        seen_logs.add(jid)
                        txt = body.decode(errors='replace')
                        footers = [line for line in txt.splitlines() if re.search(r'CHECK (PASS|FAIL)|checks passed|self.tests',line)][-12:]
                        checkout = [line for line in txt.splitlines() if HEAD in line or 'HEAD is now at' in line or ('git log' in line) or 'refs/remotes/pull/1693/merge' in line]
                        checkout_shas = sorted(set(re.findall(r'^\S+Z ([0-9a-f]{40})$', txt, re.M)))
                        record = {'job':job['name'], 'job_id':jid, 'conclusion':job['conclusion'],
                                  'log':str(dest), 'sha256':hashlib.sha256(body).hexdigest(),
                                  'footers':footers,'checkout_lines':checkout,'actual_checkout_sha_candidates':checkout_shas}
                        (OUT / f'job-{jid}-receipt.json').write_text(json.dumps(record,indent=2))
                        summary['new_logs'].append(record)
            if run['status'] == 'completed' and rid not in seen_artifacts:
                get(f'actions/runs/{rid}/artifacts?per_page=100', OUT / f'run-{rid}-artifacts.json')
                seen_artifacts.add(rid)
        (snap / 'summary.json').write_text(json.dumps(summary,indent=2))
        (OUT / 'LATEST.json').write_text(json.dumps(summary,indent=2))
        sig = json.dumps({k:v for k,v in summary.items() if k != 'utc'},sort_keys=True)
        if sig != last:
            print(json.dumps(summary),flush=True)
            last = sig
        else:
            print(json.dumps({'utc':stamp,'unchanged':True}),flush=True)
    except Exception as exc:
        print(json.dumps({'utc':stamp,'watch_error':repr(exc)}),flush=True)
    if time.monotonic() - started > 1200:
        break
    time.sleep(45)
print(json.dumps({'watch_closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'read_only':True}),flush=True)
