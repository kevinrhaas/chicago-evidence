/** Focused final-runtime integration, not the full renderer gate or a performance test.
 * One page/world at a time; two boots per viewport. No application source is modified.
 * Continuous draws are paused between UI actions. The shutter gets a real normal tick.
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { createHash as hash } from 'node:crypto';
import { createRequire } from 'node:module';

const app = '/workspace/chicago/chicago/4d';
const site = path.resolve(process.env.QA_ROOT || '/workspace/chicago-classroom-final-published');
const out = process.env.QA_OUT || '/tmp/t3656-resource-photo-notebook';
const widths = (process.env.QA_WIDTHS || '390,1280').split(',').map(Number);
assert(widths.length && widths.every(w => [390, 1280].includes(w)));
const { chromium } = createRequire('/workspace/chicago/package.json')('playwright');
const digest = bytes => hash('sha256').update(bytes).digest('hex');
const manifestPath = process.env.QA_MANIFEST || '/tmp/t3656-renderer-manifest.json';
const runtime = JSON.parse(fs.readFileSync(manifestPath));
for (const [relative, expected] of Object.entries(runtime.files))
  assert.equal(digest(fs.readFileSync(path.join(site, relative))), expected, `Frozen final-runtime mismatch: ${relative}`);
const testedFiles = Object.fromEntries([
  ...Object.keys(runtime.files), 'walk/js/moment-view.js', 'walk/js/field-notebook-view.js',
  'walk/js/reader-text.js', 'walk/js/strings/moment.js', 'walk/js/strings/notebook.js',
].map(relative => [relative, digest(fs.readFileSync(path.join(site, relative)))]));
const personId = 'hogan_john_s_c';
const directory = JSON.parse(fs.readFileSync(path.join(site, 'data/sidecars/1835/people.json')));
const personRow = directory.people.find(p => p.id === personId);
assert(personRow);
const household = JSON.parse(fs.readFileSync(path.join(site, 'data/residents', personRow.file)));
const person = household.persons.find(p => p.id === personId);
assert(person?.sources?.length);
fs.mkdirSync(out, { recursive: true });
const report = { started: new Date().toISOString(), site, manifestPath, runtimeCommit: runtime.commit, testedFiles,
  scope: 'Actual published town: People selection, photo capture, Save to notebook, edit, shared arrival, persistent photo/note/sources and on-demand stylesheet loading',
  limits: ['Continuous software-GPU draws paused between interactions; one real normal tick captures photo.',
    'Not a sustained hardware-performance measurement or the complete renderer gate.',
    'Navigator API selects screens; People row and all save/edit/copy actions use actual UI controls.',
    'Photo sources are compared with captured metadata, including honest empty sources if no place is selected. The person entry must retain real canonical citations.'],
  runs: [] };
const saveReport = () => fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.glb': 'model/gltf-binary', '.svg': 'image/svg+xml', '.wasm': 'application/wasm',
  '.ktx2': 'image/ktx2', '.webp': 'image/webp', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  try {
    let file = path.resolve(site, '.' + decodeURIComponent(new URL(req.url, 'http://local').pathname));
    if (!file.startsWith(site + path.sep) && file !== site) { res.writeHead(403); res.end(); return; }
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    fs.createReadStream(file).pipe(res);
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || '/usr/bin/chromium',
  args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--disable-features=BackForwardCache'] });
const log = (...args) => console.log(new Date().toISOString(), ...args);
async function boot(page, row) {
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
  row.bootSeconds.push((Date.now() - start) / 1000);
  log(row.width, 'boot', row.bootSeconds.length, 'seconds', row.bootSeconds.at(-1));
}
async function screen(page, name) {
  await page.evaluate(name => __chicago4d.navigator.select(name), name);
}
async function expand(page, selector) {
  const summary = page.locator(`${selector} > summary`);
  await summary.waitFor({ state: 'visible' });
  if (!(await page.locator(selector).evaluate(e => e.open))) await summary.click();
}
async function loadedStyle(page, id, filename) {
  await page.waitForFunction(({ id, filename }) => {
    const link = document.getElementById(id);
    try { return link?.rel === 'stylesheet' && new URL(link.href).pathname.endsWith('/css/' + filename)
      && link.sheet?.cssRules.length > 0; } catch { return false; }
  }, { id, filename });
  assert.equal(await page.locator(`link#${id}`).count(), 1, `${filename} is loaded once in this document`);
  return page.locator(`link#${id}`).evaluate(link => ({ href: link.href, rules: link.sheet.cssRules.length }));
}
async function snapshotNotebook(page) {
  return page.evaluate(() => {
    const raw = localStorage.getItem('chicago4d.notebook.v1');
    return { raw, data: JSON.parse(raw) };
  });
}
async function imageFacts(locator, footer = 0) {
  return locator.evaluate(async (image, footer) => {
    await image.decode();
    const c = document.createElement('canvas'); c.width = image.naturalWidth; c.height = image.naturalHeight;
    const context = c.getContext('2d'); context.drawImage(image, 0, 0);
    const pixels = context.getImageData(0, 0, c.width, c.height - footer).data;
    let lit = 0; const tones = new Set();
    for (let i = 0; i < pixels.length; i += 64) {
      if (pixels[i] + pixels[i + 1] + pixels[i + 2] > 30) lit++;
      tones.add(`${pixels[i] >> 4},${pixels[i + 1] >> 4},${pixels[i + 2] >> 4}`);
    }
    return { width: c.width, height: c.height, litFraction: lit / Math.ceil(pixels.length / 64), tones: tones.size };
  }, footer);
}
try {
  for (const width of widths) {
    const context = await browser.newContext({ viewport: { width, height: width === 390 ? 780 : 800 },
      hasTouch: width === 390, isMobile: width === 390, deviceScaleFactor: 1, acceptDownloads: true,
      reducedMotion: 'reduce', permissions: ['clipboard-read', 'clipboard-write'] });
    const row = { width, checks: [], errors: [], missing: [], bootSeconds: [], styleRequests: [] };
    report.runs.push(row); saveReport();
    await context.addInitScript(() => {
      if (!sessionStorage.getItem('t3656.final.seeded')) {
        localStorage.setItem('chicago4d.settings', JSON.stringify({ soundMaster: 0, detail: 'light', quality: 1 }));
        sessionStorage.setItem('t3656.final.seeded', '1');
      }
    });
    const { standInNarrationIndex } = await import(app + '/tools/audio_smoke_replay.mjs');
    await standInNarrationIndex(context, { origin, root: app });
    const page = await context.newPage(); page.setDefaultTimeout(30000);
    page.on('pageerror', error => row.errors.push(error.message));
    page.on('request', request => {
      if (/\/(moment|field-notebook)\.css$/.test(new URL(request.url()).pathname)) row.styleRequests.push(request.url());
    });
    page.on('response', response => {
      if (response.status() >= 400 && response.url().startsWith(origin)) row.missing.push({ url: response.url(), status: response.status() });
    });
    const check = async (label, run) => {
      log(width, 'START', label);
      try { const result = await run(); row.checks.push({ label, pass: true, result }); saveReport(); log(width, 'PASS', label); }
      catch (error) { row.checks.push({ label, pass: false, error: String(error.stack || error) }); saveReport(); throw error; }
    };
    try {
      await page.goto(origin + '/1835/?detail=light', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await boot(page, row);
      await check('Select a real person through People, save canonical citations, retain selection in Home', async () => {
        assert.equal(await page.locator('link#moment-style, link#field-notebook-style').count(), 0, 'Unopened classroom tools do not allocate their stylesheets');
        assert.deepEqual(row.styleRequests, [], 'Unopened classroom tool stylesheets are not fetched');
        await screen(page, 'people');
        await page.getByRole('searchbox', { name: 'Search the people of the town' }).fill('Hogan');
        await page.locator(`.person-row[data-person-id="${personId}"]`).click();
        await page.waitForFunction(() => {
          const button = document.querySelector('.people-notebook-save'); return !!button && !button.disabled;
        });
        assert.equal(await page.locator('.people-card-name').innerText(), personRow.name);
        await page.locator('.people-notebook-save').click();
        await page.waitForFunction(() => document.querySelector('.people-notebook-status')?.textContent.includes('Saved'));
        const { data } = await snapshotNotebook(page);
        assert.equal(data.entries.length, 1); const entry = data.entries[0];
        assert.equal(entry.kind, 'person'); assert.equal(entry.person, personId);
        assert.deepEqual(entry.sources.map(s => s.id), person.sources);
        assert(entry.sources.every(s => s.title && s.title !== s.id));
        await screen(page, 'home');
        const selected = await page.evaluate(() => __chicago4d.moment.read());
        assert.equal(selected.person, personId); assert.equal(selected.personName, personRow.name);
        return { person: selected.person, personName: selected.personName, sourceIds: entry.sources.map(s => s.id) };
      });
      await check('Production shutter captures a normal rendered frame and the UI copies that exact moment URL', async () => {
        await expand(page, '#nav-moment');
        row.momentStyle = await loadedStyle(page, 'moment-style', 'moment.css');
        assert.equal(await page.locator('link#field-notebook-style').count(), 0, 'Photo view does not allocate the unopened notebook stylesheet');
        await page.getByRole('button', { name: 'Take photo', exact: true }).evaluate(button => {
          const originalCapture = __chicago4d.moment.capture.bind(__chicago4d.moment);
          __chicago4d.moment.capture = () => originalCapture().then(photo => {
            const { blob, ...metadata } = photo; window.__qaCapturedMetadata = metadata; return photo;
          });
          __chicago4d.renderer.render = window.__qaRealRender;
          button.click();
          try { __chicago4d.step(); }
          finally { __chicago4d.renderer.render = (_scene, camera) => { camera?.updateMatrixWorld?.(); }; }
        });
        const preview = page.locator('img.moment-preview');
        await preview.waitFor({ state: 'visible', timeout: 45000 });
        const picture = await imageFacts(preview, 106);
        assert(Math.max(picture.width, picture.height) <= 1280);
        assert(picture.litFraction > .1 && picture.tones > 8, 'Photo contains rendered scene pixels outside its footer');
        row.capture = await page.evaluate(() => window.__qaCapturedMetadata);
        assert.equal(row.capture.person, personId); assert.equal(row.capture.personName, personRow.name);
        await page.getByRole('button', { name: 'Copy spot link', exact: true }).click();
        row.shareURL = await page.getByRole('textbox', { name: 'Link to this spot', exact: true }).inputValue();
        assert.equal(row.shareURL, row.capture.url);
        assert.equal(new URL(row.shareURL).searchParams.get('person'), personId);
        const download = page.waitForEvent('download');
        await page.getByRole('button', { name: 'Save picture', exact: true }).click();
        const file = path.join(out, `${width}-moment.png`); await (await download).saveAs(file);
        assert.equal(fs.readFileSync(file).subarray(1, 4).toString(), 'PNG');
        assert.equal(await page.evaluate(() => __chicago4d.renderer.getContext().getContextAttributes().preserveDrawingBuffer), false);
        return { picture, pngBytes: fs.statSync(file).size, person: row.capture.person, sourceCount: row.capture.sources.length, shareURL: row.shareURL };
      });
      await check('Actual Save to notebook stores a bounded photo with its captured sources; editing preserves it', async () => {
        await page.getByRole('button', { name: 'Save to notebook', exact: true }).click();
        await page.waitForFunction(() => document.querySelector('.moment-tools [role="status"]')?.textContent.includes('Photo saved'));
        const before = await snapshotNotebook(page);
        assert(before.raw.length <= 1500000); assert.equal(before.data.entries.length, 2);
        const photo = before.data.entries.find(e => e.kind === 'photo'); assert(photo);
        row.photoId = photo.id;
        assert.match(photo.photo, /^data:image\/jpeg;base64,/); assert(photo.photo.length <= 160000);
        assert.equal(photo.year, '1835'); assert.equal(photo.link, row.shareURL);
        assert.equal(photo.place, row.capture.place);
        assert.deepEqual(photo.sources, row.capture.sources.slice(0, 40).map(s => ({ id: s.id.slice(0, 200), title: (s.title || s.id).slice(0, 500), url: s.url })));
        await screen(page, 'guide'); await expand(page, '#field-notebook');
        row.notebookStyle = await loadedStyle(page, 'field-notebook-style', 'field-notebook.css');
        const article = page.locator(`.field-notebook-entry[data-notebook-id="${row.photoId}"]`);
        await article.waitFor({ state: 'visible' });
        const small = await imageFacts(article.locator('img'));
        assert(Math.max(small.width, small.height) <= 640);
        row.note = 'I compared this reconstructed view with the cited record. <b>This is my own note.</b>';
        await article.locator('textarea').fill(row.note);
        await article.getByRole('button', { name: 'Save changes', exact: true }).click();
        assert.equal(await article.locator('b').count(), 0);
        const edited = await snapshotNotebook(page);
        const savedPhoto = edited.data.entries.find(e => e.id === row.photoId);
        assert.equal(savedPhoto.text, row.note); assert.equal(savedPhoto.photo, photo.photo);
        assert.deepEqual(savedPhoto.sources, photo.sources);
        row.savedNotebook = { sha256: digest(edited.raw), chars: edited.raw.length,
          photoSha256: digest(savedPhoto.photo), photoChars: savedPhoto.photo.length,
          sourceIds: savedPhoto.sources.map(s => s.id), personSourceIds: person.sources };
        assert.equal(await page.locator('link#moment-style').count(), 1, 'Opening Guide retains a single photo stylesheet');
        await page.screenshot({ path: path.join(out, `${width}-notebook-before.png`) });
        return { ...row.savedNotebook, smallPhoto: small };
      });
      await check('Shared URL restores the selected person and view; the same saved photo, note and citations survive navigation', async () => {
        row.savedJaunt = await page.evaluate(async () => {
          const document = await fetch(new URL('sidecars/1835/jaunts/across-wolf-point.json', __chicago4d.dataBase)).then(r => r.json());
          const raw = JSON.stringify({ content_version: document.content_version, jaunt: document.id, events: [] });
          localStorage.setItem('c4d.jaunt.session.v1', raw); return raw;
        });
        await page.goto(row.shareURL, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await boot(page, row);
        await page.waitForFunction(() => !!__chicago4d.momentRestored, null, { timeout: 45000 });
        await page.waitForFunction(id => __chicago4d.moment.read()?.person === id, personId);
        const moment = await page.evaluate(() => __chicago4d.moment.read());
        assert(Math.abs(moment.e - row.capture.e) < 1); assert(Math.abs(moment.n - row.capture.n) < 1);
        assert.equal(moment.season, row.capture.season); assert.equal(moment.person, personId);
        assert.equal(await page.evaluate(() => localStorage.getItem('c4d.jaunt.session.v1')), row.savedJaunt);
        assert.equal(await page.evaluate(() => __chicago4d.jaunts.state?.jaunt ?? null), null);
        const persisted = await snapshotNotebook(page);
        assert.equal(digest(persisted.raw), row.savedNotebook.sha256, 'Notebook bytes survive same-tab shared-link arrival unchanged');
        const photo = persisted.data.entries.find(e => e.id === row.photoId);
        assert.equal(photo.text, row.note); assert.equal(digest(photo.photo), row.savedNotebook.photoSha256);
        assert.deepEqual(photo.sources.map(s => s.id), row.savedNotebook.sourceIds);
        assert.deepEqual(persisted.data.entries.find(e => e.kind === 'person').sources.map(s => s.id), person.sources);
        await screen(page, 'guide'); await expand(page, '#field-notebook');
        row.notebookStyle = await loadedStyle(page, 'field-notebook-style', 'field-notebook.css');
        const article = page.locator(`.field-notebook-entry[data-notebook-id="${row.photoId}"]`);
        assert.equal(await article.locator('textarea').inputValue(), row.note);
        const picture = await imageFacts(article.locator('img'));
        assert(Math.max(picture.width, picture.height) <= 640);
        await article.locator('img').scrollIntoViewIfNeeded();
        await page.screenshot({ path: path.join(out, `${width}-notebook-after.png`) });
        return { person: moment.person, e: moment.e, n: moment.n, season: moment.season,
          notebookChars: persisted.raw.length, photoChars: photo.photo.length, entryCount: persisted.data.entries.length };
      });
      await check('Zero page errors, no missing local resources, and no horizontal overflow', async () => {
        assert.deepEqual(row.errors, []); assert.deepEqual(row.missing, []);
        const dimensions = await page.evaluate(() => ({ page: document.documentElement.scrollWidth,
          viewport: innerWidth, entries: [...document.querySelectorAll('.field-notebook-entry')].map(e => ({ content: e.scrollWidth, width: e.clientWidth })) }));
        assert(dimensions.page <= dimensions.viewport);
        assert(dimensions.entries.every(e => e.content <= e.width + 1));
        assert.equal(row.bootSeconds.length, 2);
        assert(row.styleRequests.some(url => new URL(url).pathname.endsWith('/css/moment.css')));
        assert(row.styleRequests.some(url => new URL(url).pathname.endsWith('/css/field-notebook.css')));
        return { ...dimensions, momentStyle: row.momentStyle, notebookStyle: row.notebookStyle, styleRequests: row.styleRequests };
      });
    } catch (error) {
      row.fatal = String(error.stack || error); log(width, 'FAIL', error.message);
      row.failureState = await page.evaluate(() => ({ title: document.title,
        ready: window.__chicago4d?.ready, momentStatus: document.querySelector('.moment-tools [role="status"]')?.textContent,
        notebookStatus: document.querySelector('.field-notebook-status')?.textContent })).catch(() => null);
      await page.screenshot({ path: path.join(out, `${width}-failure.png`), timeout: 15000 }).catch(() => {});
    } finally { await context.close(); saveReport(); }
  }
} finally { await browser.close(); await new Promise(resolve => server.close(resolve)); saveReport(); }
const failed = report.runs.some(row => row.fatal || row.checks.some(check => !check.pass) || row.checks.length !== 5);
log(failed ? 'FINAL PHOTO NOTEBOOK FAIL' : 'FINAL PHOTO NOTEBOOK PASS', path.join(out, 'report.json'));
process.exitCode = failed ? 1 : 0;
