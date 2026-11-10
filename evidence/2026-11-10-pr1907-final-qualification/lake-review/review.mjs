// External actual-published Lake House review. Prepared CPU-only; run only in root's GPU slot.
// REVIEW_REPO=/path/to/full/repo/chicago/4d GPU_SLOT_GRANTED=lake-house \
// node review.mjs --base http://127.0.0.1:PORT/walk/ --out /tmp/lake-final-review \
//   --expected-published-sha256 HASH --before-glb /path/to/original-master.glb
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const args=process.argv.slice(2),opt=(key,fallback)=>{const i=args.indexOf(key);return i<0?fallback:args[i+1];};
const repo=process.env.REVIEW_REPO;
if(!repo)throw Error('Set REVIEW_REPO to the full chicago/4d directory; no installs are performed.');
const require=createRequire(path.resolve(repo,'tools/qa.mjs'));
const {chromium}=require('playwright');
if(process.env.GPU_SLOT_GRANTED!=='lake-house')throw Error('Root must grant the serial GPU slot with GPU_SLOT_GRANTED=lake-house.');
const base=opt('--base'),bindingFile=opt('--asset-binding');
const binding=bindingFile?JSON.parse(fs.readFileSync(bindingFile,'utf8')):null;
if(opt('--expected-web-sha256'))throw Error('Use --expected-published-sha256: source assets/web bytes may be transformed by the official publisher.');
const expectedHash=opt('--expected-published-sha256',binding?.published_asset_sha256);
if(!base||!expectedHash)throw Error('--base must point to the actual published /walk/ app and --expected-published-sha256 (or an asset binding) must pin its actual published GLB.');
if(!/^[a-f0-9]{64}$/.test(expectedHash))throw Error('Expected published asset hash must be a full SHA-256.');
if(binding){
 if(binding.structure_id!=='lake_house_construction'||binding.phase!=='shell_1835'||binding.target_date!=='1835-07-01')throw Error('Asset binding targets the wrong structure/phase/date');
 if(binding.published_asset_sha256!==expectedHash)throw Error('Explicit published hash disagrees with the binding');
 if(binding.acceptance_state!=='publisher_transform_verified')throw Error('The publisher transform is still pending; do not turn observed unequal bytes into an accepted binding.');
 const proof=binding.publisher_transform_proof;
 if(!proof?.receipt_path||!proof?.receipt_sha256)throw Error('Verified binding must name the causal publisher-transform proof receipt and its hash');
 const proofBytes=fs.readFileSync(proof.receipt_path);
 if(crypto.createHash('sha256').update(proofBytes).digest('hex')!==proof.receipt_sha256)throw Error('Publisher-transform receipt bytes changed');
}
const out=path.resolve(opt('--out','/tmp/nov10-lake-native-review/results'));
fs.mkdirSync(out,{recursive:true});
const beforePath=opt('--before-glb','/tmp/nov10-lake-native-review/before.glb');
const beforeBytes=fs.readFileSync(beforePath),sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const ID='lake_house_construction';
const all=[];
for(const [label,viewport,touch] of [['desktop',{width:1280,height:800},false],['phone',{width:390,height:780},true]].filter(([label])=>!opt('--viewport')||label===opt('--viewport'))){
 const browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--no-sandbox','--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader']});
 const context=await browser.newContext({viewport,hasTouch:touch,isMobile:touch,deviceScaleFactor:1});
 const page=await context.newPage(),errors=[],assetResponses=[];
 page.on('pageerror',e=>errors.push('pageerror: '+e.message));
 page.on('console',m=>{if(m.type()==='error'&&!m.text().startsWith('Failed to load resource'))errors.push('console.error: '+m.text());});
 page.on('response',r=>{if(r.status()>=400)errors.push('HTTP '+r.status()+' '+r.url());if(r.url().includes(ID+'__shell_1835.glb'))assetResponses.push(r);});
 page.on('requestfailed',r=>{const why=r.failure()?.errorText||'';if(!/ERR_ABORTED/.test(why))errors.push('requestfailed: '+why+' '+r.url());});
 try{
  const url=new URL(base);url.searchParams.set('year','1835');url.searchParams.set('structure',ID);url.searchParams.set('version','default');url.searchParams.set('keep-geometry','1');
  const response=await page.goto(url.href,{waitUntil:'domcontentloaded'});if(response.status()!==200)throw Error('Entry status '+response.status());
  await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000,polling:1000});
  await page.waitForFunction(()=>document.documentElement.dataset.journey==='landed',null,{timeout:90000,polling:1000});
  await page.evaluate(async id=>{const a=window.__chicago4d,until=Date.now()+90000;while(a.welcome?.state!=='world'&&Date.now()<until){if(a.welcome?.state==='welcome')a.welcome.enter('spawn');if(a.welcome?.state!=='world')await new Promise(r=>setTimeout(r,100));}if(a.welcome?.state!=='world')throw Error('Welcome did not enter the actual town');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.popup?.close?.();a.frame(id,{card:false});},ID);
  await page.waitForTimeout(500);
  const census=await page.evaluate(async({id,before64})=>{
   const a=window.__chicago4d,r=a.registry.get(id);if(!r?.gltf)throw Error('Target GLB not loaded into registry');
   const s=r.sidecar,appRoot=new URL('.',location.href),vendor=new URL('vendor/three-0.185.1/',appRoot);
   const THREE=await import(new URL('three.module.js',vendor).href);
   const {GLTFLoader}=await import(new URL('addons/loaders/GLTFLoader.js',vendor).href);
   let rawGltf=r.gltf,decodedForReview=false;
   // The real phone correctly retires the Object3D source tree after batching.
   // Re-decode exactly its published URL for inspection; do not alter the app
   // registry/batches or disable the production release policy.
   if(rawGltf.scene.collapsed||typeof rawGltf.scene.updateMatrixWorld!=='function'){
    const {MeshoptDecoder}=await import(new URL('addons/libs/meshopt_decoder.module.js',vendor).href);
    const {KTX2Loader}=await import(new URL('addons/loaders/KTX2Loader.js',vendor).href);
    const ktx=new KTX2Loader().setTranscoderPath(new URL('addons/libs/basis/',vendor).href).setWorkerLimit(1).detectSupport(a.renderer);
    rawGltf=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).setKTX2Loader(ktx).loadAsync(r.assetUrl);
    window.__lakeReviewDecoded=rawGltf;decodedForReview=true;
   }
   const raw={vertices:0,confidenceMin:Infinity,confidenceMax:-Infinity,missingConfidence:0,meshes:0,materials:[]};
   rawGltf.scene.traverse(o=>{if(!o.isMesh)return;raw.meshes++;const g=o.geometry,c=g.getAttribute('_confidence');raw.vertices+=g.getAttribute('position')?.count||0;if(!c)raw.missingConfidence++;else for(let i=0;i<c.count;i++){raw.confidenceMin=Math.min(raw.confidenceMin,c.getX(i));raw.confidenceMax=Math.max(raw.confidenceMax,c.getX(i));}for(const m of [o.material].flat())raw.materials.push(m?.name||'');});
   const beforeBuffer=Uint8Array.from(atob(before64),c=>c.charCodeAt(0)).buffer;
   const before=await new Promise((resolve,reject)=>new GLTFLoader().parse(beforeBuffer,'',resolve,reject));
   function probes(root){
    root.updateMatrixWorld(true);const ray=new THREE.Raycaster();ray.near=0;ray.far=1.4;
    const hit=(x,y,z,dx,dy,dz,far=1.4)=>{ray.far=far;ray.set(new THREE.Vector3(x,y,z),new THREE.Vector3(dx,dy,dz));const v=ray.intersectObject(root,true);return v.length?v[0].distance:null;};
    const openingHits=Array.from({length:7},(_,i)=>hit((i+.5)*24/7,1.2,-16,0,0,1));
    const upperHits=Array.from({length:7},(_,i)=>hit((i+.5)*24/7,3.6,-16,0,0,1));
    const outer=hit(.3,1.2,-16,0,0,1),inner=hit(.3,1.2,-14,0,0,-1);
    return {openingHits,upperHits,frontPierHit:outer,innerPierHit:inner,inferredWallThickness:outer===null||inner===null?null:2-outer-inner,interiorOverheadHit:hit(12,6,-7.5,0,-1,0,5.5)};
   }
   return {year:a.year,targetDate:a.scene?.target_date,phase:s?.phase,assetUrl:r.assetUrl,sidecarAsset:s?.asset,grade:s?.grade,constructionSite:s?.attributes?.construction_site,raw,decodedForReview,sourceSceneCollapsed:!!r.gltf.scene.collapsed,rendered:a.buildings.instanceBounds()[id],afterGeometry:probes(rawGltf.scene),beforeGeometry:probes(before.scene),player:{...a.player},problems:a.problems.filter(x=>String(x).includes(id))};
  },{id:ID,before64:beforeBytes.toString('base64')});
  const loadedAssets=[];for(const r of assetResponses)loadedAssets.push({url:r.url(),status:r.status(),sha256:sha(await r.body())});
  const check=(ok,why)=>{if(!ok)throw Error(why);};
  check(census.year==='1835'&&census.targetDate==='1835-07-01'&&census.phase==='shell_1835','Wrong scene date/phase');
  check(census.constructionSite?.value===true&&census.constructionSite.confidence==='reconstructed','Worksite option/provenance missing');
  check(loadedAssets.length>0&&loadedAssets.every(x=>x.sha256===expectedHash),'Actual page-loaded derivative did not match the exact expected hash');
  check(/\/data\/gltf\//.test(census.assetUrl),'Target did not use the published compressed asset route');
  check(census.raw.vertices>0&&census.raw.missingConfidence===0&&Math.abs(census.raw.confidenceMin-1)<.001&&Math.abs(census.raw.confidenceMax-1)<.001,'Published GLB lost raw reconstructed 1.0 confidence');
  check(census.rendered&&Math.abs(census.rendered.size[0]-24)<.03&&Math.abs(census.rendered.size[1]-4)<.03&&Math.abs(census.rendered.size[2]-15)<.03,'Rendered target bounds differ from 24×4×15m');
  // The existing inferred-existence display policy clamps its batched channel.
  check(census.grade?.value==='inferred'&&Math.abs(census.rendered.confidence.min-.5)<.01&&Math.abs(census.rendered.confidence.max-.5)<.01,'Unexpected existence-floor/batched confidence; report rather than changing it');
  check(census.afterGeometry.openingHits.every(x=>x===null),'A declared work opening is filled');
  check(census.afterGeometry.upperHits.slice(0,3).every(x=>x!==null)&&census.afterGeometry.upperHits.slice(3).every(x=>x===null),'The upper working lift is not stepped as declared');
  check(census.afterGeometry.frontPierHit!==null&&Math.abs(census.afterGeometry.inferredWallThickness-.46)<.03,'Expected real 0.46 m wall thickness not present');
  check(census.afterGeometry.interiorOverheadHit===null,'The worksite interior is capped');
  check(census.beforeGeometry.openingHits.every(x=>x!==null),'Supplied baseline does not represent the old closed magazine front');
  check(census.problems.length===0,'Target load problems: '+census.problems.join('; '));
  await page.screenshot({path:path.join(out,label+'-street.png')});
  await page.evaluate(id=>{const a=window.__chicago4d,s=a.registry.get(id).sidecar,p=s.placement;a.setFly(true);a.walker.teleport({local_e:p.local_e+45,local_n:p.local_n+43,altitude_m:20,yaw_deg:223,pitch_deg:-20});a.popup.close();},ID);
  await page.waitForTimeout(500);await page.screenshot({path:path.join(out,label+'-open-shell.png')});
  await page.evaluate(id=>{const a=window.__chicago4d,p=a.registry.get(id).sidecar.placement;a.setFly(true);a.walker.teleport({local_e:p.local_e-33,local_n:p.local_n-32,altitude_m:20,yaw_deg:49,pitch_deg:-17});a.popup.close();},ID);
  await page.waitForTimeout(500);await page.screenshot({path:path.join(out,label+'-stages-from-rear.png')});
  await page.evaluate(id=>{const a=window.__chicago4d;a.setFly(false);a.frame(id,{card:true});a.pick(id);},ID);
  await page.waitForTimeout(500);await page.screenshot({path:path.join(out,label+'-card.png')});
  const libertyRead=await page.evaluate(async id=>{
   const a=window.__chicago4d;await a.loadLiberties();a.pick(id);
   document.querySelector('#popup [data-pop-tab="liberties"]')?.click();
   const entry=document.querySelector('#popup details.lib[data-lib-id="L-lake-house-worksite-2379"]');
   if(!entry)throw Error('The actual card is missing the new worksite liberty');
   entry.open=true;entry.scrollIntoView({block:'start'});
   const pane=document.querySelector('#popup [data-pop-pane="liberties"]');
   return {id:entry.dataset.libId,text:entry.textContent.replace(/\s+/g,' ').trim(),paneShown:!!pane&&!pane.hidden&&pane.checkVisibility(),entryShown:entry.checkVisibility()};
  },ID);
  check(libertyRead.paneShown&&libertyRead.entryShown&&/reconstruct/i.test(libertyRead.text),'The published card did not expose its declared worksite liberty');
  await page.screenshot({path:path.join(out,label+'-liberties.png')});
  // Controlled neutral comparison after actual application captures. This is
  // explicitly a before-master versus page-loaded-after geometry comparison,
  // not a historical picture match or a claim about an earlier published UI.
  const controlled=await page.evaluate(async({id,before64})=>{
   const a=window.__chicago4d,vendor=new URL('vendor/three-0.185.1/',new URL('.',location.href));
   const THREE=await import(new URL('three.module.js',vendor).href);
   const {GLTFLoader}=await import(new URL('addons/loaders/GLTFLoader.js',vendor).href);
   const before=await new Promise((resolve,reject)=>new GLTFLoader().parse(Uint8Array.from(atob(before64),c=>c.charCodeAt(0)).buffer,'',resolve,reject));
   a.renderer.setAnimationLoop(null);
   const camera=new THREE.PerspectiveCamera(45,innerWidth/innerHeight,.1,200);
   // More distance on the narrow phone; same camera for before and after.
   const q=innerWidth<600?1.8:1;
   camera.position.set(12-31*q,3+21*q,-7.5+35*q);camera.lookAt(12,1.9,-7.5);
   const scene=new THREE.Scene();scene.background=new THREE.Color(0xe8ecef);
   scene.add(new THREE.HemisphereLight(0xdfe8f0,0x8a8070,1.1));
   const sun=new THREE.DirectionalLight(0xffffff,2.8);sun.position.set(20,40,-30);scene.add(sun);
   const capture=root=>{const clone=root.clone(true);scene.add(clone);a.renderer.render(scene,camera);const data=a.renderer.domElement.toDataURL('image/png');scene.remove(clone);return data;};
   return {before:capture(before.scene),after:capture(window.__lakeReviewDecoded?.scene||a.registry.get(id).gltf.scene)};
  },{id:ID,before64:beforeBytes.toString('base64')});
  for(const [key,value] of Object.entries(controlled))fs.writeFileSync(path.join(out,label+'-controlled-'+key+'.png'),Buffer.from(value.split(',')[1],'base64'));
  check(errors.length===0,'Page errors: '+errors.join('; '));
  const result={label,url:url.href,viewport,result:'PASS',assetBinding:binding||{published_asset_sha256:expectedHash,source_web_sha256:opt('--expected-source-web-sha256',null),publisher_transform_proof:'Root-owned causal proof; not inferred from unequal hashes'},loadedAssets,beforeMasterSha256:sha(beforeBytes),census,libertyRead,errors,visualReview:'PENDING: a human must inspect the actual screenshots for grounding, wall/stage visibility and card readability; data checks do not claim that review.'};
  fs.writeFileSync(path.join(out,label+'.json'),JSON.stringify(result,null,2)+'\n');all.push(result);console.log(label+' PASS: actual published asset/date/raw confidence/bounds/open-wall probes/baseline difference; screenshots saved for review.');
 }catch(e){fs.writeFileSync(path.join(out,label+'-failure.json'),JSON.stringify({label,result:'FAIL',error:String(e.stack||e),errors},null,2)+'\n');throw e;}
 finally{await context.close();await browser.close();}
}
fs.writeFileSync(path.join(out,'review.json'),JSON.stringify({preparedFor:'T-2379',results:all,finalVisualAcceptance:'PENDING'},null,2)+'\n');
