/** Actual published1835 keeper east-end material/body with native GPU presence. No scene/renderer/source overrides. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/shared/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const plan = JSON.parse(fs.readFileSync(process.env.JAIL_PROBE_PLAN));
const out = process.env.JAIL_PROBE_OUT, viewport = process.env.JAIL_PROBE_VIEWPORT;
const leg = process.env.JAIL_PROBE_LEG; assert.equal(leg, 'body');
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

  // Curated native east-end inspection. Historical reference cameras stay untouched.
  const body = await page.evaluate(async expected => {
    const a=window.__chicago4d,id='log_jail_keeper_house',THREE=await import('three');
    if(a.buildings.missing.has(id))throw Error('Keeper is missing from native uploaded geometry');
    const matrix=a.buildings.matrixOf(id),bounds=a.buildings.instanceBounds()[id];
    if(!matrix||!bounds)throw Error('Keeper native transform/bounds missing');
    const target=new THREE.Vector3(...expected.centroid).applyMatrix4(matrix);
    const eye=new THREE.Vector3(...expected.eye).applyMatrix4(matrix);
    const delta=target.clone().sub(eye),ground=a.walker.surfaceAt(eye.x,-eye.z);
    const placement={local_e:eye.x,local_n:-eye.z,yaw_deg:(Math.atan2(delta.x,-delta.z)*180/Math.PI+360)%360,pitch_deg:Math.atan2(delta.y,Math.hypot(delta.x,delta.z))*180/Math.PI,altitude_m:eye.y-ground};
    a.popup.close();a.navigator.dock();a.travel.stop('Keeper east-end material inspection');a.confidence.resetGrades();a.setConfidenceView(false);a.setFly(true);a.walker.setFlying(true);a.walker.teleport(placement);a.step();
    const ray=await a.buildings.pickAtAsync({x:0,y:0},a.camera);
    if(ray?.id!==id||!ray.point?.toArray().every(Number.isFinite))throw Error('Native east-end ray blocked or missed keeper: '+JSON.stringify(ray?{id:ray.id,point:ray.point?.toArray()}:null));
    const distance=ray.point.distanceTo(target);if(distance>.06)throw Error('Native ray did not reach the real east gable: '+distance);
    const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
    return{id,matrix:matrix.elements,bounds,centroidLocal:expected.centroid,actualCentroidWorld:target.toArray(),eyeWorld:eye.toArray(),placement,ray:{id:ray.id,point:ray.point.toArray(),distanceToExpected:distance},before,after:a.renderer.info.render.frame,signature,ready:a.ready,detail:a.detail,contextLost:a.renderer.getContext().isContextLost(),flying:a.walker.state.flying,scope:'Curated current native flying east-end view with a real GPU ray into the changed material face; not a historical reference camera or complete compound/passage acceptance.'};
  },plan.east_face);
  assert(body.ready&&body.detail==='full'&&body.flying&&!body.contextLost&&body.after>body.before&&body.signature.litFraction>.05);
  save('KEEPER-EAST-NATIVE-BODY.json',body);
  await page.waitForFunction(frame=>window.__chicago4d.renderer.info.render.frame>=frame+3,body.after,{timeout:180000,polling:500});
  const bodyFile=path.join(out,'keeper-east-body.jpg');await page.screenshot({path:bodyFile,type:'jpeg',quality:94});
  body.screenshot={path:bodyFile,sha256:sha(fs.readFileSync(bodyFile)),bytes:fs.statSync(bodyFile).size};save('KEEPER-EAST-NATIVE-BODY.json',body);
  // Actual native Inspect access, preserving existing source credits and field grades.
  await page.evaluate(async()=>{const a=window.__chicago4d;a.pick('log_jail_keeper_house');await a.navigator.select('inspect');a.navigator.open(2);});
  await page.waitForFunction(()=>document.getElementById('nav-app-inspect')?.dataset.structure==='log_jail_keeper_house');
  const inspect=page.locator('#nav-app-inspect');const ui={};
  for(const tab of ['design','sources']){
    await inspect.locator(`[data-insp-tab="${tab}"]`).scrollIntoViewIfNeeded();await inspect.locator(`[data-insp-tab="${tab}"]`).click();
    await page.waitForFunction(name=>document.querySelector(`#nav-app-inspect [data-insp-pane="${name}"]`)?.dataset.filled==='yes',tab);
    const pane=inspect.locator(`[data-insp-pane="${tab}"]`);assert(await pane.isVisible());
    ui[tab]=await pane.evaluate(el=>({text:el.innerText,rows:[...el.querySelectorAll('.insp-hot,details.src-fact')].map(x=>({label:x.querySelector('.insp-hot-text,.src-label')?.textContent,grade:x.dataset.grade}))}));
    assert(ui[tab].text.trim().length>20,'Real '+tab+' text present');await page.screenshot({path:path.join(out,`keeper-${tab}.jpg`),type:'jpeg',quality:92});
  }
  save('KEEPER-ACTUAL-INSPECT.json',{...ui,scope:'Actual current Design/Sources physically opened in this viewport; no full source-card text/credit screenshot acceptance is inferred.'});
  guard();assert.equal(errors.length,0,JSON.stringify(errors));assert.equal(network.length,0,JSON.stringify(network));assert.equal(consoleErrors.length,0,JSON.stringify(consoleErrors));assert.equal(serverErrors.length,0,JSON.stringify(serverErrors));
  save('RESULT.json',{status:'ACTUAL_KEEPER_EAST_BODY_INSPECT_PASS',head:plan.expected_head,viewport,body,ui,errors,network,cancelled,consoleErrors,serverErrors,wall_ms:performance.now()-started,no_retry:true,scope:'Real published keeper changed east-material face and actual Inspect; separate generic desktop/relevant smoke required. No historical fit, new camera, source grade or full compound acceptance.'});
} catch (e) {
  failure = { message: e.message, stack: e.stack };
  const settleFile = path.join(out, 'WORLD-SETTLE.json');
  if (fs.existsSync(settleFile)) { const settle = JSON.parse(fs.readFileSync(settleFile)); if (settle.status === 'WAITING') save('WORLD-SETTLE.json', { ...settle, status: 'FAIL', failure }); }
  if (page) { try { await page.screenshot({ path: path.join(out, 'FAIL.jpg'), type: 'jpeg', quality: 90 }); } catch (captureError) { failure.screenshot_error = captureError.message; } }
  save('FAIL.json', { status: 'ACTUAL_PUBLISHED_JAIL_FAIL', viewport, failure, outcome, errors, network, cancelled, consoleErrors, serverErrors, wall_ms: performance.now()-started, no_retry: true });
} finally {
  if (browser) await browser.close().catch(e => { serverErrors.push(e.message); failure ??= { close_error: e.message }; });
  server.closeAllConnections?.(); await new Promise(resolve => server.close(resolve));
  try { guard(); save('SELECTED-INPUT-CLOSURE.json', { unchanged: true }); } catch (e) { save('SELECTED-INPUT-CLOSURE.json', { unchanged: false, error: e.message }); failure ??= { guard_error: e.message }; }
  save('CLOSURE.json', { failure, errors, network, cancelled, consoleErrors, serverErrors, native_capture_timeout_unchanged: true, no_wallclock_10s_or_FPS_claim: true, no_retry: true });
}
if (failure) process.exitCode = 1;
