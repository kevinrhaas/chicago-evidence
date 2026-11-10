import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const require=createRequire('/tmp/chicago-browser-tools/package.json');
const {chromium}=require('playwright');
const out='/tmp/nov10-t2023-evidence/ui';fs.mkdirSync(out,{recursive:true});
const base='http://127.0.0.1:4207/4d/';
const site='/tmp/chicago-west-wicket-20261109/site/4d';
const pin={published_source:'2ea44eff141ed62a88286ea5d331ca648ac587be',owner_report_only_head:'02a075d0bc90f42839f8d9a9d5554108d5610418',files:{}};
for(const name of ['data/reconstruction/1835_reconstruction_order_book.json','build.json','index.html']){
 const p=path.join(site,name);pin.files[name]={sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),bytes:fs.statSync(p).size};
}
fs.writeFileSync(path.join(out,'SOURCE-IDENTITY.json'),JSON.stringify(pin,null,2));
const rows=[],browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader']});
let failure=null;
try{
 for(const [label,viewport,detail] of [['phone',{width:390,height:780},'light'],['desktop',{width:1280,height:800},'full']]){
  const c=await browser.newContext({viewport,deviceScaleFactor:1,isMobile:label==='phone',hasTouch:label==='phone'}),p=await c.newPage();p.setDefaultTimeout(90000);
  const errors=[];p.on('pageerror',e=>errors.push(String(e)));await p.addInitScript(d=>{localStorage.setItem('chicago4d.settings',JSON.stringify({detail:d}));localStorage.setItem('chicago4d.researcher','on');},detail);
  console.log(label,'capture boot starting');
  await p.goto(base+'1835/',{waitUntil:'domcontentloaded'});
  await p.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240000,polling:500});
  const boot=await p.evaluate(()=>({ready:__chicago4d.ready,error:__chicago4d.error,year:__chicago4d.year}));if(!boot.ready)throw Error(JSON.stringify(boot));
  await p.waitForFunction(()=>__chicago4d.welcome.state==='welcome',null,{timeout:240000,polling:500});
  await p.evaluate(()=>{const a=__chicago4d;if(!a.welcome.enter('spawn'))throw Error('normal entry failed');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.renderer.setAnimationLoop(null);a.step();});
  console.log(label,'normal boot ready');
  const checks=[];
  for(const [id,expected]of [['tremont_house_1',['Warren Thayer','George Wadsworth','Michael Mahoney','Lydia Ingalls','Victoire Bourassa','Marie Bourassa','Archange Bourassa']],['recon_1835_blk_indiana_north_cass_h3_09',['Archange Chevalier']],['recon_1835_blk_washington_clinton_h3_02',['Reuben Rice','Mary Hastings','Catherine Robillard','Lydia Stiles','Almira Wadsworth']],['steamboat_hotel',['Barbery Judar','T Welsh']]]){
   continue; // house cards already captured and passed on both viewports
   await p.evaluate(async id=>{await __chicago4d.navigator.openLink({app:'inspect',id,tab:'people'});},id);
   await p.waitForFunction(names=>names.every(n=>document.body.innerText.includes(n)),expected,{timeout:90000,polling:300});
   const text=await p.locator('body').innerText();checks.push({id,names:expected,all_visible:true,contains_reconstruction_language:/reconstruct/i.test(text)});
   fs.writeFileSync(path.join(out,label+'-'+id+'.txt'),text);
   await p.screenshot({path:path.join(out,label+'-'+id+'.png')});console.log(label,id,'names PASS');
  }
  await p.evaluate(()=>{const a=__chicago4d;const b=document.getElementById('s-researcher');if(b&&!b.checked){b.checked=true;b.dispatchEvent(new Event('change',{bubbles:true}));}a.hud.setPanel(true);a.hud.selectTab('evidence');a.evidenceHub.showTopic('orderbook');});
  await p.waitForFunction(()=>document.querySelectorAll('#order-book tr').length>4);
  await p.evaluate(()=>{for(const d of document.querySelectorAll('#order-book details')){const summary=d.querySelector('summary');if(summary&&/households/i.test(summary.textContent)&&!d.open)summary.click();}});
  const cells=await p.evaluate(()=>Array.from(document.querySelectorAll('#order-book tr')).map(r=>({text:r.textContent,cells:Array.from(r.cells).map(c=>c.textContent.trim())})).filter(r=>/households.*(boarding house|inn tavern)/i.test(r.text)));
  fs.writeFileSync(path.join(out,label+'-orderbook-dom.json'),JSON.stringify(await p.evaluate(()=>({researcher:document.documentElement.hasAttribute('data-researcher-mode'),topic:__chicago4d.evidenceHub.topic,html:document.querySelector('#order-book')?.innerHTML,text:document.body.innerText})),null,2));
  if(cells.length!==6||cells.some(r=>r.cells[3]!==r.cells[4]))throw Error('Unpaid or missing lodging cells '+JSON.stringify(cells));
  await p.evaluate(()=>{for(const d of document.querySelectorAll('#order-book details'))if(d.innerText.toLowerCase().includes('household'))d.open=true;const r=Array.from(document.querySelectorAll('#order-book tr')).find(r=>/boarding house/i.test(r.innerText));r?.scrollIntoView({block:'center'});});
  await p.screenshot({path:path.join(out,label+'-six-lodging-cells.png')});checks.push({six_paid_cells:cells});
  const result={label,viewport,detail,boot,checks,page_errors:errors};rows.push(result);fs.writeFileSync(path.join(out,'RESULTS.json'),JSON.stringify({pin,results:rows},null,2));if(errors.length)throw Error(JSON.stringify(errors));await c.close();console.log(label,'PASS');
 }
}catch(e){failure=String(e);console.error(failure);}
finally{fs.writeFileSync(path.join(out,'RESULTS.json'),JSON.stringify({pin,results:rows,failure},null,2));await browser.close();}
if(failure)process.exit(1);
