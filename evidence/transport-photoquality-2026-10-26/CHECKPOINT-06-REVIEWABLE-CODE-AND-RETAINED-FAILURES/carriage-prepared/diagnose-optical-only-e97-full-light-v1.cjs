// External exact-e97 optical-only hypothesis. No source/cap edits.
// Native production Full/Light stands, unfiltered failures and original ceilings.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const cp=require('node:child_process'),http=require('node:http');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const R='/tmp/chicago-photo-worker-t3084-20261026',H='e97b67d549882b13fd858e714e73fb11da5aa006';
const TREE='c4247f16a7e4672ee265715b2cd0a8b03e9b0225';
const C='/tmp/T3084-OPTICAL-ONLY-DELIVERY-CANDIDATE-E97-20261026-1';
const [pubPrefix,pubDir,out]=process.argv.slice(2);
if(!pubPrefix||!pubDir||!out)throw Error('publisher prefix, binding directory, NEW output directory required');
fs.mkdirSync(out);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),fileSha=p=>sha(fs.readFileSync(p));
const need=(p,m)=>{if(!p)throw Error(m)};
const git=(...a)=>cp.execFileSync('/usr/bin/git',a,{cwd:R,encoding:'utf8',env:{...process.env,GIT_OPTIONAL_LOCKS:'0',GIT_NO_LAZY_FETCH:'1'}}).trim();
const save=(n,v)=>fs.writeFileSync(path.join(out,n),JSON.stringify(v,null,2)+'\n');
const primary={
 '/workspace/chicago/.git/index':'195237adc725ac313d1bce7befc622cad8c54650218648c69eb781142c13f359',
 '/workspace/chicago/site/4d/tickets.json':'4e2514c9a1d70b7df3747d5c44a297c5331a3721186d6e9444368e8e8e30962b'};
const assets={
 'walk/transport/parked-brougham/brougham-near-delivery-v1.glb':'b5b183b4f115c5c7779ba0cb4ccba83fbffb62349647a9a6487f50cde49aef77',
 'walk/transport/parked-brougham/brougham-mid-delivery-v1.glb':'16daaf1d5003aae3ea64de9d037962aaabf2a5c8638ac77a5a2e037564ef2d63'};
