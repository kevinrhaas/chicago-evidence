#!/usr/bin/env python3
"""Real local Git/reference verifier controls only; no wrapper entrypoint/browser."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile

HERE = Path(__file__).parent
WRAPPER = HERE / 'run-pinned-native-memory-accepted-base.py'
OLD = Path('/tmp/run-pinned-native-memory-20261026.py')
REPO = Path('/tmp/chicago-photo-worker-t2793-20261026')
ACCEPTED = '373851d158a7b6fc701b9cae1a651aa4b3823f97'
spec = importlib.util.spec_from_file_location('accepted_native_memory', WRAPPER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
env = {**os.environ, 'GIT_NO_LAZY_FETCH': '1', 'GIT_OPTIONAL_LOCKS': '0'}
def git(*args):
    if args == ('show', ACCEPTED + ':chicago/4d/tools/memory_ceilings.json'):
        # External reference fixture only: root-controlled Git hydration is pending.
        # Compare the exact saved API content's Git blob to actual local tree metadata.
        data = (HERE / 'ACCEPTED-373851-memory_ceilings.json').read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        expected = subprocess.check_output(['git', 'rev-parse', ACCEPTED + ':chicago/4d/tools/memory_ceilings.json'], cwd=REPO, env=env).decode().strip()
        assert blob == expected == '3939da7c637d7e2195e63464abf4b66706435584'
        return data
    return subprocess.check_output(['git', *args], cwd=REPO, env=env)
checks = []
def check(name, assertion):
    assert assertion, name
    checks.append(name)
    print('PASS ' + name)
def rejects(name, action, expected):
    try:
        action()
    except expected:
        check(name, True)
    else:
        raise AssertionError(name)

reference, payloads = module.read_native_reference(git, ACCEPTED)
default, old_payloads = module.read_native_reference(git)
check('exact accepted commit pinned', reference['commit'] == ACCEPTED and reference['mode'] == 'explicit_accepted_base')
check('omitted accepted base preserves actual HEAD reference', default['commit'] == git('rev-parse', 'HEAD').decode().strip() and default['mode'] == 'HEAD_default')
check('actual current native files pass original HEAD reference check', module.verify_native_reference(REPO, git, default) == {name: row['sha256'] for name, row in default['files'].items()})
check('accepted native ceilings are exactly desktop1300/mobile400 MiB', reference['native_1904_ceilings_bytes'] == {'desktop': 1300 * 1048576, 'mobile': 400 * 1048576})
check('native measurement source unchanged between actual HEAD and accepted commit', payloads[module.METRIC_PATHS[0]] == old_payloads[module.METRIC_PATHS[0]])
check('accepted native ceiling change is separately recorded', payloads[module.METRIC_PATHS[1]] != old_payloads[module.METRIC_PATHS[1]])
for bad in ['DEV', 'HEAD', ACCEPTED[:12], 'g' * 40, ACCEPTED + ':path']:
    rejects('mutable/invalid base rejected: ' + bad, lambda bad=bad: module.read_native_reference(git, bad), ValueError)
with tempfile.TemporaryDirectory(prefix='reference-control-', dir=HERE) as tmp:
    fixture = Path(tmp)
    for path, data in payloads.items():
        f = fixture / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
    actual = module.verify_native_reference(fixture, git, reference, ACCEPTED)
    check('actual accepted file copies verified against immutable blobs/hashes', actual == {name: row['sha256'] for name, row in reference['files'].items()})
    rejects('accepted files rejected against historical HEAD', lambda: module.verify_native_reference(fixture, git, default), AssertionError)
    for path in module.METRIC_PATHS:
        f = fixture / path
        f.write_bytes(payloads[path] + b'\n')
        rejects('any current native byte change rejected: ' + path, lambda: module.verify_native_reference(fixture, git, reference, ACCEPTED), AssertionError)
        f.write_bytes(payloads[path])
    tampered = json.loads(json.dumps(reference))
    tampered['files'][module.METRIC_PATHS[0]]['sha256'] = '0' * 64
    rejects('reference receipt tampering rejected', lambda: module.verify_native_reference(fixture, git, tampered, ACCEPTED), AssertionError)
goal = 1125 * 1048576
for total, expected in [(goal - 1, True), (goal, False), (goal + 1, False)]:
    result = module.historical_desktop_comparison(total)
    check('old1125 comparison strict and non-gating: ' + str(total), result['actual_strictly_below_old_goal'] == expected and result['changes_native_gate_or_result'] is False)
old_text, text = OLD.read_text(), WRAPPER.read_text()
old_ast, new_ast = ast.parse(old_text), ast.parse(text)
def statement(tree, predicate):
    matches = [n for n in ast.walk(tree) if predicate(n)]
    assert len(matches) == 1
    return ast.dump(matches[0], include_attributes=False)
def assigned(name):
    return lambda n: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
for name in ['command', 'launch', 'intact', 'complete', 'rc']:
    # rc is assigned more than once; the gate's own conditional is compared below.
    if name == 'rc':
        continue
    check('original native/gate statement unchanged: ' + name, statement(old_ast, assigned(name)) == statement(new_ast, assigned(name)))
check('native child environment stripping unchanged', "env.pop('GIT_NO_LAZY_FETCH', None)" in text and "env.pop('CHICAGO_TICKETS_DIR', None)" in text)
check('native no-snapshot ordinary profile route retained', "'--gate', '--no-snapshot', '--year', '1904'" in text and "'--only', a.viewport" in text)
check('short scratch, full before/after snapshot, actual supervisor cleanup preserved', all(token in text for token in ["len(str(scratch)) > 30", 'before = snapshot()', 'after = snapshot()', "cleanup['cleanup_complete']", "cleanup['remaining_owned_children']"]))
result = {'status': 'PASS', 'controls': len(checks), 'scope': 'Native immutable-reference and frozen-source controls only; no wrapper entrypoint or browser', 'accepted_caps_reference_source': 'External exact-commit API blob verified against local accepted Git tree metadata; no Git hydration performed', 'actual_accepted_base_wrapper_end_to_end': 'UNRUN_WAITING_FOR_ROOT_CONTROLLED_GIT_HYDRATION', 'accepted_reference': reference, 'historical_HEAD_reference': default, 'old_wrapper_sha256': hashlib.sha256(OLD.read_bytes()).hexdigest()}
(HERE / 'WRAPPER-CONTROLS-RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(str(len(checks)) + ' wrapper controls PASS; no browser')
