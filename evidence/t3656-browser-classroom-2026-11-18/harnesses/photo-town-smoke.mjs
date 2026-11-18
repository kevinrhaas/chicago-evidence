import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const app = '/workspace/chicago/chicago/4d';
const require = createRequire('/workspace/chicago/package.json');
const { chromium } = require('playwright');
const site = process.env.QA_ROOT || '/workspace/chicago/site/4d';
const source = process.env.QA_SOURCE === '1';
const out = process.env.QA_OUT || '/tmp/classroom-feature-smoke';
const widths = (process.env.QA_WIDTHS || '390,1280').split(',').map(Number);
const bootMs = Number(process.env.QA_BOOT_MS || 180000);
const onlyBoot = process.env.QA_BOOT_ONLY === '1';
const photoOnly = true;
const stepPhoto = true;
fs.mkdirSync(out, { recursive: true });
assert(fs.existsSync(path.join(site, source ? 'renderers/web/index.html' : 'walk/index.html')), `Missing ${source ? 'source' : 'published'} renderer at ${site}`);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.glb': 'model/gltf-binary', '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.ktx2': 'image/ktx2', '.webp': 'image/webp', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  let p;
  try { p = path.resolve(site, '.' + decodeURIComponent(new URL(req.url, 'http://local').pathname)); } catch { res.writeHead(400); res.end(); return; }
  if (!p.startsWith(site + path.sep) && p !== site) { res.writeHead(403); res.end(); return; }
  try {
    if (fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
    res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    fs.createReadStream(p).pipe(res);
  } catch { res.writeHead(404); res.end('missing ' + p.slice(site.length)); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || '/usr/bin/chromium', args: ['--no-sandbox', '--enable-unsafe-swiftshader'] });
