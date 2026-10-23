#!/usr/bin/env python3
"""HELD CI_ONLY exact-head remote23 evidence; never local/merge qualification.
Reuses exact original smoke_cell/audit_job helpers; no POST/rerun/cancel capability.
"""
import argparse,base64,datetime,hashlib,json,os,pathlib,re,subprocess,time
from guarded_bake import BAKE,audit_guarded_bake_jobs,audit_guarded_bake_log
REPO='kevinrhaas/chicago'
BRANCH='steward/1835-workwear-repair-20261021'
SMOKE='.github/workflows/chicago-4d-smoke.yml'
RANGES=['1-2','3-4','5','6-7','8','9-12','13','14','15']
SMOKE_STEPS=['Set up job','Run actions/checkout@v4','Run actions/setup-node@v4','Install Playwright','Publish the mirror the smoke serves (site/4d/ is generated)','Run the smoke against the published mirror','Complete job']
NORMAL={
 '.github/workflows/chicago-4d-check.yml':('gate',['Set up job','Run actions/checkout@v4','Run actions/setup-python@v5','Run actions/setup-node@v4','Install validator dependencies','How many cores this runner has','Run the gate','Does this change carry a changelog entry?','Complete job']),
 '.github/workflows/chicago-4d-moving-frames.yml':('moving-frames',['Set up job','Run actions/checkout@v4','Run actions/setup-node@v4','Install Playwright','Publish the mirror the gate serves (site/4d/ is generated)','Walk, turn, fly and ride; hold the flora frame to its ceilings','A phone keeps the town on the GPU, not twice','Complete job']),
 '.github/workflows/chicago-4d-pr-stuck.yml':('report',['Set up job','Check the secret before doing anything','Run actions/checkout@v4','Report every pull request nothing can move','Complete job']),
 '.github/workflows/chicago-4d-humans.yml':('humans',['Set up job','Run actions/checkout@v4','Run actions/setup-python@v5','Run actions/setup-node@v4','Run pip install --quiet jsonschema','Read the Blender pin','Cache Blender','Rebuild the fixture and require the committed bytes','Install Playwright','Open every human GLB in the browser, at both viewports','Drive the browser actor with the fixture, at both viewports','Complete job']),
}


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


def checkout_sha(text,expected):
    clean=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text)
    lines=[re.sub(r'^\d{4}-\d\d-\d\dT\S+Z\s*','',x) for x in clean.splitlines()]
    values=[]
    for i,line in enumerate(lines):
        if re.fullmatch(r'\[command\].*[/ ]git log -1 --format=%H',line):
            need(i+1<len(lines) and re.fullmatch('[a-f0-9]{40}',lines[i+1]),'Missing exact checkout log SHA')
            values.append(lines[i+1])
    need(values==[expected],'Actual checkout SHA differs or is ambiguous: '+repr(values))
    return values[0]


def audit_human_jobs(jobs,run,head):
    names={j['name']:j for j in jobs}
    need(len(names)==len(jobs) and set(names)=={'humans','teamster-studies'},'Expected normal humans and explicit skipped dependent job')
    skipped=names['teamster-studies']
    need(skipped['run_id']==run['id'] and skipped.get('run_attempt')==1 and skipped.get('head_sha')==head and skipped['status']=='completed' and skipped['conclusion']=='skipped','Normal PR must not rebuild canonical teamster studies')
    name,steps=NORMAL['.github/workflows/chicago-4d-humans.yml']
    proof=audit_job(names[name],run,head,name,steps)
    proof['expected_skipped_dependent_job_id']=skipped['id']
    return names[name],proof



def audit_population_boot(text,viewport):
    # This positive ordinary-scene line is emitted before stage filtering. Old
    # zero-human smoke logs cannot qualify a first standing-population run.
    label='desktop 1280x800' if viewport=='desktop' else 'mobile 390x780'
    for suffix in ["the human layer mounts exactly the scene's eligible records",'human requests obey the exact scene-year gate']:
        matches=[line for line in text.splitlines() if 'pass  '+label+': '+suffix in line]
        need(len(matches)==1,'Missing/ambiguous actual new ordinary-population bootstrap PASS: '+suffix)
    return {'ordinary_eligible_human_boot_PASS':True,'exact_scene_year_request_gate_PASS':True}


