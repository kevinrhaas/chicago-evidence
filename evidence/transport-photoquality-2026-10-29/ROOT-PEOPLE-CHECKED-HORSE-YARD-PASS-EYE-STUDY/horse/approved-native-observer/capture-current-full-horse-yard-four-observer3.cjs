// SPDX-License-Identifier: GPL-3.0-or-later
// Four real published Full-yard horse views. Adapted from the sealed carriage
// observer. Native device profile and actual governed renderer DPR are distinct.
// No routes, alternate payloads, cap edits, layer removals or GPU mocks.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const cp=require('node:child_process'),http=require('node:http'),os=require('node:os');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const [repoArg,bindingArg,manifestArg,publishArg,prefixArg,outArg]=process.argv.slice(2);
if(process.argv.length!==8)throw Error('usage: node capture-current-full-horse-yard-four.cjs REPO SOURCE_BINDING MIRROR_MANIFEST PUBLISH_RESULT PUBLISH_SUPERVISOR_PREFIX NEW_OUT');
const repo=path.resolve(repoArg),site=path.join(repo,'site/4d'),out=path.resolve(outArg);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),fileSha=p=>sha(fs.readFileSync(p));
const need=(value,label)=>{if(!value)throw Error(label)};
const B=JSON.parse(fs.readFileSync(bindingArg)),M=JSON.parse(fs.readFileSync(manifestArg)),P=JSON.parse(fs.readFileSync(publishArg));
const pr=JSON.parse(fs.readFileSync(prefixArg+'.result.json')),pc=JSON.parse(fs.readFileSync(prefixArg+'.cleanup.json'));
need(B.HEAD&&B.TREE&&B.APP&&Array.isArray(B.paths),'Resolved current source HEAD/TREE/APP/pins required; pending-U binding refused');
need(P.HEAD===B.HEAD&&P.TREE===B.TREE&&P.APP===B.APP,'Publication tuple must equal actual source binding');
need(P.source_binding_sha256===fileSha(bindingArg)&&P.mirror_manifest_sha256===fileSha(manifestArg),'Publication must bind exact source and full mirror manifests');
need(String(P.result).startsWith('PASS')&&pr.returncode===0&&!pr.timed_out&&pc.cleanup_complete&&pc.remaining_owned_children.length===0,'Actual closed native publisher PASS and cleanup required');
need(Array.isArray(M)&&M.length>0,'Actual full native mirror file manifest required');
need(out!==repo&&!out.startsWith(repo+'/'),'Output must be outside the source worker');
need(!fs.existsSync(out),'Fresh output directory required');fs.mkdirSync(out);
const scratch=os.tmpdir();need(scratch.length<=35&&path.isAbsolute(scratch)&&scratch!==repo&&!scratch.startsWith(repo+'/'),'Short owned browser TMPDIR outside source worker required');
const scratchStat=fs.lstatSync(scratch);need(scratchStat.isDirectory()&&scratchStat.uid===process.getuid()&&!scratchStat.isSymbolicLink(),'Browser scratch must be owned ordinary directory');
need(fs.readdirSync(scratch).length===0,'Fresh empty owned browser TMPDIR required');
const git=(...args)=>cp.execFileSync('/usr/bin/git',args,{cwd:repo,encoding:'utf8',maxBuffer:64*1024*1024,env:{...process.env,GIT_OPTIONAL_LOCKS:'0',GIT_NO_LAZY_FETCH:'1'}}).trim();
function source(){
 need(git('rev-parse','HEAD')===B.HEAD,'Actual HEAD differs');
 need(git('rev-parse',B.TREE+':chicago/4d')===B.APP,'Bound APP differs from bound TREE');
 const merge=path.join(repo,'.git/MERGE_HEAD'),mh=fs.existsSync(merge)?fs.readFileSync(merge,'utf8').trim():null;
 need(mh===(B.MERGE_HEAD||null),'Actual merge state must be explicitly bound');
 need(!git('diff','--name-only')&&!git('ls-files','--others','--exclude-standard'),'No unstaged or untracked source changes');
 const staged=git('ls-files','--stage','-z').split('\0').filter(Boolean).map(row=>{
  const [meta,name]=row.split('\t'),[mode,oid,stage]=meta.split(' ');need(stage==='0','Unmerged source index refused');return[mode,oid,name].join('\t');
 }).sort();
 const tree=git('ls-tree','-r','-z',B.TREE).split('\0').filter(Boolean).map(row=>{
  const [meta,name]=row.split('\t'),[mode,kind,oid]=meta.split(' ');need(kind==='blob'||kind==='commit','Unexpected TREE entry');return[mode,oid,name].join('\t');
 }).sort();
 need(JSON.stringify(staged)===JSON.stringify(tree),'Actual complete index must equal bound TREE; no write-tree or Git writes');
 for(const row of B.paths){
  const f=path.resolve(repo,row.path);need(f.startsWith(repo+'/'),'Source containment');
  if(row.absent)need(!fs.existsSync(f),'Deleted source reappeared: '+row.path);
  else need(fs.statSync(f).size===row.bytes&&fileSha(f)===row.sha256,'Bound source changed: '+row.path);
 }
 return{HEAD:B.HEAD,TREE:B.TREE,APP:B.APP,MERGE_HEAD:mh,index_sha256:fileSha(path.join(repo,'.git/index')),source_binding_sha256:fileSha(bindingArg),paths:B.paths.length};
}
function mirror(){
 const found=[];
 for(const row of M){const f=path.resolve(site,row.path);need(f.startsWith(site+'/'),'Mirror containment');need(fs.statSync(f).size===row.bytes&&fileSha(f)===row.sha256,'Published bytes changed: '+row.path)}
 function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const f=path.join(dir,entry.name);if(entry.isDirectory())walk(f);else if(entry.isFile())found.push(path.relative(site,f).split(path.sep).join('/'));else throw Error('Mirror special file refused')}}walk(site);
 need(JSON.stringify(found.sort())===JSON.stringify(M.map(row=>row.path).sort()),'Published mirror file set differs');
 return{files:M.length,manifest_sha256:fileSha(manifestArg)};
}
const model='transport/standing-horse/horse-sevket-upper-orbital-transition-v1.glb';
const oldModels=['transport/standing-horse/horse-sevket-anatomy-v2.glb','transport/standing-horse/horse-sevket-upper-lid-strip-v1.glb'];
const modelSHA='e49b6f1c9f7b70f1fcdf19fa7f6dddf54048b32256b4d8030d6238d6dfe79d49';
const certSHA='72506859017d1f1aea57ad248d877a88bb07e701d4ec82c31e509dbb97e8d7a0';
const mode='upper_orbital_transition_v1', horseID='western_hotel_yard_standing_horse_01';
const sidecarPath='data/transport/parked/horse-sevket-sidecar.json';
const placementsPath='data/transport/parked/standing-horses.json';
const certPath='data/transport/parked/standing-horse-planted/upper-orbital-transition-v1-qualification-summary.json';
const nativeYard=JSON.parse(fs.readFileSync(path.join(site,'data/enclosures/western_hotel_wagon_yard.json')));
const insideNativeYard=(e,n)=>{const ring=nativeYard.ground.interior_local_enu_m;let inside=false;
 for(let i=0,j=ring.length-1;i<ring.length;j=i++){const [xi,yi]=ring[i],[xj,yj]=ring[j];
  if((yi>n)!==(yj>n)&&e<(xj-xi)*(n-yi)/(yj-yi)+xi)inside=!inside;
 }return inside;};
