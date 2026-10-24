#!/usr/bin/env python3
import argparse, ctypes, json, os, signal, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--cwd',required=True);p.add_argument('--timeout',type=float,default=5400);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command[1:] if a.command[:1]==['--'] else a.command
assert cmd
prefix=Path(a.prefix);prefix.parent.mkdir(parents=True,exist_ok=True)
for suffix in ['.log','.result.json','.cleanup.json']:
 assert not Path(str(prefix)+suffix).exists(), 'Use a new log name'
if ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)!=0:raise OSError(ctypes.get_errno(),'Unable to own descendant cleanup')
started=time.monotonic();child=None;rc=1;timed_out=False;reaped=[]
try:
 with open(str(prefix)+'.log','wb',buffering=0) as log:
  child=subprocess.Popen(cmd,cwd=a.cwd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  try:rc=child.wait(timeout=a.timeout)
  except subprocess.TimeoutExpired:timed_out=True;rc=124
except KeyboardInterrupt:rc=130
finally:
 if child:
  try:os.killpg(child.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  if child.poll() is None:
   try:child.wait(timeout=10)
   except subprocess.TimeoutExpired:
    os.killpg(child.pid,signal.SIGKILL);child.wait()
 # Drain every newly owned descendant; never cap the number of reaps.
 cleanup_started=time.monotonic();remaining=[]
 while True:
  try:
   pid,status=os.waitpid(-1,os.WNOHANG)
   if pid:
    reaped.append({'pid':pid,'status':status});continue
  except ChildProcessError:
   remaining=[];break
  remaining=[]
  for proc in Path('/proc').iterdir():
   if not proc.name.isdigit():continue
   try:
    stat=(proc/'stat').read_text().rsplit(')',1)[1].split()
    if int(stat[1])==os.getpid():remaining.append(int(proc.name))
   except (OSError,ValueError,IndexError):pass
  if not remaining:continue
  for pid in remaining:
   try:
    fd=os.pidfd_open(pid)
    try:
     stat=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
     if int(stat[1])==os.getpid() and stat[0]!='Z':
      sig=signal.SIGKILL if time.monotonic()-cleanup_started>2 else signal.SIGTERM
      signal.pidfd_send_signal(fd,sig,None,0)
    finally:os.close(fd)
   except (OSError,ValueError,IndexError):pass
  if time.monotonic()-cleanup_started>15:break
  time.sleep(.05)
 result={'returncode':rc,'seconds':time.monotonic()-started,'command':cmd,'cwd':a.cwd,'main_child_pid':child.pid if child else None,'timed_out':timed_out}
 Path(str(prefix)+'.result.json').write_text(json.dumps(result,indent=2)+'\n')
 Path(str(prefix)+'.cleanup.json').write_text(json.dumps({'reaped_owned_descendants':reaped,'remaining_owned_children':remaining,'cleanup_complete':not remaining},indent=2)+'\n')
 print(json.dumps(result))
raise SystemExit((rc if rc>=0 else 128-rc) if not remaining else 70)
