"""Root-released one V18 native unit; 45s, one child, four declared exports, no preview/app writes."""
from pathlib import Path
import argparse,ctypes,datetime,hashlib,json,os,resource,shutil,signal,subprocess,sys,time,traceback
HERE=Path(__file__).resolve().parent
AUTH='ONE_ROOT_AUTHORIZED_V18_LAMP_NATIVE_DIAGNOSTIC'
PYTHON='/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin/python'
NODE='/opt/codex/runtimes/codex-primary-runtime/dependencies/node/bin/node'
VALIDATOR='/workspace/shared/brougham-v12-largeforms-PROPOSAL-20261022/validate_raw.cjs'
PARENT=os.getpid();WALL=45.;WORK=42.;RSS=768*1024*1024
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise AssertionError(why)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def alive(pid):
 try:os.killpg(pid,0);return True
 except ProcessLookupError:return False
def child_limits(is_python):
 libc=ctypes.CDLL(None,use_errno=True);libc.prctl.argtypes=[ctypes.c_int,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong];libc.prctl.restype=ctypes.c_int
 if libc.prctl(1,int(signal.SIGKILL),0,0,0)!=0:raise OSError(ctypes.get_errno(),'Parent-death guard refused')
 if os.getppid()!=PARENT:os.kill(os.getpid(),signal.SIGKILL)
 resource.setrlimit(resource.RLIMIT_CPU,(42,42))
 # Node's V8 reserves large virtual ranges; its RSS is monitored separately.
 if is_python:resource.setrlimit(resource.RLIMIT_AS,(1536*1024*1024,1536*1024*1024))
