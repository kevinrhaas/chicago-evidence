#!/usr/bin/env node
// OUTSIDE diagnostic. Preparation only unless --run is explicitly supplied after root release.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import crypto from 'node:crypto';import {pathToFileURL}from'node:url';
const argv=process.argv.slice(2),get=(k,d)=>{const i=argv.indexOf(k);return i<0?d:argv[i+1];};
const checkout=get('--checkout','/workspace/chicago'),mirror=get('--mirror',path.join(checkout,'site/4d')),out=get('--out','/workspace/shared/f97-ghost-budget-diagnosis/run-receipt.json'),hudModule=get('--hud-module','/workspace/shared/hud-footprint-f97-harness/hud-qualification-v3.mjs'),limit=Number(get('--max-seconds','400'));
const smokePath=path.join(checkout,'chicago/4d/tools/smoke_renderer.mjs'),source=fs.readFileSync(smokePath,'utf8');
const helper=source.slice(source.indexOf('  const clickChrome = async (sel) => {'),source.indexOf('  // T-2620: the drawer and its hamburger'));
if(!helper.includes('el.click();')||!helper.includes('elementFromPoint'))throw Error('actual clickChrome extraction failed');
const hudOutput=path.join(path.dirname(out),path.basename(out,'.json')+'-hud-v3');
const hashFile=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const plan={harness_sha256:hashFile(new URL(import.meta.url)),hud_module_sha256:hudModule?hashFile(hudModule):null,hudOutput,kind:'standalone bounded published HUDv3 diagnostic; no route or pixel probe; not full smoke',checkout,mirror,out,limit,hudModule,viewport:{width:1280,height:800},source_sha256:crypto.createHash('sha256').update(source).digest('hex'),route:'fresh boot→world→source applyPreset normal→Home/dock→HUDv3 exact lead-ins',limits:'Does not reconstruct accumulated70minasync/lazy residency. PriorCI didnotlogcamera; actualpose andstate recorded, no claim331reproduceduntil measured.',run:argv.includes('--run')};
if(!plan.run){console.log(JSON.stringify(plan,null,2));process.exit(0);}
for(const target of[out,hudOutput])if(fs.existsSync(target))throw Error('fresh outside output required:'+target);
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
 phase('world-entered');
 phase('normal-home-dock-preparing');await page.evaluate(async()=>{const a=window.__chicago4d;const {applyPreset}=await import('/walk/js/confidence-presets.js');if(!applyPreset('normal',{hud:a.hud,view:a.confidence,announce:false}))throw Error('normal preset failed');a.setAnimationHold(false);await a.navigator.select('home');a.navigator.dock();a.popup.close();});
 receipt.normalRestored=await page.evaluate(()=>!window.__chicago4d.confidence.ghosting&&!window.__chicago4d.confidenceView);if(!receipt.normalRestored)throw Error('normalrestorationfailed');save();
 phase('normal-restored');if(hudModule){phase('hud-running');const m=await import(pathToFileURL(path.resolve(hudModule)));receipt.hud=await m.runHudQualification(page,{output:hudOutput});}
 receipt.completed=true;phase('completed');
}catch(e){try{await page?.evaluate(()=>{const r=window.__chicago4d?.renderer;if(r&&window.__smokeHeldDraw){r.render=window.__smokeHeldDraw;delete window.__smokeHeldDraw;}});}catch{}receipt.errors.push(e.stack||String(e));receipt.failedPhase=receipt.phase;try{receipt.failureState=await page?.evaluate(()=>({url:location.href,error:window.__chicago4d?.error??null,problems:window.__chicago4d?.problems??[],ready:window.__chicago4d?.ready??null,apiKeys:Object.keys(window.__chicago4d??{}),boot:window.__chicago4d?.boot??null,dataset:{...document.documentElement.dataset},text:document.body.innerText.slice(0,10000)}));await page?.screenshot({path:out+'.failure.png',timeout:5000});}catch(captureError){receipt.captureError=String(captureError);}process.exitCode=1;}finally{try{await page?.evaluate(()=>{const r=window.__chicago4d?.renderer;if(r&&window.__smokeHeldDraw){r.render=window.__smokeHeldDraw;delete window.__smokeHeldDraw;}});}catch{}clearTimeout(timer);save();await browser?.close().catch(()=>{});if(server)await new Promise(r=>server.close(r));console.log(JSON.stringify({receipt:out,completed:receipt.completed??false,errors:receipt.errors}));}
