/** One bounded current Sauganash ordinary-street stopping-rule investigation. No source camera, geometry, FOV or scene override. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire('/workspace/shared/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const plan = JSON.parse(fs.readFileSync(process.env.SAUG_PROBE_PLAN));
const out = process.env.SAUG_PROBE_OUT, viewport = process.env.SAUG_PROBE_VIEWPORT;
const leg = process.env.SAUG_PROBE_LEG; assert.equal(leg, 'body');
assert(['desktop', 'mobile'].includes(viewport)); assert(out); fs.mkdirSync(out);
const mobile = viewport === 'mobile', root = plan.site_parent;
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const save = (name, value) => fs.writeFileSync(path.join(out, name), JSON.stringify(value, null, 2) + '\n');
let tearingDown=false; const intentionalCloseAborts=[]; const errors = [], network = [], cancelled = [], consoleErrors = [], serverErrors = [];
const guard = () => { for (const [name, binding] of Object.entries(plan.input_bindings)) assert.equal(sha(fs.readFileSync(name)), binding.sha256, name); };
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.glb': 'model/gltf-binary', '.ktx2': 'image/ktx2', '.ico': 'image/x-icon', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  try {
    let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
    if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404).end(); return; }
    res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    fs.createReadStream(file).on('error', e => { serverErrors.push(e.message); res.destroy(e); }).pipe(res);
  } catch (e) { serverErrors.push(e.message); res.writeHead(500).end(); }
});
let browser, context, page, outcome = null, fortExterior = null, fortArrival = null, visibleImage = null, screenshotBinding = null, failure = null;
const started = performance.now();
try {
  guard();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const proxyUrl = process.env.HTTPS_PROXY ?? process.env.HTTP_PROXY;
  const proxy = proxyUrl ? (() => { const p = new URL(proxyUrl); return { server: p.origin, bypass: '127.0.0.1,localhost', username: decodeURIComponent(p.username) || undefined, password: decodeURIComponent(p.password) || undefined }; })() : undefined;
  process.env.PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK = '1';
  browser = await chromium.launch({ executablePath: '/usr/bin/chromium', proxy, args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader', '--disk-cache-size=2097152', '--media-cache-size=1048576'] });
  context = await browser.newContext({ viewport: { width: mobile ? 390 : 1280, height: mobile ? 780 : 800 }, hasTouch: mobile, isMobile: false, deviceScaleFactor: mobile ? 2 : 1 });
  page = await context.newPage(); page.setDefaultTimeout(90000);
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('requestfailed', r => (tearingDown && r.failure()?.errorText === 'net::ERR_ABORTED' ? intentionalCloseAborts : network).push({url:r.url(),failure:r.failure()}));
  page.on('response', r => { if (r.status() >= 400) network.push({ url: r.url(), status: r.status() }); });
  await context.addInitScript(() => { localStorage.setItem('chicago4d.researcher', 'on'); localStorage.setItem('chicago4d.settings', JSON.stringify({ detail: 'full' })); });
  assert.equal((await page.goto(`http://127.0.0.1:${server.address().port}/4d/walk/index.html?year=1835`)).status(), 200);
  await page.waitForFunction(() => window.__chicago4d?.ready === true, null, { timeout: 240000, polling: 1000 });
  await page.evaluate(async () => {
    const a = window.__chicago4d, end = Date.now() + 90000;
    while (a.welcome?.state !== 'world' && Date.now() < end) {
      if (a.welcome?.state === 'welcome') a.welcome.enter('spawn');
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    if (a.welcome?.state !== 'world') throw Error('Welcome did not enter world');
    document.exitPointerLock?.(); document.getElementById('control-help-gotit')?.click();
    a.setAnimationHold(true); a.popup.close(); a.navigator.dock();
  });
  const baseline = await page.evaluate(() => { const a = window.__chicago4d; return { frame: a.renderer.info.render.frame, ready: a.ready, welcome: a.welcome.state, visible: document.visibilityState, contextLost: a.renderer.getContext().isContextLost(), detail: a.detail }; });
  save('WORLD-SETTLE.json', { status: 'WAITING', baseline, native_counter_advances_required: 3, bound_ms: 180000 });
  assert(baseline.ready && baseline.welcome === 'world' && baseline.visible === 'visible' && !baseline.contextLost && Number.isSafeInteger(baseline.frame));
  await page.waitForFunction(start => {
    const a = window.__chicago4d;
    if (a.renderer.getContext().isContextLost()) throw Error('Native WebGL context lost');
    if (!a.ready || a.welcome.state !== 'world' || document.visibilityState !== 'visible') throw Error('World readiness changed');
    return Number.isSafeInteger(a.renderer.info.render.frame) && a.renderer.info.render.frame >= start + 3;
  }, baseline.frame, { timeout: 180000, polling: 500 });
  const settled = await page.evaluate(() => window.__chicago4d.renderer.info.render.frame);
  assert(settled >= baseline.frame + 3);
  save('WORLD-SETTLE.json', { status: 'PASS', baseline, settled, native_counter_advances_required: 3, bound_ms: 180000, scope: 'Renderer counter only; no FPS or GPU-readback timing claim' });
  const feet = await page.evaluate(() => {
    const a=window.__chicago4d,id='sauganash_hotel';
    a.popup.close();a.navigator.dock();a.travel.stop('Sauganash ordinary-street inspection');a.setFly(false);a.walker.setFlying(false);a.confidence.resetGrades();a.setConfidenceView(false);
    const framing=a.framing(id,{card:false,mode:'walk'});if(!framing)throw Error('No real native ordinary-street framing');
    if(!a.frame(id,{card:false,mode:'walk'}))throw Error('Native walking frame failed');
    const st={...a.walker.state},cls=a.router.classAt(st.e,st.n),blocked=a.router.blockedAt(st.e,st.n),surface=a.walker.surfaceAt(st.e,st.n);
    return {framing,state:st,class:cls,blocked,surface,height_above_real_surface:st.eyeY-surface,camera:a.camera.position.toArray(),fov:a.camera.fov,aspect:a.camera.aspect,detail:a.detail,missing:a.buildings.missing?.has?.(id),ready:a.ready,contextLost:a.renderer.getContext().isContextLost()};
  });
  save('NATIVE-STREET-APPROACH.json',feet);
  assert(feet.framing.front?.street,'Actual framing carries an authored street frontage, not a courtyard/radial fallback');
  assert.equal(feet.class,'sidewalk');assert.equal(feet.blocked,false);assert.equal(feet.state.flying,false);assert(feet.height_above_real_surface>=1.45&&feet.height_above_real_surface<=1.9,'Native human-eye range above actual walker surface');assert.equal(feet.missing,false);assert.equal(feet.detail,'full');
  const captures=[];
  for(const kind of ['street-whole-hotel','street-look-at-stacks']){
    const row=await page.evaluate(async({kind,feet,stacks})=>{
      const a=window.__chicago4d,id='sauganash_hotel',mat=a.buildings.matrixOf(id),inv=mat.clone().invert();
      const transform=(p,m)=>{const x=m.elements??m,w=x[3]*p[0]+x[7]*p[1]+x[11]*p[2]+x[15];return[(x[0]*p[0]+x[4]*p[1]+x[8]*p[2]+x[12])/w,(x[1]*p[0]+x[5]*p[1]+x[9]*p[2]+x[13])/w,(x[2]*p[0]+x[6]*p[1]+x[10]*p[2]+x[14])/w];};
      if(kind==='street-look-at-stacks'){
        const points=stacks.map(b=>transform([(b.min[0]+b.max[0])/2,b.max[1]-.12,(b.min[2]+b.max[2])/2],mat));
        const target=points[0].map((v,i)=>(v+points[1][i])/2),st=a.walker.state,de=target[0]-st.e,dn=-target[2]-st.n;
        a.walker.teleport({local_e:st.e,local_n:st.n,yaw_deg:(Math.atan2(de,dn)*180/Math.PI+360)%360,pitch_deg:Math.atan2(target[1]-st.eyeY,Math.hypot(de,dn))*180/Math.PI});
      }
      a.step();const before=a.renderer.info.render.frame,pending=a.capture(12);a.step();const signature=await pending;
      const centerHit=await a.buildings.pickAtAsync({x:0,y:0},a.camera),probes=[];
      for(const b of stacks){
        const local=[(b.min[0]+b.max[0])/2,b.max[1]-.12,(b.min[2]+b.max[2])/2],world=transform(local,mat),ndc=a.project(world[0],-world[2],world[1]);
        const onscreen=ndc.z>=-1&&ndc.z<=1&&Math.abs(ndc.x)<=1&&Math.abs(ndc.y)<=1;
        const hit=onscreen?await a.buildings.pickAtAsync({x:ndc.x,y:ndc.y},a.camera):null;
        const localHit=hit?.point?hit.point.clone().applyMatrix4(inv).toArray():null;
        const inside=hit?.id===id&&localHit&&localHit.every((v,i)=>v>=b.min[i]-.02&&v<=b.max[i]+.02);
        probes.push({box:b,local_sample:local,world,ndc,onscreen,hit:hit?{id:hit.id,point:hit.point?.toArray(),local_point:localHit,distance:hit.distance}:null,native_gpu_hit_inside_stack:!!inside});
      }
      const st={...a.walker.state},surface=a.walker.surfaceAt(st.e,st.n);
      return {kind,before,after:a.renderer.info.render.frame,signature,state:st,camera:a.camera.position.toArray(),height_above_real_surface:st.eyeY-surface,class:a.router.classAt(st.e,st.n),blocked:a.router.blockedAt(st.e,st.n),centerHit:centerHit?{id:centerHit.id,point:centerHit.point?.toArray(),distance:centerHit.distance}:null,stack_probes:probes,ready:a.ready,contextLost:a.renderer.getContext().isContextLost(),fov:a.camera.fov,scope:'Actual normal app walking eye on native router walk frontage; looking upward is a native walker turn, no flight/FOV/source-camera fit or geometry override.'};
    },{kind,feet,stacks:plan.stack_boxes});
    assert.equal(row.state.flying,false);assert.equal(row.class,'sidewalk');assert.equal(row.blocked,false);assert(row.height_above_real_surface>=1.45&&row.height_above_real_surface<=1.9);assert.equal(row.fov,feet.fov);assert(row.ready&&!row.contextLost&&row.after>row.before&&row.signature.litFraction>.05);
    await page.waitForFunction(frame=>window.__chicago4d.renderer.info.render.frame>=frame+3,row.after,{timeout:180000,polling:500});
    row.settled_frame=await page.evaluate(()=>window.__chicago4d.renderer.info.render.frame);
    const file=path.join(out,kind+'.jpg');await page.screenshot({path:file,type:'jpeg',quality:92});row.screenshot={path:file,sha256:sha(fs.readFileSync(file)),bytes:fs.statSync(file).size};save(kind+'.json',row);captures.push(row);
  }
  for(const list of [errors,network,consoleErrors,serverErrors])assert.equal(list.length,0,JSON.stringify(list));guard();
  outcome={status:'ACTUAL_STREET_REVIEW_CAPTURED_NOT_A_MATCH_VERDICT',viewport,head:plan.expected_head,phase:plan.expected_phase,target_date:plan.expected_target,feet,captures,errors,network,consoleErrors,serverErrors,wall_ms:performance.now()-started,scope:'One ordinary street approach/two native look directions. Direct visual ruling is separate; no generic Stage3/source camera/native bake/completion claim.'};save('RESULT.json',outcome);
} catch(e) {
  failure={message:e.message,stack:e.stack};
  if(page)try{await page.screenshot({path:path.join(out,'FAIL.jpg'),type:'jpeg',quality:90});}catch(x){failure.screenshot_error=x.message;}
  save('FAILURE.json',{failure,errors,network,consoleErrors,serverErrors,intentionalCloseAborts});
} finally {
  const preTeardown={errors:[...errors],network:[...network],consoleErrors:[...consoleErrors],serverErrors:[...serverErrors]};save('PRE-TEARDOWN-ERRORS.json',preTeardown);tearingDown=true;
  if(context)try{await context.close();}catch(e){failure??={message:e.message};}
  if(browser)try{await browser.close();}catch(e){failure??={message:e.message};}
  if(server.listening)await new Promise(resolve=>server.close(resolve));
  save('CLOSURE.json',{failure,preTeardown,intentionalCloseAborts,errors,network,consoleErrors,serverErrors,no_retry:true});
}
if(failure)process.exitCode=1;
