/** Diagnostic replay of stage 15's final navigation. One actual published world.
 * Launch only after the coordinating agent grants the CPU/published-tree window.
 * No renderer throttling, asset substitutions, application patches or error filtering.
 * The narration-index stand-in and bounded picture drain are the official smoke helpers.
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const app = path.resolve(process.env.PROBE_APP || '/workspace/chicago/chicago/4d');
assert(process.env.PROBE_ROOT, 'PROBE_ROOT must name the approved frozen published mirror');
assert(process.env.PROBE_EXPECT_COMMIT, 'PROBE_EXPECT_COMMIT must pin the approved source');
assert(process.env.PROBE_OUT, 'PROBE_OUT must name a new evidence directory');
const site = path.resolve(process.env.PROBE_ROOT);
const out = path.resolve(process.env.PROBE_OUT);
const mode = process.env.PROBE_MODE || 'immediate';
assert(['immediate', 'settled'].includes(mode));
const width = Number(process.env.PROBE_WIDTH || 1280);
assert([390, 1280].includes(width));
const height = width === 390 ? 780 : 800;
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const head = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: app, encoding: 'utf8' }).trim();
assert.equal(head, process.env.PROBE_EXPECT_COMMIT);
assert(!fs.existsSync(out), 'Never overwrite an existing attempt');
const hashes = {};
for (const rel of ['js/main.js', 'js/scene-loader.js', 'js/shared-images.js', 'js/texture-residency.js',
  'js/humans.js', 'js/pictures.js', 'js/controls/keyboard.js', 'js/controls/pointerlock.js']) {
  const source = digest(fs.readFileSync(path.join(app, 'renderers/web', rel)));
  const published = digest(fs.readFileSync(path.join(site, 'walk', rel)));
  assert.equal(published, source, `Frozen mirror mismatch: ${rel}`);
  hashes[`walk/${rel}`] = published;
}
for (const rel of ['walk/index.html', '1904/index.html', 'data/sidecars/1835/index.json', 'data/sidecars/1904/index.json'])
  hashes[rel] = digest(fs.readFileSync(path.join(site, rel)));

// Extract the current official implementations without executing the smoke runner.
const harnessPath = path.join(app, 'tools/smoke_renderer.mjs');
const harness = fs.readFileSync(harnessPath, 'utf8');
const helperStart = harness.indexOf('const pictureRefusalProbe = () => {');
const helperEnd = harness.indexOf('const server = http.createServer', helperStart);
assert(helperStart > 0 && helperEnd > helperStart, 'Official picture-helper boundary changed');
const helperSource = harness.slice(helperStart, helperEnd);
const { pictureRefusalProbe, trackPictureFiles, settlePictureWork } = new Function(
  `${helperSource}\nreturn { pictureRefusalProbe, trackPictureFiles, settlePictureWork };`)();
const { standInNarrationIndex } = await import(pathToFileURL(path.join(app, 'tools/audio_smoke_replay.mjs')));
const { chromium } = createRequire('/workspace/chicago/package.json')('playwright');

fs.mkdirSync(out);
const traceFile = path.join(out, 'events.ndjson');
const trace = fs.createWriteStream(traceFile, { flags: 'wx' });
const report = {
  started: new Date().toISOString(), source: head, app, site, mode, viewport: { width, height },
  hashes, harness: { path: harnessPath, sha256: digest(harness), helperSha256: digest(helperSource) },
  probeSha256: digest(fs.readFileSync(fileURLToPath(import.meta.url))),
  scope: 'Diagnostic actual Light1835→1904 Jump, Confidence carry-over, then stage15 forced1835 nav=jump navigation',
  limitations: ['This skips the preceding jaunt itinerary and is not a complete official smoke stage.',
    'Instrumentation records timing without delaying/retrying blob reads or changing renderer/loader behavior.',
    'An immediate-mode non-reproduction is not proof that the CI race is absent.',
    'Both modes keep all console/page/HTTP errors. Only the intermediate pre-navigation drain differs.'],
  phases: [], checks: [], errors: [], warnings: [], requestFailures: [], navigations: [], snapshots: [],
  settlements: [], events: 0, browserClosed: false, serverClosed: false,
};
let phase = 'setup';
const save = () => fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
const record = (kind, data = {}) => {
  const event = { hostWallMs: Date.now(), kind, phase, ...data };
  report.events++; trace.write(JSON.stringify(event) + '\n');
  return event;
};
const mark = (name, data = {}) => {
  phase = name; report.phases.push(record('phase', data)); save();
  console.log(new Date().toISOString(), name, JSON.stringify(data));
};
const check = (name, condition, detail) => {
  report.checks.push({ name, pass: !!condition, detail }); save();
  assert(condition, `${name}: ${JSON.stringify(detail)}`);
};
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.glb': 'model/gltf-binary', '.wasm': 'application/wasm',
  '.ktx2': 'image/ktx2', '.bin': 'application/octet-stream', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  try {
    let file = path.resolve(site, '.' + decodeURIComponent(new URL(req.url, 'http://local').pathname));
    if (!file.startsWith(site + path.sep) && file !== site) { res.writeHead(403); res.end(); return; }
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).on('error', () => res.destroy()).pipe(res);
  } catch { res.writeHead(404); res.end('Not found'); }
});
let browser, context, page, pictureFiles;

function textureTimeline() {
  const prefix = '__T3658_TEXTURE_TRACE__';
  const epoch = `${performance.timeOrigin}-${Math.random().toString(36).slice(2)}`;
  const pending = new Map(), created = new Map();
  let events = 0, dropped = 0;
  const emit = (kind, data = {}) => {
    if (++events > 20000) { dropped++; return; }
    try { console.debug(prefix + JSON.stringify({ kind, epoch, wallMs: Date.now(),
      monotonicMs: performance.now(), href: location.href, ...data })); } catch { /* diagnostics only */ }
  };
  const stack = () => String(new Error().stack || '').split('\n').slice(2, 9).join('\n');
  const create = URL.createObjectURL;
  URL.createObjectURL = function(value) {
    const url = Reflect.apply(create, URL, [value]);
    const info = { bytes: value?.size ?? null, mime: value?.type ?? null, stack: stack() };
    created.set(url, info); emit('blob-create', { url, ...info }); return url;
  };
  const revoke = URL.revokeObjectURL;
  URL.revokeObjectURL = function(url) {
    emit('blob-revoke', { url: String(url), pending: pending.has(String(url)), stack: stack() });
    created.delete(String(url)); return Reflect.apply(revoke, URL, [url]);
  };
  const fetch = globalThis.fetch;
  globalThis.fetch = function(...args) {
    const url = String(args[0]?.url ?? args[0] ?? '');
    const promise = Reflect.apply(fetch, globalThis, args);
    if (!url.startsWith('blob:')) return promise;
    const signal = args[1]?.signal ?? args[0]?.signal;
    pending.set(url, { started: performance.now(), createdHere: created.has(url) });
    emit('blob-fetch-start', { url, createdHere: created.has(url), aborted: signal?.aborted ?? null });
    const abort = () => emit('blob-fetch-abort', { url, reason: String(signal?.reason ?? '') });
    signal?.addEventListener?.('abort', abort, { once: true });
    promise.then(response => {
      emit('blob-fetch-resolved', { url, status: response.status, elapsedMs: performance.now() - pending.get(url)?.started });
      pending.delete(url); signal?.removeEventListener?.('abort', abort);
    }, error => {
      emit('blob-fetch-rejected', { url, name: error?.name, message: error?.message,
        aborted: signal?.aborted ?? null, reason: String(signal?.reason ?? ''),
        createdHere: created.has(url), elapsedMs: performance.now() - pending.get(url)?.started });
      pending.delete(url); signal?.removeEventListener?.('abort', abort);
    });
    return promise;
  };
  const snapshot = () => ({ epoch, href: location.href, wallMs: Date.now(), monotonicMs: performance.now(),
    work: { ...(globalThis.__c4dPictureWork ?? {}) }, pending: [...pending.keys()], liveObjectURLs: created.size,
    droppedEvents: dropped, visibility: document.visibilityState });
  Object.defineProperty(globalThis, '__t3658TextureSnapshot', { value: snapshot });
  for (const kind of ['beforeunload', 'pagehide', 'pageshow', 'unload'])
    addEventListener(kind, event => emit(kind, { persisted: event.persisted ?? null, snapshot: snapshot() }));
  document.addEventListener('visibilitychange', () => emit('visibilitychange', { snapshot: snapshot() }));
  emit('document-start');
}

