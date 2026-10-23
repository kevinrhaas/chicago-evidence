#!/usr/bin/env python3
"""One finite GET-only qualification snapshot; never dispatch, rerun or mutate GitHub."""
import argparse,base64,datetime,hashlib,io,json,pathlib,re,subprocess,zipfile
REPO='kevinrhaas/chicago';BRANCH='steward/1835-workwear-repair-20261021'
WORKFLOW='.github/workflows/chicago-4d-humans.yml'
WORKFLOW_SHA256='62048edeed40b6d5fe8c42feec1a031b7b2581a39ec7215ce0a20b170769c847'
ASSETS=['bardwell_otis_1835','dufresne_joseph_1835','flynn_martin_1835']
REQUIRED={
 'humans':['Rebuild the fixture and require the committed bytes','Open every human GLB in the browser, at both viewports','Drive the browser actor with the fixture, at both viewports'],
 'teamster-studies':['Verify the original body preparation','Prepare opt-in physical W01 seated study',
 'Build three canonical masters and export through the portable path','Build same-new-master parented hierarchy controls (test artifacts only)',
 'Audit declared resident animation time bounds before browser loading','Check actual resident hair material, embedded PNG and source/web LOD dimensions',
 'Validate the actual new GLB containers','Validate hierarchy control warnings with exact node pointers',
 'Measure all human exports and inspect the workwear studies','Inspect actual exported named seated residents on W01','Preserve masters, exports and inspection evidence']}
def need(ok,why):
 if not ok:raise ValueError(why)
