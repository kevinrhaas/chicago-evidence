from pathlib import Path
import fcntl,hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
for n,h in json.loads((P/'SOURCE-PINS.json').read_bytes()).items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
base=Path('/tmp/t1789-settler-s3-source-full-gate-prep-20261111/FREEZE.json');assert hashlib.sha256(base.read_bytes()).hexdigest()=='6944115f9392d917e16bcc4fe0c1adf490bc58ec64373b09d25467118084fa41';d=json.loads(base.read_bytes());wrapper=Path(d['wrapper']);assert hashlib.sha256(wrapper.read_bytes()).hexdigest()==d['wrapper_SHA256']
assert not any((P/n).exists() for n in ['FREEZE.json','READY.json','freeze.before.json','freeze.log','freeze.result.json','FREEZE-CLOSED.json']),'one attempt only'
lock=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
G='/workspace/.cloud-setup/transport-current-20261103/resource_guard.py'
def call(a):return subprocess.run(a,check=False).returncode
assert call(['python3',G,'capture',str(P/'freeze.before.json')])==0
before=json.loads((P/'freeze.before.json').read_bytes());assert before['workspace_free_bytes']>=512*1024**2+8*1024**2,'workspace margin below8MiB; pause, no cleanup'
assert hashlib.sha256(Path(G).with_name('RESTORED-RUNTIME-BASELINE.json').read_bytes()).hexdigest()=='3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
rc=call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(P/'freeze'),'--cwd','/workspace','--timeout','120','--',str(wrapper),'--','python3',str(P/'capture_freeze.py'),*sys.argv[1:]])
post=call(['python3',G,'capture',str(P/'freeze.after.json')]);pair=call(['python3',G,'pair',str(P/'freeze.before.json'),str(P/'freeze.after.json'),str(P/'freeze.resources.json')])
r=json.loads((P/'freeze.result.json').read_bytes());c=json.loads((P/'freeze.cleanup.json').read_bytes());g=json.loads((P/'freeze.resources.json').read_bytes())
accepted=rc==post==pair==0 and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and c['cleanup_complete'] and not c['remaining_owned_children'] and g['accepted'] and (P/'READY.json').is_file()
record=dict(accepted=accepted,result=r,cleanup=c,resources=g,freeze_SHA256=hashlib.sha256((P/'FREEZE.json').read_bytes()).hexdigest() if (P/'FREEZE.json').exists() else None,source_gate='PENDING_ALL16',native_bake_fixture_pose_photo='PENDING',automatic_retry=False)
(P/'FREEZE-CLOSED.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));raise SystemExit(0 if accepted else 1)
