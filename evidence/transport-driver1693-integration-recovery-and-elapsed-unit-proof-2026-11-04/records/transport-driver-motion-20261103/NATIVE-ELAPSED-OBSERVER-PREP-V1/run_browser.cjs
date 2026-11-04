// Finite extension of REAL-LOOK-RENDERED-FIXTURE-V1's server/browser scaffold.
// One actual native app load per viewport; original 120s complete deadline.
const fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const assert = require('node:assert/strict'), crypto = require('node:crypto');
const [app, out, configFile] = process.argv.slice(2);
const config = JSON.parse(fs.readFileSync(configFile));
assert.equal(config.approved, true); fs.mkdirSync(out, { recursive: false });
const report = { passed: false, runs: [],
  scope: 'Actual native configured-pace observer; no equal-origin wheel, natural-stride, trusted-UI, consumer-FPS or photographic claim',
  visual_review_required: true, original_per_viewport_seconds: 120, original_outer_seconds: 600 };
const save = () => fs.writeFileSync(path.join(out, 'REPORT.json'), JSON.stringify(report, null, 2) + '\n');
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const mime = { '.html':'text/html', '.js':'text/javascript', '.mjs':'text/javascript', '.json':'application/json',
  '.glb':'model/gltf-binary', '.wasm':'application/wasm', '.png':'image/png', '.jpg':'image/jpeg', '.ktx2':'image/ktx2' };
