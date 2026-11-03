"""Actual public dev ancestry and static Wolf delivery; no new runtime-smoke claim."""
import argparse, hashlib, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

P=Path(__file__).resolve().parent; W=Path('/tmp/wolf-poster-source-20261103'); S=W/'site/4d'
HEAD='8e5aedc13ec207020c1c08d1ea78ec0eab450654'
BASE='https://chicago.polecat.live/4d/dev/'
PICTURES='data/pictures/1835.json'; SIDECAR='data/sidecars/1835/wolf_point_tavern.json'; READER='data/reader/structures_1835.json'
MODEL='data/gltf/wolf_point_tavern__log_frame_1828.glb'; MODEL_SHA='fdc5ef22a440636e35e4cec15818661f4351f0f4d0c9e506ef36b00422a45210'
parser=argparse.ArgumentParser();parser.add_argument('--snapshot-before',action='store_true');args=parser.parse_args()
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/'+path]))
def get(path):
    request=Request(BASE+path+'?pr1666verify='+str(time.time_ns()),headers={'Cache-Control':'no-cache','User-Agent':'Chicago-Wolf-dev-delivery-verification'})
    with urlopen(request,timeout=45)as response:
        assert response.status==200; data=response.read(10_000_001)
    assert len(data)<=10_000_000;return data
def snapshot():
    first=get('build.json');paths=[PICTURES,SIDECAR,READER,MODEL]
    with ThreadPoolExecutor(max_workers=4)as pool:payloads=dict(zip(paths,pool.map(get,paths)))
    assert first==get('build.json'),'Public build changed during snapshot; take a new snapshot'
    return json.loads(first),{'build.json':first,**payloads}
def copy_reader(sidecar,overlay):
    code="import fs from'node:fs';import{pathToFileURL}from'node:url';const{readerCopy}=await import(pathToFileURL(process.argv[1]));const p=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(readerCopy(p.sidecar,p.overlay).research_note));"
    result=subprocess.check_output(['node','--input-type=module','-e',code,str(S/'walk/js/reader-text.js')],input=json.dumps({'sidecar':sidecar,'overlay':overlay}).encode())
    return json.loads(result)
if args.snapshot_before:
    build,payloads=snapshot();out=P/'public-before';assert not out.exists();out.mkdir()
    for path,data in payloads.items():
        target=out/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    note=copy_reader(json.loads(payloads[SIDECAR]),json.loads(payloads[READER]))
    result={'status':'PREMERGE_PUBLIC_STATIC_SNAPSHOT','at':datetime.now(timezone.utc).isoformat(),'public_build':build,'wolf_picture_rows':len(json.loads(payloads[PICTURES])['by_structure']['wolf_point_tavern']),'wolf_native_reader_note_sha256':hashlib.sha256(note.encode()).hexdigest(),'no_final1666_delivery_claim':True}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit()
pr=api('pulls/1666');assert pr['head']['sha']==HEAD,'PR review scope changed'
if not pr['merged']:print('NOT_MERGED_YET');raise SystemExit(20)
merge=pr['merge_commit_sha'];build,payloads=snapshot();assert build['tier']=='dev' and build['ref']=='refs/heads/dev'
comparison=api(f"compare/{merge}...{build['sha']}")
if comparison['behind_by']or comparison['status']not in ['ahead','identical']:
    print('MERGED_NOT_DEPLOYED_YET',merge,build['sha']);raise SystemExit(21)
assert hashlib.sha256(payloads[MODEL]).hexdigest()==MODEL_SHA
accepted=json.loads(Path('/tmp/wolf-final-head-qa2-20261103/PLAN.json').read_bytes());rows=json.loads(payloads[PICTURES])['by_structure']['wolf_point_tavern'];assert rows==accepted['expected_wolf_pictures'] and len(rows)==7
sidecar=json.loads(payloads[SIDECAR]);assert sidecar['id']=='wolf_point_tavern' and sidecar['phase']=='log_frame_1828' and sidecar['target_date']=='1835-07-01' and sidecar['grade']['value']=='attested'
note=copy_reader(sidecar,json.loads(payloads[READER]));assert note==accepted['expected_research_note']
out=P/('public-after-'+build['sha']);assert not out.exists();out.mkdir()
for path,data in payloads.items():
    target=out/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
result={'status':'MERGED_AND_PUBLIC_DEV_STATIC_DELIVERY_VERIFIED','at':datetime.now(timezone.utc).isoformat(),'pr':1666,'reviewed_head':HEAD,'merge_commit':merge,'deployed_build':build,'deployed_descends_from_merge':True,'wolf_images_count':7,'wolf_model_web_sha256':MODEL_SHA,'wolf_grade':sidecar['grade'],'native_reader_exact_accepted_e32':True,'native_reader_note_sha256':hashlib.sha256(note.encode()).hexdigest(),'files':{path:{'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}for path,data in payloads.items()},'scope':'HTTP build ancestry and static Wolf card/native reader/model delivery only. Existing qualified e32 actual desktop/phone and native107 proof remains bounded to unchanged targets; this is no new browser, geographic pose or whole-app smoke claim.'}
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(P/'PUBLIC-DELIVERY-RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'merge':merge,'public_build':build['sha']}))
