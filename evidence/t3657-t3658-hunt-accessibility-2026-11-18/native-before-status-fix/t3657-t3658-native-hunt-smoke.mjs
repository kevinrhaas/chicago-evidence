/** Focused native integration only. Run ONE viewport after the owner grants a browser window.
 * No publish, source mutations, route mocks, alternate images, or second simultaneous world.
 * Continuous software-GPU drawing pauses between UI interactions; actual api.step() frames
 * are drawn for town screenshots. Travel uses the existing public Instantly mode.
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const app = path.resolve(process.env.QA_APP || '/workspace/chicago-hunt/chicago/4d');
assert(process.env.QA_ROOT, 'QA_ROOT must name the frozen published COMBINED runtime');
const site = path.resolve(process.env.QA_ROOT);
const widths = (process.env.QA_WIDTHS || '').split(',').map(Number);
assert(widths.length === 1 && [390, 1280].includes(widths[0]), 'Exactly one QA_WIDTHS=390 or QA_WIDTHS=1280 per run');
const width = widths[0], height = width === 390 ? 780 : 800;
const out = path.resolve(process.env.QA_OUT || `/tmp/t3657-t3658-native-${width}`);
const day = process.env.QA_DAY || '2026-11-18';
assert(/^20\d{2}-\d{2}-\d{2}$/.test(day));
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const commit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: app, encoding: 'utf8' }).trim();
if (process.env.QA_EXPECT_COMMIT) assert.equal(commit, process.env.QA_EXPECT_COMMIT);
const testedFiles = {};
for (const relative of [
  'js/main.js', 'js/apps/home.js', 'js/photo-hunt.js', 'js/photo-hunt-view.js', 'js/strings/photo-hunt.js',
  'js/destinations.js', 'js/photos-tab.js', 'js/pictures.js', 'js/viewport.js', 'js/controls/touch.js',
  'js/navigator.js', 'js/travel.js', 'js/show-me.js', 'js/human-spacing.js', 'js/house-barriers.js',
  'js/moment.js', 'js/moment-view.js', 'js/field-notebook.js', 'js/field-notebook-view.js', 'js/apps/guide.js',
  'js/strings/moment.js', 'js/strings/notebook.js', 'css/moment.css', 'css/field-notebook.css',
  'css/photo-hunt.css', 'css/navigator.css', 'css/card.css',
]) {
  const source = digest(fs.readFileSync(path.join(app, 'renderers/web', relative)));
  const published = digest(fs.readFileSync(path.join(site, 'walk', relative)));
  assert.equal(published, source, `Published runtime differs from ${commit}: ${relative}`);
  testedFiles[`walk/${relative}`] = published;
}
for (const relative of ['walk/index.html', '1904/index.html', 'data/pictures/1904.json'])
  testedFiles[relative] = digest(fs.readFileSync(path.join(site, relative)));
const evidenceRoot = '/tmp/t3657-photo-evidence';
const photoReceipts = JSON.parse(fs.readFileSync(path.join(evidenceRoot, 'fetch-receipts.json')));
const photoAudit = digest(fs.readFileSync(path.join(evidenceRoot, 'visual-review.json')));
const { chromium } = createRequire('/workspace/chicago/package.json')('playwright');
fs.mkdirSync(out, { recursive: true });
const row = { width, height, checks: [], errors: [], httpErrors: [], requestFailures: [], cancelledRequests: [], photoResponses: [], bootSeconds: [] };
const report = {
  started: new Date().toISOString(), sourceCommit: commit, site, app, testedFiles,
  harness: { path: fileURLToPath(import.meta.url), sha256: digest(fs.readFileSync(fileURLToPath(import.meta.url))) },
  photoVisualAudit: { directory: evidenceRoot, sha256: photoAudit },
  scope: 'Published 1904 Home hunt, real hosted photographs, all five live safety decisions, real permitted visit, reload, native modal and phone zoom, actual photo capture and notebook storage',
  limits: [
    'One page/world and one viewport per invocation. Continuous software-GPU draws paused between interactions; selected frames use the actual normal step.',
    'Instantly is the real production travel mode used for the visit; this does not certify every walking route or ride.',
    'One-image assertion applies to the hunt owner; an explicit visit opens the existing Inspect photo gallery and its own images.',
    'Chromium emulated viewport/touch, not a physical device, whole-app WCAG audit, sustained performance test, or complete release gate.',
    'No network or image substitutes. Source-date strings and structured ranges are preserved separately from world year 1904.',
    'Photo caption measurement counts delegate the real browser methods. Capture elapsed time includes the normal rendered frame and PNG encoding; it is not a rendering benchmark.',
    'A public programmatic pick selects an existing canonical building record for the capture. Full metadata citations are retained; the notebook applies its existing bounded source-row format.',
  ], runs: [row],
};
const save = () => fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
save();
const log = (...args) => console.log(new Date().toISOString(), width, ...args);
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.glb': 'model/gltf-binary',
  '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.ktx2': 'image/ktx2', '.webp': 'image/webp', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  try {
    let file = path.resolve(site, '.' + decodeURIComponent(new URL(req.url, 'http://local').pathname));
    if (!file.startsWith(site + path.sep) && file !== site) { res.writeHead(403); res.end(); return; }
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    fs.createReadStream(file).pipe(res);
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
let browser, context, page;
const responseTasks = [];
const check = async (label, fn) => {
  log('START', label);
  try { const result = await fn(); row.checks.push({ label, pass: true, result }); save(); log('PASS', label); return result; }
  catch (error) { row.checks.push({ label, pass: false, error: String(error.stack || error) }); save(); throw error; }
};
async function boot() {
  const start = Date.now();
  await page.waitForFunction(() => {
    if (window.__chicago4d?.ready) { __chicago4d.renderer.setAnimationLoop(null); return true; }
    return !!window.__chicago4d?.error;
  }, null, { timeout: 240000, polling: 500 });
  assert.equal(await page.evaluate(() => __chicago4d.error ?? null), null);
  await page.waitForFunction(() => ['welcome', 'world'].includes(__chicago4d.welcome?.state), null, { timeout: 60000, polling: 500 });
  await page.evaluate(() => { if (__chicago4d.welcome.state === 'welcome') __chicago4d.welcome.enter('spawn'); });
  await page.waitForFunction(() => __chicago4d.welcome.state === 'world', null, { timeout: 60000, polling: 500 });
  await page.evaluate(() => {
    __chicago4d.renderer.setAnimationLoop(null);
    window.__qaRealRender = __chicago4d.renderer.render;
    __chicago4d.renderer.render = (_scene, camera) => { camera?.updateMatrixWorld?.(); };
  });
  row.bootSeconds.push((Date.now() - start) / 1000); save(); log('BOOT', row.bootSeconds.at(-1));
}
async function realFrame(name) {
  await page.evaluate(() => {
    __chicago4d.renderer.render = window.__qaRealRender;
    try { __chicago4d.step(); }
    finally { __chicago4d.renderer.render = (_scene, camera) => { camera?.updateMatrixWorld?.(); }; }
  });
  await page.screenshot({ path: path.join(out, `${width}-${name}.png`) });
}
async function openHunt() {
  await page.evaluate(async () => { await __chicago4d.navigator.select('home'); __chicago4d.navigator.open(2); });
  const details = page.locator('#nav-photo-hunt');
  await details.locator('summary').waitFor({ state: 'visible' });
  if (!(await details.evaluate(el => el.open))) await details.locator('summary').click();
  const open = details.getByRole('button', { name: 'Open five-photo hunt', exact: true });
  if (await open.count()) {
    const intro = await details.innerText();
    assert(intro.includes('Their dates differ from the world’s year.'));
    row.intro = intro;
    await open.click();
  }
  await details.locator('.photo-hunt-image').waitFor({ state: 'visible' });
  await page.waitForFunction(() => { const img = document.querySelector('.photo-hunt-image'); return img?.complete && img.naturalWidth > 0; });
}
const hunt = () => page.locator('.photo-hunt');
const button = name => hunt().getByRole('button', { name, exact: true });
const progress = () => page.evaluate(() => localStorage.getItem('chicago4d.photoHunt.v1'));
const pose = () => page.evaluate(() => ({ e: __chicago4d.walker.state.e, n: __chicago4d.walker.state.n,
  bearing: __chicago4d.walker.bearingDeg, pitch: __chicago4d.walker.state.pitch, flying: __chicago4d.walker.state.flying }));
async function oneImage(round) {
  await page.waitForFunction(() => { const el = document.querySelector('.photo-hunt-image'); return el?.complete && el.naturalWidth > 0; });
  const facts = await hunt().locator('img').evaluate(async image => {
    await image.decode(); return { src: image.currentSrc, width: image.naturalWidth, height: image.naturalHeight };
  });
  assert.equal(facts.src, round.image);
  assert.equal(await page.locator('.photo-hunt-image[src]').count(), 1);
  assert(Math.max(facts.width, facts.height) <= 480 && Math.min(facts.width, facts.height) > 1);
  const credit = await hunt().locator('figcaption').innerText();
  assert(credit.includes(round.credit)); assert(credit.includes(round.rights));
  return { ...facts, credit };
}
async function imagePixels(locator, footer = 0) {
  return locator.evaluate(async (image, footer) => {
    await image.decode();
    const canvas = document.createElement('canvas'); canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
    const ctx = canvas.getContext('2d'); ctx.drawImage(image, 0, 0);
    const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height - footer).data;
    let lit = 0; const tones = new Set();
    for (let i = 0; i < pixels.length; i += 64) {
      if (pixels[i] + pixels[i + 1] + pixels[i + 2] > 30) lit++;
      tones.add(`${pixels[i] >> 4},${pixels[i + 1] >> 4},${pixels[i + 2] >> 4}`);
    }
    const result = { width: canvas.width, height: canvas.height, litFraction: lit / Math.ceil(pixels.length / 64), tones: tones.size };
    canvas.width = canvas.height = 1; return result;
  }, footer);
}
async function photoAndNotebook() {
  const details = page.locator('#nav-moment');
  if (!(await details.evaluate(el => el.open))) await details.locator('summary').click();
  const shutter = page.locator('.moment-tools').getByRole('button', { name: 'Take photo', exact: true });
  await shutter.waitFor({ state: 'visible' });
  const fallbackOwner = row.rounds.find(round => round.id === row.visit.id).structure;
  const selected = await page.evaluate(fallback => {
    const api = __chicago4d, id = api.registry.has('glessner_house') ? 'glessner_house' : fallback;
    const record = api.registry.get(id)?.sidecar;
    if (!record) return null;
    const picked = api.pick(id);
    return picked ? { id, name: record.name } : null;
  }, fallbackOwner);
  assert(selected, 'An existing canonical building must be selected; never fabricate capture metadata');
  const relative = `data/sidecars/1904/${selected.id}.json`;
  const canonicalBytes = fs.readFileSync(path.join(site, relative)); testedFiles[relative] = digest(canonicalBytes);
  const record = JSON.parse(canonicalBytes);
  const canonicalSources = (record.citations ?? []).filter(source => source.source_id && source.citation)
    .map(source => ({ id: source.source_id, title: source.citation, url: source.url || source.archived_url || '' }));
  assert(canonicalSources.length, 'Selected canonical record has actual citations');
  await shutter.evaluate(button => {
    const api = __chicago4d, proto = CanvasRenderingContext2D.prototype;
    const originalMeasure = proto.measureText, originalDraw = proto.drawImage, originalCapture = api.moment.capture;
    const captionContexts = new WeakSet();
    const stats = window.__qaCaption = { measureTextCalls: 0, captionMeasureTextCalls: 0, captionContexts: 0,
      measureTextMilliseconds: 0, captionMeasureTextMilliseconds: 0, maxMeasuredChars: 0, captionMaxMeasuredChars: 0,
      started: performance.now(), finished: false };
    proto.drawImage = function(source, ...args) {
      if (source === api.renderer.domElement && !captionContexts.has(this)) {
        captionContexts.add(this); stats.captionContexts++;
      }
      return Reflect.apply(originalDraw, this, [source, ...args]);
    };
    proto.measureText = function(text, ...args) {
      const caption = captionContexts.has(this), chars = typeof text === 'string' ? text.length : 0;
      stats.measureTextCalls++; stats.maxMeasuredChars = Math.max(stats.maxMeasuredChars, chars);
      if (caption) { stats.captionMeasureTextCalls++; stats.captionMaxMeasuredChars = Math.max(stats.captionMaxMeasuredChars, chars); }
      const start = performance.now();
      try { return Reflect.apply(originalMeasure, this, [text, ...args]); }
      finally {
        const elapsed = performance.now() - start; stats.measureTextMilliseconds += elapsed;
        if (caption) stats.captionMeasureTextMilliseconds += elapsed;
      }
    };
    api.moment.capture = function(...args) {
      return Reflect.apply(originalCapture, this, args).then(photo => {
        const { blob, ...metadata } = photo;
        window.__qaMomentMetadata = metadata; stats.pngBytes = blob.size; stats.mime = blob.type;
        return photo;
      }).finally(() => {
        proto.measureText = originalMeasure; proto.drawImage = originalDraw; api.moment.capture = originalCapture;
        stats.elapsedMilliseconds = performance.now() - stats.started; stats.finished = true;
      });
    };
    api.renderer.render = window.__qaRealRender;
    button.click();
    try { api.step(); }
    finally { api.renderer.render = (_scene, camera) => { camera?.updateMatrixWorld?.(); }; }
  });
  const preview = page.locator('img.moment-preview'); await preview.waitFor({ state: 'visible', timeout: 45000 });
  const metadata = await page.evaluate(() => window.__qaMomentMetadata);
  const measurements = await page.evaluate(() => window.__qaCaption);
  fs.writeFileSync(path.join(out, `${width}-captured-metadata.json`), JSON.stringify(metadata, null, 2) + '\n');
  row.capture = { metadata, measurements }; save();
  assert.equal(metadata.structure, selected.id); assert.equal(metadata.year, '1904'); assert.equal(metadata.sourceSubject, selected.name);
  assert.deepEqual(metadata.sources, canonicalSources, 'Caption shortening preserves every original citation in capture metadata');
  const sourceCaptionChars = (`Sources for ${metadata.sourceSubject}: ${metadata.sources.map(source => source.title).join('; ')}`).length;
  assert.equal(measurements.finished, true); assert.equal(measurements.captionContexts, 1);
  assert(measurements.captionMeasureTextCalls > 0 && measurements.captionMeasureTextCalls <= 80,
    `Actual caption measurements are bounded: ${JSON.stringify(measurements)}`);
  assert(measurements.captionMaxMeasuredChars >= sourceCaptionChars, 'Real full source caption reaches the fitting code');
  assert.equal(measurements.mime, 'image/png'); assert(measurements.pngBytes > 1000);
  const full = await imagePixels(preview, 106);
  assert(Math.max(full.width, full.height) <= 1280); assert(full.litFraction > .1 && full.tones > 8, 'Captured PNG contains real scene pixels above its footer');
  assert.equal(await page.evaluate(() => __chicago4d.renderer.getContext().getContextAttributes().preserveDrawingBuffer), false);
  await page.evaluate(() => __chicago4d.closeBuilding());
  const download = page.waitForEvent('download');
  await page.locator('.moment-tools').getByRole('button', { name: 'Save picture', exact: true }).click();
  const pngPath = path.join(out, `${width}-moment.png`); await (await download).saveAs(pngPath);
  const png = fs.readFileSync(pngPath); assert.equal(png.subarray(1, 4).toString(), 'PNG'); assert.equal(png.length, measurements.pngBytes);
  await page.locator('.moment-tools').getByRole('button', { name: 'Save to notebook', exact: true }).click();
  await page.waitForFunction(() => document.querySelector('.moment-tools [role="status"]')?.textContent.includes('Photo saved'));
  const raw = await page.evaluate(() => localStorage.getItem('chicago4d.notebook.v1'));
  assert(raw.length <= 1500000);
  const notebook = JSON.parse(raw); assert.equal(notebook.entries.length, 1);
  const entry = notebook.entries[0]; assert.equal(entry.kind, 'photo'); assert.equal(entry.year, '1904'); assert.equal(entry.place, metadata.place);
  assert.equal(entry.link, metadata.url); assert.match(entry.photo, /^data:image\/jpeg;base64,/); assert(entry.photo.length <= 160000);
  assert.deepEqual(entry.sources, canonicalSources.slice(0, 40).map(source => {
    let url = ''; try { const parsed = new URL(source.url); if (['http:', 'https:'].includes(parsed.protocol)) url = parsed.href; } catch {}
    return { id: source.id.slice(0, 200), title: (source.title || source.id).slice(0, 500), url };
  }));
  await page.evaluate(async () => { await __chicago4d.navigator.select('guide'); __chicago4d.navigator.open(2); });
  const notebookView = page.locator('#field-notebook'); await notebookView.waitFor({ state: 'visible' });
  if (!(await notebookView.evaluate(el => el.open))) await notebookView.locator('summary').click();
  const article = notebookView.locator(`.field-notebook-entry[data-notebook-id="${entry.id}"]`);
  await article.waitFor({ state: 'visible' });
  const smallFooter = Math.ceil(106 * Math.min(1, 640 / Math.max(full.width, full.height)));
  const small = await imagePixels(article.locator('img'), smallFooter);
  assert(Math.max(small.width, small.height) <= 640);
  assert(small.litFraction > .1 && small.tones > 8, 'Saved JPEG retains real scene pixels above its scaled footer');
  const note = 'I compared this reconstructed view with the photographs and cited record.';
  await article.locator('textarea').fill(note); await article.getByRole('button', { name: 'Save changes', exact: true }).click();
  const editedRaw = await page.evaluate(() => localStorage.getItem('chicago4d.notebook.v1'));
  const edited = JSON.parse(editedRaw).entries.find(item => item.id === entry.id);
  assert.equal(edited.text, note); assert.equal(edited.photo, entry.photo); assert.deepEqual(edited.sources, entry.sources);
  const sizes = await article.evaluate(el => ({ width: el.clientWidth, content: el.scrollWidth, page: document.documentElement.scrollWidth, viewport: innerWidth }));
  assert(sizes.content <= sizes.width + 1); assert(sizes.page <= sizes.viewport + 1);
  await page.screenshot({ path: path.join(out, `${width}-saved-notebook-photo.png`) });
  assert.equal(await page.locator('.photo-hunt-image[src]').count(), 0);
  assert.deepEqual(row.errors, []); assert.deepEqual(row.httpErrors, []); assert.deepEqual(row.requestFailures, []);
  return { selected, measurements, sourceCaptionChars,
    fullMetadataSourceCount: metadata.sources.length, notebookSourceCount: entry.sources.length, full, small,
    png: { path: pngPath, bytes: png.length, sha256: digest(png) },
    notebook: { entryId: entry.id, chars: editedRaw.length, sha256: digest(editedRaw), photoChars: entry.photo.length,
      photoSha256: digest(entry.photo), sourceIds: entry.sources.map(source => source.id), editedNote: edited.text }, sizes };
}
async function assertReveal(round, answer) {
  const distance = Math.hypot(round.target.e - answer.e, round.target.n - answer.n);
  const score = Math.round(1000 * Math.exp(-Math.max(0, distance - 5) / 50));
  const text = await hunt().innerText();
  assert(text.includes(`${Math.round(distance)} metres from the camera spot · ${score} points`));
  assert(text.includes(`Recorded year range: ${round.years}`));
  if (round.date) assert(text.includes(`Source’s date description: ${round.date}`));
  assert.equal(await hunt().locator('h4').innerText(), round.title);
  if (round.source) assert.equal(await hunt().getByRole('link', { name: 'Read the source', exact: true }).getAttribute('href'), round.source);
  assert.equal(await hunt().getByRole('link', { name: 'Open the full photograph', exact: true }).getAttribute('href'), round.full);
  return { id: round.id, photographYears: round.years, sourceDate: round.date, worldYear: '1904', distance, score };
}
async function nativeZoom() {
  await hunt().locator('img').scrollIntoViewIfNeeded();
  const dimensions = () => page.evaluate(() => {
    const canvas = __chicago4d.renderer.domElement;
    return { canvas: [canvas.width, canvas.height], vh: document.documentElement.style.getPropertyValue('--vh'),
      sheet: document.getElementById('navigator').getBoundingClientRect().height, scale: visualViewport.scale,
      offsetLeft: visualViewport.offsetLeft, width: visualViewport.width };
  });
  const before = await dimensions();
  const box = await hunt().locator('img').boundingBox();
  const at = { x: 130, y: Math.min(height - 140, Math.max(170, box.y + Math.min(100, box.height / 2))) };
  const client = await context.newCDPSession(page);
  await client.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [
    { id: 10, x: at.x - 45, y: at.y }, { id: 11, x: at.x + 45, y: at.y },
  ] });
  for (let step = 1; step <= 35; step++) {
    const scale = await page.evaluate(() => visualViewport.scale); if (scale >= 1.95) break;
    await client.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [
      { id: 10, x: (at.x - 45 - step * 3) / scale, y: at.y / scale },
      { id: 11, x: (at.x + 45 + step * 3) / scale, y: at.y / scale },
    ] });
    await page.waitForTimeout(20);
  }
  await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await page.waitForFunction(() => visualViewport.scale > 1.8, null, { timeout: 3000 });
  const zoom = await dimensions();
  assert.deepEqual(zoom.canvas, before.canvas); assert.equal(zoom.vh, before.vh); assert(Math.abs(zoom.sheet - before.sheet) < 1);
  const scale = zoom.scale, sign = zoom.offsetLeft < (width - zoom.width) / 2 ? -1 : 1;
  await client.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ id: 20, x: 160 / scale, y: at.y / scale }] });
  for (let step = 1; step <= 8; step++) {
    await client.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ id: 20, x: (160 + sign * step * 10) / scale, y: at.y / scale }] });
    await page.waitForTimeout(20);
  }
  await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  const pan = await dimensions();
  assert(Math.abs(pan.offsetLeft - zoom.offsetLeft) > 10, `Native Navigator pan: ${JSON.stringify({ zoom, pan })}`);
  await page.screenshot({ path: path.join(out, `${width}-native-pinch-pan.png`) });
  await client.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 });
  await page.waitForFunction(() => visualViewport.scale === 1);
  await client.detach();
  return { before, zoom, pan };
}
async function visitAndModal(round) {
  const before = await pose();
  await page.evaluate(() => __chicago4d.setTravelMode('instantly'));
  await button('Visit the camera spot').click();
  await page.waitForFunction(target => {
    const api = __chicago4d;
    return api.navigator.app === 'inspect' && api.travelState.phase === 'idle'
      && Math.hypot(api.walker.state.e - target.e, api.walker.state.n - target.n) < .05;
  }, round.target);
  const after = await pose();
  const facingError = Math.abs(((after.bearing - round.target.yaw + 540) % 360) - 180);
  assert(facingError < .1, `Actual arrival facing: ${facingError}`);
  assert.equal(await page.locator('.photo-hunt-image[src]').count(), 0, 'Hidden hunt releases its image during Inspect');
  const hero = page.locator(`#insp-pane-photos .ph-hero[data-photo="${round.id}"] .ph-hero-open`);
  await hero.waitFor({ state: 'visible' });
  assert.equal(await page.locator('#insp-tab-photos').getAttribute('aria-selected'), 'true');
  await hero.scrollIntoViewIfNeeded();
  await realFrame('camera-visit');
  await hero.focus(); await page.keyboard.press('Enter');
  const dialog = page.locator('dialog.pic-viewer');
  await dialog.waitFor({ state: 'visible' });
  await page.waitForFunction(() => { const img = document.querySelector('.pic-viewer [data-pv-img]'); return img?.complete && img.naturalWidth > 0; });
  assert.equal(await dialog.evaluate(el => el.matches(':modal')), true);
  assert.equal(await dialog.locator('[data-pv-close]').evaluate(el => document.activeElement === el), true);
  assert.equal(await dialog.locator('[data-pv-full]').getAttribute('href'), round.full);
  for (let i = 0; i < 12; i++) {
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => !!document.activeElement.closest('dialog.pic-viewer')), true);
  }
  await page.keyboard.press('Shift+Tab');
  assert.equal(await page.evaluate(() => !!document.activeElement.closest('dialog.pic-viewer')), true);
  await hero.evaluate(el => el.focus());
  assert.equal(await page.evaluate(() => !!document.activeElement.closest('dialog.pic-viewer')), true, 'Native modal isolates the real Inspect opener');
  const modal = await dialog.locator('img').evaluate(el => ({ src: el.currentSrc, width: el.naturalWidth, height: el.naturalHeight }));
  assert(modal.src === round.full || modal.src === round.image);
  await page.screenshot({ path: path.join(out, `${width}-picture-modal.png`) });
  const beforeLevel = await page.evaluate(() => __chicago4d.navigator.level);
  await page.keyboard.press('n');
  assert.equal(await page.evaluate(() => __chicago4d.navigator.level), beforeLevel);
  assert.equal(await page.evaluate(() => __chicago4d.navigator.app), 'inspect');
  await page.keyboard.press('Escape'); await dialog.waitFor({ state: 'hidden' });
  assert.equal(await hero.evaluate(el => document.activeElement === el), true, 'Escape returns focus to the real photo opener');
  assert.equal(await page.evaluate(() => __chicago4d.navigator.level), beforeLevel);
  assert.deepEqual(await dialog.evaluate(el => ({ open: el.open, image: el.querySelector('img').getAttribute('src'), loading: el._loading, doc: el._doc })),
    { open: false, image: null, loading: null, doc: null });
  const travel = await page.evaluate(() => ({ state: __chicago4d.travelState, showMe: __chicago4d.showMe.last }));
  await openHunt();
  await oneImage(round);
  return { id: round.id, mode: 'instantly', before, after, facingError, travel, modal };
}

try {
  browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || '/usr/bin/chromium',
    args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--disable-features=BackForwardCache'] });
  report.browser = browser.version();
  context = await browser.newContext({ viewport: { width, height }, hasTouch: width === 390, isMobile: width === 390,
    deviceScaleFactor: 1, reducedMotion: 'reduce', permissions: ['clipboard-read', 'clipboard-write'] });
  await context.addInitScript(() => {
    if (!sessionStorage.getItem('t3657.native.seeded')) {
      localStorage.setItem('chicago4d.settings', JSON.stringify({ soundMaster: 0, detail: 'light', quality: 1 }));
      sessionStorage.setItem('t3657.native.seeded', '1');
    }
    window.__qaHuntImages = { max: 0, states: [] };
    new MutationObserver(() => {
      const srcs = [...document.querySelectorAll('.photo-hunt-image[src]')].map(el => el.getAttribute('src'));
      const trace = window.__qaHuntImages;
      trace.max = Math.max(trace.max, srcs.length);
      if (JSON.stringify(trace.states.at(-1)) !== JSON.stringify(srcs)) trace.states.push(srcs);
    }).observe(document, { subtree: true, childList: true, attributes: true, attributeFilter: ['src'] });
  });
  page = await context.newPage(); page.setDefaultTimeout(30000);
  page.on('pageerror', error => row.errors.push(error.message));
  page.on('requestfailed', request => {
    const item = { url: request.url(), error: request.failure()?.errorText };
    (item.error?.includes('ERR_ABORTED') ? row.cancelledRequests : row.requestFailures).push(item);
  });
  page.on('response', response => {
    if (response.status() >= 400) row.httpErrors.push({ url: response.url(), status: response.status() });
    const receipt = photoReceipts.find(item => item.url === response.url());
    if (receipt) responseTasks.push((async () => {
      const item = { id: receipt.id, url: response.url(), status: response.status(), mime: response.headers()['content-type'] };
      try { const bytes = await response.body(); item.bytes = bytes.length; item.sha256 = digest(bytes); }
      catch (error) { item.error = String(error); }
      row.photoResponses.push(item);
    })());
  });
  await page.goto(`${origin}/1904/?year=1904&detail=light&nav=home&hunt=1&huntDay=${day}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await boot();
  let rounds;
  await check('Real Home hunt loads the canonical five and records all live camera safety decisions', async () => {
    await openHunt();
    const result = await page.evaluate(async day => {
      const api = __chicago4d;
      const { HUNT_PHOTOS, huntRounds, huntSpotSafe } = await import('/walk/js/photo-hunt.js');
      const { BODY_R_M } = await import('/walk/js/human-spacing.js');
      const doc = await api.pictures();
      const rounds = huntRounds(doc, api.destinations, day);
      const guards = rounds.map(round => {
        const row = api.destinations.byId('photo', round.id);
        const tests = { inBounds: !!api.terrain.inBounds(row.e, row.n), water: !!api.terrain.isWater(row.e, row.n),
          blocked: !!api.router.blockedAt(row.e, row.n), barrier: !!api.houseBarriers?.near(row.e, row.n, BODY_R_M) };
        return { id: round.id, owner: row.of, expectedOwner: HUNT_PHOTOS[round.id], target: round.target, bodyRadius: BODY_R_M, ...tests,
          allowed: huntSpotSafe(row, { inBounds: () => tests.inBounds, isWater: () => tests.water,
            blockedAt: () => tests.blocked, barrierAt: () => tests.barrier }) };
      });
      return { rounds, guards, welcome: api.welcome.state, year: String(api.moment.read().year) };
    }, day);
    rounds = result.rounds; row.rounds = rounds; row.guards = result.guards;
    assert.equal(rounds.length, 5); assert.equal(new Set(rounds.map(r => r.id)).size, 5); assert.equal(result.year, '1904');
    for (const guard of result.guards) assert.equal(guard.owner, guard.expectedOwner);
    save();
    assert(result.guards.some(g => g.allowed), 'No canonical camera spot is permitted by the live guards; stop and report without inventing another target');
    await oneImage(rounds[0]); await realFrame('hunt-first');
    return result;
  });
  if (width === 390) await check('Actual Navigator permits native phone pinch and pan without shrinking the drawing buffer', nativeZoom);
  row.answers = [];
  let visited = false;
  for (let index = 0; index < rounds.length; index++) {
    const round = rounds[index];
    await check(`Round ${index + 1}: real photo, current walker guess, source dates and score`, async () => {
      const photo = await oneImage(round);
      assert.equal(await hunt().locator('h3').innerText(), `Photograph ${index + 1} of 5`);
      assert.equal(await button('Visit the camera spot').count(), 0, 'No visit before guessing');
      const before = await pose();
      await button('Guess this spot').click();
      const raw = await progress(), saved = JSON.parse(raw), answer = saved.answers[index];
      assert(raw.length < 4096); assert.equal(saved.cursor, index); assert.equal(saved.day, day);
      assert.equal(answer.id, round.id); assert.equal(answer.skipped, false); assert.equal(answer.e, before.e); assert.equal(answer.n, before.n);
      const reveal = await assertReveal(round, answer);
      row.answers.push({ ...reveal, answer, photo }); save();
      await hunt().locator('h4').scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(out, `${width}-round-${index + 1}-reveal.png`) });
      return { ...reveal, answer, photo };
    });
    const guard = row.guards.find(g => g.id === round.id);
    if (!guard.allowed) await check(`Round ${index + 1}: unsafe camera visit is visibly refused`, async () => {
      const before = await pose(); await button('Visit the camera spot').click();
      assert((await hunt().innerText()).includes('The recorded camera spot cannot be safely visited right now.'));
      assert.deepEqual(await pose(), before); assert.equal(await page.evaluate(() => __chicago4d.navigator.app), 'home');
      return { guard, before, after: await pose() };
    });
    else if (!visited) {
      await check('Permitted Visit uses real travel and walker state, then the real Inspect photo modal', async () => {
        const result = await visitAndModal(round); visited = true; row.visit = result; return result;
      });
    }
    if (index === 0) await check('Shared challenge reload preserves the exact day, first answer, reveal and order', async () => {
      const saved = await progress();
      await button('Copy challenge link').click();
      const url = await hunt().getByRole('textbox', { name: 'Challenge link', exact: true }).inputValue();
      const q = new URL(url).searchParams;
      assert.deepEqual([...q.keys()].sort(), ['hunt', 'huntDay', 'nav', 'year']);
      assert.equal(q.get('huntDay'), day); assert.equal(q.get('hunt'), '1'); assert.equal(q.get('year'), '1904'); assert.equal(q.get('nav'), 'home');
      row.shareURL = url; row.savedProgressSha256 = digest(saved); save();
      row.huntImageTraces = [await page.evaluate(() => window.__qaHuntImages)];
      assert(row.huntImageTraces[0].max <= 1);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); await boot(); await openHunt();
      assert.equal(await progress(), saved);
      assert.equal(await hunt().locator('h3').innerText(), 'Photograph 1 of 5');
      assert.equal(await button('Guess this spot').count(), 0);
      await oneImage(round); await assertReveal(round, JSON.parse(saved).answers[0]);
      const order = await page.evaluate(async day => (await import('/walk/js/photo-hunt.js')).huntOrder(day), day);
      assert.deepEqual(order, rounds.map(r => r.id));
      return { url, storedChars: saved.length, progressSha256: digest(saved), order };
    });
    await button(index === 4 ? 'Finish hunt' : 'Next photograph').click();
  }
  await check('Five rounds finish with one bounded record; all real images match the visual audit; zero errors, 404s or overflow', async () => {
    assert(visited); assert.equal(row.bootSeconds.length, 2);
    assert.equal(await hunt().locator('h3').innerText(), 'Five-photo hunt complete');
    assert.equal(await page.locator('.photo-hunt-image[src]').count(), 0);
    const saved = JSON.parse(await progress()); assert.equal(saved.cursor, 5); assert.equal(saved.answers.length, 5);
    const total = row.answers.reduce((sum, answer) => sum + answer.score, 0);
    assert((await hunt().innerText()).includes(`${total} of 5,000 points`));
    await Promise.all(responseTasks);
    for (const receipt of photoReceipts) {
      const received = row.photoResponses.filter(item => item.id === receipt.id);
      assert(received.length, `No real network response recorded for ${receipt.id}`);
      assert(received.some(item => item.status === 200 && item.mime?.startsWith('image/jpeg') && item.sha256 === receipt.sha256),
        `Actual decoded photo differs from the reviewed hosted bytes: ${JSON.stringify(received)}`);
    }
    const sizes = await page.evaluate(() => ({ page: document.documentElement.scrollWidth, viewport: innerWidth,
      hunt: [...document.querySelectorAll('.photo-hunt')].map(el => ({ width: el.clientWidth, content: el.scrollWidth })) }));
    assert(sizes.page <= sizes.viewport + 1); assert(sizes.hunt.every(el => el.content <= el.width + 1));
    await realFrame('hunt-complete');
    row.huntImageTraces.push(await page.evaluate(() => window.__qaHuntImages));
    assert(row.huntImageTraces.every(trace => trace.max <= 1), 'Hunt owns at most one image source throughout both boots');
    assert.deepEqual(row.errors, []); assert.deepEqual(row.httpErrors, []); assert.deepEqual(row.requestFailures, []);
    for (const [relative, expected] of Object.entries(testedFiles))
      assert.equal(digest(fs.readFileSync(path.join(site, relative))), expected, `Frozen runtime changed during test: ${relative}`);
    return { total, savedChars: (await progress()).length, sizes, actualPhotos: photoReceipts.map(p => p.id), permittedVisit: row.visit.id };
  });
  await check('Actual bounded-caption photo capture and notebook save retain canonical citations and the real image', photoAndNotebook);
  for (const [relative, expected] of Object.entries(testedFiles))
    assert.equal(digest(fs.readFileSync(path.join(site, relative))), expected, `Frozen runtime changed during photo/notebook check: ${relative}`);
} catch (error) {
  row.fatal = String(error.stack || error); log('FAIL', error.message);
  row.failureState = await page?.evaluate(() => ({ title: document.title, ready: window.__chicago4d?.ready,
    app: window.__chicago4d?.navigator?.app, hunt: document.querySelector('.photo-hunt')?.innerText,
    travel: window.__chicago4d?.travelState })).catch(() => null);
  await page?.screenshot({ path: path.join(out, `${width}-failure.png`), timeout: 15000 }).catch(() => {});
} finally {
  await context?.close(); await Promise.allSettled(responseTasks); await browser?.close();
  await new Promise(resolve => server.close(resolve)); report.finished = new Date().toISOString(); save();
}
const failed = !!row.fatal || row.checks.some(item => !item.pass) || row.errors.length > 0 || row.httpErrors.length > 0 || row.requestFailures.length > 0;
log(failed ? 'NATIVE HUNT FAIL' : 'NATIVE HUNT PASS', path.join(out, 'report.json'));
process.exitCode = failed ? 1 : 0;
