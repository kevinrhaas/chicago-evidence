import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/chicago/chicago/4d/tools/smoke_renderer.mjs');
const { chromium } = require('playwright');
const root = '/workspace/chicago/chicago/4d';
const out = '/tmp/notebook-fixture-smoke'; fs.mkdirSync(out, { recursive: true });
const fixture = `<!doctype html><html data-skin="control-room"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="/renderers/web/css/walk.css"><link rel="stylesheet" href="/renderers/web/css/navigator.css"><link rel="stylesheet" href="/renderers/web/css/drawer.css"><link rel="stylesheet" href="/renderers/web/css/skins.css"><link rel="stylesheet" href="/renderers/web/css/field-notebook.css"><link rel="stylesheet" href="/renderers/web/css/handout.css"><link rel="stylesheet" href="/renderers/web/css/inspect.css">
<style>html,body{overflow:auto;height:auto;min-height:100%;touch-action:auto}body{margin:0;background:var(--page);color:var(--ink);font:16px/1.4 var(--font-body);padding:12px;box-sizing:border-box}main{max-width:720px;margin:auto}h1{font-size:22px}button{font:inherit}a{color:var(--accent)}.nav-guide-sheet{display:none}</style><script type="importmap">{"imports":{"three":"/renderers/web/vendor/three-0.185.1/three.module.js","three/addons/":"/renderers/web/vendor/three-0.185.1/addons/"}}</script></head><body><main><h1>4D Chicago · Guide</h1><div id="guide-host" class="nav-screen"></div><div id="person"></div></main><script type="module">
import guide from '/renderers/web/js/apps/guide.js';
const host=document.getElementById('guide-host');
const ctx={scene:{id:'1835'},coarse:matchMedia('(pointer:coarse)').matches,actions:{guideFaq:async()=>({questions:[{q:'Is this real?',a:'Each record shows its sources.'}]}),jauntCatalog:async()=>[]}};
const screen=guide.load();screen.mount(host,ctx);screen.shown(host,ctx);window.fixture={screen,host,ctx};
</script></body></html>`;
const server=http.createServer((req,res)=>{let pathname=new URL(req.url,'http://localhost').pathname;if(pathname==='/'){res.writeHead(200,{'Content-Type':'text/html'});res.end(fixture);return;}let file=path.resolve(root,'.'+decodeURIComponent(pathname));if(!file.startsWith(root+'/')){res.writeHead(403);res.end();return;}try{fs.accessSync(file);res.writeHead(200,{'Content-Type':({'.js':'text/javascript','.css':'text/css','.json':'application/json','.woff2':'font/woff2'})[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const report={runs:[]};
try{
for(const width of [390,1280]){
 const ctx=await browser.newContext({viewport:{width,height:width<600?780:800},deviceScaleFactor:1,hasTouch:width<600,isMobile:width<600,acceptDownloads:true});
 await ctx.addInitScript(()=>{window.print=()=>{window.__printed=true;};});
 const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const row={width,checks:[],errors};report.runs.push(row);
 const check=async(name,fn)=>{try{await fn();row.checks.push({name,pass:true});}catch(e){row.checks.push({name,pass:false,error:String(e.stack||e)});}};
 await page.goto(origin);await page.locator('#field-notebook > summary').click();
 await check('Guide mount and save form',async()=>{
  await page.locator('#field-notebook form input').fill('At the river');await page.locator('#field-notebook form textarea').fill('I saw a bridge. <script>unsafe()</script>');await page.getByRole('button',{name:'Save note',exact:true}).click();
  assert.equal(await page.locator('.field-notebook-entry').count(),1);assert.equal(await page.locator('.field-notebook-entry h3').innerText(),'At the river');
  assert.match(await page.locator('.field-notebook-status').innerText(),/Saved/);assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('chicago4d.notebook.v1')).entries[0].year),'1835');
 });
 await check('edit and persistence after reload',async()=>{
  await page.locator('.field-notebook-entry textarea').fill('Revised note, still <script>not code</script>');await page.getByRole('button',{name:'Save changes',exact:true}).click();
  await page.reload();await page.locator('#field-notebook > summary').click();assert.equal(await page.locator('.field-notebook-entry textarea').inputValue(),'Revised note, still <script>not code</script>');
 });
 await check('person card saves source and grade',async()=>{
  await page.evaluate(async()=>{const {personModel,renderPersonCard}=await import('/renderers/web/js/person-card.js');const m=personModel({row:{id:'fixture-person',name:'Fixture Person'},person:{id:'fixture-person',name:'Fixture Person',grade:'inferred',note:'A fixture record for this UI test.',sources:['fixture-source']},sceneYear:1835,citations:{'fixture-source':{citation:'A test source',url:'https://example.org/source'}}});document.getElementById('person').append(renderPersonCard(document,m));});
  await page.locator('.insp-person-notebook').click();assert.equal(await page.locator('.field-notebook-entry').count(),2);const entries=await page.evaluate(()=>JSON.parse(localStorage.getItem('chicago4d.notebook.v1')).entries);assert.equal(entries[1].grade,'inferred');assert.equal(entries[1].sources[0].url,'https://example.org/source');
 });
 await check('download safe standalone HTML',async()=>{
  const [download]=await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download notebook',exact:true}).click()]);
  const file=path.join(out,`${width}-notebook.html`);await download.saveAs(file);const body=fs.readFileSync(file,'utf8');assert.match(body,/Revised note/);assert.match(body,/&lt;script&gt;/);assert.doesNotMatch(body,/<script>/);assert.match(body,/https:\/\/example.org\/source/);row.download=file;
 });
 await check('iframe print and cleanup',async()=>{
  await page.getByRole('button',{name:'Print / save PDF',exact:true}).click();await page.waitForFunction(()=>document.querySelector('.field-notebook-print-frame')?.contentWindow?.__printed===true);
  const content=await page.locator('.field-notebook-print-frame').evaluate(f=>f.contentDocument.body.innerText);assert.match(content,/Revised note/);assert.match(content,/A test source/);
  await page.locator('.field-notebook-print-frame').evaluate(f=>f.contentWindow.dispatchEvent(new Event('afterprint')));assert.equal(await page.locator('.field-notebook-print-frame').count(),0);
 });
 await check('blocked storage gives visible failure',async()=>{
  await page.evaluate(()=>{window.__setItem=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new Error('quota');};});
  await page.locator('#field-notebook form input').fill('Cannot save');await page.locator('#field-notebook form textarea').fill('Keep this draft');await page.getByRole('button',{name:'Save note',exact:true}).click();
  assert.match(await page.locator('.field-notebook-status').innerText(),/could not save/);assert.equal(await page.locator('#field-notebook form textarea').inputValue(),'Keep this draft');assert.equal(await page.locator('.field-notebook-entry').count(),2);await page.evaluate(()=>{Storage.prototype.setItem=window.__setItem;});
 });
 await page.locator('#field-notebook form input').fill('At the river');await page.locator('#field-notebook form textarea').fill('A source can tell me who built the bridge.');await page.getByRole('button',{name:'Save note',exact:true}).click();await page.locator('#field-notebook').evaluate(el=>el.scrollIntoView({block:'start'}));
 row.colors=await page.locator('#field-notebook form input').evaluate(el=>({color:getComputedStyle(el).color,background:getComputedStyle(el).backgroundColor}));
 row.overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:innerWidth}));
 await page.screenshot({path:path.join(out,`${width}-dark.png`),fullPage:false});
 await page.evaluate(()=>document.documentElement.dataset.theme='light');await page.screenshot({path:path.join(out,`${width}-light.png`),fullPage:false});
 row.screenshots=[`${width}-dark.png`,`${width}-light.png`];
 assert.equal(errors.length,0,errors.join('\n'));await ctx.close();
}
}finally{fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(JSON.stringify(report,null,2));
