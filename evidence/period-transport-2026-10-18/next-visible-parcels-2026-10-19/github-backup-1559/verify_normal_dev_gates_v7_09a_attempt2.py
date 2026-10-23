#!/usr/bin/env python3
"""Read-only parameterized exact-head normal CI gate audit. Never proves stdout union, artifacts or photographs.
No request occurs without --verify. Requires PyYAML; only normal configured gh api GET.
"""
import argparse,base64,concurrent.futures,hashlib,json,pathlib,re,subprocess,sys,time,datetime
import yaml
SHA='668e48180cfa20fe48b594041fcc0c0e2499ee72'
REPO='kevinrhaas/chicago'; BRANCH='steward/period-transport-2793'
GRID={(v,s) for v in ('desktop','mobile') for s in ('1-2','3-4','5','6-7','8','9-12','13','14','15')}
ROOT=pathlib.Path('/workspace/chicago'); SHARED=pathlib.Path('/workspace/shared')
SMOKE='.github/workflows/chicago-4d-smoke.yml'; HUMAN='.github/workflows/chicago-4d-humans.yml'
PINS={'.github/workflows/chicago-4d-smoke.yml': 'b2d6ae3c355e3604a807053088367f3e3ecda4e2d2bc63ca6bc15150848e4fde', '.github/workflows/chicago-4d-humans.yml': '62048edeed40b6d5fe8c42feec1a031b7b2581a39ec7215ce0a20b170769c847', 'chicago/4d/tools/smoke_renderer.mjs': '2b435da932f77e6dddcc93ec61917c21588ee24731df6050b56230827b48356f', 'chicago/4d/tools/human_fixture.mjs': '48c1666963013db003dd78dd9435541ac2d8a68cbbfcebb0d5b38a14295f3473', 'chicago/4d/tools/human_actor.mjs': '50e03ed95eb0b6c81879d1584a5ca0ef03b41a261d2abc3628bd4a1cddb5dad0', 'chicago/4d/tools/human_teamster.mjs': '5eb6f2c7d6379145444062fc74a90aaf02d7ac08d234edcdc93772361cf5c81a', 'chicago/4d/tools/human_export.sh': '7958fa031316794db38bd1f3e181583767a642ca513473b03243acb39c171946', 'chicago/4d/renderers/web/js/flora.js': 'bb9582d094a502b1ea82b9a0cf2de3d1eebed02157b71b80bb55160617b989dd', 'chicago/4d/tools/human_teamster_blend.py': 'a96e4dd1ca0f7dd488c82c4b43c0f12a32589fbeeadb277f788e65aa49e67fda', 'chicago/4d/tools/human_seated_study.py': '3811a931f70ac57c17f6ad78c1cff7f3a29f67f63194aea86b05a32f0acf99f7', 'chicago/4d/tools/human_seated_runtime.mjs': '1ef60a381bdf55c5b5fc35a2f3c9c3bca95a3ee1313ab6c4ddee618e915b6371', 'chicago/4d/tools/human_seated_driver.mjs': 'd66b5bdd3378a608285c8172a4e9ce6f140d53e8b88200dd29c3a299e2234164', 'chicago/4d/tools/human_seated_driver.html': '20451cb15bb8f671a19a81eb49636ec8365b0273c34e253ba960bf83b8f56c9e', 'chicago/4d/tools/human_seated_driver.cjs': '90ce8462d1fb6f28ce08d5813b8c4863db04edd8feea439c16bc4a418da56508', 'chicago/4d/tools/test_human_seated_study.py': '29fcdd7740e287de5ac59dbed5165a69bd53e75b5037de219677ef39993b251d', 'chicago/4d/tools/test_human_seated_runtime.mjs': 'c524d02f6021a349bae51093af31b3f7b9a042ced336045f55786bc7fa771d73', 'chicago/4d/tools/transport/generate_wagon.py': 'c9fa9985816071b2dc24871efddde9139088d2159b7db34fc603f20b2a9a4484', 'chicago/4d/tools/transport/smoke_wagon_driver.cjs': '155ca0c789eafe0827580f7f242b2d90f3856363dbf18e8a64eaa37e90a6b7e2', 'chicago/4d/renderers/web/transport/wagon-driver/fixture.js': 'c65530827b889357e62d806834053019a423471d99cca2d07a05e110c662e817', 'chicago/4d/renderers/web/transport/wagon-driver/index.html': '59cde5682ddc37e6db845758ee0c7f0416d8cf0a5bebb5e10d5fc4ffa2bb459f', 'chicago/4d/data/transport/studies/wagon-driver-bench.json': '1675f0fee2e3dce8c55c4bd6563a1ac5e675bf4205de175fb0cc41733f5b4fd9', 'chicago/4d/data/humans/poses/w01/bardwell_otis_1835-triangle-corrected-pose.json': 'f68233e814e084fd53a3f3cb30909c44b80558867e3d497b8f470b48f852e723', 'chicago/4d/data/humans/poses/w01/dufresne_joseph_1835-triangle-corrected-pose.json': '06ea75d314c4a4aad07f479fad2076480d246962595aabcb4bd07696bd3c3ba7', 'chicago/4d/data/humans/poses/w01/flynn_martin_1835-triangle-corrected-pose.json': '06ea75d314c4a4aad07f479fad2076480d246962595aabcb4bd07696bd3c3ba7', 'chicago/4d/data/humans/poses/w01/resident-driver-bindings.json': '43dbca2c34b1a25a8747b83f64cfdc849071f3a2f6399068405cb7143e0e1212', '.github/workflows/chicago-4d-bake.yml': 'cf7e706a594e12c0cb2628c6acb4826b35faf2bb8fd4302702a5b0ea0e62d145'}
BLOB_IDS={'.github/workflows/chicago-4d-smoke.yml': '43fdc6205607ff38d4ae768c2df608099b81d1e1', '.github/workflows/chicago-4d-humans.yml': 'bbeb04e12c66b356a9b66acb2c83a21808c2e897', 'chicago/4d/tools/smoke_renderer.mjs': '1a388c6e79dec079b2e0fbcc12218a4228bf9d7d', 'chicago/4d/tools/human_fixture.mjs': '1d65b03e80f8ba00164bfe929049b7347d0cc752', 'chicago/4d/tools/human_actor.mjs': '845d1bd7c77d3749b59fd0cd9ea10c6e5f6b175b', 'chicago/4d/tools/human_teamster.mjs': 'e9b1440d8d91ee3f64d675a48456c1fb6579ae9e', 'chicago/4d/tools/human_export.sh': 'dfa830cac6d9651b496d1763f8198be3391f784d', 'chicago/4d/renderers/web/js/flora.js': '30ccb239bdc3c29fb805a702f8dec18df44ea960', 'chicago/4d/tools/human_teamster_blend.py': '0c9a60b900bf26c5bdbb0d848e4bddcb70e55d59', 'chicago/4d/tools/human_seated_study.py': '93659a8ad809dff2900088b60fa55b8b5adaea52', 'chicago/4d/tools/human_seated_runtime.mjs': 'bd52ca54239e948376ff4e6ca768f95a081ada5b', 'chicago/4d/tools/human_seated_driver.mjs': 'ee99292f5b71f08fe23a8d7fdb2f7d632a5bee65', 'chicago/4d/tools/human_seated_driver.html': '23d1fdc89949ec6df2c7c881d2d2f4a3cb2b1a3c', 'chicago/4d/tools/human_seated_driver.cjs': '58f6f5b64fa937e416fc81a92d12a0636eaf44a2', 'chicago/4d/tools/test_human_seated_study.py': '508b5d77ebe6aff6d17f23546db2257f27757a91', 'chicago/4d/tools/test_human_seated_runtime.mjs': '3cfd23995a842dbd556ada33387fb908de02cb8f', 'chicago/4d/tools/transport/generate_wagon.py': 'd563d57fb3745853a233268c11f757b3d42ebda2', 'chicago/4d/tools/transport/smoke_wagon_driver.cjs': 'e5b7b549ebe2c56a9ba28463b59d87c3d4fad205', 'chicago/4d/renderers/web/transport/wagon-driver/fixture.js': '36318efb56c62b6177d55cdb268ccc5f0e5df317', 'chicago/4d/renderers/web/transport/wagon-driver/index.html': '4d947d2b47d484111ce01909835c22d7375c53fc', 'chicago/4d/data/transport/studies/wagon-driver-bench.json': 'c7422f38ec9d5b19d674e408cada9daa48be41fa', 'chicago/4d/data/humans/poses/w01/bardwell_otis_1835-triangle-corrected-pose.json': '2c6c00f331d12faa17c0886087bd9934f9ff826f', 'chicago/4d/data/humans/poses/w01/dufresne_joseph_1835-triangle-corrected-pose.json': '321afcd5be99d0ff774efa3e32e7df9c4fcf36c2', 'chicago/4d/data/humans/poses/w01/flynn_martin_1835-triangle-corrected-pose.json': '321afcd5be99d0ff774efa3e32e7df9c4fcf36c2', 'chicago/4d/data/humans/poses/w01/resident-driver-bindings.json': '3910796cfb81178ebeccb42f7b8186eb737255f5', '.github/workflows/chicago-4d-bake.yml': '6c8aad6e67855cc439bcb61369173ef961c5d11c'}
PINS_FINALIZED=True
PINNED_TREE='5e0bfad5fd30b322596efd469ab4dcc3f962c63d'
SEATED_STEPS=['Prepare opt-in physical W01 seated study','Inspect actual exported named seated residents on W01']
SEATED_INPUTS={'build_teamsters':True,'build_seated_driver_study':True}
HUMAN_STEPS=['Rebuild the fixture and require the committed bytes','Open every human GLB in the browser, at both viewports','Drive the browser actor with the fixture, at both viewports']
TEAM_STEPS=['Verify the original body preparation','Build three canonical masters and export through the portable path','Build same-new-master parented hierarchy controls (test artifacts only)','Audit declared resident animation time bounds before browser loading','Check actual resident hair material, embedded PNG and source/web LOD dimensions','Validate the actual new GLB containers','Validate hierarchy control warnings with exact node pointers','Measure all human exports and inspect the workwear studies']
TEAM_STEPS=TEAM_STEPS+SEATED_STEPS
SMOKE_STEPS=['Publish the mirror the smoke serves (site/4d/ is generated)','Run the smoke against the published mirror']