const sidecar=JSON.parse(fs.readFileSync(path.join(site,sidecarPath)));
const placements=JSON.parse(fs.readFileSync(path.join(site,placementsPath)));
const placed=placements.scenes['1835'].find(r=>r.id===horseID);
need(placed&&placements.models[placed.model].file===model,'Actual published current e49 selection required');
need(sidecar.runtime_asset.file===model&&sidecar.runtime_asset.sha256===modelSHA&&sidecar.runtime_asset.bytes===4159196
 &&sidecar.runtime_asset.source_qualification_mode===mode&&sidecar.runtime_asset.qualification_sha256===certSHA,'Actual sidecar exact e49 qualification required');
need(fileSha(path.join(site,'walk',model))===modelSHA&&fileSha(path.join(site,certPath))===certSHA,'Published model/certificate pins');
for(const oldModel of oldModels)need(!fs.existsSync(path.join(site,'walk',oldModel)),'Unused preserved parent must not be published: '+oldModel);
need(sidecar.idle.loaded_qualification_asset_sha256===modelSHA&&sidecar.idle.loaded_qualification_sha256===certSHA
 &&sidecar.idle.physical129_rerun_in_current_recovery===false&&sidecar.idle.external_raw_capture_arrays_available===false,'Active recorded e49 idle proof and recovery scope required');
