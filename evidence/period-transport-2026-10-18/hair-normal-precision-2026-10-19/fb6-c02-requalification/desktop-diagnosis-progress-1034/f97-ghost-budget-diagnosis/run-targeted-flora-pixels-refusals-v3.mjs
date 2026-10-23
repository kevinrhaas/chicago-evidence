#!/usr/bin/env node
// OUTSIDE diagnostic. Preparation only unless --run is explicitly supplied after root release.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import crypto from 'node:crypto';import {pathToFileURL}from'node:url';
const argv=process.argv.slice(2),get=(k,d)=>{const i=argv.indexOf(k);return i<0?d:argv[i+1];};
const checkout=get('--checkout','/workspace/chicago'),mirror=get('--mirror',path.join(checkout,'site/4d')),out=get('--out','/workspace/shared/f97-ghost-budget-diagnosis/run-receipt.json'),hudModule=null,refusalModule=get('--refusal-module','/workspace/shared/hud-footprint-f97-harness/hud-refusals-v3.mjs'),limit=Number(get('--max-seconds','600'));
const smokePath=path.join(checkout,'chicago/4d/tools/smoke_renderer.mjs'),source=fs.readFileSync(smokePath,'utf8');
const helper=source.slice(source.indexOf('  const clickChrome = async (sel) => {'),source.indexOf('  // T-2620: the drawer and its hamburger'));
if(!helper.includes('el.click();')||!helper.includes('elementFromPoint'))throw Error('actual clickChrome extraction failed');
import {compareHeldPage} from '/workspace/shared/flora-billboard-singlepass-proposal/compare-held-page-v3.mjs';
const traceSource=fs.readFileSync(new URL('./trace-one-frame-detailed.js',import.meta.url),'utf8');
const traceFunction=new Function('return ('+traceSource+')')();
const probeHelper='/workspace/shared/flora-billboard-singlepass-proposal/compare-held-page-v3.mjs',hudOutput=path.join(path.dirname(out),path.basename(out,'.json')+'-hud-v3'),pixelOutput=path.join(path.dirname(out),path.basename(out,'.json')+'-pixels');
const refusalOutput=path.join(path.dirname(out),path.basename(out,'.json')+'-refusals-v3');
const hashFile=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const plan={refusalModule,refusalOutput,refusal_module_sha256:refusalModule?hashFile(refusalModule):null,harness_sha256:hashFile(new URL(import.meta.url)),probe_helper_sha256:hashFile(probeHelper),hud_module_sha256:hudModule?hashFile(hudModule):null,hudOutput,pixelOutput,kind:'bounded pixel-only actual flora false/true/false diagnostic; not full smoke',checkout,mirror,out,limit,hudModule,viewport:{width:1280,height:800},source_sha256:crypto.createHash('sha256').update(source).digest('hex'),route:'source stage13 final camera-bearing path: instantSauganash→HoganpersonGoTherehorse→travelSimulate→instantly; no later stage13 camera-bearing action beforeT2648',limits:'Does not reconstruct accumulated70minasync/lazy residency. PriorCI didnotlogcamera; actualpose andstate recorded, no claim331reproduceduntil measured.',run:argv.includes('--run')};
if(!plan.run){console.log(JSON.stringify(plan,null,2));process.exit(0);}
for(const target of[out,hudOutput,pixelOutput,...(refusalModule?[refusalOutput]:[])])if(fs.existsSync(target))throw Error('fresh outside output required:'+target);
let browser,server,timer,page;const receipt={...plan,started_utc:new Date().toISOString(),samples:[],errors:[]};const save=()=>fs.writeFileSync(out,JSON.stringify(receipt,null,2)+'\n');const phase=x=>{receipt.phase=x;receipt.phases??=[];receipt.phases.push({phase:x,utc:new Date().toISOString()});save();};phase('starting');
try{
 const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.bin':'application/octet-stream','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.css':'text/css','.svg':'image/svg+xml'};
 phase('server-binding');server=http.createServer((req,res)=>{let f=path.resolve(mirror,'.'+decodeURIComponent(new URL(req.url,'http://x').pathname));if(!f.startsWith(path.resolve(mirror)+path.sep)){res.writeHead(403).end();return;}if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');fs.createReadStream(f).pipe(res);});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 let pw=await import('/workspace/shared/chicago-browser/node_modules/playwright/index.mjs');const chromium=pw.chromium||pw.default.chromium;
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
 timer=setTimeout(()=>{receipt.errors.push('bounded diagnostic deadline');save();browser.close().catch(()=>{});},limit*1000);
 const context=await browser.newContext({viewport:plan.viewport,hasTouch:false,isMobile:false,deviceScaleFactor:1});page=await context.newPage();await page.addInitScript(()=>{window.__MODULE_BASE='/walk/js/';});receipt.httpErrors=[];receipt.requestFailures=[];receipt.consoleErrors=[];page.on('response',r=>{if(r.status()>=400){receipt.httpErrors.push({status:r.status(),url:r.url()});save();}});page.on('requestfailed',r=>{receipt.requestFailures.push({url:r.url(),error:r.failure()});save();});page.on('console',m=>{if(m.type()==='error'){receipt.consoleErrors.push(m.text());save();}});phase('browser-launched');page.setDefaultTimeout(60_000);page.on('pageerror',e=>receipt.errors.push(e.message));
 const sourceClickChrome=new Function('page',helper+';return clickChrome;')(page);const clickChrome=async(sel)=>{phase('click:'+sel);await sourceClickChrome(sel);phase('clicked:'+sel);};const holdDraws = (on) => page.evaluate((hold) => {
    const r = window.__chicago4d.renderer;
    if (hold && !window.__smokeHeldDraw) {
      window.__smokeHeldDraw = r.render;
      r.render = () => {};
    } else if (!hold && window.__smokeHeldDraw) {
      r.render = window.__smokeHeldDraw;
      delete window.__smokeHeldDraw;
    }
  }, on);
 phase('navigating');await page.goto(`http://127.0.0.1:${server.address().port}/walk/?year=1835&keep-geometry=1`,{waitUntil:'domcontentloaded'});phase('domcontentloaded-waiting-ready');await page.waitForFunction(()=>window.__chicago4d?.ready===true||!!window.__chicago4d?.error,null,{timeout:90_000});if(await page.evaluate(()=>!!window.__chicago4d?.error))throw Error('app boot error');phase('app-ready');
 await page.evaluate(async()=>{const a=window.__chicago4d,until=Date.now()+90_000;while(a.welcome?.state!=='world'&&Date.now()<until){if(a.welcome?.state==='welcome')a.welcome.enter('spawn');await new Promise(r=>setTimeout(r,100));}if(a.welcome?.state!=='world')throw Error('world entry timeout');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();});
 phase('world-entered');await holdDraws(true);phase('draws-held-route-setup');
 // Recreate final stage13 camera-bearing route through actual person control.
 await page.evaluate(async()=>{const a=window.__chicago4d;if(!a.renderer||!a.camera||!a.scene3d)throw Error('actual renderer API unavailable');a.setFly(false);a.setPace('walk');a.setTravelMode('instantly');a.goToTarget({kind:'structure',id:'sauganash_hotel',label:'Sauganash Hotel'});a.popup.close();await a.navigator.select('people');await a.people.open('hogan_john_s_c');a.setTravelMode('horse');});
 phase('route-person-open-horse-mode-set');await clickChrome('#people-card .people-go');
 phase('route-travel-simulation');receipt.route=await page.evaluate(()=>{const a=window.__chicago4d,st=a.travelState;if(st.dest_id!=='hogan_store'||st.person!=='hogan_john_s_c')throw Error('Hoganroutepreconditionfailed');const start={...st};const end=a.travelSimulate(((st.dist_m??300)/6.5)+30);if(end.phase!=='idle'||a.popup.openId!=='hogan_store')throw Error('Hoganarrivalfailed');a.setTravelMode('instantly');a.popup.close();a.people.close();return{start,end,walker:{...a.walker.state}};});
 phase('route-arrived');
 // The intervening tour hook does not move camera (tour.js); confidence controls exact.
 await page.evaluate(async()=>{const a=window.__chicago4d;await a.navigator.select('confidence');});await page.waitForTimeout(600);
 await clickChrome('#navigator .nav-preset[data-preset="bygrade"]');await page.waitForTimeout(300);
 if(await page.evaluate(()=>document.getElementById('cm-controls-reconstructed')?.hidden!==false)){await clickChrome('#cm-look-reconstructed');await page.waitForTimeout(300);}
 phase('reconstructed-controls-open');await page.evaluate(()=>window.__chicago4d.setAnimationHold(true));phase('animation-held');await clickChrome('#cm-controls-reconstructed .nav-look[data-look="tint"]');
 const opacity=async v=>page.evaluate(v=>{const e=document.getElementById('cm-opacity-reconstructed');e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));},v);
 phase('opacity-100-setting');await opacity(100);phase('opacity-100-set');await clickChrome('#cm-controls-reconstructed .nav-swatch[data-set="safe"]');
 phase('confidence-controls-set');await holdDraws(false);phase('draws-restored-before-stats');receipt.initial=await page.evaluate(()=>{const a=window.__chicago4d;return{detail:a.detail,stats:a.stats(),walker:{...a.walker.state},camera:{position:a.camera.position.toArray(),quaternion:a.camera.quaternion.toArray()},rendererOwnMethods:{render:Object.hasOwn(a.renderer,'render'),renderBufferDirect:Object.hasOwn(a.renderer,'renderBufferDirect')},grade:a.confidence.grade('reconstructed')};});
 if(receipt.initial.stats.budget.drawCalls!==330)throw Error('unchanged330budgetpreconditionfailed');
 receipt.prewarmCamera=receipt.initial.camera;receipt.comparisons=[];
 for(const mode of ['tint','row-ghost','xray']){
  await holdDraws(true);try{
   if(mode==='tint'){await clickChrome('#cm-controls-reconstructed .nav-look[data-look="tint"]');await opacity(100);}
   if(mode==='row-ghost'){await opacity(0);await clickChrome('#cm-controls-reconstructed .nav-look[data-look="ghost"]');await opacity(40);}
   if(mode==='xray')await clickChrome('#navigator .nav-preset[data-preset="xray"]');
  }finally{await holdDraws(false);}
  phase('draws-restored-before-pixel-comparison:'+mode);if(fs.existsSync(path.join(pixelOutput,mode)))throw Error('pixel output already exists:'+mode);
  const comparison=await compareHeldPage(page,{outdir:path.join(pixelOutput,mode)});
  comparison.mode=mode;receipt.comparisons.push(comparison);receipt.preparedCamera??=comparison.stableAfter.camera;save();if(JSON.stringify(comparison.stableAfter.camera)!==JSON.stringify(receipt.preparedCamera))throw Error('prepared-camera-moved-between-modes');if(!comparison.ok)throw Error('comparison-helper-rejected');
  if(!comparison.strict330Unchanged||!comparison.frames.every(f=>f.stats.drawCalls<=330))throw Error('strict330budgetfailure:'+mode);
  if(comparison.restoredPixels.changedChannels!==0||comparison.restoreCalls!==0)throw Error('restoredpixelsorcallsnotexact:'+mode);
  if(comparison.candidatePixels.changedChannels!==0)throw Error('candidatepixelsnotexact:'+mode);
  if(mode==='tint'&&comparison.callsSaved!==0)throw Error('tintcallschanged');
  if(mode!=='tint'&&comparison.callsSaved<2)throw Error('expected-visible-billboard-draw-saving-not-demonstrated:'+mode);
 }
 receipt.sameCamera=await page.evaluate(first=>JSON.stringify([...window.__chicago4d.camera.position,...window.__chicago4d.camera.quaternion])===JSON.stringify(first),receipt.preparedCamera);
 if(!receipt.sameCamera)throw Error('cameramovedbetweenmodes');
 await clickChrome('#navigator .nav-preset[data-preset="normal"]');await page.evaluate(async()=>{const a=window.__chicago4d;a.setAnimationHold(false);await a.navigator.select('home');a.navigator.dock();a.popup.close();});
 receipt.normalRestored=await page.evaluate(()=>!window.__chicago4d.confidence.ghosting&&!window.__chicago4d.confidenceView);if(!receipt.normalRestored)throw Error('normalrestorationfailed');save();
 phase('normal-restored');if(refusalModule){phase('refusal-controls');const m=await import(pathToFileURL(path.resolve(refusalModule)));receipt.refusals=await m.runHudRefusals(page,{output:refusalOutput});save();}
 receipt.completed=true;phase('completed');
}catch(e){if(e.partialReceipt){receipt.failedComparison=e.partialReceipt;save();}try{await page?.evaluate(()=>{const r=window.__chicago4d?.renderer;if(r&&window.__smokeHeldDraw){r.render=window.__smokeHeldDraw;delete window.__smokeHeldDraw;}});}catch{}receipt.errors.push(e.stack||String(e));receipt.failedPhase=receipt.phase;try{receipt.failureState=await page?.evaluate(()=>({url:location.href,error:window.__chicago4d?.error??null,problems:window.__chicago4d?.problems??[],ready:window.__chicago4d?.ready??null,apiKeys:Object.keys(window.__chicago4d??{}),boot:window.__chicago4d?.boot??null,dataset:{...document.documentElement.dataset},text:document.body.innerText.slice(0,10000)}));await page?.screenshot({path:out+'.failure.png',timeout:5000});}catch(captureError){receipt.captureError=String(captureError);}process.exitCode=1;}finally{try{await page?.evaluate(()=>{const r=window.__chicago4d?.renderer;if(r&&window.__smokeHeldDraw){r.render=window.__smokeHeldDraw;delete window.__smokeHeldDraw;}});}catch{}clearTimeout(timer);save();await browser?.close().catch(()=>{});if(server)await new Promise(r=>server.close(r));console.log(JSON.stringify({receipt:out,completed:receipt.completed??false,errors:receipt.errors}));}
