"""Read-only delivery proof, not a browser/render execution."""
from pathlib import Path
import urllib.request,json,time,hashlib,subprocess,sys
P=Path(__file__).parent;Q=P/'gazetteer-finish';R=Path('/workspace/chicago-bridge-increment-20261102/chicago/4d');U=Q/'preview';U.mkdir(exist_ok=True);m=json.loads((Q/'MERGE-RESPONSE.json').read_text());assert m['merged'];merged=m['sha'];expected=json.loads((P/'integration-ce094/data/sidecars/1835/lake_house_construction.json').read_bytes());expected_fergus=json.loads((R/'data/sidecars/1835/sources/fergus_chicago_directory_1839.json').read_bytes());history=[];started=time.monotonic();sys.path.insert(0,str(R/'tools'));from readable_text import reader_copy
expected_text=(P/'ACTUAL-READER-FUNCTION-NOTE.txt').read_text().rstrip('\n')
def get(path):
 req=urllib.request.Request('https://chicago.polecat.live/4d/dev/'+path+'?_='+str(time.time_ns()),headers={'Cache-Control':'no-cache','User-Agent':'Chicago-source-delivery-check'})
 with urllib.request.urlopen(req,timeout=15)as response:b=response.read(8000000)
 return json.loads(b),hashlib.sha256(b).hexdigest()
while time.monotonic()-started<500:
 row={'unix':time.time(),'merged':merged,'method':'HTTP_SOURCE_AND_READER_ONLY_NO_BROWSER'}
 try:
  build,h=get('build.json');row['build']=build
  compare=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/compare/'+merged+'...'+build['sha']],timeout=25));row['preview_at_merge_or_descendant']=compare['behind_by']==0 and compare['status'] in ['identical','ahead']
  if row['preview_at_merge_or_descendant']:
   sidecar,sh=get('data/sidecars/1835/lake_house_construction.json');fergus,fh=get('data/sidecars/1835/sources/fergus_chicago_directory_1839.json');reader,rh=get('data/reader/structures_1835.json');shown=reader_copy(sidecar,reader)['attributes']['function']['note'];row.update({'Lake_sidecar_exact':sidecar==expected,'Fergus1694_source_exact':fergus==expected_fergus,'actual_reader_function_note_exact':shown==expected_text,'Lake_sidecar_sha256':sh,'Fergus_source_sha256':fh,'reader_overlay_sha256':rh});row['delivery_PASS']=all(row[k]for k in ['Lake_sidecar_exact','Fergus1694_source_exact','actual_reader_function_note_exact'])
   if row['delivery_PASS']:
    for name,data in [('ACTUAL-LIVE-LAKE.json',sidecar),('ACTUAL-LIVE-FERGUS.json',fergus),('ACTUAL-PREVIEW-ANCESTRY.json',compare)]: (U/name).write_text(json.dumps(data,indent=2)+'\n')
    (U/'ACTUAL-LIVE-FUNCTION-NOTE.txt').write_text(shown+'\n');(U/'PREVIEW-DELIVERY-PASS.json').write_text(json.dumps(row,indent=2)+'\n')
 except Exception as error:row['read_error']=repr(error)
 history.append(row);(U/'PREVIEW-DELIVERY-HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');print(json.dumps(row),flush=True)
 if row.get('delivery_PASS'):break
 time.sleep(20)
closed={'status':'PASS'if history[-1].get('delivery_PASS')else'PREVIEW_PENDING','source_dev_merge_verified':True,'samples':len(history),'latest':history[-1]};(U/'PREVIEW-DELIVERY-CLOSED.json').write_text(json.dumps(closed,indent=2)+'\n');raise SystemExit(0 if closed['status']=='PASS' else 2)
