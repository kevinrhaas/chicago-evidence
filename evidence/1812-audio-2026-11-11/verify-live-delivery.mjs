// External narrow delivery sanity check. Run ONLY after the expected DEV deployment is ready.
// Native UI/data only. Documented setup draw hold; restored before completion.
// No asset interception, fake actors/contacts/clocks, images or listening claims.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {chromium} from '/workspace/audio-tooling/node_modules/playwright/index.mjs';
const base='https://chicago.polecat.live/4d/dev/';
const expected=process.env.EXPECTED_DEV_VERSION;
assert(expected,'Set EXPECTED_DEV_VERSION to the exact deployed DEV revision');
const out=process.env.AUDIO_1812_REPORT_DIR??'/workspace/audio-1812/live-delivery-results';
await fs.mkdir(out,{recursive:true});
const sha=b=>createHash('sha256').update(b).digest('hex');
// Audio pins use immutable published-props at 3df73785f; device-profile.js
// separately pins recovery merge 4c64863fa (see merge-equivalence.json).
// The earlier prop-path-only migration preserved its JS/catalog/geometry.
// The later DEV merge changes device selection and settler models; this is NOT
// universal source equivalence. EXPECTED_DEV_VERSION names the actual live build.
const artifacts={
 "walk/js/device-profile.js": "d0016b8d173a2f5d4f639b823eb83262f7b4e0e701a8016a44ae309f90dfbe74",
 "walk/audio/catalog.json": "ba3ddc06813630c2c371139850e3a8019aa91be063fac6461ee835a34f9c46eb",
 "data/humans/work_1812.json": "8b1bc11fa24d7b12ff9e0fe3a676c16a959773d15c7244dab69884354551e4a8",
 "data/props/work_1812.glb": "64fdcbdffa35e00b0ed4704794993b21ae24286a3947bcb5961cfc1872180e7f",
 "walk/js/main.js": "61d9944d9ad1dbcd8d967acf7499f8fe440c9075076cd0b9abcc9ac6d460ace1",
 "walk/js/sound.js": "bc6b2af1198d9638a731c696691ac6bed56587cad0c1f915ef2db0ac863e621b",
 "walk/js/recorded-audio.js": "d3bc3575f13fda19986819907d2ab2629cec39d6dff8325b35ad448805a1ecd7",
 "walk/js/habitat-audio.js": "beff0f8905bbaf2683eaa73b3a9ae56c4652f8ec7736eae04a434da7a9527d35",
 "walk/js/habitat-seasons.js": "6bdb05190cbf3b6e97e66fe06e2af228a8c827adfb4ffcda53edc9e5eca9c5e7",
 "walk/js/season.js": "8407ba119eef8e26e1bfb4bf1d9dd2c4786d2981165f2d232fe53d2347a9bda7",
 "walk/js/transport-audio.js": "5ff0b2b9ddb595e80a8dd0212b3fe9ddb71088220232b611dae569c8d7c22887",
 "walk/js/hoof-contact-events.js": "6ee3f11ec220ef0b3266f4f03c847354e96cf40b95a25c5628c65810a7c5b7dc",
 "walk/js/driven-assembly-loader.js": "2b084419b11e060dfa14be5f2655167ca9f67b0785d44d0fc3adc7a3e743aa31",
 "walk/js/town-transport.js": "f079428611077f19e77e92cda35ddd27106c25ba7d54d140c40ca5a9f7c46d71",
 "walk/js/human-actions.js": "7d762946b459dbf54450c04827ccc6435d5d0e7e926d68452d753505e29b84db",
 "walk/js/human-days.js": "c4cc0baade132a9ab4e8e320e7adec8db8c824bb688f705d08e1b4dc14e0f4cd",
 "walk/js/work-activity.js": "ab9661f515effba6f48c621b531a3066bd9fa60add160959415d420af5c9e822",
 "walk/js/work-audio.js": "821f84d1e292efaee3f65eb3652dd071103d19a5244f3a4ecc7bb6e6323f3bdd"
};
const report={base,expected,started:new Date().toISOString(),physicalListening:false,
 screenshotQualityApproved:false,scope:'Live delivery/basic UI/audio handshake; published native contacts and all seasons are separately qualified',
 baseline:'/workspace/audio-1812/published-props',baselineVersion:'3df73785f',
 additionalBaseline:{path:'walk/js/device-profile.js',revision:'4c64863fa5af64c7121fb1a484111d224f46a078',evidence:'/workspace/audio-1812/merge-equivalence.json'},
 equivalenceProof:'/workspace/audio-1812/prop-path-equivalence.json',
 baselineQualification:'/workspace/audio-1812/review/results/report.json plus prop-path equivalence',
 harnessSha256:sha(await fs.readFile(new URL(import.meta.url))),artifacts,results:[]};
