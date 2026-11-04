/** Actual Lake House published Sources, Record and preserved Images in the default world. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/shared/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const plan = JSON.parse(fs.readFileSync(process.env.GT_PROBE_PLAN));
const out = process.env.GT_PROBE_OUT, viewport = process.env.GT_PROBE_VIEWPORT, leg=process.env.JAIL_PROBE_LEG; assert(['body','cards'].includes(leg));
assert(['desktop', 'mobile'].includes(viewport)); assert(out); fs.mkdirSync(out);
const mobile = viewport === 'mobile', root = plan.site_parent;
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const save = (name, value) => fs.writeFileSync(path.join(out, name), JSON.stringify(value, null, 2) + '\n');
const errors = [], network = [], cancelled = [], cleanupCancelled = [], requestTimeline = [], consoleErrors = [], serverErrors = [];
let phase='boot', teardown=false; const requestStarted=new WeakMap();
const guard = () => { for (const [name, binding] of Object.entries(plan.input_bindings)) assert.equal(sha(fs.readFileSync(name)), binding.sha256, name); };
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.glb': 'model/gltf-binary', '.ktx2': 'image/ktx2', '.ico': 'image/x-icon', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  try {
    let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
    if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404).end(); return; }
    res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    fs.createReadStream(file).on('error', e => { serverErrors.push(e.message); res.destroy(e); }).pipe(res);
  } catch (e) { serverErrors.push(e.message); res.writeHead(500).end(); }
});
let browser, context, page, jailCard=null, failure=null;
const started = performance.now();
try {
  guard();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const proxyUrl = process.env.HTTPS_PROXY ?? process.env.HTTP_PROXY;
  const proxy = proxyUrl ? (() => { const p = new URL(proxyUrl); return { server: p.origin, bypass: '127.0.0.1,localhost', username: decodeURIComponent(p.username) || undefined, password: decodeURIComponent(p.password) || undefined }; })() : undefined;
  process.env.PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK = '1';
  browser = await chromium.launch({ executablePath: '/usr/bin/chromium', proxy, args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
  context = await browser.newContext({ viewport: { width: mobile ? 390 : 1280, height: mobile ? 780 : 800 }, hasTouch: mobile, isMobile: false, deviceScaleFactor: mobile ? 2 : 1 });
  page = await context.newPage(); page.setDefaultTimeout(90000);
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('request', r=>{const entry={url:r.url(),phase,at:new Date().toISOString()};requestStarted.set(r,entry);requestTimeline.push({...entry,event:'started'});});
  page.on('requestfinished',r=>requestTimeline.push({url:r.url(),phase,at:new Date().toISOString(),event:'finished',started:requestStarted.get(r)}));
  page.on('requestfailed',r=>{const entry={url:r.url(),failure:r.failure(),phase,at:new Date().toISOString(),started:requestStarted.get(r),explicitTeardown:teardown};requestTimeline.push({...entry,event:'failed'});if(r.failure()?.errorText==='net::ERR_ABORTED')(teardown?cleanupCancelled:cancelled).push(entry);else network.push(entry);});
  page.on('response', r => { if (r.status() >= 400) network.push({ url: r.url(), status: r.status() }); });
  await context.addInitScript(() => { localStorage.setItem('chicago4d.researcher', 'on'); localStorage.setItem('chicago4d.settings', JSON.stringify({ detail: 'full' })); });
  assert.equal((await page.goto(`http://127.0.0.1:${server.address().port}/4d/walk/index.html?year=1835`)).status(), 200);
  await page.waitForFunction(() => window.__chicago4d?.ready === true, null, { timeout: 240000, polling: 1000 });
  await page.evaluate(async () => {
    const a = window.__chicago4d, end = Date.now() + 90000;
    while (a.welcome?.state !== 'world' && Date.now() < end) {
      if (a.welcome?.state === 'welcome') a.welcome.enter('spawn');
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    if (a.welcome?.state !== 'world') throw Error('Welcome did not enter world');
    document.exitPointerLock?.(); document.getElementById('control-help-gotit')?.click();
    a.setAnimationHold(true); a.setFloraSpread(true); a.popup.close(); a.navigator.dock();
  });
  phase='world-settle';
  const baseline = await page.evaluate(() => { const a = window.__chicago4d; return { frame: a.renderer.info.render.frame, ready: a.ready, welcome: a.welcome.state, visible: document.visibilityState, contextLost: a.renderer.getContext().isContextLost(), detail: a.detail }; });
  save('WORLD-SETTLE.json', { status: 'WAITING', baseline, native_counter_advances_required: 3, bound_ms: 180000 });
  assert(baseline.ready && baseline.welcome === 'world' && baseline.visible === 'visible' && !baseline.contextLost && Number.isSafeInteger(baseline.frame));
  await page.waitForFunction(start => {
    const a = window.__chicago4d;
    if (a.renderer.getContext().isContextLost()) throw Error('Native WebGL context lost');
    if (!a.ready || a.welcome.state !== 'world' || document.visibilityState !== 'visible') throw Error('World readiness changed');
    return Number.isSafeInteger(a.renderer.info.render.frame) && a.renderer.info.render.frame >= start + 3;
  }, baseline.frame, { timeout: 180000, polling: 500 });
  const settled = await page.evaluate(() => window.__chicago4d.renderer.info.render.frame);
  assert(settled >= baseline.frame + 3);
  save('WORLD-SETTLE.json', { status: 'PASS', baseline, settled, native_counter_advances_required: 3, bound_ms: 180000, scope: 'Renderer counter only; no FPS or GPU-readback timing claim' });


  if(leg==='body'){
    const targets=await page.evaluate(()=>{
      const a=window.__chicago4d,b=a.buildings.instanceBounds();
      return ['log_jail','log_jail_keeper_house'].map(id=>{const r=a.registry.get(id),m=a.buildings.matrixOf(id),feet=a.buildings.feetOf(id),box=b[id];if(!r||!m||!box||!feet.length)throw Error('Target not built '+id);const gaps=feet.map(([x,z])=>{const e=m.elements[0]*x+m.elements[8]*z+m.elements[12],n=-(m.elements[2]*x+m.elements[10]*z+m.elements[14]),y=m.elements[1]*x+m.elements[9]*z+m.elements[13];return{e,n,y,ground:a.terrain.surfaceHeight(e,n),gap:y-a.terrain.surfaceHeight(e,n)};});return{id,placement:r.sidecar.placement,phase:r.sidecar.phase,grade:r.sidecar.grade,box,gaps,placeholder:!!r.assetIsPlaceholder};});
    });
    for(const t of targets){assert(!t.placeholder);assert(t.box.size.every(v=>Number.isFinite(v)&&v>2));assert(t.gaps.every(g=>g.gap<=0.15));}save('ACTUAL-TARGET-BODIES.json',targets);
    const stands=[{name:'keeper-north-door-and-two-sash',e:476.51,n:-254.0,yaw:180,expect:'log_jail_keeper_house',point:[476.56,-269.96,1.55]}, {name:'keeper-east-gable-two-sash-and-loft',e:mobile?496.5:494,n:-272.27,yaw:270,expect:'log_jail_keeper_house',point:[479.72,-272.27,1.7]}, {name:'whole-compound-from-Randolph',e:470.5,n:-242,yaw:180,expect:null}];
    const readings=[];
    for(const stand of stands){
      phase='body:'+stand.name;
      const frame=await page.evaluate(s=>{const a=window.__chicago4d;a.popup.close();a.navigator.dock();a.setFly(false);a.walker.teleport({local_e:s.e,local_n:s.n,yaw_deg:s.yaw,pitch_deg:0});return a.renderer.info.render.frame;},stand);
      await page.waitForFunction(f=>window.__chicago4d.renderer.info.render.frame>=f+3,frame,{timeout:90000,polling:500});
      const seen=await page.evaluate(async s=>{const a=window.__chicago4d;let pick=null,ndc=null;if(s.expect){const base=a.buildings.positionOf(s.expect);ndc=a.project(s.point[0],s.point[1],base.y+s.point[2]);if(Math.abs(ndc.x)>1||Math.abs(ndc.y)>1||ndc.z< -1||ndc.z>1)throw Error('Target point out of frame');pick=await a.buildings.pickAtAsync(ndc,a.camera);}return{stand:s,player:{...a.player},frame:a.renderer.info.render.frame,ndc,picked:pick?.id??null,contextLost:a.renderer.getContext().isContextLost()};},stand);
      assert(!seen.contextLost);if(stand.expect)assert.equal(seen.picked,stand.expect,'Actual GPU-picked target must be drawn');await page.screenshot({path:path.join(out,stand.name+'.jpg'),type:'jpeg',quality:94});readings.push(seen);save('ACTUAL-BODY-STANDS.json',readings);
    }
    // Take a short real walk down the native keeper door's exterior approach.
    // No claim is made about an interior, or a closed gate being traversable.
    await page.evaluate(()=>{const a=window.__chicago4d;a.popup.close();a.setAnimationHold(false);a.setFly(false);a.walker.teleport({local_e:474.26,local_n:-267.4,yaw_deg:180,pitch_deg:0});});
    phase='native-keeper-approach';await page.locator('#view').focus();await page.waitForTimeout(250);const approachStart=await page.evaluate(()=>({...window.__chicago4d.walker.state}));assert(!approachStart.flying);await page.keyboard.down('w');
    try{await page.waitForFunction(n=>window.__chicago4d.walker.state.n<n-0.45,approachStart.n,{timeout:45000,polling:100});}finally{await page.keyboard.up('w');await page.evaluate(()=>window.__chicago4d.setAnimationHold(true));}
    const approachEnd=await page.evaluate(()=>({...window.__chicago4d.walker.state}));assert(approachEnd.n<approachStart.n-0.45);assert(Math.abs(approachEnd.e-approachStart.e)<0.3);assert(!approachEnd.blocked);save('NATIVE-KEEPER-APPROACH.json',{start:approachStart,end:approachEnd,scope:'Real forward movement in exterior doorway approach; no interior/gate traversal claim'});await page.screenshot({path:path.join(out,'keeper-entry-approach.jpg'),type:'jpeg',quality:94});
  }else{
    const cards=[];
    for(const id of ['log_jail','log_jail_keeper_house']){
      phase='cards:'+id;
      await page.evaluate(id=>{const a=window.__chicago4d;a.pick(id);document.querySelector('#popup [data-pop-tab="evidence"]')?.click();},id);
      await page.waitForFunction(id=>window.__chicago4d.popup.openId===id&&document.querySelector('#popup [data-pop-pane="evidence"]'),id,{timeout:30000});
      const card=await page.evaluate(id=>{const a=window.__chicago4d,r=a.registry.get(id),pop=document.querySelector('#popup'),pane=pop.querySelector('[data-pop-pane="evidence"]');return{id:a.popup.openId,name:r.sidecar.name,grade:r.sidecar.grade,phase:r.sidecar.phase,placement:r.sidecar.placement,sources:pane.textContent,sourceLinks:[...pane.querySelectorAll('a[href]')].map(a=>({href:a.href,text:a.textContent.trim()})),placeholder:!!r.assetIsPlaceholder};},id);
      assert.equal(card.id,id);assert(!card.placeholder);assert(card.sources.includes('Gale')||card.sources.includes('Trowbridge'));assert(card.sourceLinks.length>0);assert(card.sourceLinks.some(x=>/^https?:/.test(x.href)));await page.screenshot({path:path.join(out,id+'-sources.jpg'),type:'jpeg',quality:93});
      const citation=page.locator('#popup [data-pop-pane="evidence"] ol.cites > li').filter({hasText:/Gale|Trowbridge/i}).first();assert.equal(await citation.count(),1,'Visible source citation required');await citation.scrollIntoViewIfNeeded();const credit=await citation.evaluate(el=>{const r=el.getBoundingClientRect();let clip={left:0,top:0,right:innerWidth,bottom:innerHeight};for(let p=el.parentElement;p;p=p.parentElement){const c=getComputedStyle(p);if(/auto|scroll|hidden|clip/.test(c.overflowY+' '+c.overflowX)){const b=p.getBoundingClientRect();clip={left:Math.max(clip.left,b.left),right:Math.min(clip.right,b.right),top:Math.max(clip.top,b.top),bottom:Math.min(clip.bottom,b.bottom)};}}const probes=[[r.left+2,r.top+2],[r.right-2,r.bottom-2],[(r.left+r.right)/2,(r.top+r.bottom)/2]].map(([x,y])=>{const hit=document.elementFromPoint(x,y);return{x,y,unoccluded:!!hit&&(hit===el||el.contains(hit))};});return{text:el.textContent,rect:{left:r.left,top:r.top,right:r.right,bottom:r.bottom},clip,visible:r.width>0&&r.height>0&&r.left>=clip.left&&r.right<=clip.right&&r.top>=clip.top&&r.bottom<=clip.bottom&&probes.every(p=>p.unoccluded),probes,links:[...el.querySelectorAll('a[href]')].map(a=>{const b=a.getBoundingClientRect();return{href:a.href,text:a.textContent,visible:b.width>0&&b.height>0&&b.left>=clip.left&&b.right<=clip.right&&b.top>=clip.top&&b.bottom<=clip.bottom};})};});assert(credit.visible&&/1902/.test(credit.text)&&credit.links.some(h=>/^https?:/.test(h.href)&&h.visible),'Whole citation and its external1902 source link must be visible and unoccluded');card.visibleSourceCredit=credit;await page.screenshot({path:path.join(out,id+'-source-credit.jpg'),type:'jpeg',quality:93});
      const record=page.locator('#popup [data-pop-tab="record"]');await record.scrollIntoViewIfNeeded();await record.click();const pane=page.locator('#popup [data-pop-pane="record"]');assert(await pane.isVisible());card.record=await pane.textContent();assert(card.record.includes('1835')||card.record.includes('Beach'));await page.screenshot({path:path.join(out,id+'-record.jpg'),type:'jpeg',quality:93});
      const images=page.locator('#popup [data-pop-tab="images"]');if(await images.count()){await images.scrollIntoViewIfNeeded();await images.click();await page.waitForFunction(({id,n})=>{const a=window.__chicago4d;return !!a.popup.picturesDoc&&(a.popup.picturesDoc.by_structure[id]??[]).length===n&&!document.querySelector('#popup [data-pop-pane="images"]').textContent.includes('LOADING IMAGE INDEX');},{id,n:plan.expected_picture_rows[id].length},{timeout:30000});const imagePane=page.locator('#popup [data-pop-pane="images"]');card.images=await imagePane.textContent();const actualRows=await page.evaluate(id=>window.__chicago4d.popup.picturesDoc.by_structure[id]??[],id);assert.deepEqual(actualRows,plan.expected_picture_rows[id]);card.actualPictureRows=actualRows;
      const held=imagePane.locator('[data-pic]');assert.equal(await held.count(),0,'Current Jail pictures are link-only; no held viewer is claimed');card.viewer='NO_HELD_VIEWER_IN_CURRENT_TARGET_RECORDS';
      if(actualRows.length){const creditEl=imagePane.locator('.pop-pic-list > li').first();await creditEl.scrollIntoViewIfNeeded();const c=await creditEl.evaluate(el=>{const r=el.getBoundingClientRect();let top=0,bottom=innerHeight,left=0,right=innerWidth;for(let p=el.parentElement;p;p=p.parentElement){if(/auto|scroll|hidden|clip/.test(getComputedStyle(p).overflowY+' '+getComputedStyle(p).overflowX)){const q=p.getBoundingClientRect();top=Math.max(top,q.top);bottom=Math.min(bottom,q.bottom);left=Math.max(left,q.left);right=Math.min(right,q.right);}}const a=el.querySelector('a[href]'),b=a?.getBoundingClientRect(),hit=document.elementFromPoint((r.left+r.right)/2,(r.top+r.bottom)/2);return{text:el.textContent,href:a?.href,rect:{top:r.top,bottom:r.bottom,left:r.left,right:r.right},clip:{top,bottom,left,right},visible:r.top>=top&&r.bottom<=bottom&&r.left>=left&&r.right<=right&&!!hit&&el.contains(hit),linkVisible:!!b&&b.top>=top&&b.bottom<=bottom&&b.left>=left&&b.right<=right};});assert(c.visible&&c.linkVisible&&/Trowbridge/.test(c.text)&&/1902/.test(c.text)&&/public domain/i.test(c.text)&&c.href===actualRows[0].url);card.visibleLinkedImageCredit=c;}else assert(card.images.includes('NO PICTURE ON FILE'));
      await page.screenshot({path:path.join(out,id+'-images.jpg'),type:'jpeg',quality:93});}
      cards.push(card);save('ACTUAL-JAIL-CARDS.json',cards);
    }
  }
  phase='qualified-before-teardown';
  for(const list of [errors,network,cancelled,consoleErrors,serverErrors])assert.equal(list.length,0,JSON.stringify(list));guard();save('RESULT.json',{status:'ACTUAL_JAIL_'+leg.toUpperCase()+'_PASS',viewport,head:plan.expected_head,qualified_source_scope_sha256:plan.source_scope_sha256,errors,network,cancelled,consoleErrors,serverErrors,wall_ms:performance.now()-started,no_retry:true,scope:'Actual published Jail/keeper body or cards at this viewport; bounded partial increment. No historical camera calibration, complete photo match or original-ticket closure.'});
} catch(e) {
  failure={message:e.message,stack:e.stack};
  if(page){try{await page.screenshot({path:path.join(out,'FAIL.jpg'),type:'jpeg',quality:90});}catch(x){failure.screenshot_error=x.message;}}
  save('FAILURE.json',{failure,errors,network,cancelled,consoleErrors,serverErrors});
} finally {
  phase='browser-teardown';teardown=true;
  if(context)try{await context.close();}catch(e){failure??={message:e.message};}
  if(browser)try{await browser.close();}catch(e){failure??={message:e.message};}
  if(server.listening)await new Promise(resolve=>server.close(resolve));
  save('REQUEST-TIMELINE.json',requestTimeline);save('CLOSURE.json',{failure,errors,network,cancelled,cleanupCancelled,consoleErrors,serverErrors,no_retry:true,zero_pre_teardown_cancellations:cancelled.length===0});
}
if(failure)process.exitCode=1;
