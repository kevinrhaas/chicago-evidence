"""ROOT-only continuation after the actual exact-tree complete preflight passes."""
import pathlib, subprocess, json, datetime, time, re, os

R = pathlib.Path('/workspace/chicago-waistcoat')
A = R / 'chicago/4d'
G = pathlib.Path('/workspace/shared/T2800-PR1244-COMBINED-EA22-FULL-PREFLIGHT-G11-ACTUAL-20261023')
O = pathlib.Path('/workspace/shared/T2800-PR1244-COMBINED-EA22-GREEN-COMMIT-PUSH-PUBLISH-20261023')
BASE = 'eb1cafe12b796ff3b63aecc74a9fa4ba946ca609'
TREE = '5e7406c5d29f8a2be26e77cf098127dad5a6049d'
INCOMING = 'ea22b3c3055d0c6d40f213273138103fbc98cee3'
BRANCH = 'steward/t2800-planted-standing-v16-dev-20261023'
env = os.environ.copy()
env['PATH'] = '/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin:/workspace/shared/chicago-tools/usr/bin:' + env['PATH']
env.update({k: '1' for k in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']})
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args], env=env).decode().strip()
def save(name, data):
    (O / name).write_text(json.dumps(data, indent=2) + '\n')
def run(name, command, data=None):
    t = time.monotonic()
    with (O / (name + '.log')).open('wb') as f:
        r = subprocess.run(command, cwd=A, env=env, input=data, stdout=f, stderr=subprocess.STDOUT)
    row = {'command': command, 'returncode': r.returncode, 'seconds': time.monotonic()-t, 'at': now()}
    save(name + '.json', row)
    print(json.dumps({'step': name, **row}), flush=True)
    assert r.returncode == 0, name
def guard():
    assert git('rev-parse', 'HEAD') == BASE
    assert git('branch', '--show-current') == BRANCH
    assert git('write-tree') == TREE
    assert git('rev-parse', 'MERGE_HEAD') == INCOMING
    assert not git('diff', '--name-only') and not git('ls-files', '-u')
    assert not git('ls-files', '--others', '--exclude-standard')

assert '--root-authorized' in __import__('sys').argv
gate = json.loads((G / 'RESULT.json').read_text())
assert gate['returncode'] == 0 and gate['head'] == BASE
assert gate['staged_tree'] == gate['final_staged_tree'] == TREE and gate['unstaged'] == []
strip = lambda b: re.sub(r'\x1b\[[0-9;]*m', '', b.decode(errors='replace'))
checklog = strip((G / 'preflight-check.log').read_bytes())
summaries = re.findall(r'CHECK (PASS|FAIL).*?— (\d+) steps', checklog)
assert summaries and summaries[-1][0] == 'PASS' and 'none red.' in checklog[-700:]
assert 'PREFLIGHT PASS' in strip((G / 'PRE-FLIGHT.log').read_bytes())[-1200:]
guard()
O.mkdir(exist_ok=False)
save('ACTUAL-FULLGATE-PASS.json', {**gate, 'actual_steps': int(summaries[-1][1]), 'selftests': re.findall(r'(\d+) of them are self-tests', checklog)[-1:]})
message = ('T-2800: integrate current DEV with the planted standing horse\n\n'
           'Add the licensed canonical-metre horse and reconstructed 26-joint planted body shift, actual drawn-yard support, selection/card and owned material/mixer lifetime. Preserve existing people, vehicles and UI. Keep photographic, walking, harness, occupied and riding acceptance open.\n\n'
           'Exclude unrelated recovery archives from the existing ticket-mirror fixture, retaining all ticket inputs and original mirror assertions; clean up a failed initial copy. Isolate default-CPU fixtures from caller limits and take the real mid-lap lock in the rebuild process, with an independent live-marker assertion. Emit fixture API states in Bash and preserve dry-run diagnostics. Verify the stale-case marker and retain full push refusal details. Preserve current DEV geometry, package and source changes; preserve the authored liberty union and canonically rebuild its five generated provenance outputs. Actual complete preflight passes on this combined tree.\n')
(O / 'COMMIT-MESSAGE.txt').write_text(message)
run('01-CANDIDATE', ['git', 'commit-tree', TREE, '-p', BASE, '-p', INCOMING], message.encode())
candidate = (O / '01-CANDIDATE.log').read_text().strip()
run('02-CANDIDATE-CHANGELOG', ['node', 'tools/check-changelog-entry.mjs', INCOMING, candidate])
run('03-CANDIDATE-IDS', ['node', 'tools/resolve_id_collisions.mjs', '--base', INCOMING, '--check'])
run('04-CANDIDATE-WHITESPACE', ['git', 'diff', '--check', INCOMING, candidate])
guard()
run('05-NORMAL-MERGE-COMMIT', ['git', 'commit', '-F', str(O / 'COMMIT-MESSAGE.txt')])
head = git('rev-parse', 'HEAD')
assert git('rev-parse', 'HEAD^{tree}') == TREE and git('show', '-s', '--format=%P', head) == BASE + ' ' + INCOMING
assert not git('status', '--porcelain')
save('COMMITTED.json', {'head': head, 'tree': TREE, 'parents': [BASE, INCOMING], 'at': now()})
run('06-IMMEDIATE-NORMAL-PUSH', ['git', 'push', '-u', 'origin', 'HEAD:refs/heads/' + BRANCH])
assert git('ls-remote', 'origin', 'refs/heads/' + BRANCH).split()[0] == head
save('PUSHED.json', {'head': head, 'tree': TREE, 'branch': BRANCH, 'at': now(), 'force': False})
for label, command in [
    ('07-HEAD-CHANGELOG', ['node', 'tools/check-changelog-entry.mjs', INCOMING, head]),
    ('08-HEAD-IDS', ['node', 'tools/resolve_id_collisions.mjs', '--base', INCOMING, '--check']),
    ('09-HEAD-WHITESPACE', ['git', 'diff', '--check', INCOMING, head]),
    ('10-POSTCOMMIT-PUBLISH', ['bash', 'tools/publish.sh']),
    ('11-POSTCOMMIT-MIRROR', ['node', 'tools/check_published.mjs']),
    ('12-POSTCOMMIT-SITE', ['python3', 'tools/validate.py', '--site']),
]:
    run(label, command)
assert git('rev-parse', 'HEAD') == head and not git('status', '--porcelain')
build = json.loads((R / 'site/4d/build.json').read_text())
assert head.startswith(build['version'])
save('TERMINAL.json', {'status': 'PASS', 'head': head, 'tree': TREE, 'parents': [BASE, INCOMING], 'branch': BRANCH, 'build': build, 'at': now(), 'PR_ready_or_merge': False})
print(json.dumps({'status': 'PASS', 'head': head, 'pushed': True, 'published': True}), flush=True)
