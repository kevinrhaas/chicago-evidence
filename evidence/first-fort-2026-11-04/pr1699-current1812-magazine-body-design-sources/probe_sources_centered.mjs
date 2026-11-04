/** Actual current1812 Magazine body/Design/Sources with native GPU roof/ground presence. No scene/renderer/source overrides. */
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
const leg = process.env.FORT_PROBE_LEG; assert.equal(leg, 'body');
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
  await page.evaluate(async id=>{const a=window.__chicago4d;a.popup.close();a.pick(id);await a.navigator.select('inspect');a.navigator.open(2);},'first_fort_dearborn_magazine');
  await page.waitForFunction(()=>{const r=document.getElementById('nav-app-inspect');return r?.dataset.structure==='first_fort_dearborn_magazine'&&!!r.querySelector('.insp-tabs');});
  const inspect=page.locator('#nav-app-inspect');
  await inspect.locator('[data-insp-tab="sources"]').scrollIntoViewIfNeeded();await inspect.locator('[data-insp-tab="sources"]').click();
  await page.waitForFunction(()=>document.querySelector('#nav-app-inspect [data-insp-pane="sources"]')?.dataset.filled==='yes');
  const sources=inspect.locator('[data-insp-pane="sources"]');assert(await sources.isVisible());
  const roofFact=sources.locator('details.src-fact').filter({has:page.locator('.src-label',{hasText:/^Roof type$/i})});assert.equal(await roofFact.count(),1);await roofFact.locator(':scope > summary').scrollIntoViewIfNeeded();await roofFact.locator(':scope > summary').click();
  const roofState=await roofFact.evaluate(el=>({open:el.open,grade:el.dataset.grade,text:el.textContent,note:el.querySelector('.src-why')?.textContent??'',noteWithheld:!!el.querySelector('.src-why-later')}));assert(roofState.open&&roofState.grade==='inferred'&&/barrel vault/i.test(roofState.text)&&/1912/.test(roofState.text)&&/1808/.test(roofState.text));assert.equal(roofState.noteWithheld,plan.expectedRoofNoteWithheld,'Exact visitor readerCopy note suppression');assert.equal(roofState.note.replace(/^why\s*/i,'').replace(/\s+/g,' ').trim(),plan.expectedSourceRoofNote.replace(/\s+/g,' ').trim(),'Actual Sources note equals exact consumed readerCopy; metric/date limits retained');
  await roofFact.locator('.src-why').evaluate(el=>el.scrollIntoView({block:'center'}));await page.screenshot({path:path.join(out,'magazine-sources-roof-note.jpg'),type:'jpeg',quality:92});
  const citeFold=roofFact.locator('details.src-cites');assert.equal(await citeFold.count(),1);await citeFold.locator(':scope > summary').scrollIntoViewIfNeeded();await citeFold.locator(':scope > summary').click();
  const citations=[];
  for(const [label,pattern]of [['whistler',/Whistler/],['currey',/Currey/]]){
    const row=citeFold.locator('ol.cites > li').filter({hasText:pattern});assert.equal(await row.count(),1);await row.evaluate(el=>el.scrollIntoView({block:'center'}));
    const actual=await row.evaluate(el=>{const r=el.getBoundingClientRect();return{text:el.innerText,links:[...el.querySelectorAll('a[href]')].map(a=>a.href),rect:{x:r.x,y:r.y,width:r.width,height:r.height,intersects:r.bottom>0&&r.top<innerHeight}}});assert(actual.rect.intersects&&actual.links.length);assert(new RegExp(label==='whistler'?'1808':'1912').test(actual.text));citations.push({label,...actual});await page.screenshot({path:path.join(out,`magazine-sources-${label}-credit.jpg`),type:'jpeg',quality:92});
  }
  const riseFact=sources.locator('details.src-fact').filter({has:page.locator('.src-label',{hasText:/^Barrel rise \(m\)$/i})});assert.equal(await riseFact.count(),1);await riseFact.locator(':scope > summary').scrollIntoViewIfNeeded();await riseFact.locator(':scope > summary').click();
  const riseState=await riseFact.evaluate(el=>({open:el.open,grade:el.dataset.grade,text:el.textContent,note:el.querySelector('.src-why')?.textContent??''}));assert(riseState.open&&riseState.grade==='reconstructed'&&/not a measured vault rise/i.test(riseState.note)&&/varying tangent/i.test(riseState.note));
  await riseFact.locator('.src-why').evaluate(el=>el.scrollIntoView({block:'center'}));await page.screenshot({path:path.join(out,'magazine-sources-reconstructed-rise.jpg'),type:'jpeg',quality:92});
  save('MAGAZINE-ACTUAL-SOURCES.json',{roofState,riseState,citations,scope:'Actual current1812 Inspect Sources expanded notes and citations; screenshot crop limits require direct pixel review. No full long text visibility claim.'});

  guard();
  assert.equal(errors.length,0,JSON.stringify(errors));assert.equal(network.length,0,JSON.stringify(network));assert.equal(consoleErrors.length,0,JSON.stringify(consoleErrors));assert.equal(serverErrors.length,0,JSON.stringify(serverErrors));
  save('RESULT.json',{status:'ACTUAL_MAGAZINE_SOURCES_CENTERED_CAPTURE_PASS',viewport,head:plan.expected_head,roofState,riseState,citations,errors,network,cancelled,consoleErrors,serverErrors,wall_ms:performance.now()-started,scope:'Supplementary real native Inspect Sources captures, centered with native scrollIntoView. Earlier complete body/Design/ground checks are separate; no rerun or full long-note visibility claimed.'});
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
