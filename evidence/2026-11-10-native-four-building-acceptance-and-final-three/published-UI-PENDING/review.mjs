/** Five actual published 1835 target cards; external, no source edits or synthetic screenshots.
 * GPU-slot authorization and parent-qualified native/publish pin required before execution.
 */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const opts=Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
for(const key of ['url','viewport','out','expected'])assert(opts[key],`--${key} required`);
assert(['desktop','phone'].includes(opts.viewport));assert(process.env.PW_MODULE,'existing pinned PW_MODULE required; installs nothing');
const expected=JSON.parse(fs.readFileSync(opts.expected));assert.equal(expected.targets.length,5);
assert(/^\d+$/.test(expected.native_run)&&/^[a-f0-9]{40}$/.test(expected.source_sha)&&expected.build_prefix);
for(const id of Object.keys(expected.assets))assert(/^[a-f0-9]{64}$/.test(expected.assets[id].published.sha256));
const out=path.resolve(opts.out);fs.mkdirSync(out,{recursive:true});
const phone=opts.viewport==='phone',viewport=phone?{width:390,height:780}:{width:1280,height:800};
const url=new URL(opts.url);url.searchParams.set('year','1835');url.searchParams.set('keep-geometry','1');
assert(!url.pathname.includes('/renderers/web/'),'published layout required');
const receipt={kind:'ACTUAL_PUBLISHED_FIVE_BUILDING_CARDS_AND_SCENES_NOT_FULL_SMOKE_OR_IMAGE_MATCH',
 status:'RUNNING',url:String(url),viewport,deviceScaleFactor:phone?2:1,expected,targets:{},screenshots:[],pageErrors:[],failedRequests:[],badResponses:[],consoleErrors:[]};
