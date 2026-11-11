from pathlib import Path
import fcntl,hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
pins=json.loads((P/'SOURCE-PINS.json').read_bytes())
for n,h in pins.items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
assert not any((P/n).exists() for n in ['before.json','apply.log','apply.result.json','APPLY-RECEIPT.json','CLOSED.json']),'one attempt only; preserve failure'
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(a):return subprocess.run(a,check=False).returncode
assert call(['python3',G,'capture',str(P/'before.json')])==0
rc=call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(P/'apply'),'--cwd','/workspace','--timeout','120','--','/tmp/ROOT-GATE-BIND-PREP-V2-20261110/with-cache.sh','--','python3',str(P/'cell.py'),*sys.argv[1:]])
post=call(['python3',G,'capture',str(P/'after.json')]);pair=call(['python3',G,'pair',str(P/'before.json'),str(P/'after.json'),str(P/'resources.json')])
r=json.loads((P/'apply.result.json').read_bytes());c=json.loads((P/'apply.cleanup.json').read_bytes());g=json.loads((P/'resources.json').read_bytes());q=P/'APPLY-RECEIPT.json'
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and q.is_file()
d=dict(accepted=accepted,result=r,cleanup=c,resources=g,receipt_SHA256=hashlib.sha256(q.read_bytes()).hexdigest() if q.exists() else None,cell_SHA256=pins['cell.py'],automatic_retry=False)
(P/'CLOSED.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d));raise SystemExit(0 if accepted else 1)