AUX_WORKFLOW='.github/workflows/chicago-4d-bake.yml'
AUX_RUN=39266128054
AUX_HEAD='09a3ad1d4af7c87c5026de1077497d8a04a5a562'
AUX_IDS={'warranted':118106051521,'bake':118108138306,'smoke':118108139618,'open-pr':118108140569,'publish-bundle':118108140572,'fresh-consumer':118108140881}

def need(ok,msg):
 if not ok: raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def committed(path):return subprocess.check_output(['git','-C',str(ROOT),'show',SHA+':'+path])
def success(x,label):need(x.get('status')=='completed' and x.get('conclusion')=='success',label+' not completed SUCCESS')
RERUN_IDS={39266459095,39266463876}
def expected_attempt(rid):return 2 if rid in RERUN_IDS else 1
def rerun_receipt_ok(receipt):
 need(receipt.get('repository')==REPO and receipt.get('sha')==AUX_HEAD==SHA and receipt.get('branch')==BRANCH,'rerun receipt frozen identity mismatch')
 rows=receipt.get('reruns',[])
 need(len(rows)==2 and {r.get('run_id') for r in rows}==RERUN_IDS,'exact two diagnosed rerun IDs required')
 for r in rows:
  need(r.get('previous_attempt')==1 and r.get('required_attempt')==2 and r.get('post_succeeded') is True and r.get('method')=='POST' and r.get('endpoint')=='actions/runs/'+str(r['run_id'])+'/rerun','exact successful whole-workflow attempt2 rerun required')
  need(r.get('reason')=='contradictory terminal mandatory-step metadata' and r.get('preserved_attempt1_evidence_sha256') and re.fullmatch('[0-9a-f]{64}',r['preserved_attempt1_evidence_sha256']),'diagnosed preserved attempt1 evidence required')
