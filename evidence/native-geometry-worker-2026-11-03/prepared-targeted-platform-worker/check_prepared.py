from pathlib import Path
import os,json,subprocess,hashlib,time
import yaml
O=Path(__file__).resolve().parent
start=time.monotonic()
p=O/'postimages/.github/workflows/steward-improve.yml'
w=yaml.safe_load(p.read_bytes());before=yaml.safe_load((O/'preimages/.github/workflows/steward-improve.yml').read_bytes())
assert w['jobs']['targeted-chicago']['runs-on']=='ubuntu-26.04'
assert w['jobs']['targeted-chicago']['timeout-minutes']==150
assert w['jobs']['targeted-chicago']['steps'] is w['jobs']['improve']['steps']
assert w['jobs']['improve']['runs-on']==before['jobs']['improve']['runs-on']
assert w['jobs']['improve']['timeout-minutes']==before['jobs']['improve']['timeout-minutes']==150
assert w['jobs']['chatgpt']['timeout-minutes']==before['jobs']['chatgpt']['timeout-minutes']==180
cmd=['git','apply','--check',str(O/'targeted-worker.patch')]
r=subprocess.run(cmd,cwd=O/'preimages',capture_output=True,text=True);assert r.returncode==0,r.stderr
base=os.environ.copy()
for k in ['PROCESSOR','MODEL','EFFORT','FOCUS_APP','LANE','INPUT_SLICE','INPUT_SLICES','INPUT_MAX_TURNS','QUEUE_POSITION','FINISH_ONLY','TARGET_TICKET']:base.pop(k,None)
cases=[('default unchanged',{},0),('exact native target',{'TARGET_TICKET':'T-2380','FOCUS_APP':'chicago','PROCESSOR':'claude'},0),('other valid ticket',{'TARGET_TICKET':'T-3041','FOCUS_APP':'chicago','PROCESSOR':'claude'},0),('malformed',{'TARGET_TICKET':'T-2380\nwork elsewhere','FOCUS_APP':'chicago'},1),('wrong app',{'TARGET_TICKET':'T-2380','FOCUS_APP':'manager.polecat.live'},1),('unsupported worker',{'TARGET_TICKET':'T-2380','FOCUS_APP':'chicago','PROCESSOR':'gpt'},1),('finish-only conflict',{'TARGET_TICKET':'T-2380','FOCUS_APP':'chicago','FINISH_ONLY':'1'},1),('multiple slots',{'TARGET_TICKET':'T-2380','FOCUS_APP':'chicago','INPUT_SLICES':'2'},1),('queue ordinal conflict',{'TARGET_TICKET':'T-2380','FOCUS_APP':'chicago','QUEUE_POSITION':'1/5'},1)]
rows=[]
for name,env,expected in cases:
 r=subprocess.run(['node',str(O/'postimages/.github/steward/validate-run.mjs')],env={**base,**env},capture_output=True,text=True)
 assert (r.returncode==0)==(expected==0),(name,r.stderr)
 rows.append({'case':name,'actual_exit':r.returncode,'expected':expected})
for name in ['improve','targeted-chicago','chatgpt']:assert 'target_ticket' in w['jobs'][name]['if']
result={'status':'PREPARED_PATCH_VALIDATION_PASS_NOT_DISPATCHED','git_apply_check':True,'yaml_parse':True,'native_target_literal_image':'ubuntu-26.04','shared_complete_existing_steps':True,'native_target_budget_minutes':150,'normal_public_and_private_budgets_unchanged':True,'validator_cases':rows,'seconds':time.monotonic()-start,'scope':'External preimages/postimages only. No source/branch/workflow/dispatch/claim/model/Blender changed.'}
(O/'QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'cases':len(rows),'seconds':result['seconds']}))
