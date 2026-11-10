/** Actual published Sauganash scene/card review; no publish/install/source writes. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
const opts = Object.fromEntries(process.argv.slice(2).map((v, i, a) => v.startsWith('--') ? [v.slice(2), a[i + 1]] : null).filter(Boolean));
assert(['desktop', 'phone'].includes(opts.viewport), '--viewport desktop|phone required');
assert(opts.out, '--out required');
const OUT = path.resolve(opts.out); fs.mkdirSync(OUT, { recursive: true });
const webFile = opts['web-file'] || '/tmp/chicago-resume-20261109/chicago/4d/assets/web/sauganash_hotel__frame_1831.glb';
const bytes = fs.readFileSync(webFile), expected = crypto.createHash('sha256').update(bytes).digest('hex');
const url = new URL(opts.url || 'http://127.0.0.1:4188/walk/?year=1835');
url.searchParams.set('year', '1835'); url.searchParams.set('keep-geometry', '1');
assert(!url.pathname.includes('/renderers/web/'), 'published layout required');
const phone = opts.viewport === 'phone';
const viewport = phone ? { width: 390, height: 780 } : { width: 1280, height: 800 };
const receipt = { status: 'RUNNING', kind: 'FOCUSED_REAL_PUBLISHED_SCENE_CARD_REVIEW_NOT_FULL_SMOKE_OR_PHOTO_MATCH',
  viewport, deviceScaleFactor: phone ? 2 : 1, url: String(url), nativeRun: '42711510675', retainedNativePrefix: '254bc9871d',
  expectedWebFile: webFile, expectedWebSha256: expected, expectedWebBytes: bytes.byteLength, screenshots: [], pageErrors: [],
  failedRequests: [], badResponses: [], consoleErrors: [] };
const expectedReviewIds = ["agency_striker_log_house", "beaubien_barn", "beaubien_trading_post", "blacksmith_shop_state_st", "caldwell_agency_log_house", "clybourn_slaughterhouse", "cobweb_castle", "council_house", "jb_beaubien_homestead", "madore_beaubien_house", "mckee_log_house", "robert_kinzie_store", "robinson_caldwell_cabins", "wolf_point_trading_camp"];
function classifyProblems(raw, actualIds) {
  assert.deepEqual(actualIds, expectedReviewIds, "retained review annotations must bind exact expected actual registry records");
  const allowed = new Set(actualIds.map((id) => `${id}: review_required is set — review annotation retained; this flag does not block scene release`));
  const annotations = raw.filter((p) => allowed.has(p)), hard = raw.filter((p) => !allowed.has(p));
  assert.equal(annotations.length, actualIds.length, "every expected annotation must be retained exactly once");
  return { annotations, hard };
}
const save = () => fs.writeFileSync(path.join(OUT, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
save();
const moduleFile = process.env.PW_MODULE || '/tmp/chicago-browser-tools/node_modules/playwright/index.mjs';
const { chromium } = await import(pathToFileURL(moduleFile).href);
let browser, page;
try {
  browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || '/usr/bin/chromium', args: ['--enable-unsafe-swiftshader'] });
  const ctx = await browser.newContext({ viewport, hasTouch: phone, isMobile: false, deviceScaleFactor: phone ? 2 : 1 });
  page = await ctx.newPage(); page.setDefaultTimeout(60_000);
  page.on('pageerror', (error) => { receipt.pageErrors.push(String(error)); save(); });
  page.on('requestfailed', (r) => receipt.failedRequests.push({ url: r.url(), error: r.failure()?.errorText }));
  page.on('response', (r) => { if (r.status() >= 400) receipt.badResponses.push({ url: r.url(), status: r.status() }); });
  page.on('console', (m) => { if (m.type() === 'error') receipt.consoleErrors.push(m.text()); });
  const bootAt = Date.now();
  await page.goto(String(url), { waitUntil: 'domcontentloaded', timeout: 90_000 });
  await page.waitForFunction(() => window.__chicago4d?.ready || window.__chicago4d?.error, null, { timeout: 240_000, polling: 1000 });
  receipt.identity = await page.evaluate(async () => {
    const a = window.__chicago4d; if (!a.ready) throw Error(a.error || 'scene not ready');
    const r = a.registry.get('sauganash_hotel');
    if (!r?.gltf || r.loadFailed || !r.assetUrl) throw Error('actual Hotel native asset not loaded');
    const response = await fetch(r.assetUrl, { cache: 'no-store' }); if (!response.ok) throw Error(`Hotel web HTTP${response.status}`);
    const bytes = await response.arrayBuffer(), hash = await crypto.subtle.digest('SHA-256', bytes);
    return { ready: a.ready, scene: a.scene.id, date: a.scene.target_date, dataBase: String(a.dataBase), problems: a.problems, retainedReviewIds: [...a.registry.values()].filter((r) => r.sidecar?.review_required).map((r) => r.id).sort(),
      build: document.getElementById('gate-build')?.textContent.trim(), detail: a.detail, assetUrl: r.assetUrl, assetDetail: r.assetDetail,
      sidecarUrl: r.sidecarUrl, placement: r.sidecar.placement, footprint: r.sidecar.footprint,
      webBytes: bytes.byteLength, webSha256: [...new Uint8Array(hash)].map((v) => v.toString(16).padStart(2, '0')).join('') };
  });
  receipt.bootSeconds = (Date.now() - bootAt) / 1000; save();
  assert.equal(receipt.identity.scene, '1835');
  assert.equal(receipt.identity.date, '1835-07-01');
  assert(receipt.identity.build.startsWith('build 254bc9871d'), 'actual published build must be retained native254bc');
  assert(receipt.identity.assetUrl.includes('/data/gltf/'), 'actual published web URL required');
  assert.equal(receipt.identity.webSha256, expected, 'actual fetched Hotel web bytes differ from the newly retained native web file');
  assert.equal(receipt.identity.webBytes, bytes.byteLength);
  receipt.problemClassification = classifyProblems(receipt.identity.problems, receipt.identity.retainedReviewIds);
  assert.equal(receipt.problemClassification.hard.length, 0, 'unresolved actual app loading/render problems');
  assert.equal(receipt.pageErrors.length, 0, 'page errors during boot');
  await page.waitForFunction(() => ['welcome', 'world'].includes(window.__chicago4d.welcome?.state), null, { timeout: 90_000, polling: 500 });
  await page.evaluate(() => { const a = window.__chicago4d; if (a.welcome.state !== 'world') a.welcome.enter('spawn'); document.exitPointerLock?.(); document.getElementById('control-help-gotit')?.click(); });
  await page.waitForFunction(() => window.__chicago4d.welcome.state === 'world', null, { timeout: 90_000, polling: 500 });
  receipt.pose = await page.evaluate(() => {
    const a = window.__chicago4d, r = a.registry.get('sauganash_hotel'), p = r.sidecar.placement;
    const poly = Array.isArray(r.sidecar.footprint) ? r.sidecar.footprint : r.sidecar.footprint.polygon;
    if (p.rotation_deg !== 0) throw Error('street pose assumes the existing unchanged Hotel bearing0');
    const e = p.local_e + 18, n = p.local_n - 8;
    const centre = [p.local_e + (Math.min(...poly.map((v) => v[0])) + Math.max(...poly.map((v) => v[0]))) / 2,
      p.local_n + (Math.min(...poly.map((v) => v[1])) + Math.max(...poly.map((v) => v[1]))) / 2];
    const targetY = a.walker.surfaceAt(...centre) + 3.8, eyeY = a.walker.surfaceAt(e, n) + a.walkBudget.eyeHeight;
    const yaw = (Math.atan2(centre[0] - e, centre[1] - n) * 180 / Math.PI + 360) % 360;
    const pitch = Math.atan2(targetY - eyeY, Math.hypot(centre[0] - e, centre[1] - n)) * 180 / Math.PI;
    a.popup.close(); a.navigator.select('home'); a.navigator.dock(); a.intent.clear(); a.setAnimationHold(true); a.setFloraSpread(true); a.setFly(false);
    a.walker.teleport({ local_e: e, local_n: n, yaw_deg: yaw, pitch_deg: pitch }); a.step();
    return { method: 'actual live walker street pose from current Hotel placement+18m east/-8m north', requested: { e, n, yaw, pitch },
      actual: { e: a.walker.state.e, n: a.walker.state.n, eyeY: a.walker.state.eyeY, flying: a.walker.state.flying }, centre };
  });
  save();
  async function shot(name) { await page.screenshot({ path: path.join(OUT, name + '.png'), timeout: 90_000 }); receipt.screenshots.push(name + '.png'); save(); }
  await shot('01-sauganash-street');

  // Load disclosure before opening so its asynchronous redraw cannot invalidate
  // the image-tab lazy-source measurement. Exactly the actual app reader, no fixture.
  await page.evaluate(async () => { const a = window.__chicago4d; await a.loadLiberties(); a.pick('sauganash_hotel'); document.querySelector('#popup [data-pop-tab="evidence"]')?.click(); });
  await page.waitForFunction(() => {
    const p = document.querySelector('#popup [data-pop-pane="images"]');
    return p && !/LOADING IMAGE INDEX/.test(p.textContent) && p.querySelectorAll('.pop-pic-list li, .pop-pic-tile').length >= 2;
  }, null, { timeout: 45_000, polling: 250 });
  receipt.imagesBefore = await page.evaluate(() => {
    const p = document.querySelector('#popup [data-pop-pane="images"]');
    return { src: p.querySelectorAll('img[src]').length, deferred: p.querySelectorAll('img[data-src]').length,
      hidden: p.hidden, openId: window.__chicago4d.popup.openId };
  });
  assert.equal(receipt.imagesBefore.src, 0, 'pictures must not acquire src before Images opens');
  assert.equal(receipt.imagesBefore.openId, 'sauganash_hotel'); save();
  await page.evaluate(() => { document.querySelector('#popup [data-pop-tab="images"]').click(); document.querySelector('#popup [data-pop-pane="images"]').scrollIntoView({ block: 'start' }); });
  await page.waitForFunction(() => {
    const p = document.querySelector('#popup [data-pop-pane="images"]');
    const imgs = [...(p?.querySelectorAll('img[src]') ?? [])];
    return p && !p.hidden && (!imgs.length || imgs.some((img) => img.complete && img.naturalWidth > 0));
  }, null, { timeout: 60_000, polling: 500 });
  receipt.images = await page.evaluate(() => {
    const p = document.querySelector('#popup [data-pop-pane="images"]'), items = [...p.querySelectorAll('.pop-pic-list li, .pop-pic-tile')];
    return { shown: !p.hidden && p.checkVisibility(), items: items.length,
      uncredited: items.filter((li) => !li.querySelector('.pop-pic-meta, .pop-pic-tile-credit')?.textContent.trim()).length,
      tabCount: document.querySelector('#popup [data-pop-tab="images"] .pop-count')?.textContent.trim(),
      credits: items.map((li) => li.querySelector('.pop-pic-meta, .pop-pic-tile-credit')?.textContent.trim()),
      sources: items.map((li) => ({ text: li.innerText, href: li.querySelector('a')?.href ?? null })),
      thumbs: [...p.querySelectorAll('img')].map((img) => ({ src: img.getAttribute('src'), naturalWidth: img.naturalWidth, complete: img.complete, alt: img.alt })) };
  });
  assert(receipt.images.shown && receipt.images.items >= 2 && receipt.images.uncredited === 0);
  assert.equal(receipt.images.tabCount, String(receipt.images.items));
  if (receipt.imagesBefore.deferred > 0) assert(receipt.images.thumbs.some((i) => i.src && i.complete && i.naturalWidth > 0), 'held thumbnail must really load after opening');
  save(); await shot('02-sauganash-images-credited');

  await page.evaluate(() => document.querySelector('#popup [data-pop-tab="liberties"]').click());
  await page.waitForFunction(() => !!document.querySelector('#popup [data-lib-id="L-sauganash-ridge-join-and-shaft-section-2383"]'), null, { timeout: 30_000, polling: 250 });
  receipt.liberty = await page.evaluate(() => {
    const pane = document.querySelector('#popup [data-pop-pane="liberties"]');
    const entry = pane.querySelector('[data-lib-id="L-sauganash-ridge-join-and-shaft-section-2383"]');
    if (!entry.open) entry.querySelector('summary').click();
    entry.scrollIntoView({ block: 'start' });
    return { paneShown: !pane.hidden && pane.checkVisibility(), id: entry.dataset.libId, open: entry.open,
      title: entry.querySelector('summary').innerText, text: entry.innerText, bounds: entry.getBoundingClientRect().toJSON() };
  });
  assert(receipt.liberty.paneShown && receipt.liberty.open);
  assert(/reconstructed trials/.test(receipt.liberty.text) && /0\.60 m/.test(receipt.liberty.text), 'visible trial disclosure must retain reconstructed 0.60m qualification');
  save(); await shot('03-sauganash-roof-stack-liberty');
  receipt.finalProblems = await page.evaluate(() => window.__chicago4d.problems);
  receipt.finalProblemClassification = classifyProblems(receipt.finalProblems, receipt.identity.retainedReviewIds);
  assert.equal(receipt.finalProblemClassification.hard.length, 0, 'actual app problems after scene/card inspection');
  assert.equal(receipt.pageErrors.length, 0, 'page errors');
  assert.equal(receipt.failedRequests.length, 0, 'failed requests');
  assert.equal(receipt.badResponses.length, 0, 'HTTP errors');
  receipt.status = 'PASS_FOCUSED_REVIEW_REQUIRES_HUMAN_SCREENSHOT_INSPECTION'; save();
  console.log(JSON.stringify({ status: receipt.status, viewport, fetchedWebSha256: receipt.identity.webSha256, images: receipt.images.items,
    uncredited: receipt.images.uncredited, screenshotCount: receipt.screenshots.length, receipt: path.join(OUT, 'receipt.json') }));
} catch (error) {
  receipt.status = 'FAIL'; receipt.error = String(error.stack || error); save();
  if (page) await page.screenshot({ path: path.join(OUT, 'FAIL.png'), timeout: 30_000 }).catch(() => {});
  throw error;
} finally {
  if (page) await page.evaluate(() => window.__chicago4d?.setAnimationHold?.(false)).catch(() => {});
  if (browser) await browser.close();
}
