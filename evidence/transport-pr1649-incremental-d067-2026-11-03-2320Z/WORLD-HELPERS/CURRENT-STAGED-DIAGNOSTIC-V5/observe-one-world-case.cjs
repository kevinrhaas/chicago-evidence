// SPDX-License-Identifier: GPL-3.0-or-later
// PREPARED UNRUN. Root owns the exclusive supervisor, deadline and resource guard.
const fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const assert = require('node:assert/strict'), crypto = require('node:crypto');
const { probeTownDriverWorld } = require('./probe-town-driver-world.cjs');
const cfg = JSON.parse(fs.readFileSync(process.argv[2]));
assert.equal(cfg.root_explicit_world_interaction_GO, true); assert.equal(cfg.template_only, false);
assert(['A', 'B', 'C'].includes(cfg.scope)); assert(['1835', '1904'].includes(cfg.scene)); assert.equal(typeof cfg.touch, 'boolean');
assert(['source', 'published'].includes(cfg.tree)); assert(['1835', '1904'].includes(cfg.scene));
assert(cfg.root && cfg.output && !fs.existsSync(cfg.output));
assert(Object.keys(cfg.actual_source_pins ?? {}).length >= 10);
const digest = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
for (const [file, sha] of Object.entries(cfg.actual_source_pins)) assert.equal(digest(file), sha, file);
const root = fs.realpathSync(cfg.root), seen = new Map(), missing = [], pageErrors = [];
fs.mkdirSync(cfg.output, { recursive: true });
const types = { '.html': 'text/html', '.mjs': 'text/javascript', '.js': 'text/javascript',
  '.json': 'application/json', '.glb': 'model/gltf-binary', '.wasm': 'application/wasm',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.svg': 'image/svg+xml', '.css': 'text/css', '.ktx2': 'image/ktx2' };
const report = { status: 'ACTIVE_ACTUAL_WORLD_INTERACTION_NOT_PASS', cfg, served: [], missing, pageErrors };
const save = () => { report.served = [...seen.values()]; fs.writeFileSync(path.join(cfg.output, 'WORLD-CASE-RESULT.json'), JSON.stringify(report, null, 2) + '\n'); };
const server = http.createServer((req, res) => {
  try {
    let rel = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/+/, '');
    let file = path.resolve(root, rel); assert(file === root || file.startsWith(root + path.sep));
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { missing.push(rel); res.writeHead(404); return res.end(); }
    file = fs.realpathSync(file); assert(file.startsWith(root + path.sep));
    const body = fs.readFileSync(file), sha256 = crypto.createHash('sha256').update(body).digest('hex');
    if (seen.has(file)) assert.equal(seen.get(file).sha256, sha256, file);
    seen.set(file, { file, sha256, bytes: body.length, url: rel, firstServedUtc: seen.get(file)?.firstServedUtc ?? new Date().toISOString() });
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    res.end(body);
  } catch (error) { report.serveError = String(error); res.writeHead(500); res.end(); }
});
(async () => {
  let browser, context, page, observerProgressTimer;
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const playwright = require(path.join((process.env.NODE_PATH || '/workspace/.cloud-setup/npm/node_modules').split(path.delimiter)[0], 'playwright'));
    browser = await playwright.chromium.launch({ executablePath: process.env.PW_EXECUTABLE || undefined,
      args: ['--enable-unsafe-swiftshader'] });
    report.browserVersion = browser.version(); assert.match(report.browserVersion, /^141\./, 'Matching native Chromium141 required');
    context = await browser.newContext({ viewport: cfg.touch ? { width: 390, height: 780 } : { width: 1280, height: 800 },
      hasTouch: !!cfg.touch, deviceScaleFactor: cfg.touch ? 2 : 1, reducedMotion: 'no-preference' });
    // Existing visitor Image sharpness: Low(1), persisted through the normal settings reader.
    // Touch/DPR2/390x780/Balanced/assets/physics and every functional predicate stay unchanged.
    await context.addInitScript(({ detail }) => { try {
      const settings = JSON.parse(localStorage.getItem('chicago4d.settings') || '{}');
      settings.quality = 1; settings.detail = detail;
      localStorage.setItem('chicago4d.settings', JSON.stringify(settings));
    } catch {} }, { detail: cfg.touch ? 'balanced' : 'full' });
    report.nativeVisitorBootProfile = { detail: cfg.touch ? 'balanced' : 'full', quality: 1,
      differenceFromV2: 'Persist actual requested visitor tier before boot; original setDetail remains and original Light retirement test remains.' };
    page = await context.newPage(); page.on('pageerror', e => pageErrors.push(String(e)));
    const entry = cfg.tree === 'source' ? '/renderers/web/index.html' : '/walk/index.html';
    const moduleBase = cfg.tree === 'source' ? '/renderers/web/js/' : '/walk/js/';
    await page.goto(`http://127.0.0.1:${server.address().port}${entry}?year=${cfg.scene}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    const sampleObserverProgress = () => {
      report.observerProgress ??= [];
      report.observerProgress.push({ hostUtc: new Date().toISOString(), servedFileCount: seen.size,
        missingCount: missing.length, pageErrorCount: pageErrors.length,
        servedAssemblyStages: [...seen.values()].filter(row => /transport\/|humans\/|assembly|hitch|meshopt|people\.json/.test(row.url))
          .map(({ url, bytes, firstServedUtc }) => ({ url, bytes, firstServedUtc })) });
      save();
    };
    sampleObserverProgress();
    observerProgressTimer = setInterval(sampleObserverProgress, 10000);
    const routeProbe = cfg.recheck_whole_route ? require(cfg.actual_route_probe).probeNativeWorldRoute : null;
    report.probe = await probeTownDriverWorld(page, { sceneId: cfg.scene, touch: !!cfg.touch,
      moduleBase, outdir: cfg.output, label: `${cfg.tree}-${cfg.scene}-${cfg.touch ? 'mobile' : 'desktop'}-scope${cfg.scope}`,
      scope: cfg.scope, checkLight: cfg.check_light === true, bootReadyMs: 240000, mountReadyMs: cfg.mount_ready_ms, routeProbe });
    for (const [file, sha] of Object.entries(cfg.actual_source_pins)) assert.equal(digest(file), sha, file);
    for (const row of seen.values()) assert.equal(digest(row.file), row.sha256, row.file);
    assert.deepEqual(pageErrors, []); assert.deepEqual(missing, []); assert.equal(report.serveError, undefined);
    assert.equal(report.probe.status, 'ACTUAL_APP_WORLD_DRIVER_SCOPE_PASS');
    assert.equal(report.probe.scope, cfg.scope);
    report.status = 'ACTUAL_WORLD_INTERACTION_SCOPE_PASS';
  } catch (error) {
    report.status = 'ACTUAL_WORLD_INTERACTION_SCOPE_NONPASS'; report.failure = String(error.stack ?? error); process.exitCode = 1;
    if (page) {
      try { report.failureAPI = await page.evaluate(() => { const a = window.__chicago4d; return a ? { ready: a.ready, error: a.error, problems: [...(a.problems ?? [])], town: a.townTransport?.snapshot?.(), humans: a.humans?.count, scene: a.scene?.id, welcome: a.welcome?.state,
        cardEvents: window.__transportCardEvents, navigator: { app: a.navigator?.app, level: a.navigator?.level, link: a.navigator?.link, snapshot: a.navigator?.snapshot?.() },
        panes: [...document.querySelectorAll('.insp-pane')].map(p => ({ dataset: {...p.dataset}, hidden: p.hidden, rect: p.getBoundingClientRect().toJSON(), text: p.textContent.slice(0,500) })),
        cards: [...document.querySelectorAll('.insp-person-card')].map(c => ({ dataset: {...c.dataset}, rect: c.getBoundingClientRect().toJSON(), name: c.querySelector('.insp-person-name')?.textContent, census: !!c.querySelector('.insp-person-census'), waiting: !!c.querySelector('.insp-person-wait'), text: c.textContent.slice(0,2000) })),
        panels: [...document.querySelectorAll('#panel, #nav-app-inspect, #navigator')].map(p => ({ id:p.id, hidden:p.hidden, rect:p.getBoundingClientRect().toJSON(), classes:p.className })),
        driver: a.townTransport?.actors?.map(d => {const h=a.humans?.external(d.personId); return {personId:d.personId, interaction:h?.instance?.interaction, identity:h?.identity?.kind};})
      } : { apiAbsent: true }; }); } catch (e) { report.failureAPIError = String(e); }
      try { await page.screenshot({path: path.join(cfg.output,'ACTUAL-FAILURE-FRAME.png'),timeout:10000}); } catch (e) { report.failureScreenshotError = String(e); }
    }
  }
  finally {
    if (observerProgressTimer) clearInterval(observerProgressTimer);
    if (context) await context.close(); if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve)); save();
  }
})();
