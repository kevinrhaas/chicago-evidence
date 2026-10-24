#!/usr/bin/env python3
import hashlib, json, os, re, subprocess, time
from pathlib import Path

ROOT = Path('/workspace/chicago')
LOG = Path('/workspace/.cloud-setup/logs/transport-recovery')
MANIFEST = json.loads((LOG/'latest-dev-source-manifest.json').read_text())
OUT = LOG/'latest-dev-smoke-resume-binding.json'
assert not OUT.exists(), 'Preserve existing resume receipt and inspect before restarting'
original = json.loads((LOG/'latest-dev-smoke-batch-binding.json').read_text())
entries = {(x['viewport'], x['stage']): x for x in original['completed']}
state = {'head': MANIFEST['head'], 'tree': MANIFEST['tree'], 'status': 'running', 'started_unix': time.time(), 'completed': [], 'prior_batch_receipt': 'latest-dev-smoke-batch-binding.json', 'note': 'Original receipts remain unchanged. Persisted command return code, smoke completion and owned-child cleanup establish each leg. Outer120 with inner0 was reproduced using closed stdout; supervisor reporting fixed separately.'}

def save():
    tmp = OUT.with_suffix('.tmp')
    tmp.write_text(json.dumps(state, indent=2)+'\n')
    tmp.replace(OUT)

def verify_source():
    for key, ref in [('head', 'HEAD'), ('tree', 'HEAD^{tree}')]:
        assert subprocess.check_output(['git', 'rev-parse', ref], cwd=ROOT).decode().strip() == MANIFEST[key]
    subprocess.check_call(['git', 'diff', '--exit-code', 'HEAD'], cwd=ROOT, stdout=subprocess.DEVNULL)
    assert all(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest() == x['sha256'] for x in MANIFEST['files'])

def result(viewport, stage, outer, reused):
    prefix = LOG/f'latest-dev-smoke-{viewport}-{stage}'
    command = json.loads(Path(str(prefix)+'.result.json').read_text())
    cleanup = json.loads(Path(str(prefix)+'.cleanup.json').read_text())
    log = Path(str(prefix)+'.log').read_text(errors='replace')
    match = re.search(r'(\d+) staged-section check\(s\)', log)
    passed = command['returncode'] == 0 and not command['timed_out'] and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and match and int(match[1]) > 0 and 'SMOKE PASS' in log and 'zero page errors' in log
    assert passed, f'Command/log/cleanup did not establish pass: {viewport} {stage}'
    if not reused:
        assert outer == 0, f'New supervisor failed: {outer}'
    return {'viewport': viewport, 'stage': stage, 'command_returncode': command['returncode'], 'outer_returncode': outer, 'seconds': command['seconds'], 'staged_checks': int(match[1]), 'cleanup_complete': True, 'verified_pass': True, 'reused_persisted_receipts': reused, 'prefix': str(prefix)}

save()
try:
    for viewport in ['mobile', 'desktop']:
        stages = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13', '14', '15'] if viewport == 'mobile' else [str(x) for x in range(1, 16)]
        for stage in stages:
            verify_source()
            state['active'] = {'viewport': viewport, 'stage': stage}
            save()
            old = entries.get((viewport, stage))
            if old is not None:
                record = result(viewport, stage, old['returncode'], True)
                print(f'Retained verified smoke: {viewport} {stage}', flush=True)
            else:
                prefix = LOG/f'latest-dev-smoke-{viewport}-{stage}'
                print(f'Starting smoke: {viewport} {stage}', flush=True)
                outer = subprocess.call(['python3', '/workspace/.cloud-setup/transport-supervise.py', '--prefix', str(prefix), '--cwd', str(ROOT/'chicago/4d'), '--timeout', '1800', '--', 'env', f'SMOKE_VIEWPORT={viewport}', f'SMOKE_STAGE={stage}', 'node', 'tools/smoke_renderer.mjs', '--published'])
                record = result(viewport, stage, outer, False)
            state['completed'].append(record)
            state.pop('active', None)
            save()
    verify_source()
    assert len(state['completed']) == 24
    state['status'] = 'passed: all15stages/bothviewports; persisted command receipts verified'
    state['finished_unix'] = time.time()
    save()
except BaseException as error:
    state['status'] = 'stopped; inspect actual failure before resuming'
    state['error'] = str(error)
    save()
    raise
