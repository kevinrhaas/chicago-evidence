#!/usr/bin/env python3
"""Run the approved native owner verify argv, preserving every actual log and status."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,time
p=argparse.ArgumentParser();p.add_argument('--commands',type=Path,required=True);p.add_argument('--commands-sha',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
raw=a.commands.read_bytes();assert hashlib.sha256(raw).hexdigest()==a.commands_sha;spec=json.loads(raw);rows=spec['checks'];assert len(rows)==56 and len({r['owner']for r in rows[:53]})==53
a.out.mkdir(mode=0o700);state={'status':'ACTUAL_NATIVE_OWNER_CHECKS_RUNNING','commands':[],'expected_checks':56}
def save():(a.out/'ACTUAL-ALL-AFFECTED-CHECKS.json').write_text(json.dumps(state,indent=2)+'\n')
save()
for i,row in enumerate(rows,1):
    log=a.out/f'{i:02d}.log';actual={'owner':row['owner'],'argv':row['argv'],'origin':row['origin'],'status':'RUNNING','log':str(log)};state['commands'].append(actual);save();start=time.monotonic()
    with log.open('wb',buffering=0) as stream:
        result=subprocess.run(row['argv'],cwd='/tmp/chicago-horse-20261029/chicago/4d',env=os.environ,stdout=stream,stderr=subprocess.STDOUT)
    actual.update(status='PASS'if result.returncode==0 else'FAIL',returncode=result.returncode,seconds=time.monotonic()-start,log_bytes=log.stat().st_size,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest());save()
state['status']='ACTUAL_ALL_56_NATIVE_OWNER_AND_UPSTREAM_CHECKS_PASS'if all(r['returncode']==0 for r in state['commands']) else'NONPASS_ACTUAL_NATIVE_AFFECTED_CHECKS'
save();print(json.dumps({'status':state['status'],'checks':len(state['commands']),'failed':[r['owner'] for r in state['commands'] if r['returncode']]}));raise SystemExit(0 if state['status']=='ACTUAL_ALL_56_NATIVE_OWNER_AND_UPSTREAM_CHECKS_PASS'else 1)
