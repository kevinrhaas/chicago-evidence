#!/usr/bin/env python3
"""Read-only normal CI gate audit. Never proves stdout union, artifacts or photographs.
No request occurs without --verify. Requires PyYAML; only normal configured gh api GET.
"""
import argparse,base64,concurrent.futures,hashlib,json,pathlib,re,subprocess,sys,time,datetime
import yaml
SHA='668e48180cfa20fe48b594041fcc0c0e2499ee72'
REPO='kevinrhaas/chicago'; BRANCH='steward/period-transport-2793'
GRID={(v,s) for v in ('desktop','mobile') for s in ('1-2','3-4','5','6-7','8','9-12','13','14','15')}
ROOT=pathlib.Path('/workspace/chicago'); SHARED=pathlib.Path('/workspace/shared')
SMOKE='.github/workflows/chicago-4d-smoke.yml'; HUMAN='.github/workflows/chicago-4d-humans.yml'
PINS={'.github/workflows/chicago-4d-smoke.yml': 'b2d6ae3c355e3604a807053088367f3e3ecda4e2d2bc63ca6bc15150848e4fde', '.github/workflows/chicago-4d-humans.yml': '4812e73e20c1e7601eb61fa7df7eafa347816f808917cb201dbaeea570c02d1b', 'chicago/4d/tools/smoke_renderer.mjs': '2b435da932f77e6dddcc93ec61917c21588ee24731df6050b56230827b48356f', 'chicago/4d/tools/human_fixture.mjs': '48c1666963013db003dd78dd9435541ac2d8a68cbbfcebb0d5b38a14295f3473', 'chicago/4d/tools/human_actor.mjs': '50e03ed95eb0b6c81879d1584a5ca0ef03b41a261d2abc3628bd4a1cddb5dad0', 'chicago/4d/tools/human_teamster.mjs': '5eb6f2c7d6379145444062fc74a90aaf02d7ac08d234edcdc93772361cf5c81a', 'chicago/4d/tools/human_export.sh': '7958fa031316794db38bd1f3e181583767a642ca513473b03243acb39c171946', 'chicago/4d/renderers/web/js/flora.js': 'bb9582d094a502b1ea82b9a0cf2de3d1eebed02157b71b80bb55160617b989dd'}
BLOB_IDS={'.github/workflows/chicago-4d-smoke.yml': '43fdc6205607ff38d4ae768c2df608099b81d1e1', '.github/workflows/chicago-4d-humans.yml': '7ace02ed784ca1b3c02e28ff20788cb4dea3716c', 'chicago/4d/tools/smoke_renderer.mjs': '1a388c6e79dec079b2e0fbcc12218a4228bf9d7d', 'chicago/4d/tools/human_fixture.mjs': '1d65b03e80f8ba00164bfe929049b7347d0cc752', 'chicago/4d/tools/human_actor.mjs': '845d1bd7c77d3749b59fd0cd9ea10c6e5f6b175b', 'chicago/4d/tools/human_teamster.mjs': 'e9b1440d8d91ee3f64d675a48456c1fb6579ae9e', 'chicago/4d/tools/human_export.sh': 'dfa830cac6d9651b496d1763f8198be3391f784d', 'chicago/4d/renderers/web/js/flora.js': '30ccb239bdc3c29fb805a702f8dec18df44ea960'}
HUMAN_STEPS=['Rebuild the fixture and require the committed bytes','Open every human GLB in the browser, at both viewports','Drive the browser actor with the fixture, at both viewports']
TEAM_STEPS=['Verify the original body preparation','Build three canonical masters and export through the portable path','Build same-new-master parented hierarchy controls (test artifacts only)','Audit declared resident animation time bounds before browser loading','Check actual resident hair material, embedded PNG and source/web LOD dimensions','Validate the actual new GLB containers','Validate hierarchy control warnings with exact node pointers','Measure all human exports and inspect the workwear studies']
SMOKE_STEPS=['Publish the mirror the smoke serves (site/4d/ is generated)','Run the smoke against the published mirror']
def need(ok,msg):
 if not ok: raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def committed(path):return subprocess.check_output(['git','-C',str(ROOT),'show',SHA+':'+path])
def success(x,label):need(x.get('status')=='completed' and x.get('conclusion')=='success',label+' not completed SUCCESS')
def run_ok(x,path):
 need(x.get('head_sha')==SHA and x.get('head_branch')==BRANCH and x.get('event')=='workflow_dispatch' and x.get('path')==path and x.get('run_attempt')==1,'wrong run identity/attempt')
 success(x,'workflow '+str(x.get('id')))
def jobs_ok(jobs,rid,names):
 need(len({j['id'] for j in jobs})==len(jobs),'duplicate job IDs')
 for name,steps in names.items():
  js=[j for j in jobs if j.get('name')==name];need(len(js)==1,'missing/duplicate mandatory job '+name);j=js[0]
  need(j.get('run_id')==rid and j.get('head_sha')==SHA and j.get('run_attempt')==1,'wrong job identity');success(j,name)
  for step in steps:
   ss=[s for s in j.get('steps',[]) if s.get('name')==step];need(len(ss)==1,'missing/duplicate test step '+step);success(ss[0],step)
  # All non-post steps must finish SUCCESS; upload's always() is not a test substitute.
  for s in j.get('steps',[]):
   if s.get('name','').startswith('Post ') and s.get('status')=='completed' and s.get('conclusion')=='skipped':continue
   success(s,name+'/'+s.get('name','?'))
