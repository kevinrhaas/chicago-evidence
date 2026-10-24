from pathlib import Path
import subprocess,time,resource,json,hashlib,sys,shutil
d=Path(__file__).parent/'V32-NATIVE-REPEAT-ONLY-PROOF';start=time.monotonic();reports=[]
commands=[[shutil.which('node'),str(d/'read_native_mixer.mjs')],[sys.executable,str(d/'check_actual_readback.py')]]
try:
 for command in commands:
  p=subprocess.run(command,cwd=d,timeout=max(1,115-(time.monotonic()-start)),check=False);reports.append({'command':command,'returncode':p.returncode});assert p.returncode==0,'Actual native repeat unit FAIL; preserve failure.'
finally:
 out={'status':'ACTUAL_NATIVE_LOOPREPEAT_UNIT_PASS'if len(reports)==2 and all(q['returncode']==0 for q in reports)else'ACTUAL_NATIVE_LOOPREPEAT_UNIT_FAIL','scope':'NativeLoopRepeat only; no clamp/stop/endtoendproducer/visual/traffic qualification','original_V30_encoder_RSS_FAIL_and_V31_LoopOnce_FAIL_retained':True,'commands':reports,'maximum_child_RSS_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024,'elapsed_seconds':time.monotonic()-start,'source_sha256':{str(p.relative_to(d.parent)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[d.parent/'prepare_v32.py',d.parent/'run_repeat_v32.py',d/'read_native_mixer.mjs',d/'check_actual_readback.py']},'normalization_wrapper':False,'app_or_browser_writes':False,'natural_gait_accepted':False};(d/'ACTUAL-UNIT-RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
assert out['maximum_child_RSS_bytes']<=536870912
