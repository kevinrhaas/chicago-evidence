/** Native no-world completion fixture. Run only after the release renderer frees CPU. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';
const app=process.env.QA_APP||'/workspace/chicago-investigation/chicago/4d';
const web=path.join(app,'renderers/web'),out=process.env.QA_OUT||'/tmp/t3663-investigation-browser';
const jaunt=JSON.parse(fs.readFileSync(path.join(app,'data/sidecars/1835/jaunts/gossip-or-notice.json')));
const {chromium}=createRequire('/workspace/chicago/package.json')('playwright');
fs.mkdirSync(out,{recursive:true});const report={started:new Date().toISOString(),checks:[],errors:[],scope:'Native DOM completion/notebook/export fixture; no WebGL world. Not a published-town release gate.'};
const save=()=>fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
const check=(name,pass,detail='')=>{report.checks.push({name,pass:!!pass,detail});console.log(pass?'PASS':'FAIL',name,detail);save();assert(pass,name+': '+detail);};
const server=http.createServer((req,res)=>{const url=new URL(req.url,'http://local');if(url.pathname==='/'){res.writeHead(200,{'Content-Type':'text/html'});res.end('<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gossip comparison fixture</title><style>html{font:16px/1.5 system-ui;background:#182326;color:#edf0ec}body{margin:12px}main{max-width:42rem}button{font:inherit}button:focus-visible{outline:3px solid #ead09e}a{color:#ead09e}</style></head><body></body></html>');return;}if(url.pathname==='/favicon.ico'){res.writeHead(204).end();return;}const file=path.resolve(web,'.'+url.pathname);if(!file.startsWith(web+path.sep)){res.writeHead(403).end();return;}fs.readFile(file,(err,bytes)=>{res.writeHead(err?404:200,{'Content-Type':file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'application/octet-stream'});res.end(err?'':bytes);});});
await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||'/usr/bin/chromium',args:['--no-sandbox']});
 for(const viewport of [{width:390,height:780},{width:1280,height:800}]){
  const context=await browser.newContext({viewport,isMobile:viewport.width===390,hasTouch:viewport.width===390});
  const page=await context.newPage();const tag=String(viewport.width);page.setDefaultTimeout(10000);
  page.on('pageerror',e=>{report.errors.push({width:viewport.width,text:String(e)});save();});
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  await page.evaluate(async jaunt=>{
   const {createJauntPreview}=await import('/js/jaunt-preview.js');
   const {fieldNotebook}=await import('/js/field-notebook.js');
   const {notebookHTML}=await import('/js/field-notebook-view.js');
   window.notebook=fieldNotebook;window.exportNotebook=()=>notebookHTML(fieldNotebook.read().entries);
   const root=document.createElement('main');document.body.append(root);
   window.fixtureJaunt=jaunt;window.fixtureSession={session:'case-one',jaunt,phase:'outcome',outcome:jaunt.endings.find(e=>e.completion_eligible),visited:jaunt.stops.map(s=>({id:s.id,committed:true}))};
   window.preview=createJauntPreview({root,api:{},dataBase:new URL('/data/',location.href),destinations:{},
    getSession:()=>fixtureSession,onDismiss:()=>{window.fixtureSession=null;},
    onStart:()=>{window.fixtureSession={...fixtureSession,session:'replay',phase:'atStop'};},
    fetcher:async url=>String(url).endsWith('catalog.json')?{ok:true,json:async()=>({scene:'1835',jaunts:[]})}:{ok:false,status:404}});
   await preview.open();
  },jaunt);
  const box=page.locator('.jaunt-investigation'),summary=box.locator('summary');
  check(tag+' eligible completion is collapsed',await box.count()===1&&await box.getAttribute('open')===null);
  check(tag+' general reflection remains',await page.locator('.jaunt-understanding').count()===1);
  await summary.focus();await page.keyboard.press('Enter');
  check(tag+' native summary opens',await box.getAttribute('open')!==null);
  await page.keyboard.press('Tab');
  check(tag+' keyboard reaches first evidence checkbox',await page.evaluate(()=>document.activeElement.type==='checkbox'&&document.activeElement.value==='land-sale'));
  check(tag+' focused checkbox is visibly outlined',await page.evaluate(()=>getComputedStyle(document.activeElement).outlineStyle==='solid'));
  await page.keyboard.press('Space');await page.keyboard.press('Tab');await page.keyboard.press('Space');
  check(tag+' native Space chooses source support',await box.locator('input:checked').count()===2);
  await page.keyboard.press('Tab');await page.keyboard.press('Tab');
  check(tag+' keyboard reaches labelled claim',await page.evaluate(()=>document.activeElement.dataset.investigationField==='claim'));
  await page.keyboard.type('<script>my claim</script>: the bank was proposed.');
  await page.keyboard.press('Tab');await page.keyboard.type('The exact sale total is still missing.');
  check(tag+' draft is not persisted',await page.evaluate(()=>localStorage.getItem('chicago4d.notebook.v1')===null));
  await page.keyboard.press('Tab');await page.keyboard.press('Enter');
  check(tag+' ungraded review opens with status',await box.locator('.jaunt-investigation-review').isVisible()&&(await box.getByRole('status').innerText()).includes('ungraded'));
  await box.getByRole('button',{name:'Revise my claim',exact:true}).focus();await page.keyboard.press('Enter');
  check(tag+' revise restores claim focus',await page.evaluate(()=>document.activeElement.dataset.investigationField==='claim'));
  const content=await box.innerText();check(tag+' original uncertainty and inference visible',content.includes('Fi[v]e and […]red')&&content.includes('Inferred:')&&content.includes('108')&&!content.includes('[Six Hund]red'));
  check(tag+' text-only citations have no invented links',await box.locator('a').count()===0);
  await box.getByRole('button',{name:'Save to notebook',exact:true}).focus();await page.keyboard.press('Space');
  check(tag+' native save announces success', (await box.getByRole('status').innerText()).startsWith('Saved to your notebook')&&await page.evaluate(()=>notebook.read().entries.length===1));
  await page.keyboard.press('Space');check(tag+' repeated save is explicit and unique',(await box.getByRole('status').innerText()).includes('already')&&await page.evaluate(()=>notebook.read().entries.length===1));
  await page.evaluate(()=>preview.open());check(tag+' same-session repaint retains draft',await box.getByLabel('My claim',{exact:true}).inputValue()==='<script>my claim</script>: the bank was proposed.'&&await box.locator('input:checked').count()===2);
  await box.getByLabel('My claim',{exact:true}).fill('A revised claim');
  await page.evaluate(()=>{window.originalSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key==='chicago4d.notebook.v1')throw Error('quota');return originalSetItem.call(this,key,value);};});
  await box.getByRole('button',{name:'Save a revised copy',exact:true}).click();
  check(tag+' refused storage retains draft and earlier entry',(await box.getByRole('status').innerText()).includes('could not save')&&await box.getByLabel('My claim',{exact:true}).inputValue()==='A revised claim'&&await page.evaluate(()=>notebook.read().entries.length===1));
  await page.evaluate(()=>{Storage.prototype.setItem=originalSetItem;});
  await box.getByRole('button',{name:'Save a revised copy',exact:true}).click();
  check(tag+' revised copy saves explicitly',await page.evaluate(()=>notebook.read().entries.length===2));
  await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});
  check(tag+' comparison reads at 200 percent text without horizontal clipping',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(out,tag+'-comparison-200pct.png'),fullPage:true});
  await page.emulateMedia({media:'print'});const exported=await page.evaluate(()=>exportNotebook());
  fs.writeFileSync(path.join(out,tag+'-notebook.html'),exported);
  check(tag+' export escapes student text and retains two citations',exported.includes('&lt;script&gt;my claim&lt;/script&gt;')&&exported.includes('Fi[v]e and […]red')&&exported.includes('Springfield')&&exported.includes('Chicago Democrat')&&exported.includes('Chicago American'));
  // Inspect the existing export in the same tab, then return without another live world.
  await page.emulateMedia({media:'screen'});
  await box.getByRole('button',{name:'Close this comparison',exact:true}).click();
  check(tag+' close returns focus to summary',await box.getAttribute('open')===null&&await page.evaluate(()=>document.activeElement.tagName==='SUMMARY'));
  await page.getByRole('button',{name:'Restart Jaunt',exact:true}).click();await page.evaluate(()=>preview.open());
  check(tag+' replay removes comparison',await box.count()===0);
  await page.evaluate(()=>{fixtureSession={...fixtureSession,phase:'outcome',outcome:fixtureJaunt.endings.find(e=>e.completion_eligible)};return preview.open();});
  await box.locator('summary').click();check(tag+' new session starts with empty draft',await box.getByLabel('My claim',{exact:true}).inputValue()===''&&await box.locator('input:checked').count()===0);
  await page.getByRole('button',{name:'Close the finished outing',exact:true}).click();check(tag+' dismissal removes comparison',await box.count()===0);
  await page.setContent(exported);await page.emulateMedia({media:'print'});await page.pdf({path:path.join(out,tag+'-notebook.pdf'),format:'A4',printBackground:true});
  check(tag+' notebook export prints without hidden source text',await page.locator('body').innerText().then(text=>text.includes('Fi[v]e and […]red')&&text.includes('Inferred')&&text.includes('The exact sale total')));
  await context.close();
 }
 check('zero page errors',report.errors.length===0,JSON.stringify(report.errors));report.pass=true;
}catch(e){report.pass=false;report.error=String(e.stack||e);save();throw e;}finally{await browser?.close();await new Promise(r=>server.close(r));report.finished=new Date().toISOString();save();}
console.log('NATIVE INVESTIGATION PASS',out);