def digest(data):return hashlib.sha256(data).hexdigest()
def get(endpoint,binary=False):
 # The HTTP method is constant. There is no write-capable command path.
 r=subprocess.run(['gh','api','--method','GET',f'repos/{REPO}/'+endpoint],capture_output=True,timeout=120)
 need(r.returncode==0,'GET failed: '+r.stderr.decode(errors='replace')[:1000])
 return r.stdout if binary else json.loads(r.stdout)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sha',required=True);p.add_argument('--run-id',required=True,type=int);p.add_argument('--dispatch-receipt',required=True,type=pathlib.Path);p.add_argument('--out',required=True,type=pathlib.Path);a=p.parse_args()
 need(re.fullmatch('[0-9a-f]{40}',a.sha),'full exact40SHA required');need(a.run_id>0,'actual run ID required')
 out=a.out.resolve();need(str(out).startswith('/workspace/shared/') and not out.exists(),'fresh shared output required');out.mkdir()
 report={'repository':REPO,'branch':BRANCH,'sha':a.sha,'run_id':a.run_id,'workflow':WORKFLOW,'workflow_sha256':WORKFLOW_SHA256,
  'fetched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mechanical_qualified':False,'photographic_accepted':False,'scope':'Actual CI containers/runtime/seated/sole evidence only; no production promotion or photographic acceptance'}
 def save(name,value):
  (out/name).write_text(json.dumps(value,indent=2)+'\n');return value
 def fetch(name,endpoint):return save(name,get(endpoint))
 try:
  receipt=json.loads(a.dispatch_receipt.read_text());save('dispatch-receipt.json',receipt)
  need(receipt['repository']==REPO and receipt['branch']==BRANCH and receipt['sha']==a.sha,'dispatch receipt identity differs')
  need(receipt['workflow'] in [WORKFLOW,WORKFLOW.split('/')[-1]],'dispatch workflow differs')
  need(receipt.get('post_succeeded') is True and receipt.get('inputs')=={'build_teamsters':True,'build_seated_driver_study':True},'both explicit inputs and one successful dispatch required')
  need(len(receipt.get('runs',[]))==1 and receipt['runs'][0]['id']==a.run_id,'actual run must equal one uniquely discovered dispatch run')
  need(a.run_id not in receipt.get('before_run_ids',[]),'run predates dispatch intent')
  ref=fetch('remote-ref.json','git/ref/heads/'+BRANCH);need(ref['object']['sha']==a.sha,'remote branch moved; root must reconcile, no retry')
  source=fetch('workflow-api.json','contents/'+WORKFLOW+'?ref='+a.sha);need(source.get('encoding')=='base64','workflow encoding')
  data=base64.b64decode(source['content']);(out/'workflow-at-run.yml').write_bytes(data);need(digest(data)==WORKFLOW_SHA256,'workflow source differs; review before adapting qualifier')
  sourcepins={}
  for path in ['chicago/4d/data/humans/recipes/worker_1835.json','chicago/4d/tools/human_teamster_blend.py','chicago/4d/tools/human_workwear_fit.py','chicago/4d/tools/human_eye_components.py','chicago/4d/tools/human_export.py','chicago/4d/tools/human_export.sh','chicago/4d/tools/human_source_normals.py','chicago/4d/tools/human_sole_contact.mjs']:
   blob=get('contents/'+path+'?ref='+a.sha);need(blob.get('encoding')=='base64','source input encoding: '+path);sourcepins[path]={'git_blob_sha':blob['sha'],'sha256':digest(base64.b64decode(blob['content']))}
  save('exact-head-source-inputs.json',sourcepins)
  run=fetch('run.json',f'actions/runs/{a.run_id}')
  need(run['head_sha']==a.sha and run['head_branch']==BRANCH and run['event']=='workflow_dispatch' and run['path']==WORKFLOW,'actual run source/ref/event differs')
  need(run['run_attempt']==1,'unexpected rerun attempt; no blind retry or substitution')
  need(run['created_at']>=receipt['requested_utc'][:19]+'Z','actual run predates intent')
  jobs=fetch('jobs.json',f'actions/runs/{a.run_id}/attempts/1/jobs?per_page=100');need(jobs['total_count']==len(jobs['jobs']),'jobs response truncated')
  inventory={}
  for name,steps in REQUIRED.items():
   found=[j for j in jobs['jobs'] if j['name']==name];need(len(found)==1,'missing/ambiguous mandatory job '+name);job=found[0]
   inventory[name]={'job_id':job['id'],'status':job['status'],'conclusion':job['conclusion'],'steps':job['steps']}
  save('required-job-inventory.json',inventory)
  if run['status']!='completed':report['status']='PENDING';return
  need(run['conclusion']=='success','actual run not successful')
  for name,expected in REQUIRED.items():
   job=inventory[name];need(job['status']=='completed' and job['conclusion']=='success','mandatory job did not succeed: '+name)
   for label in expected:
    rows=[s for s in job['steps'] if s['name']==label];need(len(rows)==1 and rows[0]['status']=='completed' and rows[0]['conclusion']=='success','mandatory step missing/skipped/failed: '+label)
  # Fresh API log ZIP, not gh run view's local log cache.
  logbytes=get(f'actions/runs/{a.run_id}/attempts/1/logs',binary=True);(out/'run-attempt1-logs.zip').write_bytes(logbytes)
  with zipfile.ZipFile(io.BytesIO(logbytes)) as z:
   logindex=[{'file':n,'bytes':len(z.read(n)),'sha256':digest(z.read(n))} for n in z.namelist() if not n.endswith('/')]
  save('log-index.json',logindex);report['log_zip_sha256']=digest(logbytes)
  artifacts=fetch('artifacts.json',f'actions/runs/{a.run_id}/artifacts?per_page=100');need(artifacts['total_count']==len(artifacts['artifacts']),'artifacts response truncated')
  matches=[x for x in artifacts['artifacts'] if x['name']=='resident-teamster-studies-'+a.sha];need(len(matches)==1 and matches[0]['expired'] is False,'one fresh exact-SHA artifact required')
  artifact=matches[0];need(artifact['workflow_run']['id']==a.run_id and artifact['workflow_run']['head_sha']==a.sha and artifact['workflow_run']['head_branch']==BRANCH,'artifact workflow/run/ref binding differs')
  payload=get(f'actions/artifacts/{artifact["id"]}/zip',binary=True);(out/'resident-studies.zip').write_bytes(payload);report['artifact_zip_sha256']=digest(payload)
  with zipfile.ZipFile(io.BytesIO(payload)) as z:
   names=[n for n in z.namelist() if not n.endswith('/')]
   save('artifact-file-index.json',[{'file':n,'bytes':z.getinfo(n).file_size,'sha256':digest(z.read(n))} for n in names])
   def member(suffix):
    found=[n for n in names if n==suffix or n.endswith('/'+suffix)];need(len(found)==1,'unique artifact member required: '+suffix);return found[0]
   def read(suffix):return json.loads(z.read(member(suffix)))
   def verify_glb_hash(file,expected):
    name=member(file);need(digest(z.read(name))==expected,'inspection/artifact GLB hash differs: '+file)
   coverage={}
   for kind,runtime,asset_kind in [('web','published','web_derivatives'),('source','source','masters')]:
    j=read('teamster-studies/'+kind+'/inspection.json');save(kind+'-inspection.json',j)
    need(j['runtime']==runtime and j['asset_kind']==asset_kind and j['mechanical_passed'] is True and not j['failures'],'source/published inspection incomplete')
    rows=j['runs'];need(len(rows)==24,'exact24 resident/LOD/viewport inspections required')
    expected={(asset,lod,vp) for asset in ASSETS for lod in range(4) for vp in ['desktop','mobile']};actual=set()
    for row in rows:
     m=re.fullmatch(r'assets/humans/(web/)?(\w+)\.lod([0-3])\.glb',row['file']);need(m is not None,'unexpected inspection file');asset=m[2];lod=int(m[3]);actual.add((asset,lod,row['viewport_name']))
     need(all(row['checks'].values()) and row['gl_error']==0 and not row['page_errors'] and not row['failed_requests'],'inspection runtime failure')
     verify_glb_hash('chicago/4d/'+row['file'],row['sha256'])
     if row['viewport_name']=='desktop':
      sole=row['walk_sole_contact'];need(sole['passed'] is True,'sole result failed');s=read('teamster-studies/'+kind+'/'+sole['receipt']);need(s['passed'] is True and s['provenance']['sha256']==row['sha256'],'fresh actual sole provenance differs')
    need(actual==expected,'resident/LOD/viewport grid incomplete/duplicated')
    if kind=='web':need(len(j['frame_repair_comparisons'])==6 and all(c['passed'] for c in j['frame_repair_comparisons']),'same-new-master source/hierarchy frame controls incomplete')
    coverage[kind]={'inspections':24,'sole_receipts':12,'mechanical_passed':True}
   seated=read('teamster-studies/seated-driver/seated-driver.json');save('seated-driver.json',seated)
   need(seated['passed'] is True and seated['browser_closed'] is True and seated['server_closed'] is True and len(seated['runs'])==6 and len(seated['refusals'])==3,'actual named seated study incomplete')
   need({(r['asset'],r['viewport']['width'],r['viewport']['height']) for r in seated['runs']}=={(asset,w,h) for asset in ASSETS for w,h in [(1280,800),(390,780)]},'seated resident/viewport grid differs')
   need(all(r['passed'] is True for r in seated['refusals']),'seated refusal control failed')
   for row in seated['runs']:
    need(row['passed'] is True and row['actual']['passed'] is True and row['actual']['clip']=='sit_drive' and row['actual']['scene']=='1835','seated actor/clip failed');verify_glb_hash('chicago/4d/assets/humans/web/'+row['asset']+'.lod0.glb',row['asset_sha256'])
   for kind in ['source','published']:
    j=read('teamster-studies/wagon-driver-'+kind+'/receipt.json');save('wagon-driver-'+kind+'.json',j);need(j['passed'] is True and j['closed'] is True and len(j['runs'])==2 and all(r['passed'] for r in j['runs']),'W01 source/published runtime incomplete')
   # Preserve validation inventories verbatim; warnings are not silently waived.
   validations=[n for n in names if n.endswith('.validation.json') and 'teamster-studies/' in n];need(len(validations)==24,'24 actual source/web container validations required')
   counts=[]
   for name in validations:
    v=json.loads(z.read(name));issues=v['issues'];need(issues['numErrors']==0 and not issues.get('truncated',False),'container errors or truncated messages');counts.append({'file':name,**issues})
   save('container-validation-issues.json',counts)
  report.update(status='COMPLETE',mechanical_qualified=True,coverage=coverage,seated_runs=6,seated_refusals=3,canonical_container_validations=24)
 except Exception as error:
  report['status']='NOT_QUALIFIED';report['reason']=str(error);raise
 finally:
  save('QUALIFICATION.json',report)
  print(json.dumps(report,indent=2))
if __name__=='__main__':main()
