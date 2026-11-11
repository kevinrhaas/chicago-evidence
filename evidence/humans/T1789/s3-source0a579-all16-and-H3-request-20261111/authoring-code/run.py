"""Prepared only; ROOT admits this single metadata cell after actual S3 remote proof."""
from pathlib import Path
import argparse,fcntl,hashlib,json,re,subprocess
P=Path(__file__).resolve().parent
POST=Path('/tmp/ROOT-T1789-LINEN-S3-CHECKPOINT-POSTGATE-PREP-20261111')
parser=argparse.ArgumentParser();parser.add_argument('--binding-sha256',required=True);args=parser.parse_args()
assert re.fullmatch(r'[0-9a-f]{64}',args.binding_sha256)
assert hashlib.sha256((POST/'BINDING.json').read_bytes()).hexdigest()==args.binding_sha256
assert not any((P/n).exists() for n in ['before.json','after.json','command.log','command.result.json','CLOSED.json','AUTHORING-INTENT.json','AUTHORING.json','driver','request']),'No overwrite or automatic retry'
pins=json.loads((P/'SOURCE-PINS.json').read_text())
for name,pin in pins.items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==pin,name
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(a):return subprocess.run(a,check=False).returncode
if call(['python3',G,'capture',str(P/'before.json')]):raise SystemExit(1)
rc=call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(P/'command'),'--cwd','/workspace','--timeout','120','--','/tmp/ROOT-GATE-BIND-PREP-V2-20261110/with-cache.sh','--','python',str(P/'cell.py'),'--binding-sha256',args.binding_sha256])
post=call(['python3',G,'capture',str(P/'after.json')]);pair=call(['python3',G,'pair',str(P/'before.json'),str(P/'after.json'),str(P/'resources.json')])
r=json.loads((P/'command.result.json').read_text());c=json.loads((P/'command.cleanup.json').read_text());g=json.loads((P/'resources.json').read_text())
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and (P/'AUTHORING.json').is_file()
receipt={'accepted':accepted,'result':r,'cleanup':c,'resources':g,'cell_SHA256':pins['cell.py'],'postgate_binding_SHA256':args.binding_sha256,'AUTHORING_SHA256':hashlib.sha256((P/'AUTHORING.json').read_bytes()).hexdigest() if (P/'AUTHORING.json').exists() else None,'APP_operations':'frozen source verification only; no tracked writes','geometry_producer':False,'dispatch':False,'automatic_retry':False}
(P/'CLOSED.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'accepted':accepted,'seconds':r['seconds']}));raise SystemExit(0 if accepted else 1)
