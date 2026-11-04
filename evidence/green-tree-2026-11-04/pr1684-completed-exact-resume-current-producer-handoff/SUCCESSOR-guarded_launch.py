from pathlib import Path
import json,os,subprocess,datetime
p=Path(__file__).resolve().parent;old=Path('/tmp/native-gt-saug-observer-after-reset-20261104')
r=json.loads((old/'REAPER.json').read_text());assert r['command_exit']==0 and r['all_children_reaped'] and not r['leftover_cleanup'], 'Old watcher has not properly closed; do not start duplicate'
assert (old/'CLOSED.json').exists()
for pid in [r['wrapper_pid'],r['command_pid']]:assert not Path('/proc/'+str(pid)).exists(),'Old watcher PID still exists; inspect before renewal'
assert not (p/'STARTED.json').exists(),'Renewal already launched; inspect PID and receipt'
tasks=json.loads((old/'TASKS.json').read_text())
if (p/'ADDITIONAL-TASKS.json').exists():
 for task in json.loads((p/'ADDITIONAL-TASKS.json').read_text()):
  peer=Path(task['prior_monitor_dir']);rpeer=json.loads((peer/'CLAIM-MONITOR-REAPER.json').read_text());assert rpeer['command_exit']==0 and rpeer['all_children_reaped'] and not rpeer['leftover_cleanup'];assert (peer/'MONITOR-CLOSED.json').exists()
  for pid in [rpeer['wrapper_pid'],rpeer['command_pid']]:assert not Path('/proc/'+str(pid)).exists(),'Peer monitor still exists'
  assert not any(x['run']==task['run'] for x in tasks)
  tasks.append({k:v for k,v in task.items() if k!='prior_monitor_dir'})
(p/'TASKS.json').write_text(json.dumps(tasks,indent=2)+'\n')
for target in (old/'completed-runs').glob('*'):
 d=p/'completed-runs';d.mkdir(exist_ok=True);link=d/target.name
 if not link.exists():link.symlink_to(target,target_is_directory=True)
with (p/'STARTED.json').open('x')as out:out.write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_closed_proper0':True,'old_reaper':r,'no_duplicate_observer':True,'read_only':True},indent=2)+'\n')
subprocess.run(['python',str(p/'observe.py')],check=True)
