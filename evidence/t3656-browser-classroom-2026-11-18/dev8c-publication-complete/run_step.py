import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

label, cwd, *command = sys.argv[1:]
root = Path('/tmp/t3656-af-prefire-validation')
log = root / (label + '.log')
receipt = root / (label + '.receipt.json')
if log.exists() or receipt.exists():
    raise SystemExit('Refusing to overwrite existing receipt: ' + label)
environment = os.environ.copy()
environment['PATH'] = '/tmp/chicago-check-runtime/node_modules/node/bin:/tmp/chicago-check-runtime/bc/usr/bin:' + environment['PATH']
start = time.monotonic()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
with log.open('w') as out:
    result = subprocess.run(['timeout', '--signal=TERM', '--kill-after=5s', '595s', *command], cwd=cwd, env=environment, stdout=out, stderr=subprocess.STDOUT)
data = {'label':label, 'cwd':cwd, 'command':command, 'started_at_utc':started,
        'ended_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'elapsed_seconds':round(time.monotonic()-start,3), 'exit_code':result.returncode,
        'cap_seconds':595, 'kill_after_seconds':5, 'log':str(log)}
receipt.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
print('\n'.join(log.read_text(errors='replace').splitlines()[-20:]))
raise SystemExit(result.returncode)
