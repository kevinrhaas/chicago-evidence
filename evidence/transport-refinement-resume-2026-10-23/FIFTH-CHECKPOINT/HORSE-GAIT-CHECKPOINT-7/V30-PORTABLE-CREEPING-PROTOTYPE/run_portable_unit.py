from pathlib import Path
import subprocess,time,resource,json,hashlib,sys,shutil,os
d=Path(__file__).parent;start=time.monotonic();reports=[]
commands=[[sys.executable,str(d.parent/'encode_portable_v30.py')],[shutil.which('node'),str(d/'read_native_mixer.mjs')],[sys.executable,str(d/'check_actual_readback.py')]]
try:
 for command in commands:
  p=subprocess.run(command,cwd=d,timeout=max(1,235-(time.monotonic()-start)),check=False);reports.append({'command':command,'returncode':p.returncode});assert p.returncode==0,'Actual unit failed; do not proceed or relabel green.'
finally:
 out={'status':'ACTUAL_BOUNDED_PORTABLE_UNIT_PASS'if len(reports)==3 and all(q['returncode']==0 for q in reports)else'ACTUAL_BOUNDED_PORTABLE_UNIT_FAIL','commands':reports,'maximum_child_RSS_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024,'elapsed_seconds':time.monotonic()-start,'source_sha256':{str(p.relative_to(d.parent)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[d.parent/'encode_portable_v30.py',d/'basis.py',d/'read_native_mixer.mjs',d/'check_actual_readback.py',d/'run_portable_unit.py']},'app_or_browser_writes':False,'natural_gait_accepted':False};(d/'ACTUAL-UNIT-RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
assert out['maximum_child_RSS_bytes']<=536870912
