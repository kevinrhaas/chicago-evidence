#!/usr/bin/env python3
"""Sequential owned browser qualification only. Never commits, merges, publishes or retries."""
import hashlib
import json
import pathlib
import subprocess
import time

ROOT = pathlib.Path('/workspace/chicago')
APP = ROOT / 'chicago/4d'
LOG = pathlib.Path('/workspace/.cloud-setup/logs/transport-recovery')
SUP = pathlib.Path('/workspace/.cloud-setup/transport-supervise.py')
STATE = LOG / '70b-browser-pipeline-attempt2-state.json'
PRIMARY_STATE = LOG / '70b-save-and-publish-reconciled-state.json'
SECONDARY_STATE = LOG / 'PR1278-PIN70b-save-and-push-WAITER2-state.json'
SECONDARY_GATE = LOG / 'PR1278-PIN70b-normal-full-PREFLIGHT1'
PREF = LOG / '70b-transport-ui-full-preflight-before-commit'
PUB = LOG / '70b-transport-ui-committed-head-publish'
FOCUS_PREFIX = LOG / '70b-transport-ui-focused-wrapping-attempt2'
FOCUS_OUTPUT = LOG / '70b-transport-ui-focused-wrapping-attempt2-output'
FOCUS = LOG / '70b-transport-ui-wrapping-preparation-v1/70b-transport-ui-focused-wrapping-guarded-v1.mjs'
PREP = LOG / '70b-transport-ui-matrix-preparation-v1'
MATRIX = LOG / '70b-transport-ui-matrix-run1'
DRIVER_PREFIX = LOG / '70b-transport-ui-matrix-run1-driver'
VERIFIER_PREFIX = LOG / '70b-transport-ui-independent-final-24-verifier'
PROOF = LOG / '70b-transport-ui-independent-final-24.json'
HASHES = {
    FOCUS: '6468cda54428199b8c5b6b627b326a35215d993062183040a6a779e692ffcf06',
    PREP / 'dev70b_transport_ui_matrix_common.py': '6e42184a1f4f2bf6cbc3a3628d73c22460fe7c8ddcc10a37ce3a63187316276c',
    PREP / 'dev70b_transport_ui_matrix_driver.py': 'd4033c207d33d211a3fa3b25e47e07e2209d6c83e017ed2f1ae092b418e012c7',
    PREP / 'dev70b_transport_ui_matrix_verify.py': '19bdcbb2ab3bc53501221456ee16d47120b7791dd148f0084d6bb050c13c1a4f',
    SUP: 'a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c',
}

def read(path):
    return json.loads(pathlib.Path(path).read_bytes())

def digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()

def save(path, obj):
    path = pathlib.Path(path)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(obj, indent=2) + '\n')
    temp.replace(path)

def phase(label, **fields):
    save(STATE, {'phase': label, 'observed_unix': time.time(), **fields})
    print(label, flush=True)

def closed(prefix):
    result = read(str(prefix) + '.result.json')
    cleanup = read(str(prefix) + '.cleanup.json')
    assert result['returncode'] == 0 and not result['timed_out'], (str(prefix), result)
    assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'], str(prefix)
    return result, cleanup

def supervised(prefix, cap, command):
    for suffix in ['.log', '.result.json', '.cleanup.json']:
        assert not pathlib.Path(str(prefix) + suffix).exists(), 'Do not overwrite an existing attempt'
    subprocess.run(['python3', str(SUP), '--prefix', str(prefix), '--cwd', str(APP),
                    '--timeout', str(cap), '--', *command], check=True)
    return closed(prefix)

def checkpoint_phase(label, **fields):
    path = pathlib.Path('/workspace/.cloud-setup/queue-session.json')
    q = read(path)
    q.update(current_phase=label, updated_at_unix=time.time(), **fields)
    save(path, q)

