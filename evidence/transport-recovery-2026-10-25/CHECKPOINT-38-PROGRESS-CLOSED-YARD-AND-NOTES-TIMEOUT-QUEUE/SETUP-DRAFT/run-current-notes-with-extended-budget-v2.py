#!/usr/bin/env python3
"""Explicit once-only unchanged-observer retry after a clean overall timeout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

SETUP = Path('/workspace/.cloud-setup')
LOG = SETUP / 'logs/transport-recovery'
OLD = LOG / 'current-deployed-final-observation-bundle1'
NEW = LOG / 'current-deployed-final-notes-extended-observation1'
HELPER = LOG / '20261025T2225-CURRENT-DEV-FOLDED-NOTES-PREPARATION-v4/observe-current-dev-folded-notes-v4.mjs'

def read(p):
    return json.loads(Path(p).read_bytes())

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

for prefix in [OLD / 'notes', LOG / 'current-deployed-final-observation-bundle1-driver']:
    result = read(str(prefix) + '.result.json')
    cleanup = read(str(prefix) + '.cleanup.json')
    assert cleanup['cleanup_complete'] and cleanup['remaining_owned_children'] == []
    if prefix == OLD / 'notes':
        assert result['timed_out'] is True, 'Only an actual overall timeout authorizes this prepared retry'

report = read(OLD / 'notes-output/RESULT.json')
assert report['viewports'][0]['result'] == 'PASS'
assert all(x['result'] == 'PASS' for x in report['assertions'])
assert all(not v['errors'] for v in report['viewports'])
termination_errors = [(v['label'], v.get('error')) for v in report['viewports'] if v.get('error')]
assert len(termination_errors) == 1
assert termination_errors[0][0] == 'desktop1280x800'
assert termination_errors[0][1].startswith('locator.evaluate: Target page, context or browser has been closed\n'), 'Only the actual deadline-induced terminal close error is explained by this retry'
assert not report.get('error')
assert sha(HELPER) == '4b3cdb40d83bb53791b5322a6ee2edbce71de13110a8f113f6a449b9914853ad'
assert os.access('/home/agent/.pki/nssdb/cert9.db', os.W_OK)
assert not Path(str(NEW) + '.log').exists()
assert not Path(str(NEW) + '-output').exists()

old = read(str(OLD / 'notes') + '.result.json')
command = old['command'].copy()
assert command[0] == 'node' and command[1] == str(HELPER)
output_index = command.index('--out') + 1
assert command[output_index] == str(OLD / 'notes-output')
command[output_index] = str(NEW) + '-output'
plan = {
    'reason': 'Earlier supervisor actually timed out with all completed assertions PASS and no observed errors; no assertions or app/settings changed',
    'old_result_sha256': sha(str(OLD / 'notes') + '.result.json'),
    'old_cleanup_sha256': sha(str(OLD / 'notes') + '.cleanup.json'),
    'old_timeout_induced_terminal_error_retained': termination_errors,
    'old_report_sha256': sha(OLD / 'notes-output/RESULT.json'),
    'helper_sha256': sha(HELPER),
    'only_command_difference': 'NEW output directory; unchanged observer/inputs/deployed-D/guards',
    'new_operational_cap_seconds': 3600,
    'command': command,
}
plan_file = LOG / 'CURRENT-NOTES-EXTENDED-BUDGET-EXECUTION-PLAN.json'
assert not plan_file.exists()
plan_file.write_text(json.dumps(plan, indent=2) + '\n')
sys.exit(subprocess.call([sys.executable, str(SETUP / 'transport-supervise.py'), '--prefix', str(NEW), '--cwd', '/workspace', '--timeout', '3600', '--', *command], cwd='/workspace'))
