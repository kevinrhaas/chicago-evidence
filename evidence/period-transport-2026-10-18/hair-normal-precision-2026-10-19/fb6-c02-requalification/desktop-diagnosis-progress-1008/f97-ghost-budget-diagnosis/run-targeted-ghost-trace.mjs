#!/usr/bin/env node
// OUTSIDE diagnostic. Preparation only unless --run is explicitly supplied after root release.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import crypto from 'node:crypto';import {pathToFileURL}from'node:url';
const argv=process.argv.slice(2),get=(k,d)=>{const i=argv.indexOf(k);return i<0?d:argv[i+1];};
const checkout=get('--checkout','/workspace/chicago'),mirror=get('--mirror',path.join(checkout,'site/4d')),out=get('--out','/workspace/shared/f97-ghost-budget-diagnosis/run-receipt.json'),hudModule=get('--hud-module',null),limit=Number(get('--max-seconds','240'));
const smokePath=path.join(checkout,'chicago/4d/tools/smoke_renderer.mjs'),source=fs.readFileSync(smokePath,'utf8');
const helper=source.slice(source.indexOf('  const clickChrome = async (sel) => {'),source.indexOf('  // T-2620: the drawer and its hamburger'));
if(!helper.includes('el.click();')||!helper.includes('elementFromPoint'))throw Error('actual clickChrome extraction failed');
const traceSource=fs.readFileSync(new URL('./trace-one-frame.js',import.meta.url),'utf8');
const traceFunction=new Function('return ('+traceSource+')')();
const plan={kind:'bounded targeted published ghost draw diagnosis; not full smoke',checkout,mirror,out,limit,hudModule,viewport:{width:1280,height:800},source_sha256:crypto.createHash('sha256').update(source).digest('hex'),route:'source stage13 final camera-bearing path: instantSauganash→HoganpersonGoTherehorse→travelSimulate→instantly; no later stage13 camera-bearing action beforeT2648',limits:'Does not reconstruct accumulated70minasync/lazy residency. PriorCI didnotlogcamera; actualpose andstate recorded, no claim331reproduceduntil measured.',run:argv.includes('--run')};
if(!plan.run){console.log(JSON.stringify(plan,null,2));process.exit(0);}
if(fs.existsSync(out))throw Error('fresh outside receipt path required');
let browser,server,timer;const receipt={...plan,started_utc:new Date().toISOString(),samples:[],errors:[]};const save=()=>fs.writeFileSync(out,JSON.stringify(receipt,null,2)+'\n');
try{
 const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.bin':'application/octet-stream','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.css':'text/css','.svg':'image/svg+xml'};
 server=http.createServer((req,res)=>{let f=path.resolve(mirror,'.'+decodeURIComponent(new URL(req.url,'http://x').pathname));if(!f.startsWith(path.resolve(mirror)+path.sep)){res.writeHead(403).end();return;}if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');fs.createReadStream(f).pipe(res);});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 let pw=await import('/workspace/shared/chicago-browser/node_modules/playwright/index.mjs');const chromium=pw.chromium||pw.default.chromium;
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 timer=setTimeout(()=>{receipt.errors.push('bounded diagnostic deadline');save();browser.close().catch(()=>{});},limit*1000);
 const context=await browser.newContext({viewport:plan.viewport,hasTouch:false,isMobile:false,deviceScaleFactor:1});const page=await context.newPage();page.setDefaultTimeout(60_000);page.on('pageerror',e=>receipt.errors.push(e.message));
 const clickChrome=new Function('page',helper+';return clickChrome;')(page);
 await page.goto(`http://127.0.0.1:${server.address().port}/walk/?year=1835&keep-geometry=1`,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:90_000});
 await page.evaluate(async()=>{const a=window.__chicago4d,until=Date.now()+90_000;while(a.welcome?.state!=='world'&&Date.now()<until){if(a.welcome?.state==='welcome')a.welcome.enter('spawn');await new Promise(r=>setTimeout(r,100));}if(a.welcome?.state!=='world')throw Error('world entry timeout');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();});
 // Recreate final stage13 camera-bearing route through actual person control.
 await page.evaluate(async()=>{const a=window.__chicago4d;if(!a.renderer||!a.camera||!a.scene3d)throw Error('actual renderer API unavailable');a.setFly(false);a.setPace('walk');a.setTravelMode('instantly');a.goToTarget({kind:'structure',id:'sauganash_hotel',label:'Sauganash Hotel'});a.popup.close();await a.navigator.select('people');await a.people.open('hogan_john_s_c');a.setTravelMode('horse');});
 await clickChrome('#people-card .people-go');
 receipt.route=await page.evaluate(()=>{const a=window.__chicago4d,st=a.travelState;if(st.dest_id!=='hogan_store'||st.person!=='hogan_john_s_c')throw Error('Hoganroutepreconditionfailed');const start={...st};const end=a.travelSimulate(((st.dist_m??300)/6.5)+30);if(end.phase!=='idle'||a.popup.openId!=='hogan_store')throw Error('Hoganarrivalfailed');a.setTravelMode('instantly');a.popup.close();a.people.close();return{start,end,walker:{...a.walker.state}};});
 // The intervening tour hook does not move camera (tour.js); confidence controls exact.
 await page.evaluate(async()=>{const a=window.__chicago4d;await a.navigator.select('confidence');});await page.waitForTimeout(600);
 await clickChrome('#navigator .nav-preset[data-preset="bygrade"]');await page.waitForTimeout(300);
 if(await page.evaluate(()=>document.getElementById('cm-controls-reconstructed')?.hidden!==false)){await clickChrome('#cm-look-reconstructed');await page.waitForTimeout(300);}
 await page.evaluate(()=>window.__chicago4d.setAnimationHold(true));await clickChrome('#cm-controls-reconstructed .nav-look[data-look="tint"]');
 const opacity=async v=>page.evaluate(v=>{const e=document.getElementById('cm-opacity-reconstructed');e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));},v);
 await opacity(100);await clickChrome('#cm-controls-reconstructed .nav-swatch[data-set="safe"]');
 receipt.initial=await page.evaluate(()=>{const a=window.__chicago4d;return{detail:a.detail,stats:a.stats(),walker:{...a.walker.state},camera:{position:a.camera.position.toArray(),quaternion:a.camera.quaternion.toArray()},rendererOwnMethods:{render:Object.hasOwn(a.renderer,'render'),renderBufferDirect:Object.hasOwn(a.renderer,'renderBufferDirect')},grade:a.confidence.grade('reconstructed')};});
 if(receipt.initial.stats.budget.drawCalls!==330)throw Error('unchanged330budgetpreconditionfailed');
 const trace=async(mode,phase)=>{const sample=await page.evaluate(traceFunction);sample.mode=mode;sample.phase=phase;receipt.samples.push(sample);save();if(!sample.instrumentationValid)throw Error('drawtrace didnotaccountforactualrendererinfo');};
 for(const mode of['tint','row-ghost','xray']){
  if(mode==='tint'){await clickChrome('#cm-controls-reconstructed .nav-look[data-look="tint"]');await opacity(100);}
  if(mode==='row-ghost'){await opacity(0);await clickChrome('#cm-controls-reconstructed .nav-look[data-look="ghost"]');await opacity(40);}
  if(mode==='xray')await clickChrome('#navigator .nav-preset[data-preset="xray"]');
  await trace(mode,'cold');await page.waitForTimeout(300);await page.evaluate(()=>window.__chicago4d.capture());await trace(mode,'settled');
 }
 const first=receipt.samples[0].camera;receipt.sameCamera=receipt.samples.every(s=>JSON.stringify(s.camera)===JSON.stringify(first));if(!receipt.sameCamera)throw Error('cameramovedbetweenmodes');
 await clickChrome('#navigator .nav-preset[data-preset="normal"]');await page.evaluate(async()=>{const a=window.__chicago4d;a.setAnimationHold(false);await a.navigator.select('home');a.navigator.dock();a.popup.close();});
 receipt.normalRestored=await page.evaluate(()=>!window.__chicago4d.confidence.ghosting&&!window.__chicago4d.confidenceView);if(!receipt.normalRestored)throw Error('normalrestorationfailed');save();
 if(hudModule){const m=await import(pathToFileURL(path.resolve(hudModule)));receipt.hud=await m.runHudQualification(page,{output:path.join(path.dirname(out),'hud')});}
 receipt.completed=true;
}catch(e){receipt.errors.push(e.stack||String(e));process.exitCode=1;}finally{clearTimeout(timer);save();await browser?.close().catch(()=>{});if(server)await new Promise(r=>server.close(r));console.log(JSON.stringify({receipt:out,completed:receipt.completed??false,errors:receipt.errors}));}