try {
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(4187, '127.0.0.1', resolve); });
  const origin = 'http://127.0.0.1:4187';
  const base = `${origin}/walk/?year=1835&keep-geometry=1`;
  browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || '/usr/bin/chromium',
    args: ['--enable-unsafe-swiftshader'] });
  context = await browser.newContext({ viewport: { width, height }, hasTouch: width === 390,
    isMobile: false, deviceScaleFactor: width === 390 ? 2 : 1 });
  await standInNarrationIndex(context, { origin });
  // Keep the official work probe and the diagnostic wrapper in deterministic order.
  await context.addInitScript({ content: `(${pictureRefusalProbe.toString()})();\n(${textureTimeline.toString()})();\n`
    + `try { if (!localStorage.getItem('chicago4d.settings')) localStorage.setItem('chicago4d.settings', JSON.stringify({detail:'light'})); } catch {}\n`
    + `window.__arrivalYears=[];new MutationObserver(()=>{const y=document.getElementById('arrival-year')?.dataset.year;if(y&&y!==window.__arrivalYears.at(-1)?.year)window.__arrivalYears.push({year:y});}).observe(document,{subtree:true,childList:true,attributes:true,attributeFilter:['data-year','data-state']});` });
  page = await context.newPage(); page.setDefaultTimeout(90000);
  pictureFiles = trackPictureFiles(page);
  page.on('console', message => {
    const text = message.text();
    if (text.startsWith('__T3658_TEXTURE_TRACE__')) {
      try { record('browser-trace', { event: JSON.parse(text.slice('__T3658_TEXTURE_TRACE__'.length)) }); }
      catch { record('invalid-trace', { text }); }
    } else {
      const row = record('console', { type: message.type(), text, pageURL: page.url() });
      if (message.type() === 'error') { report.errors.push(row); save(); }
      if (message.type() === 'warning') report.warnings.push(row);
    }
  });
  page.on('pageerror', error => { report.errors.push(record('pageerror', { message: String(error), pageURL: page.url() })); save(); });
  page.on('response', response => { if (response.status() >= 400) {
    report.errors.push(record('http-error', { status: response.status(), url: response.url() })); save();
  } });
  page.on('requestfailed', request => { report.requestFailures.push(record('requestfailed', {
    url: request.url(), resourceType: request.resourceType(), failure: request.failure() })); save(); });
  page.on('framenavigated', frame => { if (frame === page.mainFrame()) {
    report.navigations.push(record('main-frame-navigation', { url: frame.url() })); save();
  } });
  const cdp = await context.newCDPSession(page);
  await cdp.send('Page.enable');
  cdp.on('Page.frameRequestedNavigation', event => record('frame-requested-navigation', event));
  const snapshot = async name => {
    const row = { name, ...(await page.evaluate(() => globalThis.__t3658TextureSnapshot?.() ?? null)),
      files: pictureFiles() };
    report.snapshots.push(row); record('snapshot', row); save(); return row;
  };
  const until = fn => page.waitForFunction(fn, null, { polling: 250 });
  const settle = async name => {
    mark(name); await snapshot(`${name}-before`);
    const result = await settlePictureWork(page, pictureFiles);
    report.settlements.push({ name, ...result }); await snapshot(`${name}-after`); save();
    console.log(new Date().toISOString(), 'SETTLE', name, JSON.stringify(result));
    return result;
  };

  mark('initial1835-boot');
  await page.goto(base, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForFunction(() => __chicago4d?.ready === true, null, { timeout: 240000, polling: 500 });
  await page.waitForFunction(() => __chicago4d?.welcome?.state === 'welcome', null, { timeout: 90000, polling: 500 });
  await page.waitForFunction(() => document.documentElement.dataset.journey === 'landed', null, { timeout: 90000, polling: 250 });
  await page.evaluate(() => __chicago4d.welcome.enter('spawn'));
  await until(() => __chicago4d.welcome.state === 'world');
  mark('initial1835-world');
  if (process.env.PROBE_WORLD_HOOK) {
    const hookPath = path.resolve(process.env.PROBE_WORLD_HOOK);
    report.worldHook = { path: hookPath, sha256: digest(fs.readFileSync(hookPath)) };
    mark('optional-world-hook');
    const hook = await import(pathToFileURL(hookPath));
    report.worldHook.result = await hook.run(page, { record, snapshot }); save();
  }
  await page.evaluate(() => __chicago4d.navigator.select('confidence'));
  await until(() => !!document.getElementById('cm-opacity-attested') && !!document.getElementById('cm-reconstructed'));
  const before = await page.evaluate(() => {
    const slider = document.getElementById('cm-opacity-attested'); slider.value = '30';
    slider.dispatchEvent(new Event('input', { bubbles: true })); slider.dispatchEvent(new Event('change', { bubbles: true }));
    document.getElementById('cm-reconstructed').click();
    const a = __chicago4d; return { year: a.scene.id, on: a.confidenceView,
      hidden: a.hud.hiddenLevels, attested: Math.round(a.confidence.grade('attested').opacity * 100) };
  });
  check('Confidence configured before Jump', before.on && before.attested === 30
    && JSON.stringify(before.hidden) === '["reconstructed"]', before);
  await page.evaluate(() => __chicago4d.navigator.select('jump'));
  await until(() => !!document.querySelector('#nav-app-jump .nav-jump:not([aria-current])'));
  mark('actual-jump-to1904'); await snapshot('before-actual-jump');
  const destination = await page.evaluate(() => {
    const card = document.querySelector('#nav-app-jump a.nav-jump[data-year="1904"]');
    card?.click(); document.querySelector('.recall-confirm .recall-go')?.click();
    return { year: card?.dataset.year, ring: !!document.querySelector('.nav-jump-ring') };
  });
  await page.waitForURL(/\/1904\//, { timeout: 30000 });
  await page.waitForFunction(() => __chicago4d?.welcome?.state === 'welcome', null, { timeout: 240000, polling: 500 });
  await page.waitForFunction(() => document.documentElement.dataset.journey === 'landed', null, { timeout: 30000, polling: 250 });
  const landed = await page.evaluate(() => ({ year: __chicago4d.scene.id,
    journey: document.documentElement.dataset.journey, transfer: document.documentElement.dataset.transfer,
    years: __arrivalYears.map(row => row.year) }));
  check('Actual Jump lands in1904', destination.year === '1904' && destination.ring
    && String(landed.year) === '1904' && landed.journey === 'landed' && landed.transfer === 'true'
    && landed.years.length >= 2 && Number(landed.years[0]) > 1904 && landed.years.at(-1) === '1904', landed);
  mark('1904-landed');
  await page.evaluate(() => __chicago4d.welcome.enter('spawn'));
  await page.waitForFunction(() => __chicago4d.welcome.state === 'world', null, { timeout: 120000, polling: 250 });
  await page.waitForFunction(() => !document.getElementById('conf-legend')?.hidden, null, { timeout: 30000, polling: 250 });
  const after = await page.evaluate(() => {
    const a = __chicago4d, u = a.confidence.uniforms.uHideLevel.value, el = document.getElementById('conf-legend');
    return { year: a.scene.id, on: a.confidenceView, hidden: a.hud.hiddenLevels, hide: [u.x,u.y,u.z],
      attested: Math.round(a.confidence.grade('attested').opacity * 100), mode: a.confidence.grade('attested').mode,
      legend: !!el && !el.hidden, dots: [...el.querySelectorAll('[data-grade]')].map(d => d.dataset.state).join(',') };
  });
  check('Confidence carries across Jump', String(after.year) === '1904' && after.on
    && JSON.stringify(after.hidden) === '["reconstructed"]' && JSON.stringify(after.hide) === '[0,0,1]'
    && after.attested === 30 && after.mode === 'tint' && after.legend && after.dots === 'tint,tint,hidden', after);
  mark('1904-carry-check-complete');
  await page.evaluate(() => { localStorage.removeItem('chicago4d.confidence'); localStorage.removeItem('chicago4d.confidence.hidden'); });
  if (mode === 'settled') await settle('1904-before-forced-navigation-drain');
  await snapshot('immediately-before-forced-navigation');
  mark('forced1835-navjump-goto-start');
  await page.goto(`${base}&nav=jump`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  mark('forced1835-navjump-domcontentloaded');
  await page.waitForFunction(() => __chicago4d?.navLinkOpened?.app === 'jump'
    && __chicago4d?.navigator?.app === 'jump', null, { timeout: 240000, polling: 500 });
  const linked = await page.evaluate(() => ({ app: __chicago4d.navigator.app, level: __chicago4d.navigator.level,
    gate: document.getElementById('gate').hidden, held: __chicago4d.navHistory?.held, href: location.href }));
  await page.evaluate(() => history.back());
  await page.waitForFunction(() => __chicago4d?.navigator?.level === 0, null, { timeout: 10000, polling: 100 });
  const backed = await page.evaluate(() => ({ app: __chicago4d.navigator.app, level: __chicago4d.navigator.level, href: location.href }));
  check('nav=jump opens and Back stays in same document', linked.app === 'jump' && linked.level > 0
    && linked.gate && linked.held === true && backed.href === linked.href && backed.app === 'home' && backed.level === 0, { linked, backed });
  await settle('final1835-before-context-close-drain');
  mark('final-context-close'); await context.close(); context = null;
  check('No console/page/HTTP errors in diagnostic path', report.errors.length === 0, report.errors);
  report.completed = true;
} catch (error) {
  report.completed = false; report.failure = String(error.stack || error); process.exitCode = 1;
  console.error(report.failure);
} finally {
  if (context) await context.close().catch(error => record('cleanup-context-error', { error: String(error) }));
  if (browser) { await browser.close(); report.browserClosed = true; }
  if (server.listening) await new Promise(resolve => server.close(resolve));
  report.serverClosed = !server.listening; report.finished = new Date().toISOString(); save();
  await new Promise(resolve => trace.end(resolve));
  console.log(JSON.stringify({ completed: report.completed, errors: report.errors.length,
    report: path.join(out, 'report.json'), trace: traceFile, browserClosed: report.browserClosed,
    serverClosed: report.serverClosed }));
}