const proxyURL=process.env.HTTPS_PROXY||process.env.HTTP_PROXY||process.env.https_proxy||process.env.http_proxy;
const u=proxyURL?new URL(proxyURL):null;
const proxy=u?{server:u.origin,...(u.username?{username:decodeURIComponent(u.username),password:decodeURIComponent(u.password)}:{})}:undefined;
async function checkBuild(context,label){
 const r=await context.request.get(base+'build.json?audio1812='+Date.now()+'-'+label,{timeout:30000,headers:{'Cache-Control':'no-cache'}});
 assert(r.ok(),`build ${label}: HTTP ${r.status()}`);const build=await r.json();
 assert.equal(build.tier,'dev');assert.equal(build.sha??build.version,expected,`DEV revision changed or stale at ${label}`);return build;
}
function validateCatalog(catalog,config){
 const asset=id=>{const a=catalog.assets.find(x=>x.id===id);assert(a?.runtime_enabled,`${id} enabled`);return a;};
 assert.equal(asset('hammer-nail').scene_placement.mode,'visible-work');
 assert.equal(asset('horse-walking').scene_placement.mode,'hoof-contact');
 assert(asset('summer-cicada-proxy').seasonal_placements.some(p=>p.scene_id==='1812'&&p.season==='summer'));
 assert(asset('late-summer-katydid').seasonal_placements.some(p=>p.scene_id==='1812'&&p.season==='summer'&&p.active_periods.includes('night')));
 assert.deepEqual(asset('robin-calls').seasonal_placements.filter(p=>p.scene_id==='1812').map(p=>p.season).sort(),['fall','spring']);
 const task=config.tasks.find(t=>t.id==='militia-packing-chest');
 assert.equal(task.actor_id,'hi_town_chicago_militia_unnamed_4_1812');
 assert.deepEqual(task.dates,{from:'1812-08-14',to:'1812-08-14'});assert.deepEqual(task.hours,[[13,18]]);
 assert.equal(config.asset,'props/work_1812.glb');return task;
}
for(const width of [390,1280]){
 const detail=width===390?'light':'full';
 const row={width,detail,pageErrors:[],badMedia:[],requests:[],drawHold:{purpose:'Setup/UI/data only; no pixels or contact timing qualified',restored:false}};
 report.results.push(row);
 const browser=await chromium.launch({proxy,executablePath:process.env.PW_EXECUTABLE??'/usr/bin/chromium',headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});
 let page,context;
 const restore=async()=>{
  if(!page)return;
  return page.evaluate(()=>{
   const a=window.__chicago4d;if(!a?.renderer)return{restored:false};
   if(window.__deliveryRender){a.renderer.render=window.__deliveryRender;delete window.__deliveryRender;}
   return{restored:!window.__deliveryRender,frame:a.renderer.info.render.frame};
  });
 };
 try{
  context=await browser.newContext({viewport:{width,height:width===390?780:800},hasTouch:width===390,serviceWorkers:'block'});
  row.buildStart=await checkBuild(context,'start-'+width);
  const delivered={};row.deliveredHashes={};
  for(const [file,hash]of Object.entries(artifacts)){
   const r=await context.request.get(base+file+'?audio1812delivery='+Date.now(),{timeout:30000});
   assert(r.ok(),`${file}: HTTP ${r.status()}`);const bytes=await r.body();
   row.deliveredHashes[file]=sha(bytes);assert.equal(sha(bytes),hash,`Delivered ${file} differs from qualified publication`);
   if(file.endsWith('.json'))delivered[file]=JSON.parse(bytes);
  }
  const catalog=delivered['walk/audio/catalog.json'],config=delivered['data/humans/work_1812.json'];
  row.task=validateCatalog(catalog,config);assert(catalog.hosting?.public_base);
  const musicURLs=catalog.assets.filter(a=>a.kind==='music').flatMap(a=>[a.opus,a.aac]).filter(Boolean);
  const townMusic=catalog.assets.filter(a=>a.kind==='music'&&String(a.era)==='1812');
  assert.equal(townMusic.length,3);
  const townMusicURLs=townMusic.flatMap(a=>[a.opus,a.aac]).filter(Boolean);
  page=await context.newPage();page.setDefaultTimeout(90000);
  page.on('pageerror',e=>row.pageErrors.push(e.message));
  page.on('request',r=>{if(r.url().startsWith(catalog.hosting.public_base))row.requests.push(r.url());});
  page.on('response',r=>{if(r.url().startsWith(catalog.hosting.public_base)&&![200,206].includes(r.status()))row.badMedia.push({url:r.url(),status:r.status()});});
  await page.addInitScript(detail=>localStorage.setItem('chicago4d.settings',JSON.stringify({soundMaster:0,soundMusic:1,soundAmbience:0,soundEffects:0,timeOfDay:'15:00',detail})),detail);
  await page.goto(base+'walk/?year=1812',{waitUntil:'domcontentloaded',timeout:60000});
  // Software rendering can block Playwright UI actions for tens of seconds.
  // Save only the render method; simulation, actor state and audio remain native.
  // The hold ends below before checking actual frame progress. It proves no pixels.
  await page.waitForFunction(()=>window.__chicago4d?.ready===true&&__chicago4d.renderer&&__chicago4d.gesture&&__chicago4d.welcome?.state==='welcome',null,{timeout:240000,polling:500});
  await page.evaluate(()=>{const a=__chicago4d;window.__deliveryRender=a.renderer.render;a.renderer.render=(scene,camera)=>camera?.updateMatrixWorld?.();});
  row.drawHold.installed=true;
  const toggle=page.locator('#arrival-sound');await toggle.waitFor({state:'visible',timeout:60000});
  const ui=await page.evaluate(()=>{
   const el=document.getElementById('arrival-sound'),r=el.getBoundingClientRect();
   return{width:r.width,height:r.height,text:el.textContent.trim(),pressed:el.getAttribute('aria-pressed'),label:el.getAttribute('aria-label'),
    effects:document.getElementById('s-sound-effects-help')?.textContent.trim(),ambience:document.getElementById('s-sound-ambience-help')?.textContent.trim(),
    redundantNotes:document.querySelectorAll('#s-sound-note,#s-sound-music-help').length};
  });
  assert.equal(ui.width,44);assert.equal(ui.height,44);assert.equal(ui.text,'');assert.equal(ui.pressed,'false');assert(ui.label);
  assert.equal(ui.effects,'Nearby actions: hoofbeats, wagon wheels and hammering.');
  assert.equal(ui.ambience,'Background environment: wind, lake waves, birds and insects.');assert.equal(ui.redundantNotes,0);
  row.ui=ui;assert.equal(row.requests.length,0,'Muted startup fetches no R2 media');row.mutedStartup=true;
  await toggle.click({noWaitAfter:true,timeout:30000});
  await page.waitForFunction(()=>__chicago4d.sound?.state.context==='running',null,{timeout:45000,polling:100});
  assert.equal(await toggle.getAttribute('aria-pressed'),'true');row.gestureContextRunning=true;
  assert(!row.requests.some(url=>musicURLs.includes(url)),'No period music in travel/arrival before welcome');
  await page.waitForFunction(()=>__chicago4d.ready===true&&__chicago4d.welcome?.state==='welcome',null,{timeout:240000,polling:250});
  assert.equal(await page.evaluate(()=>__chicago4d.detail),detail);
  row.arrival=await page.evaluate(()=>({welcome:__chicago4d.welcome.state,journey:__chicago4d.journey.state,sound:__chicago4d.sound.state}));
  assert.equal(row.arrival.sound.recorded.playing,false);
  assert(!row.requests.some(url=>musicURLs.includes(url)),'Arrival choices request no period music');
  await page.locator('#home-roam').click({noWaitAfter:true,timeout:30000});
  await page.waitForFunction(()=>__chicago4d.welcome.state==='world'&&__chicago4d.journey.state==='exploring'&&__chicago4d.sound.state.recorded.playing,null,{timeout:60000,polling:100});
  row.town=await page.evaluate(()=>{
   const a=__chicago4d;return{time:a.timeOfDay.current,detail:a.detail,sound:a.sound.state,
    workController:{present:!!a.workActivity,update:typeof a.workActivity?.update,dispose:typeof a.workActivity?.dispose,group:a.workActivity?.group?.name,state:a.workActivity?.state},
    workDayAPI:typeof a.days?.workSource};
  });
  assert.equal(row.town.time.date,'1812-08-14');assert.equal(row.town.sound.recorded.year,'1812');
  assert(townMusic.some(a=>a.title===row.town.sound.recorded.track),'Native 1812 period track selected');
  assert(row.requests.some(url=>townMusicURLs.includes(url)),'1812 period recording requested from exact R2 object');
  assert(!row.requests.some(url=>musicURLs.includes(url)&&!townMusicURLs.includes(url)),'Other eras remain separate');
  assert(row.town.workController.present);assert.equal(row.town.workController.update,'function');assert.equal(row.town.workController.dispose,'function');
  assert.equal(row.town.workController.group,'work-activities');assert.equal(row.town.workDayAPI,'function');
  assert.equal(row.town.workController.state.failed,false);assert.deepEqual(row.town.workController.state.errors,[]);
  // Controller initialization is required; its nearby-only GLB need not be loaded
  // at the default entrance. Prop delivery bytes were independently checked above.
  assert.deepEqual(row.town.sound.recorded.errors,[]);assert.deepEqual(row.pageErrors,[]);assert.deepEqual(row.badMedia,[]);
  const restored=await restore();Object.assign(row.drawHold,restored);assert(restored.restored);
  await page.waitForFunction(frame=>!window.__deliveryRender&&__chicago4d.renderer.info.render.frame>frame,restored.frame,{timeout:90000,polling:500});
  row.drawHold.frameAfter=await page.evaluate(()=>__chicago4d.renderer.info.render.frame);
  row.buildEnd=await checkBuild(context,'end-'+width);assert.deepEqual(row.pageErrors,[]);assert.deepEqual(row.badMedia,[]);row.passed=true;
 }catch(e){row.error=e.stack;row.passed=false;
  if(context)try{row.buildAfterFailure=await checkBuild(context,'failure-'+width);}catch(x){row.buildError=x.message;}
 }finally{
  if(!row.drawHold.restored)try{Object.assign(row.drawHold,await Promise.race([restore(),new Promise((_,reject)=>setTimeout(()=>reject(Error('restore timeout')),5000))]));}catch(e){row.drawHold.restoreError=e.message;}
  await browser.close();await fs.writeFile(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
 }
 console.log(JSON.stringify({width,detail,passed:row.passed,error:row.error??null}));
 if(!row.passed)break;
}
report.finished=new Date().toISOString();report.passed=report.results.length===2&&report.results.every(x=>x.passed);
await fs.writeFile(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
if(!report.passed)process.exitCode=1;
