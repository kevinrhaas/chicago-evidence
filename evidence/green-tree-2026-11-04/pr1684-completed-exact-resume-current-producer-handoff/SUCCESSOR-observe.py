from pathlib import Path
import json,subprocess,time,datetime,concurrent.futures,base64,hashlib,zipfile
P=Path(__file__).resolve().parent;FEATURE='b37fdeca6b74d8e3c70945a75687140c0718f549'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(n,d):
 q=P/n;q.parent.mkdir(exist_ok=True,parents=True);t=q.with_suffix(q.suffix+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');t.replace(q)
def api(path):return json.loads(subprocess.check_output(['gh','api','-H','Cache-Control: no-cache',path+('&'if'?'in path else'?')+'_='+str(time.time_ns())],timeout=45))
def snapshot(t):
 try:
  r=api('repos/kevinrhaas/polecat-platform/actions/runs/'+str(t['run']));assert r['head_sha']==t.get('expected_feature',FEATURE)
  jobs=api('repos/kevinrhaas/polecat-platform/actions/runs/'+str(t['run'])+'/jobs')['jobs'];j=next((x for x in jobs if x['name']=='targeted-chicago'),None)
  if j:assert 'ubuntu-26.04'in j['labels']
  tip=api('repos/kevinrhaas/chicago-tickets/git/ref/heads/main')['object']['sha'];d=api('repos/kevinrhaas/chicago-tickets/contents/'+t['ticket_file']+'?ref='+tip);b=base64.b64decode(d['content']);f={l.split(':',1)[0]:l.split(':',1)[1].strip()for l in b.decode().split('---',2)[1].splitlines()if':'in l}
  row={**t,'utc':now(),'status':r['status'],'conclusion':r['conclusion'],'feature':r['head_sha'],'job':None if not j else {k:j[k]for k in ['id','status','conclusion','labels']},'active_step':None if not j else next((s['name']for s in j['steps']if s['status']=='in_progress'),None),'ticket_blob':d['sha'],'ticket_fields':f,'our_exact_claim':f.get('state')=='claimed'and f.get('claimed_run')==r['html_url'],'read_only':True}
  if t.get('pr'):
   pr=api('repos/kevinrhaas/chicago/pulls/'+str(t['pr']));row['pr_state']={k:pr.get(k)for k in ['state','merged','draft','mergeable_state']};row['pr_head']=pr['head']['sha']
  return row
 except Exception as e:return{**t,'utc':now(),'read_error':repr(e),'not_a_worker_failure':True}
def salvage(t):
 out=P/'completed-runs'/str(t['run']);receipt=out/'ARTIFACT-VERIFIED.json'
 if receipt.exists():return json.loads(receipt.read_text())
 arts=api('repos/kevinrhaas/polecat-platform/actions/runs/'+str(t['run'])+'/artifacts')['artifacts'];a=next((x for x in arts if x['name']=='steward-stream-'+str(t['run'])and not x['expired']),None)
 if not a:return None
 out.mkdir(exist_ok=True,parents=True);raw=subprocess.check_output(['gh','api','repos/kevinrhaas/polecat-platform/actions/artifacts/'+str(a['id'])+'/zip'],timeout=120);sha=hashlib.sha256(raw).hexdigest();assert a['digest']=='sha256:'+sha;(out/'raw.zip').write_bytes(raw);dump(str(out.relative_to(P)/'ARTIFACT-IDENTITY.json'),a)
 with zipfile.ZipFile(out/'raw.zip')as z:
  for n in z.namelist():assert not Path(n).is_absolute()and'..'not in Path(n).parts;assert z.getinfo(n).file_size<100000000
  z.extractall(out/'raw')
 d={'run':t['run'],'sha256':sha,'digest_verified':True,'bytes':len(raw),'actual_record':json.loads((out/'raw/steward-record.json').read_text())};dump(str(receipt.relative_to(P)),d);return d
samples=[];events=[];previous={}
for i in range(180):
 tasks=json.loads((P/'TASKS.json').read_text())
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:rows=list(ex.map(snapshot,tasks))
 if i%5==0:
  try:
   prs=api('repos/kevinrhaas/chicago/pulls?state=open&sort=updated&direction=desc&per_page=100')
   for row in rows:
    hits=[{'number':x['number'],'head':x['head']['sha'],'title':x['title'],'branch':x['head']['ref']}for x in prs if row['ticket'].lower()in(x['title']+' '+x['head']['ref']).lower()or row['ticket'].lower().replace('-','')in x['head']['ref'].lower()];row['matching_open_prs']=hits
  except Exception as e:events.append({'utc':now(),'read_error':repr(e)})
 for row in rows:
  if row.get('status')=='completed':
   try:row['completed_artifact']=salvage(row)
   except Exception as e:row['artifact_read_error']=repr(e)
  sig=(row.get('status'),row.get('conclusion'),row.get('active_step'),row.get('ticket_blob'),row.get('pr_head'),row.get('read_error'))
  if sig!=previous.get(row['ticket']):events.append(row);print(json.dumps(row),flush=True);previous[row['ticket']]=sig
 snap={'utc':now(),'sample':i+1,'rows':rows};samples.append(snap);dump('LATEST.json',snap);dump('SNAPSHOTS.json',samples);dump('EVENTS.json',events)
 if all(r.get('status')=='completed'and r.get('completed_artifact')for r in rows):break
 if i<179:time.sleep(55)
dump('CLOSED.json',{'utc':now(),'samples':len(samples),'read_only':True,'latest':samples[-1]})
