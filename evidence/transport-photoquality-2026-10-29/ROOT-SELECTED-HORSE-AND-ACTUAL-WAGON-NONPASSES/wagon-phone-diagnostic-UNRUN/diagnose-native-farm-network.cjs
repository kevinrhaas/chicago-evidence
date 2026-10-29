// Prepared observation only: native published fixture, native UI and native counters.
// Root review/resource GO and an owned outer supervisor are required before execution.
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const os = require('node:os');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const [repoArg, outArg, sealArg, indexArg, expectedHead, profileSelection] = process.argv.slice(2);
assert.ok(['phone','both'].includes(profileSelection), 'Explicit diagnostic scope');
assert.equal(process.argv.length, 8, 'node diagnose-native-farm-network.cjs REPO FRESH_OUT FIVE_PATH_SEAL FROZEN_INDEX EXACT_EXPECTED_HEAD phone|both');
assert.match(expectedHead, /^[0-9a-f]{40}$/, 'Root supplies the exact actual precommitted or committed feature HEAD');
const repo = path.resolve(repoArg), out = path.resolve(outArg);
const app = path.join(repo, 'chicago/4d'), mirrorRoot = path.join(repo, 'site/4d');
const fixture = path.join(mirrorRoot, 'walk/transport/farm-box-master');
const {chromium} = require(require.resolve('playwright', {paths: [repo]}));
const digest = raw => crypto.createHash('sha256').update(raw).digest('hex');
const git = (...args) => cp.execFileSync('git', ['-C', repo, ...args], {maxBuffer: 64 * 1024 * 1024});
const sealRaw = fs.readFileSync(path.resolve(sealArg)), seal = JSON.parse(sealRaw);
const indexRaw = fs.readFileSync(path.resolve(indexArg));
const sourceRows = [...new Map([...seal.paths, ...seal.protected_checked_paths].map(row => [row.path, row])).values()];
const sourceRecord = JSON.parse(fs.readFileSync(path.join(app, 'assets/authored/transport/farm_box_master_v1/SOURCE.json')));
const lods = Object.fromEntries(sourceRecord.web_export.levels.map(row => [row.level, row]));
assert.ok(!fs.existsSync(out) && out !== repo && !out.startsWith(repo + '/'), 'Fresh output outside checkout');
assert.ok(fs.existsSync(fixture), 'Actual supported publication required; never synthesize fixture HTML');
const scratch = os.tmpdir(), scratchStat = fs.lstatSync(scratch);
assert.ok(process.env.TMPDIR && path.isAbsolute(scratch) && scratch.length <= 35);
assert.ok(scratchStat.isDirectory() && !scratchStat.isSymbolicLink() && scratchStat.uid === process.getuid());
assert.equal(fs.readdirSync(scratch).length, 0, 'Fresh owned scratch');
assert.ok(!scratch.startsWith(repo + '/'), 'Scratch outside checkout');
const memoryMaxText = fs.readFileSync('/sys/fs/cgroup/memory.max', 'utf8').trim();
const memoryMax = memoryMaxText === 'max' ? Infinity : Number(memoryMaxText);
const memoryCurrent = Number(fs.readFileSync('/sys/fs/cgroup/memory.current', 'utf8').trim());
assert.ok(memoryMax - memoryCurrent >= 2 * 1024 ** 3, 'Two GiB actual cgroup reserve');
const outputSpace = fs.statfsSync(path.dirname(out));
assert.ok(Number(outputSpace.bavail) * Number(outputSpace.bsize) > 50 * 1024 ** 2 + 512 * 1024 ** 2);
function snapshot() {
  assert.equal(git('rev-parse', 'HEAD').toString().trim(), expectedHead);
  assert.deepEqual(git('ls-files', '--stage', '-z'), indexRaw, 'Complete frozen semantic index');
  assert.equal(git('diff', '--name-only').toString(), '', 'No unstaged tracked source');
  const sources = sourceRows.map(row => {
    const bytes = fs.readFileSync(path.join(repo, row.path));
    assert.equal(bytes.length, row.bytes, row.path); assert.equal(digest(bytes), row.sha256, row.path);
    return {path: row.path, bytes: bytes.length, sha256: digest(bytes)};
  });
  const mirror = [];
  function walk(dir) {
    for (const name of fs.readdirSync(dir).sort()) {
      const file = path.join(dir, name), stat = fs.lstatSync(file);
      assert.ok(!stat.isSymbolicLink(), 'Ordinary published mirror');
      if (stat.isDirectory()) walk(file);
      else {
        assert.ok(stat.isFile()); const bytes = fs.readFileSync(file);
        mirror.push({path: path.relative(mirrorRoot, file), bytes: bytes.length, sha256: digest(bytes)});
      }
    }
  }
  walk(mirrorRoot);
  return {HEAD: git('rev-parse', 'HEAD').toString().trim(), semantic_index_sha256: digest(indexRaw),
    seal_sha256: digest(sealRaw), sources, mirror};
}
const before = snapshot(); fs.mkdirSync(out);
const save = (name, value) => fs.writeFileSync(path.join(out, name), JSON.stringify(value, null, 2) + '\n');
save('BEFORE.json', before);
const eventStart=process.hrtime.bigint();let eventSequence=0,phase='server-start';
const trace=(kind,data={})=>fs.appendFileSync(path.join(out,'NETWORK-EVENTS.ndjson'),JSON.stringify({seq:++eventSequence,at:new Date().toISOString(),elapsed_ms:Number(process.hrtime.bigint()-eventStart)/1e6,phase,kind,...data})+'\n');
trace('BEFORE-GUARDS-COMPLETE',{HEAD:expectedHead});
const errors = {page: [], console: [], http: [], requests: [], closure: [], integrity: []};
const warnings = [], responses = [], responseReads = [], profiles = [];
let server, browser, currentContext;
const mime = {'.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.glb': 'model/gltf-binary', '.wasm': 'application/wasm', '.webp': 'image/webp', '.png': 'image/png', '.css': 'text/css'};
function closeServer(value) { return new Promise((resolve, reject) => value.close(error => error ? reject(error) : resolve())); }
(async () => {
  try {
    server = http.createServer((request, response) => {
      try {
        const pathname = decodeURIComponent(new URL(request.url, 'http://fixture').pathname);
        let file = path.resolve(mirrorRoot, '.' + pathname);
        assert.ok(file === mirrorRoot || file.startsWith(mirrorRoot + '/'), 'Contained published URL');
        if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
          errors.http.push({pathname, status: 404}); response.writeHead(404); response.end(); return;
        }
        const body = fs.readFileSync(file);
        response.writeHead(200, {'content-type': mime[path.extname(file)] || 'application/octet-stream', 'content-length': body.length, 'cache-control': 'no-store'});
        response.end(body);
      } catch (error) { errors.http.push({message: String(error)}); response.writeHead(500); response.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    browser = await chromium.launch({executablePath: process.env.PW_EXECUTABLE || undefined});
    for (const profile of [
      {name: 'desktop', viewport: {width: 1280, height: 800}, deviceScaleFactor: 1, isMobile: false, hasTouch: false},
      {name: 'phone', viewport: {width: 390, height: 780}, deviceScaleFactor: 3, isMobile: true, hasTouch: true},
    ]) {
      if(profileSelection==='phone'&&profile.name!=='phone')continue;
      const {name, ...contextOptions} = profile;phase=name+'-context-create';trace('CONTEXT-CREATE-BEGIN',{profile});
      currentContext = await browser.newContext(contextOptions);
      const page = await currentContext.newPage(); page.setDefaultTimeout(120000);
      const requestIDs=new Map();let requestSequence=0;const rid=request=>{if(!requestIDs.has(request))requestIDs.set(request,++requestSequence);return requestIDs.get(request);};
      page.on('request',request=>trace('REQUEST',{profile:name,id:rid(request),url:request.url(),method:request.method()}));
      page.on('requestfinished',request=>trace('REQUEST-FINISHED',{profile:name,id:rid(request),url:request.url(),timing:request.timing()}));
      const activate = selector => name === 'phone' ? page.locator(selector).tap() : page.locator(selector).click();
      page.on('pageerror', error => errors.page.push({profile: name, message: String(error)}));
      page.on('console', message => { if (message.type() === 'error') errors.console.push({profile: name, message: message.text()});
        else if (message.type() === 'warning') warnings.push({profile: name, message: message.text()}); });
      page.on('requestfailed', request => {const row={profile:name,id:rid(request),url:request.url(),failure:request.failure(),timing:request.timing()};trace('REQUEST-FAILED',row);errors.requests.push(row);});
      page.on('response', response => {
        trace('RESPONSE-HEADERS',{profile:name,id:rid(response.request()),url:response.url(),status:response.status(),mime:response.headers()['content-type'],length:response.headers()['content-length']});
        if (response.status() >= 400) errors.http.push({profile: name, url: response.url(), status: response.status()});
        if (response.url().startsWith(base + '/')) responseReads.push((async () => {
          trace('BODY-READ-BEGIN',{profile:name,id:rid(response.request()),url:response.url()});
          const raw = await response.body();trace('BODY-READ-SUCCESS',{profile:name,id:rid(response.request()),url:response.url(),bytes:raw.length,sha256:digest(raw)}); responses.push({profile: name, path: new URL(response.url()).pathname,
            status: response.status(), bytes: raw.length, sha256: digest(raw)});
        })().catch(error => {const row={profile:name,id:rid(response.request()),url:response.url(),message:String(error)};trace('BODY-READ-FAILURE',row);errors.http.push(row);}));
      });
      phase=name+'-native-near';trace('NAVIGATION-BEGIN',{profile:name});
      await page.goto(base + '/walk/transport/farm-box-master/', {waitUntil: 'load'});trace('NAVIGATION-LOAD',{profile:name});
      async function ready(detail) {
        await page.waitForFunction(wanted => window.farmBoxState?.loaded === true && window.farmBoxState.detail === wanted
          && window.farmBoxRenderReceipt?.detail === wanted && document.querySelector('#status').textContent === 'Wagon ready', detail, {timeout: 180000});
        await page.evaluate(async () => { for (let n = 0; n < 3; n++) await new Promise(requestAnimationFrame); });
        const receipt = await page.evaluate(() => ({state: window.farmBoxState, render: window.farmBoxRenderReceipt,
          canvas: {width: document.querySelector('#view').width, height: document.querySelector('#view').height,
            clientWidth: document.querySelector('#view').clientWidth, clientHeight: document.querySelector('#view').clientHeight},
          pixelRatio: devicePixelRatio, coarse: matchMedia('(pointer:coarse)').matches,
          glError: document.querySelector('#view').getContext('webgl2').getError(), technical: document.querySelector('#technical-status').textContent}));
        assert.equal(receipt.glError, 0); assert.ok(receipt.render.drawCalls > 0 && receipt.render.triangles > 0);
        assert.equal(receipt.state.sourceSHA, sourceRecord.authored_files[0].sha256);
        const ratio = receipt.canvas.width / receipt.canvas.clientWidth;
        assert.equal(ratio, name === 'desktop' ? 1 : 2, 'Preserve actual native fixture DPR cap');
        assert.equal(receipt.coarse, name === 'phone');
        assert.ok(receipt.technical.startsWith(lods[detail].triangles.toLocaleString('en-US') + ' triangles'));
        trace('NATIVE-READY-FRAMES',{profile:name,detail,receipt});return receipt;
      }
      await ready('near');
      await page.locator('#steer').focus(); await page.keyboard.press('End');
      await page.locator('#travel').focus(); await page.keyboard.press('End');
      if (await page.locator('#raised').isChecked()) await activate('#raised');
      const moving = (await ready('near')).state;
      assert.equal(moving.steer, 8); assert.equal(moving.travel, 2); assert.equal(moving.raised, false);
      const p = JSON.parse(fs.readFileSync(path.join(fixture, 'farm-box.json'))).parameters;
      const k = Math.tan(8 * Math.PI / 180) / (p.axle_stations_z_m.front - p.axle_stations_z_m.rear);
      const expected = ['rear_left', 'rear_right', 'front_left', 'front_right'].map(label => {
        const [end, side] = label.split('_'), x = (side === 'left' ? 1 : -1) * p.wheel_center_track_m / 2;
        return 2 * (end === 'rear' ? 1 - k * x : 1 / Math.cos(8 * Math.PI / 180) - k * x) / p.wheel_radius_m[end];
      });
      moving.wheelAngles.forEach((angle, i) => assert.ok(Math.abs(angle - expected[i]) < 1e-10));
      await activate('#reset'); await ready('near');
      await activate('#play'); await page.waitForFunction(() => window.farmBoxState.travel > 0.02);
      await activate('#play'); const rolling = (await ready('near')).state; assert.ok(rolling.travel > 0);
      await activate('#reset'); await ready('near');
      await page.locator('#finish').selectOption('warm'); assert.equal((await ready('near')).render.finish, 'warm');
      await page.locator('#finish').selectOption('source');
      const views = [];
      async function capture(label, detail) {
        const receipt = await ready(detail); views.push({label, ...receipt});
        await page.locator('#view').screenshot({path: path.join(out, `${name}-${label}-CANVAS.png`)});
        if (label === 'near-quarter') await page.screenshot({path: path.join(out, `${name}-native-UI.png`)});
      }
      await activate('[data-view="quarter"]'); await capture('near-quarter', 'near');
      await activate('[data-view="side"]'); await capture('near-side', 'near');
      if (name === 'desktop') {
        await activate('[data-view="quarter"]');
        const fullDistance = (await ready('near')).render.cameraDistance;
        await page.locator('#view').hover(); await page.mouse.wheel(0, -240);
        assert.ok((await ready('near')).render.cameraDistance < fullDistance, 'Actual native wheel zoom');
        await capture('near-close', 'near');
      } else {
        // The current fixture has wheel zoom but no pinch/buttons for touch zoom.
        // Observe its real front-view button and retain that limitation, rather
        // than pretending a mouse wheel is an implemented phone zoom gesture.
        await activate('[data-view="front"]'); await capture('near-front', 'near');
      }
      phase=name+'-switch-mid';trace('LOD-SWITCH-BEGIN',{profile:name,detail:'mid'});
      await page.locator('#detail').selectOption('mid'); const middle = await ready('mid');trace('LOD-SWITCH-READY',{profile:name,detail:'mid'});
      phase=name+'-switch-far';trace('LOD-SWITCH-BEGIN',{profile:name,detail:'far'});
      await page.locator('#detail').selectOption('far'); await ready('far');trace('LOD-SWITCH-READY',{profile:name,detail:'far'});
      await activate('[data-view="side"]'); await capture('far-side', 'far');
      assert.ok(views.at(-1).render.rearWheelPixels <= 24.000001, 'Native far fit at no more than 24 wheel pixels');
      const cdp = await currentContext.newCDPSession(page), heap = await cdp.send('Runtime.getHeapUsage'); await cdp.detach();
      phase=name+'-body-read-join';trace('BODY-READ-JOIN-BEGIN',{profile:name});
      await Promise.all(responseReads);trace('BODY-READ-JOIN-END',{profile:name});
      const final = await ready('far'); // Recheck real GL/state after the last actual screenshot.
      profiles.push({profile, actualControls: {moving, rolling}, middle, views, final, heap,
        range_input_method: 'Native keyboard End accessibility controls, with native coarse/touch profile unchanged',
        phone_close_zoom: name === 'phone' ? 'UNSUPPORTED in current fixture: front view observed instead; no mouse-wheel substitution' : null,
        scope: 'Native portable fixture Near/Middle/Far; no world Full/Balanced/Light tier or town adoption claim'});
      save('DIAGNOSTIC-PARTIAL-PROFILES.json',profiles);trace('PROFILE-SAVED-BEFORE-NETWORK-ASSERTIONS',{profile:name});
      for (const [level, record] of Object.entries(lods)) assert.ok(responses.some(row => row.profile === name
        && row.path.endsWith('/' + record.file) && row.bytes === record.bytes && row.sha256 === record.sha256), 'Actual exact native LOD response ' + level);
      phase=name+'-normal-context-close';trace('CONTEXT-CLOSE-BEGIN',{profile:name});await currentContext.close();currentContext=null;trace('CONTEXT-CLOSE-END',{profile:name});
    }
  } catch (error) { trace('INTEGRITY-FAILURE',{message:String(error),stack:error.stack});errors.integrity.push({message: String(error), stack: error.stack}); }
  finally {
    phase='finally-context-close';trace('FINALLY-CONTEXT-CLOSE-BEGIN');
    if (currentContext) try { await currentContext.close();trace('FINALLY-CONTEXT-CLOSE-END'); } catch (error) { errors.closure.push({kind: 'context', message: String(error)}); }
    phase='finally-browser-close';trace('BROWSER-CLOSE-BEGIN');
    if (browser) try { await browser.close();trace('BROWSER-CLOSE-END'); } catch (error) { errors.closure.push({kind: 'browser', message: String(error)}); }
    if (server) try { await closeServer(server); } catch (error) { errors.closure.push({kind: 'server', message: String(error)}); }
    try { const after = snapshot(); assert.deepEqual(after, before); save('AFTER.json', after); }
    catch (error) { errors.integrity.push({kind: 'after-guards', message: String(error), stack: error.stack}); }
    const passed = profiles.length === (profileSelection==='both'?2:1) && Object.values(errors).every(rows => rows.length === 0);
    phase='diagnostic-closed';trace('DIAGNOSTIC-CLOSED',{passed,error_counts:Object.fromEntries(Object.entries(errors).map(([k,v])=>[k,v.length]))});
    save('RESULT.json', {status: passed ? 'DIAGNOSTIC_NATIVE_NETWORK_OBSERVATION_COMPLETE_NO_ACCEPTANCE' : 'NONPASS_DIAGNOSTIC_NATIVE_NETWORK_OBSERVATION',profile_selection:profileSelection,
      profiles, responses, warnings, errors, photographic_acceptance: false, town_master_adoption: false,
      personal_image_review: 'REQUIRED', world_renderer_smoke_coverage: 'NOT PROVIDED'});
    console.log(JSON.stringify({passed, profiles: profiles.length, errors: Object.fromEntries(Object.entries(errors).map(([key, rows]) => [key, rows.length])), warnings: warnings.length}));
    process.exitCode = passed ? 0 : 1;
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
