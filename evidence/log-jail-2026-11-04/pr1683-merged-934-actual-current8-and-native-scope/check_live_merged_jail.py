"""Read-only one-observation current dev delivery proof; never a browser/runtime claim."""
from pathlib import Path
import urllib.request,json,subprocess,hashlib,datetime,time
P=Path(__file__).parent;Q=P/'merge62f';read=lambda p:json.loads(Path(p).read_bytes());merge=read(Q/'MERGE-RESPONSE.json');assert merge['merged'];H=merge['sha'];base='https://chicago.polecat.live/4d/dev/';sha=lambda b:hashlib.sha256(b).hexdigest();stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S');O=Q/('live-'+stamp);O.mkdir();rows=[];build=None;status='WAITING_FOR_LIVE_DEV';error=None
try:
 def fetch(path):
  req=urllib.request.Request(base+path+'?jail_merge='+H,headers={'User-Agent':'Jail-merged-delivery-audit','Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=30)as response:return response.read()
 raw=fetch('build.json');(O/'build.json').write_bytes(raw);build=json.loads(raw);assert build.get('tier')=='dev'and build.get('ref')=='refs/heads/dev',('Wrong preview metadata',build)
 revision=build.get('sha')or build.get('version');assert revision
 commit=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/commits/'+revision]));actual=commit['sha'];comp=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/compare/'+H+'...'+actual]));(O/'BUILD-ANCESTRY.json').write_text(json.dumps(comp,indent=2)+'\n');assert comp['behind_by']==0 and comp['status']in ['identical','ahead'],('Live build does not contain merge yet',revision)
 expected=read(P/'gt26-final/CURRENT-PUBLISHED-TARGET-BINDINGS.json')
 for row in expected['all6_actualpublishedJail_glbs_sidecars_enclosures_exact_to_actual3f']:
  data=fetch(row['path']);assert sha(data)==row['sha256'],('live target mismatch',row['path']);rows.append({'path':row['path'],'bytes':len(data),'sha256':sha(data),'live_exact_actual_qualified_target':True})
 pictures=json.loads(fetch('data/pictures/1835.json'))['by_structure'];assert all(pictures[k]==v for k,v in expected['both_current_published_picture_rows_value_exact_to_actualv4_capture'].items());status='LIVE_DEV_JAIL_DELIVERY_VERIFIED'
except Exception as exc:error=repr(exc)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'base_url':base,'merge':H,'observed_build':build,'files':rows,'both_live_Jail_picture_rows_exact':status=='LIVE_DEV_JAIL_DELIVERY_VERIFIED','error':error,'new_live_browser_or_native_execution':False,'production_dispatch':False};(O/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(Q/'LATEST-LIVE-OBSERVATION.json').write_text(json.dumps({'path':str(O),'result':result},indent=2)+'\n');print(json.dumps(result));raise SystemExit(0 if status=='LIVE_DEV_JAIL_DELIVERY_VERIFIED'else 2)
