/** Focused real published 1835 review. External helper; no publish/install/source edits.
 * Run desktop and phone serially, only after the parent grants the shared GPU slot.
 */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const args=Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
for(const k of ['url','viewport','out','expected']) assert(args[k],`--${k} required`);
assert(['desktop','phone'].includes(args.viewport));
assert(process.env.PW_MODULE,'PW_MODULE must identify the already-installed pinned Playwright module; this helper installs nothing');
const expected=JSON.parse(fs.readFileSync(args.expected));
const targets=[
 {id:'cobweb_castle',lib:'L-cobweb-partial-clapboards-2374',libWords:['1.30','reconstruct'],source:'Andreas|Wau.Bun|Kinzie',offset:[18,23],targetY:2.0},
 {id:'green_tree_tavern',lib:'L-green-tree-shoulder-roof-rise-2376',libWords:['4.6','reconstruct'],source:'Andreas',offset:[19,25],targetY:4.0},
 {id:'log_jail',lib:'L-jail-palisade-height-exposure-2380',libWords:['2.44','reconstruct'],source:'Gale|Trowbridge',offset:[-10,18],targetY:2.8}
];
const assetIds=[...targets.map(t=>t.id),'log_jail_keeper_house'];
for(const id of assetIds) assert(/^[a-f0-9]{64}$/.test(expected.assets?.[id]?.sha256),`actual qualified WEB hash required: ${id}`);
assert(expected.native_run && /^[a-f0-9]{40}$/.test(expected.source_sha) && expected.build_prefix,'native run, exact source SHA and published build prefix required');
assert(Array.isArray(expected.review_ids),'exact explicitly pinned retained review_ids required');
assert(/^[a-f0-9]{64}$/.test(expected.enclosure_sha256),'actual integrated enclosure input SHA required');
const OUT=path.resolve(args.out);fs.mkdirSync(OUT,{recursive:true});
const phone=args.viewport==='phone', viewport=phone?{width:390,height:780}:{width:1280,height:800};
const url=new URL(args.url);url.searchParams.set('year','1835');url.searchParams.set('keep-geometry','1');
assert(!url.pathname.includes('/renderers/web/'),'published layout required');
const receipt={kind:'FOCUSED_REAL_PUBLISHED_GROUP_REVIEW_NOT_FULL_SMOKE_OR_PICTURE_MATCH',status:'RUNNING',url:String(url),viewport,deviceScaleFactor:phone?2:1,expected,targets:{},screenshots:[],pageErrors:[],failedRequests:[],badResponses:[],consoleErrors:[]};
const save=()=>fs.writeFileSync(path.join(OUT,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');
function classify(raw,declared){
 assert(Array.isArray(raw)&&raw.every(x=>typeof x==='string'));
 for(const r of declared) assert(r.flag===true && r.key===r.recordId && r.key===r.sidecarId,'retained note must bind actual registry key, record and flagged sidecar');
 const ids=declared.map(r=>r.key).sort();assert.equal(new Set(ids).size,ids.length);
 assert.deepEqual(ids,[...expected.review_ids].sort(),'actual retained notes differ from explicit manifest');
 const messages=ids.map(id=>`${id}: review_required is set — review annotation retained; this flag does not block scene release`);
 for(const m of messages) assert.equal(raw.filter(p=>p===m).length,1,`missing/duplicate note: ${m}`);
 const allowed=new Set(messages);return {ids,annotations:raw.filter(p=>allowed.has(p)),hard:raw.filter(p=>!allowed.has(p))};
}
save();
const {chromium}=await import(pathToFileURL(process.env.PW_MODULE).href);
let browser,page;
try{
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
 const ctx=await browser.newContext({viewport,hasTouch:phone,isMobile:false,deviceScaleFactor:phone?2:1});
 page=await ctx.newPage();page.setDefaultTimeout(60_000);
 page.on('pageerror',e=>{receipt.pageErrors.push(String(e));save();});
 page.on('requestfailed',r=>receipt.failedRequests.push({url:r.url(),error:r.failure()?.errorText}));
 page.on('response',r=>{if(r.status()>=400)receipt.badResponses.push({url:r.url(),status:r.status()});});
 page.on('console',m=>{if(m.type()==='error')receipt.consoleErrors.push(m.text());});
 const start=Date.now();await page.goto(String(url),{waitUntil:'domcontentloaded',timeout:90_000});
 await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240_000,polling:1000});
 receipt.identity=await page.evaluate(async ids=>{
  const a=window.__chicago4d;if(!a.ready)throw Error(a.error||'not ready');
  const hash=async b=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('');
  const assets=[];for(const id of ids){
   const r=a.registry.get(id);if(!r?.gltf||r.loadFailed||!r.assetUrl)throw Error(`${id}: actual native asset not loaded`);
   const res=await fetch(r.assetUrl,{cache:'no-store'});if(!res.ok)throw Error(`${id}: HTTP${res.status}`);const bytes=await res.arrayBuffer();
   assets.push({id,url:r.assetUrl,bytes:bytes.byteLength,sha256:await hash(bytes),assetDetail:r.assetDetail,sidecarUrl:r.sidecarUrl,placement:r.sidecar.placement,footprint:r.sidecar.footprint,attributes:r.sidecar.attributes});
  }
  const enclosure=a.enclosures.records.find(r=>r.id==='log_jail_palisade');if(!enclosure)throw Error('actual jail enclosure absent');
  const er=await fetch(new URL('enclosures/log_jail_palisade.json',a.dataBase),{cache:'no-store'});if(!er.ok)throw Error(`enclosure HTTP${er.status}`);
  const eb=await er.arrayBuffer();
  return {scene:a.scene.id,date:a.scene.target_date,dataBase:String(a.dataBase),build:document.getElementById('gate-build')?.textContent.trim(),detail:a.detail,problems:[...a.problems],assets,enclosure,enclosure_sha256:await hash(eb),reviewDeclarations:[...a.registry.entries()].filter(([,r])=>r.sidecar?.review_required).map(([key,r])=>({key,recordId:r.id,sidecarId:r.sidecar.id,flag:r.sidecar.review_required}))};
 },assetIds);
 receipt.bootSeconds=(Date.now()-start)/1000;save();
 const ident=receipt.identity;assert.equal(ident.scene,'1835');assert.equal(ident.date,'1835-07-01');
 assert(ident.build.startsWith(`build ${expected.build_prefix}`),'actual published build mismatch');
 assert(ident.dataBase.includes('/data/')&&!ident.dataBase.includes('/chicago/4d/data/'),'published data layout required');
 for(const a of ident.assets){assert(a.url.includes('/data/gltf/'));assert.equal(a.sha256,expected.assets[a.id].sha256,`${a.id}: actual published/native WEB differs`);assert.equal(a.bytes,expected.assets[a.id].bytes);}
 assert.equal(ident.enclosure_sha256,expected.enclosure_sha256);assert.equal(ident.enclosure.form.height_m.value,2.44);assert.equal(ident.enclosure.form.height_m.confidence,'reconstructed');
 assert.equal(ident.assets.find(a=>a.id==='cobweb_castle').attributes.compound_clapboard_height_m.value,1.3);
 assert.equal(ident.assets.find(a=>a.id==='green_tree_tavern').attributes.enclosed_left_annex.value.shoulder.roof_high_m,4.6);
 receipt.problemClassification=classify(ident.problems,ident.reviewDeclarations);assert.equal(receipt.problemClassification.hard.length,0);save();
 await page.waitForFunction(()=>['welcome','world'].includes(window.__chicago4d.welcome?.state),null,{timeout:90_000,polling:500});
 await page.evaluate(()=>{const a=window.__chicago4d;if(a.welcome.state!=='world')a.welcome.enter('spawn');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.popup.close();a.navigator.select('home');a.navigator.dock();a.intent.clear();a.setAnimationHold(true);a.setFloraSpread(true);});
 await page.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:90_000,polling:500});
 // Same holdDraws policy as existing smoke: real world calculations continue;
 // only screenshots submit a real rendered frame. Never replace screenshot pixels.
 await page.evaluate(()=>{const r=window.__chicago4d.renderer;if(!window.__smokeHeldDraw)window.__smokeHeldDraw=r.render;r.render=(s,c)=>{c?.updateMatrixWorld?.();};});
 async function shot(name){
  await page.evaluate(()=>{const a=window.__chicago4d,r=a.renderer;r.render=window.__smokeHeldDraw;try{a.step();}finally{r.render=(s,c)=>{c?.updateMatrixWorld?.();};}});
  await page.screenshot({path:path.join(OUT,name+'.png'),timeout:90_000});receipt.screenshots.push(name+'.png');save();console.log(`SHOT ${name}`);
 }
 async function pose(t,elevated=false){
  return page.evaluate(({t,elevated})=>{
   const a=window.__chicago4d,r=a.registry.get(t.id),p=r.sidecar.placement,poly=r.sidecar.footprint.polygon??r.sidecar.footprint;
   const u=(Math.min(...poly.map(v=>v[0]))+Math.max(...poly.map(v=>v[0])))/2,v=(Math.min(...poly.map(v=>v[1]))+Math.max(...poly.map(v=>v[1])))/2;
   const q=p.rotation_deg*Math.PI/180,c=Math.cos(q),s=Math.sin(q),centre=[p.local_e+c*u-s*v,p.local_n+s*u+c*v];
   const e=centre[0]+c*t.offset[0]-s*t.offset[1],n=centre[1]+s*t.offset[0]+c*t.offset[1];
   const altitude=elevated?7:null,targetY=a.buildings.positionOf(t.id).y+t.targetY,eyeY=a.walker.surfaceAt(e,n)+(altitude??a.walkBudget.eyeHeight);
   const yaw=(Math.atan2(centre[0]-e,centre[1]-n)*180/Math.PI+360)%360,pitch=Math.atan2(targetY-eyeY,Math.hypot(centre[0]-e,centre[1]-n))*180/Math.PI;
   a.popup.close();a.intent.clear();a.setFly(elevated);a.walker.teleport({local_e:e,local_n:n,yaw_deg:yaw,pitch_deg:pitch,altitude_m:altitude});
   return {method:elevated?'actual live walker elevated context':'actual live walker street pose',requested:{e,n,yaw,pitch},actual:{e:a.walker.state.e,n:a.walker.state.n,eyeY:a.walker.state.eyeY,flying:a.walker.state.flying},centre,targetY};
  },{t,elevated});
 }
 for(const t of targets){
  const rec=receipt.targets[t.id]={};rec.pose=await pose(t);assert.equal(rec.pose.actual.flying,false);save();await shot(`${t.id}-01-street`);
  if(t.id==='log_jail'){
   rec.enclosureGeometry=await page.evaluate(()=>{
    const a=window.__chicago4d,r=a.enclosures.records.find(r=>r.id==='log_jail_palisade'),paths=r.runs.map(x=>x.path_local_enu_m),V=a.camera.position.clone();let meshCount=0,count=0,min=Infinity,max=-Infinity,minE=Infinity,maxE=-Infinity,minN=Infinity,maxN=-Infinity;
    const distance=(e,n)=>{let best=Infinity;for(const p of paths)for(let i=1;i<p.length;i++){const x=p[i-1],y=p[i],dx=y[0]-x[0],dn=y[1]-x[1],q=Math.max(0,Math.min(1,((e-x[0])*dx+(n-x[1])*dn)/(dx*dx+dn*dn)));best=Math.min(best,Math.hypot(e-x[0]-q*dx,n-x[1]-q*dn));}return best;};
    a.enclosures.group.updateMatrixWorld(true);a.enclosures.group.traverse(o=>{if(!o.isMesh||!o.userData.recordIds?.includes(r.id))return;const p=o.geometry.getAttribute('position');if(!p?.array?.length)throw Error('actual enclosure geometry discarded despite keep-geometry');meshCount++;for(let i=0;i<p.count;i++){V.set(p.getX(i),p.getY(i),p.getZ(i)).applyMatrix4(o.matrixWorld);const e=V.x,n=-V.z;if(distance(e,n)>.17)continue;const relative=V.y-a.terrain.surfaceHeight(e,n);min=Math.min(min,relative);max=Math.max(max,relative);minE=Math.min(minE,e);maxE=Math.max(maxE,e);minN=Math.min(minN,n);maxN=Math.max(maxN,n);count++;}});
    return {method:'actual loaded native enclosure quantized vertices transformed to world and sampled against actual terrain; only target record chunks within0.17m of authored path',meshCount,count,relativeHeight:{min,max},worldBounds:{minE,maxE,minN,maxN},authoredPaths:paths,declaredHeight:r.form.height_m,coreOrigin:a.buildings.positionOf('log_jail').toArray(),corePlacement:a.registry.get('log_jail').sidecar.placement};
   });
   const g=rec.enclosureGeometry;assert(g.meshCount>0&&g.count>100,'actual jail enclosure geometry required');assert(Math.abs(g.relativeHeight.max-2.44)<.06,'actual fence height relative to terrain differs');assert(Math.abs(g.relativeHeight.min)<.06,'actual fence feet not terrain seated');
   const all=g.authoredPaths.flat(),es=all.map(v=>v[0]),ns=all.map(v=>v[1]);assert(Math.abs(g.worldBounds.minE-Math.min(...es))<.2&&Math.abs(g.worldBounds.maxE-Math.max(...es))<.2&&Math.abs(g.worldBounds.minN-Math.min(...ns))<.2&&Math.abs(g.worldBounds.maxN-Math.max(...ns))<.2,'actual jail fence origin/endpoints differ');
   assert(Math.abs(g.coreOrigin[0]-g.corePlacement.local_e)<1e-5&&Math.abs(g.coreOrigin[2]+g.corePlacement.local_n)<1e-5,'actual jail core origin differs from its sidecar');
   rec.elevatedPose=await pose(t,true);save();await shot('log_jail-02-roof-and-enclosure-context');await pose(t);
  }
  await page.evaluate(async id=>{const a=window.__chicago4d;await a.loadLiberties();a.pick(id);document.querySelector('#popup [data-pop-tab="evidence"]')?.click();},t.id);
  await page.waitForFunction(()=>{const p=document.querySelector('#popup [data-pop-pane="images"]');return p&&!/LOADING IMAGE INDEX/.test(p.textContent)&&p.querySelectorAll('.pop-pic-list li, .pop-pic-tile').length>0;},null,{timeout:45_000,polling:250});
  rec.sources=await page.evaluate(()=>{const p=document.querySelector('#popup [data-pop-pane="evidence"]');return {shown:!p.hidden&&p.checkVisibility(),text:p.innerText,links:[...p.querySelectorAll('a[href]')].map(a=>({text:a.innerText,href:a.href}))};});
  assert(rec.sources.shown&&new RegExp(t.source,'i').test(rec.sources.text),'visible governing source credit absent');save();await shot(`${t.id}-03-sources`);
  rec.imagesBefore=await page.evaluate(()=>{const p=document.querySelector('#popup [data-pop-pane="images"]');return {src:p.querySelectorAll('img[src]').length,deferred:p.querySelectorAll('img[data-src]').length,openId:window.__chicago4d.popup.openId};});
  assert.equal(rec.imagesBefore.openId,t.id);assert.equal(rec.imagesBefore.src,0,'images acquired src before Images opened');
  await page.evaluate(()=>{document.querySelector('#popup [data-pop-tab="images"]').click();document.querySelector('#popup [data-pop-pane="images"]').scrollIntoView({block:'start'});});
  await page.waitForFunction(()=>{const p=document.querySelector('#popup [data-pop-pane="images"]'),imgs=[...(p?.querySelectorAll('img[src]')??[])];return p&&!p.hidden&&(!imgs.length||imgs.some(i=>i.complete&&i.naturalWidth>0));},null,{timeout:60_000,polling:500});
  rec.images=await page.evaluate(()=>{const p=document.querySelector('#popup [data-pop-pane="images"]'),items=[...p.querySelectorAll('.pop-pic-list li, .pop-pic-tile')];return {shown:!p.hidden&&p.checkVisibility(),count:items.length,tabCount:document.querySelector('#popup [data-pop-tab="images"] .pop-count')?.textContent.trim(),uncredited:items.filter(li=>!li.querySelector('.pop-pic-meta, .pop-pic-tile-credit')?.textContent.trim()).length,credits:items.map(li=>li.querySelector('.pop-pic-meta, .pop-pic-tile-credit')?.textContent.trim()),links:items.map(li=>({text:li.innerText,href:li.querySelector('a')?.href??null})),thumbs:[...p.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),complete:i.complete,naturalWidth:i.naturalWidth,alt:i.alt}))};});
  assert(rec.images.shown&&rec.images.count>0&&rec.images.uncredited===0);assert.equal(rec.images.tabCount,String(rec.images.count));if(rec.imagesBefore.deferred)assert(rec.images.thumbs.some(i=>i.src&&i.complete&&i.naturalWidth>0));save();await shot(`${t.id}-04-images-credited`);
  await page.evaluate(()=>document.querySelector('#popup [data-pop-tab="liberties"]').click());
  await page.waitForFunction(id=>!!document.querySelector(`#popup [data-lib-id="${id}"]`),t.lib,{timeout:30_000,polling:250});
  rec.liberty=await page.evaluate(id=>{const p=document.querySelector('#popup [data-pop-pane="liberties"]'),e=p.querySelector(`[data-lib-id="${id}"]`);if(!e.open)e.querySelector('summary').click();e.scrollIntoView({block:'start'});return {shown:!p.hidden&&p.checkVisibility(),id:e.dataset.libId,open:e.open,text:e.innerText,bounds:e.getBoundingClientRect().toJSON()};},t.lib);
  assert(rec.liberty.shown&&rec.liberty.open);for(const word of t.libWords)assert(rec.liberty.text.toLowerCase().includes(word),`liberty lacks ${word}`);save();await shot(`${t.id}-05-liberty`);
 }
 const final=await page.evaluate(()=>{const a=window.__chicago4d;return {problems:[...a.problems],declared:[...a.registry.entries()].filter(([,r])=>r.sidecar?.review_required).map(([key,r])=>({key,recordId:r.id,sidecarId:r.sidecar.id,flag:r.sidecar.review_required}))};});
 receipt.finalProblems=final.problems;receipt.finalProblemClassification=classify(final.problems,final.declared);save();assert.equal(receipt.finalProblemClassification.hard.length,0);
 assert.equal(receipt.pageErrors.length,0,'page errors');assert.equal(receipt.failedRequests.length,0,'failed requests');assert.equal(receipt.badResponses.length,0,'HTTP errors');assert.equal(receipt.consoleErrors.length,0,'console errors');
 receipt.status='PASS_FOCUSED_REVIEW_REQUIRES_HUMAN_SCREENSHOT_INSPECTION';save();console.log(JSON.stringify({status:receipt.status,viewport,screenshots:receipt.screenshots.length,receipt:path.join(OUT,'receipt.json')}));
}catch(error){receipt.status='FAIL';receipt.error=String(error.stack||error);save();if(page)await page.screenshot({path:path.join(OUT,'FAIL.png'),timeout:30_000}).catch(()=>{});throw error;
}finally{if(page)await page.evaluate(()=>{const a=window.__chicago4d;if(a?.renderer&&window.__smokeHeldDraw){a.renderer.render=window.__smokeHeldDraw;delete window.__smokeHeldDraw;}a?.setAnimationHold?.(false);}).catch(()=>{});if(browser)await browser.close();}
