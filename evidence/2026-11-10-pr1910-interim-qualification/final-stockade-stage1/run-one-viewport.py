"""Prepared only: execute AFTER root's final-publish signal and exclusive GPU grant."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,signal,subprocess,time
p=argparse.ArgumentParser();p.add_argument('--viewport',choices=['desktop','mobile'],required=True);p.add_argument('--source-pin',required=True);p.add_argument('--published-build',required=True);a=p.parse_args()
R=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');P=Path('/tmp/nov10-final-stockade-smoke')/a.viewport;P.mkdir(parents=True,exist_ok=True);S=(R/'../../site/4d').resolve();sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
def snapshot():
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();build=json.loads((S/'build.json').read_text());files={}
 for rel in ['tools/smoke_renderer.mjs','renderers/web/js/main.js','renderers/web/js/fort-gates.js','assets/gltf/fort_dearborn_palisade__picket_1816.glb','assets/web/fort_dearborn_palisade__picket_1816.glb','assets/gltf/fort_dearborn_garrison_garden__fence_1816.glb','assets/web/fort_dearborn_garrison_garden__fence_1816.glb']:
  q=R/rel;files['source/'+rel]={'sha256':sha(q),'bytes':q.stat().st_size}
 for rel in ['build.json','data/gltf/fort_dearborn_palisade__picket_1816.glb','data/gltf/fort_dearborn_garrison_garden__fence_1816.glb']:
  q=S/rel;files['published/'+rel]={'sha256':sha(q),'bytes':q.stat().st_size}
 for root,label in [(R/'renderers/web/js','source-renderer'),(S/'walk/js','published-renderer')]:
  for q in sorted(root.rglob('*.js')):files[label+'/'+str(q.relative_to(root))]={'sha256':sha(q),'bytes':q.stat().st_size}
 return {'root_head':head,'published_build':build,'files':files}
before=snapshot();assert before['root_head']==a.source_pin,(before['root_head'],a.source_pin);assert before['published_build']['version']==a.published_build,(before['published_build'],a.published_build)
(P/'BEFORE-BINDINGS.json').write_text(json.dumps(before,indent=2)+'\n');env=os.environ.copy();env.update(PW_EXECUTABLE='/usr/bin/chromium',NODE_PATH='/tmp/chicago-browser-tools/node_modules',SMOKE_VIEWPORT=a.viewport,SMOKE_STAGE='1',SMOKE_TIMING='1');cmd=['node','tools/smoke_renderer.mjs','--published'];start=time.monotonic();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
timed_out=False
with (P/'stdout.log').open('wb') as out,(P/'stderr.log').open('wb') as err:
 proc=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err,start_new_session=True)
 try: proc.wait(timeout=590)
 except subprocess.TimeoutExpired:
  timed_out=True
  os.killpg(proc.pid,signal.SIGTERM)
  try: proc.wait(timeout=5)
  except subprocess.TimeoutExpired:
   os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=2)
 result=subprocess.CompletedProcess(cmd,proc.returncode)

after=snapshot();(P/'AFTER-BINDINGS.json').write_text(json.dumps(after,indent=2)+'\n');same=before['files']==after['files'];receipt={'status':'ACTUAL_PUBLISHED_STAGE1_PASS' if result.returncode==0 and same else 'ACTUAL_PUBLISHED_STAGE1_RED','started_utc':stamp,'seconds':time.monotonic()-start,'viewport':a.viewport,'command':cmd,'environment':{k:env[k] for k in ['PW_EXECUTABLE','NODE_PATH','SMOKE_VIEWPORT','SMOKE_STAGE','SMOKE_TIMING']},'cwd':str(R),'source_pin':a.source_pin,'published_build':a.published_build,'exit':result.returncode,'timed_out':timed_out,'assertions_and_models_unchanged_during_run':same,'stdout_sha256':sha(P/'stdout.log'),'stderr_sha256':sha(P/'stderr.log'),'claim_limit':'Supported official stage1 only, not the full smoke gate. Independent current published consumer, terrain/eye/card/picking and always-on assertions. No app/tool/assertion edits.'};(P/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));raise SystemExit(0 if result.returncode==0 and same else 1)
