"""Read-only final qualification; never dispatches, pushes, or merges."""
import datetime, hashlib, json, subprocess, sys
from pathlib import Path
from vegetation_smoke_log_qualification import qualify_log
from vegetation_core_dev072_native import qualify as qualify_current_native
from vegetation_note_fold_composition import qualify_composition

W = Path('/workspace/work')
phase = sys.argv[1]
assert phase in ('core', 'm2')
prefix = 'vegetation-dev-2423'

def read(path):
    return json.loads(Path(path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def api(path):
    from vegetation_github_api_read import read as read_api
    return read_api('repos/kevinrhaas/chicago/' + path)

push = read(W/(prefix + '-push-dispatch.json'))
pre = read(W/(prefix + '-final-preflight.json'))
proof = read(W/pre['integration_proof'])
assert push['pushed'] and push['complete_dispatches']
head, base = push['head'], push['base']
assert pre['complete'] and pre['exit_code'] == 0 and pre['head'] == head
assert pre['base'] == base and proof['final_head'] == head
assert proof['complete'] and proof['full_upstream_preserved']
assert sha(pre['log']) == pre['log_sha256']
assert 'PREFLIGHT PASS' in Path(pre['log']).read_text(errors='replace')
repo = Path(proof['repo'])
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo,
                               text=True).strip() == head
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo,
                                   text=True).strip()
for path, digest in proof['source_sha256'].items():
    assert sha(repo/path) == digest, path
pr = api('pulls/' + str(push['pr']))
assert pr['head']['sha'] == head and pr['base']['ref'] == 'dev'
live_dev = subprocess.check_output(['git', 'ls-remote', 'origin',
                                    'refs/heads/dev'], cwd=repo, text=True).split()[0]
composition = qualify_composition('m2-dev2423', proof)
assert composition['complete'] and composition['live_dev'] == live_dev
plan = read(W/push['manual_dispatch_plan'])
assert plan['head'] == head and plan['branch'] == push['branch']
assert len(plan['dispatches']) == len(push['dispatches']) == 9
for planned, accepted in zip(plan['dispatches'], push['dispatches']):
    assert accepted['accepted'] and accepted['name'] == planned['name']
    assert accepted['input'] == planned['input'] and accepted['parts'] == planned['parts']
smokes = [x for x in plan['dispatches'] if x['workflow'] == 'chicago-4d-smoke.yml']
assert len(smokes) == 8
for viewport in ('mobile', 'desktop'):
    covered = [i for x in smokes if x['input']['inputs']['viewport'] == viewport
               for i in x['parts']]
    assert sorted(covered) == list(range(1, 16)), viewport
expected = {'native', 'moving_upload', 'standard_grid'} | {x['name'] for x in smokes}
expected |= {'content_build','stuck_report'} & set(push['ci_runs'])
if phase == 'core' or 'portable_humans' in push['ci_runs']:
    expected.add('portable_humans')
rows, missing = {}, sorted(expected - set(push['ci_runs']))
for name in sorted(expected & set(push['ci_runs'])):
    run = api('actions/runs/' + str(push['ci_runs'][name]))
    assert run['head_sha'] == head and run['head_branch'] == push['branch'], name
    rows[name] = {k: run[k] for k in ('id', 'head_sha', 'path', 'event', 'status',
                                     'conclusion', 'run_attempt', 'html_url')}
    filename = next((x['workflow'] for x in smokes if x['name'] == name), {
        'native': 'chicago-4d-check.yml', 'portable_humans': 'chicago-4d-humans.yml',
        'moving_upload': 'chicago-4d-moving-frames.yml',
        'content_build': 'chicago-4d-bake.yml',
        'stuck_report': 'chicago-4d-pr-stuck.yml',
        'standard_grid': 'chicago-4d-frame-time.yml'}.get(name))
    assert run['path'] == '.github/workflows/' + filename, name