const site=path.join(R,'site/4d'),errors=[],rows=[],responses=[],pending=new Set(),stages=[];
let browser,context,server,current='initial';
const started=Date.now();
const event=(v)=>fs.appendFileSync(path.join(out,'EVENTS.ndjson'),JSON.stringify({ms:Date.now()-started,...v})+'\n');
const error=v=>{errors.push(v);event({event:'error',...v})};
const stage=(s)=>{current=s;stages.push({stage:s,ms:Date.now()-started});save('STAGES.json',stages);event({event:'stage',stage:s})};
function source(){
 const s={head:git('rev-parse','HEAD'),candidate_tree:git('rev-parse','HEAD^{tree}'),
  candidate_APP:git('rev-parse',TREE+':chicago/4d'),primary:Object.fromEntries(Object.keys(primary).map(p=>[p,fileSha(p)]))};
 need(s.head===H&&s.candidate_tree===TREE&&!fs.existsSync(path.join(R,'.git/MERGE_HEAD')),'Exact preserved clean e97 required');
 need(!git('status','--porcelain'),'Unbound source changes');
 need(JSON.stringify(s.primary)===JSON.stringify(primary),'Primary source guard');return s;
}
const pr=JSON.parse(fs.readFileSync(pubPrefix+'.result.json')),pc=JSON.parse(fs.readFileSync(pubPrefix+'.cleanup.json'));
need(pr.returncode===0&&!pr.timed_out&&pc.cleanup_complete&&!pc.remaining_owned_children.length,'Publisher actual closure');
const pb=JSON.parse(fs.readFileSync(path.join(pubDir,'BINDING.json')));
need(pb.schema==='T3084-clean-e97-publisher-v1'&&pb.pass&&pb.head===H&&pb.candidate_tree===TREE&&pb.mirror===site,'Publisher frozen candidate binding');
need(fileSha(path.join(pubDir,pb.native_result))===pb.native_result_sha256,'Publisher native receipt hash');
const mp=path.join(pubDir,pb.manifest);need(fileSha(mp)===pb.manifest_sha256,'Publisher manifest hash');
const manifest=JSON.parse(fs.readFileSync(mp));
function mirror(){
 const found=[];
 for(const row of manifest){const p=path.resolve(site,row.path);need(p.startsWith(site+'/'),'Manifest containment');need(fs.statSync(p).size===row.bytes&&fileSha(p)===row.sha256,'Published byte changed '+row.path)}
 function walk(p){for(const d of fs.readdirSync(p,{withFileTypes:true})){const f=path.join(p,d.name);if(d.isDirectory())walk(f);else if(d.isFile())found.push(path.relative(site,f).split(path.sep).join('/'));else throw Error('Mirror special entry')}}walk(site);
 need(JSON.stringify(found.sort())===JSON.stringify(manifest.map(r=>r.path).sort()),'Mirror file set changed');
 return{count:manifest.length,manifest_sha256:pb.manifest_sha256};
}
// All override bytes are explicit external hypotheses. The native mirror is
// checked byte-for-byte before/after and is NEVER edited by this diagnostic.
const overrides=new Map();
const mainPath=path.join(site,'walk/js/main.js'),oldMain=fs.readFileSync(mainPath,'utf8');
const oldHead="fetch(url, { method: 'HEAD', cache: 'no-cache' }).then((r) => { known = r.ok; }, () => { known = false; });";
need(oldMain.split(oldHead).length===2,'Exact native HEAD source needed');
const proposedMain=oldMain.replace(oldHead,"fetch(url, { method: 'HEAD', cache: 'no-cache' }).then(async (r) => { await r.arrayBuffer(); known = r.ok; }).catch(() => { known = false; });");
need(proposedMain.includes('const GLESSNER_V4_FULL_TRIANGLES = 4600000;')&&proposedMain.includes('const GLESSNER_V4_LIGHT_TRIANGLES = 1270000;'),'Original Full/Light declaration retained');
overrides.set('walk/js/main.js',Buffer.from(proposedMain));
const placements=JSON.parse(fs.readFileSync(path.join(site,'data/transport/parked/placements.json')));
const spec=placements.models.studebaker_brougham_1893;
need(spec.file==='transport/parked-brougham/brougham-near.glb'&&spec.delivery_lods.mid==='transport/parked-brougham/brougham-mid.glb','Exact physical placement paths');
spec.file=spec.delivery_lods.near='transport/parked-brougham/brougham-near-delivery-v1.glb';
spec.delivery_lods.mid='transport/parked-brougham/brougham-mid-delivery-v1.glb';
overrides.set('data/transport/parked/placements.json',Buffer.from(JSON.stringify(placements)));
for(const [rel,digest]of Object.entries(assets)){
 const data=fs.readFileSync(path.join(C,path.basename(rel)));need(sha(data)===digest,'Actual optical-only payload binding');overrides.set(rel,data);
}
const overrideManifest=[...overrides].map(([path,b])=>({path,bytes:b.length,sha256:sha(b)}));
save('EXPLICIT-EXTERNAL-OVERRIDES.json',{scope:'Unadopted optical-only GLBs/placement plus HEAD consumption; native budgets unchanged; mirror unchanged',candidate:C,overrides:overrideManifest});
function checkOverrides(){for(const [rel,digest]of Object.entries(assets))need(fileSha(path.join(C,path.basename(rel)))===digest,'External optical payload changed')}
checkOverrides();
save('BEFORE.json',{source:source(),mirror:mirror(),publisher:pb});
const drain=async()=>{while(pending.size)await Promise.allSettled([...pending])};
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.glb':'model/gltf-binary','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.ktx2':'image/ktx2','.woff2':'font/woff2'};
(async()=>{try{
 server=http.createServer((q,r)=>{
  let rel;try{rel=decodeURIComponent(new URL(q.url,'http://localhost').pathname)}catch{r.writeHead(400);r.end();return}
  let p=path.resolve(site,'.'+rel);if(!p.startsWith(site+'/')&&p!==site){r.writeHead(403);r.end();return}
  const external=overrides.get(rel.slice(1));if(external){r.writeHead(200,{'content-type':types[path.extname(p)]||'application/octet-stream'});r.end(q.method==='HEAD'?undefined:external);return}
  if(q.method==='HEAD'){event({event:'serverHEAD',method:q.method,path:rel});r.on('finish',()=>event({event:'serverHEADfinished',path:rel}));q.on('aborted',()=>event({event:'serverHEADaborted',path:rel}))}
  try{if(fs.statSync(p).isDirectory())p=path.join(p,'index.html');fs.readFile(p,(e,b)=>{r.writeHead(e?404:200,{'content-type':types[path.extname(p)]||'application/octet-stream'});r.end(e?'missing':b)})}catch{r.writeHead(404);r.end()}
 });
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 for(const v of[{name:'phone',width:390,height:780,mobile:true,dpr:3},{name:'desktop',width:1280,height:800,mobile:false,dpr:1}]){
  stage(v.name+'/launch');browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
  context=await browser.newContext({viewport:{width:v.width,height:v.height},isMobile:v.mobile,hasTouch:v.mobile,deviceScaleFactor:v.dpr});
  const page=await context.newPage();page.setDefaultTimeout(90000);
  page.on('pageerror',e=>error({kind:'pageerror',viewport:v.name,stage:current,message:e.message}));
  page.on('console',m=>{if(m.type()==='error')error({kind:'console',viewport:v.name,stage:current,message:m.text()})});
  page.on('requestfailed',q=>error({kind:'requestfailed',viewport:v.name,stage:current,method:q.method(),url:q.url(),failure:q.failure()}));
  page.on('requestfinished',q=>{if(q.method()==='HEAD')event({event:'HEADfinished',viewport:v.name,url:q.url()})});
  page.on('response',r=>{
   const u=new URL(r.url()),rel=u.pathname.slice(1);
   if(r.status()>=400)error({kind:'HTTP',viewport:v.name,stage:current,method:r.request().method(),path:u.pathname,status:r.status()});
   if(r.request().method()==='HEAD')event({event:'HEADresponse',viewport:v.name,status:r.status(),url:r.url()});
   if(u.origin!==origin||!Object.hasOwn(assets,rel))return;
   let task;task=(async()=>{const b=await r.body();const x={viewport:v.name,path:rel,status:r.status(),bytes:b.length,sha256:sha(b)};responses.push(x);need(x.status===200&&x.sha256===assets[rel],'Actual selected asset response')})().catch(e=>error({kind:'body-read',message:String(e)})).finally(()=>pending.delete(task));pending.add(task);
  });
  stage(v.name+'/boot');await page.goto(origin+'/1904/',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:420000,polling:100});
  need(await page.evaluate(()=>!window.__chicago4d.error&&String(window.__chicago4d.scene.id)==='1904'),'1904 actual boot');
  // The repository's native holdDraws, ONLY for operations reading no pixel.
  // Placement uses its separately retained real renderer. All measured frames
  // and photographs run after the real renderer has been restored.
  stage(v.name+'/nonpixel-setup');
  await page.evaluate(()=>{const a=window.__chicago4d;window.__t3084HeldRender=a.renderer.render;a.renderer.render=()=>{}});
  try{
   const roam=page.locator('#home-roam');await roam.waitFor({state:'visible'});await roam.click({trial:true});await roam.click();
   await page.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:90000,polling:100});
   // The native enterTown helper dismisses the first-entry controls card too.
   // Use its real visitor button so the diagnostic photographs the carriage.
   if(await page.locator('#control-help').isVisible()){
    const gotit=page.locator('#control-help-gotit');await gotit.click({trial:true});await gotit.click();
   }
   await page.evaluate(async()=>{const a=window.__chicago4d;await a.setDetail('full');await a.parkedTransport.setTier('full');a.setAnimationHold(true);a.renderer.setAnimationLoop(null);a.setFly(false)});
  }finally{
   await page.evaluate(()=>{const a=window.__chicago4d;if(window.__t3084HeldRender){a.renderer.render=window.__t3084HeldRender;delete window.__t3084HeldRender}});
  }
  const nativeStands=[
   {name:'quarter',kind:'carriage',distance:6},
   {name:'body-detail',kind:'carriage',distance:2.6},
   // Coordinates exact from native tools/qa_glessner_t2219.mjs.
   {name:'service-junction',kind:'glessner',position:[6,31,1.7],target:[11,22.5,4.5]},
   {name:'service-front',kind:'glessner',position:[11.5,32,1.7],target:[11.5,22.5,4.5]},
   {name:'roof-junction',kind:'glessner',position:[20,32,16],target:[10,18,9]},
   // Exact district_air walker pose from native measure_detail_ceilings.mjs.
   {name:'district-air',kind:'pose',pose:{local_e:1360,local_n:-3620,altitude_m:110,yaw_deg:-23.2,pitch_deg:-35.8}},
  ];
  save('NATIVE-STAND-DEFINITIONS.json',nativeStands);
  for(const level of ['full','light']){
   stage(v.name+'/'+level+'/nonpixel-tier');
   await page.evaluate(()=>{const a=window.__chicago4d;window.__t3084HeldRender=a.renderer.render;a.renderer.render=()=>{}});
   try{await page.evaluate(async level=>{const a=window.__chicago4d;await a.setDetail(level);await a.parkedTransport.setTier(level);a.setAnimationHold(true);a.renderer.setAnimationLoop(null)},level)}
   finally{await page.evaluate(()=>{const a=window.__chicago4d;if(window.__t3084HeldRender){a.renderer.render=window.__t3084HeldRender;delete window.__t3084HeldRender}})}
   for(const stand of nativeStands){
    stage(v.name+'/'+level+'/'+stand.name);
    const row=await page.evaluate(({stand,level})=>{
     const a=window.__chicago4d,i=a.parkedTransport.instances.find(x=>x.row.id==='prairie_parked_studebaker_brougham');
     if(!i)throw Error('Missing carriage');let exactCamera=null;
     if(stand.kind==='carriage'){
      a.setFly(false);const theta=i.group.rotation.y+Math.PI/4,target={x:i.group.position.x,y:i.group.position.y+1.1,z:i.group.position.z};
      const x=target.x+Math.sin(theta)*stand.distance,z=target.z+Math.cos(theta)*stand.distance;
      a.walker.teleport({local_e:x,local_n:-z,yaw_deg:Math.atan2(target.x-x,-(target.z-z))*180/Math.PI,pitch_deg:-5});
     }else if(stand.kind==='pose'){a.setFly(true);a.walker.teleport(stand.pose)}
     else{
      const pl=a.registry.get('glessner_house').sidecar.placement,theta=pl.rotation_deg*Math.PI/180,ground=a.terrain.surfaceHeight(pl.local_e,pl.local_n);
      const en=([x,y,z])=>[pl.local_e+x*Math.cos(theta)+y*Math.sin(theta),pl.local_n-x*Math.sin(theta)+y*Math.cos(theta),ground+z];
      const p=en(stand.position),t=en(stand.target);a.setFly(true);exactCamera={position:p,target:t};
      a.walker.teleport({local_e:p[0],local_n:p[1],altitude_m:p[2]-a.terrain.surfaceHeight(p[0],p[1]),yaw_deg:Math.atan2(t[0]-p[0],t[1]-p[1])*180/Math.PI,pitch_deg:Math.atan2(t[2]-p[2],Math.hypot(t[0]-p[0],t[1]-p[1]))*180/Math.PI});
     }
     if(window.__t3084HeldRender)throw Error('Drawing is held during measured frame');
     const gl=a.renderer.getContext(),pixel=new Uint8Array(4),ms=[];
     for(let k=0;k<2;k++){
      const start=performance.now();if(k===0||!exactCamera)a.step();
      if(exactCamera){
       // Exact native qa_glessner_t2219 camera after its walker/step update.
       // surfaceAt may include a deck above terrain; the native QA overrides
       // the eye explicitly so these remain its exact fixed source viewpoints.
       const p=exactCamera.position,t=exactCamera.target;a.camera.position.set(p[0],p[2],-p[1]);a.camera.lookAt(t[0],t[2],-t[1]);a.camera.updateMatrixWorld();a.world.follow(a.camera.position);a.world.aim(a.camera);a.renderer.render(a.scene3d,a.camera);
      }
      gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,pixel);ms.push(performance.now()-start);
     }
     const lods=i.lod.levels.map(l=>{let triangles=0,batches=0;const materials=[];l.object.traverse(n=>{if(n.isMesh){batches++;triangles+=(n.geometry.index?.count??n.geometry.attributes.position.count)/3;materials.push({name:n.material.name,transmission:n.material.transmission||0,opacity:n.material.opacity,transparent:n.material.transparent,depthWrite:n.material.depthWrite,ior:n.material.ior,side:n.material.side})}});return{triangles,batches,materials,visible:l.object.visible,distance:l.distance,hysteresis:l.hysteresis}});
     const target={x:i.group.position.x,y:i.group.position.y+1.1,z:i.group.position.z},projected=a.project(target.x,-target.z,target.y);
     return{profile:'external-optical-only-geometry-exact-hypothesis',pose:stand.name,kind:stand.kind,level,actual_detail:a.detail,stats:a.stats(),frame_ms:ms,lods,active_lod:i.active_lod,registered_triangles:i.active_triangles,
      projected,target_vehicle_pick:a.parkedTransport.pickAt(projected,a.camera)?.id,static_support:i.static_support,wheel_clearance_m:i.wheel_clearance_m,visible:i.group.visible,problems:a.problems,
      player:{...a.player},native_exact_camera:exactCamera,camera:{position:a.camera.position.toArray(),quaternion:a.camera.quaternion.toArray(),fov:a.camera.fov,zoom:a.camera.zoom,drawingHeight:a.renderer.domElement.height},
      production_shadows:{enabled:a.renderer.shadowMap.enabled,type:a.renderer.shadowMap.type,reachM:a.world.shadowRig.reachM,texelM:a.world.shadowRig.texelM},detail_policies:a.detailLevels};
    },{stand,level});
    row.viewport=v.name;row.screenshot=`${v.name}-${level}-${stand.name}.png`;rows.push(row);
    // Keep actual over-budget photographs before any assertion or proposal.
    await page.screenshot({path:path.join(out,row.screenshot),timeout:90000});
    save('PROGRESS.json',{scope:'External optical-only diagnostic, no app or cap edits',rows,errors,responses});
    if(!row.stats.withinBudget)event({event:'native-budget-red',viewport:v.name,level,pose:stand.name,triangles:row.stats.triangles,drawCalls:row.stats.drawCalls,budget:row.stats.budget});
    need(row.actual_detail===level,'Actual tier selection');
    if(row.native_exact_camera){const p=row.native_exact_camera.position;need(row.camera.position.every((v,k)=>Math.abs(v-[p[0],p[2],-p[1]][k])<1e-8),'Exact native Glessner fixed camera after real frames')}
    need(row.stats.budget.triangles===(level==='full'?4600000:1270000)&&row.stats.budget.drawCalls===7800,'Original selected-inspection tier ceilings retained');
    need(row.detail_policies.light.triangles===1270000&&row.detail_policies.balanced.triangles===2625000&&row.detail_policies.full.triangles===4600000,'Exact existing tier ladder');
    need(row.lods.length===2&&row.lods[0].triangles===45338&&row.lods[1].triangles===23062&&row.lods.every(l=>l.batches===8),'Physical geometry/8batch contract');
    need(row.lods[1].hysteresis===.05,'Native hysteresis');
    for(const lod of row.lods){const m=lod.materials.find(m=>m.name==='thin_sheet_cabin_glass_delivery_reconstruction');need(m&&m.transmission===0&&m.opacity===.14&&m.transparent&&!m.depthWrite&&m.ior===1.5,'Actual portable alpha optical profile')}
    need(row.problems.length===0,'Actual app problems');
    need(row.static_support.minimum_gap_m>=-.001&&row.static_support.maximum_gap_m<=.03&&row.wheel_clearance_m<=.03,'Native contact/clearance limits');
    if(level==='light')need(!row.visible,'Original Light zero-carriage-reach policy');
    else if(stand.kind==='carriage')need(row.visible&&row.active_lod==='near'&&row.target_vehicle_pick==='prairie_parked_studebaker_brougham','Visible/pickable actual Full near carriage');
   }
  }
  // Restore tier without drawing suppressed pixels as measurements.
  stage(v.name+'/nonpixel-restore-full');
  await page.evaluate(()=>{const a=window.__chicago4d;window.__t3084HeldRender=a.renderer.render;a.renderer.render=()=>{}});
  try{await page.evaluate(async()=>{const a=window.__chicago4d;await a.setDetail('full');await a.parkedTransport.setTier('full')})}
  finally{await page.evaluate(()=>{const a=window.__chicago4d;if(window.__t3084HeldRender){a.renderer.render=window.__t3084HeldRender;delete window.__t3084HeldRender}})}
  need(await page.evaluate(()=>{const a=window.__chicago4d;return a.detail==='full'&&a.budget.triangles===4600000&&a.detailLevels.light.triangles===1270000}),'Full/Light budget round-trip restoration');
  await context.close();context=null;await browser.close();browser=null;await drain();
 }
 }catch(e){error({kind:'diagnostic',stage:current,message:String(e),stack:e.stack})}finally{
  if(context)try{await context.close()}catch(e){error({kind:'context-close',message:String(e)})}
  if(browser)try{await browser.close()}catch(e){error({kind:'browser-close',message:String(e)})}
  await drain();if(server)await new Promise(r=>server.close(r));
  try{save('AFTER.json',{source:source(),mirror:mirror()})}catch(e){error({kind:'source-mirror-final',message:String(e)})}
  try{checkOverrides()}catch(e){error({kind:'override-final',message:String(e)})}
  const result={scope:'External optical-only e97 hypothesis; geometry exact; native caps unchanged; NO shipping source/whole-gate/photo acceptance',head:H,candidate_tree:TREE,
   rows,errors,responses,stages,pending_body_tasks:pending.size,diagnostic_complete:rows.length===24,
   source_adoption:false,current_candidate_qualified:false,full_gate:'NOT RUN',
   full_budget_red:rows.filter(x=>x.level==='full'&&!x.stats.withinBudget).length,
   light_budget_red:rows.filter(x=>x.level==='light'&&!x.stats.withinBudget).length};
  save('RESULT.json',result);console.log(JSON.stringify({diagnostic_complete:result.diagnostic_complete,rows:rows.length,errors:errors.length,full_budget_red:result.full_budget_red,light_budget_red:result.light_budget_red,current_candidate_qualified:false,output:out}));
  process.exitCode=errors.length||!result.diagnostic_complete||result.full_budget_red||result.light_budget_red?1:0;

 }
})().catch(e=>{console.error(e);process.exitCode=1});
