#!/usr/bin/env python3
"""Exact-head18-cell dispatch, or GET-only reconciliation. Default is a dry plan."""
import argparse,datetime,hashlib,json,pathlib,re,subprocess,time
REPO='kevinrhaas/chicago'; BRANCH='steward/1835-workwear-repair-20261021'
ROOT=pathlib.Path('/workspace/chicago'); SHARED=pathlib.Path('/workspace/shared')
WORKFLOW='chicago-4d-smoke.yml'; RANGES=['1-2','3-4','5','6-7','8','9-12','13','14','15']
def need(c,m):
 if not c:raise ValueError(m)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],env={**__import__('os').environ,'GIT_OPTIONAL_LOCKS':'0'})
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--activation',type=pathlib.Path);p.add_argument('--sha');p.add_argument('--pr',type=int);p.add_argument('--execute',action='store_true');p.add_argument('--reconcile',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path);a=p.parse_args()
 need(not(a.execute and a.reconcile),'Execution and reconciliation are separate operations')
 original=json.loads(a.reconcile.read_text())if a.reconcile else None
 head=a.sha or (original['sha']if original else None);pr=a.pr or (original['pr']if original else None)
 need(head is not None and re.fullmatch('[0-9a-f]{40}',head),'Supply a full immutable --sha');need(pr==1175,'This finite dispatcher is only PR1175')
 tree=git('rev-parse',head+'^{tree}').decode().strip()
 source=git('show',head+':.github/workflows/chicago-4d-bake.yml').decode()
 stage=re.search(r'^\s+stage:\s*\[([^\]]+)\]',source,re.M);need(stage is not None,'Nightly grid absent');ranges=[x.strip().strip("'\"")for x in stage[1].split(',')];need(ranges==RANGES,'Current nightly grid changed; inspect before dispatch')
 smoke=git('show',head+':.github/workflows/'+WORKFLOW).decode();need('SMOKE_VIEWPORT: ${{ inputs.viewport }}'in smoke and 'SMOKE_STAGE: ${{ inputs.stage }}'in smoke and 'run: node tools/smoke_renderer.mjs --published'in smoke,'Manual workflow input/published contract changed')
 cells=[(v,s)for v in ['desktop','mobile']for s in RANGES];priority=[('desktop','13'),('desktop','14'),('desktop','1-2'),('mobile','14'),('mobile','1-2')];cells=priority+[c for c in cells if c not in priority]
 for viewport in ['desktop','mobile']:
  covered=[n for v,s in cells if v==viewport for n in (list(range(int(s.split('-')[0]),int(s.split('-')[-1])+1)))];need(sorted(covered)==list(range(1,16)),'Coverage is not exact1..15')
 pin_paths=['.github/workflows/'+WORKFLOW,'.github/workflows/chicago-4d-bake.yml','chicago/4d/tools/smoke_renderer.mjs','chicago/4d/tools/smoke_budget.mjs','chicago/4d/tools/human_contract.py','chicago/4d/renderers/web/js/main.js','chicago/4d/renderers/web/js/humans.js','chicago/4d/renderers/web/js/human-identity.js','chicago/4d/data/scenes/1835.json','chicago/4d/data/humans/instances/1835/index.json','chicago/4d/data/humans/instances/1835/hi_rc_bardwell_otis_1835.json']
 pins={path:sha(git('show',head+':'+path))for path in pin_paths}
 blob_pins={path:git('rev-parse',head+':'+path).decode().strip() for path in pin_paths}
 baseline_bytes=(pathlib.Path(__file__).parent/'CANONICAL-BARDWELL-BASELINE.json').read_bytes();baseline=json.loads(baseline_bytes)
 need(pins['chicago/4d/data/humans/instances/1835/hi_rc_bardwell_otis_1835.json']==baseline['instance_sha256'],'Reviewed actual standing instance changed')
 for lod in baseline['web_lods']:
  need(sha(git('show',head+':chicago/4d/assets/humans/web/'+lod['filename']))==lod['sha256'],'Final source no longer imports exact qualified canonical web bytes')
 plan={'repository':REPO,'branch':BRANCH,'sha':head,'tree':tree,'pr':pr,'workflow':WORKFLOW,'canonical_baseline_sha256':sha(baseline_bytes),'focused_town_required_before_merge':True,'cells':cells,'pins':pins,'git_blob_pins':blob_pins,'prepared_workflow_identity_pins':json.loads((pathlib.Path(__file__).parent/'PREPARED-WORKFLOW-PINS.json').read_bytes())['pins'],'scope':'Exactly18 fresh final-standing-head published smoke requests may run concurrently with local final-town phases. Root independently reviews repository-required CI and actual published desktop/mobile evidence; automatic gate/report/humans plus moving proof are collected separately. Private supplemental focused-case flags remain false and are not a CI_ONLY gate. No unfiltered duplicate, canonical human rebuild, bake or production promotion.'}

 if a.execute:
  need(a.activation is not None,'HELD: explicit root activation required before POST')
  release=json.loads(a.activation.read_bytes());need(release.get('status')=='ROOT_RELEASED_HUMAN1175_EXACT_HEAD_SMOKE_DISPATCH' and release.get('released') is True and release.get('allow_dispatch') is True and release.get('sha')==head and release.get('repository')==REPO and release.get('branch')==BRANCH and release.get('pr')==pr,'Root activation identity/authorization mismatch')
  need(head not in ['34cf462ed343b8b2b70da70303344fff7e5e083f','2f75ef23dbb316ebe4cf53e65ce3af8b04f140d3'],'Old canonical source cannot qualify the new standing scene')
  need(release.get('committed_pushed') is True and release.get('full_preflight_PASS') is True,'Commit/push/full preflight not released')
  need(release.get('tree')==tree,'Exact final tree not released')
  need(release.get('focused_town_required_before_merge') is True and type(release.get('focused_published_desktop_mobile_PASS')) is bool,'Focused town evidence remains mandatory before merge; record its actual current boolean')
  need(release.get('canonical_baseline_sha256')==sha(baseline_bytes),'Actual qualified canonical baseline identity differs')
  need(git('rev-parse','HEAD').decode().strip()==head and not git('diff','--name-only') and not git('diff','--cached','--name-only'),'Root final source must be exact committed clean HEAD')
  need(release.get('dispatcher_sha256')==sha(pathlib.Path(__file__).read_bytes()),'Root release dispatcher identity mismatch')
  expected=json.loads((pathlib.Path(__file__).parent/'PREPARED-WORKFLOW-PINS.json').read_bytes())['pins']
  need(all(sha(git('show',head+':'+path))==digest for path,digest in expected.items()),'Current workflow changed from prepared identity; inspect/reprepare')
  price_path=pathlib.Path(release['final_diff_pricing']);price_bytes=price_path.read_bytes();price=json.loads(price_bytes)
  need(release.get('final_diff_pricing_sha256')==sha(price_bytes) and price.get('sha')==head and price.get('tree')==tree and price.get('expected_normal_contract') is True and price.get('selected_manual_requests')==18,'Final exact-head independent pricing missing/mismatch')
 if not a.execute and not a.reconcile:print(json.dumps({'execute':False,**plan},indent=2));return 0
 need(a.output is not None and a.output.resolve().is_relative_to(SHARED),'Fresh --output under /workspace/shared required');a.output.mkdir(exist_ok=False)
 record={**plan,'started':now(),'caller_sha256':sha(pathlib.Path(__file__).read_bytes()),'lane_identity':'human-standing-1175-nexthead-v1','activation':str(a.activation) if a.activation else None,'activation_sha256':sha(a.activation.read_bytes()) if a.activation else None,'dispatches':[],'discovered_runs':[],'operation':'reconcile-GET-only'if original else'dispatch-once','no_retry':True};deadline=time.monotonic()+180;number=0
 def checkpoint():save(a.output/'receipt.json',record)
 def api(label,endpoint,body=None):
  nonlocal number
  remaining=deadline-time.monotonic();need(remaining>0,'180s operation deadline; no further request');number+=1;stem=a.output/(f'{number:03d}-'+label);method='GET'if body is None else'POST';save(stem.with_suffix('.request.json'),{'at':now(),'method':method,'endpoint':endpoint,'body':body})
  cmd=['gh','api','--method',method,'repos/'+REPO+'/'+endpoint]
  if body is not None:cmd+=['--input','-']
  r=subprocess.run(cmd,input=json.dumps(body)if body is not None else None,text=True,capture_output=True,timeout=min(45,remaining));stem.with_suffix('.stdout').write_text(r.stdout);stem.with_suffix('.stderr').write_text(r.stderr);need(r.returncode==0,label+' API failure/ambiguity; do not retry POST');return json.loads(r.stdout)if r.stdout.strip()else None
 def remote():return api('branch','git/ref/heads/'+BRANCH)['object']['sha']
 listing='actions/runs?branch='+BRANCH.replace('/','%2F')+'&per_page=100'
 try:
  need(remote()==head,'Remote branch differs from qualified head');commit=api('commit','git/commits/'+head);need(commit['tree']['sha']==tree,'Remote tree differs');pull=api('pr','pulls/'+str(pr));need(pull['state']=='open'and pull['head']['sha']==head and pull['head']['ref']==BRANCH and pull['head']['repo']['full_name']==REPO and pull['base']['ref']=='dev','PR route/head changed')
  record['PR_source_binding']={k:pull[k] for k in ['head','base','merge_commit_sha']}
  if a.execute:need(pull['base']['sha']==release.get('base_sha') and pull['merge_commit_sha']==release.get('merge_sha'),'Pinned PR base/merge differs before POST')
  if original:
   need(original['repository']==REPO and original['branch']==BRANCH and original['sha']==head and original['tree']==tree and original['pr']==pr and original['pins']==pins,'Original receipt identity/pins differ');need(original['caller_sha256']==record['caller_sha256'],'Caller source differs from original receipt');need(len(original['dispatches'])==18 and all(d.get('post_succeeded')for d in original['dispatches']),'Not18 accepted original POSTs; inspect ambiguity manually');record['original_receipt']={'path':str(a.reconcile),'sha256':sha(a.reconcile.read_bytes()),'original_error':original.get('error')};record['dispatches']=original['dispatches']
  else:
   before=api('runs-before',listing);need(before['total_count']==len(before['workflow_runs']),'Incomplete branch run inventory before POST');before_head=[r for r in before['workflow_runs'] if r['head_sha']==head and r['path']=='.github/workflows/'+WORKFLOW];need(not before_head,'Selected workflow runs already exist; inspect before duplicating');record['before_run_ids']=[];record['branch_inventory_before_total']=before['total_count']
   (SHARED/('human-standing-1175-nexthead-'+head+'.POST.lock')).mkdir(exist_ok=False)
   for viewport,stage in cells:
    need(remote()==head,'Branch drift before POST; reconcile accepted work, never automatically redispatch');d={'viewport':viewport,'stage':stage,'requested':now(),'post_attempted':True,'post_succeeded':False};record['dispatches'].append(d);checkpoint();api('dispatch','actions/workflows/'+WORKFLOW+'/dispatches',{'ref':BRANCH,'inputs':{'viewport':viewport,'stage':stage}});d['post_succeeded']=True;checkpoint()
   if deadline-time.monotonic()>2:time.sleep(2)
  runs=api('runs-after',listing);need(runs['total_count']==len(runs['workflow_runs']),'Incomplete branch run inventory after POST');head_runs=[r for r in runs['workflow_runs'] if r['head_sha']==head and r['path']=='.github/workflows/'+WORKFLOW];record['branch_inventory_after_total']=runs['total_count'];record['run_inventory_method']='Complete branch listing filtered by exact per-run head SHA and smoke workflow path';record['discovered_runs']=[{k:r.get(k)for k in ['id','head_sha','head_branch','event','path','run_attempt','status','conclusion','created_at','html_url']}for r in head_runs];checkpoint()
  need(len(head_runs)==len(record['discovered_runs'])==18,'Discovery incomplete/extra; preserve this receipt and reconcile GET-only without new POSTs');need(len({r['id']for r in record['discovered_runs']})==18,'Duplicate run IDs')
  for r in record['discovered_runs']:need(r['head_sha']==head and r['head_branch']==BRANCH and r['event']=='workflow_dispatch'and r['path']=='.github/workflows/'+WORKFLOW and r['run_attempt']==1,'Discovered workflow identity changed')
  need(remote()==head,'Branch changed after requests');final_pull=api('final-pr','pulls/'+str(pr));need(final_pull['base']['sha']==record['PR_source_binding']['base']['sha'] and final_pull['merge_commit_sha']==record['PR_source_binding']['merge_commit_sha'],'PR base/merge moved during requests');record['dispatch_complete']=True
 except Exception as error:record['error']=str(error)
 finally:record['ended']=now();record['api_requests']=number;checkpoint();print(json.dumps({'receipt':str(a.output/'receipt.json'),'sha':head,'complete':record.get('dispatch_complete',False),'accepted_posts':sum(bool(d['post_succeeded'])for d in record['dispatches']),'error':record.get('error')},indent=2))
 return 0 if record.get('dispatch_complete')and not record.get('error')else 1
if __name__=='__main__':raise SystemExit(main())
