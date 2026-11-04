"""Owner-safe NEW T-2383 work; default READ-ONLY prepare. No automatic retry POST.
Dispatch is unavailable until a separate exact-hash root GO, public actual GO and
fresh normal claim/PR/job/source/feature-CI guards all pass. No source/ticket edits.
"""
from pathlib import Path
import argparse,base64,concurrent.futures,datetime,hashlib,json,os,re,subprocess,time,urllib.request
P=Path(__file__).resolve().parent
FEATURE='7b427d130a2cca6ed82c183c74605b965aee1d4e'
REF='steward/chicago-native-exact-ticket-20261103'
LANE='sauganash-stacks-native-20261104'
PLATFORM='repos/kevinrhaas/polecat-platform/';APP='repos/kevinrhaas/chicago/'
TICKET_PATH='T-2250-2499/T-2383-match-the-sauganash-hotel-to-its-pictures.md'
HOSTED=[41768392703,41768399310]
BASE_BLOBS={'data/structures/sauganash_hotel.json': '99ca2d0cc0af293d7f989bda0020314a7f11c30c', 'generators/archetypes/frame_tavern.py': '5f4d4fbc127f53929bd6dedc6456b42fb500ed9f', 'generators/archetypes/frame_tavern_params.py': '3c712f260ee685a1476349bb1ef535754dc40600', 'data/reference_views/sauganash_hotel/andreas-1884.json': '136533e92b091c7ca196d6794c8bfafd545c7f99', 'data/reference_views/sauganash_hotel/andreas-1884.match.json': '483370fc6f770ec929c1b05f5e75c42e6ed71626', 'docs/RESEARCH/photo-match/sauganash_hotel/andreas-1884-side-by-side.jpg': '59806b37578e79eebf59b6f51ceb28e657356ec6', 'data/sources/andreas_1884_sauganash_hotel_plate.json': 'c5e90833e4d6bc93e80eceec7719ee65bc0cdae2'}
AUTH_PREFIX='evidence/sauganash-2026-11-04/stacks-native-execution-authorization/'
FEATURE_GUARDS={'.github/steward/salvage.sh':'b675d2403cae2048da37f1941e5eed65f2b268a2a5d332a46e49a228cced65af','.github/steward/run-record.mjs':'f96017acc1e12f6d414da78f2d4e792aec02a458891ca6f25ce41f4db2dba322','.github/steward/test-salvage.sh':'e71c0fdd4909f0f3098013a61b53fbdae1eddf28b50705b5ff8b29a7b6d8e27c'}
REQUEST={'ref':REF,'inputs':{'app':'chicago','target_ticket':'T-2383','slice':'1','slices':'1','lane':LANE,'max_turns':'400'}}
MARKER='## Sauganash stacks native handoff — 2026-11-04'
PATHS=['data/structures/sauganash_hotel.json', 'generators/archetypes/frame_tavern.py', 'generators/archetypes/frame_tavern_params.py', 'data/reference_views/sauganash_hotel/andreas-1884.json', 'data/reference_views/sauganash_hotel/andreas-1884.match.json', 'docs/RESEARCH/photo-match/sauganash_hotel/andreas-1884-side-by-side.jpg', 'data/sources/andreas_1884_sauganash_hotel_plate.json', 'assets/gltf/sauganash_hotel__frame_1831.glb', 'assets/web/sauganash_hotel__frame_1831.glb', 'data/structures/green_tree_tavern.json', 'assets/gltf/green_tree_tavern__frame_1833.glb', 'assets/web/green_tree_tavern__frame_1833.glb', 'data/structures/philo_carpenter_log_shop.json', 'assets/gltf/philo_carpenter_log_shop__log_1832.glb', 'assets/web/philo_carpenter_log_shop__log_1832.glb', 'generators/archetypes/fort_structure.py', 'generators/archetypes/fort_structure_params.py', 'data/structures/fort_dearborn_blockhouse.json', 'assets/gltf/fort_dearborn_blockhouse__log_1816.glb', 'assets/web/fort_dearborn_blockhouse__log_1816.glb', 'data/structures/first_fort_dearborn_magazine.json', 'generators/emit.py', 'generators/blender.pin', 'generators/mesh_inputs.py', 'generators/code_inputs.py', 'generators/common/mesh.py', 'data/structure_grades.json', 'docs/LIBERTIES.md', 'renderers/web/js/main.js', 'renderers/web/js/buildings.js', 'renderers/web/js/scene-loader.js', 'data/reference_views/philo_carpenter_log_shop/andreas-1884.json', 'data/reference_views/philo_carpenter_log_shop/andreas-1884.match.json', 'data/reference_views/philo_carpenter_log_shop/kurz-allison-1893-panel14.json', 'data/reference_views/philo_carpenter_log_shop/kurz-allison-1893-panel14.match.json', 'data/reference_views/philo_carpenter_log_shop/trowbridge-1902.json', 'data/reference_views/philo_carpenter_log_shop/trowbridge-1902.match.json']
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(n,d):
 t=P/(n+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,P/n)