const save=()=>fs.writeFileSync(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');save();
function classify(raw,declarations){
 for(const r of declarations)assert(r.flag===true&&r.key===r.recordId&&r.key===r.sidecarId,'retained review annotation must bind actual registry and sidecar');
 const ids=declarations.map(r=>r.key).sort();assert.deepEqual(ids,expected.review_ids);assert.equal(new Set(ids).size,ids.length);
 const allowed=ids.map(id=>`${id}: review_required is set — review annotation retained; this flag does not block scene release`);
 for(const message of allowed)assert.equal(raw.filter(v=>v===message).length,1,`missing/duplicate annotation: ${message}`);
 return {ids,annotations:raw.filter(v=>allowed.includes(v)),hard:raw.filter(v=>!allowed.includes(v))};
}
const {chromium}=await import(pathToFileURL(process.env.PW_MODULE).href);let browser,page;
try{
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--no-sandbox','--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader']});
 const context=await browser.newContext({viewport,hasTouch:phone,isMobile:false,deviceScaleFactor:phone?2:1});page=await context.newPage();page.setDefaultTimeout(60_000);
 page.on('pageerror',e=>{receipt.pageErrors.push(String(e));save();});
 page.on('requestfailed',r=>receipt.failedRequests.push({url:r.url(),error:r.failure()?.errorText}));
 page.on('response',r=>{if(r.status()>=400)receipt.badResponses.push({url:r.url(),status:r.status()});});
 page.on('console',m=>{if(m.type()==='error')receipt.consoleErrors.push(m.text());});
 receipt.playwrightModule=process.env.PW_MODULE;receipt.browserVersion=browser.version();
 const began=Date.now();await page.goto(String(url),{waitUntil:'domcontentloaded',timeout:90_000});
 await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240_000,polling:1000});
 receipt.identity=await page.evaluate(async ids=>{
  const a=window.__chicago4d;if(!a.ready)throw Error(a.error||'not ready');
  const hash=async b=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(n=>n.toString(16).padStart(2,'0')).join('');
  const bind=async address=>{const u=new URL(address,location.href),r=await fetch(u,{cache:'no-store'});if(!r.ok)throw Error(`${u}: HTTP${r.status}`);const bytes=await r.arrayBuffer();return {url:String(u),bytes:bytes.byteLength,sha256:await hash(bytes)};};
  const assets=[];
  for(const id of ids){const r=a.registry.get(id);if(!r?.gltf||r.loadFailed||!r.assetUrl)throw Error(`${id}: qualified native asset not loaded`);
   assets.push({id,asset:await bind(r.assetUrl),sidecar:await bind(r.sidecarUrl),assetDetail:r.assetDetail,
    grade:r.sidecar.grade,placement:r.sidecar.placement,footprint:r.sidecar.footprint,attributes:r.sidecar.attributes});}
  const buildUrl=new URL('../build.json',a.dataBase),picturesUrl=new URL('pictures/1835.json',a.dataBase),libertiesUrl=new URL('liberties.json',a.dataBase);
  return {scene:a.scene.id,date:a.scene.target_date,dataBase:String(a.dataBase),build:document.getElementById('gate-build')?.textContent.trim(),detail:a.detail,assets,
   documents:{build:await bind(buildUrl),pictures:await bind(picturesUrl),liberties:await bind(libertiesUrl),woodpiles:await bind(new URL('yard/town_woodpiles.json',a.dataBase))},
   cobwebWoodpile:a.yard.records.find(r=>r.id==='town_woodpiles')?.lots.find(l=>l.structure_id==='cobweb_castle'),
   problems:[...a.problems],declarations:[...a.registry.entries()].filter(([,r])=>r.sidecar?.review_required).map(([key,r])=>({key,recordId:r.id,sidecarId:r.sidecar.id,flag:r.sidecar.review_required}))};
 },Object.keys(expected.assets));receipt.bootSeconds=(Date.now()-began)/1000;save();
 const identity=receipt.identity;assert.equal(identity.scene,'1835');assert.equal(identity.date,'1835-07-01');
 assert(identity.build.startsWith(`build ${expected.build_prefix}`),'published build mismatch');
 assert(identity.dataBase.includes('/data/')&&!identity.dataBase.includes('/chicago/4d/data/'));
 for(const row of identity.assets){const asset=expected.assets[row.id],sidecar=expected.sidecars[row.id];
  assert(row.asset.url.includes('/data/gltf/'),'actual WEB path required');assert.equal(row.asset.sha256,asset.published.sha256,`${row.id} actual published WEB hash`);assert.equal(row.asset.bytes,asset.published.bytes);
  assert.equal(row.sidecar.sha256,sidecar.files.published.sha256,`${row.id} published sidecar hash`);assert.equal(row.sidecar.bytes,sidecar.files.published.bytes);
  for(const field of ['grade','placement','footprint','attributes'])assert.deepEqual(row[field],sidecar.document[field],`${row.id}/${field}`);
 }
 assert.equal(identity.documents.build.sha256,expected.publishedDocuments.build.sha256);
 assert.equal(identity.documents.pictures.sha256,expected.publishedDocuments.pictures.published.sha256);
 assert.equal(identity.documents.liberties.sha256,expected.publishedDocuments.liberties.published.sha256);
 assert.equal(identity.documents.woodpiles.sha256,expected.publishedDocuments.woodpiles.published.sha256);assert.deepEqual(identity.cobwebWoodpile,expected.cobwebWoodpile,'actual loaded Cobweb yard row differs from official clearance rederive');
 receipt.problemClassification=classify(identity.problems,identity.declarations);assert.equal(receipt.problemClassification.hard.length,0);save();
 await page.waitForFunction(()=>['welcome','world'].includes(window.__chicago4d.welcome?.state),null,{timeout:90_000,polling:500});
 await page.evaluate(()=>{const a=window.__chicago4d;if(a.welcome.state!=='world')a.welcome.enter('spawn');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.popup.close();a.navigator.select('home');a.navigator.dock();a.intent.clear();a.setAnimationHold(true);a.setFloraSpread(true);});
 await page.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:90_000,polling:500});
 // Existing smoke's held-draw policy: submit actual world frame only for screenshot.
 await page.evaluate(()=>{const r=window.__chicago4d.renderer;window.__completionHeldDraw=r.render;r.render=(_scene,camera)=>camera?.updateMatrixWorld?.();});
 async function shot(name){await page.evaluate(()=>{const a=window.__chicago4d,r=a.renderer;r.render=window.__completionHeldDraw;try{a.step();}finally{r.render=(_scene,camera)=>camera?.updateMatrixWorld?.();}});await page.screenshot({path:path.join(out,`${name}.png`),timeout:90_000});receipt.screenshots.push(`${name}.png`);save();console.log(`SHOT ${name}`);}
 for(const target of expected.targets){
  const row=receipt.targets[target.id]={};
  row.pose=await page.evaluate(t=>{const a=window.__chicago4d,r=a.registry.get(t.id),p=r.sidecar.placement,poly=r.sidecar.footprint.polygon??r.sidecar.footprint;
   const u=(Math.min(...poly.map(v=>v[0]))+Math.max(...poly.map(v=>v[0])))/2,v=(Math.min(...poly.map(v=>v[1]))+Math.max(...poly.map(v=>v[1])))/2;
   const radians=p.rotation_deg*Math.PI/180,c=Math.cos(radians),s=Math.sin(radians),centre=[p.local_e+c*u-s*v,p.local_n+s*u+c*v];
   const e=centre[0]+c*t.offset[0]-s*t.offset[1],n=centre[1]+s*t.offset[0]+c*t.offset[1];
   const eyeY=a.walker.surfaceAt(e,n)+a.walkBudget.eyeHeight,targetY=a.buildings.positionOf(t.id).y+t.targetY;
   const yaw=(Math.atan2(centre[0]-e,centre[1]-n)*180/Math.PI+360)%360,pitch=Math.atan2(targetY-eyeY,Math.hypot(centre[0]-e,centre[1]-n))*180/Math.PI;
   a.popup.close();a.intent.clear();a.setFly(false);a.walker.teleport({local_e:e,local_n:n,yaw_deg:yaw,pitch_deg:pitch});
   return {method:'actual live walker and actual terrain; reconstructed review pose, not historic viewpoint',requested:{e,n,yaw,pitch},actual:{e:a.walker.state.e,n:a.walker.state.n,eyeY:a.walker.state.eyeY,flying:a.walker.state.flying},centre,targetY};
  },target);assert.equal(row.pose.actual.flying,false);save();await shot(`${target.id}-01-scene`);
  await page.evaluate(async id=>{const a=window.__chicago4d;await a.loadLiberties();a.pick(id);document.querySelector('#popup [data-pop-tab="evidence"]')?.click();},target.id);
  await page.waitForFunction(id=>window.__chicago4d.popup.picturesDoc?.by_structure&&window.__chicago4d.popup.openId===id,target.id,{timeout:45_000,polling:250});
  row.card=await page.evaluate(()=>{const p=document.querySelector('#popup');return {openId:window.__chicago4d.popup.openId,title:p.querySelector('h2,h1')?.textContent.trim(),tabs:[...p.querySelectorAll('[data-pop-tab]')].map(b=>({tab:b.dataset.popTab,text:b.textContent.trim(),disabled:b.disabled})),text:p.innerText};});assert.equal(row.card.openId,target.id);assert(row.card.title);
  row.sources=await page.evaluate(()=>{const pane=document.querySelector('#popup [data-pop-pane="evidence"]'),cites=pane.querySelector('.cites');if(!cites)throw Error('actual citations absent');cites.scrollIntoView({block:'start'});return {shown:!pane.hidden&&pane.checkVisibility(),text:cites.innerText,links:[...cites.querySelectorAll('a[href]')].map(a=>({text:a.innerText,href:a.href})),bounds:cites.getBoundingClientRect().toJSON()};});
  assert(row.sources.shown&&row.sources.links.length>0);const citations=expected.sidecars[target.id].document.citations;
  for(const cite of citations){if(cite.url)assert(row.sources.links.some(a=>a.href===new URL(cite.url,url).href),`${target.id}: actual citation URL absent ${cite.source_id}`);}
  save();await shot(`${target.id}-02-sources`);
  row.pictures=await page.evaluate(id=>window.__chicago4d.popup.picturesDoc.by_structure[id]??[],target.id);assert.deepEqual(row.pictures,expected.pictures[target.id],`${target.id}: compiled reference records`);
  row.imagesBefore=await page.evaluate(()=>{const p=document.querySelector('#popup [data-pop-pane="images"]');return {src:p.querySelectorAll('img[src]').length,deferred:p.querySelectorAll('img[data-src]').length};});assert.equal(row.imagesBefore.src,0,'image src was fetched before Images opened');
  await page.evaluate(()=>document.querySelector('#popup [data-pop-tab="images"]').click());
  await page.waitForFunction(()=>{const p=document.querySelector('#popup [data-pop-pane="images"]'),imgs=[...(p?.querySelectorAll('img[src]')??[])];return p&&!p.hidden&&(!imgs.length||imgs.some(i=>i.complete&&i.naturalWidth>0));},null,{timeout:60_000,polling:500});
  row.images=await page.evaluate(()=>{const pane=document.querySelector('#popup [data-pop-pane="images"]');return {shown:!pane.hidden&&pane.checkVisibility(),text:pane.innerText,status:pane.querySelector('.pop-pic-status')?.textContent,tabCount:document.querySelector('#popup [data-pop-tab="images"] .pop-count')?.textContent.trim(),
   held:[...pane.querySelectorAll('.pop-pic-tile')].map(e=>({title:e.getAttribute('aria-label'),credit:e.querySelector('.pop-pic-tile-credit')?.textContent.trim()})),
   linked:[...pane.querySelectorAll('.pop-pic-list li')].map(e=>({text:e.innerText,href:e.querySelector('a')?.href??null,credit:e.querySelector('.pop-pic-meta')?.textContent.trim()})),
   controls:[...document.querySelectorAll('#popup a[href],#popup button')].filter(e=>/from this spot|reference/i.test(e.textContent)).map(e=>({text:e.textContent.trim(),href:e.href??null,disabled:e.disabled??false})),
   thumbs:[...pane.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),complete:i.complete,naturalWidth:i.naturalWidth,alt:i.alt}))};});
  assert(row.images.shown);assert.equal(row.images.held.length+row.images.linked.length,row.pictures.length);if(row.pictures.length)assert.equal(row.images.tabCount,String(row.pictures.length));
  for(const e of [...row.images.held,...row.images.linked])assert(e.credit,'uncredited picture');
  const linkedExpected=row.pictures.filter(p=>!p.held);for(const p of linkedExpected){if(p.url)assert(row.images.linked.some(e=>e.href===new URL(p.url,url).href),`${target.id}: reference URL absent`);}
  if(target.id==='cobweb_castle')assert(!row.images.controls.some(c=>/from this spot/i.test(c.text)),'illustrative camera offered historical viewpoint');
  if(row.imagesBefore.deferred)assert(row.images.thumbs.some(i=>i.src&&i.complete&&i.naturalWidth>0),'held thumbnail did not hydrate');
  if(row.images.held.length){
   const held=row.pictures.find(p=>p.held);await page.locator('#popup .pop-pic-tile').first().click();
   await page.waitForFunction(()=>{const viewer=document.querySelector('.pic-viewer');return viewer&&!viewer.hidden;});
   row.referenceViewer=await page.evaluate(()=>{const credit=document.querySelector('.pic-viewer-credit');return {text:credit.innerText,links:[...credit.querySelectorAll('a[href]')].map(a=>({text:a.innerText,href:a.href}))};});
   for(const text of [held.title,held.creator,held.holder])assert(row.referenceViewer.text.includes(text),'held viewer credit incomplete');
   if(held.url)assert(row.referenceViewer.links.some(a=>a.href===new URL(held.url,url).href),'actual held reference URL absent');
   await page.locator('.pic-viewer-close').click();save();
  }
  await page.evaluate(()=>document.querySelector('#popup [data-pop-tab="liberties"]').click());
  await page.waitForFunction(id=>!!document.querySelector(`#popup [data-lib-id="${id}"]`),target.liberty,{timeout:30_000,polling:250});
  row.liberty=await page.evaluate(id=>{const pane=document.querySelector('#popup [data-pop-pane="liberties"]'),entry=pane.querySelector(`[data-lib-id="${id}"]`);if(!entry.open)entry.querySelector('summary').click();entry.querySelector('summary').scrollIntoView({block:'center'});return {shown:!pane.hidden&&pane.checkVisibility(),id:entry.dataset.libId,open:entry.open,text:entry.innerText,bounds:entry.getBoundingClientRect().toJSON(),summaryBounds:entry.querySelector('summary').getBoundingClientRect().toJSON()};},target.liberty);
  assert(row.liberty.shown&&row.liberty.open);for(const word of target.libertyWords)assert(row.liberty.text.toLowerCase().includes(word.toLowerCase()),`${target.id}: final liberty lacks ${word}`);
  assert(row.liberty.summaryBounds.top>=0&&row.liberty.summaryBounds.bottom<=viewport.height,'liberty summary not visible in actual viewport');save();await shot(`${target.id}-03-liberties`);
 }
 receipt.final=await page.evaluate(()=>{const a=window.__chicago4d;return {problems:[...a.problems],declarations:[...a.registry.entries()].filter(([,r])=>r.sidecar?.review_required).map(([key,r])=>({key,recordId:r.id,sidecarId:r.sidecar.id,flag:r.sidecar.review_required}))};});
 receipt.finalProblemClassification=classify(receipt.final.problems,receipt.final.declarations);assert.equal(receipt.finalProblemClassification.hard.length,0);
 for(const key of ['pageErrors','failedRequests','badResponses','consoleErrors'])assert.equal(receipt[key].length,0,key);
 assert.equal(receipt.screenshots.length,15);receipt.status='PASS_TARGET_UI_ASSERTIONS_REQUIRES_DIRECT_SCENE_AND_CARD_SCREENSHOT_REVIEW';save();console.log(JSON.stringify({status:receipt.status,viewport,screenshots:15,receipt:path.join(out,'receipt.json')}));
}catch(error){receipt.status='FAIL';receipt.error=String(error.stack||error);save();if(page)await page.screenshot({path:path.join(out,'FAIL.png'),timeout:30_000}).catch(()=>{});throw error;
}finally{if(page)await page.evaluate(()=>{const a=window.__chicago4d;if(a?.renderer&&window.__completionHeldDraw){a.renderer.render=window.__completionHeldDraw;delete window.__completionHeldDraw;}a?.setAnimationHold?.(false);}).catch(()=>{});if(browser)await browser.close();}
