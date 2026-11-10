/** Focused real published-app review. Does not publish, install, or modify source.
 * Run only after the parent grants the shared GPU slot and native15 is qualified.
 */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';

const args = Object.fromEntries(process.argv.slice(2).map((v, i, a) => v.startsWith('--') ? [v.slice(2), a[i + 1]] : null).filter(Boolean));
for (const k of ['url', 'viewport', 'out', 'expected']) assert(args[k], `--${k} required`);
assert(['desktop', 'phone'].includes(args.viewport));
assert(process.env.PW_MODULE, 'PW_MODULE must name the already-installed pinned Playwright module; this helper installs nothing');
const expected = JSON.parse(fs.readFileSync(args.expected));
const OUT = path.resolve(args.out);
fs.mkdirSync(OUT, { recursive: true });
const west = ['first_fort_dearborn_pickets_outer:w', 'first_fort_dearborn_pickets_inner:w'];
const south = west.map((id) => id.replace(/:w$/, ':s'));
for (const id of west) assert(/^[a-f0-9]{64}$/.test(expected.assets?.[id.split(':')[0]]?.sha256), `native web SHA256 required for ${id}`);
assert(expected.source_sha && expected.native_run, 'expected metadata must identify actual baked source and native run');
const phone = args.viewport === 'phone';
const viewport = phone ? { width: 390, height: 780 } : { width: 1280, height: 800 };
const receipt = { kind: 'FOCUSED_PUBLISHED_APP_REVIEW_NOT_FULL_SMOKE_OR_IMAGE_MATCH', status: 'RUNNING',
  url: args.url, viewport, deviceScaleFactor: phone ? 2 : 1, expected, observations: [], screenshots: [], pageErrors: [], failedRequests: [], badResponses: [] };
const save = () => fs.writeFileSync(path.join(OUT, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');

// Exactly retained review notes are annotations under AGENTS and smoke_renderer
// 1892-1906. Keep every raw problem; unrelated, malformed or duplicate notes fail.
function classifyProblems(raw, declared) {
  assert(Array.isArray(raw) && raw.every((p) => typeof p === 'string'), 'raw app problems must remain a string list');
  assert(Array.isArray(declared), 'actual registry review declarations required');
  for (const r of declared) {
    assert(r.flag === true && typeof r.key === 'string' && r.key === r.recordId && r.key === r.sidecarId,
      'retained annotation must bind one actual registry key, record and flagged sidecar');
  }
  const ids = declared.map((r) => r.key).sort();
  assert.equal(new Set(ids).size, ids.length, 'duplicate registry annotation declaration');
  if (expected.review_ids !== undefined) {
    assert(Array.isArray(expected.review_ids) && expected.review_ids.every((id) => typeof id === 'string'), 'expected review_ids must be a string list');
    assert.deepEqual(ids, [...expected.review_ids].sort(), 'actual retained review records differ from the optional native-manifest pin');
  }
  const messages = ids.map((id) => `${id}: review_required is set — review annotation retained; this flag does not block scene release`);
  for (const message of messages) assert.equal(raw.filter((p) => p === message).length, 1,
    `missing or duplicate retained review annotation: ${message}`);
  const allowed = new Set(messages);
  return { actualFlaggedIds: ids, annotations: raw.filter((p) => allowed.has(p)), hard: raw.filter((p) => !allowed.has(p)) };
}

const { chromium } = await import(pathToFileURL(process.env.PW_MODULE).href);
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || undefined,
  args: ['--enable-unsafe-swiftshader'] });
