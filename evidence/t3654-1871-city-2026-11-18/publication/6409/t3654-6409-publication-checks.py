from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import time

app = Path('/workspace/chicago/chicago/4d')
out = Path('/tmp/t3654-6409-publication-receipt.json')
expected = '6409dda1222e1284e111ab0efde1c471f3284d60'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=app, text=True).strip()

assert git('rev-parse', 'HEAD') == expected
assert not git('status', '--porcelain', '--untracked-files=no')
receipt = {'head': expected, 'tree': git('rev-parse', 'HEAD^{tree}'),
           'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'checks': [], 'complete': False}
for name, command in [
    ('publish', ['bash', 'tools/publish.sh']),
    ('mirror', ['node', 'tools/check_published.mjs']),
    ('boot', ['node', 'tools/pack_boot_sidecars.mjs', '--check']),
]:
    log = Path(f'/tmp/t3654-6409-{name}.log')
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(['timeout', '--kill-after=5s', '590s', *command],
                                cwd=app, env=os.environ, stdout=stream,
                                stderr=subprocess.STDOUT)
    receipt['checks'].append({'name': name, 'command': command,
        'exit_code': result.returncode, 'duration_s': round(time.monotonic()-started, 3),
        'log': str(log), 'sha256': hashlib.sha256(log.read_bytes()).hexdigest()})
    out.write_text(json.dumps(receipt, indent=2)+'\n')
    print(f'{name}: exit {result.returncode}', flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
receipt['runtime_input_hash'] = subprocess.check_output(
    ['node', 'tools/dev-smoke-state.mjs', 'hash'], cwd=app, text=True).strip()
receipt['end_head'] = git('rev-parse', 'HEAD')
receipt['end_status'] = git('status', '--porcelain', '--untracked-files=no')
receipt['complete'] = receipt['end_head'] == expected and receipt['end_status'] == ''
receipt['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
out.write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2), flush=True)
raise SystemExit(0 if receipt['complete'] else 1)
