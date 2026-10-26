// Diagnostic only: current physical glass versus a delivery hypothesis.
// Hypothesis frames are not actual shipping-runtime or HEAD qualification.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const cp=require('node:child_process'),http=require('node:http');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const R='/tmp/chicago-photo-worker-t3084-20261026',H='5ea4a9851c8b8a56ca6736175c6bdf030b31743c';
const B='a575dddeed356333423b20361a1f90f3b39a862f',TREE='f3a628daf61327fc1adc2bf3efab44b83cb634cd';
const [pubPrefix,pubDir,out]=process.argv.slice(2);
if(!pubPrefix||!pubDir||!out)throw Error('publisher prefix, binding directory, NEW output directory required');
fs.mkdirSync(out);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),fileSha=p=>sha(fs.readFileSync(p));
const need=(p,m)=>{if(!p)throw Error(m)};
const git=(...a)=>cp.execFileSync('git',a,{cwd:R,encoding:'utf8',env:{...process.env,GIT_OPTIONAL_LOCKS:'0'}}).trim();
const save=(n,v)=>fs.writeFileSync(path.join(out,n),JSON.stringify(v,null,2)+'\n');
const primary={
 '/workspace/chicago/.git/index':'195237adc725ac313d1bce7befc622cad8c54650218648c69eb781142c13f359',
 '/workspace/chicago/site/4d/tickets.json':'4e2514c9a1d70b7df3747d5c44a297c5331a3721186d6e9444368e8e8e30962b'};
const assets={
 'walk/transport/parked-brougham/brougham-near.glb':'3d2f3a802f4b32dba6a3e61f2c188dddce4db05cecfcbba81e1e8d369d5dfe89',
 'walk/transport/parked-brougham/brougham-mid.glb':'d5cdd34e981d29db41634ac780c22526742f6a20527b5866d2349c727a67400d'};