let page;
try {
  const ctx = await browser.newContext({ viewport, hasTouch: phone, isMobile: false, deviceScaleFactor: phone ? 2 : 1 });
  page = await ctx.newPage();
  page.setDefaultTimeout(60_000);
  page.on('pageerror', (e) => { receipt.pageErrors.push(String(e)); save(); });
  page.on('requestfailed', (r) => { receipt.failedRequests.push({ url: r.url(), error: r.failure()?.errorText }); });
  page.on('response', (r) => { if (r.status() >= 400) receipt.badResponses.push({ url: r.url(), status: r.status() }); });
  const url = new URL(args.url);
  url.searchParams.set('year', '1812');
  url.searchParams.set('keep-geometry', '1');
  assert(!url.pathname.includes('/renderers/web/'), 'published layout required');
  await page.goto(String(url), { waitUntil: 'domcontentloaded', timeout: 90_000 });
  await page.waitForFunction(() => window.__chicago4d?.ready === true || !!window.__chicago4d?.error,
    null, { timeout: 240_000, polling: 1000 });
  const identity = await page.evaluate(async () => {
    const a = window.__chicago4d;
    if (!a.ready) throw Error(a.error || 'not ready');
    const assets = [];
    for (const row of ['outer', 'inner']) {
      const id = `first_fort_dearborn_pickets_${row}`, record = a.registry.get(id);
      if (!record?.gltf || record.loadFailed || !record.assetUrl) throw Error(`${id}: no actual loaded native asset`);
      const response = await fetch(record.assetUrl, { cache: 'no-store' });
      if (!response.ok) throw Error(`${record.assetUrl}: ${response.status}`);
      const bytes = await response.arrayBuffer();
      const sha256 = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map((n) => n.toString(16).padStart(2, '0')).join('');
      assets.push({ id, url: record.assetUrl, bytes: bytes.byteLength, sha256, sidecarUrl: record.sidecarUrl,
        sidecar: { phase: record.sidecar.phase, placement: record.sidecar.placement, footprint: record.sidecar.footprint,
          gates: Object.fromEntries(['gate_sides', 'gate_width_m', 'gate_offset_m', 'gate_overrides'].map((k) => [k, record.sidecar.attributes[k]])) } });
    }
    return { ready: a.ready, error: a.error, scene: a.scene.id, targetDate: a.scene.target_date, dataBase: String(a.dataBase),
      buildStamp: document.getElementById('gate-build')?.textContent?.trim(), detail: a.detail, problems: a.problems,
      reviewDeclarations: [...a.registry.entries()].filter(([, r]) => r.sidecar?.review_required).map(([key, r]) =>
        ({ key, recordId: r.id, sidecarId: r.sidecar.id, flag: r.sidecar.review_required })),
      gates: a.fortGates.gates.map((g) => ({ id: g.id, state: g.state, at: g.at, span: g.span })), assets };
  });
  receipt.identity = identity; save();
  assert.equal(identity.scene, '1812');
  assert.equal(identity.targetDate, '1812-08-14');
  assert(!identity.dataBase.includes('/chicago/4d/data/') && identity.dataBase.includes('/data/'), 'published compressed-asset layout required');
  if (expected.build_prefix) assert(identity.buildStamp.startsWith(`build ${expected.build_prefix}`), 'published page build mismatch');
  for (const asset of identity.assets) {
    assert(asset.url.includes('/data/gltf/'), 'must read published web derivative');
    assert.equal(asset.sha256, expected.assets[asset.id].sha256, `${asset.id}: published/native web bytes differ`);
    assert.equal(asset.sidecar.placement.rotation_deg, 0);
    const row = asset.id.endsWith('inner') ? 'inner' : 'outer';
    assert.equal(asset.sidecar.gates.gate_width_m.value, 1.89);
    assert.equal(asset.sidecar.gates.gate_offset_m.value, row === 'inner' ? -2.62 : -2.83);
  }
  assert(west.concat(south).every((id) => identity.gates.some((g) => g.id === id && g.state === 'closed')), 'both west and south gates must start closed');
  receipt.problemClassification = classifyProblems(identity.problems, identity.reviewDeclarations);
  save();
  assert.equal(receipt.problemClassification.hard.length, 0, 'actual app reports unresolved hard loading/rendering problems');
  await page.waitForFunction(() => ['welcome', 'world'].includes(window.__chicago4d?.welcome?.state), null, { timeout: 90_000, polling: 500 });
  await page.evaluate(() => {
    const a = window.__chicago4d;
    if (a.welcome.state !== 'world') a.welcome.enter('spawn');
    document.exitPointerLock?.();
    document.getElementById('control-help-gotit')?.click();
    a.popup?.close(); a.navigator?.select('home'); a.navigator?.dock();
    a.setAnimationHold(true); a.setFloraSpread(true); a.intent.clear();
  });
  await page.waitForFunction(() => window.__chicago4d.welcome.state === 'world', null, { timeout: 90_000, polling: 500 });
  // Existing smoke_renderer holdDraws policy: measurements which read no pixel
  // still use the real app/world but need not submit the whole town to the GPU.
  await page.evaluate(() => {
    const r = window.__chicago4d.renderer;
    if (!window.__smokeHeldDraw) window.__smokeHeldDraw = r.render;
    r.render = (scene, camera) => { camera?.updateMatrixWorld?.(); };
  });


  async function pose(id, distance = 4, context = false, reverse = false) {
    return page.evaluate(({ id, distance, context, reverse }) => {
      const a = window.__chicago4d, g = a.fortGates.gates.find((v) => v.id === id);
      const west = id.endsWith(':w'), e = g.at[0] - (west ? distance : 0), n = g.at[1] - (west ? (context ? 5 : 0) : distance);
      a.intent.clear(); a.setFly(context);
      const altitude = context ? 8 : null;
      const targetY = a.walker.surfaceAt(...g.at) + 2;
      const eyeY = a.walker.surfaceAt(e, n) + (altitude ?? a.walkBudget.eyeHeight);
      const yaw = reverse ? (west ? 270 : 180) : (Math.atan2(g.at[0] - e, g.at[1] - n) * 180 / Math.PI + 360) % 360;
      const pitch = context ? Math.atan2(targetY - eyeY, Math.hypot(g.at[0] - e, g.at[1] - n)) * 180 / Math.PI : 0;
      a.walker.teleport({ local_e: e, local_n: n, yaw_deg: yaw, altitude_m: altitude, pitch_deg: pitch });
      a.interactKey.refresh();
      return { at: g.at, e: a.walker.state.e, n: a.walker.state.n, flying: a.walker.state.flying };
    }, { id, distance, context, reverse });
  }
  async function shot(name) {
    // Submit exactly one REAL frame at the actual pose, then leave the last
    // composited canvas in place while screenshot reads it. No substitute pixels.
    await page.evaluate(() => {
      const a = window.__chicago4d, r = a.renderer;
      if (!window.__smokeHeldDraw) throw Error('expected existing smoke draw hold');
      r.render = window.__smokeHeldDraw;
      try { a.step(); } finally { r.render = (scene, camera) => { camera?.updateMatrixWorld?.(); }; }
    });
    await page.screenshot({ path: path.join(OUT, name + '.png'), timeout: 90_000 });
    receipt.screenshots.push(name + '.png'); save(); console.log(`SHOT ${name}`, { screenshots: receipt.screenshots.length });
  }
  async function setStates(states) {
    const result = await page.evaluate((states) => {
      const a = window.__chicago4d, changed = [];
      for (const [id, state] of Object.entries(states)) {
        const g = a.fortGates.gates.find((x) => x.id === id);
        if (g.running) throw Error(`${id}: unexpected active interaction`);
        if (g.state !== state) { const result = a.interactions.act(id, state === 'open' ? 'open' : 'close'); if (!result.ok) throw Error(JSON.stringify(result)); changed.push(id); }
      }
      a.interactions.update(2);
      return changed.map((id) => ({ id, state: a.fortGates.gates.find((g) => g.id === id).state }));
    }, states);
    receipt.observations.push({ method: 'real app interactions engine, synchronous time advance', stateChanges: result }); save();
  }
  async function uiOpen(id) {
    await pose(id, 1.0);
    const before = await page.evaluate(() => { const a = window.__chicago4d; a.interactKey.refresh(); const b = document.getElementById('btn-interact');
      return { current: a.interactKey.current?.id, hidden: b.hidden, disabled: b.getAttribute('aria-disabled'), label: b.getAttribute('aria-label'), text: b.innerText }; });
    assert.equal(before.current, id, 'actual nearby Interact offer must target this leaf');
    assert(!before.hidden && before.disabled !== 'true');
    if (phone) await page.locator('#btn-interact').tap({ timeout: 60_000 });
    else { await page.locator('body').focus(); await page.keyboard.press('KeyR'); }
    const after = await page.evaluate((id) => { const a = window.__chicago4d, g = a.fortGates.gates.find((v) => v.id === id);
      const started = !!g.running; a.interactions.update(2); a.interactKey.refresh(); return { started, state: g.state, swing: g.swing }; }, id);
    assert(after.started && after.state === 'open' && after.swing === 1, 'actual UI action must start and finish the real leaf swing');
    receipt.observations.push({ id, method: phone ? 'actual Interact button tap' : 'actual R keyboard event', before, after }); save();
  }
  async function walk(ids, label, openIds = []) {
    await setStates(Object.fromEntries(ids.map((id) => [id, openIds.includes(id) ? 'open' : 'closed'])));
    const result = await page.evaluate(({ ids, label }) => {
      const a = window.__chicago4d, outer = a.fortGates.gates.find((g) => g.id === ids[0]), inner = a.fortGates.gates.find((g) => g.id === ids[1]);
      const west = ids[0].endsWith(':w'), start = [outer.at[0] - (west ? 4 : 0), outer.at[1] - (west ? 0 : 4)];
      a.intent.clear(); a.setFly(false); a.walker.teleport({ local_e: start[0], local_n: start[1], yaw_deg: west ? 90 : 0 });
      const distance = 4 + Math.hypot(inner.at[0] - outer.at[0], inner.at[1] - outer.at[1]) + 4;
      const steps = Math.ceil(distance / a.walkBudget.speed * 60), samples = [];
      for (let i = 0; i < steps; i++) { a.intent.forward = 1; a.walker.update(1 / 60, a.intent); if (i % 30 === 0) samples.push({ e: a.walker.state.e, n: a.walker.state.n, blocked: a.walker.state.blocked }); }
      a.intent.clear(); a.interactKey.refresh();
      return { label, method: 'actual loaded app walker + shared intent, terrain and current native-scene collision; synchronous 1/60 s steps',
        states: ids.map((id) => ({ id, state: a.fortGates.gates.find((g) => g.id === id).state })), start,
        end: [a.walker.state.e, a.walker.state.n], outer: outer.at, inner: inner.at, radius: a.walkBudget.radius, speed: a.walkBudget.speed,
        flying: a.walker.state.flying, groundY: a.walker.state.groundY, samples };
    }, { ids, label });
    const axis = ids[0].endsWith(':w') ? 0 : 1, e = result.end[axis], outer = result.outer[axis], inner = result.inner[axis];
    assert(!result.flying);
    assert(Math.abs(result.end[1 - axis] - result.outer[1 - axis]) < 0.08, `${label}: walk must stay in the actual aligned passage`);
    if (!openIds.includes(ids[0])) assert(e > outer - 1.2 && e < outer - result.radius + 0.05, `${label}: must reach and stop at actual shut outer leaf`);
    else if (!openIds.includes(ids[1])) assert(e > inner - 1.2 && e < inner - result.radius + 0.05 && e > outer + 0.3, `${label}: must stop between real rows at inner leaf`);
    else {
      assert(e > inner + 3, `${label}: actual terrain/collision must admit visitor into fort`);
      const sc = identity.assets.find((asset) => asset.id === ids[1].split(':')[0]).sidecar;
      const poly = Array.isArray(sc.footprint) ? sc.footprint : sc.footprint.polygon;
      const points = poly.map(([u, v]) => [sc.placement.local_e + u, sc.placement.local_n + v]);
      let inside = false;
      for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
        const [xi, yi] = points[i], [xj, yj] = points[j], [x, y] = result.end;
        if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside;
      }
      assert(inside, `${label}: successful walk must end within the actual inner footprint`);
    }
    receipt.observations.push(result); save(); console.log(`CASE ${label}: PASS`);
  }

  await pose(west[0], 12, true); await shot('01-west-context-closed');
  await pose(west[0], 4); await shot('02-west-outer-closed');
  await walk(west, 'west both shut');
  await walk(west, 'west inner-only open', [west[1]]);
  await setStates({ [west[1]]: 'closed' });
  await uiOpen(west[0]); await pose(west[0], 4); await shot('03-west-outer-open-inner-closed');
  await walk(west, 'west outer-only open', [west[0]]);
  await uiOpen(west[1]); await pose(west[0], 4); await shot('04-west-both-open');
  await walk(west, 'west both open', west);
  await page.evaluate(() => { const a = window.__chicago4d; a.walker.teleport({ yaw_deg: 270 }); });
  await shot('05-west-through-looking-back');
  await pose(south[0], 5); await shot('06-south-preserved-closed');
  await walk(south, 'south both shut');
  await walk(south, 'south both open', south);
  await page.evaluate(() => { const a = window.__chicago4d; a.walker.teleport({ yaw_deg: 180 }); });
  await shot('07-south-through-looking-back');
  const final = await page.evaluate(() => {
    const a = window.__chicago4d;
    return { problems: [...a.problems], reviewDeclarations: [...a.registry.entries()]
      .filter(([, r]) => r.sidecar?.review_required).map(([key, r]) =>
        ({ key, recordId: r.id, sidecarId: r.sidecar.id, flag: r.sidecar.review_required })) };
  });
  receipt.finalProblems = final.problems;
  receipt.finalProblemClassification = classifyProblems(final.problems, final.reviewDeclarations);
  save();
  assert.deepEqual(receipt.finalProblemClassification.actualFlaggedIds, receipt.problemClassification.actualFlaggedIds,
    'retained review records must not change during this focused scene review');
  assert.equal(receipt.finalProblemClassification.hard.length, 0, 'actual app reports unresolved hard problems after gate review');
  assert.equal(receipt.pageErrors.length, 0, 'page errors');
  assert.equal(receipt.failedRequests.length, 0, 'failed network requests');
  assert.equal(receipt.badResponses.length, 0, 'HTTP error responses');
  receipt.status = 'PASS_FOCUSED_REVIEW_REQUIRES_HUMAN_SCREENSHOT_INSPECTION'; save();
  console.log(JSON.stringify({ status: receipt.status, viewport, screenshots: receipt.screenshots.length, receipt: path.join(OUT, 'receipt.json') }));
} catch (error) {
  receipt.status = 'FAIL'; receipt.error = String(error.stack || error); save();
  if (page) await page.screenshot({ path: path.join(OUT, 'FAIL.png'), timeout: 30_000 }).catch(() => {});
  throw error;
} finally {
  if (page) await page.evaluate(() => {
    const a = window.__chicago4d;
    if (a?.renderer && window.__smokeHeldDraw) { a.renderer.render = window.__smokeHeldDraw; delete window.__smokeHeldDraw; }
    a?.setAnimationHold?.(false);
  }).catch(() => {});
  await browser.close();
}
