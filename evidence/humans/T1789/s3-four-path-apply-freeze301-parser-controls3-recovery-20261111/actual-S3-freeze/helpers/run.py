from pathlib import Path
import fcntl,hashlib,json,subprocess,sys,re,os
P=Path(__file__).resolve().parent;part=int(sys.argv[1]);assert part in range(1,17)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in json.loads((P/'SOURCE-PINS.json').read_bytes()).items():assert sha(P/n)==h,n
raw=(P/'FREEZE.json').read_bytes();pin=hashlib.sha256(raw).hexdigest();d=json.loads(raw);assert json.loads((P/'READY.json').read_bytes())['freeze_SHA256']==pin and d['parts']==16 and d['CHECK_JOBS']==4
closed=json.loads((P/'FREEZE-CLOSED.json').read_bytes());assert closed['accepted'] and closed['freeze_SHA256']==pin
for prior in range(1,part):
 c=json.loads((P/f'part{prior}.CLOSED.json').read_bytes());assert c['accepted'] and c['freeze_SHA256']==pin and c['CHECK_JOBS']==4 and c['partition_count']==16 and c['part']==prior
 assert sha(P/f'part{prior}.log')==c['log_SHA256'],'previous actual evidence changed'
wrapper=Path(d['wrapper']);assert sha(wrapper)==d['wrapper_SHA256'];prefix=P/f'part{part}'
assert not any(Path(str(prefix)+'.'+s).exists() for s in ['before.json','log','result.json','CLOSED.json']),'one attempt, sequential parts, no retry'
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(a):return subprocess.run(a,check=False).returncode
assert call(['python3',G,'capture',str(prefix)+'.before.json'])==0
env=dict(os.environ,CHECK_JOBS='4',PYTHONDONTWRITEBYTECODE='1')
rc=subprocess.run(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd','/workspace','--timeout','600','--',str(wrapper),'--','bash',str(P/f'part{part}.sh')],env=env,check=False).returncode
post=call(['python3',G,'capture',str(prefix)+'.after.json']);pair=call(['python3',G,'pair',str(prefix)+'.before.json',str(prefix)+'.after.json',str(prefix)+'.resources.json'])
r=json.loads(Path(str(prefix)+'.result.json').read_bytes());c=json.loads(Path(str(prefix)+'.cleanup.json').read_bytes());g=json.loads(Path(str(prefix)+'.resources.json').read_bytes());log=Path(str(prefix)+'.log').read_bytes();display=re.sub(r'\x1b\[[0-9;]*m','',log.decode(errors='replace'));markers=[s for s in display.splitlines() if s.startswith('CHECK PASS') or s.startswith('CHECK FAIL')]
marker='S3_SOURCE_VERIFIED '+pin
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==600 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and len(markers)==1 and re.fullmatch(r'CHECK PASS — part '+str(part)+r'/16: (\d+) steps, none red\.',markers[0]) is not None and display.count(marker)==2 and sha(P/'FREEZE.json')==pin
record=dict(accepted=accepted,part=part,result=r,cleanup=c,resources=g,actual_final_markers=markers,freeze_SHA256=pin,log_SHA256=hashlib.sha256(log).hexdigest(),qualification='SOURCE_GATE_ONLY_NATIVE_BAKE_FIXTURE_POSE_PHOTO_PENDING',commit=False,push=False,CHECK_JOBS=4,partition_count=16,sequential_parts=True)
Path(str(prefix)+'.CLOSED.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(part=part,accepted=accepted,seconds=r['seconds'],markers=markers)));raise SystemExit(0 if accepted else 1)
