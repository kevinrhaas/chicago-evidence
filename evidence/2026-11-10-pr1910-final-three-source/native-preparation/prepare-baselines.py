from pathlib import Path
import datetime,hashlib,json,sys
r=Path(__file__).resolve().parent;repo=Path('/tmp/chicago-west-wicket-20261109');app=repo/'chicago/4d';sys.path.insert(0,str(app/'generators'));from common import versions
rows=json.load(open(r/'SCOPE-ROWS.json'));m=json.load(open(app/'assets/manifest.json'))['assets'];w=json.load(open(app/'assets/manifest.web.json'))['masters'];v=json.load(open(app/'assets/manifest.versions.json'))['assets'];receipt=[]
def file(p):
 b=p.read_bytes();return {'path':str(p.relative_to(repo)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
for x in rows:
 key=x['asset_key'];master=file(app/'assets/gltf'/key);web=[file(app/'assets/web'/key)]+[file(app/'assets/web'/k)for k in versions.lod_asset_keys(key).values()];claim=(m if x['kind']=='default'else v)[key];assert master['bytes']==claim['bytes'];assert master['sha256']==(w[key]if x['kind']=='default'else claim['web_master_sha256']);receipt.append({'kind':x['kind'],'asset_key':key,'structure_id':x['structure_id'],'selected':x['stale'],'before_master':master,'before_web_outputs':web})
j={'status':'PROVISIONAL_ASSET_BASELINES_ONLY_NOT_HEAD_PIN','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'default_rows':len(m),'variant_rows':len(v),'actual_files_read_hashed':sum(1+len(x['before_web_outputs'])for x in receipt),'rows':receipt,'claim_limit':'Actual current old MASTER/WEB/LOD bytes only; final clean source binding will recapture all files after Root signal.'};p=r/'PROVISIONAL-ASSET-BASELINES.json';p.write_text(json.dumps(j,indent=2)+'\n');print('Read/hash',j['actual_files_read_hashed'],'actual old MASTER/WEB/LOD files; no HEAD pin')