const site=path.join(R,'site/4d'),errors=[],rows=[],responses=[],pending=new Set(),stages=[];
let browser,context,server,current='initial';
const started=Date.now();
const event=(v)=>fs.appendFileSync(path.join(out,'EVENTS.ndjson'),JSON.stringify({ms:Date.now()-started,...v})+'\n');
const error=v=>{errors.push(v);event({event:'error',...v})};
const stage=(s)=>{current=s;stages.push({stage:s,ms:Date.now()-started});save('STAGES.json',stages);event({event:'stage',stage:s})};
function source(){
 const s={head:git('rev-parse','HEAD'),MERGE_HEAD:git('rev-parse','MERGE_HEAD'),candidate_tree:git('write-tree'),
  candidate_APP:git('rev-parse',TREE+':chicago/4d'),primary:Object.fromEntries(Object.keys(primary).map(p=>[p,fileSha(p)]))};
 need(s.head===H&&s.MERGE_HEAD===B&&s.candidate_tree===TREE,'Exact frozen WIP candidate required');
 need(!git('diff','--name-only')&&!git('ls-files','--others','--exclude-standard','--','chicago/4d'),'Unbound source changes');
 need(JSON.stringify(s.primary)===JSON.stringify(primary),'Primary source guard');return s;
}
const pr=JSON.parse(fs.readFileSync(pubPrefix+'.result.json')),pc=JSON.parse(fs.readFileSync(pubPrefix+'.cleanup.json'));
need(pr.returncode===0&&!pr.timed_out&&pc.cleanup_complete&&!pc.remaining_owned_children.length,'Publisher actual closure');
const pb=JSON.parse(fs.readFileSync(path.join(pubDir,'BINDING.json')));
need(pb.schema==='T3084-exact-working-tree-publisher-v1'&&pb.pass&&pb.head===H&&pb.MERGE_HEAD===B&&pb.candidate_tree===TREE&&pb.mirror===site,'Publisher frozen candidate binding');
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
for(const [p,s]of Object.entries(assets))need(fileSha(path.join(site,p))===s,'Actual selected GLB binding');
save('BEFORE.json',{source:source(),mirror:mirror(),publisher:pb});
const drain=async()=>{while(pending.size)await Promise.allSettled([...pending])};
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.glb':'model/gltf-binary','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.ktx2':'image/ktx2','.woff2':'font/woff2'};
(async()=>{try{
 server=http.createServer((q,r)=>{
  let rel;try{rel=decodeURIComponent(new URL(q.url,'http://localhost').pathname)}catch{r.writeHead(400);r.end();return}
  let p=path.resolve(site,'.'+rel);if(!p.startsWith(site+'/')&&p!==site){r.writeHead(403);r.end();return}
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
  const originals=await page.evaluate(()=>{
   const a=window.__chicago4d,i=a.parkedTransport.instances.find(x=>x.row.id==='prairie_parked_studebaker_brougham');if(!i)throw Error('Carriage missing');
   const m=new Set();i.group.traverse(n=>{if(n.isMesh&&n.material.name==='thin_physical_cabin_glass_reconstruction')m.add(n.material)});
   if(m.size!==2)throw Error('Expected exact near+mid cabin materials');
   window.__t3084Glass=[...m].map(m=>({m,values:{transmission:m.transmission,transparent:m.transparent,opacity:m.opacity,depthWrite:m.depthWrite,ior:m.ior,side:m.side,roughness:m.roughness}}));
   return window.__t3084Glass.map(x=>x.values);
  });save(v.name+'-ORIGINAL-MATERIALS.json',originals);
  try{for(const profile of['physical-current-source','alpha-delivery-hypothesis']){
   await page.evaluate(p=>{for(const x of window.__t3084Glass){Object.assign(x.m,x.values);if(p==='alpha-delivery-hypothesis')Object.assign(x.m,{transmission:0,transparent:true,opacity:.14,depthWrite:false});x.m.needsUpdate=true}},profile);
   for(const pose of['quarter','body-detail']){
    stage(v.name+'/'+profile+'/'+pose);
    const row=await page.evaluate(({profile,pose})=>{
     const a=window.__chicago4d,i=a.parkedTransport.instances.find(x=>x.row.id==='prairie_parked_studebaker_brougham');
     const d=pose==='body-detail'?2.6:6,t=i.group.rotation.y+Math.PI/4;
     const target={x:i.group.position.x,y:i.group.position.y+1.1,z:i.group.position.z};
     const x=target.x+Math.sin(t)*d,z=target.z+Math.cos(t)*d,yaw=Math.atan2(target.x-x,-(target.z-z))*180/Math.PI;
     a.walker.teleport({local_e:x,local_n:-z,yaw_deg:yaw,pitch_deg:-5});
     const gl=a.renderer.getContext(),pixel=new Uint8Array(4),ms=[];
     for(let k=0;k<2;k++){const start=performance.now();a.step();gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,pixel);ms.push(performance.now()-start)}
     let triangles=0,batches=0;const materials=[];i.lod.levels[i.lod.getCurrentLevel()].object.traverse(n=>{if(n.isMesh){batches++;triangles+=(n.geometry.index?.count??n.geometry.attributes.position.count)/3;materials.push({name:n.material.name,transmission:n.material.transmission||0,opacity:n.material.opacity,transparent:n.material.transparent,depthWrite:n.material.depthWrite,ior:n.material.ior,side:n.material.side})}});
     const projected=a.project(target.x,-target.z,target.y);
     return{profile,pose,stats:a.stats(),frame_ms:ms,active_lod:i.active_lod,decoded_triangles:triangles,batches,materials,projected,target_vehicle_pick:a.parkedTransport.pickAt(projected,a.camera)?.id,static_support:i.static_support,wheel_clearance_m:i.wheel_clearance_m,visible:i.group.visible,problems:a.problems,player:{...a.player},camera:{position:a.camera.position.toArray(),quaternion:a.camera.quaternion.toArray(),fov:a.camera.fov,drawingHeight:a.renderer.domElement.height},production_shadows:{enabled:a.renderer.shadowMap.enabled,type:a.renderer.shadowMap.type}};
    },{profile,pose});
    row.viewport=v.name;row.screenshot=`${v.name}-${profile}-${pose}.png`;rows.push(row);
    // Capture existing red frames too; failure is retained, not hidden by an
    // assertion that discards the image needed to diagnose the failure.
    await page.screenshot({path:path.join(out,row.screenshot),timeout:90000});
    save('PROGRESS.json',{scope:'Diagnostic only; hypothesis not shipping runtime',rows,errors,responses});
    if(!row.stats.withinBudget)event({event:'native-budget-red',viewport:v.name,profile,pose,drawCalls:row.stats.drawCalls,triangles:row.stats.triangles,budget:row.stats.budget});
    need(row.active_lod==='near'&&row.decoded_triangles===45338&&row.batches===8,'Exact selected source geometry changed');
    need(row.visible&&row.target_vehicle_pick==='prairie_parked_studebaker_brougham','Actual visible/pickable carriage');
    need(row.problems.length===0,'Actual app problems');
    need(row.static_support.minimum_gap_m>=-.001&&row.static_support.maximum_gap_m<=.03,'Actual static contacts');
   }
  }}finally{
  const restored=await page.evaluate(()=>{for(const x of window.__t3084Glass){Object.assign(x.m,x.values);x.m.needsUpdate=true}return window.__t3084Glass.map(x=>Object.fromEntries(Object.keys(x.values).map(k=>[k,x.m[k]])))});
  need(JSON.stringify(restored)===JSON.stringify(originals),'Original physical materials not restored');save(v.name+'-RESTORED-MATERIALS.json',restored);
  }
  await context.close();context=null;await browser.close();browser=null;await drain();
 }
 }catch(e){error({kind:'diagnostic',stage:current,message:String(e),stack:e.stack})}finally{
  if(context)try{await context.close()}catch(e){error({kind:'context-close',message:String(e)})}
  if(browser)try{await browser.close()}catch(e){error({kind:'browser-close',message:String(e)})}
  await drain();if(server)await new Promise(r=>server.close(r));
  try{save('AFTER.json',{source:source(),mirror:mirror()})}catch(e){error({kind:'source-mirror-final',message:String(e)})}
  const result={scope:'Explicit glass rendering diagnostic on exact uncommitted source; hypothesis pixels are not shipping runtime/HEAD/APP qualification',head:H,candidate_tree:TREE,
   rows,errors,responses,stages,pending_body_tasks:pending.size,diagnostic_complete:rows.length===8,
   current_candidate_qualified:false,full_gate:'NOT RUN',hypothesis:'transmission0, transparent, opacity0.14, depthWritefalse; geometry/otheroptics/light/camera unchanged',
   physical_budget_red:rows.filter(x=>x.profile==='physical-current-source'&&!x.stats.withinBudget).length,
   hypothesis_budget_red:rows.filter(x=>x.profile==='alpha-delivery-hypothesis'&&!x.stats.withinBudget).length};
  save('RESULT.json',result);console.log(JSON.stringify({diagnostic_complete:result.diagnostic_complete,rows:rows.length,errors:errors.length,physical_budget_red:result.physical_budget_red,hypothesis_budget_red:result.hypothesis_budget_red,source_candidate_qualified:false,output:out}));
  process.exitCode=errors.length||!result.diagnostic_complete||result.physical_budget_red||result.hypothesis_budget_red?1:0;
 }
})().catch(e=>{console.error(e);process.exitCode=1});
