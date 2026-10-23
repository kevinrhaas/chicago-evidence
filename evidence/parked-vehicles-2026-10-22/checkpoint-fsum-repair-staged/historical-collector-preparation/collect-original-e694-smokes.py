#!/usr/bin/env python3
"""One bounded GET-only observer of an already-dispatched exact-head smoke grid."""
import argparse, datetime, hashlib, json, os, pathlib, re, subprocess, time

REPO='kevinrhaas/chicago'
BRANCH='steward/parked-period-vehicles-20261021'
RANGES=['1-2','3-4','5','6-7','8','9-12','13','14','15']
SMOKE='.github/workflows/chicago-4d-smoke.yml'
NORMAL={
 '.github/workflows/chicago-4d-check.yml':('pull_request','gate',[
  'Set up job','Run actions/checkout@v4','Run actions/setup-python@v5',
  'Run actions/setup-node@v4','Install validator dependencies','How many cores this runner has',
  'Run the gate','Does this change carry a changelog entry?','Complete job']),
 '.github/workflows/chicago-4d-moving-frames.yml':('pull_request','moving-frames',[
  'Set up job','Run actions/checkout@v4','Run actions/setup-node@v4','Install Playwright',
  'Publish the mirror the gate serves (site/4d/ is generated)',
  'Walk, turn, fly and ride; hold the flora frame to its ceilings',
  'A phone keeps the town on the GPU, not twice','Complete job']),
 '.github/workflows/chicago-4d-pr-stuck.yml':('push','report',[
  'Set up job','Check the secret before doing anything','Run actions/checkout@v4',
  'Report every pull request nothing can move','Complete job']),
}
SMOKE_STEPS=['Set up job','Run actions/checkout@v4','Run actions/setup-node@v4',
 'Install Playwright','Publish the mirror the smoke serves (site/4d/ is generated)',
 'Run the smoke against the published mirror','Complete job']
def need(c,m):
 if not c:raise ValueError(m)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def save(path,value):
 tmp=path.with_suffix(path.suffix+'.new');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)
def smoke_cell(text):
 """Bind inputs to the actual published-smoke step's env, never dispatch order."""
 clean=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text)
 lines=[re.sub(r'^\d{4}-\d\d-\d\dT\S+Z\s*','',x) for x in clean.splitlines()]
 starts=[i for i,x in enumerate(lines) if x=='##[group]Run node tools/smoke_renderer.mjs --published']
 need(len(starts)==1,'Expected exactly one actual published-smoke log group')
 start=starts[0];end=next((i for i in range(start+1,len(lines)) if lines[i]=='##[endgroup]'),None)
 need(end is not None,'Incomplete published-smoke log group')
 group='\n'.join(lines[start:end])
 viewport=re.findall(r'^\s*SMOKE_VIEWPORT:\s*(\S+)\s*$',group,re.M)
 stage=re.findall(r'^\s*SMOKE_STAGE:\s*(\S+)\s*$',group,re.M)
 need(len(viewport)==len(stage)==1,'Missing or ambiguous actual viewport/stage')
 viewport,stage=viewport[0],stage[0]
 need(viewport in ['desktop','mobile'] and stage in RANGES,'Unexpected actual smoke cell')
 need(f'NOT THE FULL GATE — viewports filtered to "{viewport}"' in lines,'Runtime viewport does not match step env')
 need(f'NOT THE FULL GATE — stages filtered to "{stage}" of 15' in lines,'Runtime stage does not match step env')
 need(lines.count('SMOKE PASS')==1,'Actual single-cell smoke did not print one terminal PASS')
 return viewport,stage
def audit_job(job,run,head,name,required):
 need(job['run_id']==run['id'] and job.get('run_attempt')==1 and job.get('head_sha')==head,'Job identity/attempt drift')
 need(job['name']==name and job['status']=='completed' and job['conclusion']=='success','Job did not succeed')
 steps=job.get('steps',[])
 for wanted in required:
  matches=[s for s in steps if s['name']==wanted]
  need(len(matches)==1 and matches[0]['status']=='completed' and matches[0]['conclusion']=='success','Required actual step did not succeed: '+wanted)
 need(all(s['conclusion']=='success' for s in steps),'Unexpected skipped/failed job step')
 return {'run_id':run['id'],'job_id':job['id'],'job_name':name,'required_steps':required,'PASS':True}
