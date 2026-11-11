from pathlib import Path
import argparse,fcntl,hashlib,json,os,re,subprocess
P=Path(__file__).resolve().parent
PREP=P.parent
PHASE=P.name
parser=argparse.ArgumentParser()
parser.add_argument('--binding-sha256',required=True)
args=parser.parse_args()
assert re.fullmatch('[0-9a-f]{64}',args.binding_sha256)
assert hashlib.sha256((PREP/'BINDING.json').read_bytes()).hexdigest()==args.binding_sha256
os.environ['T1789_S4_POSTGATE_BINDING_SHA256']=args.binding_sha256
assert PHASE in ['COMMIT','PREFLIGHT','PUSH','REMOTE-VERIFY']
pins=json.loads((PREP/'SOURCE-PINS.json').read_text())
for name,pin in pins.items():
    assert hashlib.sha256((PREP/name).read_bytes()).hexdigest()==pin,name
assert not any((P/n).exists() for n in ['before.json','command.log','command.result.json','CLOSED.json']), 'Refuse overwrite or automatic retry'
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(args):return subprocess.run(args,check=False).returncode
if call(['python3',G,'capture',str(P/'before.json')]):raise SystemExit(1)
rc=call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(P/'command'),'--cwd','/workspace','--timeout','120','--','/tmp/ROOT-GATE-BIND-PREP-V2-20261110/with-cache.sh','--','bash',str(P/'cell.sh')])
post=call(['python3',G,'capture',str(P/'after.json')])
pair=call(['python3',G,'pair',str(P/'before.json'),str(P/'after.json'),str(P/'resources.json')])
r=json.loads((P/'command.result.json').read_text());c=json.loads((P/'command.cleanup.json').read_text());g=json.loads((P/'resources.json').read_text())
name={'COMMIT':'COMMIT','PREFLIGHT':'PREFLIGHT','PUSH':'PUSH','REMOTE-VERIFY':'REMOTE'}[PHASE]+'-RECEIPT.json'
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and (P/name).is_file()
record={'phase':PHASE,'accepted':accepted,'result':r,'cleanup':c,'resources':g,'chain_SHA256':pins['chain.py'],'binding_SHA256':args.binding_sha256,'receipt':str(P/name),'receipt_SHA256':hashlib.sha256((P/name).read_bytes()).hexdigest() if (P/name).exists() else None,'automatic_retry':False}
(P/'CLOSED.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'phase':PHASE,'accepted':accepted,'seconds':r['seconds'],'receipt':str(P/name)}))
raise SystemExit(0 if accepted else 1)
