#!/usr/bin/env node
// External observer only: real published assets, native APIs, real WebGL readback.
import fs from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import crypto from 'node:crypto';
import { promisify } from 'node:util';
import { execFile } from 'node:child_process';
const run = promisify(execFile);
const arg = (name) => process.argv[process.argv.indexOf(name) + 1];
for (const key of ['--app-root', '--published-root', '--out', '--runtime-manifest']) {
  if (!process.argv.includes(key)) throw new Error(`Missing required ${key}`);
}
const appRoot = path.resolve(arg('--app-root'));
const mirror = path.resolve(arg('--published-root'));
const out = path.resolve(arg('--out'));
function validateRuntimeManifest(bytes) {
  const rows = JSON.parse(bytes.toString('utf8'));
  const required = new Set([
    'renderers/web/js/ktx2.js',
    'renderers/web/js/texture-residency.js',
    'renderers/web/js/main.js',
    'renderers/web/js/shared-images.js',
    'renderers/web/js/buildings.js',
  ]);
  if (!Array.isArray(rows) || rows.length !== required.size) {
    throw new Error('Runtime manifest must contain exactly the five reviewed runtime paths');
  }
  const seen = new Set();
  for (const row of rows) {
    if (!row || !required.has(row.path)) throw new Error(`Unknown runtime manifest path ${row?.path}`);
    if (seen.has(row.path)) throw new Error(`Duplicate runtime manifest path ${row.path}`);
    if (typeof row.proposed_sha256 !== 'string' || !/^[a-f0-9]{64}$/i.test(row.proposed_sha256)) {
      throw new Error(`Invalid runtime manifest SHA-256 for ${row.path}`);
    }
    seen.add(row.path);
  }
  return rows.map((row) => ({ ...row, proposed_sha256: row.proposed_sha256.toLowerCase() }));
}
const manifestBytes = await fs.readFile(arg('--runtime-manifest'));
const expectedManifest = validateRuntimeManifest(manifestBytes);
const runtimeManifestSha256 = crypto.createHash('sha256').update(manifestBytes).digest('hex');
if ([appRoot, mirror].some((root) => out === root || out.startsWith(`${root}/`))) {
  throw new Error('Observer outputs must stay outside source and published mirror');
}
if (!process.env.TMPDIR || path.resolve(process.env.TMPDIR).length > 40) {
  throw new Error('Use a fresh, short owned browser TMPDIR (absolute length<=40)');
}
await fs.mkdir(out, { recursive: false });
const started = Date.now();
const result = { scope: 'T3173 actual published 1904 lifecycle observer', started_utc: new Date().toISOString(),
  app_root: appRoot, published_root: mirror, runtime_manifest: path.resolve(arg('--runtime-manifest')),
  runtime_manifest_sha256: runtimeManifestSha256, runtime_module_count: expectedManifest.length,
  execution_mode: 'Native renderer animation loop stopped after real enter/hold; original explicit native step and window RAF loops unchanged',
  status: 'RUNNING', rows: [], failures: [], visual_acceptance: 'UNRUN', memory_acceptance: 'SEPARATE_NATIVE_TOOL',
  browser_closed: false, server_closed: false };
