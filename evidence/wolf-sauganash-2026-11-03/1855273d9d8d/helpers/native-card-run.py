from pathlib import Path
import json,os,hashlib,subprocess,time
R=Path('/workspace/chicago-bridge-increment-20261102');A=R/'chicago/4d';O=Path('/workspace/combined-native-card-smoke-20261103')
plan=json.load(open('/workspace/combined-wolf-saug-plan-20261102.json'))
E=dict(os.environ,TMPDIR='/tmp/bg1102',TMP='/tmp/bg1102',TEMP='/tmp/bg1102',NODE_COMPILE_CACHE='/tmp/combined-native-card-cache-20261103',GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1')
for k in list(E):
 if k.startswith('SMOKE_'):del E[k]
def save(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
def guard():
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,env=E,text=True).strip()==plan['expected_head']
 assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=R,env=E)
 for p,r in plan['input_bindings'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==r['sha256'],p
x=json.load(open('/workspace/combined-wolf-saug-both-actual-20261102/RESULT.json'));assert x['status']=='FOCUSED_PUBLISHED_COMBINED_WOLF_SAUG_BOTH_PASS' and x['head']==plan['expected_head']
assert plan['expected_head']=='1855273d9d8d423db20ea072a95d8169bda7ae71'
assert x['source_scope_sha256']==plan['source_scope_sha256']
guard();rows=[]
for viewport in ['mobile','desktop']:
 guard();log=O/(viewport+'.log');rp=O/(viewport+'-REAPER.json');assert not log.exists()and not rp.exists()
 env=dict(E,SMOKE_VIEWPORT=viewport,SMOKE_STAGE='3',SMOKE_ROOT=str(R/'site/4d'),SMOKE_SHOTS=str(O/(viewport+'-shots')))
 cmd=['python3','/workspace/shared/run-with-reaping.py',str(rp),'--','timeout','--signal=TERM','--kill-after=15s','600s','nice','-n','19','taskset','-c','0,1,3,4','node','tools/smoke_renderer.mjs','--published']
 t=time.monotonic()
 with log.open('xb')as f:p=subprocess.run(cmd,cwd=A,env=env,stdout=f,stderr=subprocess.STDOUT)
 receipt=json.load(open(rp));row={'viewport':viewport,'exit':p.returncode,'seconds':time.monotonic()-t,'log':str(log),'reaper':receipt};rows.append(row);save('PROGRESS.json',rows);guard()
 print(json.dumps({k:row[k]for k in ['viewport','exit','seconds']}),flush=True)
 assert p.returncode==receipt['command_exit']==0 and receipt['all_children_reaped']and not receipt['leftover_cleanup'],row
 assert 'SMOKE PASS' in log.read_text(errors='replace')
save('RESULT.json',{'status':'NATIVE_PUBLISHED_CARD_PART3_BOTH_PASS','head':plan['expected_head'],'rows':rows,'selected_inputs_and_source_clean':True,'scope':'Native published part3 card/ground/confidence regression at both viewports after combined Wolf picture/source and Sauganash MASTER/WEB geometry changes. Targeted combined visible-card/exterior/native-arrival PASS is a prerequisite. Whole15-part gate, historical source-camera calibration, door traversal and full-hotel picture signoff are not claimed.'})