def audit_focused_town(release, head, baseline):
 """Local completed receipts, separate from remote CI; no browser/network or fabricated PASS."""
 need(release.get('focused_published_desktop_mobile_PASS') is True,'Actual focused desktop/mobile PASS is mandatory before final merge qualification')
 need(release.get('focused_town_pngs_reviewed') is True,'Root must actually review final-head desktop/mobile PNGs')
 cp=pathlib.Path(release.get('canonical_inputs_path') or '')
 need(cp.is_absolute() and cp.is_relative_to('/workspace/shared'),'Exact outside canonical-input receipt path required')
 cb=cp.read_bytes();canonical=json.loads(cb);need(sha(cb)==release.get('canonical_inputs_sha256'),'Canonical input JSON hash differs')
 need(canonical.get('state')=='ROOT_PINNED_FINAL_CANONICAL_INPUTS' and canonical.get('final_head')==head,'Actual final canonical/head differs')
 for key in ['canonical_run_id','canonical_source_sha','artifact_zip_sha256','instance_sha256','web_lods']:
  need(canonical.get(key)==baseline.get(key),'Actual final canonical baseline differs: '+key)
 entries=release.get('focused_town_receipts');phases={'desktop_visual','desktop_functional','mobile_full'}
 need(isinstance(entries,list) and len(entries)==3 and {r.get('phase') for r in entries}==phases,'Three actual final split-town phase receipts required')
 proofs={};shared_pins=None;shared_index=None
 for entry in entries:
  rp=pathlib.Path(entry.get('path') or '');need(rp.is_absolute() and rp.is_relative_to('/workspace/shared'),'Outside town receipt path required')
  raw=rp.read_bytes();row=json.loads(raw);need(sha(raw)==entry.get('sha256'),'Town receipt byte pin differs')
  phase=entry['phase'];need(row.get('identity')=='actual_published_bardwell_final_head_split_v1','Actual final split-town receipt identity required');config=row.get('config',{});need(config.get('phase')==phase and config.get('viewport')==('mobile' if phase=='mobile_full' else 'desktop') and config.get('expectedHead')==head and config.get('expectedIndexDigest')==canonical.get('final_index_digest') and config.get('expectedCanonicalInputsSHA')==sha(cb) and config.get('maxMillis')==540000 and config.get('released') is True and config.get('rootLaneClosed') is True,'Actual town release/framing/cap identity differs');need(row.get('phase')==phase and row.get('head')==head and row.get('pass') is True and row.get('closed') is True and row.get('sourceUnchanged') is True and not row.get('deadlineReached') and not row.get('error') and not row.get('closeError'),'Actual final-head town phase not PASS/CLOSED/unchanged')
  need(not row.get('pageErrors') and not row.get('httpErrors'),'Actual town phase has runtime/HTTP errors')
  need(row.get('indexDigest')==canonical.get('final_index_digest'),'Town/canonical index differs')
  need(row.get('inputPins',{}).get(str(cp))==sha(cb),'Town phase lacks exact canonical JSON pin')
  if shared_pins is None:shared_pins=row['inputPins'];shared_index=row['indexDigest']
  need(row.get('inputPins')==shared_pins and row['indexDigest']==shared_index,'Town phases do not share exact final source/published/canonical pins')
  captures=row.get('captures',[])
  if phase=='desktop_visual':need(row.get('desktopVisualPass') is True and len(captures)==4 and row.get('timing',{}).get('samples')==7 and not row.get('loader') and not row.get('far'),'Desktop visual coverage incomplete')
  elif phase=='desktop_functional':need(row.get('desktopFunctionalPass') is True and not captures and [r.get('lod') for r in row.get('loader',[])]==list(range(4)) and row.get('far',{}).get('state',{}).get('lod')==3,'Desktop functional loader/far coverage incomplete')
  else:need(len(captures)==4 and row.get('timing',{}).get('samples')==7 and [r.get('lod') for r in row.get('loader',[])]==list(range(4)) and row.get('far',{}).get('state',{}).get('lod')==3,'Mobile full coverage incomplete')
  for image in captures:
   filename=image.get('file','');need(pathlib.Path(filename).name==filename and filename.endswith('.png'),'Unexpected capture filename')
   data=(rp.parent/filename).read_bytes();need(len(data)==image.get('bytes') and sha(data)==image.get('sha256'),'Actual reviewed town PNG bytes differ')
  proofs[phase]={'path':str(rp),'sha256':sha(raw),'captures':len(captures),'receipt':row}
 inherited=proofs['desktop_functional']['receipt'].get('inheritedVisual',{})
 need(inherited.get('receipt')==proofs['desktop_visual']['path'] and inherited.get('sha256')==proofs['desktop_visual']['sha256'] and inherited.get('head')==head and inherited.get('separateExecution') is True,'Functional phase does not bind actual same-head visual receipt')
 return {'PASS':True,'head':head,'indexDigest':shared_index,'canonical_inputs_path':str(cp),'canonical_inputs_sha256':sha(cb),'phases':{name:{k:v for k,v in proof.items() if k!='receipt'} for name,proof in proofs.items()},'scope':'Actual three final split-town phases plus root PNG review; no photo/full-population acceptance'}

