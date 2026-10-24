"""HELD one Node static b479 fit/contact replay. Stdlib supervisor only."""
from pathlib import Path
import ctypes,hashlib,json,os,resource,signal,subprocess,sys,time
P=Path(__file__).resolve().parent;PARENT=os.getpid()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def child_limits():
 libc=ctypes.CDLL(None,use_errno=True);libc.prctl.argtypes=[ctypes.c_int,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong];libc.prctl.restype=ctypes.c_int
 if libc.prctl(1,int(signal.SIGKILL),0,0,0)!=0:raise OSError(ctypes.get_errno(),'PDEATHSIG refused')
 if os.getppid()!=PARENT:os.kill(os.getpid(),signal.SIGKILL)
 resource.setrlimit(resource.RLIMIT_CPU,(20,20))
def alive(pid):
 try:os.killpg(pid,0);return True
 except ProcessLookupError:return False
def main():
 assert sys.version_info[:3]==(3,11,17)
 binding_path=Path(sys.argv[1]).resolve();b=json.loads(binding_path.read_text())
 template=json.loads((P/'BINDING-RELEASED-FALSE.json').read_text());expected=dict(template);expected['released']=True
 assert b==expected,'Only released:true may differ from frozen template'
 assert b['released'] is True and b['authorization']=='ONE_FRESH_1904_GLTFLOADER_CLONE_MIXER129_CPU_ONLY'
 assert b['maximum_runs']==1 and b['maximum_wall_seconds']==20 and b['maximum_rss_bytes']==256*1024*1024
 assert b['Node_or_browser_execution_held_until_root_release'] is True
 for name,h in b['source_sha256'].items():assert sha(P/name)==h,name
 for name,pin in b['inputs'].items():assert sha(name)==pin['sha256'],name
 out=P/'ACTUAL';assert not out.exists();out.mkdir()
 (out/'ROOT-RELEASE.json').write_text(json.dumps(b,indent=2)+'\n')
 env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',UV_THREADPOOL_SIZE='1',NODE_OPTIONS='')
 start=time.monotonic();peak=0;reason=None;child=None;code=None;error=None
 previous=signal.signal(signal.SIGTERM,lambda signum,frame:(_ for _ in()).throw(RuntimeError('Supervisor interrupted')))
 try:
  with (out/'stdout.log').open('w')as stdout,(out/'stderr.log').open('w')as stderr:
   child=subprocess.Popen(['nice','-n','19',b['node_path'],'--v8-pool-size=1','--max-old-space-size=256','--max-semi-space-size=8',str(P/'proof.mjs'),str(binding_path)],cwd=P,env=env,stdout=stdout,stderr=stderr,start_new_session=True,preexec_fn=child_limits)
   while child.poll()is None:
    try:
     for line in(Path('/proc')/str(child.pid)/'status').read_text().splitlines():
      if line.startswith('VmRSS:'):peak=max(peak,int(line.split()[1])*1024)
    except FileNotFoundError:pass
    if time.monotonic()-start>20:reason='WALL_LIMIT_20_SECONDS'
    elif peak>256*1024*1024:reason='RSS_LIMIT_256_MiB'
    if reason:break
    time.sleep(.025)
 except BaseException as e:error={'type':type(e).__name__,'message':str(e)};reason=reason or'SUPERVISOR_EXCEPTION'
 finally:
  if child is not None:
   if child.poll()is None:
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   code=child.wait()
  signal.signal(signal.SIGTERM,previous)
 elapsed=time.monotonic()-start;peak=max(peak,int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)*1024)
 if peak>256*1024*1024 or elapsed>20:reason=reason or'RESOURCE_LIMIT_EXCEEDED'
 closed=child is None or not alive(child.pid)
 if not closed:
  try:os.killpg(child.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  time.sleep(.025);closed=not alive(child.pid);reason=reason or'UNEXPECTED_OWNED_CHILD_GROUP'
 result_path=out/'READBACK.json';result=None;parse_error=None
 try:
  if result_path.exists():result=json.loads(result_path.read_text())
 except (ValueError,OSError) as e:parse_error=str(e);reason=reason or'MALFORMED_OR_UNREADABLE_READBACK'
 try:
  for name,h in b['source_sha256'].items():
   if sha(P/name)!=h:reason=reason or'FINAL_SOURCE_DRIFT'
  for name,pin in b['inputs'].items():
   if sha(name)!=pin['sha256']:reason=reason or'FINAL_INPUT_DRIFT'
 except OSError as e:reason=reason or'FINAL_PIN_READ_REFUSAL';error=error or{'type':type(e).__name__,'message':str(e)}
 ok=not reason and closed and code==0 and result is not None and result['status']=='FRESH_GLTFLOADER_PRODUCTION_CLONE_MIXER129_HOSTED_CPU_PASS_ONLY'
 terminal={'status':'FRESH_1904_LOADER_CLONE_MIXER129_CPU_PASS_ONLY'if ok else'FRESH_1904_LOADER_CLONE_MIXER129_CPU_FAIL_OR_REFUSAL','exit_code':code,'elapsed_seconds':elapsed,'peak_rss_bytes':peak,'resource_or_supervisor_failure':reason,'parent_error':error,'readback_parse_error':parse_error,'child_reaped':child is not None and code is not None,'no_owned_child_active':closed,'world_qualified':False,'app_or_GPU_or_photo_accepted':False,'activation_or_next_phase':False,'new_browser':False,'new_GLTFLoader_import':True,'reruns':0}
 (out/'TERMINAL.json').write_text(json.dumps(terminal,indent=2)+'\n');print(json.dumps(terminal));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
