/** Actual published1812 First Fort NE house evidence/one Currey source link, zero held pictures card and current pyramidroof exterior/arrival per viewport. No source or renderer overrides. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/shared/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const plan = JSON.parse(fs.readFileSync(process.env.FORT_PROBE_PLAN));
const out = process.env.FORT_PROBE_OUT, viewport = process.env.FORT_PROBE_VIEWPORT;
const leg = process.env.FORT_PROBE_LEG; assert(['cards', 'body'].includes(leg));
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
let browser, context, page, outcome = null, fortExterior = null, fortArrival = null, visibleImage = null, screenshotBinding = null, failure = null;
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
  assert.equal((await page.goto(`http://127.0.0.1:${server.address().port}/4d/walk/index.html?year=1812`)).status(), 200);
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
  // A real delegated surface must exist, not merely disappear from a counter.
  // Use the application's GPU ray picker: phone geometry arrays are released
  // after upload, so a CPU proxy or a sidecar footprint is not presence proof.
  const parade = await page.evaluate(async () => {
    const a = window.__chicago4d;
    const id = 'first_fort_dearborn_parade', owner = 'first_fort_dearborn_parade_ground';
    const rows = a.yards?.interiors?.filter(i => i.record === owner && i.treatment === 'trodden_earth') ?? [];
    if (rows.length !== 1) throw Error('Actual native parade ground owner/interior missing');
    const interior = rows[0], at = interior.at;
    if (!Array.isArray(at) || at.length !== 2 || !at.every(Number.isFinite)) throw Error('Actual parade interior has no finite native sample');
    if (a.yards.group.parent !== a.scene3d || a.yards.treatmentAt(...at) !== 'trodden_earth') throw Error('Parade ground is not mounted with the native treatment');
    const THREE = await import('three');
    const { gpuPick } = await import(new URL('./js/gpu-pick.js', location.href).href);
    a.yards.group.updateWorldMatrix(true, true);
    const candidates = [];
    a.yards.group.traverse(o => {
      if (!o.isMesh || !(o.geometry?.getAttribute('position')?.count >= 3)) return;
      let troddenEarth = false;
      for (let p = o; p; p = p.parent) {
        if (p.visible === false) return;
        if (p.name === 'yard-trodden_earth') troddenEarth = true;
      }
      if (troddenEarth) candidates.push(o);
    });
    if (!candidates.length) throw Error('Native ground owner has no drawable geometry');
    const surface = a.walker.surfaceAt(at[0], at[1]);
    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 40);
    camera.position.set(at[0], surface + 20, -at[1]);
    camera.up.set(0, 0, -1); camera.lookAt(at[0], surface, -at[1]);
    camera.updateProjectionMatrix(); camera.updateMatrixWorld(true);
    const hit = gpuPick(candidates, { x: 0, y: 0 }, camera, 40);
    if (!hit || !Number.isFinite(hit.distance) || !hit.point?.toArray().every(Number.isFinite)) throw Error('Native GPU ray missed the actual parade ground');
    if (Math.abs(hit.point.x - at[0]) > 0.01 || Math.abs(hit.point.z + at[1]) > 0.01) throw Error('Native parade ray answered a different location');
    return { id, owner, interior: { id: interior.id, record: interior.record, treatment: interior.treatment, at, points: interior.pts.length },
      roll: a.buildings.roll, missing: a.buildings.missing.has(id), hasBuildingBox: !!a.buildings.instanceBounds()[id],
      actualGroundCandidates: candidates.length, nativeRay: { mesh: hit.object.name, treatment: 'trodden_earth', point: hit.point.toArray(), distance: hit.distance },
      scope: 'Existing native ground geometry, mounted owner and actual GPU ray hit. No fabricated building box/standing count or historical-camera claim.' };
  });
  assert.equal(parade.roll.delegatedGround[parade.id], parade.owner);
  assert.equal(parade.missing, false); assert.equal(parade.hasBuildingBox, false);
  assert.equal(parade.roll.standing, parade.roll.expected);
  save('FORT-PARADE-GROUND-PRESENCE.json', parade);
  if (leg === 'cards') {
  outcome = await page.evaluate(async expected => {
    const a=window.__chicago4d,id='first_fort_dearborn_small_house_ne';
    a.popup.close();a.navigator.dock();a.travel.stop('First Fort NE evidence inspection');a.setFly(false);a.confidence.resetGrades();a.setConfidenceView(false);
    const arrived=a.spawnAtDestination({kind:'structure',id}),framed=a.frame(id,{card:false});a.pick(id);
    document.querySelector('#popup [data-pop-tab="images"]')?.click();
    const end=Date.now()+20000;
    while(Date.now()<end&&(!a.popup.picturesDoc||/LOADING IMAGE INDEX/i.test(document.querySelector('#popup [data-pop-pane="images"]')?.textContent??'')))await new Promise(r=>setTimeout(r,100));
    if(!a.popup.picturesDoc?.by_structure)throw Error('Actual1812 picture index did not finish loading');
    const p=document.querySelector('#popup [data-pop-pane="images"]'),rows=a.popup.picturesDoc?.by_structure?.[id]??[];
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return {id,arrived,framed,rows,shown:!!p&&!p.hidden,imageCount:p?.querySelectorAll('img[src]').length??0,links:[...(p?.querySelectorAll('a[href]')??[])].map(a=>a.href),text:p?.textContent??'',before,after:a.renderer.info.render.frame,signature,ready:a.ready,welcome:a.welcome.state,contextLost:a.renderer.getContext().isContextLost(),detail:a.detail};
  },plan.expected_picture_ids);
  assert(outcome.arrived&&outcome.framed&&outcome.shown&&outcome.ready&&outcome.welcome==='world'&&!outcome.contextLost&&outcome.detail==='full');
  assert.deepEqual(outcome.rows,plan.fort_picture_rows,'Exact NE picture rows preserved; no Currey card-member or grade promotion');
  assert.equal(outcome.imageCount,plan.expected_held_count);assert.equal(outcome.rows.length,1);assert(outcome.rows.every(r=>!r.held&&!r.spot));assert(/Currey/.test(outcome.text)&&/1912/.test(outcome.text)&&outcome.links.includes(plan.fort_picture_rows[0].url),'Actual credited Currey1912 link without held derivative or historical Spot');
  assert(outcome.after>outcome.before&&outcome.signature.litFraction>0.05&&Number.isFinite(outcome.signature.mean));
  await page.locator('#popup [data-pop-pane="images"]').evaluate(el=>el.scrollIntoView({block:'start'}));
  await page.screenshot({path:path.join(out,'fort-images.jpg'),type:'jpeg',quality:92});
  const recordTab=page.locator('#popup [data-pop-tab="record"]');await recordTab.scrollIntoViewIfNeeded();await recordTab.click();
  const summary=page.locator('#popup [data-pop-pane="record"] details.research summary');await summary.scrollIntoViewIfNeeded();await summary.click();
  const reader=await page.evaluate(()=>{const p=document.querySelector('#popup [data-pop-pane="record"]');return {shown:!p.hidden,open:p.querySelector('details.research').open,text:p.querySelector('.research-body').textContent};});
  assert(reader.shown&&reader.open);assert.equal(reader.text,plan.expected_research_note);save('FORT-RECORD.json',reader);
  await page.locator('#popup [data-pop-pane="record"] .research-body').evaluate(el=>el.scrollIntoView({block:'start'}));
  await page.screenshot({path:path.join(out,'fort-record.jpg'),type:'jpeg',quality:92});
  const evidenceTab=page.locator('#popup [data-pop-tab="evidence"]');await evidenceTab.scrollIntoViewIfNeeded();await evidenceTab.click();
  const roof=page.locator('#popup [data-pop-pane="evidence"] .attrs tr').filter({has:page.locator('th',{hasText:/^roof type$/i})});
  assert.equal(await roof.count(),1);await roof.locator('[data-toggle-note]').click();
  const actualRoof=await roof.evaluate(el=>({text:el.textContent,open:el.querySelector('[data-note]')?.hidden===false,grade:el.querySelector('.chip')?.textContent??''}));
  assert(actualRoof.open&&/pyramid/i.test(actualRoof.text)&&/inferred/i.test(actualRoof.text)&&/1912/.test(actualRoof.text)&&/1808/.test(actualRoof.text)&&/diagnostic/i.test(actualRoof.text));
  await roof.evaluate(el=>el.scrollIntoView({block:'start'}));save('FORT-ROOF-EVIDENCE.json',actualRoof);
  await page.screenshot({path:path.join(out,'fort-roof-evidence.jpg'),type:'jpeg',quality:92});
  const cite=page.locator('#popup [data-pop-pane="evidence"] .cites > li').filter({hasText:/Currey/});
  assert.equal(await cite.count(),1);await cite.evaluate(el=>el.scrollIntoView({block:'start'}));
  const actualCitation=await cite.evaluate(el=>({text:el.textContent,links:[...el.querySelectorAll('a[href]')].map(a=>({text:a.textContent,href:a.href})),rect:(()=>{const r=el.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height,inViewport:r.bottom>0&&r.top<innerHeight};})()}));
  assert(actualCitation.rect.inViewport&&/1912/.test(actualCitation.text)&&actualCitation.links.length>0);save('FORT-ACTUAL-CURREY-CREDIT.json',actualCitation);
  await page.screenshot({path:path.join(out,'fort-source-credit.jpg'),type:'jpeg',quality:92});
  save('FORT-CARD-RESULT.json',{outcome,reader,actualRoof,actualCitation,scope:'Actual1812 NE card, unchanged one Currey source link, zero held pictures and inferred structuregrade; source roof evidence and credits, no picture acceptance or historical camera claim.'});
  } else {
  // Trusted native skyclick only; no DOM/style hiding of the look hint.
  await page.mouse.click(mobile?195:640,mobile?250:180);save('NATIVE-LOOK-STATE.json',await page.evaluate(()=>({pointerLock:document.pointerLockElement?.tagName??null})));
  // Curated flying inspection uses the native walker; the renderer remains its owner.
  fortExterior = await page.evaluate(async reference => {
    const a=window.__chicago4d,id='first_fort_dearborn_small_house_ne';
    a.popup.close();a.navigator.dock();a.travel.stop('First Fort NE house exterior inspection');
    a.confidence.resetGrades();a.setConfidenceView(false);a.setFly(true);a.walker.setFlying(true);
    const box=a.buildings.instanceBounds()[id],matrix=a.buildings.matrixOf(id),anchor=a.buildings.matrixOf('first_fort_dearborn_small_house_ne');
    const missing=a.buildings.missing?.has?.(id);
    if(missing!==false||!box||!matrix||!anchor)throw Error('Missing real First Fort NE house/First Fort NE house geometry or transform');
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
      scope:'Curated current1812 in-app flying exterior inspection; not a calibrated source camera, historical visitor pose, picture-match verdict or obstruction-free claim.'};
  },plan.fort_reference_camera);
  save('FORT-EXTERIOR.json',fortExterior);
  assert(fortExterior.missing===false&&fortExterior.flying&&fortExterior.ready&&fortExterior.welcome==='world'&&!fortExterior.contextLost&&fortExterior.detail==='full','Actual full-detail First Fort NE house exterior');
  assert(fortExterior.projected.length===8&&fortExterior.projected.every(p=>Number.isFinite(p.ndc.x)&&Number.isFinite(p.ndc.y)&&p.ndc.z>=-1&&p.ndc.z<=1&&Math.abs(p.ndc.x)<=0.96&&Math.abs(p.ndc.y)<=0.96),'Eight actual rendered First Fort NE house corners fit the unchanged frustum');
  assert(fortExterior.after>fortExterior.before&&fortExterior.signature.litFraction>0.05&&Number.isFinite(fortExterior.signature.mean),'Actual First Fort NE house native readback');
  await page.waitForFunction(frame=>{const a=window.__chicago4d;if(!a.ready||a.welcome.state!=='world'||document.visibilityState!=='visible'||a.renderer.getContext().isContextLost())throw Error('Curated inspection world readiness changed');return a.renderer.info.render.frame>=frame+3;},fortExterior.after,{timeout:180000,polling:500});
  fortExterior.settled_frame=await page.evaluate(()=>window.__chicago4d.renderer.info.render.frame);
  const exteriorFile=path.join(out,'fort-exterior.jpg');await page.screenshot({path:exteriorFile,type:'jpeg',quality:92});
  fortExterior.screenshot={path:exteriorFile,sha256:sha(fs.readFileSync(exteriorFile)),bytes:fs.statSync(exteriorFile).size};save('FORT-EXTERIOR.json',fortExterior);
  const byGrade=await page.evaluate(async()=>{const a=window.__chicago4d;a.setConfidenceView(true);const before=a.renderer.info.render.frame,p=a.capture(12);a.step();const signature=await p;return {enabled:a.confidenceView,before,after:a.renderer.info.render.frame,signature,stats:a.stats()};});assert(byGrade.enabled&&byGrade.after>byGrade.before&&byGrade.stats.withinBudget);save('FORT-BYGRADE.json',byGrade);await page.screenshot({path:path.join(out,'fort-exterior-ByGrade.jpg'),type:'jpeg',quality:92});await page.evaluate(()=>window.__chicago4d.setConfidenceView(false));
  fortArrival=await page.evaluate(async entrance=>{
    const a=window.__chicago4d,id='first_fort_dearborn_small_house_ne';a.popup.close();a.navigator.dock();a.travel.stop('First Fort NE house native arrival');a.setFly(false);a.confidence.resetGrades();a.setConfidenceView(false);
    const arrived=a.spawnAtDestination({kind:'structure',id}),framed=a.frame(id,{card:false});
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return {id,arrived,framed,missing:a.buildings.missing.has(id),position:{...a.walker.state},camera_world:a.camera.position.toArray(),entrance,
      before,after:a.renderer.info.render.frame,signature,
      ready:a.ready,welcome:a.welcome.state,contextLost:a.renderer.getContext().isContextLost(),detail:a.detail,flying:a.walker.state.flying,
      scope:'Native public structure spawnAtDestination followed by frame(card:false). No walking through the door, full-bbox framing, absence of foreground occlusion, or whole-compound image acceptance is claimed.'};
  },plan.fort_entrance);
  save('FORT-ARRIVAL.json',fortArrival);
  assert(fortArrival.arrived===true&&fortArrival.framed===true&&fortArrival.missing===false&&!fortArrival.flying&&fortArrival.ready&&fortArrival.welcome==='world'&&!fortArrival.contextLost&&fortArrival.detail==='full','Actual native First Fort NE house arrival');
  assert(fortArrival.after>fortArrival.before&&fortArrival.signature.litFraction>0.05&&Number.isFinite(fortArrival.signature.mean),'Actual arrival native readback');
  const arrivalFile=path.join(out,'fort-arrival.jpg');await page.screenshot({path:arrivalFile,type:'jpeg',quality:92});
  fortArrival.screenshot={path:arrivalFile,sha256:sha(fs.readFileSync(arrivalFile)),bytes:fs.statSync(arrivalFile).size};save('FORT-ARRIVAL.json',fortArrival);
  assert.equal(errors.length,0,JSON.stringify(errors));assert.equal(network.length,0,JSON.stringify(network));assert.equal(consoleErrors.length,0,JSON.stringify(consoleErrors));assert.equal(serverErrors.length,0,JSON.stringify(serverErrors));
  const ground=await page.evaluate(async()=>{const a=window.__chicago4d,s=a.walker.state,e=s.e,n=s.n;const before=a.renderer.info.render.frame,p=a.capture(12);a.step();const signature=await p;return {e,n,blocked:a.router.blockedAt(e,n),water:a.terrain.isWater(e,n),surface:a.walker.surfaceAt(e,n),ground:s.groundY,eye:s.eyeY,flying:s.flying,hudFlying:a.hud.flying,intentFlying:a.intent.flying,before,after:a.renderer.info.render.frame,signature};});
  assert(!ground.blocked&&!ground.water&&!ground.flying&&!ground.hudFlying&&!ground.intentFlying&&Math.abs(ground.ground-ground.surface)<1e-6&&ground.eye>ground.ground&&ground.after>ground.before);
  save('FORT-NATIVE-GROUND-ARRIVAL.json',{...ground,scope:'Native safe arrival on real1812 ground; no hand-authored doorway or traversal claim.'});
  await page.screenshot({path:path.join(out,'fort-native-ground-arrival.jpg'),type:'jpeg',quality:92});

  }
  guard();
  assert.equal(errors.length,0,JSON.stringify(errors));assert.equal(network.length,0,JSON.stringify(network));assert.equal(consoleErrors.length,0,JSON.stringify(consoleErrors));assert.equal(serverErrors.length,0,JSON.stringify(serverErrors));
  save('RESULT.json', { status: leg === 'cards' ? 'ACTUAL_FORT_CARDS_PASS' : 'ACTUAL_FORT_BODY_PASS', viewport, leg, head: plan.expected_head, qualified_source_scope_sha256: plan.source_scope_sha256, outcome, visibleImage, screenshot: screenshotBinding, fortExterior, fortArrival, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true, scope: leg === 'cards' ? 'Actual1812 full-detail native NE world and physically scrolled Record, roof evidence, source credit and one Currey source link without held image or Spot. No full-size viewer claim.' : 'Separate actual full-detail native world on the same frozen head; curated First Fort NE house Normal/ByGrade exterior, native arrival and grounded native arrival. No historical camera, door traversal, photo match or original completion claim.' });
} catch (e) {
  failure = { message: e.message, stack: e.stack };
  const settleFile = path.join(out, 'WORLD-SETTLE.json');
  if (fs.existsSync(settleFile)) { const settle = JSON.parse(fs.readFileSync(settleFile)); if (settle.status === 'WAITING') save('WORLD-SETTLE.json', { ...settle, status: 'FAIL', failure }); }
  if (page) { try { await page.screenshot({ path: path.join(out, 'FAIL.jpg'), type: 'jpeg', quality: 90 }); } catch (captureError) { failure.screenshot_error = captureError.message; } }
  save('FAIL.json', { status: 'ACTUAL_PUBLISHED_FORT_FAIL', viewport, failure, outcome, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, no_retry: true });
} finally {
  if (browser) await browser.close().catch(e => { serverErrors.push(e.message); failure ??= { close_error: e.message }; });
  server.closeAllConnections?.(); await new Promise(resolve => server.close(resolve));
  try { guard(); save('SELECTED-INPUT-CLOSURE.json', { unchanged: true }); } catch (e) { save('SELECTED-INPUT-CLOSURE.json', { unchanged: false, error: e.message }); failure ??= { guard_error: e.message }; }
  save('CLOSURE.json', { failure, errors, network, cancelled, consoleErrors, serverErrors, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true });
}
if (failure) process.exitCode = 1;
