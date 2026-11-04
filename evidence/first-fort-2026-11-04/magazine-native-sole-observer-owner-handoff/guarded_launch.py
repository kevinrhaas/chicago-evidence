from pathlib import Path
import json,os,subprocess,datetime,hashlib
p=Path(__file__).resolve().parent;old=Path('/tmp/native-picture-pr-observer-renewal-20261104-0400');peer=Path('/tmp/first-fort-magazine-prep-20261104')
old_expected={'CLOSED.json':'1141c09cf1f5910e03ff477d5c625da4a42386855a4359ae6b318264613d3573','REAPER.json':'51279d906916734749c2e0654fe920842022e5e440ad8f0a57b1401d75713c9e'}
for n,h in old_expected.items():assert hashlib.sha256((old/n).read_bytes()).hexdigest()==h,'Prior receipt changed; inspect before launch'
r=json.loads((old/'REAPER.json').read_text());assert r['command_exit']==0 and r['all_children_reaped'] and not r['leftover_cleanup']
for pid in [r['wrapper_pid'],r['command_pid'],945235]:assert not Path('/proc/'+str(pid)).exists(),'Prior observer PID still alive'
assert (peer/'MONITOR-CLOSED.json').exists(),'Initial monitor has not closed; no duplicate'
rpeer=json.loads((peer/'INITIAL-MONITOR-REAPER.json').read_text());assert rpeer['command_exit']==0 and rpeer['all_children_reaped']and not rpeer['leftover_cleanup'],'Initial monitor not properly reaped'
for pid in [rpeer['wrapper_pid'],rpeer['command_pid']]:assert not Path('/proc/'+str(pid)).exists(),'Peer initial monitor PID alive'
latest=json.loads((peer/'MONITOR-CLOSED.json').read_text())['latest'];assert latest['run']==41782312201 and latest['feature']=='7b427d130a2cca6ed82c183c74605b965aee1d4e';assert not latest.get('ownership_mismatch');assert 'ubuntu-26.04'in latest['target_job']['labels']
assert hashlib.sha256((p/'observe.py').read_bytes()).hexdigest()=='a575b57bdc517a4a0d2b4e4c49365b7f4a2ec5f87404a3c5f17827e18270b338'
assert not(p/'STARTED.json').exists(),'Successor already launched; inspect existing process'
tasks=[{'ticket':'T-3041','parent_ticket':'T-2387','run':41782312201,'pr':None,'ticket_file':'T-3000-3249/T-3041-match-the-first-fort-dearborn-buildings-against-.md','expected_feature':'7b427d130a2cca6ed82c183c74605b965aee1d4e','lane':'first-fort-magazine-native-20261104','prior_monitor_dir':str(peer),'native_scope':'fort_structure25; preserve243outbuilding/currentcupola','prior_completed_proofs':{'cupola':'6bfea816f195698095308a069967f6861b726652','green_tree':'37facc34d6030a69832e5f8e94b5712eb323c223','cobweb':'ab6c32b1323b0dd4b2e06026e3f4b606dec8f918','sauganash':'e553c1f836bbb79ca3edd2b18c9a04fcb2eaed21'}}]
(p/'TASKS.json').write_text(json.dumps(tasks,indent=2)+'\n')
with(p/'STARTED.json').open('x')as out:out.write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_closed_guards':old_expected,'prior_reaper':r,'peer_reaper':rpeer,'peer_closed_sha256':hashlib.sha256((peer/'MONITOR-CLOSED.json').read_bytes()).hexdigest(),'peer_reaper_sha256':hashlib.sha256((peer/'INITIAL-MONITOR-REAPER.json').read_bytes()).hexdigest(),'actual_initial_latest':latest,'no_duplicate_observer':True,'all_prior_completed_rows_retired':True,'read_only':True},indent=2)+'\n')
subprocess.run(['python',str(p/'observe.py')],check=True)