def audit_ci_only_scope(release, head, baseline):
 """Retain false local evidence honestly; CI_ONLY never supplies local/merge PASS."""
 need(release.get('collection_mode')=='CI_ONLY','Explicit CI_ONLY release mode required')
 local=release.get('ci_only_local_evidence')
 need(isinstance(local,dict) and local.get('status')=='CI_ONLY_NOT_FINAL_QUALIFICATION','Explicit CI_ONLY local context required; no final qualification supplied')
 cp=pathlib.Path(release.get('canonical_inputs_path') or '')
 need(cp.is_absolute() and cp.is_relative_to('/workspace/shared'),'Exact outside canonical-input receipt path required')
 cb=cp.read_bytes();canonical=json.loads(cb);need(sha(cb)==release.get('canonical_inputs_sha256'),'Canonical input JSON hash differs')
 need(canonical.get('state')=='ROOT_PINNED_FINAL_CANONICAL_INPUTS' and canonical.get('final_head')==head,'Actual pinned canonical/head differs')
 for key in ['canonical_run_id','canonical_source_sha','artifact_zip_sha256','instance_sha256','web_lods']:
  need(canonical.get(key)==baseline.get(key),'Actual pinned canonical baseline differs: '+key)
 return {'mode':'CI_ONLY','PASS':False,'local_qualified':False,'head':head,'canonical_inputs_path':str(cp),'canonical_inputs_sha256':sha(cb),'actual_local_evidence':local,'scope':'Exact-head remote23 evidence only. Recorded local successes and supplementary stress failures stay separate; CI_ONLY never supplies final qualification or merge readiness.'}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--release',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True)
 a=p.parse_args();release=json.loads(a.release.read_bytes());source=pathlib.Path(__file__)
 need(release.get('released') is True and release.get('status')=='ROOT_RELEASED_HUMAN1175_CI_ONLY_GET_COLLECTION' and release.get('allow_GET_collection') is True,'HELD: root immutable GET collection release required')
 need(release.get('collector_sha256')==sha(source.read_bytes()),'Collector identity differs')
 need(release.get('repository')==REPO and release.get('branch')==BRANCH and release.get('pr')==1175 and release.get('base_ref')=='dev','Release route differs')
 head,tree,base,merge=[release.get(k) for k in ['sha','tree','base_sha','merge_sha']]
 need(all(isinstance(x,str) and re.fullmatch('[a-f0-9]{40}',x) for x in [head,tree,base,merge]),'Root must pin final head/tree/base/merge')
 need(head not in ['34cf462ed343b8b2b70da70303344fff7e5e083f','2f75ef23dbb316ebe4cf53e65ce3af8b04f140d3'],'Historical canonical head cannot qualify new standing population')
 need(release.get('poll_seconds')==61 and release.get('max_minutes')==150,'Fixed61s polling/150min bound required')
 baseline_bytes=(source.parent/'CANONICAL-BARDWELL-BASELINE.json').read_bytes();baseline=json.loads(baseline_bytes)
 need(release.get('canonical_baseline_sha256')==sha(baseline_bytes),'Actual canonical baseline pin differs')
 focused_proof=audit_ci_only_scope(release,head,baseline)
 receipt_path=pathlib.Path(release['dispatch_receipt']);d=json.loads(receipt_path.read_bytes())
 need(release.get('dispatch_receipt_sha256')==sha(receipt_path.read_bytes()),'Dispatch receipt binding differs')
 need(d.get('lane_identity')=='human-standing-1175-nexthead-v1' and d.get('repository')==REPO and d.get('branch')==BRANCH and d.get('sha')==head and d.get('tree')==tree and d.get('pr')==1175 and d.get('dispatch_complete') is True and not d.get('error'),'Not completed exact new-head dispatch/reconciliation')
 need(d.get('caller_sha256')==sha((source.parent/'dispatch-once.py').read_bytes()),'Dispatcher source binding differs')
 need(d.get('canonical_baseline_sha256')==sha(baseline_bytes) and d.get('focused_town_required_before_merge') is True,'Dispatch did not bind current canonical baseline/deferred local obligation')
 pins=json.loads((source.parent/'PREPARED-WORKFLOW-PINS.json').read_bytes())['pins']
 need(d.get('prepared_workflow_identity_pins')==pins,'Prepared workflow identity changed')
 cells={(v,s) for v in ['desktop','mobile'] for s in RANGES};selected={r['id'] for r in d['discovered_runs']}
 need(len(selected)==len(d['discovered_runs'])==18 and len(d['dispatches'])==18 and all(x.get('post_succeeded') for x in d['dispatches']) and {(x['viewport'],x['stage']) for x in d['dispatches']}==cells,'Exact18 accepted/discovered smoke grid required')
 normal=release.get('normal_runs');need(isinstance(normal,list) and len(normal)==4 and {x['path'] for x in normal}==set(NORMAL),'Pin exactly gate/moving/report/humans routes')
 normal_by_id={x['id']:x for x in normal};need(len(normal_by_id)==4 and not selected.intersection(normal_by_id),'Duplicate selected/normal run IDs')
 expected_events={'.github/workflows/chicago-4d-check.yml':'pull_request','.github/workflows/chicago-4d-pr-stuck.yml':'push','.github/workflows/chicago-4d-humans.yml':'pull_request'}
 pricepath=pathlib.Path(release['final_diff_pricing']);price=json.loads(pricepath.read_bytes())
 need(sha(pricepath.read_bytes())==release.get('final_diff_pricing_sha256') and price.get('sha')==head and price.get('tree')==tree and price.get('pr_base')==base and price.get('expected_normal_contract') is True,'Final diff pricing/source/base binding differs')
 guard=release.get('guarded_bake_run');guarded_by_id={}
 if price.get('expected_guarded_bake') is not None:
  rule=price['expected_guarded_bake'];need(rule.get('path')==BAKE and rule.get('event')=='push' and rule.get('source_owned') is False and rule.get('source_owned_trigger_paths')==[] and rule.get('workflow_sha256')==pins[BAKE],'Pricing does not bind exact expected source-owned=false bake guard')
  need(isinstance(guard,dict) and set(guard)=={'id','path','event'} and isinstance(guard['id'],int) and guard['path']==BAKE and guard['event']=='push' and guard['id'] not in selected|set(normal_by_id),'Pin one distinct actual guarded bake run')
  need(release.get('guarded_bake_audit_sha256')==sha((source.parent/'guarded_bake.py').read_bytes()),'Reviewed bake audit helper identity differs');guarded_by_id={guard['id']:guard}
 else:need(guard is None,'Unpriced extra guard run is not allowed')
 expected_events['.github/workflows/chicago-4d-moving-frames.yml']=price['moving_required_event']
 need(all(x.get('event')==expected_events[x['path']] for x in normal),'Normal trigger route does not match actual final diff')
 out=a.output.resolve();need(out.is_relative_to('/workspace/shared') and not out.exists(),'Fresh shared output required')
 # A persistent exact-head lock prevents duplicate owners, even after interruption.
 for proc in pathlib.Path('/proc').iterdir():
  if not proc.name.isdigit() or int(proc.name)==os.getpid():continue
  try:args=[x.decode(errors='replace') for x in (proc/'cmdline').read_bytes().split(b'\0') if x]
  except (FileNotFoundError,PermissionError,ProcessLookupError):continue
  need(not(args and 'python' in pathlib.Path(args[0]).name and any(x.endswith('/collect-GET-only.py') for x in args[1:]) and '--release' in args),'A GET collector is already live; no duplicate owner')
 lock=pathlib.Path('/workspace/shared')/('human-standing-1175-'+head+'.GET-owner.lock');lock.mkdir(exist_ok=False);out.mkdir(exist_ok=False)
 started=time.monotonic();deadline=started+150*60;counter=0;audited={};bound={};last=None;workflow_ids={}
 state={'status':'GET_COLLECTING','focused_town_proof':focused_proof,'qualification_pass':False,'ci_only_pass':False,'ready_for_root_fresh_merge_review':False,'collection_mode':'CI_ONLY','head':head,'tree':tree,'base_ref':'dev','base_sha':base,'merge_sha':merge,'pr':1175,'branch':BRANCH,'observer_pid':os.getpid(),'started':now(),'deadline_utc':(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=150)).isoformat(),'poll_seconds':61,'max_minutes':150,'collector_sha256':sha(source.read_bytes()),'release_sha256':sha(a.release.read_bytes()),'dispatch_receipt_sha256':sha(receipt_path.read_bytes()),'POSTs':0,'reruns':0,'cancellations':0,'scope':'CI_ONLY exact-head remote18+normal4+guardedbake1 with exact head/base/workflow/job/log bindings. Supplementary local stress failures remain documented separately. No final qualification, merge readiness or merge permission is supplied.'}
 save(out/'owner.json',state);save(lock/'owner.json',{'pid':os.getpid(),'output':str(out),'release':str(a.release),'started':state['started']})
 def api(label,endpoint,kind='json'):
  nonlocal counter
  need(time.monotonic()<deadline,'Observer150min deadline reached');counter+=1;stem=out/(f'{counter:04d}-'+label)
  try:
   result=subprocess.run(['gh','api','--method','GET','repos/'+REPO+'/'+endpoint],capture_output=True,timeout=min(45,max(1,deadline-time.monotonic())))
  except subprocess.TimeoutExpired as error:
   stem.with_suffix('.stdout').write_bytes(error.stdout or b'');stem.with_suffix('.stderr').write_bytes((error.stderr or b'')+b'\nGET process exceeded bounded timeout; no retry.\n')
   with (out/'GET-ATTEMPTS.jsonl').open('a') as f:f.write(json.dumps({'at':now(),'method':'GET','endpoint':endpoint,'timed_out':True,'stdout_file':stem.with_suffix('.stdout').name,'stderr_file':stem.with_suffix('.stderr').name})+'\n')
   raise
  stem.with_suffix('.stdout').write_bytes(result.stdout);stem.with_suffix('.stderr').write_bytes(result.stderr)
  record={'at':now(),'method':'GET','endpoint':endpoint,'returncode':result.returncode,'stdout_file':stem.with_suffix('.stdout').name,'stderr_file':stem.with_suffix('.stderr').name,'stdout_sha256':sha(result.stdout),'stderr_sha256':sha(result.stderr)}
  with (out/'GET-ATTEMPTS.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
  need(result.returncode==0,'GET failed; preserve output and stop, no automatic mutation/retry: '+label+' '+result.stderr.decode(errors='replace')[-1000:])
  if kind=='json':return json.loads(result.stdout)
  if kind=='text':return result.stdout.decode('utf8')
  return {'file':str(stem.with_suffix('.stdout')),'bytes':len(result.stdout),'sha256':sha(result.stdout)}
 def bind_pr():
  pull=api('PR1175','pulls/1175')
  need(pull['state']=='open' and pull['head']['sha']==head and pull['head']['ref']==BRANCH and pull['head']['repo']['full_name']==REPO and pull['base']['ref']=='dev' and pull['base']['sha']==base and pull['merge_commit_sha']==merge,'PR source/base/merge changed; qualification held')
  need(api('human-ref','git/ref/heads/'+BRANCH)['object']['sha']==head,'Human source ref moved')
  return {k:pull.get(k) for k in ['number','state','draft','mergeable','mergeable_state','updated_at']}
 def retain_failure(run,jobs):
  evidence={'run':run,'jobs':jobs,'job_logs':[],'retrieval_errors':[]}
  for job in jobs.get('jobs',[]):
   if job.get('status')!='completed' or job.get('conclusion')=='skipped':continue
   try:evidence['job_logs'].append({'job_id':job['id'],'log':api('failure-job-'+str(job['id']),'actions/jobs/'+str(job['id'])+'/logs','bytes')})
   except Exception as err:evidence['retrieval_errors'].append(str(err))
  try:evidence['artifacts']=api('failure-artifacts-'+str(run['id']),'actions/runs/'+str(run['id'])+'/artifacts?per_page=100')
  except Exception as err:evidence['retrieval_errors'].append(str(err))
  try:evidence['run_attempt1_logs']=api('failure-run-'+str(run['id'])+'-logs','actions/runs/'+str(run['id'])+'/attempts/1/logs','bytes')
  except Exception as err:evidence['retrieval_errors'].append(str(err))
  save(out/('FAILURE-'+str(run['id'])+'.json'),evidence)
 try:
  state['pr_state']=bind_pr()
  commit=api('source-commit','git/commits/'+head);need(commit['tree']['sha']==tree,'Actual remote source tree differs')
  merge_commit=api('PR-merge-commit','git/commits/'+merge);need([x['sha'] for x in merge_commit['parents']]==[base,head],'Actual PR merge parents differ from pinned base/head')
  for path,digest in {**d['pins'],**pins}.items():
   blob=d['git_blob_pins'][path] if path in d['git_blob_pins'] else None
   if blob is None:
    content=api('workflow-pin-'+str(counter),'contents/'+path+'?ref='+head)
   else:
    # Git blob API accepts the actual >1MiB smoke source, unlike Contents.
    content=api('source-pin-'+str(counter),'git/blobs/'+blob)
    need(content['sha']==blob,'Actual source Git blob pin differs: '+path)
   need(content.get('encoding')=='base64' and sha(base64.b64decode(content['content']))==digest,'Exact final source byte pin differs: '+path)
  for path in [SMOKE,*NORMAL,*({BAKE} if guarded_by_id else set())]:
   metadata=api('workflow-'+pathlib.Path(path).stem,'actions/workflows/'+pathlib.Path(path).name)
   need(metadata['path']==path and metadata['state']=='active','Actual workflow path not active');workflow_ids[path]=metadata['id']
   if path in NORMAL and any(x['path']==path and x['event']=='pull_request' for x in normal):
    content=api('merge-workflow-'+str(counter),'contents/'+path+'?ref='+merge)
    need(content.get('encoding')=='base64' and sha(base64.b64decode(content['content']))==pins[path],'PR checkout workflow bytes differ from pinned source')
  while time.monotonic()<deadline:
   tick=time.monotonic();listing=api('branch-runs','actions/runs?branch='+BRANCH.replace('/','%2F')+'&per_page=100')
   need(listing['total_count']==len(listing['workflow_runs']),'Incomplete complete-branch run inventory')
   head_runs=[r for r in listing['workflow_runs'] if r['head_sha']==head];byid={r['id']:r for r in head_runs};expected=selected|set(normal_by_id)|set(guarded_by_id)
   need(len(head_runs)==len(byid),'Duplicate exact-head IDs in complete branch inventory')
   need(expected<=set(byid),'A pinned actual selected/normal run is absent; no implicit redispatch')
   need(set(byid)==expected,'Unexpected exact-head runs; inspect before admitting duplicates or new scopes')
   current=[]
   for ident in sorted(expected):
    run=byid[ident];path=SMOKE if ident in selected else (guarded_by_id if ident in guarded_by_id else normal_by_id)[ident]['path'];event='workflow_dispatch' if ident in selected else (guarded_by_id if ident in guarded_by_id else normal_by_id)[ident]['event']
    need(run['head_sha']==head and run['head_branch']==BRANCH and run['run_attempt']==1 and run['event']==event and run['path']==path and run['workflow_id']==workflow_ids[path] and run['repository']['full_name']==REPO,'Run source/workflow/event/attempt identity changed')
    if event=='pull_request':
     matches=[x for x in run.get('pull_requests',[]) if x.get('number')==1175]
     need(len(matches)==1 and matches[0]['head']['sha']==head and matches[0]['base']['sha']==base and matches[0]['base']['ref']=='dev','Actual PR run base/head binding differs')
    current.append({k:run.get(k) for k in ['id','path','event','head_sha','run_attempt','status','conclusion','html_url']})
    if ident in audited or run['status']!='completed':continue
    jobs=api('jobs-'+str(ident),'actions/runs/'+str(ident)+'/attempts/1/jobs?per_page=100')
    if jobs['total_count']!=len(jobs['jobs']):
     retain_failure(run,jobs);raise ValueError('Incomplete attempt1 jobs')
    if run['conclusion']!='success':
     retain_failure(run,jobs);raise ValueError('Actual run failed: '+str(ident)+' '+str(run['conclusion']))
    try:
     if path=='.github/workflows/chicago-4d-humans.yml':job,proof=audit_human_jobs(jobs['jobs'],run,head)
     elif path==BAKE:job,proof=audit_guarded_bake_jobs(jobs['jobs'],run,head)
     else:
      need(len(jobs['jobs'])==1,'Unexpected selected job count');job=jobs['jobs'][0]
      name,steps=('smoke',SMOKE_STEPS) if ident in selected else NORMAL[path];proof=audit_job(job,run,head,name,steps)
     text=api('job-'+str(job['id'])+'-log','actions/jobs/'+str(job['id'])+'/logs','text')
     proof['actual_checkout_sha']=checkout_sha(text,merge if event=='pull_request' else head)
     if path==BAKE:proof.update(audit_guarded_bake_log(text))
     proof.update(workflow_path=path,event=event,job_log_sha256=sha(text.encode()),check_run_url=job['check_run_url'])
     if ident in selected:
      cell=smoke_cell(text);need(cell not in bound,'Two actual runs claim one viewport/stage');bound[cell]=ident;proof.update(viewport=cell[0],stage=cell[1],**audit_population_boot(text,cell[0]))
    except Exception:
     retain_failure(run,jobs);raise
    audited[ident]=proof;save(out/'audited-jobs.json',list(audited.values()))
   state.update(at=now(),pr_state=bind_pr(),runs=current,selected_strict_success=len(selected.intersection(audited)),normal_strict_success=len(set(normal_by_id).intersection(audited)),guarded_bake_strict_success=len(set(guarded_by_id).intersection(audited)),bound_cells=[{'viewport':v,'stage':s,'run_id':ident} for (v,s),ident in sorted(bound.items())],api_requests=counter)
   save(out/'latest.json',state)
   summary=(state['selected_strict_success'],state['normal_strict_success'],tuple((r['id'],r['status'],r['conclusion']) for r in current))
   if summary!=last:
    with (out/'transitions.jsonl').open('a') as f:f.write(json.dumps(state)+'\n')
    print(json.dumps({'at':state['at'],'selected':state['selected_strict_success'],'normal':state['normal_strict_success'],'deadline':state['deadline_utc']}),flush=True);last=summary
   if set(audited)==expected:
    need(set(bound)==cells,'Incomplete actual log-bound18 grid')
    state['final_check_runs']=api('final-check-runs','commits/'+head+'/check-runs?per_page=100')
    state['final_statuses']=api('final-statuses','commits/'+head+'/status')
    need(state['final_check_runs']['total_count']==len(state['final_check_runs']['check_runs']),'Incomplete final check-run inventory')
    checks={c['url']:c for c in state['final_check_runs']['check_runs']}
    for proof in audited.values():
     check=checks.get(proof['check_run_url']);need(check is not None and check['head_sha']==head and check['status']=='completed' and check['conclusion']=='success' and check['name']==proof['job_name'],'Final check-run/job binding differs')
    need(audit_ci_only_scope(release,head,baseline)==focused_proof,'Pinned CI_ONLY canonical/local evidence changed during remote collection')
    state.update(status='CI_ONLY_ACTUAL_23_QUALIFIED',ci_only_pass=True,qualification_pass=False,ready_for_root_fresh_merge_review=False);break
   remaining=min(61-(time.monotonic()-tick),deadline-time.monotonic())
   # Never block the steward for >60s; cadence remains at least61s.
   while remaining>0:
    delay=min(remaining,30);time.sleep(delay);remaining-=delay
  need(state['ci_only_pass'],'Observer150min deadline without complete remote23 proof; no cancel/rerun')
 except Exception as error:state.update(status='STOPPED_WITH_EVIDENCE',error=str(error))
 finally:
  state.update(ended=now(),elapsed_seconds=time.monotonic()-started,api_requests=counter,selected_strict_success=len(selected.intersection(audited)),normal_strict_success=len(set(normal_by_id).intersection(audited)),guarded_bake_strict_success=len(set(guarded_by_id).intersection(audited)))
  save(out/'latest.json',state);save(out/'terminal.json',state)
  print(json.dumps({'output':str(out),'status':state['status'],'qualification_pass':state['qualification_pass'],'selected':state['selected_strict_success'],'normal':state['normal_strict_success'],'error':state.get('error')}),flush=True)
 return 0 if state['ci_only_pass'] else 1
if __name__=='__main__':raise SystemExit(main())
