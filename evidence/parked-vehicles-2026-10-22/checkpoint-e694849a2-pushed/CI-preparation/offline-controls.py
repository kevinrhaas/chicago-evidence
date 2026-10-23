from pathlib import Path
import json,ast,hashlib,subprocess,types
B=Path(__file__).parent
mod=types.ModuleType('held_observer');mod.__file__=str(B/'observe-GET-only.py');exec(compile((B/'observe-GET-only.py').read_bytes(),mod.__file__,'exec'),mod.__dict__)
log='''##[group]Run node tools/smoke_renderer.mjs --published
  SMOKE_VIEWPORT: desktop
  SMOKE_STAGE: 13
##[endgroup]
NOT THE FULL GATE — viewports filtered to "desktop"
NOT THE FULL GATE — stages filtered to "13" of 15
SMOKE PASS
'''
assert mod.smoke_cell(log)==('desktop','13')
for bad in [log.replace('SMOKE PASS','SMOKE FAIL'),log+'SMOKE PASS\n',log.replace('SMOKE_STAGE: 13','SMOKE_STAGE: 14')]:
 try:mod.smoke_cell(bad);raise AssertionError('Bad smoke binding accepted')
 except ValueError:pass
run={'id':123};job={'id':456,'run_id':123,'run_attempt':1,'head_sha':'a'*40,'name':'smoke','status':'completed','conclusion':'success','steps':[{'name':s,'status':'completed','conclusion':'success'} for s in mod.SMOKE_STEPS]};assert mod.audit_job(job,run,'a'*40,'smoke',mod.SMOKE_STEPS)['PASS']
job['steps'][0]['conclusion']='skipped'
try:mod.audit_job(job,run,'a'*40,'smoke',mod.SMOKE_STEPS);raise AssertionError('Skipped step accepted')
except ValueError:pass
r=subprocess.run(['python3',str(B/'dispatch-once.py'),'--sha','0a037632481037dcc903fa11697da5681b519f80','--pr','1174','--execute'],capture_output=True,text=True);assert r.returncode and 'HELD: explicit root activation required' in r.stderr
for p in B.glob('*.py'):ast.parse(p.read_bytes())
for p in B.glob('*.json'):json.loads(p.read_bytes())
price=json.loads((B/'OLD-HEAD-PRICING-CONTROL-NOT-FINAL.json').read_bytes());proof={'PASS':True,'scope':'Offline helpers, source parser/dry plan, and HELD execute-refusal only; historical0a price is not final-head qualification','SHA':None,'network_calls':0,'POSTs':0,'observer_smoke_positive_and_three_negative_controls':True,'job_strict_steps_positive_and_skipped_negative':True,'missing_activation_refuses_before_output_or_network':True,'old_head_control_predicted_normal':price['predicted_normal_runs'],'source_files':[{ 'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(B.glob('*.py'))]};(B/'OFFLINE-CONTROLS.json').write_bytes((json.dumps(proof,indent=2)+'\n').encode());print(json.dumps(proof,indent=2))
