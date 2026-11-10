from pathlib import Path
import hashlib,json,re,shutil,subprocess,time
root=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');own=Path('/tmp/nov9-group-green_tree/chicago/4d');base=Path('/tmp/nov10-final-three-native/green-tree-after');r=base/'chicago/4d';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='114b98c2dc057bbc47f66ce158bc984be438399e0c4984222b93e810d542714f'
for rel in ['assets/gltf','data/reference_views/green_tree_tavern','data/sources','docs/RESEARCH/photo-match/green_tree_tavern']:(r/rel).mkdir(parents=True,exist_ok=True)
for link,target in [(r/'renderers',root/'renderers'),(r/'tools',root/'tools'),(r/'assets/manifest.json',root/'assets/manifest.json'),(r/'data/sources/assets',root/'data/sources/assets'),(r.parent/'reference',root.parent/'reference')]:
 if not link.exists():link.symlink_to(target,target_is_directory=target.is_dir())
model=root/'assets/gltf/green_tree_tavern__frame_1833.glb';assert sha(model)==expected and model.stat().st_size==297628;shutil.copyfile(model,r/'assets/gltf/green_tree_tavern__frame_1833.glb')
for sub in ['raw','logs']:(base/sub).mkdir(exist_ok=True)
rows=[]
for view in ['andreas_1838','trowbridge_1902','kurz_1893_panel11']:
 cam=Path('data/reference_views/green_tree_tavern')/(view+'.json');assert sha(root/cam)==sha(own/cam);shutil.copyfile(root/cam,r/cam);shutil.copyfile(own/cam.with_suffix('.match.json'),r/cam.with_suffix('.match.json'))
 assert json.load(open(r/cam.with_suffix('.match.json')))['verdict']=='differs'
 started=time.time();result=subprocess.run(['node','tools/photo_match.mjs',str(cam)],cwd=r,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(base/'logs'/(view+'.log')).write_text(result.stdout);print(view,'exit',result.returncode,'seconds',round(time.time()-started,3),flush=True);assert result.returncode==0,result.stdout[-5000:]
 record=json.load(open(r/cam.with_suffix('.match.json')));photo=(root/cam.parent/json.load(open(root/cam))['photo']).resolve();assert record['glb_sha256']==expected and record['camera_sha256']==sha(root/cam)==sha(own/cam)and record['photo_sha256']==sha(photo)and record['verdict']=='unreviewed'
 raw=re.search(r'^\s+(/tmp/[^\n]+-render\.png)$',result.stdout,re.M);assert raw;raw_dst=base/'raw'/(view+'-render.png');shutil.copyfile(raw.group(1),raw_dst);rows.append({'view':view,'native_run':42758213227,'native_source':'b9c767997c452740c6b690cf2d280d7f75c8c9d5','retained_native':'6908d896ffba7af2e99d9e5daffd1b49f3f1c9c1','MASTER_sha256':expected,'camera_sha256':record['camera_sha256'],'photo_sha256':record['photo_sha256'],'pair':record['side_by_side'],'pair_sha256':sha(r/record['side_by_side']),'raw_png':str(raw_dst),'raw_sha256':sha(raw_dst),'exit_code':result.returncode,'seconds':round(time.time()-started,3),'verdict':'unreviewed'})
 (base/'RENDER-BINDINGS.json').write_text(json.dumps(rows,indent=2)+'\n')
assert sha(model)==expected
print('THREE B AFTER RENDERS COMPLETE; no verdict assigned',flush=True)
