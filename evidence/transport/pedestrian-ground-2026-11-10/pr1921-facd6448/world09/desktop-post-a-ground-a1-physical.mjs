// First desktop placement cell ONLY. Qualified parent fixture stays read-only.
import fs from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import { once } from 'node:events';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
const TASK='/workspace/.cloud-setup/coachman-placement-plan-20261110';
const APP='/workspace/.cloud-setup/coachman-placement-7d-post-a-20261110/chicago/4d';
const DEV='a1bc31a8df080f2e5956056fe0800761bd47bc10';
const REPO=path.resolve(APP,'../..');
import { sampleGroundCut } from './ground-cut-observer.mjs';
const SITE='/workspace/.cloud-setup/pages-alias-actual-20261110/site';
const OUT=process.argv[2];if(!OUT)throw Error('usage: node desktop-placement.mjs FRESH_OUTPUT');
await fs.mkdir(OUT,{recursive:false});
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const candidateBinding=JSON.parse(await fs.readFile(path.join(TASK,'CANDIDATE-7D-POST-A-SOURCE.json'),'utf8'));
for(const [file,row]of Object.entries(candidateBinding.files)){const b=await fs.readFile(path.resolve(APP,'../..',file));if(hash(b)!==row.sha256)throw Error('Own coach candidate changed since sealed preflight: '+file);}
const actual=JSON.parse(await fs.readFile(path.join(TASK,'HANDOFF-04-ACTUAL-FILES.json'),'utf8'));
const expected=new Map(actual.map(r=>[r.path,r]));
const sourcePrefix='4d/dev/';const overlay=new Map();
// Source-current baseline additions are explicit local overlays over the frozen artifact.
// Protected alias-aware consumers must remain exact; they are checked below.
const baselineOverlay=[];
for(const rel of execFileSync('git',['-C',REPO,'diff','--name-only','9d293d140002f3dc8ce5e71896c234c7675b630a',DEV,'--','chicago/4d/renderers/web/js','chicago/4d/data/humans/instances/1904','chicago/4d/data/liberties.json','chicago/4d/data/sidecars/1904/sources/uses.json'],{encoding:'utf8'}).trim().split('\n')){
 const published=rel.replace('chicago/4d/renderers/web/js/','4d/dev/walk/js/').replace('chicago/4d/data/','4d/dev/data/');
 const raw=execFileSync('git',['-C',REPO,'show',DEV+':'+rel],{maxBuffer:8*1024*1024});
 const b=rel.endsWith('.json')?Buffer.from(JSON.stringify(JSON.parse(raw))):raw;
 const shared=await fs.readFile(path.join(SITE,published)).catch(()=>null);
 if(!shared||hash(shared)!==hash(b)){overlay.set(published,b);baselineOverlay.push({source:rel,published,bytes:b.length,sha256:hash(b)});}
}

