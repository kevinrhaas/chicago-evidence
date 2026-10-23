#!/usr/bin/env python3
"""Outside-only exclusive detached observer launcher. No API calls or retries here."""
import argparse,pathlib,subprocess,json,hashlib,os,time,sys,datetime
SHARED=pathlib.Path('/workspace/shared')
def need(c,m):
 if not c:raise ValueError(m)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,x):
 with p.open('x')as f:json.dump(x,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def identity(pid):
 raw=(pathlib.Path('/proc')/str(pid)/'stat').read_text();return {'pid':pid,'start_ticks':raw[raw.rfind(')')+2:].split()[19],'boot_id':pathlib.Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
def observers():
 found=[]
 for p in pathlib.Path('/proc').iterdir():
  if not p.name.isdigit()or int(p.name)==os.getpid():continue
  try:
   args=[v.decode()for v in (p/'cmdline').read_bytes().split(b'\0')if v]
   if any(pathlib.Path(v).name.startswith('watch_transport_metadata')and v.endswith('.py')for v in args):found.append(identity(int(p.name)))
  except (OSError,UnicodeError):pass
 return found

def main():
 a=argparse.ArgumentParser();a.add_argument('--source',required=True,type=pathlib.Path);a.add_argument('--source-sha256',required=True);a.add_argument('--dispatch',required=True,type=pathlib.Path);a.add_argument('--canonical',required=True,type=pathlib.Path);a.add_argument('--out',required=True,type=pathlib.Path);a.add_argument('--max-seconds',type=int,required=True);a.add_argument('--launch',action='store_true');a.add_argument('--child',action='store_true');x=a.parse_args();source=x.source.resolve();out=x.out.resolve();need(0<x.max_seconds<=10800,'At most180min positive bound required');need(source.is_relative_to(SHARED)and out.is_relative_to(SHARED),'Outside shared paths required');need(hashlib.sha256(source.read_bytes()).hexdigest()==x.source_sha256,'Reviewed source hash mismatch')
 lock=out.with_name(out.name+'.owner-lock');receipt=out.with_name(out.name+'.launch.json');go=lock/'go'
 if x.child:
  deadline=time.monotonic()+10
  while not go.exists()and time.monotonic()<deadline:time.sleep(.02)
  need(go.exists(),'Parent identity receipt missing; no polling')
  os.execv(sys.executable,[sys.executable,str(source),str(x.dispatch),'--canonical',str(x.canonical),'--out',str(out),'--pr','1041','--max-seconds',str(x.max_seconds)])
 plan={'execute':x.launch,'source':str(source),'source_sha256':x.source_sha256,'out':str(out),'wall_seconds':x.max_seconds,'poll_seconds':60,'no_api_retry':True,'no_new_workflow_dispatch':True}
 if not x.launch:print(json.dumps(plan,indent=2));return
 need(not out.exists()and not receipt.exists(),'Fresh output/receipt required');existing=observers();need(not existing,'Existing observer process; no duplicate')
 lock.mkdir(exist_ok=False);save(lock/'owner.json',{'at':now(),'launcher_identity':identity(os.getpid()),**plan})
 stdout=out.with_name(out.name+'.stdout.log');stderr=out.with_name(out.name+'.stderr.log')
 # Exclusive files and independent session avoid inherited exec-server pipes.
 with stdout.open('x')as so,stderr.open('x')as se:
  cmd=[sys.executable,str(pathlib.Path(__file__).resolve()),'--child','--max-seconds',str(x.max_seconds),'--source',str(source),'--source-sha256',x.source_sha256,'--dispatch',str(x.dispatch),'--canonical',str(x.canonical),'--out',str(out)]
  child=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=so,stderr=se,start_new_session=True,close_fds=True)
 try:
  record={**plan,'at':now(),'identity':identity(child.pid),'session_id':os.getsid(child.pid),'stdin':'DEVNULL','stdout':str(stdout),'stderr':str(stderr),'owner_lock':str(lock),'source_launcher_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'existing_observers_before_launch':existing};save(receipt,record);save(go,{'at':now(),'receipt':str(receipt)});print(json.dumps(record,indent=2))
 except BaseException:
  child.terminate();child.wait(timeout=5);raise
if __name__=='__main__':main()