def source_ok(raw):
 for path,b in raw.items():need(digest(b)==PINS[path],'frozen source pin mismatch '+path)
 for path,job_names in [(SMOKE,{'smoke':SMOKE_STEPS}),(HUMAN,{'humans':HUMAN_STEPS,'teamster-studies':TEAM_STEPS})]:
  text=raw[path].decode();doc=yaml.safe_load(text)
  need('continue-on-error' not in text,'continue-on-error forbidden')
  for name,required in job_names.items():
   job=doc['jobs'][name];need('if' not in job or (path==HUMAN and name=='teamster-studies' and job['if']=="github.event_name == 'workflow_dispatch' && inputs.build_teamsters"),'conditional mandatory job')
   need(job.get('runs-on')=='ubuntu-latest','unexpected runner')
   need(job.get('timeout-minutes',0)>0,'missing job timeout')
   steps=job['steps'];checkout=[s for s in steps if str(s.get('uses','')).startswith('actions/checkout@')]
   need(len(checkout)==1 and not checkout[0].get('with',{}).get('ref'),'checkout ref override')
   for name2 in required:
    matches=[s for s in steps if s.get('name')==name2];need(len(matches)==1,'source mandatory step absent '+name2);s=matches[0]
    need('if' not in s and 'run' in s and s.get('working-directory')=='chicago/4d','conditional/nonrun/wrongdirectory mandatory step')
    code=s['run'];need(not re.search(r'\|\|\s*(?:true|:|echo)|set\s+\+e|exit\s+0\b',code),'shell swallows failure')
    need(s.get('shell') in (None,'bash') and not job.get('defaults'),'unexpected shell/defaults; default ubuntu bash -e is required')
    if '| tee ' in code:need('pipefail' in code,'pipeline lacks pipefail')
  if path==SMOKE:
   s=next(x for x in doc['jobs']['smoke']['steps'] if x.get('name')==SMOKE_STEPS[1]);need(s['run']=='node tools/smoke_renderer.mjs --published','not actual published smoke')
   need(s.get('env')=={'SMOKE_VIEWPORT':'${{ inputs.viewport }}','SMOKE_STAGE':'${{ inputs.stage }}'},'dispatch input wiring changed')
  else:
   code=next(x for x in doc['jobs']['teamster-studies']['steps'] if x.get('name')==TEAM_STEPS[-1])['run']
   for fragment in ['bash tools/publish.sh','tools/human_teamster.mjs --published --sole-contact','tools/human_teamster.mjs --masters --sole-contact','tools/test_human_inspection.mjs']:need(fragment in code,'inspection command missing '+fragment)
   need('process.exitCode = 1' in text,'container validation failure not propagated')
 smoke=raw['chicago/4d/tools/smoke_renderer.mjs'].decode();need('process.exit(1)' in smoke and "console.log('SMOKE PASS')" in smoke,'smoke failure propagation absent')
 need('const PARTS = 15' in smoke,'unexpected stage topology')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify',action='store_true');ap.add_argument('--out',required=True);ap.add_argument('--dispatch',default=str(SHARED/'transport-smoke-dispatch-c02-668e48180.json'));ap.add_argument('--canonical',default=str(SHARED/'human-probe-dispatch-668e48180.json'));ap.add_argument('--terminal-jobs',default=str(SHARED/'final-668e-metadata/terminal-jobs.json'));args=ap.parse_args()
 if not args.verify:print(json.dumps({'execute':False,'sha':SHA,'source_pins':PINS,'source_blob_ids':BLOB_IDS,'network':'GET JSON only; total45second audit deadline; no retries/logs/artifacts','out':args.out},indent=2));return 0
 out=pathlib.Path(args.out);need(out.is_absolute() and str(out).startswith('/workspace/shared/'),'outside shared output required');out.mkdir(exist_ok=False)
 report={'sha':SHA,'source_blob_ids':BLOB_IDS,'standard_ci_gate_passed':False,'coverage_proof_passed':False,'strict_log_union':'UNPROVEN','artifacts':'UNINSPECTED','photographic_acceptance':'UNACCEPTED','errors':[],'scope':'Normal CI metadata gate only; no ready/merge action or stdout-equivalence claim'}
 try:
  need(subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()==SHA,'local HEAD differs')
  raw={p:committed(p) for p in PINS};source_ok(raw)
  dispatch=load(args.dispatch);can=load(args.canonical);saved=load(args.terminal_jobs)
  for d in [dispatch,can]:need(d['repository']==REPO and d['branch']==BRANCH and d['sha']==SHA and d['remote_head_after']==SHA,'dispatch frozen identity mismatch')
  ds=dispatch['dispatches'];need(len(ds)==18 and {(x['viewport'],x['stage']) for x in ds}==GRID and all(x['post_succeeded'] is True for x in ds),'not exact18 successful grid POSTs')
  ids={x['id'] for x in dispatch['discovered_runs']};need(len(ids)==18 and all(x['head_sha']==SHA and x['run_attempt']==1 for x in dispatch['discovered_runs']),'wrong18 discovered runs')
  need(can['post_succeeded'] is True and can['inputs']=={'build_teamsters':True} and len(can['runs'])==1,'canonical dispatch not true/single')
  cid=can['runs'][0]['id'];need(cid not in ids and can['runs'][0]['head_sha']==SHA,'canonical run identity')
  deadline=time.monotonic()+45
  def get(endpoint):
   remaining=deadline-time.monotonic();need(remaining>0,'45s metadata deadline exceeded')
   result=subprocess.run(['gh','api','--method','GET','repos/'+REPO+'/'+endpoint],capture_output=True,text=True,timeout=remaining)
   need(result.returncode==0,'normal GitHub GET failed '+endpoint+' (no retry)')
   data=json.loads(result.stdout);return data
  queries={'smoke_runs':'actions/workflows/chicago-4d-smoke.yml/runs?head_sha='+SHA+'&event=workflow_dispatch&per_page=100','canonical_run':'actions/runs/'+str(cid),'canonical_jobs':'actions/runs/'+str(cid)+'/jobs?filter=latest&per_page=100','checks':'commits/'+SHA+'/check-runs?per_page=100','statuses':'commits/'+SHA+'/status?per_page=100','pr':'pulls/1041','dev_ref':'git/ref/heads/dev'}
  queries.update({'source_'+str(i):'git/blobs/'+BLOB_IDS[p] for i,p in enumerate(PINS)})
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
   futures={pool.submit(get,e):k for k,e in queries.items()};results={}
   for f in concurrent.futures.as_completed(futures):
    key=futures[f];results[key]=f.result();(out/(key+'.json')).write_text(json.dumps(results[key],indent=2)+'\n')
  for i,p in enumerate(PINS):
   blob=results['source_'+str(i)];need(blob.get('sha')==BLOB_IDS[p] and blob.get('encoding')=='base64','remote code blob identity/encoding mismatch '+p)
   data=base64.b64decode(blob['content']);need(digest(data)==PINS[p] and data==raw[p],'remote frozen source differs '+p)
   need(subprocess.check_output(['git','-C',str(ROOT),'rev-parse',SHA+':'+p],text=True).strip()==BLOB_IDS[p],'local committed blob identity mismatch '+p)
  runs=results['smoke_runs'];need(runs['total_count']==18 and len(runs['workflow_runs'])==18 and {r['id'] for r in runs['workflow_runs']}==ids,'remote dispatch run set differs: extras/missing')
  for r in runs['workflow_runs']:
   run_ok(r,SMOKE);record=saved.get(str(r['id']));need(record is not None,'missing terminal job evidence');need(record['attempt']==1 and record['head_sha']==SHA,'wrong saved job record');jobs_ok(record['jobs'],r['id'],{'smoke':SMOKE_STEPS})
  run_ok(results['canonical_run'],HUMAN);cj=results['canonical_jobs'];need(cj['total_count']==len(cj['jobs']),'truncated canonical jobs');jobs_ok(cj['jobs'],cid,{'humans':HUMAN_STEPS,'teamster-studies':TEAM_STEPS})
  checks=results['checks'];need(checks['total_count']==len(checks['check_runs']),'truncated check list')
  for c in checks['check_runs']:
   need(c.get('head_sha')==SHA and c.get('status')=='completed','wronghead/pending check')
   need(c.get('conclusion')=='success' or (c['name']=='teamster-studies' and c.get('conclusion')=='skipped'),'non-success check '+c['name'])
  for n in ['gate','moving-frames','humans','report']:need(any(c['name']==n and c['conclusion']=='success' for c in checks['check_runs']),'mandatory check absent '+n)
  statuses=results['statuses'];need(statuses['total_count']==len(statuses['statuses']),'truncated statuses');need(all(s['state']=='success' for s in statuses['statuses']),'non-success legacy status')
  pr=results['pr'];need(pr['base']['sha']==results['dev_ref']['object']['sha'],'PR base metadata stale relative to actualdev');need(pr['state']=='open' and pr['head']['sha']==SHA and pr['head']['repo']['full_name']==REPO and pr['head']['ref']==BRANCH and pr['base']['ref']=='dev' and pr['mergeable'] is True and pr['mergeable_state']=='clean','PR not exacthead/open/dev/clean/mergeable')
  report.update(standard_ci_gate_passed=True,smoke_workflows_success=18,canonical_workflows_success=1,pr_draft=pr['draft'],input_pairing='Individual run-to-input pairing not inferred; successful dispatchset and exact remote runset independently reconciled',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:report['errors'].append(str(e))
 (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if report['standard_ci_gate_passed'] else 1
if __name__=='__main__':sys.exit(main())