def api(p,missing=False):
 r=subprocess.run(['gh','api','-H','Cache-Control: no-cache','-H','Pragma: no-cache',p+('&'if'?'in p else'?')+'_='+str(time.time_ns())],capture_output=True,timeout=45)
 if r.returncode:
  if missing and b'HTTP 404'in r.stderr:return None
  raise RuntimeError(r.stderr.decode()[:1500])
 return json.loads(r.stdout)
def blob(p,ref,repo=APP):
 d=api(repo+'contents/'+p+'?ref='+ref)
 if d.get('content'):
  b=base64.b64decode(d['content']);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['sha'];return d,b
 return d,None

def ticket():
 h=api('repos/kevinrhaas/chicago-tickets/git/ref/heads/main')['object']['sha'];d,b=blob(TICKET_PATH,h,'repos/kevinrhaas/chicago-tickets/');assert b is not None
 f={l.split(':',1)[0]:l.split(':',1)[1].strip()for l in b.decode().split('---',2)[1].splitlines()if':'in l};return d,b,f

def active_runs():
 out=[]
 for status in ['in_progress','queued','waiting','pending','requested']:
  for page in range(1,11):
   xs=api(PLATFORM+f'actions/runs?status={status}&per_page=100&page={page}')['workflow_runs'];out.extend(xs)
   if len(xs)<100:break
  else:raise RuntimeError('Active-run pagination incomplete')
 return list({x['id']:x for x in out}.values())
def open_target_prs():
 out=[]
 for page in range(1,11):
  rows=api(APP+f'pulls?state=open&per_page=100&page={page}')
  for p in rows:
   if re.search(r'(?i)T[-_ ]?2383\b',p['title']+' '+p['head']['ref']+' '+(p.get('body')or'')):out.append({'number':p['number'],'title':p['title'],'head':p['head']['sha'],'ref':p['head']['ref']})
  if len(rows)<100:return out
 raise RuntimeError('Open-PR pagination incomplete')
def source():
 h=api(APP+'git/ref/heads/dev')['object']['sha'];c=api(APP+'git/commits/'+h)
 def one(p):
  d,_=blob('chicago/4d/'+p,h);return {'path':p,'git_blob':d['sha'],'bytes':d['size']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(one,PATHS))
 manifests={}
 for n in ['manifest.json','manifest.web.json','manifest.versions.json']:
  _,b=blob('chicago/4d/assets/'+n,h);assert b is not None;manifests[n]=json.loads(b)
 family={}
 for a in ['fort_structure','outbuilding','frame_tavern']:
  defaults={k:v for k,v in manifests['manifest.json']['assets'].items()if v.get('archetype')==a};variants={k:v for k,v in manifests['manifest.versions.json']['assets'].items()if v.get('archetype')==a}
  family[a]={'defaults':defaults,'variants':variants,'web_master_bindings':{k:manifests['manifest.web.json']['masters'][k]for k in defaults}}
 return {'head':h,'tree':c['tree']['sha'],'paths':rows,'families':family,'scope':'Read-only current baseline; never a new native execution claim.'}
def feature():
 assert api(PLATFORM+'git/ref/heads/'+REF)['object']['sha']==FEATURE,'Feature branch moved'
 rows=[]
 for p,want in FEATURE_GUARDS.items():
  d,b=blob(p,FEATURE,PLATFORM);assert sha(b)==want,(p,sha(b),want);rows.append({'path':p,'blob':d['sha'],'sha256':want})
 d,b=blob('.github/workflows/steward-improve.yml',FEATURE,PLATFORM);assert b'target_ticket:'in b and b'ubuntu-26.04'in b and b'resume_pr:'in b and b'timeout-minutes: 150'in b
 hosted=[]
 for rid in HOSTED:
  r=api(PLATFORM+'actions/runs/'+str(rid));assert r['head_sha']==FEATURE;hosted.append({k:r[k]for k in ['id','status','conclusion','head_sha']})
 return {'owner_guards':rows,'workflow_blob':d['sha'],'workflow_sha256':sha(b),'hosted':hosted}
