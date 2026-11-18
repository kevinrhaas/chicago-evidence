import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

APP = Path('/workspace/1871-isolation/chicago/4d')
ROOT = APP.parents[1]
OUT = Path('/tmp/t3654-isolation-proof')
OUT.mkdir(exist_ok=True)
rows = json.loads(Path('/tmp/t3654-isolation-declared-commands.json').read_text())
row = rows[int(sys.argv[1])]
stem = Path(row['tool']).stem
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt = {'tool': row['tool'], 'head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=APP,text=True).strip(),
           'app': str(APP), 'source_sha256': sha(APP/row['tool']), 'commands': [],
           'harbor_fix_sha256': sha(APP/'tools/trace_harbor_1869.py'),
           'census_before_sha256': sha(APP/'tools/step_isolation.json')}
probe = APP/'tools/isolation_probe'
env = dict(os.environ, ISOLATION_ROOT=str(ROOT), ISOLATION_OUT=str(OUT/f'{stem}-verified-probe.jsonl'),
           PYTHONPATH=str(probe)+(':'+os.environ['PYTHONPATH'] if os.environ.get('PYTHONPATH') else ''),
           NODE_OPTIONS='--require '+str(probe/'node_probe.js')+(' '+os.environ['NODE_OPTIONS'] if os.environ.get('NODE_OPTIONS') else ''))
Path(env['ISOLATION_OUT']).write_text('')
for n, item in enumerate(row['commands']):
    log = OUT/f'{stem}-command-{n}.log'
    start = time.time_ns()
    with log.open('w') as f:
        result = subprocess.run(['bash','-c',item['command']],cwd=APP,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=280)
    receipt['commands'].append({**item, 'exit_code': result.returncode, 'wall_seconds':(time.time_ns()-start)/1e9,
                                'log':str(log),'log_sha256':sha(log)})
    if result.returncode:
        (OUT/f'{stem}.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(log.read_text()[-8000:]); sys.exit(result.returncode)
before = set(Path('/tmp').glob('c4d-iso1-*'))
log = OUT/f'{stem}-measurement.log'
start = time.time_ns()
with log.open('w') as f:
    result = subprocess.run(['node','tools/measure_step_isolation.mjs','--tool',row['tool']],cwd=APP,
                            stdout=f,stderr=subprocess.STDOUT,timeout=280)
new = set(Path('/tmp').glob('c4d-iso1-*'))-before
assert result.returncode == 0 and len(new) == 1, (result.returncode, new)
raw = next(iter(new))/'probe.jsonl'
copied = OUT/f'{stem}-measurement-probe.jsonl'
shutil.copyfile(raw,copied)
def own_records(p):
    records = [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
    return [x for x in records if x.get('argv') and x['argv'][0].endswith(row['tool'])]
verified = own_records(Path(env['ISOLATION_OUT']))
measured = own_records(copied)
assert len(measured) >= len(row['commands']) and len(verified) >= len(row['commands']), (verified,measured)
assert {p for r in measured for p in r['wrote']} == {p for r in verified for p in r['wrote']}, (verified,measured)
receipt['measurement'] = {'command':'node tools/measure_step_isolation.mjs --tool '+row['tool'],
                          'exit_code':result.returncode,'wall_seconds':(time.time_ns()-start)/1e9,
                          'log':str(log),'log_sha256':sha(log),'raw_probe':str(copied),
                          'raw_probe_sha256':sha(copied),'verified_probe':env['ISOLATION_OUT'],
                          'verified_probe_sha256':sha(env['ISOLATION_OUT']),
                          'matching_processes':len(measured)}
receipt['measured_row'] = json.loads((APP/'tools/step_isolation.json').read_text())['tools'][row['tool']]
receipt['census_after_sha256'] = sha(APP/'tools/step_isolation.json')
(OUT/f'{stem}.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'tool':row['tool'],'commands':receipt['commands'], 'measurement':receipt['measurement'],
                  'measured_row':receipt['measured_row']},indent=2))