def main():
 p=argparse.ArgumentParser(description='HELD exact-e694 historical smoke collection only, never current merge qualification')
 p.add_argument('--release',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True)
 p.add_argument('--minutes',type=int,default=180);p.add_argument('--interval',type=int,default=60);a=p.parse_args()
 head='e694849a2c516a9862a2564c5ff86d97406e09ab';receipt=pathlib.Path('/workspace/shared/parked-covered-2981-'+head+'-dispatch-once/receipt.json')
 previous=pathlib.Path('/workspace/shared/parked-covered-2981-'+head+'-CI-GET-owner1');d=json.loads(receipt.read_bytes());release=json.loads(a.release.read_bytes())
 need(1<=a.minutes<=180 and a.interval>=60,'Bound <=180min/poll no more than once a minute')
 need(release.get('status')=='ROOT_RELEASED_HISTORICAL_RUNTIME_COLLECTION' and release.get('allow_GET_collection') is True,'HELD: root historical collection release required')
 need(release.get('source_sha256')==sha(pathlib.Path(__file__).read_bytes()) and release.get('original_head')==head and release.get('original_dispatch_receipt_sha256')==sha(receipt.read_bytes()),'Release source/head/dispatch binding differs')
 need(d['repository']==REPO and d['branch']==BRANCH and d['sha']==head and d['pr']==1174 and d.get('dispatch_complete') is True and not d.get('error'),'Not the original completed e694 dispatch receipt')
 need(len(d['dispatches'])==18 and all(v.get('post_succeeded') for v in d['dispatches']),'Original18 POSTs not all accepted')
 selected={v['id'] for v in d['discovered_runs']};cells={(v,s) for v in ['desktop','mobile'] for s in RANGES}
 need(len(selected)==18 and {(v['viewport'],v['stage']) for v in d['dispatches']}==cells,'Original selected runs/grid differs')
 old=json.loads((previous/'terminal.json').read_bytes());need(old.get('qualification_pass') is False and old.get('error')=='Actual workflow failed: 39705450602 failure','Original failed qualification must remain recorded')
 need(not pathlib.Path('/proc',str(old['observer_pid'])).exists(),'Original observer still live; no duplicate owner')
 known=previous/'failure-gate-39705450602/FAILURE-EVIDENCE.json';kf=json.loads(known.read_bytes());need(kf['head']==head and kf['run_id']==39705450602 and kf['conclusion']=='failure' and kf['log_sha256']=='db35cfe6d80c7361d0a939c6e420867989254a9fc18595f91a1087cf739f620b','Known failed gate evidence differs')
 out=a.output.resolve();need(out.is_relative_to('/workspace/shared') and not out.exists(),'Fresh shared output required')
 for proc in pathlib.Path('/proc').iterdir():
  if not proc.name.isdigit() or int(proc.name)==os.getpid():continue
  try:args=[v.decode(errors='replace') for v in (proc/'cmdline').read_bytes().split(b'\0') if v]
  except (FileNotFoundError,PermissionError,ProcessLookupError):continue
  need(not(args and 'python' in pathlib.Path(args[0]).name and any(v.endswith('/collect-original-e694-smokes.py') for v in args[1:])),'A historical collector is already active')
 lock=pathlib.Path('/workspace/shared/parked-covered-2981-'+head+'.HISTORICAL-SMOKE-GET-owner1.lock');lock.mkdir(exist_ok=False);out.mkdir(exist_ok=False)
 deadline=time.monotonic()+a.minutes*60;start=time.monotonic();counter=0;audited={};bound={};last=None
 state={'status':'COLLECTING_ORIGINAL_E694_SMOKES_ONLY','original_head':head,'tree':d['tree'],'PR':1174,'repository':REPO,'original_branch':BRANCH,'started':now(),'collector_pid':os.getpid(),'source_sha256':sha(pathlib.Path(__file__).read_bytes()),'release':str(a.release),'release_sha256':sha(a.release.read_bytes()),'original_dispatch_receipt':str(receipt),'original_dispatch_receipt_sha256':sha(receipt.read_bytes()),'qualification_pass':False,'current_head_qualified':False,'known_normal_gate_failure':{'run_id':39705450602,'head':head,'evidence':str(known),'evidence_sha256':sha(known.read_bytes()),'log_sha256':kf['log_sha256'],'permanent_result':'failure; never rerun or erased by collection'},'source_pins_at_original_head':d['pins'],'prepared_workflow_identity_pins':d['prepared_workflow_identity_pins'],'scope':'Historical original18 exact-e694 runtime evidence, even after branch/PR head advances. Root alone owns runtime/source equivalence, fresh current-head normals and merge decisions. No current-head qualification claim.','POSTs':0,'reruns':0,'cancellations':0,'prior_owner_terminal_preserved':True}
 save(out/'owner.json',state)
 def api(label,endpoint,plain=False):
  nonlocal counter
  for attempt in range(1,4):
   need(time.monotonic()<deadline,'Observer deadline reached');counter+=1
   stem=out/(f'{counter:04d}-'+label+f'-attempt{attempt}')
   r=subprocess.run(['gh','api','--method','GET','repos/'+REPO+'/'+endpoint],text=True,capture_output=True,timeout=min(45,max(1,deadline-time.monotonic())))
   stem.with_suffix('.stdout').write_text(r.stdout);stem.with_suffix('.stderr').write_text(r.stderr)
   transient=(not re.search(r'HTTP (?:401|403)\b',r.stderr) and bool(re.search(r'HTTP (?:502|503|504)\b|unexpected EOF|connection reset by peer|transport read',r.stderr,re.I)))
   retry=bool(r.returncode and transient and attempt<3)
   record={'at':now(),'counter':counter,'label':label,'endpoint':endpoint,'attempt':attempt,'returncode':r.returncode,'transient_read':transient,'retry':retry,'delay_seconds':2**attempt if retry else 0,'stdout_sha256':sha(r.stdout.encode()),'stderr_sha256':sha(r.stderr.encode())}
   with (out/'GET-ATTEMPTS.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
   if retry:
    delay=2**attempt;need(time.monotonic()+delay<deadline,'Observer deadline reached before bounded GET retry');time.sleep(delay);continue
   need(r.returncode==0,'GET failed after explicit bounded read attempts: '+label+' '+r.stderr[-1200:])
   return r.stdout if plain else json.loads(r.stdout)

 try:
  while time.monotonic()<deadline:
   tick=time.monotonic();listing=api('original-head-runs','actions/runs?head_sha='+head+'&per_page=100');need(listing['total_count']==len(listing['workflow_runs']),'Incomplete original-head workflow listing')
   byid={r['id']:r for r in listing['workflow_runs']};need(selected<=set(byid),'An original selected run disappeared')
   current=[]
   for ident in sorted(selected):
    r=byid[ident];need(r['head_sha']==head and r['head_branch']==BRANCH and r['event']=='workflow_dispatch' and r['path']==SMOKE and r['run_attempt']==1,'Original selected source/workflow/attempt changed')
    current.append({k:r.get(k) for k in ['id','head_sha','head_branch','event','path','run_attempt','status','conclusion','html_url']})
   state.update(at=now(),original_selected_runs=current,other_workflows_at_original_head=[{k:r.get(k) for k in ['id','path','event','head_sha','status','conclusion']} for i,r in byid.items() if i not in selected],api_requests=counter)
   save(out/'latest.json',state)
   for r in current:
    if r['status']!='completed' or r['id'] in audited:continue
    need(r['conclusion']=='success','Original selected workflow failed: '+str(r['id'])+' '+str(r['conclusion']))
    jobs=api('jobs-'+str(r['id']),'actions/runs/'+str(r['id'])+'/jobs?per_page=100');need(jobs['total_count']==len(jobs['jobs'])==1,'Expected exactly one actual selected workflow job')
    job=jobs['jobs'][0];proof=audit_job(job,r,head,'smoke',SMOKE_STEPS)
    log=api('job-'+str(job['id'])+'-log','actions/jobs/'+str(job['id'])+'/logs',True);cell=smoke_cell(log);need(cell not in bound,'Two original runs claim the same cell')
    bound[cell]=r['id'];proof.update(viewport=cell[0],stage=cell[1],job_log_sha256=sha(log.encode()),workflow_path=SMOKE,original_head=head,historical_evidence_only=True);audited[r['id']]=proof;save(out/'audited-original-jobs.json',list(audited.values()))
   state.update(at=now(),selected_strict_success=len(audited),bound_cells=[{'viewport':v,'stage':s,'run_id':i} for (v,s),i in sorted(bound.items())],api_requests=counter)
   save(out/'latest.json',state);summary=(len(audited),tuple((r['id'],r['status'],r['conclusion']) for r in current))
   if summary!=last:print(json.dumps({'at':state['at'],'historical_original_selected_strict_success':len(audited),'qualification_pass':False}),flush=True);last=summary
   if len(audited)==18:
    need(set(bound)==cells,'Original log-bound coverage incomplete');state.update(status='ORIGINAL_E694_18_SMOKES_COLLECTED',historical_smoke_collection_complete=True);break
   remaining=min(a.interval-(time.monotonic()-tick),deadline-time.monotonic())
   if remaining>0:time.sleep(remaining)
  need(state.get('historical_smoke_collection_complete') is True,'Collector deadline without complete original18')
 except Exception as error:state.update(status='HISTORICAL_COLLECTION_STOPPED',error=str(error))
 finally:
  state.update(ended=now(),elapsed_seconds=time.monotonic()-start,selected_strict_success=len(audited),bound_cells=[{'viewport':v,'stage':s,'run_id':i} for (v,s),i in sorted(bound.items())],api_requests=counter,qualification_pass=False,current_head_qualified=False)
  save(out/'latest.json',state);save(out/'terminal.json',state);print(json.dumps({'status':state['status'],'historical_selected':len(audited),'qualification_pass':False,'known_normal_gate':'failure','error':state.get('error'),'output':str(out)}),flush=True)
 return 0 if state.get('historical_smoke_collection_complete') else 1
if __name__=='__main__':raise SystemExit(main())