def audit(strict=False):
 ftr=feature();t,b,f=ticket();prs=open_target_prs();runs=active_runs();conflicts=[{k:x[k]for k in ['id','display_title','status','head_sha']}for x in runs if LANE in x['display_title']or re.search(r'(?i)T[-_ ]?2383\b',x['display_title'])];src=source();by={r['path']:r['git_blob']for r in src['paths']};block=[]
 if any(f.get(k)!='null'for k in ['claimed_by','claimed_run','claimed_at','pr'])or f.get('state')!='open':block.append('OriginalT2383 not normally OPEN/free')
 if prs:block.append('OpenPR mentions T2383; inspect association before any work')
 if conflicts:block.append('Live T2383/unique lane run')
 if any(by.get(p)!=h for p,h in BASE_BLOBS.items()):block.append('Currentdev approved Sauganash record/producer/camera/source baseline moved; rebind/review')
 fam=src['families']['frame_tavern'];defaults=fam['defaults'];variants=fam['variants']
 if len(defaults)!=23 or len(variants)!=2:block.append('Fresh frame inventory is not23defaults+2variants; inspect actual scope')
 gt='green_tree_tavern__frame_1833.glb'
 if defaults.get(gt,{}).get('inputs_sha256')!='712cb7c9530c5c6d6fba6b83c7d2b6e2e19d49f78e94da7ebf688ee3937c6974' or fam['web_master_bindings'].get(gt)!='f213818f5a686d31bfbb07217233a7021c514be64b841035d3c29996a380807b':block.append('MergedGT712cb/f213 preservation guard moved')
 if any(v.get('structure_id')=='sauganash_hotel'for v in variants.values()):block.append('Sauganash variant now exists; re-inventory affected scope')
 if MARKER.encode()not in b:block.append('Reviewed public handoff not yet attached to original ticket')
 if not all(x['status']=='completed'and x['conclusion']=='success'for x in ftr['hosted']):block.append('Exact owner-safe feature CI not green')
 if strict:assert not block,block
 return {'utc':now(),'feature':FEATURE,'feature_guards':ftr,'request':REQUEST,'ticket_blob':t['sha'],'ticket_fields':f,'ticket_body_sha256':sha(b),'open_target_prs':prs,'live_target_runs':conflicts,'source':src,'blockers':block,'dispatch_allowed':not block,'read_only':True}

def verify_public_go(go_bytes):
 receipt=json.loads((P/'PUBLIC-GO-RECEIPT.json').read_bytes());assert receipt['prefix']==AUTH_PREFIX
 assert receipt['files']['ROOT-GO.json']['sha256']==sha(go_bytes)
 url='https://raw.githubusercontent.com/kevinrhaas/chicago-evidence/'+receipt['commit']+'/'+AUTH_PREFIX+'ROOT-GO.json'
 with urllib.request.urlopen(url,timeout=30)as r:raw=r.read()
 assert raw==go_bytes,'Exact actual rootGO must be PUBLIC before any POST'
 # The stable handoff locator must also resolve to this actual GO, never a false template.
 stable='https://raw.githubusercontent.com/kevinrhaas/chicago-evidence/main/'+AUTH_PREFIX+'ROOT-GO.json'
 with urllib.request.urlopen(stable+'?_='+str(time.time_ns()),timeout=30)as r:assert r.read()==go_bytes
 proof={'utc':now(),'public_commit':receipt['commit'],'immutable_url':url,'stable_url':stable,'root_go_sha256':sha(go_bytes),'actual_GO_public_BEFORE_POST':True}
 dump('PUBLIC-GO-VERIFIED.json',proof);return proof

def prepare():
 assert not(P/'DISPATCH-ATTEMPT.json').exists(),'Already attempted; inspect instead of duplicating'
 dump('REQUEST.json',REQUEST);r=audit();dump('PREPARED.json',r);dump('ARTIFACT-HASHES.json',{'request':sha((P/'REQUEST.json').read_bytes()),'patch':sha((P/'UNQUALIFIED-DATA-ONLY.patch').read_bytes()),'handoff':sha((P/'HANDOFF.md').read_bytes()),'controller':sha(Path(__file__).read_bytes())});print(json.dumps({'prepared':True,'no_dispatch':True,'blockers':r['blockers']}),flush=True)
