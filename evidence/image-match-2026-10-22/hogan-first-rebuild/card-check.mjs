import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire('/workspace/node_modules/playwright/package.json');
const {chromium}=require('playwright');
const root='/workspace/chicago/site', out='/tmp/t2377-model/card-check';fs.mkdirSync(out,{recursive:true});
const types={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.glb':'model/gltf-binary'};
const server=http.createServer((req,res)=>{let p=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!p.startsWith(root+'/')){res.writeHead(403).end();return;}if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');if(!fs.existsSync(p)){res.writeHead(404).end();return;}res.setHeader('Content-Type',types[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader']});
const results=[];
try{
 for(const [label,width,height,touch] of [['mobile',390,780,true],['desktop',1280,800,false]]){
  if(process.env.QA_VIEWPORT&&process.env.QA_VIEWPORT!==label)continue;
  const context=await browser.newContext({viewport:{width,height},hasTouch:touch,deviceScaleFactor:1});
  try{
   const page=await context.newPage(), errors=[], network=[]; page.setDefaultTimeout(90_000); page.on('pageerror',e=>errors.push(e.message)); page.on('response',r=>{if(r.status()>=400)network.push({url:r.url(),status:r.status()});}); page.on('requestfailed',r=>network.push({url:r.url(),failure:r.failure()}));
   const response=await page.goto(`http://127.0.0.1:${server.address().port}/4d/walk/index.html?year=1835&keep-geometry=1`);assert.equal(response.status(),200);
   await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000,polling:1000});
   await page.evaluate(async()=>{const a=window.__chicago4d,deadline=Date.now()+90000;while(a.welcome?.state!=='world'&&Date.now()<deadline){if(a.welcome?.state==='welcome')a.welcome.enter('spawn');await new Promise(r=>setTimeout(r,100));}if(a.welcome&&a.welcome.state!=='world')throw Error('welcome did not enter world');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.frame('hogan_store');});
   await page.waitForTimeout(1500);
   const data=await page.evaluate(()=>{const a=window.__chicago4d,s=a.registry.get('hogan_store')?.sidecar;return {grade:s?.grade,attributes:s?.attributes,problems:a.problems??[],expectedReviews:[...a.registry.values()].filter(r=>r.sidecar?.review_required).map(r=>r.sidecar.id).sort(),scene:a.scene?.id};});
   assert.equal(data.grade?.value,'attested');assert(data.grade.pictures.includes('cameron_c1900_first_post_office'));
   for(const k of ['front_set_out','window_w_m','window_h_m','door_w_m','door_h_m','end_openings','chimney_ridge_at','ridge_stack_w_m'])assert.equal(data.attributes[k].confidence,'reconstructed',k);
   assert.deepEqual(data.attributes.front_set_out.value,[['door',8.45],['window',11.55]]);assert.deepEqual(data.attributes.chimney_ridge_at.value,[0.6]);
   fs.writeFileSync(path.join(out,`${label}-diagnostic.json`),JSON.stringify({data,errors,network},null,2)); const reviews=data.problems.filter(p=>/review_required is set/.test(p)); assert.deepEqual(reviews.map(p=>p.split(':',1)[0]).sort(),data.expectedReviews); const hard=data.problems.filter(p=>!/provisional|PLACEHOLDER|placeholder|review_required is set/i.test(p)); assert.deepEqual(hard,[]); assert.deepEqual(network,[]);
   await page.screenshot({path:path.join(out,`${label}-scene.png`)});
   await page.evaluate(async()=>{const a=window.__chicago4d;a.pick('hogan_store');await a.navigator.select('inspect');a.navigator.open(2);});
   await page.waitForFunction(()=>document.querySelector('#nav-app-inspect')?.dataset.structure==='hogan_store'&&!!document.querySelector('#nav-app-inspect [data-insp-tab="photos"]'),null,{timeout:30000,polling:250});
   await page.evaluate(()=>document.querySelector('#nav-app-inspect [data-insp-tab="photos"]').click());
   await page.waitForFunction(()=>document.querySelector('#nav-app-inspect [data-insp-pane="photos"]')?.dataset.filled==='yes',null,{timeout:30000,polling:250});
   await page.locator('#nav-app-inspect [data-insp-pane="photos"] details.ph-links summary').click();
   const photos=await page.evaluate(()=>{const p=document.querySelector('#nav-app-inspect [data-insp-pane="photos"]');return {text:p.innerText,links:[...p.querySelectorAll('a')].map(a=>a.href),visible:p.checkVisibility(),overflow:document.documentElement.scrollWidth>innerWidth};});
   assert.equal(photos.visible,true);assert.match(photos.text,/Cameron/i);assert(photos.links.some(h=>h.includes('commons.wikimedia.org')));assert.equal(photos.overflow,false);
   await page.screenshot({path:path.join(out,`${label}-photos.png`)});
   await page.locator('#nav-app-inspect [data-insp-tab="sources"]').click();
   await page.waitForFunction(()=>document.querySelector('#nav-app-inspect [data-insp-pane="sources"]')?.dataset.filled==='yes',null,{timeout:30000});
   await page.evaluate(()=>{const f=[...document.querySelectorAll('#nav-app-inspect [data-insp-pane="sources"] details.src-fact')].find(n=>n.textContent.includes('Cameron'));if(!f)throw Error('Cameron source fact missing');f.querySelector(':scope > summary').click();for(const n of f.querySelectorAll('details.src-cites > summary'))n.click();f.querySelector('ol.cites')?.scrollIntoView({block:'center'});});
   const sourceText=await page.locator('#nav-app-inspect [data-insp-pane="sources"]').innerText();fs.writeFileSync(path.join(out,`${label}-sources.txt`),sourceText); assert.match(sourceText,/Chicago Historical Society/i); assert.match(sourceText,/Cameron/i); await page.screenshot({path:path.join(out,`${label}-sources.png`)});
   assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
   results.push({viewport:label,width,height,page_errors:errors,loader_problems:hard,declared_review_records:data.expectedReviews,grade:data.grade,photos,source_credit:'Cameron and Chicago Historical Society verified in Sources',opening_and_station_assertions:'passed',screenshots:[`${label}-scene.png`,`${label}-photos.png`,`${label}-sources.png`]});
   fs.writeFileSync(path.join(out,`${label}-result.json`),JSON.stringify({status:'PASS',...results.at(-1)},null,2)+'\n');
   console.log(`${label}: Hogan rebuilt attributes, grade, credited photo link, viewport and page/loader errors passed`);
  }finally{await context.close();}
 }
 fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({status:'PASS',scope:'targeted Hogan app/card check; not the full renderer smoke',results:['mobile','desktop'].map(label=>JSON.parse(fs.readFileSync(path.join(out,`${label}-result.json`),'utf8')))},null,2)+'\n');
}finally{await browser.close();await new Promise(r=>server.close(r));}
