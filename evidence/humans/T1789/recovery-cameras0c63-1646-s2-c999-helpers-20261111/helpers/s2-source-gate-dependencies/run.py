from pathlib import Path
import fcntl,hashlib,json,subprocess,sys,re,os
P=Path(__file__).resolve().parent
part=int(sys.argv[1]);assert part in range(1,17)
raw=(P/'FREEZE.json').read_bytes();pin=hashlib.sha256(raw).hexdigest();d=json.loads(raw)
assert json.loads((P/'READY.json').read_text())['freeze_SHA256']==pin
freeze_closed=json.loads((P/'FREEZE-CLOSED.json').read_text());assert freeze_closed['accepted'] and freeze_closed['freeze_SHA256']==pin
wrapper=Path(d['wrapper']);assert hashlib.sha256(wrapper.read_bytes()).hexdigest()==d['wrapper_SHA256']
prefix=P/f'part{part}'
assert not any(Path(str(prefix)+'.'+s).exists() for s in ['before.json','log','result.json','CLOSED.json']), 'Refuse overwrite/retry'
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(a):return subprocess.run(a,check=False).returncode
if call(['python3',G,'capture',str(prefix)+'.before.json']):raise SystemExit(1)
rc=call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd','/workspace','--timeout','600','--',str(wrapper),'--','bash',str(P/f'part{part}.sh')])
post=call(['python3',G,'capture',str(prefix)+'.after.json'])
pair=call(['python3',G,'pair',str(prefix)+'.before.json',str(prefix)+'.after.json',str(prefix)+'.resources.json'])
r=json.loads(Path(str(prefix)+'.result.json').read_text());c=json.loads(Path(str(prefix)+'.cleanup.json').read_text());g=json.loads(Path(str(prefix)+'.resources.json').read_text())
log=Path(str(prefix)+'.log').read_bytes();display=re.sub(r'\x1b\[[0-9;]*m','',log.decode(errors='replace'))
markers=[s for s in display.splitlines() if s.startswith('CHECK PASS') or s.startswith('CHECK FAIL')]
source_marker='S2_SOURCE_VERIFIED '+pin+' native8_fixture_primary_ref_unchanged parts16'
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==600 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and len(markers)==1 and markers[0].startswith('CHECK PASS') and f'part {part}/16' in markers[0] and display.count(source_marker)==2 and hashlib.sha256((P/'FREEZE.json').read_bytes()).hexdigest()==pin
receipt={'accepted':accepted,'part':part,'result':r,'cleanup':c,'resources':g,'actual_final_markers':markers,'freeze_SHA256':pin,'log_SHA256':hashlib.sha256(log).hexdigest(),'qualification':'SOURCE_GATE_ONLY_NATIVE_BAKE_FIXTURE_POSE_PHOTO_PENDING','commit':False,'push':False,'CHECK_JOBS':os.environ.get('CHECK_JOBS','repository_default_nproc_capped8'),'partition_count':16}
Path(str(prefix)+'.CLOSED.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'part':part,'accepted':accepted,'seconds':r['seconds'],'markers':markers}))
raise SystemExit(0 if accepted else 1)
