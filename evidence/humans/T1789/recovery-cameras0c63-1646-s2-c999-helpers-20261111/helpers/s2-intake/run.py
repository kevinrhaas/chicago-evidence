"""Prepared only; ROOT explicitly admits each finite metadata/download/validate cell."""
from pathlib import Path
import fcntl,hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
mode=sys.argv[1];assert mode in ['metadata','download','validate']
prefix=P/mode
assert not any(Path(str(prefix)+'.'+s).exists() for s in ['before.json','log','result.json','CLOSED.json']), 'No overwrite or automatic retry'
pins=json.loads((P/'PREPARED.json').read_text())['files']
for name in ['intake.py','EXPECTED.json']:
    assert hashlib.sha256((P/name).read_bytes()).hexdigest()==pins[name]['sha256']
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(args):return subprocess.run(args,check=False).returncode
if call(['python3',G,'capture',str(prefix)+'.before.json']):raise SystemExit(1)
command=['python3',str(P/'intake.py'),*sys.argv[1:]]
if mode!='metadata':command+=['--guard-before',str(prefix)+'.before.json']
rc=call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd','/workspace','--timeout','120','--',*command])
post=call(['python3',G,'capture',str(prefix)+'.after.json'])
pair=call(['python3',G,'pair',str(prefix)+'.before.json',str(prefix)+'.after.json',str(prefix)+'.resources.json'])
r=json.loads(Path(str(prefix)+'.result.json').read_text());c=json.loads(Path(str(prefix)+'.cleanup.json').read_text());g=json.loads(Path(str(prefix)+'.resources.json').read_text())
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted']
receipt={'mode':mode,'accepted':accepted,'result':r,'cleanup':c,'resources':g,'APP_operations':False,'native_install':False,'automatic_retry':False}
Path(str(prefix)+'.CLOSED.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'mode':mode,'accepted':accepted,'seconds':r['seconds']}))
raise SystemExit(0 if accepted else 1)
