import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const { chromium } = createRequire('/workspace/chicago/package.json')('playwright');
const app = '/workspace/chicago-rail/chicago/4d', web = path.join(app,'renderers/web');
const out = '/tmp/t3658-keyboard-ownership-browser';
fs.mkdirSync(out,{recursive:true});
const index=fs.readFileSync(path.join(web,'index.html'),'utf8');
const start=index.indexOf('<section id="navigator"'), end=index.indexOf('\n</section>',start)+'\n</section>'.length;
assert(start>=0 && end>start);
const script=`
import { createNavigator } from '/js/navigator.js';
import { createIntent, createBackendSwitch } from '/js/controls/intent.js';
import { createPointerLockBackend } from '/js/controls/pointerlock.js';
import { createDesktopKeyCapture } from '/js/controls/keyboard.js';
const canvas=document.getElementById('world'), popup=document.getElementById('popup');
const intent=createIntent(), backends=createBackendSwitch(intent);
let locks=0, activates=0, clicks=0, holding=false, byHand=false, preventCode=null;
// Observe the actual PointerLockControls request boundary without taking browser focus.
canvas.requestPointerLock=()=>{locks++;};
const apps=[{id:'home',label:'Home',order:0,panel:'nav-home'},...['map','inspect','settings'].map((id,i)=>({id,label:id,order:(i+1)*10,mount(el){const h=document.createElement('h2');h.textContent=id;const b=document.createElement('button');b.id=id+'-action';b.textContent='Activate '+id;b.onclick=()=>clicks++;el.append(h,b);}}))];
const nav=createNavigator({root:document.getElementById('navigator'),apps,storage:null,scene:{id:'1835',target_date:'1835-07-01',lighting:{local_time:'10:30'}}});
const backend=createPointerLockBackend({intent,domElement:canvas,holding:()=>holding,inspecting:()=>byHand&&nav.app==='inspect'});
backends.activate(backend);
window.addEventListener('keydown',e=>{if(e.code===preventCode)e.preventDefault();},{capture:true});
window.addEventListener('keydown',createDesktopKeyCapture({holding:()=>holding,inspecting:()=>byHand&&nav.app==='inspect',activate:()=>{activates++;backends.activate(backend);},lock:()=>backend.lock()}),{capture:true});
document.getElementById('outside-action').onclick=()=>clicks++;
document.getElementById('dialog-close').onclick=()=>document.getElementById('native-dialog').close();
window.qa={nav,intent,backend,canvas,
  reset(){window.dispatchEvent(new Event('blur'));intent.clear();intent.flying=false;locks=activates=clicks=0;holding=byHand=false;preventCode=null;popup.hidden=true;},
  popup(value){holding=value;popup.hidden=!value;},
  byHand(value){byHand=value;}, prevent(code){preventCode=code;}, consume(){return intent.takeInteract();},
  snap(){backend.update();return {locks,activates,clicks,forward:intent.forward,strafe:intent.strafe,rise:intent.rise,sprint:intent.sprint,interact:intent.interact,source:intent.interactSource,focus:document.activeElement?.id,app:nav.app,level:nav.level,dialogOpen:document.getElementById('native-dialog').open};}
};
window.fixtureReady=true;
`;
const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Desktop keyboard ownership fixture</title><link rel="icon" href="data:,"><link rel="stylesheet" href="/css/navigator.css"><script type="importmap">{"imports":{"three":"/vendor/three-0.185.1/three.module.js","three/addons/":"/vendor/three-0.185.1/addons/"}}</script><style>
:root{--ink:#f7f2df;--ink-dim:#d9d0b5;--ink-faint:#b4aa8c;--panel:#242620;--panel-solid:#242620;--edge:#858068;--edge-strong:#aea387;--accent:#ffcf69;--signal:#ff7979;--font-body:system-ui,sans-serif;--font-mono:ui-monospace,monospace;--ease-detent:ease;--shadow:0 8px 20px #0007}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#111811;font:15px system-ui,sans-serif}[hidden]{display:none!important}button,input,summary{font:inherit;color:inherit;background:#30392d;border:1px solid #858068;padding:8px;min-height:36px}button:focus-visible,canvas:focus-visible,dialog:focus-visible{outline:3px solid #ffcf69;outline-offset:2px}.fixture-controls{position:relative;margin-left:auto;width:280px;padding:12px}canvas{display:block;background:#284033;width:240px;height:75px}dialog{background:#242620;color:#fff;max-width:280px}.visually-hidden{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}#popup{position:absolute;z-index:50;right:8px;top:60px;background:#242620;padding:12px}
</style></head><body><div class="fixture-controls"><h1>Keyboard ownership</h1><p>Real Navigator and desktop input modules; no world or renderer.</p><canvas id="world" tabindex="0" aria-label="World focus target"></canvas><button id="outside-action">Native action</button><details id="native-details"><summary id="native-summary">Native summary</summary><p>Opened by Space.</p></details></div>${index.slice(start,end)}<aside id="popup" hidden tabindex="-1"><button id="popup-action">Card action</button><input id="popup-input" aria-label="Card note"></aside><dialog id="native-dialog" tabindex="-1"><p>Native dialog with no explicit role.</p><button id="dialog-close">Close</button></dialog><script type="module" src="/fixture.js"></script></body></html>`;
fs.writeFileSync(path.join(out,'fixture.html'),html);fs.writeFileSync(path.join(out,'fixture.js'),script);
const hash=b=>createHash('sha256').update(b).digest('hex');
const report={started:new Date().toISOString(),sourceCommit:execFileSync('git',['rev-parse','HEAD'],{cwd:app,encoding:'utf8'}).trim(),workingDiff:execFileSync('git',['diff','--stat'],{cwd:app,encoding:'utf8'}).trim(),sourceHashes:{},runs:[],requests:[],scope:'Actual Navigator, desktop capture, PointerLockControls and movement backend; native keyboard/button/dialog/focus behavior; no world/WebGL.',limits:['PointerLockControls requests are observed at the canvas method; the fixture does not grant mouse capture.','Chromium emulated viewports; not physical-device or screen-reader certification.']};
for(const p of ['js/controls/keyboard.js','js/controls/pointerlock.js','js/controls/intent.js','js/navigator.js','js/nav-rail.js','js/main.js','css/navigator.css'])report.sourceHashes[p]=hash(fs.readFileSync(path.join(web,p)));
report.harness={path:fileURLToPath(import.meta.url),sha256:hash(fs.readFileSync(fileURLToPath(import.meta.url)))};
const save=()=>fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
const server=http.createServer((req,res)=>{const p=new URL(req.url,'http://local').pathname;report.requests.push(p);if(p==='/'){res.setHeader('Content-Type','text/html');res.end(html);return;}if(p==='/fixture.js'){res.setHeader('Content-Type','text/javascript');res.end(script);return;}if(!(/^\/(js|vendor)\/[a-zA-Z0-9_.\/-]+\.js$/.test(p)||p==='/css/navigator.css')){res.statusCode=403;res.end();return;}const f=path.resolve(web,'.'+p);if(!f.startsWith(web+path.sep)||!fs.existsSync(f)){res.statusCode=404;res.end();return;}res.setHeader('Content-Type',p.endsWith('.css')?'text/css':'text/javascript');res.end(fs.readFileSync(f));});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
let browser;
try{
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-gpu','--disable-webgl']});
 for(const width of [390,1280]){
  const row={width,height:width===390?780:800,checks:[],errors:[],httpErrors:[],blockedRequests:[]};report.runs.push(row);
  const ctx=await browser.newContext({viewport:{width,height:row.height},reducedMotion:'reduce'}), page=await ctx.newPage();page.setDefaultTimeout(10000);
  page.on('pageerror',e=>row.errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)row.httpErrors.push({url:r.url(),status:r.status()});});
  await page.route('**/*',route=>{if(!route.request().url().startsWith(origin+'/')){row.blockedRequests.push(route.request().url());return route.abort();}return route.continue();});
  const snap=()=>page.evaluate(()=>qa.snap());
  const still=s=>assert.deepEqual([s.forward,s.strafe,s.rise,s.sprint,s.interact],[0,0,0,false,false],JSON.stringify(s));
  const check=async(label,fn)=>{try{const details=await fn();row.checks.push({label,pass:true,details});console.log(width,'PASS',label);save();}catch(e){row.checks.push({label,pass:false,error:String(e.stack||e),snapshot:await snap().catch(()=>null)});save();throw e;}};
  const tabUntil=async(sel,reverse=false)=>{const ids=[];for(let i=0;i<24;i++){await page.keyboard.press(reverse?'Shift+Tab':'Tab');const s=await page.evaluate(sel=>({id:document.activeElement.id,match:document.activeElement.matches(sel)}),sel);ids.push(s.id);if(s.match)return ids;}throw Error('Tab never reached '+sel+': '+ids.join(','));};
  try{
   await page.goto(origin,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.fixtureReady);
   await check('Native rail arrows move focus; Space activates its button without world input',async()=>{await page.keyboard.press('n');await tabUntil('.nav-tabs [role="tab"]',true);await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');let s=await snap();assert.equal(s.focus,'nav-tab-map');assert.equal(s.app,'home');assert.equal(s.locks,0);still(s);await page.keyboard.press('Space');await page.waitForFunction(()=>qa.nav.app==='map');s=await snap();assert.equal(s.focus,'nav-app-map');assert.equal(s.locks,0);still(s);return s;});
   await check('Native app-button Space clicks once and does not inspect',async()=>{await page.keyboard.press('Tab');assert.equal((await snap()).focus,'map-action');await page.keyboard.press('Space');const s=await snap();assert.equal(s.clicks,1);assert.equal(s.locks,0);still(s);return s;});
   await check('Standalone native button and summary keep their Space defaults',async()=>{await page.evaluate(()=>qa.reset());await page.locator('#outside-action').focus();await page.keyboard.press('Space');await page.locator('#native-summary').focus();await page.keyboard.press('Space');assert.equal(await page.locator('#native-details').evaluate(el=>el.open),true);const s=await snap();assert.equal(s.clicks,1);assert.equal(s.locks,0);still(s);return s;});
   await check('Role-less native dialog itself owns Arrow and E; its Close button keeps Space',async()=>{await page.evaluate(()=>{qa.reset();qa.popup(true);const d=document.getElementById('native-dialog');d.showModal();d.focus();});await page.keyboard.press('ArrowDown');await page.keyboard.press('e');let s=await snap();assert.equal(s.focus,'native-dialog');assert(s.dialogOpen);assert.equal(s.locks,0);still(s);await page.keyboard.press('Tab');assert.equal((await snap()).focus,'dialog-close');await page.keyboard.press('Space');s=await snap();assert.equal(s.dialogOpen,false);still(s);return s;});
   await check('Popup E closes by inspect intent while text entry keeps E',async()=>{await page.evaluate(()=>{qa.reset();qa.popup(true);});await page.locator('#popup-action').focus();await page.keyboard.press('e');let s=await snap();assert.equal(s.interact,true);assert.equal(s.source,'key');await page.evaluate(()=>qa.consume());await page.locator('#popup-input').focus();await page.keyboard.type('e');assert.equal(await page.locator('#popup-input').inputValue(),'e');s=await snap();still(s);assert.equal(s.locks,0);return s;});
   await check('Hand-opened Navigator Inspect retains E; automatic Inspect keeps it',async()=>{await page.evaluate(async()=>{qa.reset();await qa.nav.select('inspect');qa.byHand(true);});await page.locator('#inspect-action').focus();await page.keyboard.press('e');let s=await snap();assert(s.interact);await page.evaluate(()=>{qa.consume();qa.byHand(false);});await page.keyboard.press('e');s=await snap();still(s);assert.equal(s.locks,0);return s;});
   await check('World focus walks and inspects while Navigator stays visible',async()=>{await page.evaluate(()=>qa.reset());await page.locator('#world').focus();await page.keyboard.down('w');let s=await snap();assert.equal(s.forward,1);assert.equal(s.locks,1);assert(s.level>0);await page.keyboard.up('w');await page.keyboard.press('Space');s=await snap();assert.equal(s.interact,true);assert.equal(s.forward,0);await page.evaluate(()=>qa.consume());return s;});
   await check('Tab transfers real focus and releases already-held movement without resurrecting it',async()=>{await page.evaluate(()=>{qa.reset();qa.nav.dock();});await page.locator('#world').focus();await page.keyboard.down('w');assert.equal((await snap()).forward,1);await page.keyboard.press('Tab');let s=await snap();assert(s.focus.startsWith('nav-'));still(s);await page.locator('#world').focus();s=await snap();still(s);await page.keyboard.up('w');return s;});
   await check('Already-prevented native keys cannot activate capture or backend',async()=>{await page.evaluate(()=>{qa.reset();qa.prevent('KeyW');});await page.locator('#world').focus();await page.keyboard.press('w');let s=await snap();assert.equal(s.locks,0);assert.equal(s.activates,0);still(s);await page.evaluate(()=>qa.prevent(null));return s;});
   await check('No page errors, external fetches or HTTP failures',async()=>{assert.deepEqual(row.errors,[]);assert.deepEqual(row.httpErrors,[]);assert.deepEqual(row.blockedRequests,[]);await page.evaluate(()=>qa.nav.select('map'));await page.locator('#map-action').focus();await page.screenshot({path:path.join(out,width+'-focused-control.png')});return {errors:row.errors,requests:report.requests.length};});
  }finally{await ctx.close();save();}
 }
 report.pass=true;
}catch(e){report.pass=false;report.error=String(e.stack||e);throw e;}finally{await browser?.close();await new Promise(r=>server.close(r));report.finished=new Date().toISOString();save();}
console.log('KEYBOARD OWNERSHIP BROWSER PASS',out);