const assets={['walk/'+model]:modelSHA};
// Bind actual HTTP JSON as well as GLB bytes. Renderer/module/build identities
// are already included in the mandatory complete source/mirror manifests.
const observed={...assets,[sidecarPath]:fileSha(path.join(site,sidecarPath)),[placementsPath]:fileSha(path.join(site,placementsPath))};
const save=(name,data)=>fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,2)+'\n');
const rows=[],errors=[],warnings=[],responses=[],failures=[],pending=new Set();let browser,context,server,current='initial';
const start=Date.now(),event=data=>fs.appendFileSync(path.join(out,'EVENTS.ndjson'),JSON.stringify({elapsed_ms:Date.now()-start,...data})+'\n');
const error=data=>{errors.push({stage:current,...data});event({event:'error',stage:current,...data})};
const check=(ok,label,detail)=>{if(!ok){failures.push({stage:current,label,detail});event({event:'assertion-failure',stage:current,label,detail})}};
const drain=async()=>{while(pending.size)await Promise.allSettled([...pending])};
const before={source:source(),mirror:mirror()};save('BEFORE.json',before);
const profiles=[{name:'desktop',width:1280,height:800,dpr:1,mobile:false},{name:'phone',width:390,height:780,dpr:3,mobile:true}];
const stands=[
 {name:'body-quarter',target:[0,.95,.10],eye:[4.9,0,2.3],altitude:1.65},
 {name:'head-eye',target:[.095,1.52,1.33],eye:[1.4,0,1.33],altitude:1.55},
];
save('EXACT-FOUR-VIEW-PLAN.json',{profiles,stands,scene:'1835',detail:'full',source_mode:mode,source_sha256:modelSHA,
 native_published_overrides:false,renderer_DPR:'actual native governed ratio; self-consistent canvas buffer required, not equality to context DPR',protocol_correction:'Unrun20261027 context3/native3 parity assumption replaced by actual current main.js bootQuality/governor behavior; required native gates unchanged',hold_pose:'actual elapsed/bones recorded; no asserted T0'});
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.glb':'model/gltf-binary','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.ktx2':'image/ktx2','.woff2':'font/woff2'};
(async()=>{try{
 server=http.createServer((request,response)=>{
  let relative;try{relative=decodeURIComponent(new URL(request.url,'http://local').pathname)}catch{response.writeHead(400);response.end();return}
  let file=path.resolve(site,'.'+relative);if(file!==site&&!file.startsWith(site+'/')){response.writeHead(403);response.end();return}
  try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');fs.readFile(file,(e,body)=>{response.writeHead(e?404:200,{'content-type':types[path.extname(file)]||'application/octet-stream',...(e?{}:{'content-length':body.length})});response.end(request.method==='HEAD'?undefined:e?'missing':body)})}catch{response.writeHead(404);response.end()}
 });await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port;
 for(const v of profiles){
  current=v.name+'/launch';event({event:'stage',stage:current});browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
  context=await browser.newContext({viewport:{width:v.width,height:v.height},isMobile:v.mobile,hasTouch:v.mobile,deviceScaleFactor:v.dpr});
  const page=await context.newPage();page.setDefaultTimeout(90000);
  page.on('pageerror',e=>error({kind:'pageerror',viewport:v.name,message:String(e)}));
  page.on('console',m=>{if(m.type()==='error')error({kind:'console',viewport:v.name,message:m.text()});else if(m.type()==='warning')warnings.push({viewport:v.name,stage:current,message:m.text()})});
  page.on('requestfailed',q=>error({kind:'requestfailed',viewport:v.name,method:q.method(),url:q.url(),failure:q.failure()}));
  page.on('response',response=>{
   if(response.status()>=400)error({kind:'HTTP',viewport:v.name,status:response.status(),url:response.url()});
   const url=new URL(response.url()),rel=url.pathname.slice(1);if(url.origin!==origin||!Object.hasOwn(observed,rel))return;
   let task;task=(async()=>{const bytes=await response.body(),row={viewport:v.name,path:rel,status:response.status(),bytes:bytes.length,sha256:sha(bytes)};responses.push(row);check(row.status===200&&row.sha256===observed[rel],'Actual HTTP response exact',row)})().catch(e=>error({kind:'asset-body',message:String(e)})).finally(()=>pending.delete(task));pending.add(task);
  });
  current=v.name+'/boot';await page.goto(origin+'/1835/',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:420000,polling:100});
  need(await page.evaluate(()=>!window.__chicago4d.error&&String(window.__chicago4d.scene.id)==='1835'),'Actual1835 boot required');
  // Use only existing native controls. The real renderer is never replaced.
  await page.evaluate(()=>{const a=window.__chicago4d;a.setAnimationHold(true);a.renderer.setAnimationLoop(null)});
  const roam=page.locator('#home-roam');await roam.waitFor({state:'visible'});await roam.click({trial:true});await roam.click();
  await page.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:90000,polling:100});
  if(await page.locator('#control-help').isVisible()){const gotit=page.locator('#control-help-gotit');await gotit.click({trial:true});await gotit.click()}
  await page.evaluate(async()=>{const a=window.__chicago4d;await a.setDetail('full');a.setAnimationHold(true);a.renderer.setAnimationLoop(null);a.setFly(true);
   a.walker.teleport({local_e:-123,local_n:-296,altitude_m:1.65,yaw_deg:270,pitch_deg:0});
   a.standingHorses.update(a.camera,0,{paused:true});await a.standingHorses.ready;
   if(!a.standingHorses.instances.some(i=>i.row.id==='western_hotel_yard_standing_horse_01'))throw Error('Actual native standing horse did not load');
  });
  // Only desktop uses the supported real canvas click/pointer-lock path.
  // Native phone keeps isMobile+hasTouch and its coarse/touch entry backend;
  // it naturally has no desktop engage hint. Never change its boot inputs.
  if(!v.mobile){
   const canvas=page.locator('#view');
   await canvas.click({position:{x:v.width*.5,y:v.height*.45},trial:true});
   await canvas.click({position:{x:v.width*.5,y:v.height*.45}});
   await page.waitForFunction(()=>document.pointerLockElement===window.__chicago4d.renderer.domElement
    &&window.__chicago4d.gesture.state.engaged&&document.getElementById('look-tag').hidden,null,{timeout:30000,polling:100});
   event({event:'native-desktop-canvas-engaged',viewport:v.name,actual:await page.evaluate(()=>({backend:window.__chicago4d.controlBackend,
    pointer_locked:document.pointerLockElement===window.__chicago4d.renderer.domElement,gesture:window.__chicago4d.gesture.state}))});
  }
  for(const stand of stands){
   current=v.name+'/full/'+stand.name;event({event:'stage',stage:current});
   const row=await page.evaluate(({stand})=>{
    const a=window.__chicago4d,i=a.standingHorses.instances.find(i=>i.row.id==='western_hotel_yard_standing_horse_01');if(!i)throw Error('Missing actual horse');
    i.root.updateMatrixWorld(true);
    const target=i.root.localToWorld(a.camera.position.clone().fromArray(stand.target));
    const eye=i.root.localToWorld(a.camera.position.clone().fromArray(stand.eye));
    const yaw=Math.atan2(target.x-eye.x,-target.z+eye.z)*180/Math.PI;
    a.setFly(true);a.walker.teleport({local_e:eye.x,local_n:-eye.z,yaw_deg:yaw,altitude_m:stand.altitude,pitch_deg:0});
    const pitch=Math.atan2(target.y-a.camera.position.y,Math.hypot(target.x-eye.x,target.z-eye.z))*180/Math.PI;
    a.walker.teleport({local_e:eye.x,local_n:-eye.z,yaw_deg:yaw,altitude_m:stand.altitude,pitch_deg:pitch});
    const gl=a.renderer.getContext(),pixel=new Uint8Array(4),frame_ms=[],gl_errors=[];
    for(let k=0;k<2;k++){const t=performance.now();a.step();gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,pixel);frame_ms.push(performance.now()-t);gl_errors.push(gl.getError())}
    const meshes=[],bones=[],bounds={min:[Infinity,Infinity,Infinity],max:[-Infinity,-Infinity,-Infinity]},q=a.camera.position.clone();
    i.root.updateMatrixWorld(true);i.root.traverse(m=>{if(!m.isMesh)return;if(m.isSkinnedMesh)m.skeleton.update();
     const geometry=m.geometry,position=geometry.getAttribute('position');
     for(let k=0;k<position.count;k++){m.getVertexPosition(k,q).applyMatrix4(m.matrixWorld).project(a.camera);for(let j=0;j<3;j++){bounds.min[j]=Math.min(bounds.min[j],q.getComponent(j));bounds.max[j]=Math.max(bounds.max[j],q.getComponent(j))}}
     meshes.push({name:m.name,triangles:(geometry.index?.count??position.count)/3,skinned:m.isSkinnedMesh,visible:m.visible,
      material:{name:m.material.name,metalness:m.material.metalness,roughness:m.material.roughness,map:m.material.map?.name,normalMap:m.material.normalMap?.name,side:m.material.side}});
     if(!bones.length&&m.skeleton)bones.push(...m.skeleton.bones.map(b=>({name:b.name,world_matrix:b.matrixWorld.toArray()})));
    });
    const projected=a.project(target.x,-target.z,target.y),pick=a.standingHorses.pickAt(projected,a.camera);
    return{actual_detail:a.detail,profile:a.device?.choice,stats:a.stats(),frame_ms,gl_errors,context_lost:gl.isContextLost(),
     actual_device_DPR:devicePixelRatio,native_governor:{...a.governor},canvas_backing:{width:a.renderer.domElement.width,height:a.renderer.domElement.height},css_viewport:{width:innerWidth,height:innerHeight},renderer_pixel_ratio:a.renderer.getPixelRatio(),
     drawing_buffer:{width:gl.drawingBufferWidth,height:gl.drawingBufferHeight},canvas_css:{width:a.renderer.domElement.clientWidth,height:a.renderer.domElement.clientHeight},
     visible:i.group.visible,placement:i.row,receipt:i.receipt,idle:i.idle?.status,bones,meshes,projected_horse_bounds_ndc:bounds,
     target_pick:pick?{id:pick.id,record:pick.record,distance:pick.distance,point:pick.point.toArray()}:null,
     target_world:target.toArray(),requested_native_camera:{local_e:eye.x,local_n:-eye.z,yaw_deg:yaw,altitude_m:stand.altitude,pitch_deg:pitch},
     player:{...a.player},camera:{position:a.camera.position.toArray(),quaternion:a.camera.quaternion.toArray(),fov:a.camera.fov,zoom:a.camera.zoom,near:a.camera.near,far:a.camera.far},
     exposure:a.exposure,production_shadows:{enabled:a.renderer.shadowMap.enabled,type:a.renderer.shadowMap.type,reachM:a.world.shadowRig.reachM,texelM:a.world.shadowRig.texelM},
     detail_policies:a.detailLevels,problems:[...a.problems],
     expected_review_ids:[...a.registry.values()].filter(r=>r.sidecar?.review_required).map(r=>r.sidecar.id).sort(),
     native_engagement:{backend:a.controlBackend,coarse_pointer:matchMedia('(pointer: coarse)').matches,max_touch_points:navigator.maxTouchPoints,touch_first:document.body.classList.contains('touch-first'),pointer_locked:document.pointerLockElement===a.renderer.domElement,gesture:a.gesture.state,look_tag_hidden:document.getElementById('look-tag').hidden},card:i.card};
   },{stand});
   row.viewport=v.name;row.pose=stand.name;row.screenshot=`${v.name}-full-${stand.name}.png`;
   await page.screenshot({path:path.join(out,row.screenshot),timeout:90000});const png=fs.readFileSync(path.join(out,row.screenshot));row.png={bytes:png.length,sha256:sha(png),width:png.readUInt32BE(16),height:png.readUInt32BE(20),scope:'Native browser screenshot at requested context DPR; renderer raster DPR is recorded separately'};
   row.bone_state_sha256=sha(JSON.stringify(row.bones));rows.push(row);save('PROGRESS.json',{rows,failures,errors,warnings,responses});
   check(insideNativeYard(row.requested_native_camera.local_e,row.requested_native_camera.local_n)
    &&insideNativeYard(row.target_world[0],-row.target_world[2]),
    'Actual camera and horse target inside the unchanged native yard footprint',
    {camera:row.requested_native_camera,target:row.target_world,ring:nativeYard.ground.interior_local_enu_m});
   check(row.actual_detail==='full','Actual Full tier',row.actual_detail);
   check(row.stats.withinBudget,'Actual native frame budget; no cap override',row.stats);
   check(row.gl_errors.every(n=>n===0)&&row.context_lost===false,'Actual postdraw GL0 and context not lost',{errors:row.gl_errors,lost:row.context_lost});
   check(row.actual_device_DPR===v.dpr&&row.css_viewport.width===v.width&&row.css_viewport.height===v.height,'Actual requested CSS/device profile; native renderer DPR only recorded',row.css_viewport);
   const ratio=row.renderer_pixel_ratio,g=row.native_governor;
   const actualBufferConsistent=Number.isFinite(ratio)&&ratio>0&&ratio<=row.actual_device_DPR
    &&row.canvas_css.width===v.width&&row.canvas_css.height===v.height
    &&row.drawing_buffer.width===Math.floor(row.canvas_css.width*ratio)
    &&row.drawing_buffer.height===Math.floor(row.canvas_css.height*ratio)
    &&row.canvas_backing.width===row.drawing_buffer.width&&row.canvas_backing.height===row.drawing_buffer.height
    &&g.ratio===ratio&&Number.isFinite(g.ceiling)&&Number.isFinite(g.scale)&&g.scale>0&&g.scale<=1
    &&Math.abs(g.ceiling*g.scale-ratio)<=1e-9;
   check(actualBufferConsistent,'Actual native governed DPR and canvas buffer are self-consistent',{context_device_DPR:v.dpr,renderer_DPR:ratio,governor:g,css:row.canvas_css,buffer:row.drawing_buffer,canvas:row.canvas_backing});
   check(row.visible&&row.meshes.length===3&&row.meshes.every(m=>m.skinned)&&row.meshes.reduce((sum,m)=>sum+m.triangles,0)===17390,'Real visible exact native three-mesh horse',row.meshes);
   check(row.receipt.asset_sha256===modelSHA&&row.receipt.source_qualification_mode===mode&&row.receipt.mixer_count===1&&row.receipt.original_six_autoplay===false,'Actual e49 standing ownership/selection',row.receipt);
   check(row.placement.at_local_enu_m[0]===-127.5&&row.placement.at_local_enu_m[1]===-296&&row.placement.bearing_deg===90&&JSON.stringify(row.receipt.support_quaternion_xyzw)===JSON.stringify(placed.support_quaternion_xyzw),'Native unchanged yard stand/support',row.placement);
   const gaps=Object.values(row.receipt.minimum_gap_by_hoof_m),slab=Object.values(row.receipt.equal_10mm_slab_minimum_gaps_m);
   check(gaps.length===4&&gaps.every(n=>Number.isFinite(n)&&n<=.001&&n>=-1e-5)&&slab.length===4&&slab.every(n=>Number.isFinite(n)&&n>=-1e-5),'Actual native per-foot sampled minimum1mm/no sampled penetration receipt',row.receipt);
   check(row.target_pick?.id===horseID,'Actual native projected horse pick/credit',row.target_pick);
   if(stand.name==='body-quarter')check(row.projected_horse_bounds_ndc.min.every(n=>n>=-1)&&row.projected_horse_bounds_ndc.max.every(n=>n<=1),'Actual full body and feet inside measured frustum',row.projected_horse_bounds_ndc);
   // Same exact review-ID consistency and fatal classification as the native
   // smoke_renderer.mjs1859–1875. Keep all actual notices in the immutable row.
   const reviews=row.problems.filter(p=>/review_required is set/.test(p));
   const reportedReviews=reviews.map(p=>p.split(':',1)[0]).sort();
   check(row.expected_review_ids.length>0&&JSON.stringify(reportedReviews)===JSON.stringify(row.expected_review_ids),
    'Native exact declared review annotations',{reported:reportedReviews,expected:row.expected_review_ids,notices:reviews});
   const hard=row.problems.filter(p=>!/provisional|PLACEHOLDER|placeholder|review_required is set/i.test(p));
   check(hard.length===0,'Native no unexpected loader problems',hard);
   const engagement=row.native_engagement;
   if(v.mobile)check(engagement.backend==='touch'&&engagement.coarse_pointer&&engagement.max_touch_points>0
    &&engagement.touch_first&&!engagement.pointer_locked&&engagement.look_tag_hidden&&!engagement.gesture.tag,
    'Unchanged native phone coarse touch backend naturally has no desktop hint',engagement);
   else check(engagement.pointer_locked&&engagement.backend==='pointerlock'&&engagement.gesture.engaged
    &&engagement.look_tag_hidden&&!engagement.coarse_pointer,
    'Trusted native desktop canvas pointer engagement hides hint',engagement);
   // Context/device DPR and the product's native governed raster ratio may differ.
   // Preserve their actual values; do not change sharpness or disable the governor.
   if(!actualBufferConsistent)throw Error('Native governed buffer is inconsistent; actual row and PNG retained');
  }
  await drain();for(const rel of Object.keys(observed))check(responses.some(r=>r.viewport===v.name&&r.path===rel&&r.sha256===observed[rel]),'Exact real HTTP model/placement/sidecar served: '+v.name+'/'+rel);
  await context.close();context=null;await browser.close();browser=null;
 }
 }catch(e){error({kind:'capture-fatal',message:String(e),stack:e.stack})}finally{
  if(context)try{await context.close()}catch(e){error({kind:'context-close',message:String(e)})}
  if(browser)try{await browser.close()}catch(e){error({kind:'browser-close',message:String(e)})}
  await drain();if(server)await new Promise(resolve=>server.close(resolve));
  try{const after={source:source(),mirror:mirror()};save('AFTER.json',after);check(JSON.stringify(before)===JSON.stringify(after),'Complete bound source/index/mirror before-after exact')}catch(e){error({kind:'source-mirror-final',message:String(e)})}
  const complete=rows.length===4,pass=complete&&!failures.length&&!errors.length;
  save('RESULT.json',{state:pass?'PASS_BOUNDED_CURRENT_E49_FULL_YARD_CAPTURE':'NONPASS',scope:'Four current published Full-yard runtime/views only; images require personal review. Not photoMATCHES/T3088DONE/whole gate/DEV merge.',HEAD:B.HEAD,TREE:B.TREE,APP:B.APP,rows,failures,errors,warnings,responses,complete_four_rows:complete,elapsed_seconds:(Date.now()-start)/1000,pending_body_tasks:pending.size,no_published_overrides:true,source_sha256:modelSHA,source_qualification_mode:mode,physical129_proof:'existing exact e49 source-bound qualification; not rerun by this capture',native_fullgate_or_smoke_acceptance:false,context_listener_proof:'NOT CLAIMED; actual getError/isContextLost recorded'});process.exitCode=pass?0:1;
 }
})().catch(e=>{error({kind:'outer-unhandled',message:String(e)});process.exitCode=1});
