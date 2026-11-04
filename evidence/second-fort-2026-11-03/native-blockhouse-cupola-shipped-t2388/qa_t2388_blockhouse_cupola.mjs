// T-2388 review: the second fort blockhouse's cupola, in the published app, at one viewport.
//   QA_VIEW=1280x800 QA_OUT=/tmp/t2388-desktop node /tmp/qa_t2388.mjs
import fs from 'node:fs';
import os from 'node:os';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';
const root = process.cwd(), require = createRequire(path.join(root, 'tools/smoke_renderer.mjs'));
let chromium; try { ({ chromium } = require('playwright')); } catch { ({ chromium } = await import('/opt/node-tools/node_modules/playwright/index.mjs')); }
const site = path.resolve(root, process.env.QA_SITE || '../../site/4d');
const out = process.env.QA_OUT || path.join(os.tmpdir(), 't2388');
const [vw, vh] = (process.env.QA_VIEW || '1280x800').split('x').map(Number);
fs.mkdirSync(out, { recursive: true });
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.glb': 'model/gltf-binary', '.svg': 'image/svg+xml', '.ktx2': 'image/ktx2', '.wasm': 'application/wasm', '.webp': 'image/webp', '.bin': 'application/octet-stream' };
const miss = [];
const server = http.createServer((req, res) => {
  let p = path.join(site, decodeURIComponent(req.url.split('?')[0]));
  try { if (fs.statSync(p).isDirectory()) p = path.join(p, 'index.html'); res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream', 'Cache-Control': 'no-store' }); fs.createReadStream(p).pipe(res); }
  catch { miss.push(req.url.split('?')[0]); res.writeHead(404); res.end('missing'); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || undefined, args: ['--no-sandbox', '--enable-unsafe-swiftshader'] });
const errors = [];
try {
  const context = await browser.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: 1, isMobile: vw < 600, hasTouch: vw < 600 });
  const page = await context.newPage(); page.setDefaultTimeout(600000);
  page.on('pageerror', (e) => errors.push('pageerror: ' + String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('requestfailed', (r) => errors.push('requestfailed: ' + r.url().split('?')[0]));
  page.on('response', (r) => { if (r.status() >= 400) errors.push('http ' + r.status() + ': ' + r.url().split('?')[0]); });
  await page.goto(`http://127.0.0.1:${server.address().port}/1835/`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.__chicago4d?.ready || window.__chicago4d?.error, null, { timeout: 600000, polling: 1000 });
  await page.waitForFunction(() => window.__chicago4d?.welcome?.state === 'welcome', null, { timeout: 600000, polling: 1000 });
  await page.evaluate(() => { const a = __chicago4d; a.welcome.enter('spawn'); document.exitPointerLock?.(); document.getElementById('control-help-gotit')?.click(); a.renderer.setAnimationLoop(null); a.step(); });

  // Stand south-west of the blockhouse, outside the stockade, looking at its corner.
  const stand = await page.evaluate(() => {
    const a = __chicago4d;
    const r = a.registry.get('fort_dearborn_blockhouse');
    const p = r?.sidecar?.placement ?? {};
    const e = p.local_e, n = p.local_n;
    a.setFly?.(false); a.walker.teleport({ local_e: e - 19, local_n: n - 15, yaw_deg: 52, pitch_deg: 10 });
    for (let i = 0; i < 6; i++) a.step();
    return { e, n, grade: r?.sidecar?.grade?.value, why: r?.sidecar?.grade?.why,
             asset: r?.sidecar?.asset, flying: a.player?.flying,
             at: { e: a.player?.e, n: a.player?.n, y: a.player?.y } };
  });
  await page.waitForTimeout(1200);
  await page.evaluate(() => { __chicago4d.step(); __chicago4d.step(); });
  await page.screenshot({ path: path.join(out, `blockhouse-normal-${vw}.jpg`), quality: 85, timeout: 240000 });

  await page.keyboard.press('KeyC');
  await page.waitForTimeout(900);
  await page.evaluate(() => { __chicago4d.step(); __chicago4d.step(); });
  await page.screenshot({ path: path.join(out, `blockhouse-bygrade-${vw}.jpg`), quality: 85, timeout: 240000 });
  await page.keyboard.press('KeyC');
  await page.waitForTimeout(600);

  // The card: Record, then Images.
  const card = await page.evaluate(async () => {
    const a = __chicago4d;
    a.pick('fort_dearborn_blockhouse');
    await new Promise((r) => setTimeout(r, 2500));
    const tabs = [...document.querySelectorAll('#popup .pop-tab')].map((t) => t.dataset.popTab);
    document.querySelector('#popup [data-pop-tab="record"]')?.click();
    return { tabs, open: !!document.querySelector('#popup') && getComputedStyle(document.getElementById('popup')).display };
  });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(out, `card-record-${vw}.jpg`), quality: 85, timeout: 240000 });
  const pics = await page.evaluate(async () => {
    const t = document.querySelector('#popup [data-pop-tab="pictures"]') || document.querySelector('#popup [data-pop-tab="images"]');
    t?.click();
    await new Promise((r) => setTimeout(r, 2500));
    const pane = document.querySelector('#popup .pop-pane');
    return { clicked: t?.dataset?.popTab ?? null, text: (pane?.innerText ?? '').slice(0, 900) };
  });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(out, `card-images-${vw}.jpg`), quality: 85, timeout: 240000 });
  console.log(JSON.stringify({ stand, card, pics, viewport: `${vw}x${vh}` }, null, 1));
} finally {
  await browser.close(); server.close();
  console.log('ERRORS:', errors.length ? errors.slice(0, 20).join(' | ') : 'none');
  console.log('404s:', miss.length ? [...new Set(miss)].slice(0, 10).join(' | ') : 'none');
}
