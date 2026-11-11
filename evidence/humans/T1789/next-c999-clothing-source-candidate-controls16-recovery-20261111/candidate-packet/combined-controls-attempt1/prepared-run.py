"""PREPARED ONLY. No execution until ROOT admits this exact pinned attempt."""
from pathlib import Path
import fcntl, hashlib, json, subprocess
P = Path(__file__).resolve().parent
plan = json.loads((P/'PLAN.json').read_text()); out = Path(plan['output'])
assert not any(out.iterdir()), 'Fresh attempt only; no automatic retry'
for row in plan['pins']:
    assert hashlib.sha256(Path(row['file']).read_bytes()).hexdigest() == row['sha256'], row['file']
lock = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
G = '/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(args): return subprocess.run(args, check=False).returncode
if call(['python3','-B',G,'capture',str(out/'before.json')]): raise SystemExit(1)
before = json.loads((out/'before.json').read_text())
reserve = dict(RAM_bytes=512*1024*1024, tmp_bytes=8*1024*1024,
    RAM_floor_bytes=4*1024**3, tmp_floor_bytes=1024**3, workspace_floor_bytes=512*1024**2)
allowed = (before['available_memory_bytes']-reserve['RAM_bytes'] >= reserve['RAM_floor_bytes']
    and before['tmp_free_bytes']-reserve['tmp_bytes'] >= reserve['tmp_floor_bytes']
    and before['workspace_free_bytes'] >= reserve['workspace_floor_bytes'])
with (out/'RESERVE.json').open('x') as stream: json.dump(dict(accepted=allowed, **reserve),stream,indent=2);stream.write('\n')
if not allowed:
    with (out/'CLOSED.json').open('x') as stream:
        json.dump(dict(accepted=False,status='NONPASS_RESOURCE_RESERVE_BEFORE_EXECUTION',test_execution=False,automatic_retry=False),stream,indent=2);stream.write('\n')
    raise SystemExit(1)
rc = call(['python3','-B','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(out/'command'),
    '--cwd','/workspace','--timeout','120','--','/tmp/ROOT-GATE-BIND-PREP-V2-20261110/with-cache.sh','--','bash',str(P/'cell.sh')])
post = call(['python3','-B',G,'capture',str(out/'after.json')])
pair = call(['python3','-B',G,'pair',str(out/'before.json'),str(out/'after.json'),str(out/'resources.json')])
r = json.loads((out/'command.result.json').read_text())
c = json.loads((out/'command.cleanup.json').read_text())
g = json.loads((out/'resources.json').read_text())
t = json.loads((out/'TEST-RESULT.json').read_text()) if (out/'TEST-RESULT.json').exists() else None
accepted = (rc == post == pair == 0 and r['returncode'] == 0 and not r['timed_out']
    and r['requested_timeout_seconds'] == r['effective_timeout_seconds'] == 120
    and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children']
    and g['accepted'] and t is not None and t['returncode'] == 0 and t['test_entry'] is not None
    and t['test_entry']['success'] and t['test_entry']['actual_tests'] == 16
    and t['source_301_head_tree_primary_native8_fixture_candidate19_protected7_preserved'])
closed = dict(status='SIXTEEN_SOURCE_CONTROLS_PASS_NATIVE_PENDING' if accepted else 'NONPASS_FIRST_FAILURE_STOP_NO_RETRY',
    accepted=accepted,result=r,cleanup=c,resources=g,reserve=reserve,test=t,
    plan_SHA256=hashlib.sha256((P/'PLAN.json').read_bytes()).hexdigest(),
    APP_mutations=False,native_fit_accepted=False,automatic_retry=False)
with (out/'CLOSED.json').open('x') as stream: json.dump(closed,stream,indent=2);stream.write('\n')
print(json.dumps(dict(status=closed['status'],accepted=accepted,seconds=r['seconds'],output=str(out))))
raise SystemExit(0 if accepted else 1)
