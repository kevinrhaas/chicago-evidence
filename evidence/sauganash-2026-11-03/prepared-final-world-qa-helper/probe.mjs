/** Actual published partial Sauganash Hotel held Images card and current hotel exterior/arrival per viewport. No source or renderer overrides. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/shared/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const plan = JSON.parse(fs.readFileSync(process.env.SAUG_PROBE_PLAN));
const out = process.env.SAUG_PROBE_OUT, viewport = process.env.SAUG_PROBE_VIEWPORT;
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
    const a = window.__chicago4d, id = 'sauganash_hotel';
    a.popup.close(); a.navigator.dock(); a.travel.stop('Sauganash Hotel Images acceptance'); a.setFly(false); a.confidence.resetGrades(); a.setConfidenceView(false);
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
  save('ACTUAL-SAUG-CARD.json',outcome);
  // Use the actual card's scroll container so the feature being accepted is on screen.
  const imageTab=page.locator('#popup [data-pop-tab="images"]');
  await imageTab.scrollIntoViewIfNeeded(); await imageTab.click();
  await page.locator('#popup [data-pop-pane="images"]').evaluate(el=>el.scrollIntoView({block:'start'}));
  const imageLocator=page.locator('#popup [data-pop-pane="images"] img');
  assert.equal(await imageLocator.count(),plan.expected_held_count,'Native thumbnail count follows actual compiled held rows');
  const loadedImages=[];
  for(let index=0;index<plan.expected_held_count;index++){
    const item=imageLocator.nth(index);await item.scrollIntoViewIfNeeded();
    await item.evaluate(async image=>{const until=Date.now()+60000;while((!image.complete||image.naturalWidth===0)&&Date.now()<until)await new Promise(r=>setTimeout(r,100));if(!image.complete||image.naturalWidth===0)throw Error('Native held picture did not load');});
    const actual=await item.evaluate(image=>{const r=image.getBoundingClientRect();return{src:image.currentSrc,naturalWidth:image.naturalWidth,naturalHeight:image.naturalHeight,rect:{x:r.x,y:r.y,width:r.width,height:r.height},inViewport:r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth};});
    assert(actual.inViewport&&actual.naturalWidth>0,'Genuine held thumbnail loaded through physical card scrolling');loadedImages.push(actual);
  }
  const paneVisibility=await page.locator('#popup [data-pop-pane="images"]').evaluate(p=>{const r=p.getBoundingClientRect();return{width:r.width,height:r.height,inViewport:r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight};});
  assert(paneVisibility.inViewport,'Native credited Images pane is physically visible');
  const visibleImage={expected_held_count:plan.expected_held_count,loadedImages,paneVisibility,no_held_thumbnail_claim:plan.expected_held_count===0};
  save('VISIBLE-IMAGE.json',visibleImage);
  const screenshot=path.join(out,'saug-images.jpg');await page.screenshot({path:screenshot,type:'jpeg',quality:90});
  const screenshotBinding={path:screenshot,sha256:sha(fs.readFileSync(screenshot)),bytes:fs.statSync(screenshot).size};
  assert(outcome.arrived===true&&outcome.framed===true,'Actual Sauganash Hotel arrival/frame');
  assert(outcome.shown&&outcome.srcBefore===0&&outcome.items===plan.expected_picture_count&&outcome.uncredited===0&&outcome.tabCount===String(outcome.items),'Actual credited Images tab with no pre-open image src');
  assert(outcome.missingExpected.length===0,'Every frozen compiled Sauganash Hotel picture row is present');
  assert.deepEqual(outcome.rows,plan.saug_picture_rows,'Actual published picture rows and credits match the frozen plan');
  assert(outcome.after>outcome.before&&outcome.ready&&outcome.welcome==='world'&&!outcome.contextLost&&outcome.detail==='full','Actual usable full-detail native frame');
  assert(outcome.signature.litFraction>0.05&&Number.isFinite(outcome.signature.mean),'Actual native readback contains a real frame');
  assert.equal(errors.length, 0, JSON.stringify(errors)); assert.equal(network.length, 0, JSON.stringify(network)); assert.equal(consoleErrors.length, 0, JSON.stringify(consoleErrors)); assert.equal(serverErrors.length, 0, JSON.stringify(serverErrors));
  assert(outcome.rows.length===plan.expected_picture_count&&outcome.rows.filter(r=>r.held).length===plan.expected_held_count,'Actual held/link counts match the frozen native compiled card');
  save('SAUG-CARD-RESULT.json', {outcome,visibleImage,screenshot:screenshotBinding});
  const rt=page.locator('#popup [data-pop-tab="record"]');await rt.scrollIntoViewIfNeeded();await rt.click();const sum=page.locator('#popup [data-pop-pane="record"] details.research summary');await sum.scrollIntoViewIfNeeded();await sum.click();
  const record=await page.evaluate(()=>{const p=document.querySelector('#popup [data-pop-pane="record"]');return {shown:!p.hidden,open:p.querySelector('details.research').open,text:p.querySelector('.research-body').textContent};});assert(record.shown&&record.open);assert.equal(record.text,plan.expected_research_note);assert(/Andreas.?s\s+1884\s+engraving/i.test(record.text)&&/is now held on this hotel.?s Images tab/i.test(record.text)&&/roof shapes.*remain under review/is.test(record.text),'Current native Record states held Andreas engraving and remaining hotel shape review');save('SAUG-NATIVE-READER.json',record);await page.locator('#popup [data-pop-pane="record"] .research-body').evaluate(el=>el.scrollIntoView({block:'end'}));const currentNote=await page.evaluate(()=>{const el=document.querySelector('#popup [data-pop-pane="record"] .research-body'),w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const i=n.textContent.indexOf("Andreas's 1884 engraving");if(i>=0){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+"Andreas's 1884 engraving".length);const q=r.getBoundingClientRect();return {x:q.x,y:q.y,width:q.width,height:q.height,visible:q.width>0&&q.height>0&&q.top>=0&&q.bottom<=innerHeight};}}return {visible:false};});assert(currentNote.visible,'Current Andreas paragraph is physically visible after native card scroll');save('SAUG-CURRENT-READER-VISIBLE.json',currentNote);await page.screenshot({path:path.join(out,'saug-record.jpg'),type:'jpeg',quality:92});await page.evaluate(()=>window.__chicago4d.popup.close());
  // Trusted native skyclick only; no DOM/style hiding of the look hint.
  await page.mouse.click(mobile?195:640,mobile?250:180);save('NATIVE-LOOK-STATE.json',await page.evaluate(()=>({pointerLock:document.pointerLockElement?.tagName??null})));
  // Curated flying inspection uses the native walker; the renderer remains its owner.
  saugExterior = await page.evaluate(async reference => {
    const a=window.__chicago4d,id='sauganash_hotel';
    a.popup.close();a.navigator.dock();a.travel.stop('Sauganash Hotel exterior inspection');
    a.confidence.resetGrades();a.setConfidenceView(false);a.setFly(true);a.walker.setFlying(true);
    const box=a.buildings.instanceBounds()[id],matrix=a.buildings.matrixOf(id),anchor=a.buildings.matrixOf('sauganash_hotel');
    const missing=a.buildings.missing?.has?.(id);
    if(missing!==false||!box||!matrix||!anchor)throw Error('Missing real Sauganash Hotel/Sauganash Hotel geometry or transform');
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
      const roof=Math.max(...corners.map(p=>p[1]));const lift=Math.max(0,Math.max(ground+2,roof+2)-eye[1]);eye[1]+=lift;
      const de=center[0]-eye[0],dn=eye[2]-center[2],rise=center[1]-eye[1];
      const yaw=(Math.atan2(de,dn)*180/Math.PI+360)%360,pitch=Math.atan2(rise,Math.hypot(de,dn))*180/Math.PI;
      placement={local_e:eye[0],local_n:-eye[2],yaw_deg:yaw,pitch_deg:pitch,altitude_m:eye[1]-ground};
      a.walker.teleport(placement);
      // Native step applies the teleported camera/projection matrices before fit measurements.
      a.step();
      projected=corners.map(p=>({world:p,ndc:a.project(p[0],-p[2],p[1])}));
      if(projected.every(p=>Number.isFinite(p.ndc.x)&&Number.isFinite(p.ndc.y)&&p.ndc.z>=-1&&p.ndc.z<=1&&Math.abs(p.ndc.x)<=0.96&&Math.abs(p.ndc.y)<=0.96))break;
      distance*=1.2;
    }
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return {id,missing,box,matrix:m,anchor_matrix:am,reference_eye_enu:reference.eye,reference_world_eye:referenceEye,reference_direction_only:true,center,direction,radius,distance,placement,projected,
      actual_walker:{...a.walker.state},camera_world:a.camera.position.toArray(),before,after:a.renderer.info.render.frame,signature,ready:a.ready,welcome:a.welcome.state,
      contextLost:a.renderer.getContext().isContextLost(),detail:a.detail,flying:a.walker.state.flying,
      scope:'Curated current in-app flying exterior inspection; not a calibrated source camera, historical visitor pose, picture-match verdict or obstruction-free claim.'};
  },plan.saug_reference_camera);
  save('SAUG-EXTERIOR.json',saugExterior);
  assert(saugExterior.missing===false&&saugExterior.flying&&saugExterior.ready&&saugExterior.welcome==='world'&&!saugExterior.contextLost&&saugExterior.detail==='full','Actual full-detail Sauganash Hotel exterior');
  assert(saugExterior.projected.length===8&&saugExterior.projected.every(p=>Number.isFinite(p.ndc.x)&&Number.isFinite(p.ndc.y)&&p.ndc.z>=-1&&p.ndc.z<=1&&Math.abs(p.ndc.x)<=0.96&&Math.abs(p.ndc.y)<=0.96),'Eight actual rendered Sauganash Hotel corners fit the unchanged frustum');
  assert(saugExterior.after>saugExterior.before&&saugExterior.signature.litFraction>0.05&&Number.isFinite(saugExterior.signature.mean),'Actual Sauganash Hotel native readback');
  await page.waitForFunction(frame=>{const a=window.__chicago4d;if(!a.ready||a.welcome.state!=='world'||document.visibilityState!=='visible'||a.renderer.getContext().isContextLost())throw Error('Curated inspection world readiness changed');return a.renderer.info.render.frame>=frame+3;},saugExterior.after,{timeout:180000,polling:500});
  saugExterior.settled_frame=await page.evaluate(()=>window.__chicago4d.renderer.info.render.frame);
  const exteriorFile=path.join(out,'saug-exterior.jpg');await page.screenshot({path:exteriorFile,type:'jpeg',quality:92});
  saugExterior.screenshot={path:exteriorFile,sha256:sha(fs.readFileSync(exteriorFile)),bytes:fs.statSync(exteriorFile).size};save('SAUG-EXTERIOR.json',saugExterior);
  const byGrade=await page.evaluate(async()=>{const a=window.__chicago4d;a.setConfidenceView(true);const before=a.renderer.info.render.frame,p=a.capture(12);a.step();const signature=await p;return {enabled:a.confidenceView,before,after:a.renderer.info.render.frame,signature,stats:a.stats()};});assert(byGrade.enabled&&byGrade.after>byGrade.before&&byGrade.stats.withinBudget);save('SAUG-BYGRADE.json',byGrade);await page.screenshot({path:path.join(out,'saug-exterior-ByGrade.jpg'),type:'jpeg',quality:92});await page.evaluate(()=>window.__chicago4d.setConfidenceView(false));
  saugArrival=await page.evaluate(async entrance=>{
    const a=window.__chicago4d,id='sauganash_hotel';a.popup.close();a.navigator.dock();a.travel.stop('Sauganash Hotel native arrival');a.setFly(false);a.confidence.resetGrades();a.setConfidenceView(false);
    const arrived=a.spawnAtDestination({kind:'structure',id}),framed=a.frame(id,{card:false});
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return {id,arrived,framed,missing:a.buildings.missing.has(id),position:{...a.walker.state},camera_world:a.camera.position.toArray(),entrance,
      horizontal_distance_to_entrance_m:Math.hypot(a.walker.state.e-entrance.at_local_enu_m[0],a.walker.state.n-entrance.at_local_enu_m[1]),before,after:a.renderer.info.render.frame,signature,
      ready:a.ready,welcome:a.welcome.state,contextLost:a.renderer.getContext().isContextLost(),detail:a.detail,flying:a.walker.state.flying,
      scope:'Native public structure spawnAtDestination followed by frame(card:false). No walking through the door, full-bbox framing, absence of foreground occlusion, or whole-compound image acceptance is claimed.'};
  },plan.saug_entrance);
  save('SAUG-ARRIVAL.json',saugArrival);
  assert(saugArrival.arrived===true&&saugArrival.framed===true&&saugArrival.missing===false&&!saugArrival.flying&&saugArrival.ready&&saugArrival.welcome==='world'&&!saugArrival.contextLost&&saugArrival.detail==='full','Actual native Sauganash Hotel arrival');
  assert(saugArrival.after>saugArrival.before&&saugArrival.signature.litFraction>0.05&&Number.isFinite(saugArrival.signature.mean),'Actual arrival native readback');
  const arrivalFile=path.join(out,'saug-arrival.jpg');await page.screenshot({path:arrivalFile,type:'jpeg',quality:92});
  saugArrival.screenshot={path:arrivalFile,sha256:sha(fs.readFileSync(arrivalFile)),bytes:fs.statSync(arrivalFile).size};save('SAUG-ARRIVAL.json',saugArrival);
  assert.equal(errors.length,0,JSON.stringify(errors));assert.equal(network.length,0,JSON.stringify(network));assert.equal(consoleErrors.length,0,JSON.stringify(consoleErrors));assert.equal(serverErrors.length,0,JSON.stringify(serverErrors));
  const entry=await page.evaluate(async door=>{const a=window.__chicago4d,b=door.bearing_deg*Math.PI/180,rows=[];a.popup.close();a.setFly(false);for(const distance of[3,2]){const e=door.at_local_enu_m[0]+Math.sin(b)*distance,n=door.at_local_enu_m[1]+Math.cos(b)*distance;a.walker.teleport({local_e:e,local_n:n,yaw_deg:(door.bearing_deg+180)%360});a.step();rows.push({distance,e,n,blocked:a.router.blockedAt(e,n),water:a.terrain.isWater(e,n),surface:a.walker.surfaceAt(e,n),ground:a.walker.state.groundY,eye:a.walker.state.eyeY,actualE:a.walker.state.e,actualN:a.walker.state.n,flying:a.walker.state.flying,hudFlying:a.hud.flying,intentFlying:a.intent.flying});}const before=a.renderer.info.render.frame,p=a.capture(12);a.step();const signature=await p;return {door,rows,before,after:a.renderer.info.render.frame,signature};},plan.saug_entrance);assert(entry.after>entry.before);for(const x of entry.rows){assert(!x.blocked&&!x.water&&!x.flying&&!x.hudFlying&&!x.intentFlying);assert(Math.abs(x.ground-x.surface)<1e-6&&x.eye>x.ground&&Math.hypot(x.actualE-x.e,x.actualN-x.n)<.01);}save('SAUG-NATIVE-ENTRY.json',entry);await page.screenshot({path:path.join(out,'saug-native-front-entry.jpg'),type:'jpeg',quality:92});
  guard();
  save('RESULT.json', { status: 'ACTUAL_FINAL_SAUGANASH_PASS', viewport, head: plan.expected_head, qualified_source_scope_sha256: plan.source_scope_sha256, outcome, visibleImage, screenshot: screenshotBinding, saugExterior, saugArrival, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true, scope: 'Actual Sauganash Hotel credited visible Images pane; Sauganash Hotel curated bbox exterior and native arrival. Native readbacks and screenshots, no whole-body/full-size viewer/door traversal/historical-camera/full-Green-Tree signoff claim' });
} catch (e) {
  failure = { message: e.message, stack: e.stack };
  const settleFile = path.join(out, 'WORLD-SETTLE.json');
  if (fs.existsSync(settleFile)) { const settle = JSON.parse(fs.readFileSync(settleFile)); if (settle.status === 'WAITING') save('WORLD-SETTLE.json', { ...settle, status: 'FAIL', failure }); }
  if (page) { try { await page.screenshot({ path: path.join(out, 'FAIL.jpg'), type: 'jpeg', quality: 90 }); } catch (captureError) { failure.screenshot_error = captureError.message; } }
  save('FAIL.json', { status: 'ACTUAL_PUBLISHED_SAUGANASH_FAIL', viewport, failure, outcome, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, no_retry: true });
} finally {
  if (browser) await browser.close().catch(e => { serverErrors.push(e.message); failure ??= { close_error: e.message }; });
  server.closeAllConnections?.(); await new Promise(resolve => server.close(resolve));
  try { guard(); save('SELECTED-INPUT-CLOSURE.json', { unchanged: true }); } catch (e) { save('SELECTED-INPUT-CLOSURE.json', { unchanged: false, error: e.message }); failure ??= { guard_error: e.message }; }
  save('CLOSURE.json', { failure, errors, network, cancelled, consoleErrors, serverErrors, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true });
}
if (failure) process.exitCode = 1;
