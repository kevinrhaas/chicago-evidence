from pathlib import Path
import json,subprocess,hashlib,zipfile,time,datetime
P=Path(__file__).resolve().parent;Q=P/'completed-runs';Q.mkdir(exist_ok=True)
expected={41740271907:126279743846,41742893188:126288564761,41746386858:126300351548};done={};attempts={}
def api(p):return json.loads(subprocess.check_output(['gh','api',p],timeout=45))
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
for poll in range(120):
 latest=json.loads((P/'observer/LATEST.json').read_text())
 for row in latest['health']:
  run=row['run']
  if run not in expected or run in done or row.get('status')!='completed':continue
  attempts[run]=attempts.get(run,0)+1
  try:
   art=api(f'repos/kevinrhaas/polecat-platform/actions/runs/{run}/artifacts?_={int(time.time())}')
   stream=[a for a in art['artifacts']if a['name']==f'steward-stream-{run}' and not a['expired']]
   if not stream:continue
   assert len(stream)==1;a=stream[0];assert a['digest'].startswith('sha256:')
   R=Q/str(run);R.mkdir(exist_ok=True);dump(R/'ARTIFACT-IDENTITY.json',a)
   b=subprocess.check_output(['gh','api',f"repos/kevinrhaas/polecat-platform/actions/artifacts/{a['id']}/zip"],timeout=120)
   digest=hashlib.sha256(b).hexdigest();assert a['digest']=='sha256:'+digest
   zpath=R/'raw.zip';zpath.write_bytes(b)
   with zipfile.ZipFile(zpath)as z:
    members=[]
    for n in z.namelist():
     p=Path(n);assert not p.is_absolute()and'..'not in p.parts
     info=z.getinfo(n);assert info.file_size<100000000
     members.append({'name':n,'bytes':info.file_size})
    z.extractall(R/'raw')
   rec={'run':run,'job':expected[run],'digest_verified':True,'sha256':digest,'archive_bytes':len(b),'members':members,'native_job_conclusion':row.get('conclusion'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification_claimed':False}
   dump(R/'ARTIFACT-VERIFIED.json',rec);done[run]=rec;print(json.dumps(rec),flush=True)
  except Exception as e:print(json.dumps({'run':run,'attempt':attempts[run],'error':repr(e)}),flush=True)
 dump(Q/'LATEST.json',{'poll':poll+1,'done':done,'attempts':attempts,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 if len(done)==len(expected):break
 if(P/'observer/CLOSED.json').exists()and all(r in done for r in expected if any(x['run']==r and x.get('status')=='completed'for x in latest['health'])):break
 time.sleep(30)
dump(Q/'CLOSED.json',{'done':done,'attempts':attempts,'observer_closed':(P/'observer/CLOSED.json').exists(),'all3_salvaged':len(done)==3})
