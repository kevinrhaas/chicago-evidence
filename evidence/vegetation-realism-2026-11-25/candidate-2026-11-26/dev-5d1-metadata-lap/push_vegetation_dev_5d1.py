"""Push the exact metadata lap, preserving existing scene-test executions."""
import datetime
import json
import subprocess
from pathlib import Path

from vegetation_github_api_read import read as api
from vegetation_note_fold_composition import qualify_composition
from vegetation_dev_5d1_render_input_equivalence import manual_source_equivalence

W = Path('/workspace/work')
P = 'vegetation-dev-5d1'
M = 'vegetation-dev-31a'
read = lambda p: json.loads(Path(p).read_text())
proof = read(W/(P+'-final-integration-proof.json'))
pre = read(W/(P+'-final-preflight.json'))
old = read(W/(M+'-push-dispatch.json'))
binding = manual_source_equivalence(proof)
r = Path(proof['repo'])


def git(*args):
    return subprocess.check_output(['git', *args], cwd=r, text=True).strip()


head = proof['final_head']
assert pre['complete'] and pre['exit_code'] == 0 and pre['head'] == head
assert pre['base'] == proof['actual_dev']
assert git('rev-parse', 'HEAD') == head and not git('status', '--porcelain')
assert git('rev-parse', 'HEAD^{tree}') == proof['final_tree']
assert git('ls-remote', 'origin', 'refs/heads/'+old['branch']).split()[0] == old['head']
cp = read(W/'better-trees-current-checkpoint.json')
assert git('ls-remote', 'origin', 'refs/heads/lap/pr-2414').split()[0] == cp['process']['m2_lap_sha']
composition = qualify_composition('m2-dev5d1', proof)
assert old['pushed'] and old['complete_dispatches'] and old['all_required_run_ids_confirmed']
assert old['head'] == binding['manual_tested_head'] and old['pr'] == 2414
plan = read(W/old['manual_dispatch_plan'])
names = {row['name'] for row in plan['dispatches']}
assert len(names) == 9
if 'content_build' in old['ci_runs']:
    names.add('content_build')
native_id = old['ci_runs']['native']
native = api(f'repos/kevinrhaas/chicago/actions/runs/{native_id}')
jobs = api(f'repos/kevinrhaas/chicago/actions/runs/{native_id}/jobs?per_page=100')
assert native['head_sha'] == old['head']
failures = [j for j in jobs['jobs'] if j['status'] == 'completed'
            and j['conclusion'] not in ('success', 'skipped', 'neutral')]
inventory = {'head': old['head'], 'run': native, 'jobs': jobs['jobs'],
             'actual_failures': failures,
             'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'scope': 'Before the metadata lap push. Only the preceding automatic '
                      'Native run may be superseded by normal PR concurrency. '
                      'All manual smoke/stock jobs continue unchanged.'}
target_inventory = W/(P+'-preceding-native-inventory.json')
assert not target_inventory.exists()
target_inventory.write_text(json.dumps(inventory, indent=2)+'\n')
assert not failures, 'Retain and diagnose any actual failure before superseding Native'
receipt = {
    'pr': 2414, 'head': head, 'base': proof['actual_dev'], 'branch': old['branch'],
    'pushed': False, 'complete_dispatches': True,
    'manual_dispatch_plan': old['manual_dispatch_plan'],
    'dispatches': old['dispatches'], 'dispatches_issued_by_this_lap': 0,
    'manual_source_prefix': M, 'manual_source_equivalence': binding,
    'source_equivalent_run_names': sorted(names),
    'ci_runs': {k: old['ci_runs'][k] for k in sorted(names)},
    'run_source_heads': {k: old['head'] for k in sorted(names)},
    'all_required_run_ids_confirmed': False,
    'integration_proof': P+'-final-integration-proof.json',
    'final_preflight': P+'-final-preflight.json',
    'native_qualification': 'vegetation-roughness-channel-fix-native-qualification.json',
    'calibration_qualification': 'vegetation-roughness-channel-fix-calibrated-qualification.json',
    'live_dev_composition': composition,
    'scope': 'The entire scene/test/asset/data source equals the existingac69 '
             'manual executions; only exact official release notes differ. '
             'Their actual heads and runs remain unchanged. Fresh automatic '
             'Native and regressions must qualify this exact new PR head.',
}
target = W/(P+'-push-dispatch.json')
assert not target.exists()
global_path = W/'vegetation-m2-final-push-dispatch-receipt.json'
backup = W/(P+'-previous-global-push-receipt.json')
assert not backup.exists()
backup.write_bytes(global_path.read_bytes())


def save():
    target.write_text(json.dumps(receipt, indent=2)+'\n')
    global_path.write_text(json.dumps(receipt, indent=2)+'\n')


save()
subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/'+old['branch'],
                '--force-with-lease=refs/heads/'+old['branch']+':'+old['head']],
               cwd=r, check=True)
assert git('ls-remote', 'origin', 'refs/heads/'+old['branch']).split()[0] == head
receipt.update(pushed=True, time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
save()
print(json.dumps({'pushed': True, 'head': head, 'manual_jobs_preserved': True,
                  'new_manual_dispatches': 0}), flush=True)