logs, absent_logs = [], []
for row in smokes:
    path = W/(prefix + '-final-ci')/(row['name'] + '.log')
    meta = path.with_suffix('.json')
    if not path.exists() or not meta.exists():
        absent_logs.append(row['name'])
        continue
    retained = read(meta)
    assert retained['run_id'] == push['ci_runs'][row['name']]
    assert retained['head'] == head and retained['log_sha256'] == sha(path)
    result = qualify_log(path.read_text(errors='replace'),
                         row['input']['inputs']['viewport'],
                         row['input']['inputs']['stage'])
    logs.append({**result, 'name': row['name'], 'run_id': retained['run_id'],
                 'log': str(path), 'log_sha256': sha(path)})
native = read(W/'vegetation-roughness-channel-fix-native-qualification.json')
assert native['complete'] and native['all32_residues_exactly_once']
revalidated_native = qualify_current_native('vegetation-roughness-channel-fix', 'm2')
assert {k:v for k,v in revalidated_native.items() if k != 'time_utc'} == {
    k:v for k,v in native.items() if k != 'time_utc'}
assert native['candidate_tree'] == proof['native_candidate_tree']
cal_name = 'vegetation-roughness-channel-fix-calibrated-qualification.json'
current_head_calibration = read(W/cal_name)
from qualify_vegetation_roughness_channel_fix_calibration import qualify as requalify_calibration
checked = requalify_calibration('m2')
assert {k:v for k,v in checked.items() if k!='time_utc'} == {k:v for k,v in current_head_calibration.items() if k!='time_utc'}
assert current_head_calibration['complete'] and current_head_calibration['candidate_tree'] == native['candidate_tree']
assert current_head_calibration['required_cpu'] == 'AMD EPYC 7763 64-Core Processor' and current_head_calibration['required_cores'] == 4
assert current_head_calibration['required_real_profile_measured'] and current_head_calibration['all_actual_timing_results_passed'] and current_head_calibration['zero_page_errors']
from vegetation_dev_2423_source_inspection import qualify as qualify_render_inputs
render_input_equivalence = qualify_render_inputs(proof)
assert render_input_equivalence['complete']
from vegetation_pr_final_grid import qualify as qualify_stock_grid
stock_grid = qualify_stock_grid(prefix)
from vegetation_stock_frame_budget_audit import qualify as qualify_frame_budgets
frame_budget_audit = qualify_frame_budgets(prefix)
(W/(prefix+'-frame-budget-audit.json')).write_text(json.dumps(frame_budget_audit, indent=2)+'\n')
ci_green = not missing and all(r['status'] == 'completed' and
                              r['conclusion'] == 'success' for r in rows.values())
combined_native = None
if ci_green:
    from vegetation_pr_merge_native import qualify as qualify_actual_merge_native
    combined_native = qualify_actual_merge_native(prefix, composition)
out = {'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'phase': phase, 'head': head, 'base': base, 'pr': push['pr'],
       'live_dev': live_dev, 'dev_matches_validated_base': live_dev == base,
       'draft': pr['draft'], 'labels': [x['name'] for x in pr['labels']],
       'mergeable': pr['mergeable'], 'mergeable_state': pr['mergeable_state'],
       'missing_runs': missing, 'runs': rows, 'ci_green': ci_green,
       'missing_complete_raw_smoke_logs': absent_logs, 'smoke_logs': logs,
       'all15_exactly_once_both_viewports': not absent_logs and len(logs) == 8,
       'native_qualification': 'vegetation-roughness-channel-fix-native-qualification.json',
       'calibration_qualification': cal_name,
       'calibrated_source_to_authored_head': render_input_equivalence,
       'live_dev_composition': composition,
       'actual_combined_PR_native': combined_native,
       'complete_source_bound_stock_grid': stock_grid,
       'stock_frame_budget_audit': frame_budget_audit,
       'merge_candidate_ready': ci_green and not absent_logs and composition['complete'] and stock_grid['complete'] and bool(combined_native and combined_native['complete']),
       'scope': 'Read-only CI/source qualification. A live owned lap, current reviews '
                'and unresolved threads, current mergeable clean state, exact expected '
                'head, and final Dev composition must still be checked before squash. '
                'No older head, incomplete smoke body, or different CPU result is substituted.'}
(W/(prefix + '-merge-readiness.json')).write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('runs', 'smoke_logs', 'scope', 'live_dev_composition')}))
for name, row in rows.items():
    print(name, row['id'], row['status'], row['conclusion'])
