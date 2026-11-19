/** One-viewport published-town focus reproduction. Requires an explicit frozen QA_ROOT.
 * One town only, normal api.step frames, no publisher or source mutations. */
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import assert from 'node:assert/strict';
import {createRequire} from 'node:module';import {createHash} from 'node:crypto';import {execFileSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const app=path.resolve(process.env.QA_APP||'/workspace/chicago-rail/chicago/4d');assert(process.env.QA_ROOT,'QA_ROOT required');const site=path.resolve(process.env.QA_ROOT),out=path.resolve(process.env.QA_OUT||'/tmp/t3658-stage13-published-focus');
const width=Number(process.env.QA_WIDTH||1280),height=width===390?780:800;assert([390,1280].includes(width));
const hash=b=>createHash('sha256').update(b).digest('hex');const sourceCommit=execFileSync('git',['rev-parse','HEAD'],{cwd:app,encoding:'utf8'}).trim();
const testedFiles={};for(const f of ['main.js','navigator.js','nav-rail.js','controls/keyboard.js','controls/pointerlock.js','controls/intent.js']){const source=hash(fs.readFileSync(path.join(app,'renderers/web/js',f))),published=hash(fs.readFileSync(path.join(site,'walk/js',f)));assert.equal(source,published,f+' published/source mismatch');testedFiles[f]=source;}
const smoke=fs.readFileSync(path.join(app,'tools/smoke_renderer.mjs'),'utf8');const start=smoke.indexOf('    // Space is mode-scoped:');const end=smoke.indexOf('    // And neither fires from inside the Go-to box:',start);assert(start>0&&end>start);const block=smoke.slice(start,end);
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'tested-smoke-block.js'),block);
const report={started:new Date().toISOString(),sourceCommit,site,width,height,testedFiles,smokeHash:hash(smoke),blockHash:hash(block),harnessHash:hash(fs.readFileSync(fileURLToPath(import.meta.url))),checks:[],errors:[],httpErrors:[],requestsFailed:[],navigation:[],consoleWarnings:[],scope:'One published 1835 town, Light detail, actual source Space/UI/inspection smoke block and normal api.step frames. Continuous drawing paused between interactions. Not the full stage14 release gate.'};const save=()=>fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');save();
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.glb':'model/gltf-binary','.wasm':'application/wasm','.svg':'image/svg+xml','.ktx2':'image/ktx2','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{try{let f=path.resolve(site,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!f.startsWith(site+path.sep)&&f!==site){res.writeHead(403).end();return;}if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream','Cache-Control':'no-store'});fs.createReadStream(f).pipe(res);}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;report.origin=origin;
const {chromium}=createRequire('/workspace/chicago/package.json')('playwright');let browser,context,page;
const check=(label,pass,detail='')=>{report.checks.push({label,pass:!!pass,detail});console.log(new Date().toISOString(),pass?'PASS':'FAIL',label,detail);save();assert(pass,label+': '+detail);};
const snapshot=()=>page.evaluate(()=>{const a=window.__chicago4d,el=document.activeElement;return{focus:{tag:el?.tagName,id:el?.id},nav:{app:a.navigator.app,level:a.navigator.level},inspecting:a.inspecting,flying:a.player.flying,alt:a.player.altitude,e:a.player.e,n:a.player.n};});
try{
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader','--disable-features=BackForwardCache']});context=await browser.newContext({viewport:{width,height},hasTouch:width===390,isMobile:width===390,deviceScaleFactor:1,reducedMotion:'reduce'});
 await context.addInitScript(()=>{if(location.origin !== 'null')localStorage.setItem('chicago4d.settings',JSON.stringify({soundMaster:0,detail:'light',quality:1}));});
 page=await context.newPage();page.setDefaultTimeout(60000);page.on('pageerror',e=>{report.errors.push({at:Date.now(),text:String(e)});save();});page.on('console',m=>{if(m.type()==='error'&&!m.text().startsWith('Failed to load resource')){report.errors.push({at:Date.now(),text:m.text()});save();}});page.on('response',r=>{if(r.status()>=400)report.httpErrors.push({url:r.url(),status:r.status()});});page.on('requestfailed',r=>report.requestsFailed.push({url:r.url(),reason:r.failure()?.errorText}));
 page.on('framenavigated',f=>{if(f===page.mainFrame()){report.navigation.push({at:new Date().toISOString(),kind:'navigated',url:f.url()});console.log('NAVIGATED',f.url());save();}});
 page.on('request',r=>{if(r.isNavigationRequest()){report.navigation.push({at:new Date().toISOString(),kind:'request',url:r.url()});save();}});
 page.on('crash',()=>{report.navigation.push({at:new Date().toISOString(),kind:'crash'});save();});
 page.on('close',()=>{report.navigation.push({at:new Date().toISOString(),kind:'close'});save();});
 page.on('console',m=>{if(m.type()==='warning'){report.consoleWarnings.push({at:new Date().toISOString(),text:m.text()});save();}});
 await page.goto(origin+'/walk/?year=1835&detail=light&keep-geometry=1',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>{const a=window.__chicago4d;if(a?.ready){a.renderer.setAnimationLoop(null);return true;}return!!a?.error;},null,{timeout:240000,polling:500});
 check('Published town ready',await page.evaluate(()=>window.__chicago4d.ready&&!window.__chicago4d.error));
 await page.waitForFunction(()=>['welcome','world'].includes(window.__chicago4d.welcome?.state),null,{timeout:90000,polling:500});await page.evaluate(()=>{if(__chicago4d.welcome.state==='welcome')__chicago4d.welcome.enter('spawn');});await page.waitForFunction(()=>__chicago4d.welcome.state==='world',null,{timeout:90000,polling:500});
 await page.evaluate(async()=>{const a=__chicago4d;a.renderer.setAnimationLoop(null);await a.navigator.select('guide');a.navigator.open(2);});
 // Same focus+click semantics as the smoke helper; no camera/keyboard mutation.
 await page.evaluate(()=>{const el=document.getElementById('nav-close');el.focus({preventScroll:true});el.click();});
 report.afterClose=await snapshot();
 await page.evaluate(()=>{const a=__chicago4d;a.goTo('from_above');a.setFly(false);a.goTo('sauganash');a.frame('sauganash_hotel',26);a.nameCards?.setShown(false);a.closeBuilding();a.step();});
 report.beforeUnfocusedSpace=await snapshot();
 check('Camera setup retains Navigator control focus', ['nav-grip','nav-collapse'].includes(report.beforeUnfocusedSpace.focus.id),JSON.stringify(report.beforeUnfocusedSpace));
 await page.keyboard.press('Space');await page.waitForTimeout(250);await page.evaluate(()=>__chicago4d.step());report.afterUnfocusedSpace=await snapshot();
 check('Original missing-world-focus setup activates UI instead of inspecting',!report.afterUnfocusedSpace.inspecting&&!report.afterUnfocusedSpace.flying&&report.afterUnfocusedSpace.nav.level>0,JSON.stringify(report.afterUnfocusedSpace));
 await page.evaluate(()=>{__chicago4d.closeBuilding();__chicago4d.navigator.dock();__chicago4d.setFly(false);});
 const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;await new AsyncFunction('page','check','label',block)(page,check,`focused published ${width}x${height}`);
 report.final=await snapshot();await page.screenshot({path:path.join(out,width+'-verified-space.png')});
 check('Zero page/console errors',report.errors.length===0,JSON.stringify(report.errors));check('Zero HTTP errors',report.httpErrors.length===0,JSON.stringify(report.httpErrors));
 report.pass=true;
}catch(e){report.pass=false;report.error=String(e.stack||e);report.errorUrl=page?.url();console.error('PROBE FAILED',report.error);save();throw e;}finally{report.cleanupStarted=new Date().toISOString();save();await browser?.close();await new Promise(r=>server.close(r));report.finished=new Date().toISOString();save();}
console.log('PUBLISHED SPACE FOCUS PASS',out);