def run_ok(x,path):
 need(x.get('head_sha')==SHA and x.get('head_branch')==BRANCH and x.get('event')=='workflow_dispatch' and x.get('path')==path and x.get('run_attempt')==expected_attempt(x.get('id')),'wrong run identity/attempt')
 success(x,'workflow '+str(x.get('id')))
def jobs_ok(jobs,rid,names):
 need(len({j['id'] for j in jobs})==len(jobs),'duplicate job IDs')
 for name,steps in names.items():
  js=[j for j in jobs if j.get('name')==name];need(len(js)==1,'missing/duplicate mandatory job '+name);j=js[0]
  need(j.get('run_id')==rid and j.get('head_sha')==SHA and j.get('run_attempt')==expected_attempt(rid),'wrong job identity');success(j,name)
  need(j.get('html_url')=='https://github.com/'+REPO+'/actions/runs/'+str(rid)+'/job/'+str(j['id']),'mandatory job/check ID mismatch')
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
   job=doc['jobs'][name];need('if' not in job or (path==HUMAN and name=='teamster-studies' and job['if']=="github.event_name == 'workflow_dispatch' && (inputs.build_teamsters || inputs.build_seated_driver_study)"),'conditional mandatory job')
   need(job.get('runs-on')=='ubuntu-latest','unexpected runner')
   need(job.get('timeout-minutes',0)>0,'missing job timeout')
   steps=job['steps'];checkout=[s for s in steps if str(s.get('uses','')).startswith('actions/checkout@')]
   need(len(checkout)==1 and not checkout[0].get('with',{}).get('ref'),'checkout ref override')
   for name2 in required:
    matches=[s for s in steps if s.get('name')==name2];need(len(matches)==1,'source mandatory step absent '+name2);s=matches[0]
    need((s.get('if')=='inputs.build_seated_driver_study' if name2 in SEATED_STEPS else 'if' not in s) and 'run' in s and s.get('working-directory')=='chicago/4d','conditional/nonrun/wrongdirectory mandatory step')
    code=s['run'];need(not re.search(r'\|\|\s*(?:true|:|echo)|set\s+\+e|exit\s+0\b',code),'shell swallows failure')
    need(s.get('shell') in (None,'bash') and not job.get('defaults'),'unexpected shell/defaults; default ubuntu bash -e is required')
    if '| tee ' in code:need('pipefail' in code,'pipeline lacks pipefail')
  if path==SMOKE:
   s=next(x for x in doc['jobs']['smoke']['steps'] if x.get('name')==SMOKE_STEPS[1]);need(s['run']=='node tools/smoke_renderer.mjs --published','not actual published smoke')
   need(s.get('env')=={'SMOKE_VIEWPORT':'${{ inputs.viewport }}','SMOKE_STAGE':'${{ inputs.stage }}'},'dispatch input wiring changed')
  else:
   code=next(x for x in doc['jobs']['teamster-studies']['steps'] if x.get('name')=='Measure all human exports and inspect the workwear studies')['run']
   for fragment in ['bash tools/publish.sh','tools/human_teamster.mjs --published --sole-contact','tools/human_teamster.mjs --masters --sole-contact','tools/test_human_inspection.mjs']:need(fragment in code,'inspection command missing '+fragment)
   prep=next(x for x in doc['jobs']['teamster-studies']['steps'] if x.get('name')==SEATED_STEPS[0])['run'];inspection=next(x for x in doc['jobs']['teamster-studies']['steps'] if x.get('name')==SEATED_STEPS[1])['run']
   need('tools/transport/generate_wagon.py --parameters data/transport/studies/wagon-driver-bench.json' in prep and 'tools/test_human_seated_study.py' in prep,'physical bench producer/pure study probe absent')
   need('tools/test_human_seated_runtime.mjs --supported renderers/web/transport/wagon-driver/wagon-w01.glb --baseline renderers/web/transport/wagon/wagon-w01.glb' in prep,'actual source bench probe missing')
   need('node tools/transport/smoke_wagon_driver.cjs . ' in inspection,'actual source bench browser probe missing')
   published_lines=[line for line in inspection.splitlines() if 'node tools/transport/smoke_wagon_driver.cjs ../../site/4d ' in line];need(len(published_lines)==1 and '--published' in published_lines[0],'actual published bench browser probe missing')
   need('node tools/human_seated_driver.cjs' in inspection,'actual named seated inspection missing')
   need('process.exitCode = 1' in text,'container validation failure not propagated')
 smoke=raw['chicago/4d/tools/smoke_renderer.mjs'].decode();need('process.exit(1)' in smoke and "console.log('SMOKE PASS')" in smoke,'smoke failure propagation absent')
 need('const PARTS = 15' in smoke,'unexpected stage topology')
 auxiliary_source_ok(raw[AUX_WORKFLOW])

