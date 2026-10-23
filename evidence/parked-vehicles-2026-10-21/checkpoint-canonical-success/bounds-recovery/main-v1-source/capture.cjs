// Main harness/server/identity/screenshot path adapted from parked-scene-capture-2026-10-21.cjs.
// PREPARED ONLY: requires explicit final source/index pins and a free browser lane.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),crypto=require('node:crypto');
const{execFileSync,spawnSync}=require('node:child_process');
const{chromium}=require('/workspace/shared/chicago-browser/node_modules/playwright');
const install=require('./browser-control.cjs'),cfg=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const root='/workspace/chicago',out=path.resolve(cfg.output),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
if(!out.startsWith('/workspace/shared/')||!/[a-f0-9]{40}/.test(cfg.expectedHead||'')||!/[a-f0-9]{64}/.test(cfg.expectedIndexDigest||''))throw Error('Outside output and explicit exact HEAD/index pins required');
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',maxBuffer:8*1024*1024}).trim();
const indexDigest=()=>sha(execFileSync('git',['ls-files','--stage'],{cwd:root,maxBuffer:8*1024*1024}));
const noUnstaged=()=>spawnSync('git',['diff','--quiet'],{cwd:root}).status===0;
const initialHead=git('rev-parse','HEAD'),initialIndex=indexDigest();
if(initialHead!==cfg.expectedHead||initialIndex!==cfg.expectedIndexDigest||!noUnstaged())throw Error('Exact source/index guard failed before creating a browser');
fs.mkdirSync(out,{recursive:false});
const common=['js/main.js','js/yard.js','js/parked-transport.js','js/buildings.js','js/confidence.js','js/terrain.js','js/walker.js','js/angles.js'];
const data=['transport/parked/placements.json','yard/town_trade_goods.json','terrain/epochs/e1834_harbor_cut/heightfield.json','terrain/epochs/e1834_harbor_cut/heightfield.bin',
  ...cfg.targets.map(t=>'enclosures/'+t.enclosure+'.json')];
const manifest=JSON.parse(fs.readFileSync(path.join(root,'chicago/4d/data/transport/parked/placements.json')));
for(const model of Object.values(manifest.models))for(const field of['file','support_file'])if(model[field])common.push(model[field]);
const pinFiles=[...new Set([...common.flatMap(p=>['chicago/4d/renderers/web/'+p,'site/4d/walk/'+p]),...data.flatMap(p=>['chicago/4d/data/'+p,'site/4d/data/'+p]),'site/4d/walk/index.html'])];
const inputPins=Object.fromEntries(pinFiles.map(p=>[p,sha(fs.readFileSync(path.join(root,p)))]));
for(const p of common)if(inputPins['chicago/4d/renderers/web/'+p]!==inputPins['site/4d/walk/'+p])throw Error('Stale renderer mirror '+p);
for(const p of data)if(inputPins['chicago/4d/data/'+p]!==inputPins['site/4d/data/'+p])throw Error('Stale data mirror '+p);
for(const t of cfg.targets)if(inputPins['chicago/4d/renderers/web/'+manifest.models[t.model].file]!==t.glbSha256)throw Error('Unreviewed covered model '+t.model);
if(!fs.readFileSync(path.join(root,'chicago/4d/renderers/web/js/main.js'),'utf8').includes('parkedTransport.setFallback((id, visible) => yard.setReplacementVisible(id, visible))'))throw Error('Main fallback link changed; review helper before running');
const receipt={scope:'Bounded actual1835 covered main proof;22 planned normal screenshots, partial angles only; no photo/LOD completion',started:new Date().toISOString(),headAtStart:initialHead,indexDigestAtStart:initialIndex,
 stagedFiles:git('diff','--cached','--name-only').split('\n').filter(Boolean),inputPins,config:cfg,adaptedFrom:'parked-scene-capture-2026-10-21.cjs',pages:[],pass:false};
