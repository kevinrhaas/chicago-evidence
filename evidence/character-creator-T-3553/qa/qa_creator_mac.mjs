// Character creator QA (T-3553): boots the dev preview with this branch's files routed over it,
// opens the creator and shoots each category, desktop and phone. Run from this folder:
//   node qa_creator_mac.mjs            (needs playwright; uses the Mac GPU, no SwiftShader)
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
let playwright;
for (const base of [here, path.join(here, '..'), process.cwd()]) { try { playwright = createRequire(path.join(base, 'x.js'))('playwright'); break; } catch {} }
if (!playwright) { console.error('playwright not found: npm i playwright in this folder'); process.exit(2); }
const files = path.join(here, 'files');
const out = path.join(here, 'shots'); fs.mkdirSync(out, { recursive: true });
const log = (...a) => { const s = a.join(' '); console.log(s); fs.appendFileSync(path.join(out, 'log.txt'), s + '\n'); };
const browser = await playwright.chromium.launch({ headless: true, args: ['--ignore-gpu-blocklist', '--enable-gpu'] });
async function run(name, width, height, dsf, person, route = true) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dsf });
  if (route) await ctx.route('**/4d/dev/**', async (r) => {
    const rel = new URL(r.request().url()).pathname.replace(/^\/4d\/dev\//, '');
    let local = null;
    if (rel.startsWith('walk/js/')) local = path.join(files, 'renderers/web/js', rel.slice(8));
    else if (rel.startsWith('walk/css/')) local = path.join(files, 'renderers/web/css', rel.slice(9));
    if (local && fs.existsSync(local)) {
      const type = local.endsWith('.js') ? 'text/javascript' : 'text/css';
      return r.fulfill({ status: 200, body: fs.readFileSync(local), headers: { 'content-type': type, 'cache-control': 'no-store' } });
    }
    return r.continue();
  });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => log(name, 'PAGEERROR', e.message));
  page.on('console', (m) => { if (m.type() === 'error' || /person|portrait|creator/i.test(m.text())) log(name, 'CONSOLE', m.text().slice(0, 300)); });
  await page.addInitScript((p) => { try { localStorage.setItem('chicago4d.person', JSON.stringify({ saved: '2026-11-27T00:00:00Z', ...p })); localStorage.setItem('chicago4d.tour.done', '1'); } catch {} }, person);
  const t0 = Date.now();
  await page.goto('https://dev.chicago.polecat.live/4d/dev/walk/index.html?year=1904', { timeout: 180000 });
  await page.waitForFunction(() => window.__chicago4d?.ready === true, null, { timeout: 15 * 60_000, polling: 1000 });
  log(name, 'ready', (Date.now() - t0) / 1000);
  for (let i = 0; i < 30; i++) {
    const s = await page.evaluate(() => { try { window.__chicago4d.welcome.enter('spawn'); } catch {} return window.__chicago4d.welcome?.state; });
    if (s === 'world') break;
    await page.waitForTimeout(1000);
  }
  await page.evaluate(() => document.exitPointerLock?.());
  await page.waitForFunction(() => !!window.__chicago4d.personSettings && !!window.__chicago4d.humans?.createActor, null, { timeout: 300000 });
  if (!route) { await ctx.close(); return; }
  const t1 = Date.now();
  await page.evaluate(() => window.__chicago4d.personSettings.openCreator('body'));
  const settle = () => page.evaluate(() => window.__chicago4d.personSettings.creator.settle());
  await settle(); log(name, 'body settled', (Date.now() - t1) / 1000);
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(out, `${name}-1-body.png`) });
  for (const [i, tab] of [[2, 'face'], [3, 'skin'], [4, 'hair'], [5, 'clothes']]) {
    const t = Date.now();
    await page.click(`.pc-tab[data-tab="${tab}"]`);
    await page.waitForTimeout(200); await settle();
    log(name, tab, 'settled', (Date.now() - t) / 1000);
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(out, `${name}-${i}-${tab}.png`) });
  }
  // A turn: time a drag's worth of turns on the figure already built.
  const turns = await page.evaluate(async () => {
    const c = window.__chicago4d.personSettings.creator, v = document.querySelector('.pc-view');
    const p = window.__chicago4d.personSettings; const t = performance.now();
    const b = v.getBoundingClientRect(); const x0 = b.left + b.width / 2, y = b.top + b.height / 2;
    v.dispatchEvent(new PointerEvent('pointerdown', { clientX: x0, clientY: y, pointerId: 7, bubbles: true }));
    let frames = 0; const longest = { ms: 0 }; let last = performance.now();
    await new Promise((done) => { const step = () => { const now = performance.now(); longest.ms = Math.max(longest.ms, now - last); last = now; frames++;
      v.dispatchEvent(new PointerEvent('pointermove', { clientX: x0 + frames * 6, clientY: y, pointerId: 7, bubbles: true }));
      if (frames < 60) requestAnimationFrame(step); else done(); }; requestAnimationFrame(step); });
    v.dispatchEvent(new PointerEvent('pointerup', { clientX: x0 + 360, clientY: y, pointerId: 7, bubbles: true }));
    await c.settle();
    return { ms: performance.now() - t, frames, longestFrameMs: longest.ms };
  });
  log(name, 'drag', JSON.stringify(turns));
  await page.screenshot({ path: path.join(out, `${name}-6-turned.png`) });
  await page.click('.pc-tab[data-tab="clothes"]');
  await page.click('.pc-seg [data-frame="face"]'); await page.waitForTimeout(300); await settle(); await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(out, `${name}-7-face-zoom.png`) });
  await page.click('.pc-seg [data-frame="whole"]');
  // Randomize three times, shot each.
  for (let k = 0; k < 3; k++) {
    const t = Date.now();
    await page.click('.pc-roll'); await page.waitForTimeout(300); await settle(); await page.waitForTimeout(800);
    log(name, 'roll', k, (Date.now() - t) / 1000, await page.evaluate(() => JSON.stringify(window.__chicago4d.person.choice).slice(0, 160)));
    await page.screenshot({ path: path.join(out, `${name}-8-roll${k}.png`) });
  }
  log(name, 'stats', await page.evaluate(() => JSON.stringify(window.__chicago4d.personPortrait?.stats?.())));
  await page.click('.pc-done'); await page.waitForTimeout(1500);
  await ctx.close();
}
try { await run('desk', 1280, 800, 2, {}); } catch (e) { log('desk', 'FAILED', e.message); }
try { await run('phone', 390, 780, 2, { sex: 'female' }); } catch (e) { log('phone', 'FAILED', e.message); }
await browser.close();
log('done');