// Every actual candidate module below is read from the exact committed ROOT source, never the older sealed worktree.
const person='pa1904_glessner_john_j_c1900_charles_nelson';
const instance='hi_pa1904_glessner_john_j_c1900_charles_nelson_1904';
const instanceRel=`data/humans/instances/1904/${instance}.json`;
if(!overlay.has(sourcePrefix+instanceRel))throw Error('Exact current candidate Charles record missing from source overlay');
const native=JSON.parse(await fs.readFile('/workspace/.cloud-setup/pages-alias-publisher-20261110/receipts/actual-03/OVERLAY.json','utf8'));
const nativeBinding=[];
for(const r of native.files){
 const old=await fs.readFile(path.join(SITE,r.path));if(hash(old)!==r.newSha256)throw Error('Frozen native consumer changed after handoff');
 const rel=r.path.replace('4d/dev/walk/js/','chicago/4d/renderers/web/js/');
 const current=execFileSync('git',['-C',REPO,'show',DEV+':'+rel],{maxBuffer:8*1024*1024});
 if(r.path.endsWith('/terrain.js')){
  if(!overlay.has(r.path)||hash(overlay.get(r.path))!==hash(current))throw Error('Intentional terrain source overlay missing');
  const start=current.toString().indexOf('    /** Read-only admission for human support.');
  const end=current.toString().indexOf('    /** Backward-compatible names',start);
  if(start<0||end<start)throw Error('Bounded terrain admission range missing');
  const withoutGround=(current.toString().slice(0,start)+current.toString().slice(end)).replace("import { definitelyCutByRedMask } from './pedestrian-ground.js';\n",'');
  if(hash(Buffer.from(withoutGround))!==hash(old))throw Error('Terrain alias/decode logic changed beyond the two reviewed ground hunks');
  nativeBinding.push({file:r.path,status:'INTENTIONAL_TERRAIN_GROUND_DELTA',oldSHA256:hash(old),currentSHA256:hash(current),aliasDecodeAndAllOtherTerrainBytesUnchanged:true});
 }else{
  if(overlay.has(r.path)||hash(current)!==hash(old))throw Error('One of seven protected native consumers changed: '+r.path);
  nativeBinding.push({file:r.path,status:'UNCHANGED_NATIVE_CONSUMER',sha256:hash(current)});
 }
}
const baselinePhysical=path.join(TASK,'desktop-post-a-06/browser/PHYSICAL-FIRST-IMMUTABLE.json');
const state={nativeBinding,baselineComparison:{source:'2c9df872237b9dc2e6c95564eb6a4e125b80f185',path:baselinePhysical,sha256:hash(await fs.readFile(baselinePhysical)),scope:'Separately sourced immutable06 comparison; no paired current baseline world'},inheritedBalancedTriangleBudget:2675000,physicalErrors:[],status:'RUNNING_NOT_PASS',scope:'One physical-only1280 Balanced1904 finite native pose; no screenshots/UI gestures/quiet sequence/tour/phone/stance or photographic acceptance',sourceBase:'11d4bb29bb4cf14bf20e2796da4b4b99c1273a4c',sourceCandidate:DEV,baselineOverlay,frozenNativeAliasOverlaySourcePin:'68c3abd16e0bbb9704ebf3017fa5efba4190d6c0',recipePublicationSource:'119692a3ab849c6e75f679fe187009bd2d1f8287',fixture:'saved9d+actual03native8+declared119recipepublication+explicitcurrenta1bccommittedgroundcandidate;7nativeconsumersunchanged+intentionalterrain/newhelperdelta; local fixture, not live deployed commit',overlay:[...overlay].map(([file,b])=>({file,bytes:b.length,sha256:hash(b)})),errors:[],failedRequests:[],served:{},cells:[],budgetFailures:[],resources:[],images:[],physicalReviewRequired:[],noSharedFixtureWrites:true};
if(process.argv.includes('--prepare-only')){await fs.writeFile(path.join(OUT,'BINDING.json'),JSON.stringify({...state,status:'PREPARED_SOURCE_BINDINGS_ONLY_NO_BROWSER',protocolSHA256:hash(await fs.readFile(new URL(import.meta.url))),observerSHA256:hash(await fs.readFile(new URL('./ground-cut-observer.mjs',import.meta.url)))},null,2)+'\n');console.log(JSON.stringify({source:DEV,baselineOverlay:baselineOverlay.length,allOverlay:overlay.size,unchangedNativeConsumers:nativeBinding.filter(r=>r.status==='UNCHANGED_NATIVE_CONSUMER').length,intentionalTerrainDelta:1}));process.exit(0);}
const types={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.glb':'model/gltf-binary','.bin':'application/octet-stream','.gz':'application/gzip','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.svg':'image/svg+xml','.woff2':'font/woff2','.ktx2':'image/ktx2','.geojson':'application/json','.mp4':'video/mp4','.webm':'video/webm'};
const server=http.createServer(async(req,res)=>{try{
 const pathname=decodeURIComponent(new URL(req.url,'http://local').pathname);let file=path.resolve(SITE,'.'+pathname);
 if(!file.startsWith(SITE+path.sep))throw Error('Outside owned fixture');
 const candidate=req.headers['x-coachman-fixture']==='candidate';
 const initialRel=path.relative(SITE,file).split(path.sep).join('/');
 if(!(candidate&&overlay.has(initialRel))&&(await fs.stat(file)).isDirectory())file=path.join(file,'index.html');
 const rel=path.relative(SITE,file).split(path.sep).join('/');
 const own=candidate&&overlay.has(rel),expectedRow=expected.get(rel);
 if(!own&&!expectedRow)throw Error('Unexpected fixture file '+rel);
 res.writeHead(200,{'content-type':types[path.extname(file)]??'application/octet-stream','cache-control':'no-store','content-length':own?overlay.get(rel).length:expectedRow.bytes});
 if(own){const b=overlay.get(rel);state.served['candidate '+rel]={sha256:hash(b),bytes:b.length,overlay:true};res.end(b);}
 else{const digest=crypto.createHash('sha256');let bytes=0;for await(const chunk of createReadStream(file)){digest.update(chunk);bytes+=chunk.length;if(!res.write(chunk))await once(res,'drain');}const sha256=digest.digest('hex');if(sha256!==expectedRow.sha256||bytes!==expectedRow.bytes)throw Error('Fixture changed after handoff: '+rel);state.served[(candidate?'candidate ':'baseline ')+rel]={sha256,bytes,overlay:false};res.end();}
 }catch(e){state.errors.push('server '+String(e));if(res.headersSent)res.destroy();else res.writeHead(404).end('Missing or changed fixture');}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
if(process.argv.includes('--http-control')){
 const helper='4d/dev/walk/js/pedestrian-ground.js';const expectedHelper=overlay.get(helper);if(!expectedHelper)throw Error('Committed helper is missing');
 const response=await fetch('http://127.0.0.1:'+server.address().port+'/'+helper,{headers:{'x-coachman-fixture':'candidate'}});const bytes=Buffer.from(await response.arrayBuffer());
 if(response.status!==200||hash(bytes)!==hash(expectedHelper))throw Error('New helper HTTP source control failed');
 await new Promise(r=>server.close(r));await fs.writeFile(path.join(OUT,'HTTP-CONTROL.json'),JSON.stringify({source:DEV,path:helper,status:response.status,bytes:bytes.length,sha256:hash(bytes),protectedConsumers:nativeBinding},null,2)+'\n');console.log('PASS exact new committed helper is served although absent from frozen fixture;7 native consumers exact/terrain delta bounded');process.exit(0);
}
const globalRoot=(process.env.NODE_PATH??execFileSync('npm',['root','-g'],{encoding:'utf8'}).trim()).split(path.delimiter)[0];
const pw=await import(path.join(globalRoot,'playwright/index.js'));const chromium=pw.chromium??pw.default?.chromium;
let browser,page,context,cdp,browserTmp;
const heartbeat=setInterval(()=>{const value={phase:state.phase,at:new Date().toISOString(),elapsedSeconds:(Date.now()-begun)/1000,served:state.served,errors:state.errors,failedRequests:state.failedRequests};void fs.writeFile(path.join(OUT,'HEARTBEAT.json'),JSON.stringify(value,null,2)+'\n').catch(()=>{});},15000);heartbeat.unref();const begun=Date.now();let phaseCounter=0;
async function stage(name,run){await progress(name+'-start');const start=Date.now();try{return await run();}finally{state.timings??=[];state.timings.push({name,seconds:(Date.now()-start)/1000,elapsedSeconds:(Date.now()-begun)/1000});await progress(name+'-end');}}

async function progress(phase){state.phase=phase;state.elapsedSeconds=(Date.now()-begun)/1000;console.log(JSON.stringify({phase,seconds:state.elapsedSeconds}));await fs.writeFile(path.join(OUT,'STATE.json'),JSON.stringify(state,null,2)+'\n');}
async function resources(phase){const f=path.join(OUT,`resource-${++phaseCounter}.json`);try{execFileSync('python3',['/workspace/.cloud-setup/transport-current-20261103/resource_guard.py','capture',f],{stdio:'pipe'});}finally{state.resources.push({phase,file:f,snapshot:JSON.parse(await fs.readFile(f,'utf8'))});}}
async function frame(){const n=await page.evaluate(()=>__chicago4d.renderer.info.render.frame);await page.waitForFunction(n=>__chicago4d.renderer.info.render.frame>n,n,{timeout:90000});}
async function settle(){await page.evaluate(async()=>{await __chicago4d.parkedTransport.ready();});await page.waitForFunction(()=>__chicago4d.parkedTransport.pending===0&&(__chicago4d.residency?.pending??0)===0,null,{timeout:90000});await frame();}
async function physical(cell,label){const value=await page.evaluate(async({person,row,sampleSource})=>{
 const diagnostic={};try{
 const sampleGroundCut=(0,eval)('('+sampleSource+')');
 const a=__chicago4d,c=a.humans.get(person),i=a.parkedTransport.instances.find(i=>i.row.id===row);diagnostic.actor=c?{e:c.e,n:c.n,position:c.position,lod:c.lod,wanted:c.wanted,pending:!!c.pending,bodyLod:c.body?.lod,visible:c.root?.visible,indoors:c.indoors,meshes:c.body?.meshes.map(m=>({name:m.name,vertices:m.geometry.attributes.position.count,indexCount:m.geometry.index?.count??null}))}:null;if(!c?.body||!i?.team)throw Error('Actual actor/team not loaded');
 const THREE=await import('/4d/dev/walk/vendor/three-0.185.1/three.module.js');const {createRoadTriangleHeight}=await import('/4d/dev/walk/js/road-triangle-height.js');
 const cut=a.streetGrid?.groundCut,texture=cut?.mask,image=texture?.image;
 if(!cut||!image?.data||texture.format!==THREE.RedFormat||texture.type!==THREE.UnsignedByteType
   ||texture.magFilter!==THREE.LinearFilter||texture.minFilter!==THREE.LinearFilter
   ||texture.wrapS!==THREE.ClampToEdgeWrapping||texture.wrapT!==THREE.ClampToEdgeWrapping
   ||texture.generateMipmaps||texture.flipY)throw Error('Actual groundCut texture does not match the measured shader sampler');
 const materials=new Map();a.scene3d.traverse(o=>{if(!o.isMesh)return;for(const m of Array.isArray(o.material)?o.material:[o.material]){
   if(m?.userData?.cut?.tex.value===texture){const found=materials.get(m)??{material:m,objects:[]};found.objects.push({name:o.name,visible:o.visible,parentVisible:o.parent?.visible});materials.set(m,found);}
 }});
 const gl=a.renderer.getContext(),groundUniforms=[];
 for(const {material:m,objects}of materials.values()){
   const props=a.renderer.properties.get(m),program=props.currentProgram,uniforms=props.uniforms,declared=m.userData.cut;
   if(!program||!uniforms)throw Error('Ground material has no actual compiled shader uniform proof: '+m.name);
   for(const [name,object]of [['uChiCutOn',declared.on],['uChiCut',declared.tex],['uChiCutBox',declared.box]])
     if(uniforms[name]!==object)throw Error('Compiled shader cut uniform is not the actual material uniform: '+name);
   const active=program.getUniforms().map;
   const get=name=>{if(!active[name]?.addr)throw Error('Actual cut shader uniform missing: '+name);return gl.getUniform(program.program,active[name].addr);};
   const box=Array.from(get('uChiCutBox')),on=get('uChiCutOn'),unit=get('uChiCut');
   if(!(on>.5)||box.some((v,k)=>v!==Math.fround(declared.box.value.toArray()[k])))throw Error('Actual GL cut uniforms disagree with material values');
   groundUniforms.push({material:m.name,uuid:m.uuid,objects,box,on,samplerUnit:unit,textureIdentityExact:true,compiledUniformObjectsExact:true});
 }
 if(groundUniforms.length<2)throw Error('Both tile/base actual ground-cut materials must be accounted for');
 diagnostic.compiledGroundUniforms=groundUniforms;
 const maskSHA=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',image.data))).map(v=>v.toString(16).padStart(2,'0')).join('');
 diagnostic.groundCutTexture={name:texture.name,uuid:texture.uuid,width:image.width,height:image.height,sha256:maskSHA,flipY:texture.flipY};
 const sampleAt=(e,n)=>groundUniforms.map(u=>({material:u.material,uuid:u.uuid,...sampleGroundCut({data:image.data,width:image.width,height:image.height,box:u.box,on:u.on,flipY:texture.flipY},e,n)}));
 const groups=new Map();a.scene3d.getObjectByName('street-grid').traverse(m=>{if(m.isMesh&&['parkway','walk','carriageway','curb','margin'].includes(m.userData.cls)){const list=groups.get(m.userData.cls)??[];list.push(m);groups.set(m.userData.cls,list);}});
 const surfaces=[];for(const [cls,meshes]of groups)surfaces.push({cls,reader:createRoadTriangleHeight(meshes)});
 const support=(e,n)=>{const values=surfaces.map(s=>({cls:s.cls,height:s.reader.heightAt(e,n)})).filter(v=>Number.isFinite(v.height));const terrain=a.terrain.surfaceHeight(e,n);return{values,terrain,drawnHeight:values.length?Math.max(...values.map(v=>v.height)):null};};
 try{
  c.root.updateMatrixWorld(true);i.group.updateMatrixWorld(true);const cb=new THREE.Box3().setFromObject(c.body.scene,true),vb=new THREE.Box3().setFromObject(i.group,true);
  const axes=['x','y','z'].map(k=>({axis:k,gap:Math.max(cb.min[k]-vb.max[k],vb.min[k]-cb.max[k])}));
  const feet={},domainFailures=[];diagnostic.feet=feet;for(const side of ['l','r']){let count=0,min=Infinity,max=-Infinity,minimum=null,uncovered=0,maskedAllMaterials=0;const domain=[],allVertices=[];
   for(const mesh of c.body.meshes){const g=mesh.geometry,skin=g.attributes.skinIndex,w=g.attributes.skinWeight;if(!skin||!w)continue;mesh.skeleton.update();const seed=new Set();for(let k=0;k<skin.count;k++)for(let j=0;j<4;j++)if(w.getComponent(k,j)>0&&[`foot_${side}`,`ball_${side}`].includes(mesh.skeleton.bones[skin.getComponent(k,j)]?.name))seed.add(k);
    const ids=new Set(seed),ix=g.index;const total=ix?ix.count:g.attributes.position.count;for(let k=0;k<total;k+=3){const tri=[0,1,2].map(j=>ix?ix.getX(k+j):k+j);if(tri.some(v=>seed.has(v)))for(const id of tri)ids.add(id);}
    if(!ids.size)continue;domain.push({mesh:mesh.name,material:Array.isArray(mesh.material)?mesh.material.map(m=>m.name):mesh.material.name,vertices:ids.size});
    for(const id of ids){const p=mesh.getVertexPosition(id,new THREE.Vector3()).applyMatrix4(mesh.matrixWorld),s=support(p.x,-p.z),mask=sampleAt(p.x,-p.z);count++;const hidden=mask.every(u=>u.discarded);if(hidden)maskedAllMaterials++;
     const actualBase=hidden?s.drawnHeight:(s.drawnHeight===null?s.terrain:Math.max(s.terrain,s.drawnHeight));
     allVertices.push({mesh:mesh.name,vertex:id,e:p.x,n:-p.z,y:p.y,drawnStreetHeight:s.drawnHeight,rawTerrainHeight:s.terrain,mask,terrainDiscardedInAllMaterials:hidden,visibleBaseHeight:actualBase,visibleBaseGap:actualBase===null?null:p.y-actualBase});
     if(s.drawnHeight===null){uncovered++;continue;}const gap=p.y-s.drawnHeight;max=Math.max(max,gap);if(gap<min){min=gap;minimum={mesh:mesh.name,vertex:id,e:p.x,n:-p.z,y:p.y,gap,support:s};}}
   }
   if(count!==({l:1466,r:1476})[side]||!Number.isFinite(min))domainFailures.push({side,count,expected:({l:1466,r:1476})[side],minimumFinite:Number.isFinite(min),uncovered});feet[side]={classifier:'All vertices with any positive skin influence from foot/ball bones, union every vertex of incident triangles; no min-height/pixel selection',count,uncovered,min,max,minimum,domain,maskedAllMaterials,allVertices};
  }
  if(domainFailures.length)throw Error('Complete original actual foot domain changed or cannot be measured: '+JSON.stringify(domainFailures));
  const road=surfaces.find(s=>s.cls==='carriageway')?.reader;if(!road)throw Error('No drawn carriageway');
  const contact=await(await fetch(new URL(i.row.stationary_team.horse.contact_file,a.dataBase))).json();const horseFeet=[];
  for(const [horseIndex,h]of i.team.horses.entries()){let body=null;h.root.traverse(m=>{if(m.isSkinnedMesh&&m.geometry.attributes.position.count===contact.body_vertex_count&&m.material.name===contact.body_material_name)body=m;});if(!body)throw Error('Original horse body classifier missing');body.skeleton.update();const limbs={};for(const [limb,ids]of Object.entries(contact.feet)){let min=Infinity,max=-Infinity;for(const id of ids){const p=body.getVertexPosition(id,new THREE.Vector3()).applyMatrix4(body.matrixWorld),y=road.heightAt(p.x,-p.z);if(!Number.isFinite(y))throw Error('Drawn road missing under horse');const gap=p.y-y;min=Math.min(min,gap);max=Math.max(max,gap);}if(min<contact.limits.minimum_clearance_m||min>contact.limits.maximum_per_hoof_minimum_gap_m)throw Error('Original horse contact limit failed');limbs[limb]={min,max,vertices:ids.length};}horseFeet.push({horseIndex,limbs});}
  return{actor:{e:c.e,n:c.n,lod:c.lod,wanted:c.wanted,pending:!!c.pending,rootHeight:c.position.y,rawCentre:a.terrain.surfaceHeight(c.position.e,c.position.n),visibleStreetCentre:a.streetGrid.pedestrianHeight(c.position.e,c.position.n),runtimeCutAdmission:a.terrain.pedestrianGroundCutAt(c.position.e,c.position.n,a.streetGrid.groundCut.mask),mixerTime:c.body.mixer.time,clock:c.clock},pedestrianSupportIndex:a.streetGrid.pedestrianSupportReading(),feet,groundCut:{texture:{name:texture.name,uuid:texture.uuid,width:image.width,height:image.height,bytes:image.data.byteLength,sha256:maskSHA,flipY:texture.flipY,format:texture.format,type:texture.type,minFilter:texture.minFilter,magFilter:texture.magFilter,wrapS:texture.wrapS,wrapT:texture.wrapT},sourceBox:[cut.x0,cut.z0,1/cut.width,1/cut.depth],groundUniforms,shaderRule:'on > 0.5 && u > 0 && v > 0 && u < 1 && v < 1 && bilinearRed > 0.5'},actorAnchorSupport:support(c.position.e,c.position.n),charlesBounds:{min:cb.min.toArray(),max:cb.max.toArray()},vehicleTeamBounds:{min:vb.min.toArray(),max:vb.max.toArray()},axisSeparation:axes,conservativeBoundsDisjoint:axes.some(x=>x.gap>0),horseFeet,horseLimits:contact.limits,parkwayMeshCount:groups.get('parkway')?.length??0,walkMeshCount:groups.get('walk')?.length??0};
 }finally{for(const s of surfaces)s.reader.dispose();}
 }catch(e){return{observerFailure:String(e.stack??e),diagnostic};}
 },{person,row:'prairie_parked_studebaker_brougham',sampleSource:sampleGroundCut.toString()});cell.physical.push({label,...value});if(value.observerFailure){await fs.writeFile(path.join(OUT,'PHYSICAL-FIRST.json'),JSON.stringify({source:DEV,baselineComparison:state.baselineComparison,scope:state.scope,label,...value},null,2)+'\n');state.physicalErrors.push({label,failure:value.observerFailure,diagnostic:value.diagnostic});state.errors.push('Physical observer NONPASS: '+value.observerFailure);await progress(cell.kind+'-physical-'+label+'-NONPASS-SAVED');return value;}for(const side of ['l','r']){const f=value.feet[side];if(f.min<0||f.maskedAllMaterials===f.count&&f.min>0)state.physicalReviewRequired.push({cell:cell.kind,label,side,minimumGap:f.min,allTerrainDiscarded:f.maskedAllMaterials===f.count,scope:'Finite measured gap; no invented pose tolerance or visual acceptance'});}await fs.writeFile(path.join(OUT,'PHYSICAL-FIRST.json'),JSON.stringify({source:DEV,baselineComparison:state.baselineComparison,scope:state.scope,label,...value},null,2)+'\n');await progress(cell.kind+'-physical-'+label);return value;}

try{
 await resources('before-browser');browserTmp=await fs.mkdtemp('/tmp/cch-');process.env.TMPDIR=browserTmp;state.browserTemp=browserTmp;browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 for(const kind of ['candidate']){
  const cell={kind,states:[],physical:[],bootStartedAt:new Date().toISOString()};state.cells.push(cell);
  context=await browser.newContext({viewport:{width:1280,height:800},deviceScaleFactor:1,extraHTTPHeaders:{'x-coachman-fixture':kind}});
  await context.addInitScript(()=>{localStorage.setItem('chicago4d.settings',JSON.stringify({detail:'light',vehicles:'shown',people:'shown',timeOfDay:'morning'}));localStorage.setItem('chicago4d.help.seen','1');});
  page=await context.newPage();page.on('pageerror',e=>state.errors.push(kind+' '+String(e)));page.on('console',m=>{if(m.type()==='error')state.errors.push(kind+' '+m.text());});page.on('requestfailed',r=>state.failedRequests.push({kind,url:r.url(),error:r.failure()?.errorText}));page.on('response',r=>{if(r.status()>=400)state.errors.push(kind+' HTTP'+r.status()+' '+r.url());});
  await progress(kind+'-boot');const t=Date.now();await stage('navigate',()=>page.goto('http://127.0.0.1:'+server.address().port+'/4d/dev/walk/?year=1904&seed=1279',{waitUntil:'domcontentloaded',timeout:180000}));await stage('actual-world-ready',()=>page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:400000}));
  await stage('roam',()=>page.locator('#home-roam').click({timeout:90000}));cell.bootSeconds=(Date.now()-t)/1000;await resources(kind+'-booted');
  await stage('camera-date-detail',()=>page.evaluate(async()=>{const a=__chicago4d;a.setAnimationHold(true);a.setFly(true);a.walker.teleport({local_e:1407.9,local_n:-3245,yaw_deg:292,altitude_m:1.68,pitch_deg:0});await a.timeOfDay.set('morning',{date:'1904-07-01',transient:true});await a.setDetail('balanced');}));await stage('initial-native-settle',()=>settle());
  await page.waitForFunction(id=>{const a=__chicago4d.humans.get(id);return !!a?.body&&a.root.visible&&!a.indoors;},person,{timeout:90000});
  await stage('actual-current-human-lod-ready',()=>page.waitForFunction(id=>{const c=__chicago4d.humans.get(id);return !!c?.body&&!c.pending&&c.lod===c.wanted&&c.body.lod===c.lod;},person,{timeout:90000}));
  cell.prePhysicalActor=await page.evaluate(id=>{const c=__chicago4d.humans.get(id);return{e:c.e,n:c.n,position:c.position,lod:c.lod,wanted:c.wanted,bodyLod:c.body?.lod,pending:!!c.pending,visible:c.root.visible,indoors:c.indoors};},person);await progress('actual-actor-before-physical');
  await stage('physical-first',()=>physical(cell,'held-initial'));
  await progress('physical-proof-durable-stop');
  await context.close();context=null;page=null;await resources(kind+'-closed');
 }
 if(state.errors.length||state.failedRequests.length)throw Error('Browser/server/HTTP errors occurred');
 state.functionalChecksPassed=true;state.status='PHYSICAL_OBSERVATION_COMPLETE_REVIEW_REQUIRED_NOT_STANCE_PASS';
}catch(e){state.status='NONPASS_FIRST_DESKTOP_CELL';state.failure=String(e.stack??e);process.exitCode=1;
}finally{
 clearInterval(heartbeat);if(context)await context.close().catch(()=>{});if(browser)await browser.close();if(browserTmp)await fs.rm(browserTmp,{recursive:true,force:true});await new Promise(r=>server.close(r));state.browserClosed=true;state.serverClosed=true;state.elapsedSeconds=(Date.now()-begun)/1000;
 await fs.writeFile(path.join(OUT,'CLOSED.json'),JSON.stringify(state,null,2)+'\n');console.log(JSON.stringify({status:state.status,seconds:state.elapsedSeconds,cells:state.cells.length,images:state.images.length,budgetFailures:state.budgetFailures,physicalReviewRequired:state.physicalReviewRequired,failure:state.failure??null}));
}
if(state.budgetFailures.length)process.exitCode=1;
