import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/chicago/chicago/4d/tools/smoke_renderer.mjs');
const { chromium } = require('playwright');
const root = '/workspace/chicago/chicago/4d';
const out = '/tmp/lesson-fixture-smoke'; fs.mkdirSync(out, { recursive: true });
const fixture = `<!doctype html><html data-skin="control-room"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="/renderers/web/css/walk.css"><link rel="stylesheet" href="/renderers/web/css/navigator.css"><link rel="stylesheet" href="/renderers/web/css/drawer.css"><link rel="stylesheet" href="/renderers/web/css/skins.css"><link rel="stylesheet" href="/renderers/web/css/handout.css"><link rel="stylesheet" href="/renderers/web/css/inspect.css">
<style>html,body{overflow:auto;height:auto;min-height:100%;touch-action:auto}body{margin:0;background:var(--page);color:var(--ink);font:16px/1.4 var(--font-body);padding:12px;box-sizing:border-box}main{max-width:720px;margin:auto}h1{font-size:22px}button{font:inherit}a{color:var(--accent)}</style><script type="importmap">{"imports":{"three":"/renderers/web/vendor/three-0.185.1/three.module.js","three/addons/":"/renderers/web/vendor/three-0.185.1/addons/"}}</script></head><body><main><h1>4D Chicago · Guide</h1><div id="guide-host" class="nav-screen"></div></main><script type="module">
import guide from '/renderers/web/js/apps/guide.js';
const host=document.getElementById('guide-host');
const ctx={scene:{id:'1835'},coarse:matchMedia('(pointer:coarse)').matches,actions:{guideFaq:async()=>({questions:[]}),jauntCatalog:async y=>{const r=await fetch('/data/sidecars/'+y+'/jaunts/catalog.json');return (await r.json()).jaunts;},jauntDocument:async(y,id)=>{if(window.fixture.holdNext){window.fixture.holdNext=false;await new Promise(r=>window.fixture.release=r);}const r=await fetch('/data/sidecars/'+y+'/jaunts/'+id+'.json');if(!r.ok)throw Error('unavailable');return r.json();}}};
const screen=guide.load();screen.mount(host,ctx);screen.shown(host,ctx);window.fixture={screen,host,ctx};
</script></body></html>`;
const server=http.createServer((req,res)=>{let pathname=new URL(req.url,'http://localhost').pathname;if(pathname==='/'){res.writeHead(200,{'Content-Type':'text/html'});res.end(fixture);return;}let file=path.resolve(root,'.'+decodeURIComponent(pathname));if(!file.startsWith(root+'/')){res.writeHead(403);res.end();return;}try{fs.accessSync(file);res.writeHead(200,{'Content-Type':({'.js':'text/javascript','.css':'text/css','.json':'application/json','.woff2':'font/woff2'})[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
const report={runs:[]};
try{
for(const width of [390,1280]){
 const ctx=await browser.newContext({viewport:{width,height:width<600?780:800},deviceScaleFactor:1,hasTouch:width<600,isMobile:width<600});
 await ctx.addInitScript(()=>{window.print=()=>{window.__printed=true;};});
 const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const row={width,checks:[],errors};report.runs.push(row);
 const check=async(name,fn)=>{try{await fn();row.checks.push({name,pass:true});console.log(width,'PASS',name);}catch(e){row.checks.push({name,pass:false,error:String(e.stack||e)});console.log(width,'FAIL',name,e.message);}};
 await page.goto(origin);await page.getByRole('button',{name:'Choose a lesson guide',exact:true}).click();
 const sel=key=>page.locator('[data-lesson-select="'+key+'"]');
 await check('integrated Guide controls and all available groups',async()=>{
  const groups=[];
  for(const year of ['1812','1835','1904']){
   await sel('year').selectOption(year);await sel('grade').selectOption('9-10');
   const names=await sel('group').locator('option').evaluateAll(es=>es.map(e=>e.value));
   for(const group of names){await sel('group').selectOption(group);await page.getByRole('button',{name:'Prepare lesson',exact:true}).click();await page.locator('.lesson-guide').waitFor();assert.equal(await page.locator('.lesson-guide').getAttribute('data-lesson'),year+':'+group+':9-10');assert(await page.locator('.lesson-document').count()>=2);groups.push(year+':'+group);}
  }
  assert.equal(groups.length,10);row.groups=groups;
 });
 await check('grade choice and stale request ignored',async()=>{
  await sel('year').selectOption('1835');await sel('group').selectOption('Places');await sel('grade').selectOption('9-10');
  await page.evaluate(()=>fixture.holdNext=true);await page.getByRole('button',{name:'Prepare lesson',exact:true}).click();await page.waitForFunction(()=>!!fixture.release);
  await sel('grade').selectOption('11-12');await page.getByRole('button',{name:'Prepare lesson',exact:true}).click();await page.locator('.lesson-guide').waitFor();
  assert.equal(await page.locator('.lesson-guide').getAttribute('data-lesson'),'1835:Places:11-12');
  await page.evaluate(()=>fixture.release());await page.waitForTimeout(150);
  assert.equal(await page.locator('.lesson-guide').getAttribute('data-lesson'),'1835:Places:11-12');
 });
 await check('source links, labels and printable PDF',async()=>{
  const links=await page.locator('.lesson-source-links a').evaluateAll(es=>es.map(a=>({href:a.href,rel:a.rel,target:a.target})));
  assert(links.length>0);assert(links.every(a=>/^https?:/.test(a.href)&&a.rel.includes('noopener')&&a.target==='_blank'));row.sourceLinks=links;
  assert.match(await page.locator('.lesson-guide').innerText(),/not a quotation from the original document/);
  await page.getByRole('button',{name:'Print or save as PDF',exact:true}).click();await page.waitForFunction(()=>document.querySelector('#lesson-print'));
  assert.equal(await page.locator('#lesson-print .lesson-guide').count(),1);
  const file=path.join(out,width+'-lesson.pdf');await page.pdf({path:file,format:'Letter',printBackground:true});row.pdf=file;
  await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));assert.equal(await page.locator('#lesson-print').count(),0);
 });
 await check('no overflow and readable dark/light controls',async()=>{
  await page.locator('.lesson-guide').evaluate(e=>e.scrollIntoView({block:'start'}));
  row.overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:innerWidth}));assert(row.overflow.scroll<=row.overflow.width);
  row.colors=await sel('year').evaluate(el=>({color:getComputedStyle(el).color,background:getComputedStyle(el).backgroundColor}));assert.notEqual(row.colors.color,row.colors.background);
  await page.screenshot({path:path.join(out,width+'-dark.png'),fullPage:false});
  await page.evaluate(()=>document.documentElement.dataset.theme='light');await page.screenshot({path:path.join(out,width+'-light.png'),fullPage:false});
 });
 await check('zero page errors',async()=>assert.equal(errors.length,0,errors.join('\n')));await ctx.close();
}
}finally{fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));await browser.close();server.close();}
if(report.runs.some(r=>r.checks.some(c=>!c.pass)))process.exitCode=1;
