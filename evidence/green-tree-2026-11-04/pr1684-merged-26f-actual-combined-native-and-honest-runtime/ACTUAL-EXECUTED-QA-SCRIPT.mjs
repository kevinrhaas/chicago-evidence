// Both-viewport published-app review of the Green Tree Tavern at its stand (T-2376).
// usage: node /tmp/qa-t2376/qa_green_tree_t2376.mjs <repoRoot-chicago/4d> <outDir>
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

const root = process.argv[2];
const out = process.argv[3];
fs.mkdirSync(out, { recursive: true });
const require = createRequire(path.join(root, 'tools/qa.mjs'));
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }
const site = path.resolve(root, '../../site/4d');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.glb': 'model/gltf-binary', '.ktx2': 'image/ktx2', '.svg': 'image/svg+xml', '.wasm': 'application/wasm' };
const serverMisses = [];
const server = http.createServer((req, res) => {
  let p = path.join(site, decodeURIComponent(req.url.split('?')[0]));
  try {
    if (fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
    res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    fs.createReadStream(p).pipe(res);
  } catch { serverMisses.push(req.url); res.writeHead(404); res.end('missing'); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const results = [];
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || undefined, args: ['--no-sandbox', '--enable-unsafe-swiftshader'] });
try {
  for (const [label, viewport, detail] of [['desktop', { width: 1280, height: 800 }, 'full'], ['mobile', { width: 390, height: 780 }, 'light']]) {
    const context = await browser.newContext({ viewport, deviceScaleFactor: 1, isMobile: label === 'mobile', hasTouch: label === 'mobile' });
    const page = await context.newPage();
    page.setDefaultTimeout(300000);
    const pageErrors = [], consoleErrors = [], badResponses = [], failedRequests = [];
    page.on('pageerror', (e) => pageErrors.push(String(e)));
    page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
    page.on('response', (r) => { if (r.status() >= 400) badResponses.push(`${r.url()}:${r.status()}`); });
    page.on('requestfailed', (r) => failedRequests.push(`${r.url()}:${r.failure()?.errorText}`));
    await page.goto(`http://127.0.0.1:${port}/1835/`, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => window.__chicago4d?.ready || window.__chicago4d?.error, null, { timeout: 300000, polling: 1000 });
    const boot = await page.evaluate(() => ({ ready: !!__chicago4d.ready, error: __chicago4d.error ?? null, scene: __chicago4d.scene?.id }));
    await page.waitForFunction(() => window.__chicago4d?.welcome?.state === 'welcome', null, { timeout: 300000, polling: 1000 });
    await page.evaluate(async (d) => {
      const a = __chicago4d;
      a.welcome.enter('spawn');
      document.exitPointerLock?.();
      document.getElementById('control-help-gotit')?.click();
      a.renderer.setAnimationLoop(null);
      if (a.setDetail) await a.setDetail(d);
      a.step();
    }, detail);
    const obs = await page.evaluate(() => {
      const a = __chicago4d;
      a.goTo('green_tree');
      for (let i = 0; i < 6; i++) a.step();
      a.renderer.render(a.scene3d, a.camera);
      let found = null;
      a.scene3d.traverse((o) => {
        const n = String(o.name || '');
        if (!/green_tree/i.test(n)) return;
        if (!o.geometry) return;
        o.geometry.computeBoundingBox?.();
        const bb = o.geometry.boundingBox;
        if (!bb) return;
        found = found || { name: n, minY: Infinity, maxY: -Infinity, meshes: 0 };
        found.meshes += 1;
        found.minY = Math.min(found.minY, bb.min.y);
        found.maxY = Math.max(found.maxY, bb.max.y);
      });
      const st = a.stats?.() ?? {};
      return {
        detail: a.detail,
        where: a.hud?.whereAmI?.() ?? a.walker?.position ?? null,
        greenTree: found,
        problems: (a.problems ?? []).filter((p) => /green_tree|green tree/i.test(String(p))),
        stats: { withinBudget: st.withinBudget, triangles: st.triangles, drawCalls: st.drawCalls ?? st.calls },
      };
    });
    await page.waitForTimeout(600);
    await page.evaluate(() => { __chicago4d.step(); __chicago4d.renderer.render(__chicago4d.scene3d, __chicago4d.camera); });
    await page.screenshot({ path: path.join(out, `t2376-green-tree-${label}.jpg`), type: 'jpeg', quality: 82, timeout: 240000 });
    const row = { label, viewport, boot, ...obs, pageErrors, consoleErrors, badResponses, failedRequests };
    results.push(row);
    console.log(`${label}: boot=${boot.ready ? 'ready' : 'FAIL'} scene=${boot.scene} greenTree=${JSON.stringify(obs.greenTree)} pageErrors=${pageErrors.length} consoleErrors=${consoleErrors.length} bad=${badResponses.length} failed=${failedRequests.length} problems=${obs.problems.length}`);
    await context.close();
  }
} finally {
  fs.writeFileSync(path.join(out, 'browser-validation-t2376.json'),
    JSON.stringify({ method: 'Published /1835/ app from the site/4d mirror this tree publishes; normal boot, animation paused, goTo(green_tree).', serverMisses, results }, null, 2) + '\n');
  await browser.close();
  server.close();
}
const bad = results.filter((r) => !r.boot.ready || r.pageErrors.length || r.consoleErrors.length || r.badResponses.length || r.failedRequests.length);
console.log(serverMisses.length ? `server 404s: ${serverMisses.length}` : 'server 404s: 0');
if (bad.length) { console.log('QA FAIL'); process.exit(1); }
console.log('QA PASS — both viewports clean');
