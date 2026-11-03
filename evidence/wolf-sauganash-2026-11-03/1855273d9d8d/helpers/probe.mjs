/** Actual published Wolf Images card and Sauganash exterior/arrival per viewport. No source or renderer overrides. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/shared/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const plan = JSON.parse(fs.readFileSync(process.env.WOLF_PROBE_PLAN));
const out = process.env.WOLF_PROBE_OUT, viewport = process.env.WOLF_PROBE_VIEWPORT;
assert(['desktop', 'mobile'].includes(viewport)); assert(out); fs.mkdirSync(out);
const mobile = viewport === 'mobile', root = plan.site_parent;
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const save = (name, value) => fs.writeFileSync(path.join(out, name), JSON.stringify(value, null, 2) + '\n');
const errors = [], network = [], cancelled = [], consoleErrors = [], serverErrors = [];
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
let browser, context, page, outcome = null, saugExterior = null, saugArrival = null, failure = null;
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
  page.on('requestfailed', r => (r.failure()?.errorText === 'net::ERR_ABORTED' ? cancelled : network).push({ url: r.url(), failure: r.failure() }));
  page.on('response', r => { if (r.status() >= 400) network.push({ url: r.url(), status: r.status() }); });
  await context.addInitScript(() => { localStorage.setItem('chicago4d.researcher', 'on'); localStorage.setItem('chicago4d.settings', JSON.stringify({ detail: 'full' })); });
  assert.equal((await page.goto(`http://127.0.0.1:${server.address().port}/4d/walk/index.html?year=1835&keep-geometry=1`)).status(), 200);
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
  outcome = await page.evaluate(async expected => {
    const a = window.__chicago4d, id = 'wolf_point_tavern';
    a.popup.close(); a.navigator.dock(); a.travel.stop('Wolf Images acceptance'); a.setFly(false); a.confidence.resetGrades(); a.setConfidenceView(false);
    const arrived = a.spawnAtDestination({kind:'structure',id}), framed = a.frame(id, {card:false});
    a.pick(id);
    document.querySelector('#popup [data-pop-tab="evidence"]')?.click();
    const pane = () => document.querySelector('#popup [data-pop-pane="images"]');
    const deadline = Date.now()+20000;
    const actualRows = () => a.popup.picturesDoc?.by_structure?.[id] ?? [];
    while (Date.now()<deadline && (expected.some(e=>!actualRows().some(r=>r.id===e)) || /LOADING IMAGE INDEX/.test(pane()?.textContent ?? 'LOADING IMAGE INDEX'))) await new Promise(r=>setTimeout(r,100));
    if (expected.some(e=>!actualRows().some(r=>r.id===e))) throw Error('Expected native picture rows did not become ready');
    const srcBefore = pane()?.querySelectorAll('img[src]').length ?? -1;
    document.querySelector('#popup [data-pop-tab="images"]')?.click();
    const p = pane(), doc = a.popup.picturesDoc;
    const rows = doc?.by_structure?.[id] ?? [];
    const items = [...(p?.querySelectorAll('.pop-pic-list li, .pop-pic-tile') ?? [])];
    const imageRows=items.map(el=>({text:el.textContent.trim(),credit:el.querySelector('.pop-pic-meta, .pop-pic-tile-credit')?.textContent.trim()??'',href:el.querySelector('a')?.href??null}));
    const missingExpected=expected.filter(id=>!rows.some(p=>p.id===id));
    const before=a.renderer.info.render.frame;
    const pending=a.capture(12);a.step();const signature=await pending;
    return {id,arrived,framed,shown:!!p&&!p.hasAttribute('hidden'),srcBefore,rows,imageRows,items:items.length,missingExpected,
      uncredited:imageRows.filter(x=>!x.credit).length,tabCount:document.querySelector('#popup [data-pop-tab="images"] .pop-count')?.textContent.trim()??'',
      noHistoricalSpots:rows.filter(p=>expected.includes(p.id)).every(p=>!p.spot),before,after:a.renderer.info.render.frame,signature,
      ready:a.ready,welcome:a.welcome.state,contextLost:a.renderer.getContext().isContextLost(),detail:a.detail};
  }, plan.expected_picture_ids);
  save('ACTUAL-WOLF-CARD.json',outcome);
  // Use the actual card's scroll container so the feature being accepted is on screen.
  const imageTab=page.locator('#popup [data-pop-tab="images"]');
  await imageTab.scrollIntoViewIfNeeded(); await imageTab.click();
  await page.locator('#popup [data-pop-pane="images"]').evaluate(el=>el.scrollIntoView({block:'start'}));
  await page.waitForFunction(()=>{
    const pane=document.querySelector('#popup [data-pop-pane="images"]');
    const imgs=[...(pane?.querySelectorAll('img')??[])];
    return imgs.length===1&&imgs.every(img=>img.complete&&img.naturalWidth>0);
  },null,{timeout:60000,polling:250});
  const visibleImage=await page.locator('#popup [data-pop-pane="images"] img').evaluate(el=>{
    const r=el.getBoundingClientRect();return {src:el.currentSrc,naturalWidth:el.naturalWidth,naturalHeight:el.naturalHeight,rect:{x:r.x,y:r.y,width:r.width,height:r.height},inViewport:r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth};
  });
  assert(visibleImage.inViewport&&visibleImage.naturalWidth>0,'Actual held thumbnail loaded and is visible');
  save('VISIBLE-IMAGE.json',visibleImage);
  const screenshot=path.join(out,'wolf-images.jpg');await page.screenshot({path:screenshot,type:'jpeg',quality:90});
  const screenshotBinding={path:screenshot,sha256:sha(fs.readFileSync(screenshot)),bytes:fs.statSync(screenshot).size};
  assert(outcome.arrived===true&&outcome.framed===true,'Actual Wolf arrival/frame');
  assert(outcome.shown&&outcome.srcBefore===0&&outcome.items>=6&&outcome.uncredited===0&&outcome.tabCount===String(outcome.items),'Actual credited Images tab with no pre-open image src');
  assert(outcome.missingExpected.length===0&&outcome.noHistoricalSpots,'Seven reviewed diagnostic views join six credited sources without invented historical camera spots');
  assert(outcome.after>outcome.before&&outcome.ready&&outcome.welcome==='world'&&!outcome.contextLost&&outcome.detail==='full','Actual usable full-detail native frame');
  assert(outcome.signature.litFraction>0.05&&Number.isFinite(outcome.signature.mean),'Actual native readback contains a real frame');
  assert.equal(errors.length, 0, JSON.stringify(errors)); assert.equal(network.length, 0, JSON.stringify(network)); assert.equal(consoleErrors.length, 0, JSON.stringify(consoleErrors)); assert.equal(serverErrors.length, 0, JSON.stringify(serverErrors));
  assert(outcome.rows.length===6&&outcome.rows.filter(r=>r.held).length===1&&outcome.rows.filter(r=>!r.held).length===5,'Actual Wolf card is one held image and five credited links');
  save('WOLF-RESULT.json', {outcome,visibleImage,screenshot:screenshotBinding});
  // Curated flying inspection uses the native walker; the renderer remains its owner.
  saugExterior = await page.evaluate(async reference => {
    const a=window.__chicago4d,id='sauganash_hotel';
    a.popup.close();a.navigator.dock();a.travel.stop('Sauganash exterior inspection');
    a.confidence.resetGrades();a.setConfidenceView(false);a.setFly(true);a.walker.setFlying(true);
    const box=a.buildings.instanceBounds()[id],matrix=a.buildings.matrixOf(id),anchor=a.buildings.matrixOf('philo_carpenter_log_shop');
    const missing=a.buildings.missing?.has?.(id);
    if(missing!==false||!box||!matrix||!anchor)throw Error('Missing real Sauganash/Carpenter geometry or transform');
    const transform=(p,m)=>{
      const w=m[3]*p[0]+m[7]*p[1]+m[11]*p[2]+m[15];
      return [(m[0]*p[0]+m[4]*p[1]+m[8]*p[2]+m[12])/w,(m[1]*p[0]+m[5]*p[1]+m[9]*p[2]+m[13])/w,(m[2]*p[0]+m[6]*p[1]+m[10]*p[2]+m[14])/w];
    };
    const m=[...matrix.elements],am=[...anchor.elements],corners=[];
    for(const x of [box.min[0],box.max[0]])for(const y of [box.min[1],box.max[1]])for(const z of [box.min[2],box.max[2]])corners.push(transform([x,y,z],m));
    const center=transform(box.min.map((v,i)=>(v+box.max[i])/2),m);
    const referenceEye=transform([reference.eye[0],reference.eye[2],-reference.eye[1]],am);
    const delta=referenceEye.map((v,i)=>v-center[i]),length=Math.hypot(...delta),direction=delta.map(v=>v/length);
    if(!Number.isFinite(length)||length<=0)throw Error('Invalid reference-derived inspection direction');
    const radius=Math.max(...corners.map(p=>Math.hypot(...p.map((v,i)=>v-center[i]))));
    const vfov=(a.camera.getEffectiveFOV?.()??a.camera.fov)*Math.PI/180,aspect=a.camera.aspect;
    if(!(radius>0&&vfov>0&&vfov<Math.PI&&aspect>0))throw Error('Invalid real bounds or camera frustum');
    const half=Math.min(vfov/2,Math.atan(Math.tan(vfov/2)*aspect));
    let distance=radius/Math.sin(half)*1.15,placement=null,projected=null;
    for(let attempt=0;attempt<6;attempt++){
      const eye=center.map((v,i)=>v+direction[i]*distance),ground=a.walker.surfaceAt(eye[0],-eye[2]);
      // Clearance is an explicit curated inspection choice, never a source-camera fit.
      const lift=Math.max(0,ground+2-eye[1]);eye[1]+=lift;
      const de=center[0]-eye[0],dn=eye[2]-center[2],rise=center[1]-eye[1];
      const yaw=(Math.atan2(de,dn)*180/Math.PI+360)%360,pitch=Math.atan2(rise,Math.hypot(de,dn))*180/Math.PI;
      placement={local_e:eye[0],local_n:-eye[2],yaw_deg:yaw,pitch_deg:pitch,altitude_m:eye[1]-ground};
      a.walker.teleport(placement);
      projected=corners.map(p=>({world:p,ndc:a.project(p[0],-p[2],p[1])}));
      if(projected.every(p=>Number.isFinite(p.ndc.x)&&Number.isFinite(p.ndc.y)&&p.ndc.z>=-1&&p.ndc.z<=1&&Math.abs(p.ndc.x)<=0.96&&Math.abs(p.ndc.y)<=0.96))break;
      distance*=1.2;
    }
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return {id,missing,box,matrix:m,anchor_matrix:am,reference_eye_enu:reference.eye,reference_world_eye:referenceEye,center,direction,radius,distance,placement,projected,
      actual_walker:{...a.walker.state},camera_world:a.camera.position.toArray(),before,after:a.renderer.info.render.frame,signature,ready:a.ready,welcome:a.welcome.state,
      contextLost:a.renderer.getContext().isContextLost(),detail:a.detail,flying:a.walker.state.flying,
      scope:'Curated current in-app flying exterior inspection; not a calibrated source camera, historical visitor pose, picture-match verdict or obstruction-free claim.'};
  },plan.saug_reference_camera);
  save('SAUG-EXTERIOR.json',saugExterior);
  assert(saugExterior.missing===false&&saugExterior.flying&&saugExterior.ready&&saugExterior.welcome==='world'&&!saugExterior.contextLost&&saugExterior.detail==='full','Actual full-detail Sauganash exterior');
  assert(saugExterior.projected.length===8&&saugExterior.projected.every(p=>Number.isFinite(p.ndc.x)&&Number.isFinite(p.ndc.y)&&p.ndc.z>=-1&&p.ndc.z<=1&&Math.abs(p.ndc.x)<=0.96&&Math.abs(p.ndc.y)<=0.96),'Eight actual rendered Sauganash corners fit the unchanged frustum');
  assert(saugExterior.after>saugExterior.before&&saugExterior.signature.litFraction>0.05&&Number.isFinite(saugExterior.signature.mean),'Actual Sauganash native readback');
  await page.waitForFunction(frame=>{const a=window.__chicago4d;if(!a.ready||a.welcome.state!=='world'||document.visibilityState!=='visible'||a.renderer.getContext().isContextLost())throw Error('Curated inspection world readiness changed');return a.renderer.info.render.frame>=frame+3;},saugExterior.after,{timeout:180000,polling:500});
  saugExterior.settled_frame=await page.evaluate(()=>window.__chicago4d.renderer.info.render.frame);
  const exteriorFile=path.join(out,'saug-exterior.jpg');await page.screenshot({path:exteriorFile,type:'jpeg',quality:92});
  saugExterior.screenshot={path:exteriorFile,sha256:sha(fs.readFileSync(exteriorFile)),bytes:fs.statSync(exteriorFile).size};save('SAUG-EXTERIOR.json',saugExterior);
  saugArrival=await page.evaluate(async entrance=>{
    const a=window.__chicago4d,id='sauganash_hotel';a.popup.close();a.navigator.dock();a.travel.stop('Sauganash native arrival');a.setFly(false);a.confidence.resetGrades();a.setConfidenceView(false);
    const arrived=a.spawnAtDestination({kind:'structure',id}),framed=a.frame(id,{card:false});
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return {id,arrived,framed,missing:a.buildings.missing.has(id),position:{...a.walker.state},camera_world:a.camera.position.toArray(),entrance,
      horizontal_distance_to_entrance_m:Math.hypot(a.walker.state.e-entrance.at_local_enu_m[0],a.walker.state.n-entrance.at_local_enu_m[1]),before,after:a.renderer.info.render.frame,signature,
      ready:a.ready,welcome:a.welcome.state,contextLost:a.renderer.getContext().isContextLost(),detail:a.detail,flying:a.walker.state.flying,
      scope:'Native public structure spawnAtDestination followed by frame(card:false). No walking through the door, full-bbox framing, absence of foreground occlusion, or whole-hotel image acceptance is claimed.'};
  },plan.saug_entrance);
  save('SAUG-ARRIVAL.json',saugArrival);
  assert(saugArrival.arrived===true&&saugArrival.framed===true&&saugArrival.missing===false&&!saugArrival.flying&&saugArrival.ready&&saugArrival.welcome==='world'&&!saugArrival.contextLost&&saugArrival.detail==='full','Actual native Sauganash arrival');
  assert(saugArrival.after>saugArrival.before&&saugArrival.signature.litFraction>0.05&&Number.isFinite(saugArrival.signature.mean),'Actual arrival native readback');
  const arrivalFile=path.join(out,'saug-arrival.jpg');await page.screenshot({path:arrivalFile,type:'jpeg',quality:92});
  saugArrival.screenshot={path:arrivalFile,sha256:sha(fs.readFileSync(arrivalFile)),bytes:fs.statSync(arrivalFile).size};save('SAUG-ARRIVAL.json',saugArrival);
  assert.equal(errors.length,0,JSON.stringify(errors));assert.equal(network.length,0,JSON.stringify(network));assert.equal(consoleErrors.length,0,JSON.stringify(consoleErrors));assert.equal(serverErrors.length,0,JSON.stringify(serverErrors));
  guard();
  save('RESULT.json', { status: 'ACTUAL_PUBLISHED_COMBINED_WOLF_SAUG_PASS', viewport, head: plan.expected_head, qualified_source_scope_sha256: plan.source_scope_sha256, outcome, visibleImage, screenshot: screenshotBinding, saugExterior, saugArrival, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true, scope: 'Actual Wolf credited visible Images pane; Sauganash curated bbox exterior and native arrival. Native readbacks and screenshots, no whole-body/full-size viewer/door traversal/historical-camera/full-hotel signoff claim' });
} catch (e) {
  failure = { message: e.message, stack: e.stack };
  const settleFile = path.join(out, 'WORLD-SETTLE.json');
  if (fs.existsSync(settleFile)) { const settle = JSON.parse(fs.readFileSync(settleFile)); if (settle.status === 'WAITING') save('WORLD-SETTLE.json', { ...settle, status: 'FAIL', failure }); }
  if (page) { try { await page.screenshot({ path: path.join(out, 'FAIL.jpg'), type: 'jpeg', quality: 90 }); } catch (captureError) { failure.screenshot_error = captureError.message; } }
  save('FAIL.json', { status: 'ACTUAL_PUBLISHED_COMBINED_WOLF_SAUG_FAIL', viewport, failure, outcome, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, no_retry: true });
} finally {
  if (browser) await browser.close().catch(e => { serverErrors.push(e.message); failure ??= { close_error: e.message }; });
  server.closeAllConnections?.(); await new Promise(resolve => server.close(resolve));
  try { guard(); save('SELECTED-INPUT-CLOSURE.json', { unchanged: true }); } catch (e) { save('SELECTED-INPUT-CLOSURE.json', { unchanged: false, error: e.message }); failure ??= { guard_error: e.message }; }
  save('CLOSURE.json', { failure, errors, network, cancelled, consoleErrors, serverErrors, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true });
}
if (failure) process.exitCode = 1;