const persist=()=>fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify(receipt,null,2)+'\n');
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.css':'text/css','.wasm':'application/wasm'};
const server=http.createServer((req,res)=>{if(req.url==='/favicon.ico'){res.writeHead(204);return res.end();}try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!f.startsWith(root+'/'))throw Error('path');if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end('not found');}});
let browser,currentPage,activePage;
function classify(page){return page.requestFailures.map(f=>{const response=page.responses.find(r=>r.requestId===f.requestId&&r.status===200),known=f.method==='HEAD'&&f.errorText==='net::ERR_ABORTED'&&/^\/(?:chicago\/4d|site\/4d)\/data\/sidecars\/1835\/people\.json$/.test(new URL(f.url).pathname)&&response;
 return{...f,accepted:!!known,reason:known?'Exact diagnosed people HEAD received HTTP200 then net::ERR_ABORTED; official smoke excludes ERR_ABORTED; this caller narrows that exception to this successful HEAD only':'Unclassified request failure remains a blocker',matchingResponse:response||null};});}
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 for(const job of cfg.pages){
  currentPage={label:job.label,detail:job.detail,published:job.published,viewport:[job.width,job.height],phase:'boot',errors:[],messages:[],requestFailures:[],responses:[],captures:[],controls:[]};receipt.pages.push(currentPage);persist();
  browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});
  const page=await browser.newPage({viewport:{width:job.width,height:job.height},hasTouch:job.viewport==='mobile',deviceScaleFactor:job.viewport==='mobile'?2:1});activePage=page;page.setDefaultTimeout(90000);
  const pr=currentPage,ids=new WeakMap();let requestSequence=0;const id=r=>{if(!ids.has(r))ids.set(r,++requestSequence);return ids.get(r);};
  page.on('pageerror',e=>pr.errors.push({phase:pr.phase,text:e.message}));
  page.on('requestfailed',r=>pr.requestFailures.push({requestId:id(r),phase:pr.phase,url:r.url(),method:r.method(),errorText:r.failure()?.errorText||''}));
  page.on('response',r=>{if(r.request().method()==='HEAD'||r.status()>=400)pr.responses.push({requestId:id(r.request()),phase:pr.phase,url:r.url(),method:r.request().method(),status:r.status()});if(r.status()>=400)pr.errors.push({phase:pr.phase,text:'HTTP'+r.status()+' '+r.url()});});
  page.on('console',m=>{if(['warning','error'].includes(m.type()))pr.messages.push({phase:pr.phase,type:m.type(),text:m.text(),location:m.location()});});
  await page.addInitScript(detail=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail})),job.detail);
  pr.url=origin+(job.published?'/site/4d/walk/':'/chicago/4d/renderers/web/')+'?year=1835&keep-geometry=1';
  await page.goto(pr.url,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240000,polling:1000});
  await page.evaluate(async detail=>{const a=window.__chicago4d;if(!a.ready)throw Error('boot '+a.error);const end=performance.now()+90000;while(a.welcome?.state!=='world'&&performance.now()<end){if(a.welcome?.state==='welcome')a.welcome.enter('spawn');await new Promise(r=>setTimeout(r,100));}if(a.welcome?.state!=='world')throw Error('World welcome did not finish');document.getElementById('control-help-gotit')?.click();document.exitPointerLock?.();if(a.detail!==detail)await a.setDetail(detail);},job.detail);
  pr.installed=await page.evaluate(install,{targets:cfg.targets,detail:job.detail});persist();
  async function shot(target,angle,mode){
   pr.phase=target.label+'-'+angle+'-'+mode;const state=await page.evaluate(({id,mode})=>window.__coveredInspection.capture(id,mode),{id:target.originalId,mode});
   const name=job.label+'-'+target.label+'-'+angle+'-'+mode,entry={name,angle,mode,state,screenshot:'pending'};pr.captures.push(entry);persist();
   console.log('STATE '+name+' '+JSON.stringify(state.draw));const file=path.join(out,name+'.png');
   try{await page.screenshot({path:file,timeout:90000});}catch(error){entry.screenshot='failed';entry.captureError=error.message;persist();throw error;}const raw=fs.readFileSync(file);entry.screenshot='saved';entry.sha256=sha(raw);entry.bytes=raw.length;entry.pngSize=[raw.readUInt32BE(16),raw.readUInt32BE(20)];persist();return entry;
  }
  for(const target of cfg.targets){
   pr.view=await page.evaluate(id=>window.__coveredInspection.view(id,'front-quarter'),target.originalId);persist();
   const old=await shot(target,'front-quarter','legacy'),fresh=await shot(target,'front-quarter','refined');
   for(const key of['camera','projection','lighting'])if(JSON.stringify(old.state[key])!==JSON.stringify(fresh.state[key]))throw Error('Matched reference changed '+key);
   pr.phase=target.label+'-controls';const controls=await page.evaluate(async id=>({id,runtime:await window.__coveredInspection.controls(id),clearance:await window.__coveredInspection.clearance(id)}),target.originalId);pr.controls.push(controls);persist();
   for(const angle of job.extraAngles||[]){pr.view=await page.evaluate(({id,angle})=>window.__coveredInspection.view(id,angle),{id:target.originalId,angle});persist();await shot(target,angle,'refined');}
  }
  pr.phase='end-of-page-disposal';pr.disposal=await page.evaluate(()=>window.__coveredInspection.disposeCheck());persist();
  pr.phase='closing';await page.close();await browser.close();browser=null;pr.requestClassification=classify(pr);
  pr.pass=!pr.errors.length&&!pr.messages.some(m=>m.type==='error')&&!pr.requestClassification.some(f=>!f.accepted)&&pr.captures.every(c=>c.screenshot==='saved');persist();
  if(!pr.pass)throw Error('Page errors or unclassified requests in '+job.label);
 }
 const count=receipt.pages.reduce((n,p)=>n+p.captures.length,0);if(count!==cfg.expectedScreenshots)throw Error('Planned screenshot count differs: '+count);receipt.pass=receipt.pages.every(p=>p.pass);
})().catch(async e=>{receipt.pass=false;receipt.error=e.stack;if(currentPage)currentPage.requestClassification=classify(currentPage);if(activePage)receipt.failureState=await activePage.evaluate(()=>({title:document.title,text:document.body.innerText.slice(0,6000),ready:window.__chicago4d?.ready,error:window.__chicago4d?.error,problems:window.__chicago4d?.problems})).catch(error=>({readError:error.message}));process.exitCode=1;}).finally(async()=>{
 if(browser)await browser.close().catch(e=>{receipt.closeError=e.message;receipt.pass=false;});if(server.listening)await new Promise(r=>server.close(r));receipt.browserAndServerClosed=true;receipt.ended=new Date().toISOString();
 try{receipt.headAtEnd=git('rev-parse','HEAD');receipt.indexUnchanged=indexDigest()===initialIndex;receipt.noUnstagedAtEnd=noUnstaged();receipt.inputsUnchanged=pinFiles.every(p=>sha(fs.readFileSync(path.join(root,p)))===inputPins[p]);if(receipt.headAtEnd!==initialHead||!receipt.indexUnchanged||!receipt.noUnstagedAtEnd||!receipt.inputsUnchanged)receipt.pass=false;}catch(e){receipt.reconciliationError=e.message;receipt.pass=false;}
 if(!receipt.pass)process.exitCode=1;fs.writeFileSync(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify({out,pass:receipt.pass,error:receipt.error,pages:receipt.pages.length,screenshots:receipt.pages.reduce((n,p)=>n+p.captures.filter(c=>c.screenshot==='saved').length,0),closed:true}));
});
