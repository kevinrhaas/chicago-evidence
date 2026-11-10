#!/usr/bin/env python3
"""Run only with parent-granted serial GPU slot and supplied genuine final MASTER."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, time
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--glb',required=True);a=p.parse_args()
r=Path(__file__).resolve().parent/'chicago/4d';own=Path('/tmp/nov9-group-green_tree/chicago/4d')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
src=Path(a.glb).resolve();target=r/'assets/gltf/green_tree_tavern__frame_1833.glb'
assert src.is_file() and src.read_bytes()[:4]==b'glTF'
assert sha(src)=='124bf0599a8900855c02a1e7b90ac57c2097718a2bf2f7985e9d58f7c7dab84a' and src.stat().st_size==293260,'Not the genuine retained9dd Green Tree MASTER'
shutil.copyfile(src,target)
base=Path(__file__).resolve().parent
(base/'raw').mkdir(exist_ok=True);(base/'logs').mkdir(exist_ok=True)
rows=[]
for view in ['andreas_1838','trowbridge_1902','kurz_1893_panel11']:
 camera=Path('data/reference_views/green_tree_tavern')/(view+'.json')
 assert sha(r/camera)==sha(own/camera),'External fixture changed the committed camera bytes'
 started=time.time();result=subprocess.run(['node','tools/photo_match.mjs',str(camera)],cwd=r,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (base/'logs'/(view+'.log')).write_text(result.stdout)
 print(view,'exit',result.returncode,'seconds',round(time.time()-started,3),flush=True)
 assert result.returncode==0,result.stdout[-5000:]
 raw=re.search(r'^\s+(/tmp/[^\n]+-render\.png)$',result.stdout,re.M);assert raw,result.stdout
 raw_dst=base/'raw'/(view+'-render.png');shutil.copyfile(raw.group(1),raw_dst)
 record=json.loads((r/camera.with_suffix('.match.json')).read_text())
 photo=(r/camera.parent/json.loads((r/camera).read_text())['photo']).resolve()
 assert record['glb']=='assets/gltf/green_tree_tavern__frame_1833.glb'
 assert record['glb_sha256']==sha(target)==sha(src)
 assert record['camera_sha256']==sha(r/camera)
 assert record['photo_sha256']==sha(photo)
 assert record['verdict']=='unreviewed','Do not inherit a match verdict before actual final pair review'
 assert (r/record['side_by_side']).is_file()
 rows.append({**{key:record[key]for key in ['view','glb_sha256','camera_sha256','photo_sha256','side_by_side','verdict']},'exit_code':result.returncode,'seconds':round(time.time()-started,3),'raw_png':str(raw_dst),'raw_sha256':sha(raw_dst),'pair_sha256':sha(r/record['side_by_side']),'log':str(base/'logs'/(view+'.log'))})
(r.parent.parent/'RENDER-BINDINGS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