def dispatch():
 assert not(P/'DISPATCH-ATTEMPT.json').exists(),'No blind retry of POST'
 go_bytes=(P/'ROOT-GO.json').read_bytes();go=json.loads(go_bytes);expected=json.loads((P/'ARTIFACT-HASHES.json').read_bytes());actual={'request':sha((P/'REQUEST.json').read_bytes()),'patch':sha((P/'UNQUALIFIED-DATA-ONLY.patch').read_bytes()),'handoff':sha((P/'HANDOFF.md').read_bytes()),'controller':sha(Path(__file__).read_bytes())};assert actual==expected and go.get('authorized')is True and go.get('feature')==FEATURE and go.get('artifacts')==actual,'Separate exact reviewed root GO required'
 public_go=verify_public_go(go_bytes)
 assert json.loads((P/'REQUEST.json').read_bytes())==REQUEST and'resume_pr'not in REQUEST['inputs']and'model'not in REQUEST['inputs']
 old=json.loads((P/'PREPARED.json').read_bytes());fresh=audit(True);assert old['source']==fresh['source']and old['ticket_blob']==fresh['ticket_blob'],'Current source/ticket moved: prepare+review again'
 assert go.get('prepared_sha256')==sha((P/'PREPARED.json').read_bytes());dump('FRESH-PREFLIGHT.json',fresh)
 before=api(PLATFORM+'actions/workflows/steward-improve.yml/runs?event=workflow_dispatch&per_page=100')['workflow_runs'];prior={x['id']for x in before}
 # Recheck ownership and base immediately before the ONE POST.
 t,b,f=ticket();assert t['sha']==fresh['ticket_blob']and f.get('state')=='open'and f.get('claimed_run')=='null'
 assert not open_target_prs();assert not[x for x in active_runs()if LANE in x['display_title']or re.search(r'(?i)T[-_ ]?2383\b',x['display_title'])]
 assert api(APP+'git/ref/heads/dev')['object']['sha']==fresh['source']['head'];assert api(PLATFORM+'git/ref/heads/'+REF)['object']['sha']==FEATURE
 with(P/'DISPATCH-ATTEMPT.json').open('x')as out:json.dump({'utc':now(),'request':REQUEST,'feature':FEATURE,'public_GO':public_go,'state':'RESERVED_BEFORE_SINGLE_POST_NO_RETRY'},out,indent=2)
 r=subprocess.run(['gh','api','--method','POST',PLATFORM+'actions/workflows/steward-improve.yml/dispatches','--input',str(P/'REQUEST.json')],capture_output=True,timeout=45);dump('DISPATCH-RESPONSE.json',{'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()});assert r.returncode==0,'Uncertain/failed POST: inspect remote, NEVER repeat blindly'
 for i in range(16):
  rows=api(PLATFORM+'actions/workflows/steward-improve.yml/runs?event=workflow_dispatch&per_page=100')['workflow_runs'];matches=[x for x in rows if x['id']not in prior and x['head_sha']==FEATURE and x['head_branch']==REF and LANE in x['display_title']];assert len(matches)<=1
  if matches:dump('ACTUAL-RUN.json',matches[0]);print(matches[0]['html_url'],flush=True);return
  time.sleep(5)
 raise RuntimeError('POST accepted but exactrun not discovered; inspect, do not retry')
def monitor(snapshots=10,interval=30):
 actual=json.loads((P/'ACTUAL-RUN.json').read_bytes());rid=actual['id'];url=actual['html_url'];rows=[];assert 1<=snapshots<=15 and 1<=interval<=45
 for i in range(snapshots):
  r=api(PLATFORM+'actions/runs/'+str(rid));assert r['head_sha']==FEATURE and r['head_branch']==REF and LANE in r['display_title']
  jobs=api(PLATFORM+'actions/runs/'+str(rid)+'/jobs')['jobs'];job=next((x for x in jobs if x['name']=='targeted-chicago'),None)
  if job:assert 'ubuntu-26.04'in job['labels']
  t,b,f=ticket();ours=f.get('state')=='claimed'and f.get('claimed_run')==url;mismatch=f.get('state')=='claimed'and not ours
  row={'utc':now(),'run':rid,'run_url':url,'feature':FEATURE,'status':r['status'],'conclusion':r['conclusion'],'target_job':None if job is None else{k:job[k]for k in ['id','status','conclusion','labels']},'ticket_blob':t['sha'],'ticket_fields':f,'our_exact_claim':ours,'ownership_mismatch':mismatch,'read_only':True};rows.append(row);dump('MONITOR-LATEST.json',row);dump('MONITOR-HISTORY.json',rows)
  if ours or mismatch or r['status']=='completed':break
  if i+1<snapshots:time.sleep(interval)
 dump('MONITOR-CLOSED.json',{'read_only':True,'latest':rows[-1],'samples':len(rows)})
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','dispatch','monitor'],default='prepare',nargs='?');a.add_argument('--snapshots',type=int,default=10);a.add_argument('--interval',type=int,default=30);x=a.parse_args()
 if x.mode=='prepare':prepare()
 elif x.mode=='dispatch':dispatch()
 else:monitor(x.snapshots,x.interval)
