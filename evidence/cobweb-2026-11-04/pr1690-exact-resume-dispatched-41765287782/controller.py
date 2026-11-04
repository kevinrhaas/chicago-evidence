"""Exact existing-PR dispatcher and read-only claim monitor; defaults to preparation.
Dispatch requires a separate root authorization file and green exact-SHA hosted CI.
No source/ticket edits; no automatic retry of the dispatch POST.
"""
from pathlib import Path
import argparse,base64,concurrent.futures,datetime,hashlib,json,os,re,subprocess,time
P=Path(__file__).resolve().parent
FEATURE='b37fdeca6b74d8e3c70945a75687140c0718f549'
REF='steward/chicago-native-exact-ticket-20261103'
HEAD='e9d93bf385623353a2134a18a98b959fbd84efb7'
LANE='cobweb-apertures-native-20261104'
PLATFORM='repos/kevinrhaas/polecat-platform/'
APP='repos/kevinrhaas/chicago/'
TICKET='repos/kevinrhaas/chicago-tickets/contents/T-2250-2499/T-2374-match-cobweb-castle-to-its-pictures.md'
OLD_RUN=41746386858
HOSTED=[41752421848,41752413970]
REQUEST={'ref':REF,'inputs':{'app':'chicago','target_ticket':'T-2374','resume_pr':'1690','slice':'1','slices':'1','lane':LANE,'max_turns':'400'}}
WORKFLOW='.github/workflows/steward-improve.yml'
W=Path('/tmp/wolf-poster-source-20261103/chicago/4d')
PATHS=['assets/gltf/cobweb_castle__log_1820.glb','assets/web/cobweb_castle__log_1820.glb','assets/manifest.json','assets/manifest.web.json','generators/archetypes/log_dwelling.py','generators/archetypes/log_dwelling_params.py','generators/archetypes/facade_openings.py','generators/common/openings.py','generators/common/logwork.py','data/structures/cobweb_castle.json','data/structure_grades.json','docs/LIBERTIES.md']

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(name,obj):
 tmp=P/(name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,P/name)
def api(path,missing=False):
 suffix = '&' if '?' in path else '?'
 r=subprocess.run(['gh','api','-H','Cache-Control: no-cache','-H','Pragma: no-cache',path+suffix+'_='+str(time.time_ns())],capture_output=True,timeout=45)
 if r.returncode:
  if missing and b'HTTP 404' in r.stderr:return None
  raise RuntimeError(r.stderr.decode()[:1500])
 return json.loads(r.stdout)
def emit(kind,**kw):print(json.dumps({'utc':now(),'event':kind,**kw}),flush=True)
def fields(data):
 front=data.decode().split('---',2)[1]
 return {line.split(':',1)[0]:line.split(':',1)[1].strip() for line in front.splitlines() if ':'in line}
def current_ticket():
 tip=api('repos/kevinrhaas/chicago-tickets/git/ref/heads/main')['object']['sha'];obj=api(TICKET+'?ref='+tip);data=base64.b64decode(obj['content']);assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==obj['sha'];return obj,data,fields(data)
