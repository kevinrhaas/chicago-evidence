#!/usr/bin/env python3
"""Finalize only the frozen347 local mobile cohort after its normal2–12 runner ends."""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('runner', '/tmp/t3658-final-mobile-runner-v2.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
root = Path('/tmp/t3658-347-mobile-2-12')
manifest_path = root / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
assert manifest['status'] == 'completed', 'Do not finalize an active/incomplete cohort'
assert [s['stage'] for s in manifest['stages']] == list(range(2, 13))
cfg = r.load_config('/tmp/t3658-347-mobile-2-12-config.json')
assert r.sha(r.canonical(cfg)) == manifest['config_sha256']
assert r.file_sha('/tmp/t3658-final-mobile-runner-v2.py') == manifest['runner_sha256']
baseline = json.loads((root / 'mirror-inventory.json').read_text())
assert r.sha(r.canonical(baseline)) == manifest['mirror_inventory_sha256']
assert manifest['mirror_final']['full_content_checked'] is True
assert manifest['mirror_final']['inventory_sha256'] == manifest['mirror_inventory_sha256']
assert manifest['quiet_final']['active_local_renderers'] == []
stage_rows = []
for row in manifest['stages']:
    assert row['status'] == 'passed' and row['exit_code'] == 0 and row['ended_utc']
    assert row['stop_signal'] is None
    receipt_path = root / f'mobile-{row["stage"]}-receipt.json'
    assert json.loads(receipt_path.read_text()) == row
    log = root / row['log']
    assert r.file_sha(log) == row['log_sha256']
    parsed = r.parse_log(log.read_text(errors='replace'), row['stage'], cfg['mirror'], 0)
    assert parsed['passed'] and parsed == row['validation']
    for key in ['provenance_before', 'provenance_after']:
        assert row[key]['head'] == cfg['expected_head']
        assert row[key]['git_tree'] == cfg['expected_tree']
        assert row[key]['harness_sha256'] == cfg['expected_harness_sha256']
        assert row[key]['source_main_sha256'] == cfg['expected_main_sha256']
        assert row[key]['published_main_sha256'] == cfg['expected_main_sha256']
    assert row['mirror_before']['metadata_sha256'] == row['mirror_after']['metadata_sha256']
    assert row['quiet_after']['active_local_renderers'] == []
    stage_rows.append({'stage': row['stage'], 'completion_kind': 'normal_supervisor_exit',
                       'exit_code': 0, 'actual_process_seconds': row['elapsed_seconds'],
                       'summary': parsed['summary'], 'counts': parsed['section_counts'],
                       'required_guards': parsed['required_guards'],
                       'receipt': str(receipt_path), 'receipt_sha256': r.file_sha(receipt_path),
                       'log': str(log), 'log_sha256': row['log_sha256']})
recovered_path = Path(cfg['prior_separate_recovery_receipt']['path'])
assert r.file_sha(recovered_path) == cfg['prior_separate_recovery_receipt']['sha256']
rec = json.loads(recovered_path.read_text())
kernel = next(p for p in rec['processes'] if p['pid'] == 234227)
assert kernel['kernel_exit_status'] == 0 and kernel['exit_code'] == 0 and kernel['state'] == 'Z'
assert rec['identity_proof']['start_difference_seconds'] < 1
assert rec['identity_proof']['timeout_pid_matches_durable_start_and_spawn_events'] is True
assert rec['full_mirror_after']['full_content_checked'] is True
assert rec['full_mirror_after']['inventory_sha256'] == manifest['mirror_inventory_sha256']
assert rec['provenance_after']['head'] == cfg['expected_head']
first_log = recovered_path.parent / 'mobile-1.log'
assert r.file_sha(first_log) == rec['log_sha256']
first = r.parse_log(first_log.read_text(), 1, cfg['mirror'], kernel['exit_code'])
assert first['passed'] and first == rec['validation']
stage_rows.insert(0, {'stage': 1, 'completion_kind': 'root_accepted_recovered_kernel_exit',
                     'exit_code': 0, 'actual_process_seconds': None,
                     'harness_reported_seconds': first['runtime']['seconds'],
                     'summary': first['summary'], 'counts': first['section_counts'],
                     'required_guards': first['required_guards'],
                     'receipt': str(recovered_path), 'receipt_sha256': r.file_sha(recovered_path),
                     'log': str(first_log), 'log_sha256': rec['log_sha256'],
                     'limitation': rec['limitation']})
current_pins = r.provenance(cfg)
current_inventory = r.mirror_checks(cfg, baseline)
quiet = r.assert_quiet()
out = Path('/tmp/t3658-347-mobile1-12-complete.json')
assert not out.exists(), 'Final immutable receipt already exists'
payload = {'generated_utc': r.now(), 'scope': 'Local mobile1–12 only; not the full renderer gate',
           'head': cfg['expected_head'], 'git_tree': cfg['expected_tree'],
           'harness_sha256': cfg['expected_harness_sha256'],
           'source_main_sha256': cfg['expected_main_sha256'], 'build': cfg['expected_build'],
           'completion_status': 'PASS, with stage1 explicitly recovered from kernel exit evidence',
           'normal_stages': list(range(2, 13)), 'recovered_stages': [1],
           'totals': {'passed': sum(s['summary']['passed'] for s in stage_rows),
                      'failed': sum(s['summary']['failed'] for s in stage_rows),
                      'staged_checks': sum(s['counts']['staged'] for s in stage_rows),
                      'repeated_always_on_checks': sum(s['counts']['always_on'] for s in stage_rows),
                      'normal_process_seconds': sum(s['actual_process_seconds'] or 0 for s in stage_rows)},
           'final_current_pin_check': current_pins, 'final_current_mirror_metadata': current_inventory,
           'runner_final_full_mirror_hash': manifest['mirror_final'], 'quiet_final': quiet,
           'normal_manifest': str(manifest_path), 'normal_manifest_sha256': r.file_sha(manifest_path),
           'stages': stage_rows,
           'limits': ['Stages13–15, desktop coverage and source/published/upload gates remain separate.',
                      'Stage1 has no invented normal supervisor exit or exact end timestamp.',
                      'Only completed stages count; original supervisor-interrupted evidence remains preserved.']}
r.durable_json(out, payload)
print(json.dumps({'receipt': str(out), 'sha256': r.file_sha(out), 'totals': payload['totals'],
                  'full_mirror_unchanged': True, 'active_renderers': quiet['active_local_renderers']}))
