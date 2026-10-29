from pathlib import Path
import subprocess,json,hashlib,tarfile,datetime
APP=Path('/tmp/chicago-transport-resume-20261029/chicago/4d');REPO=APP.parent.parent;MIRROR=REPO/'site/4d';OUT=Path(__file__).parent
assert not subprocess.check_output(['git','diff','--name-only'],cwd=REPO).strip(),'Unstaged source mutation remains'
changed=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO,text=True).splitlines()
assert len(changed)==33 and all(p.startswith('chicago/4d/') for p in changed)
tree=subprocess.check_output(['git','write-tree'],cwd=REPO,text=True).strip()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
app_tree=subprocess.check_output(['git','rev-parse',tree+':chicago/4d'],cwd=REPO,text=True).strip()
semantic=[]
for row in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=REPO).split(b'\0'):
 if not row:continue
 meta,name=row.split(b'\t',1);mode,obj,stage=meta.decode().split(' ');semantic.append(dict(mode=mode,object=obj,stage=int(stage),path=name.decode()))
def pin(f,root):
 raw=f.read_bytes();return {'path':f.relative_to(root).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
extra=['renderers/web/js/humans.js','renderers/web/js/scene-loader.js','renderers/web/vendor/three-0.185.1/three.module.js','renderers/web/vendor/three-0.185.1/three.core.js','renderers/web/vendor/three-0.185.1/addons/loaders/GLTFLoader.js','renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js','renderers/web/vendor/three-0.185.1/addons/utils/SkeletonUtils.js','tools/human_fixture.mjs','tools/human_fixture.html','data/humans/contract.json','tools/human_contract.py','renderers/web/js/frame-governor.js']
source=set(REPO/p for p in changed)|set(APP/p for p in extra)|set((APP/'assets/humans').rglob('*.glb'))
guard={'schema':'human_world_motion_guard_v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':head,'tree':tree,'app_tree':app_tree,'semantic_index':semantic,'source_files':[pin(f,APP) for f in sorted(source)],'published_files':[pin(f,MIRROR) for f in sorted(MIRROR.rglob('*')) if f.is_file()]}
assert len([r for r in guard['source_files'] if r['path'].endswith('.glb')])==16
assert len([r for r in guard['source_files'] if not r['path'].endswith('.glb')])>=31
(OUT/'FINAL-WORLD-GUARD-01.json').write_text(json.dumps(guard,indent=2)+'\n')
manifest={'created_utc':guard['created_utc'],'head':head,'tree':tree,'app_tree':app_tree,'changed_files':[pin(REPO/p,APP) for p in changed],'generated_assets_recipe':'data/humans/animations/natural-standing-v1.json','scope':'Postowners latestDEV9400 source; actualnativeall16x2 cost passed, finiteCPU129original+metadataequivalence retained; WORLD/fullgate/PR delivery pending.'}
(OUT/'FINAL-SOURCE-MANIFEST-01.json').write_text(json.dumps(manifest,indent=2)+'\n')
with tarfile.open(OUT/'FINAL-SOURCE-01.tar.gz','w:gz') as tar:
 for p in changed:
  if not p.endswith('.glb'):tar.add(REPO/p,arcname='source/'+str(Path(p).relative_to('chicago/4d')),recursive=False)
 tar.add(OUT/'FINAL-SOURCE-MANIFEST-01.json',arcname='SOURCE-MANIFEST.json',recursive=False)
for name in ['FINAL-WORLD-GUARD-01.json','FINAL-SOURCE-MANIFEST-01.json','FINAL-SOURCE-01.tar.gz']:
 f=OUT/name;print(name,f.stat().st_size,hashlib.sha256(f.read_bytes()).hexdigest())
print(json.dumps({'head':head,'tree':tree,'app_tree':app_tree,'source_files':len(guard['source_files']),'semantic_index':len(semantic),'mirror_files':len(guard['published_files']),'mirror_bytes':sum(r['bytes'] for r in guard['published_files'])}))