def auxiliary_source_ok(raw):
 d=yaml.safe_load(raw);jobs=d['jobs'];need(set(jobs)==set(AUX_IDS),'auxiliary source jobset changed')
 need('if' not in jobs['warranted'],'warranted job conditional')
 steps=jobs['warranted']['steps'];need(len(steps)==4 and steps[2].get('id')=='q' and 'if' not in steps[2] and steps[3].get('id')=='live' and steps[3].get('if')=="steps.q.outputs.bake == '1'",'warranted q/live source order/condition changed')
 need('bake=0' in steps[2]['run'] and 'bake=1' in steps[2]['run'] and '0|1)' in steps[2]['run'],'q output contract not bounded0/1')
 need(jobs['warranted']['outputs']['bake']=="${{ steps.live.outputs.declined == '1' && 'declined' || steps.q.outputs.bake }}",'warranted output expression changed')
 need(jobs['bake']['needs']=='warranted' and jobs['bake']['if']=="needs.warranted.outputs.bake == '1'",'bake prerequisite/condition changed')
 need(jobs['smoke']['needs']=='bake' and 'if' not in jobs['smoke'],'dependent auxiliary smoke changed')
 need(jobs['open-pr']['needs']==['bake','smoke'] and jobs['open-pr']['if']=="needs.bake.outputs.changed == '1' && needs.bake.outputs.base_live == '1'",'open-pr dependency changed')
 need(jobs['publish-bundle']['needs']==['bake','smoke'] and jobs['publish-bundle']['if']=="needs.bake.outputs.bundle == '1'",'bundle dependency changed')
 need(jobs['fresh-consumer']['needs']==['bake','publish-bundle'] and 'if' not in jobs['fresh-consumer'],'consumer dependency changed')

