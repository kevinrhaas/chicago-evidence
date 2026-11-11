from pathlib import Path
import fcntl,hashlib,json,subprocess
P=Path(__file__).resolve().parent
for n,h in json.loads((P/'SOURCE-PINS.json').read_bytes()).items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
assert not any((P/n).exists() for n in ['copy.before.json','copy.log','copy.result.json','CLOSED.json']), 'one attempt only; never retry or overwrite'
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def run(a):return subprocess.run(a,check=False).returncode
assert run(['python3',G,'capture',str(P/'copy.before.json')])==0
rc=run(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(P/'copy'),'--cwd','/workspace','--timeout','120','--','/tmp/ROOT-GATE-BIND-PREP-V2-20261110/with-cache.sh','--','python3',str(P/'prepare.py')])
post=run(['python3',G,'capture',str(P/'copy.after.json')]);pair=run(['python3',G,'pair',str(P/'copy.before.json'),str(P/'copy.after.json'),str(P/'resources.json')])
r=json.loads((P/'copy.result.json').read_bytes());c=json.loads((P/'copy.cleanup.json').read_bytes());g=json.loads((P/'resources.json').read_bytes());m=Path('/tmp/T1789-SETTLER-S2-AFTER-OBSERVATION-PREP-20261111/MANIFEST.json')
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and m.is_file()
record=dict(accepted=accepted,result=r,cleanup=c,resources=g,manifest_sha256=hashlib.sha256(m.read_bytes()).hexdigest() if m.exists() else None,native_fit_accepted=False,browser_run=False,automatic_retry=False)
(P/'CLOSED.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));raise SystemExit(0 if accepted else 1)
