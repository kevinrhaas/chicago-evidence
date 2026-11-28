"""Map fresh automatic checks while retaining exact source-equivalent manual IDs."""
import datetime
import json
import re
from pathlib import Path

from vegetation_github_api_read import read as api
from vegetation_dev_5d1_render_input_equivalence import manual_source_equivalence

W = Path('/workspace/work')
P = 'vegetation-dev-5d1'
read = lambda p: json.loads(Path(p).read_text())
path = W/(P+'-push-dispatch.json')
push = read(path)
proof = read(W/push['integration_proof'])
binding = manual_source_equivalence(proof)
assert push['pushed'] and binding == push['manual_source_equivalence']
head = push['head']
checks = api(f'repos/kevinrhaas/chicago/commits/{head}/check-runs?per_page=100')
assert checks['total_count'] <= 100
ids = set()
for check in checks['check_runs']:
    assert check['head_sha'] == head
    match = re.match(r'https://github.com/kevinrhaas/chicago/actions/runs/(\d+)(?:/|$)',
                     check.get('details_url') or '')
    if match:
        ids.add(int(match[1]))
runs = [api(f'repos/kevinrhaas/chicago/actions/runs/{i}') for i in sorted(ids)]
assert all(r['head_sha'] == head and r['head_branch'] == push['branch'] for r in runs)
expected = {'native', 'portable_humans', 'moving_upload'}
for name, filename, event in [
    ('native', 'chicago-4d-check.yml', 'pull_request'),
    ('portable_humans', 'chicago-4d-humans.yml', 'pull_request'),
    ('moving_upload', 'chicago-4d-moving-frames.yml', 'pull_request'),
    ('stuck_report', 'chicago-4d-pr-stuck.yml', 'push'),
    ('content_build', 'chicago-4d-bake.yml', 'push'),
]:
    found = [r for r in runs if r['path'] == '.github/workflows/'+filename and r['event'] == event]
    if not found:
        # A pending concurrency slot can exist before GitHub creates any
        # check-run/job. Bind that already-created run; never dispatch a copy.
        pending = api('repos/kevinrhaas/chicago/actions/workflows/'+filename+
                      f'/runs?head_sha={head}&event={event}&per_page=10')
        found = [r for r in pending['workflow_runs'] if r['head_sha'] == head
                 and r['head_branch'] == push['branch'] and r['event'] == event]
    assert len(found) <= 1, (name, [r['id'] for r in found])
    if found:
        push['ci_runs'][name] = found[0]['id']
        push['run_source_heads'][name] = head
        if name in push['source_equivalent_run_names']:
            push['source_equivalent_run_names'].remove(name)
        expected.add(name)
    elif name == 'content_build' and name in push['ci_runs']:
        expected.add(name)
plan = read(W/push['manual_dispatch_plan'])
expected |= {row['name'] for row in plan['dispatches']}
old = read(W/(push['manual_source_prefix']+'-push-dispatch.json'))
for name in push['source_equivalent_run_names']:
    assert push['ci_runs'][name] == old['ci_runs'][name]
    assert push['run_source_heads'][name] == old['head'] == binding['manual_tested_head']
push.update(all_required_run_ids_confirmed=set(push['ci_runs']) == expected,
            last_run_reconciliation_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
path.write_text(json.dumps(push, indent=2)+'\n')
(W/'vegetation-m2-final-push-dispatch-receipt.json').write_text(json.dumps(push, indent=2)+'\n')
folder = W/(P+'-final-ci')
folder.mkdir(exist_ok=True)
for name, run_id in sorted(push['ci_runs'].items()):
    run = api(f'repos/kevinrhaas/chicago/actions/runs/{run_id}')
    assert run['head_sha'] == push['run_source_heads'][name]
    (folder/(name+'-run.json')).write_text(json.dumps(run, indent=2)+'\n')
    print(name, run_id, run['head_sha'][:9], run['status'], run['conclusion'])
print('Missing:', sorted(expected-set(push['ci_runs'])))