assert not STATE.exists(), 'Preserve earlier pipeline state; never relaunch automatically'
try:
    assert not FOCUS_OUTPUT.exists() and not MATRIX.exists() and not PROOF.exists()
    for path, expected in HASHES.items():
        assert digest(path) == expected, 'Reviewed helper changed: ' + str(path)
    phase('WAITING: actual primary publication and separate PR1278 fullgate/head-push closure; no browser launched')
    started = time.monotonic()
    while True:
        assert time.monotonic() - started < 7200, 'Resource handoff wait expired; explicit ROOT review required'
        try:
            primary, secondary = read(PRIMARY_STATE), read(SECONDARY_STATE)
        except (FileNotFoundError, json.JSONDecodeError):
            time.sleep(.5)
            continue
        assert not primary.get('phase', '').startswith('STOPPED:'), 'Primary continuation stopped'
        assert not secondary.get('phase', '').startswith('STOPPED:'), 'Secondary continuation stopped; ROOT must review resource handoff'
        if primary.get('phase', '').startswith('PASS:') and secondary.get('phase', '').startswith('PASS:'):
            closed(PUB)
            closed(PREF)
            closed(SECONDARY_GATE)
            break
        time.sleep(.5)
    binding = read(LOG / '70b-transport-ui-committed-gate-binding.json')
    head = binding['head']
    assert head == primary['head'] and len(head) == 40
    assert binding['tree'] == '9fa9511eabff9a0e42da32410edf09a8e3608889'
    assert binding['app_subtree'] == 'da9f71f6749ebf52e09ad51f673a9e4debbf4478'
    assert binding['incoming_dev'] == '70bcc4366a455a15f1e54e3edfce50c046c0ddce'
    phase('RUNNING: actual fresh focused browser proof; primary source/index/entire mirror FROZEN', head=head, focused_prefix=str(FOCUS_PREFIX))
    checkpoint_phase('H3 fresh focused browser RUNNING; source/index/entire mirror FROZEN',
                     head=head, tree=binding['tree'], app_subtree=binding['app_subtree'],
                     active_focused={'prefix': str(FOCUS_PREFIX), 'output': str(FOCUS_OUTPUT), 'head': head},
                     new_focused_helper={'path': str(FOCUS), 'sha256': HASHES[FOCUS], 'state': 'ACTUAL RUNNING', 'prefix': str(FOCUS_PREFIX), 'output': str(FOCUS_OUTPUT)},
                     primary_coordination_invariant='No primary ticket.mjs mutations, publish, derive, source/index writes during focused or matrix. All source and entire published mirror remain frozen. Other clones may perform metadata-only actions and evidence saves; no concurrent heavy job.')
    supervised(FOCUS_PREFIX, 3600, ['env', 'GIT_TRACE2_EVENT=' + str(LOG / '70b-focused-index-startup-diagnosis/attempt2-git-trace.jsonl'), 'node', str(FOCUS), '--execute-after-gate', '--expected-head', head,
                                  '--preflight-prefix', str(PREF), '--publish-prefix', str(PUB), '--output', str(FOCUS_OUTPUT)])
    focus = read(FOCUS_OUTPUT / 'FOCUSED-CURRENT-NOTES-RESULT.json')
    assert focus['result'] == 'PASS' and focus['expected_head'] == head
    assert focus['final_bindings_verified'] and focus['final_viewport_errors_verified']
    assert len(focus['viewports']) == 2 and all(v['errors'] == [] and not v.get('cleanup_error') for v in focus['viewports'])
    assert all(c['result'] == 'PASS' for c in focus['components'].values())
    assert read(FOCUS_OUTPUT / 'PUBLISHED-MANIFEST-BEFORE.json') == read(FOCUS_OUTPUT / 'PUBLISHED-MANIFEST-AFTER.json')
    pause_path = pathlib.Path('/workspace/.cloud-setup/transport-browser-resource-pause.json')
    pause = read(pause_path)
    assert pause['owner'] == 'root' and pause['reserved_for'] == 'PR1279-pinned70b-intake-and-PR1278-canonical-owner-quiet-window'
    released = LOG / '70b-root-browser-resource-reservation-release.json'
    assert not released.exists()
    save(released, {'actual_closed_focused_prefix': str(FOCUS_PREFIX), 'head': head,
                    'prior_owned_reservation': pause, 'released_unix': time.time(),
                    'state': 'Only ROOT-owned quiet reservation released after actual successful focused cleanup; no gate bypass.'})
    pause_path.unlink()
    phase('RUNNING: fresh source-bound24-leg browser matrix; zero inherited H330/C4 results', head=head, run_dir=str(MATRIX), driver_prefix=str(DRIVER_PREFIX))
    checkpoint_phase('H3 focused PASS; fresh24matrix RUNNING; source/index/entire mirror FROZEN',
                     smoke_driver_active=True, smoke_matrix_run_dir=str(MATRIX),
                     new_focused_helper={'path': str(FOCUS), 'sha256': HASHES[FOCUS], 'state': 'ACTUAL PASS; result0/cleanup0/finalbindings/errors PASS', 'prefix': str(FOCUS_PREFIX), 'output': str(FOCUS_OUTPUT)},
                     new_matrix_preparation={'directory': str(PREP), 'state': 'ACTUAL fresh24matrix RUNNING; zero results inherited from H330/C4'},
                     smoke_driver_supervisor_prefix=str(DRIVER_PREFIX), smoke_binding={'head': head, 'tree': binding['tree'], 'app_subtree': binding['app_subtree'], 'zero_inherited_results': True})
    supervised(DRIVER_PREFIX, 43200, ['python3', str(PREP / 'dev70b_transport_ui_matrix_driver.py'),
                                    '--execute-fresh-matrix', '--head', head, '--out', str(MATRIX),
                                    '--preflight-prefix', str(PREF), '--publish-prefix', str(PUB),
                                    '--focused-prefix', str(FOCUS_PREFIX), '--focused-output', str(FOCUS_OUTPUT)])
    phase('VERIFYING: actual matrix driver closed0/cleanup0; separate independent verification', head=head)
    supervised(VERIFIER_PREFIX, 600, ['python3', str(PREP / 'dev70b_transport_ui_matrix_verify.py'),
                                    '--head', head, '--run-dir', str(MATRIX), '--receipt', str(PROOF)])
    phase('PASS: actual focused/full24/independent verifier and all owned cleanup CLOSED; DEV merge still pending',
          head=head, run_dir=str(MATRIX), driver_prefix=str(DRIVER_PREFIX), verifier_prefix=str(VERIFIER_PREFIX),
          independent_proof=str(PROOF), independent_proof_sha256=digest(PROOF))
    checkpoint_phase('H3 focused/full24/independent verifier PASS; no DEV merge yet; ROOT endgame pending', smoke_driver_active=False)
except BaseException as error:
    phase('STOPPED: actual failure/interruption retained; no automatic retry or source transfer', error=str(error))
    raise