const save = async () => fs.writeFile(path.join(out, 'ACTUAL-STATE.json'), `${JSON.stringify(result, null, 2)}\n`);
function check(label, ok, detail = null) {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${label}${detail === null ? '' : ` ${JSON.stringify(detail)}`}`);
  if (!ok) result.failures.push({ label, detail });
}
async function shaFile(file) {
  const hash = crypto.createHash('sha256');
  for await (const bytes of createReadStream(file)) hash.update(bytes);
  return hash.digest('hex');
}
async function inventory(root, source = false) {
  let files = [];
  if (source) {
    const { stdout } = await run('git', ['-C', root, 'ls-files', '-z', '--', '.'],
      { encoding: 'utf8', maxBuffer: 16 * 1024 * 1024, env: { ...process.env, GIT_NO_LAZY_FETCH: '1' } });
    files = stdout.split('\0').filter(Boolean).sort();
  } else {
    async function visit(dir, prefix = '') {
      for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
        const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
        if (entry.isDirectory()) await visit(path.join(dir, entry.name), relative);
        else if (entry.isFile()) files.push(relative);
        else throw new Error(`Unexpected published nonregular entry ${relative}`);
      }
    }
    await visit(root); files.sort();
  }
  const rows = [];
  for (const relative of files) {
    const file = path.join(root, relative);
    const stat = await fs.lstat(file);
    if (stat.isSymbolicLink()) rows.push({ path: relative, link: await fs.readlink(file) });
    else rows.push({ path: relative, bytes: stat.size, sha256: await shaFile(file) });
  }
  const digest = crypto.createHash('sha256').update(JSON.stringify(rows)).digest('hex');
  return { files: rows.length, bytes: rows.reduce((n, row) => n + (row.bytes || 0), 0), digest, rows };
}
async function guard(name) {
  const source = await inventory(appRoot, true);
  const published = await inventory(mirror);
  const vendorRows = source.rows.filter((row) => row.path.startsWith('renderers/web/vendor/'));
  const vendor = crypto.createHash('sha256').update(JSON.stringify(vendorRows)).digest('hex');
  for (const row of expectedManifest) {
    const actual = source.rows.find((entry) => entry.path === row.path);
    if (!actual || actual.sha256 !== row.proposed_sha256) throw new Error(`Runtime pin mismatch ${row.path}`);
    const mirrorPath = row.path.replace('renderers/web/', 'walk/');
    const served = published.rows.find((entry) => entry.path === mirrorPath);
    if (!served || served.sha256 !== row.proposed_sha256) throw new Error(`Published runtime pin mismatch ${mirrorPath}`);
  }
  const { stdout: head } = await run('git', ['-C', appRoot, 'rev-parse', 'HEAD'],
    { env: { ...process.env, GIT_NO_LAZY_FETCH: '1' } });
  const record = { source, published, vendor_digest: vendor, source_head: head.trim() };
  await fs.writeFile(path.join(out, `${name}-SOURCE-MIRROR-VENDOR.json`), `${JSON.stringify(record, null, 2)}\n`);
  return { source: source.digest, mirror: published.digest, vendor, source_head: head.trim(),
    source_files: source.files, mirror_files: published.files };
}
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.glb': 'model/gltf-binary', '.bin': 'application/octet-stream',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.wasm': 'application/wasm', '.ktx2': 'image/ktx2', '.woff2': 'font/woff2', '.md': 'text/markdown' };
let browser, server;
const profileRows = [
  { name: 'mobile', viewport: { width: 390, height: 780 }, hasTouch: true, isMobile: true, deviceScaleFactor: 3, detail: 'light' },
  { name: 'desktop', viewport: { width: 1280, height: 800 }, hasTouch: false, isMobile: false, deviceScaleFactor: 1, detail: 'full' },
];
const stand = { local_e: 1405, local_n: -3230, yaw_deg: 270, pitch_deg: 0 };
// Native FLY.maxAltitude is absolute camera Y above datum, not ground-relative altitude.
function matchesNativeFlightClamp(observed, requestedAltitude) {
  const { ground_y: ground, eye_y: eye, altitude } = observed.walker;
  const { max_altitude: max, min_clearance: min } = observed.native_flight || {};
  if (![ground, eye, altitude, max, min, requestedAltitude].every(Number.isFinite)
      || max !== 900 || min <= 0 || !observed.walker.flying) return false;
  const requestedEye = ground + Math.max(min, requestedAltitude);
  const expectedEye = Math.max(ground + min, Math.min(max, requestedEye));
  return eye === expectedEye && observed.camera[1] === expectedEye
    && altitude === expectedEye - ground;
}
async function enterAndHold(page) {
  await page.waitForFunction(() => window.__chicago4d?.ready || window.__chicago4d?.error,
    null, { timeout: 420000 });
  const error = await page.evaluate(() => window.__chicago4d.error);
  if (error) throw new Error(`Application boot error: ${error}`);
  await page.evaluate(async () => {
    const api = window.__chicago4d;
    const deadline = Date.now() + 90000;
    while (api.welcome.state !== 'world' && Date.now() < deadline) {
      if (api.welcome.state === 'welcome') api.welcome.enter('spawn');
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    if (api.welcome.state !== 'world') throw new Error('Welcome did not enter the actual world');
    api.setAnimationHold(true);
    const { FLY } = await import(new URL('../walk/js/travel-settings.js', location.href).href);
    if (!Number.isFinite(FLY.maxAltitude) || !Number.isFinite(FLY.minClearance)) {
      throw new Error('Native flight settings unavailable');
    }
    window.__t3173ObserverFlight = { max_altitude: FLY.maxAltitude, min_clearance: FLY.minClearance };
    // Stop only Three's implicit renderer RAF. Every explicit native step() and
    // window requestAnimationFrame loop below remains byte-for-byte unchanged.
    api.renderer.setAnimationLoop(null);
    window.__t3173ObserverManualLoop = true;
  });
}
async function settle(page, waypoint = null) {
  return page.evaluate(async (at) => {
    const api = window.__chicago4d;
    if (at) {
      api.setFly(typeof at.altitude_m === 'number');
      api.walker.teleport(at);
    }
    const deadline = Date.now() + 90000;
    // Existing native APIs drive the actual production residency and draw path.
    for (let i = 0; i < 10; i++) {
      api.step(); await new Promise((resolve) => requestAnimationFrame(resolve));
    }
    while ((api.residency?.pending || 0) > 0 && Date.now() < deadline) {
      api.step(); await new Promise((resolve) => requestAnimationFrame(resolve));
    }
    for (let i = 0; i < 5; i++) {
      api.step(); await new Promise((resolve) => requestAnimationFrame(resolve));
    }
    const r = api.residency;
    return { detail: api.detail, profile: api.device?.choice, welcome: api.welcome.state,
      renderer_calls: api.renderer.info.render.calls, triangles: api.renderer.info.render.triangles,
      camera: api.camera.position.toArray(), camera_quaternion: api.camera.quaternion.toArray(), banked_assets: api.bankedAssets,
      native_flight: { ...window.__t3173ObserverFlight }, manual_renderer_loop: window.__t3173ObserverManualLoop === true,
      walker: { e: api.walker.state.e, n: api.walker.state.n, altitude: api.walker.state.altitude,
        ground_y: api.walker.state.groundY, eye_y: api.walker.state.eyeY,
        flying: api.walker.state.flying }, upload_release: api.uploadRelease,
      residency: r && { ...r, problems: [...r.problems] }, crash_guard: { ...api.crashGuard } };
  }, waypoint);
}
async function structureState(page, remember = false) {
  return page.evaluate(async (saveIdentity) => {
    const api = window.__chicago4d, record = api.registry.get('glessner_house');
    if (!record?.gltf?.scene) throw new Error('Actual Glessner source scene is missing');
    if (saveIdentity) window.__t3173ObserverIdentity = { registry: api.registry, record, sidecar: record.sidecar };
    const identity = window.__t3173ObserverIdentity;
    const geometries = [], materials = new Set();
    record.gltf.scene.traverse((node) => {
      if (node.geometry) geometries.push({ name: node.name,
        attributes: Object.entries(node.geometry.attributes).map(([key, attr]) => ({ key, count: attr.count,
          itemSize: attr.itemSize, normalized: attr.normalized, array: (attr.data?.array || attr.array)?.constructor.name })),
        index: node.geometry.index?.count || 0 });
      for (const material of [].concat(node.material || [])) materials.add(material);
    });
    const materialState = [...materials].map((material) => ({ name: material.name, type: material.type,
      color: material.color?.toArray(), roughness: material.roughness, metalness: material.metalness,
      opacity: material.opacity, side: material.side, transparent: material.transparent, transmission: material.transmission,
      textures: Object.entries(material).filter(([, value]) => value?.isTexture).map(([key, tex]) => ({ key,
        format: tex.format, type: tex.type, wrapS: tex.wrapS, wrapT: tex.wrapT, minFilter: tex.minFilter,
        magFilter: tex.magFilter, anisotropy: tex.anisotropy, channel: tex.channel, colorSpace: tex.colorSpace,
        flipY: tex.flipY, offset: tex.offset.toArray(), repeat: tex.repeat.toArray(), rotation: tex.rotation,
        image: [tex.image?.width, tex.image?.height], mips: tex.mipmaps?.map((m) => [m.width, m.height]) })) }));
    const digest = async (value) => [...new Uint8Array(await crypto.subtle.digest('SHA-256',
      new TextEncoder().encode(JSON.stringify(value))))].map((n) => n.toString(16).padStart(2, '0')).join('');
    return { id: record.id, asset_url: record.assetUrl, asset_detail: record.assetDetail, version: record.version,
      sidecar_sha256: await digest(record.sidecar), geometry_metadata_sha256: await digest(geometries),
      material_sampler_sha256: await digest(materialState), mesh_count: geometries.length,
      stable_references: !!identity && identity.registry === api.registry && identity.record === record
        && identity.sidecar === record.sidecar, banked_assets: api.bankedAssets,
      roll: { expected: api.roll?.expected, standing: api.roll?.standing, missing: api.roll?.missing } };
  }, remember);
}
async function frame(page, name) {
  const captured = await page.evaluate(async (key) => {
    const api = window.__chicago4d; api.step();
    const gl = api.renderer.getContext(), w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    const pixels = new Uint8Array(w * h * 4);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
    const glError = gl.getError();
    let lit = 0, sum = 0;
    for (let i = 0; i < pixels.length; i += 4) {
      const luminance = .2126 * pixels[i] + .7152 * pixels[i + 1] + .0722 * pixels[i + 2];
      sum += luminance; if (luminance > 8) lit++;
    }
    window.__t3173ObserverPixels ??= {};
    window.__t3173ObserverPixels[key] = pixels;
    const digest = [...new Uint8Array(await crypto.subtle.digest('SHA-256', pixels))]
      .map((n) => n.toString(16).padStart(2, '0')).join('');
    const canvas = document.createElement('canvas'); canvas.width = w; canvas.height = h;
    const image = new Uint8ClampedArray(pixels.length);
    for (let y = 0; y < h; y++) image.set(pixels.subarray(y * w * 4, (y + 1) * w * 4), (h - y - 1) * w * 4);
    canvas.getContext('2d').putImageData(new ImageData(image, w, h), 0, 0);
    return { width: w, height: h, gl_error: glError, pixel_sha256: digest,
      mean_luminance: sum / (w * h), lit_fraction: lit / (w * h), png: canvas.toDataURL('image/png') };
  }, name);
  const png = Buffer.from(captured.png.split(',')[1], 'base64'); delete captured.png;
  const file = `${name}.png`; await fs.writeFile(path.join(out, file), png);
  captured.png = { file, bytes: png.length, sha256: crypto.createHash('sha256').update(png).digest('hex') };
  check(`${name}: actual populated GPU frame`, captured.gl_error === 0 && captured.mean_luminance > 8
    && captured.lit_fraction > .25, captured);
  return captured;
}
async function compare(page, first, second) {
  return page.evaluate(([a, b]) => {
    const p = window.__t3173ObserverPixels[a], q = window.__t3173ObserverPixels[b];
    if (!p || !q || p.length !== q.length) throw new Error('Missing or mismatched actual pixel buffers');
    let changed = 0, squared = 0, max = 0;
    for (let i = 0; i < p.length; i += 4) {
      let moved = false;
      for (let k = 0; k < 3; k++) {
        const difference = Math.abs(p[i + k] - q[i + k]);
        max = Math.max(max, difference); squared += difference * difference;
        if (difference > 8) moved = true;
      }
      if (moved) changed++;
    }
    return { changed_pixels_over_8: changed, changed_share: changed / (p.length / 4),
      rgb_rmse: Math.sqrt(squared / (p.length / 4 * 3)), max_channel_difference: max };
  }, [first, second]);
}
try {
  result.before = await guard('BEFORE'); await save();
  server = http.createServer(async (req, res) => {
    try {
      const relative = decodeURIComponent(new URL(req.url, 'http://local').pathname).replace(/^\/+/, '');
      let file = path.resolve(mirror, relative);
      if (file !== mirror && !file.startsWith(`${mirror}/`)) throw new Error('Path outside mirror');
      if ((await fs.stat(file)).isDirectory()) file = path.join(file, 'index.html');
      res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream' });
      createReadStream(file).pipe(res);
    } catch { res.writeHead(404); res.end('not found'); }
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  let playwright;
  try { playwright = await import('playwright'); }
  catch {
    const { stdout } = await run('npm', ['root', '-g']);
    playwright = await import(path.join(stdout.trim(), 'playwright', 'index.js'));
  }
  const chromium = playwright.chromium || playwright.default.chromium;
  browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || '/usr/bin/chromium',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  for (const config of profileRows) {
    const { name, detail, ...profile } = config;
    const ctx = await browser.newContext(profile);
    const row = { profile: name, target_detail: detail, errors: [], request_failures: [], console_errors: [],
      http_errors: [], warnings: [], captures: {}, glb_requests: [], phase: 'boot' };
    result.rows.push(row); await save();
    try {
      await ctx.addInitScript((tier) => {
        localStorage.setItem('chicago4d.settings', JSON.stringify({ detail: tier }));
      }, detail);
      const page = await ctx.newPage(); page.setDefaultTimeout(90000);
      let loads = 0;
      page.on('load', () => loads++);
      page.on('request', (request) => {
        if (new URL(request.url()).pathname.endsWith('.glb')) row.glb_requests.push({ url: request.url(), phase: row.phase });
      });
      page.on('pageerror', (error) => row.errors.push(String(error)));
      page.on('requestfailed', (request) => row.request_failures.push({ url: request.url(), failure: request.failure() }));
      page.on('response', (response) => {
        if (response.status() >= 400) row.http_errors.push({ url: response.url(), status: response.status() });
      });
      page.on('console', (message) => {
        if (message.type() === 'error') row.console_errors.push(message.text());
        if (message.type() === 'warning') row.warnings.push(message.text());
      });
      await page.goto(`http://127.0.0.1:${server.address().port}/1904/?device=standard`, { waitUntil: 'domcontentloaded' });
      await enterAndHold(page); row.initial = await settle(page, stand);
      check(`${name}: actual requested detail and released compressed sources`, row.initial.banked_assets === 0 && row.initial.detail === detail && row.initial.profile?.textures === (name === 'mobile' ? 'light' : 'full')
        && row.initial.upload_release.compressed > 0 && row.initial.residency?.released > 0
        && row.initial.residency.pending === 0 && row.initial.residency.problems.length === 0, row.initial);
      row.captures.before = await frame(page, `${name}-before`);
      await settle(page); row.captures.noise = await frame(page, `${name}-noise`);
      row.held_noise = await compare(page, `${name}-before`, `${name}-noise`);
      row.away = await settle(page, { ...stand, altitude_m: 1000, pitch_deg: -30 });
      check(`${name}: native absolute flight clamp and complete real source eviction`,
        matchesNativeFlightClamp(row.away, 1000) && row.away.manual_renderer_loop
        && row.initial.residency.resident > 0 && row.away.residency.resident === 0
        && row.away.residency.evictions - row.initial.residency.evictions === row.initial.residency.resident, row.away);
      row.returned = await settle(page, stand);
      check(`${name}: actual return retranscodes and uploads`, row.returned.residency.retranscodes > row.initial.residency.retranscodes
        && row.returned.residency.uploads > row.initial.residency.uploads && row.returned.residency.pending === 0
        && row.returned.residency.problems.length === 0 && row.returned.banked_assets === 0, row.returned);
      row.captures.returned = await frame(page, `${name}-returned`);
      row.return_comparison = await compare(page, `${name}-before`, `${name}-returned`);
      check(`${name}: return camera is exactly the original camera`, JSON.stringify(row.initial.camera) === JSON.stringify(row.returned.camera)
        && JSON.stringify(row.initial.camera_quaternion) === JSON.stringify(row.returned.camera_quaternion));
      check(`${name}: returned appearance adds no changed pixels beyond held baseline noise`,
        row.return_comparison.changed_pixels_over_8 <= row.held_noise.changed_pixels_over_8,
        { noise: row.held_noise, returned: row.return_comparison });
      await save();
      if (name === 'desktop') {
        row.detail_cycle = { before: await structureState(page, true) };
        row.phase = 'detail-balanced';
        await page.evaluate(async () => { await window.__chicago4d.setDetail('balanced'); });
        row.detail_cycle.balanced = await settle(page, stand);
        row.detail_cycle.balanced_structure = await structureState(page);
        check('desktop: real Balanced replacement refetches its declared lower asset without a raw bank',
          row.detail_cycle.balanced.detail === 'balanced' && row.detail_cycle.balanced.banked_assets === 0
          && row.detail_cycle.balanced_structure.asset_detail === 'balanced'
          && row.detail_cycle.balanced_structure.asset_url !== row.detail_cycle.before.asset_url
          && row.detail_cycle.balanced_structure.stable_references
          && row.glb_requests.some((request) => request.phase === 'detail-balanced'
            && request.url === row.detail_cycle.balanced_structure.asset_url), row.detail_cycle.balanced_structure);
        row.phase = 'detail-full-return';
        await page.evaluate(async () => { await window.__chicago4d.setDetail('full'); });
        row.detail_cycle.returned = await settle(page, stand);
        row.detail_cycle.returned_structure = await structureState(page);
        const previous = row.detail_cycle.before, restored = row.detail_cycle.returned_structure;
        check('desktop: real Full return refetches and preserves structure identity, geometry metadata and material/samplers',
          row.detail_cycle.returned.detail === 'full' && row.detail_cycle.returned.banked_assets === 0
          && restored.stable_references && restored.asset_detail === 'full' && restored.asset_url === previous.asset_url
          && restored.sidecar_sha256 === previous.sidecar_sha256 && restored.mesh_count === previous.mesh_count
          && restored.geometry_metadata_sha256 === previous.geometry_metadata_sha256
          && restored.material_sampler_sha256 === previous.material_sampler_sha256
          && JSON.stringify(restored.roll) === JSON.stringify(previous.roll)
          && row.glb_requests.some((request) => request.phase === 'detail-full-return' && request.url === restored.asset_url), restored);
        row.captures.detail_returned = await frame(page, 'desktop-detail-returned');
        row.detail_cycle.pixel_comparison = await compare(page, 'desktop-returned', 'desktop-detail-returned');
        check('desktop: Full detail cycle restores the exact camera',
          JSON.stringify(row.detail_cycle.returned.camera) === JSON.stringify(row.returned.camera)
          && JSON.stringify(row.detail_cycle.returned.camera_quaternion) === JSON.stringify(row.returned.camera_quaternion));
        check('desktop: Full detail cycle adds no changed pixels beyond held baseline noise',
          row.detail_cycle.pixel_comparison.changed_pixels_over_8 <= row.held_noise.changed_pixels_over_8,
          { noise: row.held_noise, full_detail_cycle: row.detail_cycle.pixel_comparison });
        row.phase = 'context-loss'; await save();
        row.context_before = { loads, ...await page.evaluate(() => ({ guard: { ...window.__chicago4d.crashGuard },
          compressed: window.__chicago4d.uploadRelease.compressed })) };
        row.context_loss = await page.evaluate(async () => {
          const api = window.__chicago4d, gl = api.renderer.getContext();
          const extension = gl.getExtension('WEBGL_lose_context');
          if (!extension) throw new Error('Actual WEBGL_lose_context extension unavailable');
          const lost = new Promise((resolve) => gl.canvas.addEventListener('webglcontextlost', (event) => {
            resolve({ default_prevented: event.defaultPrevented });
          }, { once: true }));
          extension.loseContext(); const event = await lost;
          await new Promise((resolve) => setTimeout(resolve, 50));
          const beforeRestore = { notice: api.crashGuard.notice, losses: api.crashGuard.sessionLosses,
            reloads: api.crashGuard.reloads, ...event };
          extension.restoreContext(); return beforeRestore;
        });
        await page.waitForFunction(() => window.__chicago4d?.ready
          && window.__chicago4d.crashGuard.reloads === 1, null, { timeout: 450000 });
        await enterAndHold(page); row.context_reloaded = await settle(page, stand);
        row.context_loads = loads;
        check('desktop: genuine context loss restored via one normal reload', row.context_loss.default_prevented
          && row.context_loss.losses === 1 && row.context_loss.reloads === 0
          && row.context_reloaded.crash_guard.reloads === 1 && row.context_reloaded.crash_guard.sessionLosses === 1
          && loads === row.context_before.loads + 1, { before: row.context_before, lost: row.context_loss,
            after: row.context_reloaded.crash_guard, loads });
        check('desktop: normal reload rebuilds Full compressed-source lifecycle', row.context_reloaded.detail === 'full'
          && row.context_reloaded.profile?.textures === 'full' && row.context_reloaded.banked_assets === 0
          && row.context_reloaded.upload_release.compressed > 0
          && row.context_reloaded.residency?.pending === 0 && row.context_reloaded.residency.problems.length === 0, row.context_reloaded);
        row.captures.reloaded = await frame(page, 'desktop-context-reloaded');
      }
      await page.waitForLoadState('networkidle', { timeout: 30000 });
      check(`${name}: no page/request/HTTP/console errors`, !row.errors.length && !row.request_failures.length
        && !row.http_errors.length && !row.console_errors.length,
        { errors: row.errors, requests: row.request_failures, http: row.http_errors, console: row.console_errors });
      row.status = 'COMPLETE'; await save();
    } finally { await ctx.close(); }
  }
  result.visual_acceptance = result.failures.length ? 'FAILED_OBSERVER_REVIEW_REQUIRED' : 'SAME_CAMERA_PIXEL_CHECK_PASS_ROOT_IMAGE_REVIEW_REQUIRED';
} catch (error) {
  result.exception = String(error.stack || error); result.failures.push({ label: 'Observer exception', detail: result.exception });
} finally {
  if (browser) { await browser.close(); result.browser_closed = true; }
  if (server) { await new Promise((resolve) => server.close(resolve)); result.server_closed = true; }
  try {
    result.after = await guard('AFTER');
    check('source, mirror, vendor and HEAD remain pinned', JSON.stringify(result.before) === JSON.stringify(result.after));
  } catch (error) { result.failures.push({ label: 'Final source/mirror guard failed', detail: String(error) }); }
  result.status = result.failures.length ? 'FAIL' : 'PASS';
  result.elapsed_seconds = (Date.now() - started) / 1000;
  result.finished_utc = new Date().toISOString(); await save();
  await fs.writeFile(path.join(out, 'ACTUAL-RESULT.json'), `${JSON.stringify(result, null, 2)}\n`);
  process.exitCode = result.failures.length ? 1 : 0;
  console.log(`ACTUAL ${result.status}: ${result.rows.length} profiles, ${result.failures.length} failures; ${result.elapsed_seconds}s`);
}
