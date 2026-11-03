"""One bounded post-merge static delivery check; it does not assert a live UI run."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,time
from urllib.request import Request,urlopen
from urllib.parse import quote

merge=sys.argv[1]
assert len(merge)==40 and all(c in '0123456789abcdef'for c in merge)
base='https://chicago.polecat.live/4d/dev/'
out=Path(sys.argv[2]);assert not out.exists()
sid='green_tree_tavern'
def get(path):
    req=Request(base+path+'?verify='+str(time.time_ns()),headers={'Cache-Control':'no-cache','User-Agent':'Chicago-GT-merge-delivery-verification'})
    with urlopen(req,timeout=30)as r:return r.read()
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/'+path],stderr=subprocess.PIPE))
receipt={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'merge':merge,'base_url':base,'scope':'Static delivered build ancestry, GT source/card/yard and exact shipped WEB; no new browser or original-ticket completion claim.'}
build=json.loads(get('build.json'));receipt['build']=build
version=build.get('sha');assert isinstance(version,str)and version
public=api('commits/'+quote(version,safe=''))['sha'];compare=api('compare/'+merge+'...'+public);receipt['public_full_sha']=public;receipt['ancestry_status']=compare['status']
if compare['status']not in ['ahead','identical']:
    receipt['status']='MERGED_NOT_DEPLOYED_YET';out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'public':public,'merge':merge}));raise SystemExit(21)
doc=json.loads(get('data/sidecars/1835/'+sid+'.json'));pictures=json.loads(get('data/pictures/1835.json'))['by_structure'][sid];yard=json.loads(get('data/yard/town_trade_goods.json'))
annex=doc['attributes']['enclosed_left_annex']['value'];assert annex['shoulder_enclosed']is True
assert doc['grade']['value']=='attested' and doc['phase']=='frame_1833' and doc['target_date']=='1835-07-01'
assert 'CURRENT PICTURE-LED WORKING READING'in doc.get('research_note','')
belongs=lambda x:x.get('belongs_to')==sid or x.get('structure_id')==sid
wagons=[x for x in yard['wagons']if belongs(x)];assert len(wagons)==2 and all(not x.get('tilt')and not x.get('under_shed')and x.get('kind')!='covered'for x in wagons)
assert not any(belongs(x)for x in yard['sheds'])
asset=doc['asset'];assert not asset.startswith('/')and'..'not in asset.split('/')
web=get('data/'+asset);digest=hashlib.sha256(web).hexdigest();assert digest=='0154cfad5d6512a0d68e74a4f76c0cd5adad540a84844adc1f4a2fdc1d9d51e4',('later GT model differs; inspect actual native provenance',digest)
expected_pictures=json.loads(Path('/tmp/cobweb-active-20261103/chicago/4d/data/pictures/1835.json').read_bytes())['by_structure'][sid]
assert len(pictures)==4 and pictures==expected_pictures
held=[x for x in pictures if x['id']=='chm_green_tree_1859'];assert len(held)==1 and held[0]['rights']=='check required' and not held[0].get('spot')
assert len([x for x in pictures if x.get('spot')])==1 and next(x['id']for x in pictures if x.get('spot'))=='andreas_1884_green_tree_hotel_plate'
receipt.update(status='DELIVERED_GT_INCREMENT_STATIC_VERIFIED',gt_sidecar=doc,gt_picture_rows=pictures,gt_wagons=wagons,gt_web_sha256=digest,gt_web_bytes=len(web))
out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'public':public,'merge':merge,'web':digest}))
