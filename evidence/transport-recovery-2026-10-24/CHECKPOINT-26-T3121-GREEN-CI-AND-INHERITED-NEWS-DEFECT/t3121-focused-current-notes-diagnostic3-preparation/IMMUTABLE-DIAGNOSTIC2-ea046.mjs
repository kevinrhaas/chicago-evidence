#!/usr/bin/env node
// EXTERNAL FOCUSED CURRENT-NOTES PROOF. Not canonical PART13, all-stage smoke, or confidence persistence.
// DIAGNOSTIC2 COPY: unchanged assertions/source pins; bounded geometry + prethrow failure screenshots. Root must authorize execution.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import vm from 'node:vm';
const REPO='/workspace/chicago-smoke-infra-t3121';
const BASE='33a99a557bd53aa637cc7173589d610f8a15f14b';
const STAGED_TREE='534ff7c9f129235ad6433e20de124e186d7729f6';
const WORKFLOW_SHA='f0f6c6f5cf942af4e49609b7854bdd1472bd98e06159e687ed76893138e7a73c';
const NOTES_SHA='54d80dc8e4e180f5e1cd05a192e9a2f6ee336535d61e1977ddfef6ff245fdbf1';
const CANONICAL_SMOKE_SHA='4586e7101000910cde7743048b72b72b3b04f7896417f5fe1a97af14e1e941bd';
const APP=path.join(REPO,'chicago/4d'), SITE=path.join(REPO,'site/4d');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(p);
const git=(...args)=>execFileSync('git',args,{cwd:REPO,encoding:'utf8',maxBuffer:128*1024*1024,env:{...process.env,GIT_OPTIONAL_LOCKS:'0'}});
const arg=k=>{const i=process.argv.indexOf(k);return i<0?null:process.argv[i+1];};
if(!process.argv.includes('--execute-after-gate')||!arg('--output')){
 console.error('Prepared helper only. Root launch after green full preflight: node <helper> --execute-after-gate --expected-head <actualHEAD> --output <NEW external output directory>');
 process.exit(2);
}
const EXPECTED_HEAD=arg('--expected-head')||BASE;
if(!/^[0-9a-f]{40}$/.test(EXPECTED_HEAD))throw new Error('Expected head must be a complete40hexSHA');
const OUTPUT=path.resolve(arg('--output'));
if(!OUTPUT.startsWith('/workspace/.cloud-setup/')||fs.existsSync(OUTPUT))throw new Error('Output must be a NEW external .cloud-setup directory');
fs.mkdirSync(OUTPUT,{recursive:true});
const started=Date.now(), assertions=[], viewportResults=[];
const report={label:'FOCUSED CURRENT-NOTES PROOF ONLY — NOT A NEW FULL PART13 OR FULL GATE',base:BASE,expected_head:EXPECTED_HEAD,staged_tree:STAGED_TREE,workflow_sha256:WORKFLOW_SHA,notes_sha256:NOTES_SHA,canonical_smoke_sha256:CANONICAL_SMOKE_SHA,assertions,viewports:viewportResults,coverage_limits:['Does not re-run other PART13 assertions, confidence persistence, renderer matrices or full gates.','Composite evidence additionally requires separately verified accepted18-leg coverage and exact source/hash equivalence; this script does not replace either.']};
const cleanUrl=v=>{try{const u=new URL(v);u.search='';u.hash='';u.username='';u.password='';return u.href;}catch{return String(v);}};
const cleanText=s=>String(s).replace(/https?:\/\/[^\s<>"']+/g,cleanUrl);
function check(name,condition,detail=null){const r={name,result:condition?'PASS':'FAIL',seconds:(Date.now()-started)/1000,detail};assertions.push(r);console.log(`${r.result} ${name}${detail===null?'':` ${JSON.stringify(detail)}`}`);if(!condition)throw new Error(name);}
function saveReport(){report.finished_utc=new Date().toISOString();report.seconds=(Date.now()-started)/1000;fs.writeFileSync(path.join(OUTPUT,'FOCUSED-CURRENT-NOTES-RESULT.json'),JSON.stringify(report,null,2)+'\n');}
function listingRecords(raw,tree=false){return raw.split('\0').filter(Boolean).map(r=>{const [meta,p]=r.split('\t');const fields=meta.split(' ');return [p,fields[0],tree?fields[2]:fields[1],tree?'0':fields[2]].join('\t');}).sort();}
function assertBindings(){
 check('HEAD equals explicitly provided candidate binding',git('rev-parse','HEAD').trim()===EXPECTED_HEAD);
 if(EXPECTED_HEAD!==BASE)check('committed candidate tree equals validated stagedtree534',git('rev-parse',EXPECTED_HEAD+'^{tree}').trim()===STAGED_TREE);
 check('app subtree equals pinned accepted33 source',git('rev-parse',EXPECTED_HEAD+':chicago/4d').trim()==='85318f4e2583bd004aef6a713e65717bc0b98ac9');
 check('staged index equals pinned candidate tree534 without writing an index',JSON.stringify(listingRecords(git('ls-files','--stage','-z')))===JSON.stringify(listingRecords(git('ls-tree','-rz',STAGED_TREE),true)));
 check('no unstaged tracked source changes',git('diff','--name-only').trim()==='');
 check('candidate changes only the workflow',git('diff','--cached','--name-only',BASE).trim()==='.github/workflows/chicago-4d-smoke.yml');
 check('workflow and canonical smoke bytes remain pinned',sha(read(path.join(REPO,'.github/workflows/chicago-4d-smoke.yml')))===WORKFLOW_SHA&&sha(read(path.join(APP,'tools/smoke_renderer.mjs')))===CANONICAL_SMOKE_SHA);
 check('source notes remain pinned',sha(read(path.join(APP,'renderers/web/js/changelog.js')))===NOTES_SHA);
}
function manifest(root){const files=[];const walk=dir=>{for(const e of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.isFile()){const b=read(p);files.push({path:path.relative(root,p),bytes:b.length,sha256:sha(b)});}else throw new Error('Unexpected published symlink/non-file '+p);}};walk(root);return files;}
const indexBefore=sha(read(path.join(REPO,'.git/index')));
let server=null, activeBrowser=null, beforePublished=null;
try{
 const gate=JSON.parse(read('/workspace/.cloud-setup/logs/transport-recovery/t3121-full-preflight-before-commit.result.json'));
 check('full preflight completed successfully before this explicit launch',gate.returncode===0&&gate.timed_out===false,{returncode:gate.returncode,timed_out:gate.timed_out});
 assertBindings();
 const publishedBuild=JSON.parse(read(path.join(SITE,'build.json')));
 const expectedVersion=git('rev-parse','--short',EXPECTED_HEAD).trim();
 check('published build.version equals the provided expectedHEAD',publishedBuild.version===expectedVersion,{expected_head:EXPECTED_HEAD,expectedVersion,publishedBuild});report.published_build=publishedBuild;
 const stateSource=read(path.join(APP,'tools/dev-smoke-state.mjs')).toString();
 const array=name=>{const m=stateSource.match(new RegExp('const '+name+' = (\\[[\\s\\S]*?\\]);'));if(!m)throw new Error('Missing canonical hash array '+name);return vm.runInNewContext(m[1]);};
 const inputRows=git('ls-files','-s','--',...array('SMOKE_INPUTS')), notesRows=git('ls-files','-s','--',...array('CHANGELOG_INPUTS'));
 check('canonical indexed source input rows equal frozen broad baseline',sha(Buffer.from(inputRows))==='770d7ae5bfa6c1f55114cc71b1212834744cdb9c6fcdbce139b72b4bf75ff5ac');
 check('canonical notes index digest equals current33 notes binding',sha(Buffer.from(notesRows))==='5f9fc879b184e3eeed7a7f4485202da3fe2e48f54e599feb54396c3063043001');
 const baselineBroad=sha(Buffer.from(inputRows+'\nsite/4d/walk/index.html\n'));
 check('frozen absent-mirror broad baseline reconstructs exactly',baselineBroad==='c99ccd04ae0d493be425078902f96c768bb8436394ecc3b096d6ccacbf41c63c');
 const normalizedPage=read(path.join(SITE,'walk/index.html')).toString().replace(/build\s+[0-9a-f]{6,}\s+·[^<\n]*/g,'build <stamp>');
 report.hash_binding={source_listing_sha256:sha(Buffer.from(inputRows)),notes_index_sha256:sha(Buffer.from(notesRows)),frozen_absent_mirror_broad_sha256:baselineBroad,actual_present_mirror_broad_sha256:sha(Buffer.from(inputRows+'\nsite/4d/walk/index.html\n'+normalizedPage)),normalized_published_page_sha256:sha(Buffer.from(normalizedPage)),limitation:'The frozen standard baseline had no mirror extra. The actual post-publish normalized-page digest is reported separately, never falsely equated or used alone to transfer coverage.'};
 const sourceBytes=read(path.join(APP,'renderers/web/js/changelog.js'));
 const source=await import('data:text/javascript;base64,'+sourceBytes.toString('base64'));
 const feed=source.CHANGELOG, newest=feed[0], versions=feed.map(e=>e.v);
 check('actual source newest release is2255 and has predecessor2254',source.LATEST_VERSION===2255&&newest.v===2255&&feed.some(e=>e.v===2254),{newest});
 report.source_newest=newest;report.feed_release_count=feed.length;report.actual_versions=versions;
 const {WALK_SHIM}=await import(pathToFileURL(path.join(APP,'tools/changelog_shim.mjs')).href);
 check('published fleet changelog bytes equal actual source',read(path.join(SITE,'js/changelog.js')).equals(sourceBytes));
 check('published walk file equals canonical re-export stub',read(path.join(SITE,'walk/js/changelog.js')).equals(Buffer.from(WALK_SHIM)));
 beforePublished=manifest(SITE);fs.writeFileSync(path.join(OUTPUT,'PUBLISHED-MANIFEST-BEFORE.json'),JSON.stringify(beforePublished,null,2)+'\n');
 report.published_manifest_digest=sha(Buffer.from(JSON.stringify(beforePublished)));report.published_files=beforePublished.length;
 const MIME={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.wasm':'application/wasm','.glb':'model/gltf-binary','.gltf':'model/gltf+json','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml','.webp':'image/webp','.ico':'image/x-icon','.woff2':'font/woff2','.bin':'application/octet-stream'};
 server=http.createServer((req,res)=>{try{let requested=decodeURIComponent(new URL(req.url,'http://localhost').pathname);let file=path.resolve(SITE,'.'+requested);if(file!==SITE&&!file.startsWith(SITE+path.sep)){res.writeHead(403);res.end();return;}if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');if(!fs.existsSync(file)){res.writeHead(404);res.end('not found');return;}res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);}catch{res.writeHead(400);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`, entry=origin+'/walk/?year=1835&keep-geometry=1';
 let pw;try{pw=await import('playwright');}catch{const root=(process.env.NODE_PATH||execFileSync('npm',['root','-g'],{encoding:'utf8'})).trim().split(path.delimiter)[0];pw=await import(pathToFileURL(path.join(root,'playwright/index.js')).href);}const {chromium}=pw.chromium?pw:pw.default;
 for(const [label,viewport,touch] of [['mobile390x780',{width:390,height:780},true],['desktop1280x800',{width:1280,height:800},false]]){
  const v={label,viewport,hasTouch:touch,started_utc:new Date().toISOString(),errors:[],network:[],screenshots:[],boots:[]};viewportResults.push(v);const viewStart=Date.now();
  let diagnosticPage=null;
  const captureFailure=async(p,stem)=>{
   if(!p)return;
   const record={stage:stem,at_seconds:(Date.now()-viewStart)/1000};
   try{record.dom=await p.evaluate(()=>{
    const name=el=>!el?null:`${el.tagName.toLowerCase()}${el.id?'#'+el.id:''}${typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''}`;
    const rect=el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
    const detail=el=>{if(!el)return null;const c=getComputedStyle(el);let a=el.parentElement,scroll=null;while(a){const x=getComputedStyle(a);if(['auto','scroll','hidden','clip'].includes(x.overflowX)||['auto','scroll','hidden','clip'].includes(x.overflowY)){scroll={element:name(a),rect:rect(a),clientWidth:a.clientWidth,scrollWidth:a.scrollWidth,clientHeight:a.clientHeight,scrollHeight:a.scrollHeight,overflowX:x.overflowX,overflowY:x.overflowY};break;}a=a.parentElement;}return {element:name(el),rect:rect(el),clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,clientHeight:el.clientHeight,scrollHeight:el.scrollHeight,hidden:el.hidden,hiddenAncestor:name(el.closest('[hidden]')),display:c.display,visibility:c.visibility,transform:c.transform,position:c.position,overflowX:c.overflowX,overflowY:c.overflowY,width:c.width,minWidth:c.minWidth,maxWidth:c.maxWidth,gridTemplateColumns:c.gridTemplateColumns,paddingLeft:c.paddingLeft,paddingRight:c.paddingRight,zoom:c.zoom,whiteSpace:c.whiteSpace,overflowWrap:c.overflowWrap,wordBreak:c.wordBreak,closestScrollParent:scroll};};
    const selectors=['#navigator','#nav-app-settings','#panel','.panel-scroll','.panel-body[data-panel="whatsnew"]','#whatsnew','.wn-list'];
    return {viewport:{width:innerWidth,height:innerHeight},journey:document.documentElement.dataset.journey,subtab:window.__chicago4d?.hud?.tab,navApp:window.__chicago4d?.navigator?.app,navLevel:window.__chicago4d?.navigator?.level,selectedTabs:[...document.querySelectorAll('#panel .panel-tab[aria-selected="true"]')].map(x=>({tab:x.dataset.tab,hidden:x.hidden})),entries:document.querySelectorAll('#whatsnew .wn-entry').length,hostBusy:document.getElementById('whatsnew')?.getAttribute('aria-busy'),hostTextStart:document.getElementById('whatsnew')?.textContent.slice(0,160),nodes:selectors.map(selector=>({selector,...detail(document.querySelector(selector))}))};
   });}catch(e){record.dom_error=cleanText(e.message||e);}
   try{const filename=`${label}-${stem}-FAILURE.png`;await p.screenshot({path:path.join(OUTPUT,filename)});record.screenshot=filename;v.screenshots.push(filename);}catch(e){record.screenshot_error=cleanText(e.message||e);}
   (v.failure_diagnostics??=[]).push(record);fs.writeFileSync(path.join(OUTPUT,`${label}-${stem}-DIAGNOSTIC.json`),JSON.stringify(record,null,2)+'\n');
  };
  try{
   activeBrowser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
   const ctx=await activeBrowser.newContext({viewport,hasTouch:touch,isMobile:false,deviceScaleFactor:touch?2:1});const page=await ctx.newPage();diagnosticPage=page;page.setDefaultTimeout(90_000);
   const newsRequests=[];page.on('request',r=>{if(/\/js\/changelog\.js$/.test(new URL(r.url()).pathname))newsRequests.push({path:new URL(r.url()).pathname,at_seconds:(Date.now()-viewStart)/1000});});
   page.on('pageerror',e=>v.errors.push('pageerror: '+cleanText(e.message||e)));page.on('response',r=>{if(r.status()>=400)v.errors.push(`HTTP ${r.status()} ${cleanUrl(r.url())}`);if(/\/js\/changelog\.js$/.test(new URL(r.url()).pathname))v.network.push({path:new URL(r.url()).pathname,status:r.status()});});page.on('requestfailed',r=>{const why=r.failure()?.errorText||'';if(!/ERR_ABORTED/.test(why))v.errors.push(`request failed (${cleanText(why)}) ${cleanUrl(r.url())}`);});page.on('console',m=>{if(m.type()==='error'&&!m.text().startsWith('Failed to load resource'))v.errors.push('console.error: '+cleanText(m.text()));});
  const clickChrome = async (sel) => {
    const why = await page.evaluate(async (s) => {
      const el = document.querySelector(s);
      if (!el) return `nothing matches ${s}`;
      if (el.disabled) return `${s} is disabled`;
      // T-0701: the drawer SLIDES. `#panel[hidden]` keeps its layout and sits at
      // translateX(102%), and opening it is a .24 s transform — so for a quarter
      // of a second after `setPanel(true)` a tab has a real box whose centre is
      // off the right edge of the viewport, and `elementFromPoint` answers
      // `null` for it. A visitor clicks a drawer that has arrived; so does this.
      // Waited for, never assumed: the hit-test below still runs on the settled
      // box, and a control that is genuinely covered still fails here.
      const drawer = el.closest('#panel');
      if (drawer) {
        for (let i = 0; i < 40 && getComputedStyle(drawer).transform !== 'none'; i++) {
          await new Promise((r) => setTimeout(r, 50));
        }
      }
      // The Navigator WIDENS too. On a desktop its open is a .28 s width transition from
      // the 58 px rail to 400 px, and the transition's clock only moves when the page gets
      // to draw; on a runner where a frame of the town takes seconds, a fixed wait can end
      // with the panel still a sliver. T-2622's keyboard check ends on Escape (the panel
      // collapsed to its rail) and T-2630's opens it and clicks Home's Go to after 400 ms:
      // "covered at its own centre by <button class=\"nav-choice\">". Waited for the same
      // way as the drawer: the hit-test still runs, on the settled box.
      const device = el.closest('#navigator');
      if (device?.getAnimations) {
        for (let i = 0; i < 60 && device.getAnimations().some((a) => a.playState === 'running'); i++) {
          await new Promise((r) => setTimeout(r, 50));
        }
      }
      // The same scroll `page.click` would do, in the same round trip as the
      // reading — a result row far down the Go-to list is off the panel's
      // viewport until this runs, and `elementFromPoint` would then answer for
      // whatever is at those coordinates instead.
      el.scrollIntoView({ block: 'center', inline: 'center' });
      const b = el.getBoundingClientRect();
      if (b.width < 1 || b.height < 1) {
        return `${s} has no box (${Math.round(b.width)}x${Math.round(b.height)})`;
      }
      const top = document.elementFromPoint(b.x + b.width / 2, b.y + b.height / 2);
      if (!top || !(top === el || el.contains(top))) {
        const cls = top && typeof top.className === 'string' ? top.className : '';
        // NAME THE OVERLAY, NOT JUST THE TAG IT ENDS IN (T-0369). The first
        // report of this failure said only `<h2>`, and an `<h2>` is a heading
        // inside something — the thing worth naming is the panel that heading
        // belongs to. Walking up to the nearest ancestor carrying an id turns
        // "covered by <h2>" into "covered by <h2> inside #popup", which is the
        // whole diagnosis of a stale overlay left open by an earlier stage.
        let owner = top;
        while (owner && !owner.id && owner !== document.body) owner = owner.parentElement;
        const inside = owner && owner.id && owner !== el ? ` inside #${owner.id}` : '';
        // T-2620: the Navigator covers chrome only when it is open; say which height it was at.
        const nav = top?.closest?.('#navigator');
        const at = nav ? ` (Navigator ${nav.dataset.detent}, app ${window.__chicago4d?.navigator?.app ?? '?'})` : '';
        return `${s} is covered at its own centre by `
          + `<${top ? top.tagName.toLowerCase() : 'nothing'}${cls ? ` class="${cls}"` : ''}>${inside}${at}`;
      }
      // A real mouse press FOCUSES a focusable control, and an untrusted
      // `.click()` does not — which is a difference the suite already depends on
      // and which this helper got wrong on its first run, honestly and visibly.
      // Part 8 closes the panel and then presses `g`, and `g` only reaches the
      // window shortcut if focus has left the Go-to search box first: the shared
      // `isTyping(e.target)` guard swallows it otherwise, which is the whole
      // point of that guard. Without this line the panel stayed shut, `g` did
      // nothing, and the next reading was a result row with a 0x0 box. So this
      // is fidelity to the click being replaced, not a convenience.
      if (typeof el.focus === 'function') el.focus({ preventScroll: true });
      el.click();
      return null;
    }, sel);
    if (why) throw new Error(`clickChrome: ${why}`);
  };
  // T-2620: the drawer and its hamburger are gone; each of the drawer's sections is held by
  // a Navigator app (apps/drawer-host.js). A visitor reaches one by the app's rail icon —
  // on a phone the rail shows once the sheet is open, so the handle comes first — and,
  // where the app holds two sections, by the section's own tab. Each is a hit-tested click.
  const SECTION_APP = { travel: 'move', people: 'people', businesses: 'people',
    controls: 'guide', evidence: 'guide', settings: 'settings', whatsnew: 'settings' };
  const openSection = async (tab) => {
    const opened = () => page.waitForFunction(() => {
      const r = document.getElementById('navigator')?.getBoundingClientRect();
      return r && (innerWidth > 620 ? r.width >= 380 : r.height >= innerHeight * 0.4);
    }, null, { timeout: 60_000, polling: 100 });
    if (touch && await page.evaluate(() => window.__chicago4d.navigator?.level === 0)) {
      await clickChrome('#nav-grip');
      await opened();
    }
    await clickChrome(`#nav-rail [data-app="${SECTION_APP[tab]}"]`);
    await opened();
    await page.waitForFunction(() => { const p = document.getElementById('panel'); return p && !p.hidden && !!p.closest('.nav-screen:not([hidden])'); },
      null, { timeout: 60_000, polling: 100 });
    if (await page.evaluate(() => window.__chicago4d.hud.tab) !== tab) await clickChrome(`.panel-tab[data-tab="${tab}"]`);
  };
  // T-2613: Home appears halfway through the landing's flip, not at ready (the old
  // #gate-btn sat on screen at ready), so a click on #home-roam waits for the journey
  // to land. Bounded, and loud: a landing that never comes fails here by name, with
  // the journey state and the landing phase it stopped in.
  const untilLanded = async (timeout = 90_000) => {
    try {
      await page.waitForFunction(() => document.documentElement.dataset.journey === 'landed',
        null, { timeout, polling: 100 });
    } catch {
      const at = await page.evaluate(() => ({
        journey: document.documentElement.dataset.journey ?? '(none)',
        landing: document.querySelector('.gate-card')?.dataset.landing ?? '(none)',
        gate: document.getElementById('gate')?.dataset.state ?? '(none)',
      })).catch(() => ({}));
      throw new Error(`the landing never reached "landed" within ${timeout / 1000} s after ready — `
        + `journey ${at.journey}, landing phase ${at.landing}, gate ${at.gate}`);
    }
  };

   const bootReady=()=>page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240_000,polling:1000});
   const boot=async(reload=false)=>{const t=Date.now();if(reload)await page.reload({waitUntil:'domcontentloaded'});else await page.goto(entry,{waitUntil:'domcontentloaded'});await bootReady();await untilLanded();await clickChrome('#home-roam');await page.waitForTimeout(150);await page.evaluate(()=>document.exitPointerLock?.());await page.waitForFunction(()=>document.getElementById('gate')?.hasAttribute('hidden'),null,{timeout:90_000,polling:100});if(await page.evaluate(()=>{const h=document.getElementById('control-help');return !!h&&!h.hasAttribute('hidden');}))await clickChrome('#control-help-gotit');v.boots.push({reload,seconds:(Date.now()-t)/1000,journey:await page.evaluate(()=>document.documentElement.dataset.journey)});};
   const dots=()=>page.evaluate(()=>({chip:!document.getElementById('help-dot')?.hasAttribute('hidden'),tab:!document.getElementById('whatsnew-dot')?.hasAttribute('hidden')}));
   const waitFeed=async()=>{try{await page.waitForFunction(()=>document.querySelector('#whatsnew .wn-entry')&&document.getElementById('help-dot')?.hasAttribute('hidden'),null,{timeout:20_000,polling:100});}catch(e){await captureFailure(page,'feed-wait-timeout');throw e;}};
   const snapshot=()=>page.evaluate(()=>{const host=document.getElementById('whatsnew');return {rows:[...host.querySelectorAll('.wn-entry')].map(el=>({title:el.querySelector('.wn-title')?.textContent||'',meta:el.querySelector('.wn-meta')?.textContent||'',items:[...el.querySelectorAll('.wn-items li')].map(x=>x.textContent),isNew:el.classList.contains('is-new')})),cleared:document.getElementById('help-dot')?.hasAttribute('hidden')&&document.getElementById('whatsnew-dot')?.hasAttribute('hidden'),seen:localStorage.getItem('chicago4d.whatsnew.seen')};});
   const screenshot=async name=>{const file=`${label}-${name}.png`;await page.screenshot({path:path.join(OUTPUT,file)});v.screenshots.push(file);};
   const layout=async name=>{
    const result=await page.evaluate(()=>{
     const s=document.querySelector('#nav-app-settings');if(!s||s.hidden)return {error:'no shown Settings/news screen'};
     const box=s.getBoundingClientRect();const hidden=el=>el.closest('.visually-hidden, [aria-hidden="true"]');const all=[...s.querySelectorAll('*')].filter(el=>el.getClientRects().length&&!hidden(el));
     const name=el=>`${el.tagName.toLowerCase()}${el.id?'#'+el.id:''}${typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''}`;
     const past=all.filter(el=>{const r=el.getBoundingClientRect();return r.width>0&&(r.right>box.right+1||r.left<box.left-1);});
     const cut=all.filter(el=>{if(!el.textContent.trim())return false;const cs=getComputedStyle(el);if(['auto','scroll'].includes(cs.overflowX)||['auto','scroll'].includes(cs.overflowY))return false;if(cs.overflowX==='visible'&&cs.overflowY==='visible'&&cs.textOverflow!=='ellipsis')return false;return el.scrollWidth>el.clientWidth+1||el.scrollHeight>el.clientHeight+2;});
     const strips=[s,...all].filter(el=>!el.matches('.insp-swipe')&&['auto','scroll'].includes(getComputedStyle(el).overflowX)&&el.scrollWidth>el.clientWidth+1);
     const rect=el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
     const detail=el=>{const c=getComputedStyle(el);let a=el.parentElement,scroll=null;while(a){const x=getComputedStyle(a);if(['auto','scroll','hidden','clip'].includes(x.overflowX)||['auto','scroll','hidden','clip'].includes(x.overflowY)){scroll={element:name(a),rect:rect(a),clientWidth:a.clientWidth,scrollWidth:a.scrollWidth,clientHeight:a.clientHeight,scrollHeight:a.scrollHeight,overflowX:x.overflowX,overflowY:x.overflowY};break;}a=a.parentElement;}return {element:name(el),rect:rect(el),clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,clientHeight:el.clientHeight,scrollHeight:el.scrollHeight,hiddenAncestor:el.closest('[hidden]')?name(el.closest('[hidden]')):null,display:c.display,visibility:c.visibility,transform:c.transform,width:c.width,minWidth:c.minWidth,gridTemplateColumns:c.gridTemplateColumns,overflowX:c.overflowX,overflowY:c.overflowY,whiteSpace:c.whiteSpace,overflowWrap:c.overflowWrap,wordBreak:c.wordBreak,closestScrollParent:scroll,textStart:el.textContent.slice(0,120)};};
     return {scale:getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim(),stored:JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').textScale,subtab:window.__chicago4d?.hud?.tab,screen:{left:box.left,right:box.right,width:box.width},past_count:past.length,cut_count:cut.length,strips_count:strips.length,past_first8:past.slice(0,8).map(detail),cut_first8:cut.slice(0,8).map(detail),strips_first8:strips.slice(0,8).map(detail)};
    });
    v[name]=result;const pass=!result.error&&result.past_count===0&&result.cut_count===0&&result.strips_count===0;
    if(!pass)await captureFailure(page,name+'-layout');
    check(`${label}: ${name} no horizontal overflow or clipped text`,pass,result);
   };
   await boot();check(`${label}: no changelog network import before first notes open`,newsRequests.length===0,newsRequests);
   const meta=await page.evaluate(()=>document.querySelector('meta[name="c4d-releases"]')?.content||'');const decoded=[];for(const part of meta.split(',')){const m=/^(\d+)(?:-(\d+))?$/.exec(part.trim());if(!m)throw new Error('Invalid release meta '+meta);const lo=Number(m[1]),hi=m[2]?Number(m[2]):lo;if(hi<lo)throw new Error('Descending release meta');for(let n=lo;n<=hi;n++)decoded.push(n);}check(`${label}: published releases meta equals actual source versions`,JSON.stringify(decoded.sort((a,b)=>a-b))===JSON.stringify([...versions].sort((a,b)=>a-b)),{meta,count:decoded.length});
   const unread=await dots();check(`${label}: canonical1 first-time visitor has both unread dots`,unread.chip&&unread.tab,unread);
   await openSection('whatsnew');await waitFeed();const first=await snapshot();v.first={entries:first.rows.length,items:first.rows.reduce((s,r)=>s+r.items.length,0),seen:first.seen,newest:first.rows[0]};
   check(`${label}: canonical2 feed renders every release`,first.rows.length>=5&&first.rows.reduce((s,r)=>s+r.items.length,0)>=first.rows.length,v.first);
   check(`${label}: canonical3 newest entry has title and CT date`,first.rows[0].title.length>4&&/CT$/.test(first.rows[0].meta),first.rows[0]);
   check(`${label}: canonical4 opening clears both dots and stores seen`,first.cleared&&Number(first.seen)>0,{cleared:first.cleared,seen:first.seen});
   check(`${label}: canonical5 first visit has no is-new flags`,first.rows.every(r=>!r.isNew));
   check(`${label}: exact source2255 title items and date rendered`,first.rows[0].title===newest.title&&JSON.stringify(first.rows[0].items)===JSON.stringify(newest.items)&&first.rows[0].meta.endsWith(newest.date)&&Number(first.seen)===source.LATEST_VERSION,first.rows[0]);
   check(`${label}: complete feed titles/items match actual source in order`,first.rows.length===feed.length&&first.rows.every((r,i)=>r.title===feed[i].title&&JSON.stringify(r.items)===JSON.stringify(feed[i].items||[])));
   v.first_open_lazy_responses=v.network.slice();check(`${label}: real first notes open fetched both re-export chain URLs before diagnostic imports`,['/walk/js/changelog.js','/js/changelog.js'].every(p=>v.first_open_lazy_responses.some(r=>r.path===p&&r.status===200)),v.first_open_lazy_responses);
   const modules=await page.evaluate(async()=>{const a=await import('/walk/js/changelog.js'),b=await import('/js/changelog.js');return {sameArray:a.CHANGELOG===b.CHANGELOG,sameLatest:a.LATEST_VERSION===b.LATEST_VERSION,latest:a.LATEST_VERSION,count:a.CHANGELOG.length};});check(`${label}: actual lazy re-export chain returns identical feed exports`,modules.sameArray&&modules.sameLatest&&modules.latest===source.LATEST_VERSION&&modules.count===feed.length,modules);check(`${label}: both lazy import URLs succeeded`,['/walk/js/changelog.js','/js/changelog.js'].every(p=>v.network.some(r=>r.path===p&&r.status===200)),v.network);
   await layout('normal-news');check(`${label}: fresh normal text size is100percent`,v['normal-news'].scale==='1');await screenshot('first-normal');
   await openSection('settings');await page.selectOption('#s-text-size','1.4');await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1.4',null,{timeout:20_000,polling:100});await openSection('whatsnew');await layout('140pct-news');check(`${label}: actual140percent preference applied and stored`,v['140pct-news'].scale==='1.4'&&v['140pct-news'].stored===1.4);await screenshot('first-140pct');await openSection('settings');await page.selectOption('#s-text-size','1');await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1',null,{timeout:20_000,polling:100});check(`${label}: text size restored to100percent and stored`,await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1'&&JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').textScale===1));await openSection('whatsnew');
   await page.evaluate(()=>localStorage.setItem('chicago4d.whatsnew.seen','3'));await boot(true);await openSection('whatsnew');await waitFeed();const ret=await snapshot(),flagged=ret.rows.filter(r=>r.isNew).map(r=>r.title),expected=feed.filter(e=>e.v>3).map(e=>e.title);v.returning_seen3={total:ret.rows.length,flagged:flagged.length,expected:expected.length,seen_after:ret.seen};check(`${label}: canonical6 returning seen3 flags exactly every subsequent release`,flagged.length===ret.rows.length-3&&flagged.length>0&&JSON.stringify(flagged)===JSON.stringify(expected)&&ret.cleared&&Number(ret.seen)===source.LATEST_VERSION,v.returning_seen3);await screenshot('returning-seen3');
   await page.evaluate(()=>localStorage.setItem('chicago4d.whatsnew.seen','2254'));await boot(true);const beforeAbout=await dots();check(`${label}: seen2254 sees both unread dots for2255`,beforeAbout.chip&&beforeAbout.tab,beforeAbout);await openSection('settings');check(`${label}: actual Settings About news link exists under About`,await page.evaluate(()=>!!document.getElementById('s-open-whatsnew')?.closest('#s-about')));await clickChrome('#s-open-whatsnew');await waitFeed();check(`${label}: Settings About link opens actual news tab`,await page.evaluate(()=>window.__chicago4d.hud.tab==='whatsnew'));
   const delta=await snapshot();const just=delta.rows.filter(r=>r.isNew);v.returning_seen2254={flagged:just,seen_after:delta.seen,cleared:delta.cleared};check(`${label}: seen2254 flags only actual2255 and clears unread state`,just.length===1&&just[0].title===newest.title&&JSON.stringify(just[0].items)===JSON.stringify(newest.items)&&just[0].meta.endsWith(newest.date)&&Number(delta.seen)===2255&&delta.cleared,v.returning_seen2254);await screenshot('about-returning-seen2254');
   check(`${label}: zero page console HTTP and request errors`,v.errors.length===0,v.errors);v.result='PASS';
  }catch(e){if(!v.failure_diagnostics?.length)await captureFailure(diagnosticPage,'other-failure');v.result='FAIL';v.exception=cleanText(e.stack||e);console.error(`${label} FAIL ${v.exception}`);}finally{v.seconds=(Date.now()-viewStart)/1000;if(activeBrowser){await activeBrowser.close().catch(e=>{v.cleanup_error=cleanText(e);});activeBrowser=null;}}
 }
 check('both required viewport focused proofs passed',viewportResults.length===2&&viewportResults.every(v=>v.result==='PASS'&&!v.cleanup_error),viewportResults.map(v=>({label:v.label,result:v.result,seconds:v.seconds})));
 assertBindings();const after=manifest(SITE);fs.writeFileSync(path.join(OUTPUT,'PUBLISHED-MANIFEST-AFTER.json'),JSON.stringify(after,null,2)+'\n');check('published mirror remained byte-identical throughout focused run',JSON.stringify(after)===JSON.stringify(beforePublished));check('real Git index remained byte-identical',sha(read(path.join(REPO,'.git/index')))===indexBefore);report.result='PASS';
}catch(e){report.result='FAIL';report.exception=cleanText(e.stack||e);console.error(report.exception);process.exitCode=1;}finally{if(activeBrowser)await activeBrowser.close().catch(()=>{});if(server){server.closeAllConnections?.();await new Promise(r=>server.close(r));}report.index_sha256_before=indexBefore;report.index_sha256_after=sha(read(path.join(REPO,'.git/index')));saveReport();const files=fs.readdirSync(OUTPUT).filter(n=>fs.statSync(path.join(OUTPUT,n)).isFile()).map(n=>{const b=read(path.join(OUTPUT,n));return{path:n,bytes:b.length,sha256:sha(b)};});fs.writeFileSync(path.join(OUTPUT,'OUTPUT-MANIFEST.json'),JSON.stringify({files},null,2)+'\n');console.log(`${report.result}: FOCUSED CURRENT NOTES ONLY; not a new canonical PART13/full gate; ${(Date.now()-started)/1000}s`);}