def auxiliary_jobs_ok(run,data):
 need(SHA==AUX_HEAD and run['id']==AUX_RUN and run['head_sha']==SHA and run['head_branch']==BRANCH and run['event']=='push' and run['path']==AUX_WORKFLOW and run['run_attempt']==1,'wrong auxiliary workflow identity')
 success(run,'auxiliary workflow');jobs=data['jobs'];need(data['total_count']==len(jobs)==len(AUX_IDS),'truncated/extra auxiliary jobs')
 for name,jid in AUX_IDS.items():
  found=[j for j in jobs if j['id']==jid and j['name']==name];need(len(found)==1,'auxiliary job identity changed '+name);j=found[0]
  need(j['run_id']==AUX_RUN and j['head_sha']==SHA and j['run_attempt']==1 and j['check_run_url'].endswith('/check-runs/'+str(jid)),'auxiliary job/check binding mismatch')
  if name=='warranted':
   success(j,'warranted prerequisite')
   need(any(s['number']==4 and s['name']=='Run set -uo pipefail' and s['status']=='completed' and s['conclusion']=='success' for s in j['steps']),'actual q prerequisite missing/success not established')
   need(any(s['number']==5 and s['name']=='Run set -uo pipefail' and s['status']=='completed' and s['conclusion']=='skipped' for s in j['steps']),'actual conditional live skip missing')
   for step in j['steps']:
    if step.get('number')==5 and step.get('name')=='Run set -uo pipefail' and step.get('status')=='completed' and step.get('conclusion')=='skipped':continue
    if step.get('name','').startswith('Post ') and step.get('status')=='completed' and step.get('conclusion')=='skipped':continue
    success(step,'warranted/'+step.get('name','?'))
  else:need(j['status']=='completed' and j['conclusion']=='skipped' and not j['steps'],'auxiliary job was not an unexecuted dependency skip '+name)
 return {'scope':'Exact auxiliary push workflow only; never selected qualification runs','workflow_run_id':AUX_RUN,'check_ids':AUX_IDS,'warranted_success':True,'bake_condition_result':'q output0 inferred from bounded0/1 source, successful q step4 and conditional live step5 skipped; job output falls through to q; bake condition false','actual_output_value':'Not exposed by ordinary jobs/check metadata; no FRESH/declined value claim','downstream':'Skipped via frozen prerequisite DAG/conditions','logs_or_artifacts_read':False}

