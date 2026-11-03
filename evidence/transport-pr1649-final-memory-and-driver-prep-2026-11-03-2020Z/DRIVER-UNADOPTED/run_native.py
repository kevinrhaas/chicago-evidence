from pathlib import Path
import fcntl, importlib.util, json, os, subprocess, sys

D = Path(__file__).resolve().parent
APP = Path('/workspace/chicago-driver-motion-20261103/chicago/4d')
out = D / sys.argv[1]
out.mkdir(exist_ok=False)
lock = open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock', 'a+')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
spec = importlib.util.spec_from_file_location('guard', '/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
before = g.snapshot(); assert g.check(before)['accepted']
(out/'RESOURCES-BEFORE.json').write_text(json.dumps(before, indent=2)+'\n')
prefix = out/'native'
command = ['node', str(D/'native_seated_look.mjs'), str(APP), str(D/'generated'), str(out/'models')]
q = subprocess.run([sys.executable, '/workspace/.cloud-setup/transport-supervise.py', '--prefix', str(prefix), '--cwd', str(APP), '--timeout', '600', '--', *command], stdout=(out/'supervisor.stdout').open('xb'), stderr=subprocess.STDOUT)
result = json.loads(Path(str(prefix)+'.result.json').read_text())
cleanup = json.loads(Path(str(prefix)+'.cleanup.json').read_text())
after = g.snapshot(); resources = g.pair(before, after)
record = dict(returncode=q.returncode, result=result, cleanup=cleanup, resources=resources)
if (out/'models/RESULT.json').exists():
    record['native'] = json.loads((out/'models/RESULT.json').read_text())
record['passed'] = (q.returncode == result['returncode'] == 0 and not result['timed_out']
                    and result['effective_timeout_seconds'] == result['requested_timeout_seconds'] == 600
                    and result['timeout_override_reason'] is None and cleanup['cleanup_complete']
                    and not cleanup['remaining_owned_children'] and resources['accepted']
                    and record.get('native', {}).get('passed') is True)
(out/'RESOURCES-AFTER.json').write_text(json.dumps(after, indent=2)+'\n')
(out/'CLOSED.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(dict(passed=record['passed'], output=str(out), seconds=result['command_seconds'])))
raise SystemExit(0 if record['passed'] else 1)