def lap():
 r=subprocess.run(['node','tools/ticket.mjs','lap','1690','--status'],cwd=W,capture_output=True,timeout=120)
 row={'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()}
 assert r.returncode==0 and row['stdout'].startswith(('free ','stale ')),row
 return row

def active_runs():
 rows=[]
 for status in ['in_progress','queued','waiting','pending','requested']:
  page=1
  while True:
   xs=api(PLATFORM+f'actions/runs?status={status}&per_page=100&page={page}')['workflow_runs'];rows.extend(xs)
   if len(xs)<100:break
   page+=1;assert page<10,'Unexpected active-run pagination; do not guess'
 return list({r['id']:r for r in rows}.values())
def hosted(require_green):
 rows=[]
 for rid in HOSTED:
  r=api(PLATFORM+'actions/runs/'+str(rid));assert r['head_sha']==FEATURE
  row={k:r[k] for k in ['id','status','conclusion','head_sha','event','head_branch']};rows.append(row)
  if require_green:assert row['status']=='completed' and row['conclusion']=='success',row
 return rows

def source_state():
 dev=api(APP+'git/ref/heads/dev')['object']['sha'];commit=api(APP+'git/commits/'+dev)
 def one(path):
  row=api(APP+'contents/chicago/4d/'+path+'?ref='+dev)
  return {'path':path,'git_blob':row['sha'],'size':row['size']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:checks=list(pool.map(one,PATHS))
 return {'dev':dev,'tree':commit['tree']['sha'],'guarded_paths':checks}

def audit(require_green=False):
 emit('preflight-start',hosted_green_required=require_green)
 assert api(PLATFORM+'git/ref/heads/'+REF)['object']['sha']==FEATURE,'Feature branch moved'
 workflow=api(PLATFORM+'contents/'+WORKFLOW+'?ref='+FEATURE)
 workflow_bytes=base64.b64decode(workflow['content'])
 assert b'resume_pr:' in workflow_bytes and b'timeout-minutes: 150' in workflow_bytes
 r=api(APP+'pulls/1690');assert r['state']=='open'and r['head']['sha']==HEAD and r['head']['ref']=='steward/t2374-cobweb-front-apertures'and r['base']['ref']=='dev'
 assert 'resume'in[x['name']for x in r['labels']]
 old=api(PLATFORM+'actions/runs/'+str(OLD_RUN));assert old['status']=='completed' and old['conclusion']=='failure'
 t,data,f=current_ticket();assert f.get('state')=='open'and f.get('claimed_run')=='null'and f.get('claimed_by')=='null'and f.get('pr')=='null',f
 assert b'## Exact existing-PR recovery' in data and b'UNQUALIFIED working-source plus raw log/hash checkpoints' in data
 matches=[]
 for page in range(1,11):
  prs=api(APP+f'pulls?state=open&per_page=100&page={page}')
  for pr in prs:
   if re.search(r'(?i)(?:T[-_ ]?2374|t2374)',pr['title']+' '+pr['head']['ref']+' '+(pr.get('body')or'')):matches.append(pr['number'])
  if len(prs)<100:break
 else:raise AssertionError('Open PR pagination incomplete')
 assert set(matches)=={1690},matches
 active=active_runs();conflicts=[{k:x[k]for k in ['id','display_title','status','head_sha']}for x in active if LANE in x['display_title']or re.search(r'(?i)T-?2374',x['display_title'])]
 assert not conflicts,conflicts
 before=api(PLATFORM+'actions/workflows/steward-improve.yml/runs?event=workflow_dispatch&per_page=100')['workflow_runs']
 laps=lap();sources=source_state();ci=hosted(require_green)
 result={'utc':now(),'feature_sha':FEATURE,'workflow_blob':workflow['sha'],'workflow_sha256':hashlib.sha256(workflow_bytes).hexdigest(),'pr':1690,'pr_head':HEAD,'pr_branch':r['head']['ref'],'ticket_blob':t['sha'],'ticket_fields':f,'ticket_body_sha256':hashlib.sha256(data).hexdigest(),'old_run_completed_failure':True,'only_matching_open_pr':matches,'no_active_target_lane':True,'active_run_count':len(active),'lap':laps,'source':sources,'hosted':ci,'prior_dispatch_run_ids':[x['id']for x in before]}
 emit('preflight-passed',dev=sources['dev'],hosted=ci)
 return result

def prepare():
 assert not(P/'DISPATCH-ATTEMPT.json').exists(),'Already attempted: do not prepare another dispatch'
 dump('REQUEST.json',REQUEST);a=audit(False);dump('PREPARED.json',a)
 dump('PREPARED-REQUEST-HASH.json',{'sha256':hashlib.sha256((P/'REQUEST.json').read_bytes()).hexdigest()})
 emit('prepared-no-dispatch',request=REQUEST,authorization_file_exists=(P/'ROOT-GO.json').exists())

def dispatch():
 assert not(P/'DISPATCH-ATTEMPT.json').exists(),'Dispatch already attempted; inspect response/run, never retry blindly'
 authorization=json.loads((P/'ROOT-GO.json').read_text());request_bytes=(P/'REQUEST.json').read_bytes();reqhash=hashlib.sha256(request_bytes).hexdigest()
 assert authorization.get('authorized')is True and authorization.get('feature_sha')==FEATURE and authorization.get('request_sha256')==reqhash,'Explicit matching root authorization required'
 assert json.loads(request_bytes)==REQUEST
 expected=json.loads((P/'PREPARED.json').read_text());fresh=audit(True)
 assert fresh['source']==expected['source'],'dev/source tree moved since preparation: stop, report and re-prepare with root review'
 assert fresh['workflow_sha256']==expected['workflow_sha256'] and fresh['ticket_blob']==expected['ticket_blob']
 dump('FRESH-PREFLIGHT.json',fresh)
 # The final remote guards run after source/CI reads and immediately before the one POST.
 t,data,f=current_ticket();assert t['sha']==fresh['ticket_blob'] and f['state']=='open'and f['claimed_run']=='null'
 assert api(APP+'pulls/1690')['head']['sha']==HEAD
 assert api(PLATFORM+'git/ref/heads/'+REF)['object']['sha']==FEATURE
 assert api(APP+'git/ref/heads/dev')['object']['sha']==fresh['source']['dev']
 assert not[x for x in active_runs()if LANE in x['display_title']or re.search(r'(?i)T-?2374',x['display_title'])]
 final_lap=lap()
 attempt={'utc':now(),'feature':FEATURE,'request':REQUEST,'request_sha256':reqhash,'final_lap':final_lap,'state':'ATTEMPT_RESERVED_BEFORE_POST_NO_AUTOMATIC_RETRY'}
 with (P/'DISPATCH-ATTEMPT.json').open('x')as out:out.write(json.dumps(attempt,indent=2)+'\n')
 emit('dispatch-single-post',request=REQUEST)
 r=subprocess.run(['gh','api','--method','POST',PLATFORM+'actions/workflows/steward-improve.yml/dispatches','--input',str(P/'REQUEST.json')],capture_output=True,timeout=45)
 dump('DISPATCH-RESPONSE.json',{'utc':now(),'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'request_sha256':reqhash})
 assert r.returncode==0,'Dispatch response uncertain/failure: inspect exact remote runs, never duplicate POST'
 prior=set(fresh['prior_dispatch_run_ids'])
 for attempt in range(16):
  runs=api(PLATFORM+'actions/workflows/steward-improve.yml/runs?event=workflow_dispatch&per_page=100')['workflow_runs']
  matches=[x for x in runs if x['id']not in prior and x['head_sha']==FEATURE and LANE in x['display_title']and x['head_branch']==REF]
  assert len(matches)<=1,'Multiple matching new runs: stop for ownership review'
  if matches:
   actual=matches[0];dump('ACTUAL-RUN.json',actual);emit('exact-run-discovered',run=actual['id'],url=actual['html_url']);return
  emit('await-run-discovery',iteration=attempt+1)
  time.sleep(5)
 raise RuntimeError('No exact run discovered; POST NOT repeated, inspect remote')

def monitor(snapshots,interval):
 actual=json.loads((P/'ACTUAL-RUN.json').read_text());rid=actual['id'];url=actual['html_url'];rows=[]
 assert 1<=snapshots<=15 and 1<=interval<=45
 for i in range(snapshots):
  r=api(PLATFORM+'actions/runs/'+str(rid));assert r['head_sha']==FEATURE and r['head_branch']==REF and LANE in r['display_title']
  jobs=api(PLATFORM+'actions/runs/'+str(rid)+'/jobs')['jobs'];target=next((j for j in jobs if j['name']=='targeted-chicago'),None)
  t,data,f=current_ticket();pr=api(APP+'pulls/1690')
  our=f.get('state')=='claimed'and f.get('claimed_run')==url
  mismatch=f.get('state')=='claimed'and not our
  row={'utc':now(),'run':rid,'run_url':url,'feature_sha':r['head_sha'],'run_status':r['status'],'run_conclusion':r['conclusion'],'target_job':None if not target else {k:target[k]for k in ['id','status','conclusion','labels']},'active_step':None if not target else next((s['name']for s in target['steps']if s['status']=='in_progress'),None),'ticket_blob':t['sha'],'ticket_fields':f,'our_exact_claim':our,'ownership_mismatch':mismatch,'existing_pr_head':pr['head']['sha'],'existing_pr_state':pr['state'],'read_only':True}
  if target:assert 'ubuntu-26.04'in target['labels'],target['labels']
  rows.append(row);dump('MONITOR-LATEST.json',row);dump('MONITOR-SNAPSHOTS.json',rows);emit('claim-monitor',**row)
  if our or mismatch or r['status']=='completed':break
  if i+1<snapshots:time.sleep(interval)
 dump('MONITOR-CLOSED.json',{'utc':now(),'read_only':True,'snapshots':len(rows),'latest':rows[-1]})

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','dispatch','monitor'],nargs='?',default='prepare');p.add_argument('--snapshots',type=int,default=10);p.add_argument('--interval',type=int,default=30);a=p.parse_args()
 if a.mode=='prepare':prepare()
 elif a.mode=='dispatch':dispatch()
 else:monitor(a.snapshots,a.interval)
