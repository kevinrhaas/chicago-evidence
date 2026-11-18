import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const { chromium } = createRequire('/workspace/chicago/package.json')('playwright');
const app = '/workspace/chicago-rail/chicago/4d';
const web = path.join(app, 'renderers/web');
const out = '/tmp/t3658-rail-keyboard';
fs.mkdirSync(out, { recursive: true });
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const index = fs.readFileSync(path.join(web, 'index.html'), 'utf8');
const start = index.indexOf('<section id="navigator"');
assert(start >= 0);
const end = index.indexOf('\n</section>', start) + '\n</section>'.length;
const navigatorMarkup = index.slice(start, end);
const fixtureJS = `
import { createNavigator } from '/js/navigator.js';
import jump from '/js/apps/jump.js';
let conditional = true;
const mount = (name) => (el) => {
  const h=document.createElement('h2'); h.textContent=name;
  const p=document.createElement('p'); p.textContent='Keyboard fixture: no town or world assets are loaded.';
  const b=document.createElement('button'); b.type='button'; b.id='fixture-'+name.toLowerCase(); b.textContent=name+' control';
  el.append(h,p,b);
};
const apps=[
  {id:'home', label:'Home', order:0, panel:'nav-home'},
  {id:'map', label:'Map', order:20, mount:mount('Map')},
  {id:'inspect', label:'Inspect', order:30, when:c=>c.conditional, mount:mount('Inspect')},
  {id:'settings', label:'Settings', order:100, pin:'bottom', mount:mount('Settings')},
  {...jump, load:undefined, mount:mount('Jump')},
  {id:'move', label:'Move', order:60, inRail:false, mount:mount('Move')},
];
const nav=createNavigator({root:document.getElementById('navigator'), apps,
  scene:{id:'1835',target_date:'1835-07-01',lighting:{local_time:'10:30'}},
  context:()=>({conditional}), storage:null,
});
// The same listener as main.js:4135; only the fixture's year chip supplies its DOM.
document.getElementById('year-badge').addEventListener('click',()=>void nav.select('jump'));
window.qa={nav, async conditional(value){conditional=value; await new Promise(r=>setTimeout(r,270)); nav.update();},
  unregister(id){return nav.unregister(id);},
  snapshot(){
    const tabs=[...document.querySelectorAll('.nav-tabs [role=tab]')].map(b=>({id:b.dataset.app,hidden:b.hidden,tabIndex:b.tabIndex,
      selected:b.getAttribute('aria-selected'),visible:b.getClientRects().length>0&&getComputedStyle(b).visibility!=='hidden'}));
    const el=document.activeElement, css=el?getComputedStyle(el):null;
    return {app:nav.app,level:nav.level,detent:nav.detent,tabs,focus:el?.id??null,
      focusVisible:!!el&&el.matches(':focus-visible')&&css.outlineStyle!=='none'&&parseFloat(css.outlineWidth)>0,
      canvases:document.querySelectorAll('canvas').length};
  }
};
window.fixtureReady=true;
`;
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Navigator keyboard fixture</title><link rel="icon" href="data:,">
<link rel="stylesheet" href="/css/navigator.css">
<style>
:root{--ink:#f7f2df;--ink-dim:#d9d0b5;--ink-faint:#b4aa8c;--panel:#242620;--panel-solid:#242620;--edge:#858068;--edge-strong:#aea387;--accent:#ffcf69;--signal:#ff7979;--font-body:system-ui,sans-serif;--font-mono:ui-monospace,monospace;--ease-detent:ease;--shadow:0 8px 20px #0007}
*{box-sizing:border-box}body{margin:0;background:#111811;color:var(--ink);font:15px system-ui,sans-serif;min-height:100vh}
[hidden]{display:none!important}button{font:inherit;color:inherit;background:#30392d;border:1px solid #858068;padding:8px;min-height:36px;cursor:pointer}
button:focus-visible{outline:3px solid #ffcf69;outline-offset:2px}.fixture-header{padding:18px;max-width:470px;margin-left:auto}.fixture-header h1{font-size:20px;margin:0 0 12px}.fixture-header p{font-size:13px;line-height:1.4;color:#dedacb}.fixture-after{position:fixed;right:12px;bottom:12px}
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.nav-screen h2{font-size:19px}.nav-screen p{font-size:13px;line-height:1.4}.nav-screen>button{display:block;margin:12px 0}
</style></head><body><header class="fixture-header"><h1>Navigator keyboard fixture</h1><p>Actual Navigator markup, styles and modules. Small app bodies; no world, WebGL or remote assets.</p><button id="before">Before Navigator</button><span id="year-badge"><button class="badge-year" id="year-chip">1835 · Other years</button></span></header>
${navigatorMarkup}<button class="fixture-after" id="after">After Navigator</button><script type="module" src="/fixture.js"></script></body></html>`;
fs.writeFileSync(path.join(out, 'fixture.html'), html);
fs.writeFileSync(path.join(out, 'fixture.js'), fixtureJS);
const report = {started:new Date().toISOString(),app,sourceCommit:execFileSync('git',['rev-parse','HEAD'],{cwd:app,encoding:'utf8'}).trim(),
  workingDiff:execFileSync('git',['diff','--stat'],{cwd:app,encoding:'utf8'}).trim(), sourceHashes:{}, requests:[],runs:[],
  scope:'DOM-only native keyboard fixture using real createNavigator/createRail and Navigator markup/CSS; no world, WebGL or external assets.',
  limits:['Fixture bodies replace business logic of apps; no whole-app conformance claim.','Chromium emulated viewport, not a physical phone or assistive-technology certification.','Year chip reproduces the production navigator.select(jump) listener; Home Move uses the real Navigator handler.']};
for(const relative of ['js/nav-rail.js','js/navigator.js','js/apps/jump.js','css/navigator.css'])report.sourceHashes[relative]=hash(fs.readFileSync(path.join(web,relative)));
report.harness={path:fileURLToPath(import.meta.url),sha256:hash(fs.readFileSync(fileURLToPath(import.meta.url)))};
const save=()=>fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
const server=http.createServer((req,res)=>{
  const pathname=new URL(req.url,'http://local').pathname;
  report.requests.push(pathname);
  if(pathname==='/'){res.setHeader('Content-Type','text/html');res.end(html);return;}
  if(pathname==='/fixture.js'){res.setHeader('Content-Type','text/javascript');res.end(fixtureJS);return;}
  if(!(/^\/js\/[a-zA-Z0-9_/-]+\.js$/.test(pathname)||pathname==='/css/navigator.css')){res.statusCode=403;res.end('Fixture forbids this resource');return;}
  const file=path.resolve(web,'.'+pathname);
  if(!file.startsWith(web+path.sep)||!fs.existsSync(file)){res.statusCode=404;res.end();return;}
  res.setHeader('Content-Type',pathname.endsWith('.css')?'text/css':'text/javascript');res.setHeader('Cache-Control','no-store');res.end(fs.readFileSync(file));
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin='http://127.0.0.1:'+server.address().port;report.origin=origin;
let browser;
try{
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-gpu','--disable-webgl']});
  for(const width of [390,1280])for(const motion of ['reduce','no-preference']){
    const height=width===390?780:800;
    const row={width,height,reducedMotion:motion,checks:[],errors:[],blockedRequests:[],httpErrors:[]};report.runs.push(row);save();
    const context=await browser.newContext({viewport:{width,height},reducedMotion:motion});
    const page=await context.newPage();page.setDefaultTimeout(10000);
    page.on('pageerror',e=>row.errors.push(String(e)));
    page.on('response',res=>{if(res.status()>=400)row.httpErrors.push({url:res.url(),status:res.status()});});
    await page.route('**/*',route=>{if(!route.request().url().startsWith(origin+'/')){row.blockedRequests.push(route.request().url());return route.abort();}return route.continue();});
    const snap=()=>page.evaluate(()=>qa.snapshot());
    const check=async(label,fn)=>{try{const details=await fn();row.checks.push({label,pass:true,details});console.log(width,motion,'PASS',label);save();return details;}catch(e){row.checks.push({label,pass:false,error:String(e.stack||e),snapshot:await snap().catch(()=>null)});save();throw e;}};
    const pressUntil=async(selector,{reverse=false,max=36}={})=>{
      const steps=[];
      for(let i=0;i<max;i++){
        await page.keyboard.press(reverse?'Shift+Tab':'Tab');
        const state=await page.evaluate(sel=>({id:document.activeElement?.id,match:document.activeElement?.matches(sel)}),selector);steps.push(state.id);
        if(state.match)return steps;
      }
      throw Error('Tab traversal never reached '+selector+': '+steps.join(' -> '));
    };
    const oneStop=s=>{
      const visible=s.tabs.filter(t=>t.visible&&!t.hidden);
      assert.equal(visible.filter(t=>t.tabIndex===0).length,1,JSON.stringify(s.tabs));
      assert(s.tabs.filter(t=>t.hidden).every(t=>t.tabIndex===-1),'hidden tabs are not Tab stops');
      assert.equal(s.canvases,0);
    };
    const railSelector='.nav-tabs [role="tab"]:not([hidden])';
    try{
      await page.goto(origin,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.fixtureReady);
      await check('N opens Home with visible keyboard focus',async()=>{await page.keyboard.press('n');await page.waitForTimeout(320);const s=await snap();assert.equal(s.app,'home');assert(s.level>0);assert.equal(s.focus,'nav-home');assert(s.focusVisible);oneStop(s);return s;});
      await check('Home Move opens by Tab and Enter, preserving one truthful visible rail stop',async()=>{const keys=await pressUntil('#nav-tile-move');await page.keyboard.press('Enter');await page.waitForFunction(()=>qa.nav.app==='move');const s=await snap();assert.equal(s.focus,'nav-app-move');oneStop(s);assert(s.tabs.filter(t=>!t.hidden).every(t=>t.selected==='false'));assert.equal(s.tabs.find(t=>t.id==='move').selected,'true');return {keys,state:s};});
      await check('Shift+Tab reaches rail; arrows move focus manually; Enter activates',async()=>{const keys=await pressUntil(railSelector,{reverse:true});let s=await snap();assert(s.focusVisible);const before=s.app;await page.keyboard.press('ArrowDown');s=await snap();assert.equal(s.app,before);assert.equal(s.focus,'nav-tab-map');await page.keyboard.press('Enter');await page.waitForFunction(()=>qa.nav.app==='map');s=await snap();assert.equal(s.focus,'nav-app-map');oneStop(s);return {keys,state:s};});
      await check('Escape returns visible focus to handle; N reopens current app',async()=>{await page.keyboard.press('Escape');await page.waitForTimeout(320);let s=await snap();assert.equal(s.level,0);assert.equal(s.focus,width===390?'nav-grip':'nav-collapse');assert(s.focusVisible);await page.keyboard.press('n');await page.waitForTimeout(320);s=await snap();assert.equal(s.app,'map');assert.equal(s.focus,'nav-app-map');oneStop(s);return s;});
      await check('Year chip opens Jump by keyboard and native Tab reaches a visible rail tab',async()=>{await page.keyboard.press('Escape');await page.waitForTimeout(320);const before=await pressUntil('#year-chip',{reverse:true});await page.keyboard.press('Enter');await page.waitForFunction(()=>qa.nav.app==='jump');await page.waitForTimeout(320);const opened=await snap();assert.equal(opened.focus,'year-chip');oneStop(opened);assert(opened.tabs.filter(t=>!t.hidden).every(t=>t.selected==='false'));assert.equal(opened.tabs.find(t=>t.id==='jump').selected,'true');const after=await pressUntil(railSelector);const s=await snap();assert(s.focusVisible);await page.screenshot({path:path.join(out,width+'-'+motion+'-jump-rail.png')});return {before,after,opened,state:s};});
      await check('Home and End move rail focus without activating Jump; Enter returns Home',async()=>{await page.keyboard.press('End');let s=await snap();assert.equal(s.app,'jump');assert.equal(s.focus,'nav-tab-settings');await page.keyboard.press('Home');s=await snap();assert.equal(s.app,'jump');assert.equal(s.focus,'nav-tab-home');await page.keyboard.press('Enter');await page.waitForFunction(()=>qa.nav.app==='home');s=await snap();oneStop(s);assert.equal(s.focus,'nav-home');return s;});
      await check('Conditional selected tab disappearing restores a surviving visible rail stop',async()=>{await pressUntil(railSelector,{reverse:true});await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');await page.keyboard.press('ArrowDown');assert.equal((await snap()).focus,'nav-tab-inspect');await page.keyboard.press('Enter');await page.waitForFunction(()=>qa.nav.app==='inspect');await page.evaluate(()=>qa.conditional(false));await page.waitForTimeout(380);const s=await snap();assert.equal(s.app,'home');oneStop(s);assert.equal(s.tabs.find(t=>t.id==='inspect').hidden,true);return s;});
      await check('Unregistering current rail app leaves rail reachable with native Tab',async()=>{await page.evaluate(()=>qa.nav.select('map'));await page.evaluate(()=>qa.unregister('map'));const s=await snap();oneStop(s);assert(!s.tabs.some(t=>t.id==='map'));const keys=await pressUntil(railSelector);const reached=await snap();assert(reached.focusVisible);return {keys,state:reached};});
      await check('No page errors, forbidden requests or world canvas',async()=>{assert.deepEqual(row.errors,[]);assert.deepEqual(row.blockedRequests,[]);assert.deepEqual(row.httpErrors,[]);assert.equal((await snap()).canvases,0);return {errors:row.errors,canvases:0};});
    }finally{await context.close();save();}
  }
  report.pass=true;
}catch(error){report.pass=false;report.error=String(error.stack||error);throw error;}
finally{await browser?.close();await new Promise(resolve=>server.close(resolve));report.finished=new Date().toISOString();save();}
console.log('RAIL KEYBOARD PASS',out);
