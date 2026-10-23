#!/usr/bin/env python3
"""Read-only exact-f2f18smoke+5normal CI gate; no request without --verify. Never marks ready or merges."""
import argparse,base64,concurrent.futures,datetime,hashlib,importlib.util,json,pathlib,subprocess,time,sys
S=pathlib.Path('/workspace/shared');R=pathlib.Path('/workspace/chicago');SHA='f2f607b0b6a82e9973c260d55c57fc4b661fb0b4';TREE='955d48d151c6a00e87a5d636f07a0dfcf5de505a';REPO='kevinrhaas/chicago';BRANCH='steward/period-transport-2793'
HELPER=S/'verify_normal_dev_gates_v8_aedc80126.py';HELPER_SHA='87ad8568b3e4704a125122160f68d6686b5a7f51facdb71a8e50aca8cbc0b5e9';OBSERVER=S/'watch_f2f607b0_exact18_and_normal_V2.py';OBSERVER_SHA='e7f1abaab03930dc9e6560b2b575b9a1adff594c68737d5b515a7bd5e5400d35'
AUX_RUN=39309713612;AUX_IDS={'warranted':118255833840,'bake':118257500408,'smoke':118257500707,'publish-bundle':118257504593,'open-pr':118257504792,'fresh-consumer':118257505925};HUMAN_RUN=39309722006;TEAM_SKIP=118258083403
NORMAL={'gate':(39309722010,['Run the gate','Does this change carry a changelog entry?']),'moving-frames':(39309721950,['Publish the mirror the gate serves (site/4d/ is generated)','Walk, turn, fly and ride; hold the flora frame to its ceilings','A phone keeps the town on the GPU, not twice']),'report':(39309713514,['Check the secret before doing anything','Report every pull request nothing can move'])}
def need(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads(pathlib.Path(p).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def module(name,p,sha):
 need(digest(p.read_bytes())==sha,'Reviewed helper changed '+str(p));sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
def configure():
 v=module('strict_source_contract',HELPER,HELPER_SHA);v.SHA=SHA;v.PINNED_TREE=TREE;v.AUX_RUN=AUX_RUN;v.AUX_ATTEMPT=1;v.AUX_HEAD=SHA;v.AUX_IDS=AUX_IDS.copy();return v
def optional_skip_check(c):return c.get('id')==TEAM_SKIP and c.get('name')=='teamster-studies'and c.get('head_sha')==SHA and c.get('status')=='completed'and c.get('conclusion')=='skipped'and c.get('html_url')==f'https://github.com/{REPO}/actions/runs/{HUMAN_RUN}/job/{TEAM_SKIP}'
def run_ok(run,rid,spec):
 need(run['id']==rid and run['head_sha']==SHA and run['head_branch']==BRANCH and run['path']==spec['path']and run['event']==spec['event']and run['run_attempt']==1,'Fresh run identity/attempt changed '+str(rid));need(run['status']=='completed'and run['conclusion']=='success','Workflow not completed SUCCESS '+str(rid))
def records_ok(v,saved,runs,expected):
 need(set(saved)=={str(k)for k in expected},'Exactly23 saved terminal job records required');jobids=set();auxiliary=None
 for rid,spec in expected.items():
  run=runs[rid];run_ok(run,rid,spec);record=saved[str(rid)];need(record['run_id']==rid and record['attempt']==1 and record['head_sha']==SHA,'Saved terminal record identity changed');jobs=record['jobs'];need(jobs and len({j['id']for j in jobs})==len(jobs),'Missing/duplicate job IDs')
  for j in jobs:
   need(j['id']not in jobids and j['run_id']==rid and j['run_attempt']==1 and j['head_sha']==SHA and j['check_run_url'].endswith('/check-runs/'+str(j['id']))and j['html_url']==f"https://github.com/{REPO}/actions/runs/{rid}/job/{j['id']}",'Job/check binding changed');jobids.add(j['id'])
  if spec['selected_smoke']:
   need(len(jobs)==1,'Selected smoke job count changed');v.jobs_ok(jobs,rid,{'smoke':v.SMOKE_STEPS})
  elif rid==AUX_RUN:auxiliary=v.auxiliary_jobs_ok(run,{'total_count':len(jobs),'jobs':jobs})
  elif rid==HUMAN_RUN:
   need(len(jobs)==2 and {j['name']for j in jobs}=={'humans','teamster-studies'},'Normal human jobset changed');v.jobs_ok(jobs,rid,{'humans':v.HUMAN_STEPS});skip=next(j for j in jobs if j['name']=='teamster-studies');need(skip['id']==TEAM_SKIP and skip['status']=='completed'and skip['conclusion']=='skipped'and not skip['steps'],'Normal PR optional-teamster skip changed')
  else:
   hit=[(name,steps)for name,(known,steps)in NORMAL.items()if known==rid];need(len(hit)==1 and len(jobs)==1,'Unknown normal workflow/job count');name,steps=hit[0];v.jobs_ok(jobs,rid,{name:steps})
 need(auxiliary is not None,'Actual auxiliary DAG audit absent');return jobids,auxiliary
def checks_ok(v,data,jobids):
 need(data['total_count']==len(data['check_runs'])==len(jobids)and {c['id']for c in data['check_runs']}==jobids,'Current checkset missing/extra/truncated relative to all23 actual jobs')
 for c in data['check_runs']:
  need(c.get('head_sha')==SHA and c.get('status')=='completed','Wrong-head/pending check')
  need(c.get('conclusion')=='success'or v.auxiliary_skip_check(c)or optional_skip_check(c),'Non-success/unbound check '+c['name'])
 for name in ['gate','moving-frames','humans','report']:need(any(c['name']==name and c['conclusion']=='success'for c in data['check_runs']),'Mandatory normal check missing '+name)
def normal_source_contracts(v,manifest):
 # The entire committed tree is pinned and compared remotely; read these contracts from f2f objects, never current checkout.
 reports=[]
 for name,(rid,steps)in NORMAL.items():
  spec=next(x for x in manifest['known_normal_runs']if x['id']==rid);raw=git('show',SHA+':'+spec['path']);doc=v.yaml.safe_load(raw);job=doc['jobs'][name];need('continue-on-error'not in raw.decode(),'Normal workflow swallows failures');need('if'not in job,'Conditional mandatory normal job');checkouts=[s for s in job['steps']if str(s.get('uses','')).startswith('actions/checkout@')];need(len(checkouts)==1 and not checkouts[0].get('with',{}).get('ref'),'Normal checkout ref overridden')
  for step in steps:
   found=[s for s in job['steps']if s.get('name')==step];need(len(found)==1 and 'run'in found[0],'Required normal source step missing');need('if'not in found[0]or(name=='gate'and step=='Does this change carry a changelog entry?'and found[0]['if']=="github.event_name == 'pull_request'"),'Conditional mandatory normal source step')
  reports.append({'path':spec['path'],'sha256':digest(raw),'required_steps':steps})
 return reports
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--verify',action='store_true');a.add_argument('--out',required=True,type=pathlib.Path);a.add_argument('--dispatch',type=pathlib.Path,default=S/'f2f607b0-exact18-dispatch-v2/receipt.json');a.add_argument('--terminal-jobs',type=pathlib.Path,default=S/'final-f2f607b0-metadata/terminal-jobs.json');x=a.parse_args()
 if not x.verify:print(json.dumps({'execute':False,'sha':SHA,'tree':TREE,'scope':'23 actual workflows/current checks/required steps/source pins/auxDAG; no localHEAD or fixeddev requirement','stdout_union':'UNPROVEN','artifacts':'UNINSPECTED','photographic_acceptance':'OPEN'},indent=2));return 0
 out=x.out.resolve();need(out.is_relative_to(S),'Outside shared output required');out.mkdir(exist_ok=False);report={'sha':SHA,'tree':TREE,'standard_ci_gate_passed':False,'merge_qualified':False,'stdout_union':'UNPROVEN','artifacts':'UNINSPECTED','photographic_acceptance':'OPEN','errors':[],'scope':'Normal metadata CI gate only; no ready/merge action, no frozen-dev prerequisite'}
 try:
  v=configure();w=module('approved_observer_inputs',OBSERVER,OBSERVER_SHA);manifest,dispatch,expected=w.inputs(x.dispatch);need(manifest['sha']==SHA and manifest['tree']==TREE,'Frozen manifest changed');need(git('rev-parse',SHA+'^{commit}').decode().strip()==SHA and git('rev-parse',SHA+'^{tree}').decode().strip()==TREE,'Exact source object/tree unavailable');raw={p:git('show',SHA+':'+p)for p in v.PINS};v.source_ok(raw);report['normal_source_contracts']=normal_source_contracts(v,manifest);saved=load(x.terminal_jobs);deadline=time.monotonic()+45
  queries={'smokes':f'actions/workflows/chicago-4d-smoke.yml/runs?head_sha={SHA}&event=workflow_dispatch&per_page=100','checks':f'commits/{SHA}/check-runs?per_page=100','statuses':f'commits/{SHA}/status?per_page=100','pr':'pulls/1041','dev':'git/ref/heads/dev','branch':'git/ref/heads/'+BRANCH,'commit':'git/commits/'+SHA};queries.update({'normal_'+str(rid):'actions/runs/'+str(rid)for rid,spec in expected.items()if not spec['selected_smoke']});queries.update({'code_'+str(i):'git/blobs/'+v.BLOB_IDS[p]for i,p in enumerate(v.PINS)})
  def get(key,endpoint):
   remaining=deadline-time.monotonic();need(remaining>0,'45s total metadata deadline');r=subprocess.run(['gh','api','--hostname','github.com','--method','GET','repos/'+REPO+'/'+endpoint],capture_output=True,text=True,timeout=remaining);(out/(key+'.stdout.json')).write_text(r.stdout);(out/(key+'.stderr.txt')).write_text(r.stderr);need(r.returncode==0,'Normal GET failed; no retry '+endpoint);return json.loads(r.stdout)
  with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
   futures={pool.submit(get,k,e):k for k,e in queries.items()};data={}
   for f in concurrent.futures.as_completed(futures):data[futures[f]]=f.result()
  need(data['branch']['object']['sha']==SHA and data['commit']['sha']==SHA and data['commit']['tree']['sha']==TREE,'Remote head/tree changed')
  for i,p in enumerate(v.PINS):
   b=data['code_'+str(i)];need(b['sha']==v.BLOB_IDS[p]and b['encoding']=='base64','Remote CODE blob identity changed');decoded=base64.b64decode(b['content']);need(decoded==raw[p]and digest(decoded)==v.PINS[p]and git('rev-parse',SHA+':'+p).decode().strip()==v.BLOB_IDS[p],'Remote/local CODE source mismatch '+p)
  listing=data['smokes'];smokeids={rid for rid,spec in expected.items()if spec['selected_smoke']};need(listing['total_count']==len(listing['workflow_runs'])==18 and {r['id']for r in listing['workflow_runs']}==smokeids,'Exact remote18 runset changed');runs={r['id']:r for r in listing['workflow_runs']};runs.update({rid:data['normal_'+str(rid)]for rid,spec in expected.items()if not spec['selected_smoke']});jobids,auxiliary=records_ok(v,saved,runs,expected);checks_ok(v,data['checks'],jobids);statuses=data['statuses'];need(statuses['total_count']==len(statuses['statuses'])and all(s['state']=='success'for s in statuses['statuses']),'Legacy status truncated/non-success')
  pr=data['pr'];need(pr['state']=='open'and pr['head']['sha']==SHA and pr['head']['ref']==BRANCH and pr['head']['repo']['full_name']==REPO and pr['base']['ref']=='dev','PR exact source/target/state changed')
  # Distinct final snapshot; dev observations are recorded separately, never required equal to the manifest or stale PRbase metadata.
  with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
   a=pool.submit(get,'pr_final','pulls/1041');b=pool.submit(get,'dev_final','git/ref/heads/dev');c=pool.submit(get,'branch_final','git/ref/heads/'+BRANCH);pr2,dev2,branch2=a.result(),b.result(),c.result()
  need(branch2['object']['sha']==SHA and pr2['state']=='open'and pr2['head']['sha']==SHA and pr2['head']['ref']==BRANCH and pr2['head']['repo']['full_name']==REPO and pr2['base']['ref']=='dev','Final exact source/target/state changed')
  report.update(standard_ci_gate_passed=True,selected_workflows_success=18,normal_workflows_success=5,all_actual_jobs=len(jobids),all26remote_CODE_pins=True,auxiliary_skip_classification=auxiliary,optional_teamster_skip_id=TEAM_SKIP,pr_draft=pr2['draft'],pr_mergeable=pr2.get('mergeable'),pr_mergeable_state=pr2.get('mergeable_state'),actual_dev_first=data['dev']['object']['sha'],actual_dev_final=dev2['object']['sha'],pr_base_metadata_first=pr['base']['sha'],pr_base_metadata_final=pr2['base']['sha'],normal_merge_still_required='Fresh actual mergeability/current required checks plus ordinary exact-head conditional DEV merge respecting protection; no admin/bypass',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:report['errors'].append(str(e))
 (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if report['standard_ci_gate_passed']else 1
if __name__=='__main__':sys.exit(main())
