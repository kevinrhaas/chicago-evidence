from pathlib import Path
import json,subprocess,time,datetime,base64,hashlib,zipfile
P=Path(__file__).parent;DONE={};rows=[];last=None
EXPECTED={41755835659:{'head':'777f69cd6a45e1567ad52320bebf00fea910fc80','job':126331614416,'name':'improve'},41755970879:{'head':'b37fdeca6b74d8e3c70945a75687140c0718f549','job':126332042871,'name':'targeted-chicago'}}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(n,d):p=P/(n+'.tmp');p.write_text(json.dumps(d,indent=2)+'\n');p.replace(P/n)
def api(p,missing=False):
 r=subprocess.run(['gh','api','-H','Cache-Control: no-cache',p+('&'if'?'in p else'?')+'_='+str(time.time_ns())],capture_output=True,timeout=40)
 if r.returncode:
  if missing and b'HTTP 404'in r.stderr:return None
  raise RuntimeError(r.stderr.decode()[:500])
 return json.loads(r.stdout)
def salvage(rid):
 if rid in DONE:return DONE[rid]
 xs=api(f'repos/kevinrhaas/polecat-platform/actions/runs/{rid}/artifacts')['artifacts'];xs=[x for x in xs if x['name']==f'steward-stream-{rid}'and not x['expired']]
 if not xs:return None
 assert len(xs)==1;a=xs[0];R=P/str(rid);R.mkdir(exist_ok=True);b=subprocess.check_output(['gh','api',f"repos/kevinrhaas/polecat-platform/actions/artifacts/{a['id']}/zip"],timeout=120);digest=hashlib.sha256(b).hexdigest();assert a['digest']=='sha256:'+digest;(R/'raw.zip').write_bytes(b)
 with zipfile.ZipFile(R/'raw.zip')as z:
  for n in z.namelist():assert not Path(n).is_absolute()and'..'not in Path(n).parts and z.getinfo(n).file_size<100000000
  z.extractall(R/'raw')
 (R/'ARTIFACT-IDENTITY.json').write_text(json.dumps(a,indent=2));d={'id':a['id'],'run':rid,'sha256':digest,'archive_bytes':len(b),'digest_verified':True,'actual_outcome':None}
 q=R/'raw/steward-record.json'
 if q.exists():d['actual_outcome']=json.load(open(q))
 (R/'ARTIFACT-VERIFIED.json').write_text(json.dumps(d,indent=2));DONE[rid]=d;return d
for i in range(60):
 sample={'utc':now(),'sample':i+1,'runs':[],'lap':None,'pr':None,'ticket':None,'read_errors':[],'source_or_claim_mutations':False}
 for rid,e in EXPECTED.items():
  try:
   j=api(f'repos/kevinrhaas/polecat-platform/actions/jobs/{e['job']}');assert j['run_id']==rid and j['head_sha']==e['head']and j['name']==e['name'];r={'run':rid,'job':e['job'],'head':j['head_sha'],'status':j['status'],'conclusion':j['conclusion'],'labels':j['labels'],'active_step':next((s['name']for s in j['steps']if s['status']=='in_progress'),None)}
   if rid==41755970879:assert'ubuntu-26.04'in j['labels']
   if r['status']=='completed':r['artifact']=salvage(rid)
   sample['runs'].append(r)
  except Exception as ex:sample['read_errors'].append({'run':rid,'error':repr(ex)})
 try:
  marker=api('repos/kevinrhaas/chicago/git/ref/heads/lap/pr-1687',missing=True)
  if marker:
   c=api('repos/kevinrhaas/chicago/git/commits/'+marker['object']['sha']);sample['lap']={'sha':marker['object']['sha'],'message':c['message'],'date':c['committer']['date']}
  else:sample['lap']={'free':True}
  pr=api('repos/kevinrhaas/chicago/pulls/1687');sample['pr']={'head':pr['head']['sha'],'state':pr['state'],'merged':pr['merged'],'merge_sha':pr['merge_commit_sha'],'mergeable_state':pr['mergeable_state']}
  t=api('repos/kevinrhaas/chicago-tickets/contents/T-2250-2499/T-2388-match-the-second-fort-dearborn-1835-to-its-pictu.md');b=base64.b64decode(t['content']);sample['ticket']={'blob':t['sha'],'fields':{s.split(':',1)[0]:s.split(':',1)[1].strip()for s in b.decode().split('---',2)[1].splitlines()if':'in s}}
 except Exception as ex:sample['read_errors'].append({'ownership_read':repr(ex)})
 rows.append(sample);dump('LATEST.json',sample);dump('SNAPSHOTS.json',rows);sig=json.dumps({k:sample[k]for k in ['runs','lap','pr','ticket','read_errors']},sort_keys=True)
 if sig!=last:print(json.dumps(sample),flush=True);last=sig
 if len(DONE)==2:break
 if i<59:time.sleep(55)
dump('CLOSED.json',{'utc':now(),'samples':len(rows),'all_two_artifacts_salvaged':len(DONE)==2,'done':DONE,'latest':rows[-1],'source_or_claim_mutations':False})