def auxiliary_skip_check(c):
 return c.get('name')!='warranted' and AUX_IDS.get(c.get('name'))==c.get('id') and c.get('head_sha')==SHA==AUX_HEAD and c.get('status')=='completed' and c.get('conclusion')=='skipped' and c.get('html_url')=='https://github.com/'+REPO+'/actions/runs/'+str(AUX_RUN)+'/job/'+str(c['id'])

def main():
 global SHA
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify',action='store_true');ap.add_argument('--sha',required=True);ap.add_argument('--out',required=True);ap.add_argument('--dispatch',required=True);ap.add_argument('--canonical',required=True);ap.add_argument('--terminal-jobs',required=True);ap.add_argument('--reruns',required=True);args=ap.parse_args();need(re.fullmatch(r'[0-9a-f]{40}',args.sha) is not None,'--sha must be full40hex');SHA=args.sha
 if not args.verify:print(json.dumps({'execute':False,'pins_finalized':PINS_FINALIZED,'pinned_tree':PINNED_TREE,'canonical_inputs':SEATED_INPUTS,'sha':SHA,'source_pins':PINS,'source_blob_ids':BLOB_IDS,'network':'GET JSON only; total45second audit deadline; no retries/logs/artifacts','out':args.out},indent=2));return 0
 need(PINS_FINALIZED,'final reviewed source pins not yet frozen; execution prohibited')
 out=pathlib.Path(args.out);need(out.is_absolute() and str(out).startswith('/workspace/shared/'),'outside shared output required');out.mkdir(exist_ok=False)
 report={'sha':SHA,'source_blob_ids':BLOB_IDS,'pinned_tree':PINNED_TREE,'standard_ci_gate_passed':False,'report_ci_steps_passed':False,'coverage_proof_passed':False,'strict_log_union':'UNPROVEN','artifacts':'UNINSPECTED','photographic_acceptance':'UNACCEPTED','errors':[],'scope':'Normal CI metadata gate only; no ready/merge action or stdout-equivalence claim'}
 try:
  need(subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()==SHA,'local HEAD differs')
  need(subprocess.check_output(['git','-C',str(ROOT),'rev-parse',SHA+'^{tree}'],text=True).strip()==PINNED_TREE,'final commit tree differs reviewedstagedtree')
  raw={p:committed(p) for p in PINS};source_ok(raw)
  dispatch=load(args.dispatch);can=load(args.canonical);saved=load(args.terminal_jobs);rerun_receipt_ok(load(args.reruns))
  for d in [dispatch,can]:need(d['repository']==REPO and d['branch']==BRANCH and d['sha']==SHA and d['remote_head_after']==SHA,'dispatch frozen identity mismatch')
  ds=dispatch['dispatches'];need(len(ds)==18 and {(x['viewport'],x['stage']) for x in ds}==GRID and all(x['post_succeeded'] is True for x in ds),'not exact18 successful grid POSTs')
  ids={x['id'] for x in dispatch['discovered_runs']};need(len(ids)==18 and all(x['head_sha']==SHA and x['run_attempt']==1 for x in dispatch['discovered_runs']),'wrong18 discovered runs')
  need(can['post_succeeded'] is True and can['inputs']==SEATED_INPUTS and len(can['runs'])==1,'canonical dispatch not true/single')
  cid=can['runs'][0]['id'];need(cid not in ids and can['runs'][0]['head_sha']==SHA,'canonical run identity')
  deadline=time.monotonic()+45
  def get(endpoint):
   remaining=deadline-time.monotonic();need(remaining>0,'45s metadata deadline exceeded')
   result=subprocess.run(['gh','api','--method','GET','repos/'+REPO+'/'+endpoint],capture_output=True,text=True,timeout=remaining)
   need(result.returncode==0,'normal GitHub GET failed '+endpoint+' (no retry)')
   data=json.loads(result.stdout);return data
  queries={'smoke_runs':'actions/workflows/chicago-4d-smoke.yml/runs?head_sha='+SHA+'&event=workflow_dispatch&per_page=100','canonical_run':'actions/runs/'+str(cid),'canonical_jobs':'actions/runs/'+str(cid)+'/jobs?filter=latest&per_page=100','checks':'commits/'+SHA+'/check-runs?per_page=100','statuses':'commits/'+SHA+'/status?per_page=100','pr':'pulls/1041','dev_ref':'git/ref/heads/dev','head_commit':'git/commits/'+SHA,'auxiliary_run':'actions/runs/'+str(AUX_RUN),'auxiliary_jobs':'actions/runs/'+str(AUX_RUN)+'/jobs?filter=latest&per_page=100'}
  queries.update({'source_'+str(i):'git/blobs/'+BLOB_IDS[p] for i,p in enumerate(PINS)})
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
   futures={pool.submit(get,e):k for k,e in queries.items()};results={}
   for f in concurrent.futures.as_completed(futures):
    key=futures[f];results[key]=f.result();(out/(key+'.json')).write_text(json.dumps(results[key],indent=2)+'\n')
  need(results['head_commit']['sha']==SHA and results['head_commit']['tree']['sha']==PINNED_TREE,'remote committed tree differs reviewedtree')
  for i,p in enumerate(PINS):
   blob=results['source_'+str(i)];need(blob.get('sha')==BLOB_IDS[p] and blob.get('encoding')=='base64','remote code blob identity/encoding mismatch '+p)
   data=base64.b64decode(blob['content']);need(digest(data)==PINS[p] and data==raw[p],'remote frozen source differs '+p)
   need(subprocess.check_output(['git','-C',str(ROOT),'rev-parse',SHA+':'+p],text=True).strip()==BLOB_IDS[p],'local committed blob identity mismatch '+p)
  runs=results['smoke_runs'];need(runs['total_count']==18 and len(runs['workflow_runs'])==18 and {r['id'] for r in runs['workflow_runs']}==ids,'remote dispatch run set differs: extras/missing')
  for r in runs['workflow_runs']:
   run_ok(r,SMOKE);record=saved.get(str(r['id']));need(record is not None,'missing terminal job evidence');need(record['attempt']==expected_attempt(r['id']) and record['head_sha']==SHA,'wrong saved job record');jobs_ok(record['jobs'],r['id'],{'smoke':SMOKE_STEPS})
  run_ok(results['canonical_run'],HUMAN);cj=results['canonical_jobs'];need(cj['total_count']==len(cj['jobs']),'truncated canonical jobs');jobs_ok(cj['jobs'],cid,{'humans':HUMAN_STEPS,'teamster-studies':TEAM_STEPS})
  report['auxiliary_skip_classification']=auxiliary_jobs_ok(results['auxiliary_run'],results['auxiliary_jobs'])
  checks=results['checks'];need(checks['total_count']==len(checks['check_runs']),'truncated check list')
  current_ids={c['id'] for c in checks['check_runs']}
  for rid in ids:
   for j in saved[str(rid)]['jobs']:
    if j['name']=='smoke':need(j['id'] in current_ids,'selected attempt mandatory job/check not current')
  for j in cj['jobs']:
   if j['name'] in ('humans','teamster-studies'):need(j['id'] in current_ids,'canonical mandatory job/check not current')
  for c in checks['check_runs']:
   need(c.get('head_sha')==SHA and c.get('status')=='completed','wronghead/pending check')
   need(c.get('conclusion')=='success' or (c['name']=='teamster-studies' and c.get('conclusion')=='skipped') or auxiliary_skip_check(c),'non-success check '+c['name'])
  for n in ['gate','moving-frames','humans','report']:need(any(c['name']==n and c['conclusion']=='success' for c in checks['check_runs']),'mandatory check absent '+n)
  statuses=results['statuses'];need(statuses['total_count']==len(statuses['statuses']),'truncated statuses');need(all(s['state']=='success' for s in statuses['statuses']),'non-success legacy status')
  report['report_ci_steps_passed']=True
  report['chosen_attempts']={str(rid):expected_attempt(rid) for rid in ids|{cid}}
  report['attempt1_contradictions_preserved']=True
  pr=results['pr'];need(pr['base']['sha']==results['dev_ref']['object']['sha'],'PR base metadata stale relative to actualdev');need(pr['state']=='open' and pr['head']['sha']==SHA and pr['head']['repo']['full_name']==REPO and pr['head']['ref']==BRANCH and pr['base']['ref']=='dev' and pr['mergeable'] is True and pr['mergeable_state']=='clean','PR not exacthead/open/dev/clean/mergeable')
  # A final bounded consistency read detects dev/PR advancement during this audit;
  # this is a distinct final snapshot, not a retry of a failed request.
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   pf=pool.submit(get,'pulls/1041');df=pool.submit(get,'git/ref/heads/dev');last_pr=pf.result();last_dev=df.result()
  (out/'pr_final.json').write_text(json.dumps(last_pr,indent=2)+'\n');(out/'dev_ref_final.json').write_text(json.dumps(last_dev,indent=2)+'\n')
  need(last_dev['object']['sha']==results['dev_ref']['object']['sha'],'actual dev advanced during audit')
  need(last_pr['state']=='open' and last_pr['head']['sha']==SHA and last_pr['base']['ref']=='dev' and last_pr['base']['sha']==last_dev['object']['sha'] and last_pr['mergeable'] is True and last_pr['mergeable_state']=='clean','PR changed/not clean at final consistency read')
  report['fresh_final_base_sha']=last_dev['object']['sha']
  report.update(standard_ci_gate_passed=True,smoke_workflows_success=18,canonical_workflows_success=1,pr_draft=pr['draft'],input_pairing='Individual run-to-input pairing not inferred; successful dispatchset and exact remote runset independently reconciled',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:report['errors'].append(str(e))
 (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if report['standard_ci_gate_passed'] else 1
if __name__=='__main__':sys.exit(main())