let server, browser;
async function main() {
  const pw = require('/workspace/.cloud-setup/npm/node_modules/playwright');
  server = http.createServer((request, response) => {
    const pathname = new URL(request.url, 'http://native').pathname;
    const file = path.resolve(app, '.' + decodeURIComponent(pathname));
    if (!file.startsWith(path.resolve(app) + path.sep)) return response.writeHead(403).end();
    fs.readFile(file, (error, bytes) => {
      if (error) { (report.missing ??= []).push(pathname); return response.writeHead(404).end(); }
      response.setHeader('Content-Type', mime[path.extname(file)] ?? 'application/octet-stream');
      response.setHeader('Cache-Control', 'no-store'); response.end(bytes);
    });
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  for (const testCase of config.cases) {
    const started = Date.now(), deadline = started + 120000;
    const row = { ...testCase, passed: false, PNG_pairs: [] }; report.runs.push(row); save();
    const budget = () => { assert(Date.now() < deadline, 'Original complete120s viewport deadline exhausted'); return deadline - Date.now(); };
    const bounded = async (operation, label) => {
      let timer;
      try { return await Promise.race([operation(), new Promise((_, reject) => {
        timer = setTimeout(() => reject(Error(`Original120s viewport deadline: ${label}`)), budget());
      })]); } finally { clearTimeout(timer); }
    };
    let context, page, background;
    const errors = [];
    try {
      browser = await bounded(() => pw.chromium.launch({ executablePath: config.browser,
        args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }), 'browser launch');
      context = await bounded(() => browser.newContext({ viewport: testCase.viewport, deviceScaleFactor: 1,
        hasTouch: testCase.viewport.width === 390, isMobile: false, reducedMotion: 'no-preference' }), 'context');
      page = await context.newPage();
      page.on('pageerror', error => errors.push({ kind: 'pageerror', message: error.message }));
      page.on('requestfailed', request => errors.push({ kind: 'requestfailed', url: request.url(), failure: request.failure() }));
      page.on('response', response => { if (response.status() >= 400) errors.push({ kind: 'HTTP', url: response.url(), status: response.status() }); });
      await page.route('**/*', route => {
        const url = route.request().url();
        if (url.startsWith(origin + '/') || url.startsWith('blob:') || url.startsWith('data:')) return route.continue();
        errors.push({ kind: 'unexpected_remote', url }); return route.abort();
      });
      await page.addInitScript(() => { window.__MODULE_BASE = '/renderers/web/js/'; });
      await bounded(() => page.goto(`${origin}/renderers/web/index.html?year=${testCase.scene}&debug=1`,
        { waitUntil: 'domcontentloaded', timeout: budget() }), 'native app load');
      await bounded(() => page.waitForFunction(() => window.__chicago4d?.ready === true, null,
        { timeout: budget(), polling: 250 }), 'native ready');
      await bounded(() => page.addScriptTag({ path: path.join(__dirname, 'observer.js') }), 'outside observer injection');
      await bounded(() => page.evaluate(options => window.nativeElapsedObserver.initialize(options),
        { scene: testCase.scene, tier: testCase.tier, remaining_viewport_ms: budget() }), 'native assembly/camera admission');
      row.boot_and_admission_seconds = (Date.now() - started) / 1000;
      const screenshot = async name => {
        const file = `${testCase.scene}-${testCase.viewport.width}-${name}.png`;
        await bounded(() => page.screenshot({ path: path.join(out, file), timeout: Math.min(30000, budget()) }), name);
        const bytes = fs.readFileSync(path.join(out, file));
        return { file, bytes: bytes.length, sha256: sha(bytes) };
      };
      for (const fps of [1, 2, 4]) {
        await bounded(() => page.evaluate(() => window.nativeElapsedObserver.prepareWindow()), 'native held before-frame');
        const before = await screenshot(`${fps}fps-before`);
        const actual = await bounded(() => page.evaluate(fps => window.nativeElapsedObserver.runWindow(fps, 2), fps), `${fps}FPS real timer window`);
        const after = await screenshot(`${fps}fps-after`);
        row.PNG_pairs.push({ requested_fps: fps, before, after, actual_native_wall_seconds: actual.actual_native_wall_seconds,
          distance_m: actual.distance_m, identical_camera_recipe: true, pixel_ROI_threshold_used: false });
        save();
      }
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.beginControls()), 'control setup');
      for (const stoppedTick of [false, true]) await bounded(() => page.evaluate(value => window.nativeElapsedObserver.stopContinue(value), stoppedTick), 'native Stop/Continue');
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.hold()), 'native animation hold');
      await bounded(() => page.emulateMedia({ reducedMotion: 'reduce' }), 'actual reduced-motion preference');
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.heldStep('Reduced motion')), 'native reduced hold');
      await bounded(() => page.emulateMedia({ reducedMotion: 'no-preference' }), 'actual preference resume');
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.resumedStep('First actual reduced-motion resume')), 'native reduced resume');
      await bounded(() => page.emulateMedia({ reducedMotion: 'reduce' }), 'preference toggle');
      await bounded(() => page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve))), 'native preference event delivery without app tick');
      await bounded(() => page.emulateMedia({ reducedMotion: 'no-preference' }), 'preference toggle back');
      await bounded(() => page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve))), 'native preference return event delivery without app tick');
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.resumedStep('Reduced-motion toggles without held tick')), 'no-held-tick preference resume');
      background = await bounded(() => context.newPage(), 'actual background tab');
      await bounded(() => background.bringToFront(), 'actual page hide');
      assert.equal(await bounded(() => page.evaluate(() => document.hidden), 'native visibility read'), true,
        'Native hidden state unavailable; no document.hidden substitution is permitted');
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.heldStep('Actual hidden tab')), 'native hidden hold');
      await bounded(() => page.bringToFront(), 'actual page show');
      assert.equal(await page.evaluate(() => document.hidden), false);
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.resumedStep('First actual shown-page resume')), 'native shown resume');
      await bounded(() => background.close(), 'background cleanup'); background = null;
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.confidenceWithoutHeldTick()), 'native confidence hide/show');
      await bounded(() => page.evaluate(() => window.nativeElapsedObserver.range()), 'native range return');
      row.actual = await bounded(() => page.evaluate(() => window.nativeElapsedObserver.finish()), 'native final report');
      assert(row.actual.passed); assert.deepEqual(errors, []);
      row.cleanup = await bounded(() => page.evaluate(() => window.nativeElapsedObserver.cleanup()), 'native asset cleanup');
      assert(row.cleanup.passed); row.passed = true;
    } finally {
      row.page_errors = errors;
      try { if (page && !page.isClosed() && !row.cleanup) row.cleanup = await page.evaluate(() => window.nativeElapsedObserver?.cleanup()); } catch (error) { row.cleanup_error = String(error); }
      await background?.close(); await context?.close(); await browser?.close(); browser = null;
      row.viewport_elapsed_seconds = (Date.now() - started) / 1000; row.browser_closed = true; save();
    }
    assert(row.viewport_elapsed_seconds <= 120, 'Complete viewport exceeded original120s cap');
  }
  assert.equal(report.runs.length, 2); assert(report.runs.every(row => row.passed));
  assert.deepEqual(report.missing ?? [], []); report.passed = true;
}
main().catch(error => { report.error = String(error.stack ?? error); process.exitCode = 1; }).finally(async () => {
  await browser?.close(); if (server?.listening) await new Promise(resolve => server.close(resolve));
  report.browser_closed = true; report.server_closed = true; save();
  console.log(JSON.stringify({ passed: report.passed, runs: report.runs.length, error: report.error }));
});