const report = { started: new Date().toISOString(), site, source, runs: [] };
let activePage = null;
const log = (...args) => console.log(new Date().toISOString(), ...args);
async function waitBoot(page, row) {
  const begin = Date.now();
  await page.waitForFunction(() => {
    const api = window.__chicago4d;
    if (api?.ready) { api.renderer.setAnimationLoop(null); return true; }
    return !!api?.error;
  }, null, { timeout: bootMs, polling: 500 });
  const error = await page.evaluate(() => window.__chicago4d?.error ?? null);
  assert(!error, String(error));
  await page.waitForFunction(() => ['welcome', 'world'].includes(window.__chicago4d?.welcome?.state), null, { timeout: 90000, polling: 500 });
  await page.evaluate(() => { if (__chicago4d.welcome.state === 'welcome') __chicago4d.welcome.enter('spawn'); });
  await page.waitForFunction(() => window.__chicago4d?.welcome?.state === 'world', null, { timeout: 60000, polling: 250 });
  await page.evaluate(() => { __chicago4d.renderer.setAnimationLoop(null); });
  row.bootSeconds = (Date.now() - begin) / 1000;
  log(row.width, 'world ready', row.bootSeconds);
}
async function expand(page, selector) {
  await page.locator(selector).waitFor();
  await page.locator(selector).evaluate(el => { el.open = true; el.dispatchEvent(new Event('toggle')); });
}
async function runCheck(row, label, fn) {
  log(row.width, 'START', label);
  if (activePage) await holdDraws(activePage, true);
  try { const result = await fn(); row.checks.push({ label, pass: true, result }); log(row.width, 'PASS', label); }
  catch (error) {
    row.checks.push({ label, pass: false, error: String(error.stack || error) }); log(row.width, 'FAIL', label, error.message);
    if (activePage) {
      row.failureState = await activePage.evaluate(() => ({ captureError: window.__classroomCaptureError, photoStatus: document.querySelector('.moment-tools [role=status]')?.textContent, apiReady: __chicago4d.ready, welcomeState: __chicago4d.welcome.state, nav: __chicago4d.navigator.snapshot(), body: document.body.innerText.slice(-10000), notebook: document.getElementById('field-notebook')?.getBoundingClientRect().toJSON() })).catch(() => null);
      await activePage.screenshot({ path: path.join(out, `${row.width}-failure-${row.checks.length}.png`), timeout: 15000 }).catch(() => {});
    }
  }
}
async function holdDraws(page, on) {
  await page.evaluate(hold => {
    const renderer = __chicago4d.renderer;
    if (hold && !window.__classroomRealRender) {
      window.__classroomRealRender = renderer.render;
      renderer.render = (_scene, camera) => { camera?.updateMatrixWorld?.(); };
    } else if (!hold && window.__classroomRealRender) {
      renderer.render = window.__classroomRealRender;
      delete window.__classroomRealRender;
    }
  }, on);
}
try {
  for (const width of widths) {
    const phone = width < 600;
    const context = await browser.newContext({ viewport: { width, height: phone ? 780 : 800 }, deviceScaleFactor: 1, hasTouch: phone, isMobile: phone, reducedMotion: phone ? 'reduce' : 'no-preference', acceptDownloads: true });
    const row = { width, checks: [], errors: [], missing: [] };
    report.runs.push(row);
    // The ordinary audio settings mute this test; no audio assertions are made.
    await context.addInitScript(() => {
      window.print = () => { window.__classroomPrinted = (window.__classroomPrinted || 0) + 1; };
      if (!sessionStorage.getItem('classroom.smoke.seeded')) {
        localStorage.setItem('chicago4d.settings', JSON.stringify({ soundMaster: 0, detail: 'light', quality: 1 }));
        sessionStorage.setItem('classroom.smoke.seeded', '1');
      }
    });
    // Same explicit empty narration index used by the existing renderer smoke.
    const { standInNarrationIndex } = await import(app + '/tools/audio_smoke_replay.mjs');
    await standInNarrationIndex(context, { origin, root: app });
    const page = await context.newPage(); activePage = page; page.setDefaultTimeout(25000);
    page.on('pageerror', e => { row.errors.push(e.message); log(width, 'PAGEERROR', e.message); });
    page.on('response', r => { if (r.status() >= 400 && r.url().startsWith(origin)) row.missing.push({ url: r.url(), status: r.status() }); });
    try {
      const entry = source ? '/renderers/web/index.html?year=1835&detail=light' : '/1835/?detail=light';
      await page.goto(origin + entry, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await waitBoot(page, row);
      await holdDraws(page, true);
      log(width, 'DOM-only interactions: native renderer draws held as in existing smoke');
      row.renderer = await page.evaluate(() => ({ canvases: document.querySelectorAll('canvas').length, preserveDrawingBuffer: __chicago4d.renderer.getContext().getContextAttributes().preserveDrawingBuffer, year: __chicago4d.scene?.id ?? __chicago4d.scene?.scene_id }));
      if (!onlyBoot) {
        if (!photoOnly) {
        await runCheck(row, 'notebook save, literal text, download and persisted storage', async () => {
          await page.evaluate(() => __chicago4d.navigator.select('guide'));
          await expand(page, '#field-notebook');
          const note = page.locator('#field-notebook');
          await note.getByLabel('Title', { exact: true }).fill('Smoke field note');
          await note.getByLabel('My notes', { exact: true }).fill('Evidence <b>stays literal</b> & sources matter.');
          await note.getByRole('button', { name: 'Save note', exact: true }).click();
          await page.waitForFunction(() => document.querySelector('.field-notebook-entry')?.textContent.includes('Smoke field note'));
          assert.equal(await page.locator('.field-notebook-entry b').count(), 0);
          const downloadPromise = page.waitForEvent('download');
          await note.getByRole('button', { name: 'Download notebook', exact: true }).click();
          const download = await downloadPromise;
          const file = path.join(out, `${width}-notebook.html`); await download.saveAs(file);
          const html = fs.readFileSync(file, 'utf8');
          assert(html.includes('Smoke field note')); assert(html.includes('&lt;b&gt;'));
          const edit = page.locator('.field-notebook-entry').first();
          await edit.locator('textarea').fill('Edited evidence <b>stays literal</b>.');
          await edit.getByRole('button', { name: 'Save changes', exact: true }).click();
          await note.getByRole('button', { name: 'Print / save PDF', exact: true }).click();
          await page.locator('iframe.field-notebook-print-frame').waitFor({ state: 'attached' });
          await page.waitForFunction(() => !!document.querySelector('iframe.field-notebook-print-frame')?.contentWindow?.__classroomPrinted);
          const printText = await page.locator('iframe.field-notebook-print-frame').evaluate(el => el.contentDocument.body.textContent);
          assert(printText.includes('Edited evidence'));
          const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('chicago4d.notebook.v1')));
          await page.screenshot({ path: path.join(out, `${width}-notebook.png`) });
          return { bytes: fs.statSync(file).size, stored: saved };
        });
        await runCheck(row, 'lesson guide prepares real sources and print view', async () => {
          await page.evaluate(() => __chicago4d.navigator.select('guide'));
          await page.locator('#guide-lessons').getByRole('button', { name: 'Choose a lesson guide', exact: true }).click();
          await page.locator('[data-lesson-select="group"]').waitFor();
          await page.getByRole('button', { name: 'Prepare lesson', exact: true }).click();
          await page.locator('.lesson-guide').waitFor({ timeout: 45000 });
          const words = await page.locator('.lesson-guide').innerText();
          assert(words.length > 600);
          assert(/source|evidence/i.test(words));
          await page.getByRole('button', { name: 'Print or save as PDF', exact: true }).click();
          await page.locator('#lesson-print').waitFor({ state: 'attached' });
          assert(await page.evaluate(() => !!window.__classroomPrinted));
          const pdf = await page.pdf({ format: 'Letter', path: path.join(out, `${width}-lesson.pdf`) });
          assert(pdf.length > 1000);
          await page.evaluate(() => dispatchEvent(new Event('afterprint')));
          await page.screenshot({ path: path.join(out, `${width}-lesson.png`) });
          return { words: words.length, pdfBytes: pdf.length };
        });
        }
        await runCheck(row, 'photo capture and share link', async () => {
          await page.evaluate(() => __chicago4d.navigator.select('home'));
          await expand(page, '#nav-moment');
          const shutter = page.getByRole('button', { name: 'Take photo', exact: true });
          await shutter.waitFor({ state: 'visible' });
          // Restore the real renderer and request capture in ONE browser task. Otherwise
          // a held render can fulfill pendingPhoto with an already-cleared WebGL canvas.
          await shutter.evaluate((button, useStep) => {
            if (window.__classroomRealRender) {
              __chicago4d.renderer.render = window.__classroomRealRender;
              delete window.__classroomRealRender;
            }
            const capture = __chicago4d.moment.capture.bind(__chicago4d.moment);
            __chicago4d.moment.capture = () => capture().catch(error => {
              window.__classroomCaptureError = String(error.stack || error); throw error;
            });
            button.click();
            if (useStep) {
              __chicago4d.step();
              window.__classroomRealRender = __chicago4d.renderer.render;
              __chicago4d.renderer.render = (_scene, camera) => { camera?.updateMatrixWorld?.(); };
            }
          }, stepPhoto);
          await page.locator('img.moment-preview').waitFor({ state: 'visible', timeout: 45000 });
          await holdDraws(page, true);
          const picture = await page.locator('img.moment-preview').evaluate(i => {
            const canvas = document.createElement('canvas'); canvas.width = i.naturalWidth; canvas.height = i.naturalHeight;
            const ctx = canvas.getContext('2d'); ctx.drawImage(i, 0, 0);
            const data = ctx.getImageData(0, 0, canvas.width, canvas.height - 106).data;
            let lit = 0; const tones = new Set();
            for (let n = 0; n < data.length; n += 64) { if (data[n] + data[n + 1] + data[n + 2] > 30) lit++; tones.add(`${data[n] >> 4},${data[n + 1] >> 4},${data[n + 2] >> 4}`); }
            return { width: i.naturalWidth, height: i.naturalHeight, litFraction: lit / Math.ceil(data.length / 64), tones: tones.size };
          });
          assert(picture.width > 0 && picture.height > 0); assert(Math.max(picture.width, picture.height) <= 1280);
          assert(picture.litFraction > .1 && picture.tones > 8, `Native town photo must contain rendered content: ${JSON.stringify(picture)}`);
          const downloadPromise = page.waitForEvent('download');
          await page.getByRole('button', { name: 'Save picture', exact: true }).click();
          const download = await downloadPromise; const file = path.join(out, `${width}-moment.png`); await download.saveAs(file);
          assert(fs.readFileSync(file).subarray(1, 4).toString() === 'PNG');
          const moment = await page.evaluate(() => __chicago4d.moment.read());
          assert.equal(await page.evaluate(() => __chicago4d.renderer.getContext().getContextAttributes().preserveDrawingBuffer), false);
          row.share = { moment, url: await page.evaluate(() => __chicago4d.moment.link()) };
          await page.screenshot({ path: path.join(out, `${width}-photo.png`) });
          await holdDraws(page, true);
          return { picture, bytes: fs.statSync(file).size, url: row.share.url };
        });
        if (!photoOnly) {
        await runCheck(row, 'jaunt outcome three optional checks and retry', async () => {
          await page.evaluate(() => __chicago4d.navigator.select('jaunts'));
          await page.evaluate(() => __chicago4d.jaunts.start('across-wolf-point', { mode: 'instantly' }));
          for (let i = 0; i < 100; i++) {
            const state = await page.evaluate(() => { const j = __chicago4d.jaunts, s = j.state; return { phase: s?.phase, stop: s?.stopIndex, choice: s?.choice }; });
            if (state.phase === 'outcome') break;
            await page.evaluate(async () => {
              const j = __chicago4d.jaunts, s = j.state;
              if (s.phase === 'closing') { j.finish(); return; }
              if (s.phase === 'paused' || s.phase === 'travelling' || s.phase === 'opening') { j.straight(); __chicago4d.travel.simulate?.(600); return; }
              if (s.phase === 'atStop') {
                const stop = s.jaunt.stops.find(x => x.id === s.visited[s.stopIndex]?.id);
                if (stop?.choices?.length && !s.choice) j.choose(stop.choices[0].id);
                j.next();
              }
            });
            await page.waitForTimeout(200);
          }
          await page.waitForFunction(() => __chicago4d.jaunts.state.phase === 'outcome', null, { timeout: 45000 });
          await expand(page, 'details.jaunt-understanding');
          assert.equal(await page.locator('textarea[data-check-answer]').count(), 3);
          await page.locator('textarea[data-check-answer="0"]').fill('The source supports this claim.');
          await page.getByRole('button', { name: 'Compare with the sources', exact: true }).first().click();
          await page.getByRole('button', { name: 'Revise your answer', exact: true }).first().click();
          assert.equal(await page.locator('textarea[data-check-answer="0"]').inputValue(), 'The source supports this claim.');
          await page.screenshot({ path: path.join(out, `${width}-checks.png`) });
          return await page.locator('details.jaunt-understanding').innerText();
        });
        }
        if (true) {
        await runCheck(row, 'shared moment restores and notebook survives page navigation', async () => {
          assert(row.share?.url, 'No share URL captured');
          row.savedJaunt = await page.evaluate(async () => {
            const base = location.pathname.includes('/renderers/web/') ? '../../data/' : '../data/';
            const doc = await fetch(new URL(base + 'sidecars/1835/jaunts/across-wolf-point.json', location.href)).then(r => r.json());
            const saved = JSON.stringify({ content_version: doc.content_version, jaunt: doc.id, events: [] });
            localStorage.setItem('c4d.jaunt.session.v1', saved); return saved;
          });
          await page.goto(row.share.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
          await waitBoot(page, row);
          await holdDraws(page, true);
          await page.waitForFunction(() => !!__chicago4d.momentRestored, null, { timeout: 30000 });
          const after = await page.evaluate(() => ({ restored: __chicago4d.momentRestored, moment: __chicago4d.moment.read(), notebook: localStorage.getItem('chicago4d.notebook.v1') }));
          assert(Math.abs(after.moment.e - row.share.moment.e) < 1); assert(Math.abs(after.moment.n - row.share.moment.n) < 1);
          assert.equal(after.moment.season, row.share.moment.season);
          assert.equal(await page.evaluate(() => localStorage.getItem('c4d.jaunt.session.v1')), row.savedJaunt, 'Shared arrival retains saved outing');
          assert.equal(await page.evaluate(() => __chicago4d.jaunts.state?.jaunt ?? null), null, 'Saved outing does not auto-resume');
          if (!photoOnly) assert(after.notebook?.includes('Smoke field note'));
          return after;
        });
        }
      }
      await runCheck(row, 'zero page errors, no missing local resources, no horizontal overflow', async () => {
        assert.deepEqual(row.errors, []); assert.deepEqual(row.missing, []);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        assert.equal(row.renderer.preserveDrawingBuffer, false);
        return row.renderer;
      });
    } catch (error) {
      row.fatal = String(error.stack || error);
      row.bootState = await page.evaluate(() => ({ error: window.__chicago4d?.error, gate: document.getElementById('gate')?.innerText.slice(0, 2000), title: document.title })).catch(() => null);
      log(width, 'FATAL', error.message);
      await page.screenshot({ path: path.join(out, `${width}-fatal.png`), timeout: 15000 }).catch(() => {});
    } finally { await context.close(); fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2)); }
  }
} finally { await browser.close(); await new Promise(r => server.close(r)); }
const failed = report.runs.some(r => r.fatal || r.checks.some(c => !c.pass));
log(failed ? 'FAIL' : 'PASS', path.join(out, 'report.json'));
process.exitCode = failed ? 1 : 0;