def main(release_path):
 start=time.monotonic();require(sys.version_info[:3]==(3,11,17),'Approved Python3.11.17 required')
 require(Path(sys.executable).resolve()==Path(PYTHON).resolve(),'Approved executable required')
 release=json.loads(release_path.read_text());manifest_path=HERE/'MANIFEST.json';manifest=json.loads(manifest_path.read_text())
 require(release.get('released')is True and release.get('authorization')==AUTH,'Explicit root release required')
 for field in ['independent_source_review_complete','current_root_native_only_release','native_generation_authorized','native_readback_authorized','Khronos_authorized']:require(release.get(field)is True,'Required root release condition: '+field)
 require(release.get('browser_or_canonical_intake_authorized')is False,'No preview/app authorization in this unit')
 require(release.get('source_manifest_sha256')==sha(manifest_path),'Exact reviewed source manifest required')
 require(release.get('maximum_wall_seconds')==45 and release.get('maximum_generator_invocations')==4 and release.get('maximum_index_transforms')==2 and release.get('maximum_Khronos_invocations')==4,'Fixed finite counts required')
 for name,row in manifest.items():require(sha(HERE/name)==row['sha256']and(HERE/name).stat().st_size==row['bytes'],'Source drift: '+name)
 pins=json.loads((HERE/'INPUT-PINS.json').read_text())
 for row in list(pins['baseline_files'].values())+pins['runtime_files']:require(sha(row['path'])==row['sha256']and Path(row['path']).stat().st_size==row['bytes'],'Input/runtime drift: '+row['path'])
 out=HERE/'ACTUAL';require(not out.exists(),'One-shot output already exists; no retry')
 require(shutil.disk_usage(HERE).free>=32*1024*1024,'Insufficient space for bounded private outputs')
 out.mkdir();(out/'baseline').mkdir();(out/'logs').mkdir()
 intent={'authorization':AUTH,'started_utc':utc(),'source_manifest_sha256':sha(manifest_path),'root_release':release,'maximum_wall_seconds':45,'work_deadline_seconds':42,'maximum_generator_invocations':4,'maximum_index_transforms':2,'maximum_Khronos_invocations':4,'maximum_concurrent_children':1,'RSS_monitor_bytes':RSS,'Python_child_address_limit_bytes':1536*1024*1024,'child_CPU_limit_seconds':42,'nice':19,'numerical_threads':1,'native_readback_authorized':True,'browser_or_world_or_photo_accepted':False}
 (out/'INTENT.json').write_text(json.dumps(intent,indent=2)+'\n')
 active=None;all_pids=[];peak=0;closure=True
 receipt={'pass':False,'scope':'ONE V18 native candidate unit; matched8/world/photo remain held','started_utc':intent['started_utc'],'stages':[],'runs':1,'automatic_retries':0,'generation_invocations':0,'index_transforms':0,'Khronos_invocations':0,'browser_invocations':0,'canonical_writes':0,'source_manifest_sha256':intent['source_manifest_sha256']}
 def save():(out/'TERMINAL.json').write_text(json.dumps(receipt,indent=2)+'\n')
 def close_active():
  nonlocal active,closure
  if active is None:return
  child=active
  try:
   # A reaped direct child can still have an owned process-group survivor.
   # Keep the child reference through this group-level kill/reap/readback.
   if child.poll()is None or alive(child.pid):
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   child.wait(timeout=1)
   if alive(child.pid):
    closure=False;receipt.setdefault('cleanup_errors',[]).append('Owned process group remains after SIGKILL/reap: '+str(child.pid))
  except BaseException as error:closure=False;receipt.setdefault('cleanup_errors',[]).append(repr(error))
  finally:active=None
 def interrupted(signum,frame):raise RuntimeError('Owner interrupted by signal '+str(signum))
 oldsignals={s:signal.signal(s,interrupted)for s in [signal.SIGTERM,signal.SIGINT]}
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',UV_THREADPOOL_SIZE='1',GOMAXPROCS='1',PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1')
 def run(label,args):
  nonlocal active,peak
  require(time.monotonic()-start<WORK,'Work deadline exhausted')
  stage={'label':label,'argv':args,'started_utc':utc()};receipt['stages'].append(stage);save()
  with(out/'logs'/(label+'.stdout')).open('w')as stdout,(out/'logs'/(label+'.stderr')).open('w')as stderr:
   active=subprocess.Popen(['nice','-n','19',*args],cwd=out,env=env,stdout=stdout,stderr=stderr,start_new_session=True,preexec_fn=lambda:child_limits(args[0]==PYTHON));all_pids.append(active.pid);stage['pid']=active.pid;save()
   while active.poll()is None:
    try:
     for line in (Path('/proc')/str(active.pid)/'status').read_text().splitlines():
      if line.startswith('VmRSS:'):peak=max(peak,int(line.split()[1])*1024)
    except FileNotFoundError:pass
    require(time.monotonic()-start<WORK,'Work deadline exceeded during '+label)
    require(peak<=RSS,'Child RSS monitoring limit exceeded during '+label)
    time.sleep(.025)
   code=active.wait();pid=active.pid;stage.update(returncode=code,elapsed_owner_seconds=time.monotonic()-start,child_reaped=True)
   require(not alive(pid),'Unexpected owned process-group survivor after '+label)
   active=None # Transfer ownership only after group-exit confirmation.
  save();require(code==0,'Actual stage failed: '+label+'; preserve failure/no retry')
 try:
  for name,row in pins['baseline_files'].items():
   data=Path(row['path']).read_bytes();require(hashlib.sha256(data).hexdigest()==row['sha256'],'Baseline drift while staging');(out/'baseline'/name).write_bytes(data)
  for name,detail,recipe in [('near-A','near','lods.json'),('near-B-repeat','near','lods.json'),('mid-A','mid','ring16-mid-lods.json'),('mid-B-repeat','mid','ring16-mid-lods.json')]:
   receipt['generation_invocations']+=1
   run('generate-'+name,[PYTHON,str(HERE/'source/generate.py'),'--parameters',str(HERE/'source/parameters.json'),'--detail',detail,'--lod-recipe',str(HERE/'source'/recipe),'--rear-quarter-recipe',str(HERE/'source/rear-quarter.json'),'--output',str(out/name)])
  run('native-readback',[PYTHON,str(HERE/'check_lamp_delta_HELD.py'),'--actual',str(out)])
  native=json.loads((out/'NATIVE-RESULT.json').read_text());require(native['pass']is True,'Native actual result did not pass');receipt['index_transforms']=2
  for row in native['rows']:
   detail=row['detail'];pairs=[('raw','brougham-source.glb'if detail=='near'else'brougham-mid-source.glb','source_sha256'),('indexed','brougham-near.glb'if detail=='near'else'brougham-mid.glb','indexed_sha256')]
   for variant,filename,hashkey in pairs:
    file=out/'delivery'/filename;before=sha(file);require(before==row[hashkey],'Actual validator input drift');label='khronos-'+detail+'-'+variant;report=out/(label+'.json');receipt['Khronos_invocations']+=1
    run(label,[NODE,'--v8-pool-size=1','--max-old-space-size=256',VALIDATOR,str(file),str(report)])
    require(sha(file)==before,'Validator input changed');report_json=json.loads(report.read_text());issues=report_json['issues'];info=report_json['info']
    require(report_json['validatorVersion']=='2.0.0-dev.3.10','Existing validator version drift')
    require(issues['numErrors']==issues['numWarnings']==0 and issues['numInfos']==4 and not issues['truncated'],'Fresh Khronos issues')
    require(sorted((v['code'],v['pointer'])for v in issues['messages'])==[('NODE_EMPTY','/nodes/'+str(i))for i in [13,14,15,16]],'Unexpected validator info inventory')
    require(info['totalTriangleCount']==row['triangles']and info['drawCallCount']==25 and info['hasSkins']is False and info['hasTextures']is False,'Fresh validator actual model inventory')
    receipt.setdefault('fresh_validator_bindings',[]).append({'input_file':filename,'input_sha256':before,'report':report.name,'report_sha256':sha(report),'actual_triangles':info['totalTriangleCount']})
  require(receipt['generation_invocations']==4 and receipt['index_transforms']==2 and receipt['Khronos_invocations']==4,'Exact stage counts')
  for row in list(pins['baseline_files'].values())+pins['runtime_files']:require(sha(row['path'])==row['sha256'],'Original baseline/runtime changed during owner')
  for name,row in manifest.items():require(sha(HERE/name)==row['sha256'],'Frozen source changed during owner')
  receipt['pass']=True
 except BaseException as error:receipt['failure']={'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc()}
 finally:
  close_active();peak=max(peak,int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)*1024)
  for sig,handler in oldsignals.items():signal.signal(sig,handler)
  elapsed=time.monotonic()-start
  if elapsed>WALL or peak>RSS or not closure:receipt['pass']=False;receipt['resource_or_closure_failure']=True
  receipt.update(finished_utc=utc(),elapsed_seconds=elapsed,actual_peak_child_RSS_bytes=peak,owned_child_pids=all_pids,no_owned_child_active=closure and all(not alive(pid)for pid in all_pids),lifecycle='CLOSED'if closure else'CLOSURE_FAILURE',source8_or_world_or_photo_accepted=False,next_phase_authorized=False)
  if not receipt['no_owned_child_active']:receipt['pass']=False
  save()
 print(json.dumps(receipt));return 0 if receipt['pass']else 2
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--release',type=Path,required=True);args=parser.parse_args();raise SystemExit(main(args.release.resolve()))
