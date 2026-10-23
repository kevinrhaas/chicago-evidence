// HELD: one finite phase; existing owned-process supervisor handles deadlines/cleanup.
import fs from 'node:fs/promises';import path from 'node:path';import crypto from 'node:crypto';
import {createServer} from 'node:http';import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),args=process.argv.slice(2);
if(args.length!==4||args[0]!=='--lane-released'||!['materials','yard-desktop','yard-mobile'].includes(args[1]))throw Error('Require one explicit released phase');
const phase=args[1],cfg=JSON.parse(await fs.readFile(args[2],'utf8')),out=path.resolve(args[3]);
if(cfg.released!==true||cfg.browser_lane_free!==true||cfg.phase!==phase||!Object.keys(cfg.expected_files??{}).length)throw Error('HELD: root release and exact phase/input pins required');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const [file,hash]of Object.entries(cfg.expected_files))if(sha(await fs.readFile(file))!==hash)throw Error('Input changed: '+file);
const model=await fs.readFile(cfg.source_model);if(model.length!==3211248||sha(model)!=='41acd9bee7bf05fbcdd813fad965027b01b8801d6a21ca1c22eb2178c8842988')throw Error('Unchanged licensed source pin mismatch');
await fs.mkdir(out,{recursive:false});
const report={phase,scope:'Development-base static smoke only, no photographic/anatomical/continuous-contact/ride/hitch/phone-hardware acceptance',pass:false,errors:[],requests:[],captures:[],inputPins:cfg.expected_files,started:new Date().toISOString()};
let server,browser,page;
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.bin':'application/octet-stream','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.css':'text/css','.wasm':'application/wasm','.svg':'image/svg+xml','.md':'text/markdown'};
try{
 const app='/workspace/chicago/chicago/4d',vendor=path.join(app,'renderers/web/vendor');
 server=createServer(async(req,res)=>{try{
  const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204);return res.end();}
  let file,bytes;
  if(phase==='materials'){
   if(u.pathname==='/fixture/')file=path.join(here,'materials.html');
   else if(u.pathname==='/fixture/materials.js')file=path.join(here,'materials.js');
   else if(u.pathname==='/transport/standing-horse/horse-sevket-native.glb')file=cfg.source_model;
   else if(u.pathname.startsWith('/vendor/')){file=path.resolve(vendor,u.pathname.slice(8));if(!file.startsWith(vendor+'/'))throw Error('Path');}
   else if(u.pathname.startsWith('/runtime/')){const name=u.pathname.slice(9);if(name.includes('/')||name.includes('..'))throw Error('Path');file=name==='standing-horses.js'?path.join(cfg.proposal_root,'renderers/web/js',name):path.join(app,'renderers/web/js',name);}
   else{const m=u.pathname.match(/^\/case\/(source_native|organic_dielectric_v1)\/data\/transport\/parked\/(standing-horses|horse-sevket-sidecar)\.json$/);if(!m)throw Error('Route');file=path.join(cfg.proposal_root,'data/transport/parked',m[2]+'.json');if(m[2]==='standing-horses'){const j=JSON.parse(await fs.readFile(file,'utf8'));j.scenes['1835'][0].material_variant=m[1];bytes=Buffer.from(JSON.stringify(j));}}
  }else{
   file=path.resolve(cfg.site_root,'.'+decodeURIComponent(u.pathname));if(!file.startsWith(cfg.site_root+'/'))throw Error('Path');if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');
  }
  bytes??=await fs.readFile(file);res.writeHead(200,{'Content-Type':mime[path.extname(file)]??'application/octet-stream','Cache-Control':'no-store'});res.end(bytes);
 }catch{res.writeHead(404);res.end('Unavailable');}});
 await new Promise((r,j)=>{server.once('error',j);server.listen(0,'127.0.0.1',r);});const origin='http://127.0.0.1:'+server.address().port;
 const {chromium}=await import('/workspace/shared/chicago-browser/node_modules/playwright/index.mjs');
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const mobile=phase==='yard-mobile';page=await browser.newPage({viewport:mobile?{width:390,height:780}:{width:1280,height:800},deviceScaleFactor:mobile?2:1,hasTouch:mobile,isMobile:mobile,reducedMotion:'reduce'});
 page.setDefaultTimeout(45000);page.on('pageerror',e=>report.errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)report.errors.push(`HTTP${r.status()} ${r.url()}`);});page.on('request',r=>{if(r.url().includes('horse-sevket-native.glb'))report.requests.push(r.url());});
 const shot=async(name,state)=>{const file=name+'.png',bytes=await page.screenshot({path:path.join(out,file)});report.captures.push({file,sha256:sha(bytes),state});await fs.writeFile(path.join(out,'progress.json'),JSON.stringify(report,null,2)+'\n');};
 // Same actual indexed-vertex readback for fixture and town; no fitting/reposing.
 const snapshot=async(kind)=>page.evaluate(async kind=>{
  const a=window.__chicago4d,f=window.fixture,layer=kind==='materials'?f.layer:a.standingHorses,camera=kind==='materials'?f.camera:a.camera;
  const i=layer.instances[0];if(!i)throw Error('Missing standing horse');const T=await import('three'),p=new T.Vector3(),b=new T.Box3();
  let count=0,clipped=0;const ndc={min:[Infinity,Infinity,Infinity],max:[-Infinity,-Infinity,-Infinity]},meshes=[];
  i.root.updateMatrixWorld(true);camera.updateMatrixWorld(true);
  i.root.traverse(m=>{if(!m.isMesh)return;if(!m.isSkinnedMesh||!m.visible||m.skeleton.bones.length!==15)throw Error('Lost actual source mesh/skin');m.skeleton.update();const ids=new Set(m.geometry.index.array);for(const id of ids){m.getVertexPosition(id,p).applyMatrix4(m.matrixWorld);b.expandByPoint(p);p.project(camera);count++;if(!p.toArray().every(Number.isFinite)||Math.abs(p.x)>.97||Math.abs(p.y)>.97||p.z< -1||p.z>1)clipped++;for(let k=0;k<3;k++){ndc.min[k]=Math.min(ndc.min[k],p.getComponent(k));ndc.max[k]=Math.max(ndc.max[k],p.getComponent(k));}}meshes.push({name:m.name,bones:m.skeleton.bones.length,vertices:m.geometry.attributes.position.count,metalness:m.material.metalness,confidence_values:Array.from(new Set(m.geometry.attributes._confidence.array)),scale:m.scale.toArray()});});
  if(meshes.length!==3||clipped)throw Error('Actual source groups missing/clipped in fixed view; no camera adaptation: '+JSON.stringify({clipped,ndc}));
  const renderer=kind==='materials'?f.renderer:a.renderer;if(renderer.getContext().getError()!==0)throw Error('WebGL error');
  return{indexed_vertices:count,projected_bounds:ndc,world_bounds:[b.min.toArray(),b.max.toArray()],meshes,clips:i.asset.animations.map(c=>c.name),receipt:i.receipt,camera:{position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),fov:camera.fov},stats:kind==='materials'?{draws:renderer.info.render.calls,triangles:renderer.info.render.triangles}:a.stats()};
 },kind);
 if(phase==='materials'){
  for(const variant of ['source_native','organic_dielectric_v1']){
   await page.goto(origin+'/fixture/?variant='+variant,{waitUntil:'networkidle',timeout:45000});await page.waitForFunction(()=>window.fixture?.ready);
   for(const view of ['side','three-quarter']){await page.evaluate(view=>window.fixture.setView(view),view);await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const state=await snapshot('materials');if(state.meshes.some(m=>m.metalness!==(variant==='source_native'?1:0)))throw Error('Undeclared material response');await shot(variant+'-'+view,state);}
   await page.evaluate(()=>window.fixture.layer.dispose());
  }
 }else{
  const initial=mobile?'light':'full';await page.addInitScript(detail=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail})),initial);
  await page.goto(origin+'/walk/?year=1835',{waitUntil:'domcontentloaded',timeout:45000});await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240000,polling:1000});
  await page.evaluate(()=>{const a=window.__chicago4d;if(!a.ready||a.error||!a.standingHorses)throw Error('Actual new layer not ready');if(a.welcome.state==='welcome')a.welcome.enter('spawn');});
  await page.waitForFunction(()=>{const w=window.__chicago4d?.welcome;if(w?.state==='welcome')w.enter('spawn');return w?.state==='world';},null,{timeout:30000,polling:100});if(report.requests.length)throw Error('Far spawn fetched horse GLB');
  report.initial=await page.evaluate(()=>({detail:window.__chicago4d.detail,coarse:matchMedia('(pointer:coarse)').matches,instances:window.__chicago4d.standingHorses.instances.length}));
  const views=mobile?{side:{local_e:-127.5,local_n:-289.5,yaw_deg:180,pitch_deg:-7},quarter:{local_e:-123.1,local_n:-291.6,yaw_deg:225,pitch_deg:-7}}:{side:{local_e:-127.5,local_n:-291.4,yaw_deg:180,pitch_deg:-12},quarter:{local_e:-124.9,local_n:-293.4,yaw_deg:225,pitch_deg:-12}};
  if(mobile){await page.evaluate(p=>{const a=window.__chicago4d;a.setFly(false);a.walker.teleport(p);a.step();},views.side);if(report.requests.length)throw Error('Light near stand fetched horse GLB');await page.evaluate(async()=>{const a=window.__chicago4d;await a.setDetail('balanced');a.step();await a.standingHorses.ready;});}
  for(const [name,camera]of Object.entries(views)){
   await page.evaluate(async p=>{const a=window.__chicago4d;a.setFly(false);a.walker.teleport(p);a.step();await a.standingHorses.ready;},camera);
   await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const state=await snapshot('yard');if(!state.stats.withinBudget)throw Error('Existing public render budget exceeded');await shot(name,state);
  }
  report.ground=await page.evaluate(async()=>{
   const a=window.__chicago4d,T=await import('three'),i=a.standingHorses.instances[0],spec=await fetch(new URL('transport/parked/horse-sevket-sidecar.json',a.dataBase)).then(r=>r.json());
   const body=i.root.getObjectByName(spec.contact_mesh.renderer_name),p=new T.Vector3(),feet={};i.root.updateMatrixWorld(true);body.skeleton.update();
   for(const [name,patch]of Object.entries(spec.contacts)){const values=[];for(const fi of patch.source_triangle_ids){const v=[];for(let j=0;j<3;j++){body.getVertexPosition(body.geometry.index.getX(fi*3+j),p).applyMatrix4(body.matrixWorld);v.push(p.clone());}for(const q of [...v,v[0].clone().add(v[1]).multiplyScalar(.5),v[1].clone().add(v[2]).multiplyScalar(.5),v[2].clone().add(v[0]).multiplyScalar(.5),v[0].clone().add(v[1]).add(v[2]).multiplyScalar(1/3)]){const h=a.yards.drawnBaseHeightAt(q.x,-q.z,i.row.ground_record_id,i.row.ground_support_region_id);if(!Number.isFinite(h))throw Error('Missing actual retained yard triangle');values.push(q.y-h);}}const min=Math.min(...values),max=Math.max(...values);if(min< -1e-5||min>.001)throw Error('Actual source surface contact fails accepted development bound');feet[name]={actual_triangle_vertex_edge_centroid_samples:values.length,minimum_gap_m:min,maximum_gap_m:max};}
   const support={...a.yards.staticSupport};if(support.regions!==1||support.triangles>32||support.bytes>4096)throw Error('Support retention cap failed');
   const released=a.yards.group.children.map(m=>({name:m.name,position_null:m.geometry.attributes.position.array===null,index_empty:!m.geometry.index||m.geometry.index.array.length===0}));
   return{feet,support,yard_source_cpu_arrays:released,coarse:matchMedia('(pointer:coarse)').matches,query:location.search,receipt:i.receipt};
  });
  if(mobile&&(!report.ground.coarse||!report.ground.yard_source_cpu_arrays.every(x=>x.position_null&&x.index_empty)))throw Error('Normal coarse upload-release path not exercised; no keep-geometry workaround');
  report.selection=await page.evaluate(async()=>{
   const a=window.__chicago4d,T=await import('three'),i=a.standingHorses.instances[0],p=new T.Vector3(i.group.position.x,i.group.position.y+.95,i.group.position.z).project(a.camera),hit=a.standingHorses.pickAt(new T.Vector2(p.x,p.y),a.camera);if(hit?.id!==i.row.id)throw Error('Horse layer pick failed');a.popup.show(hit.record);const text=document.querySelector('#popup').innerText;if(!text.includes('sevketkabatas')||!text.includes('Unidentified'))throw Error('Actual selection card lacks source credit/identity limit');a.popup.close();const prior=a.confidence.hidden.reconstructed;a.confidence.setHidden('reconstructed',true);a.standingHorses.update(a.camera);if(i.group.visible||a.standingHorses.pickAt(new T.Vector2(p.x,p.y),a.camera))throw Error('Hidden reconstructed horse still draws/picks');a.confidence.setHidden('reconstructed',prior);a.standingHorses.update(a.camera);return{id:hit.id,text,confidence_hide_pick_pass:true};
  });
  report.teardown=await page.evaluate(async()=>{const a=window.__chicago4d,i=a.standingHorses.instances[0],disposed={geometry:0,material:0};i.root.traverse(m=>{if(m.isMesh){m.geometry.addEventListener('dispose',()=>disposed.geometry++);m.material.addEventListener('dispose',()=>disposed.material++);}});await a.standingHorses.setTier('light');if(a.standingHorses.instances.length)throw Error('Light did not retire horse');a.standingHorses.dispose();return{disposed,instances:a.standingHorses.instances.length};});
 }
 if(report.errors.length)throw Error('Browser errors recorded');report.pass=true;
}catch(error){report.error=String(error.stack??error);process.exitCode=1;}
finally{
 if(browser)await browser.close();if(server){server.closeAllConnections();await new Promise(r=>server.close(r));}
 report.closed=true;report.ended=new Date().toISOString();report.inputs_unchanged=true;
 for(const [file,hash]of Object.entries(cfg.expected_files))if(sha(await fs.readFile(file))!==hash)report.inputs_unchanged=false;
 if(!report.inputs_unchanged){report.pass=false;process.exitCode=1;}
 await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({phase,pass:report.pass,captures:report.captures.length,closed:report.closed,error:report.error}));
}
