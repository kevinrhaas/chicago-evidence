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
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--receipt',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True)
 p.add_argument('--minutes',type=int,default=180);p.add_argument('--interval',type=int,default=60)
 a=p.parse_args();need(1<=a.minutes<=180 and a.interval>=60,'Bound <=180min; poll no more than once/minute')
 d=json.loads(a.receipt.read_text());head=d['sha'];pr=d['pr']
 need(d.get('lane_identity')=='parked-covered-2981-nexthead-v1','Not a fresh next-head dispatch receipt')
 need(head not in ['2aebef95f6a5b6fa1bd8353db936c7674a73c32f','0a037632481037dcc903fa11697da5681b519f80'],'Historical head cannot qualify')
 need(d.get('caller_sha256')==sha((pathlib.Path(__file__).parent/'dispatch-once.py').read_bytes()),'Dispatch source identity mismatch')
 need(d.get('prepared_workflow_identity_pins')==json.loads((pathlib.Path(__file__).parent/'PREPARED-WORKFLOW-PINS.json').read_bytes())['pins'],'Mandatory workflow pin identity differs')
 need(d['repository']==REPO and d['branch']==BRANCH and d.get('dispatch_complete') and not d.get('error'),'Dispatch/reconciliation receipt not complete')
 need(re.fullmatch('[0-9a-f]{40}',head) and isinstance(pr,int),'Invalid head/PR')
 selected={r['id'] for r in d['discovered_runs']};cells={(v,s) for v in ['desktop','mobile'] for s in RANGES}
 need(len(selected)==18 and len(d['dispatches'])==18 and all(x.get('post_succeeded') for x in d['dispatches']),'Not exactly18 accepted/discovered requests')
 need({(x['viewport'],x['stage']) for x in d['dispatches']}==cells,'Dispatch cell coverage changed')
 out=a.output.resolve();need(out.is_relative_to(pathlib.Path('/workspace/shared')),'Output must be fresh under shared');out.mkdir(exist_ok=False)
 (pathlib.Path('/workspace/shared')/('parked-covered-2981-nexthead-'+head+'.GET-OBSERVER.lock')).mkdir(exist_ok=False)
 deadline=time.monotonic()+a.minutes*60;start=time.monotonic();counter=0;audited={};bound={};last=None
 state={'head':head,'pr':pr,'repository':REPO,'branch':BRANCH,'started':now(),'observer_pid':os.getpid(),
  'source_sha256':sha(pathlib.Path(__file__).read_bytes()),'dispatch_receipt':str(a.receipt),
  'dispatch_receipt_sha256':sha(a.receipt.read_bytes()),'scope':'GET-only CI qualification; root still performs fresh required-check/mergeability and ordinary merge','qualification_pass':False}
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

 def current_pr():
  obj=api('pr','pulls/'+str(pr));need(obj['state']=='open' and obj['head']['sha']==head and obj['head']['ref']==BRANCH and obj['head']['repo']['full_name']==REPO and obj['base']['ref']=='dev','PR route/source changed')
  return {k:obj.get(k) for k in ['number','state','draft','mergeable','mergeable_state','updated_at']}
 try:
  while time.monotonic()<deadline:
   tick=time.monotonic();runs=api('runs','actions/runs?head_sha='+head+'&per_page=100')
   need(runs['total_count']==len(runs['workflow_runs']),'Incomplete workflow list')
   byid={r['id']:r for r in runs['workflow_runs']}
   need(selected<=set(byid),'Dispatched run disappeared')
   normal=[];unexpected=[]
   for r in byid.values():
    need(r['head_sha']==head and r['head_branch']==BRANCH and r['run_attempt']==1,'Workflow identity/attempt changed')
    if r['id'] in selected:need(r['path']==SMOKE and r['event']=='workflow_dispatch','Selected workflow route changed')
    elif r['path'] in NORMAL:
     need(r['event']==NORMAL[r['path']][0],'Normal workflow trigger changed');normal.append(r)
    else:unexpected.append({'id':r['id'],'path':r['path'],'event':r['event'],'status':r['status'],'conclusion':r['conclusion']})
   need(not unexpected,'Unexpected workflow; inspect current source triggers before qualifying: '+str(unexpected))
   for path in NORMAL:need(sum(r['path']==path for r in normal)<=1,'Duplicate normal run; inspect before qualifying')
   for r in byid.values():
    if r['status']!='completed' or r['id'] in audited:continue
    need(r['conclusion']=='success','Actual workflow failed: '+str(r['id'])+' '+str(r['conclusion']))
    jobs=api('jobs-'+str(r['id']),'actions/runs/'+str(r['id'])+'/jobs?per_page=100')
    need(jobs['total_count']==len(jobs['jobs'])==1,'Expected exactly one actual workflow job')
    job=jobs['jobs'][0]
    if r['id'] in selected:
     proof=audit_job(job,r,head,'smoke',SMOKE_STEPS)
     log=api('job-'+str(job['id'])+'-log','actions/jobs/'+str(job['id'])+'/logs',True)
     cell=smoke_cell(log);need(cell not in bound,'Two actual runs claim the same viewport/stage')
     bound[cell]=r['id'];proof.update(viewport=cell[0],stage=cell[1],job_log_sha256=sha(log.encode()))
    else:
     _,name,required=NORMAL[r['path']];proof=audit_job(job,r,head,name,required)
    proof['workflow_path']=r['path'];audited[r['id']]=proof;save(out/'audited-jobs.json',list(audited.values()))
   state.update(at=now(),pr_state=current_pr(),workflow_count=len(byid),
    runs=[{k:r.get(k) for k in ['id','path','event','status','conclusion','html_url']} for r in byid.values()],
    selected_success=sum(i in audited for i in selected),normal_success=sum(r['id'] in audited for r in normal),
    bound_cells=[{'viewport':v,'stage':s,'run_id':i} for (v,s),i in sorted(bound.items())],api_requests=counter)
   summary=(state['selected_success'],state['normal_success'],tuple(sorted((r['id'],r['status'],r['conclusion']) for r in byid.values())))
   save(out/'latest.json',state)
   if summary!=last:
    with (out/'transitions.jsonl').open('a') as f:f.write(json.dumps(state)+'\n')
    print(json.dumps({'at':state['at'],'selected_strict_success':state['selected_success'],'normal_strict_success':state['normal_success'],'total_workflows':state['workflow_count']}),flush=True);last=summary
   if state['selected_success']==18 and len(normal)==3 and state['normal_success']==3:
    need(set(bound)==cells,'Actual log-bound grid coverage incomplete')
    state['current_checks']=api('fresh-checks','commits/'+head+'/check-runs?per_page=100')
    state['current_statuses']=api('fresh-statuses','commits/'+head+'/status')
    need(api('fresh-branch','git/ref/heads/'+BRANCH)['object']['sha']==head,'Remote source branch changed')
    state['pr_state']=current_pr();state['qualification_pass']=True;state['ready_for_root_fresh_merge_check']=True
    break
   remaining=min(a.interval-(time.monotonic()-tick),deadline-time.monotonic())
   if remaining>0:time.sleep(remaining)
  need(state.get('qualification_pass'),'Observer deadline without complete actual qualification')
 except Exception as error:
  state['error']=str(error)
 finally:
  state.update(ended=now(),elapsed_s=time.monotonic()-start,api_requests=counter)
  save(out/'latest.json',state);save(out/'terminal.json',state)
  print(json.dumps({'qualification_pass':state['qualification_pass'],'selected':state.get('selected_success',0),'normal':state.get('normal_success',0),'error':state.get('error'),'output':str(out)}),flush=True)
 return 0 if state.get('qualification_pass') else 1
if __name__=='__main__':raise SystemExit(main())
