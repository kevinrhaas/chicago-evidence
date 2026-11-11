// Published Prairie household call, paired conversation, appearance and Interact UI.
// Run from chicago/4d after tools/publish.sh. NODE_PATH may supply Playwright.
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const { chromium } = createRequire(import.meta.url)('playwright');
const root = path.resolve(process.env.PROBE_ROOT || '../../site/4d');
console.log('published build', JSON.parse(fs.readFileSync(path.join(root, 'build.json'), 'utf8')));
const proofLabel = 'younger-residents';
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm', '.jpg': 'image/jpeg', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  let file = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!file.startsWith(root + '/') || !fs.existsSync(file)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise((resolve) => server.listen(4204, '127.0.0.1', resolve));
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE || undefined, args: ['--enable-unsafe-swiftshader'] });
try {
  for (const viewport of [{ width: 390, height: 780 }, { width: 1280, height: 800 }]) {
    if (process.env.PROBE_VIEWPORT && Number(process.env.PROBE_VIEWPORT) !== viewport.width) continue;
    const page = await browser.newPage({ viewport, hasTouch: viewport.width < 600 });
    await page.addInitScript(id => { window.__probePerson=id; }, process.env.PROBE_PERSON || 'pa1904_kimball_william_w');
    await page.addInitScript(age => { window.__probeExpectedAge=age; }, process.env.PROBE_EXPECT_AGE ? Number(process.env.PROBE_EXPECT_AGE) : null);
    await page.addInitScript(asset => { window.__probeExpectedAsset=asset; }, process.env.PROBE_EXPECT_ASSET || null);
    const errors = [];
    page.on('console', m => { if (m.text().startsWith('pair ')) console.log(m.text()); });
    page.on('pageerror', (e) => { errors.push(e.message); console.log('PAGE ERROR', e.message); });
    page.on('response', r => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url()); });
    await page.addInitScript((quality) => localStorage.setItem('chicago4d.settings', JSON.stringify({ timeOfDay: '23:00', ...(quality ? { quality } : {}) })), process.env.PROBE_QUALITY ? Number(process.env.PROBE_QUALITY) : null);
    await page.goto('http://127.0.0.1:4204/1904/', { waitUntil: 'domcontentloaded', timeout: 180000 });
    await page.waitForFunction(() => window.__chicago4d?.ready || window.__chicago4d?.error, null, { timeout: 240000, polling: 1000 }).catch(async (error) => {
      console.log('BOOT FAILURE', await page.evaluate(() => ({ ready: window.__chicago4d?.ready, error: window.__chicago4d?.error, text: document.body.innerText.slice(-1800) })));
      throw error;
    });
    console.log('ready', viewport.width);
    // As in the canonical smoke's holdDraws helper, let the arrival UI finish
    // without repeated software-GPU draws. Restore the draw for the screenshot.
    await page.evaluate(() => {
      const r = window.__chicago4d.renderer;
      window.__probeDraw = r.render;
      r.render = (scene, camera) => camera?.updateMatrixWorld?.();
    });
    // Ready precedes the arrival card's landing, as in the canonical smoke.
    await page.waitForFunction(() => ['welcome', 'world'].includes(window.__chicago4d.welcome.state), null, { timeout: 90000, polling: 100 }).catch(async error => {
      console.log('ARRIVAL FAILURE', await page.evaluate(() => ({ state: window.__chicago4d.welcome.state, error: window.__chicago4d.error, text: document.body.innerText.slice(-2500) })));
      throw error;
    });
    await page.evaluate(() => { if (window.__chicago4d.welcome.state === 'welcome') document.getElementById('home-roam').click(); });
    await page.waitForFunction(() => window.__chicago4d.welcome.state === 'world', null, { timeout: 90000, polling: 100 });

    const cases = process.env.PROBE_PERSON ? process.env.PROBE_PERSON.split(',') : ['pa1904_walker_james_r_c1900_arthur_m_walker', 'pa1904_shortall_john_l_c1900_margaret_shortall', 'pa1904_glessner_john', 'pa1904_longini_a_c1900_marcel_longini', 'pa1904_cunningham_elizabeth_s'];
    await page.evaluate(() => {
      const a = window.__chicago4d;
      a.navigator.dock(); a.renderer.setAnimationLoop(null); a.renderer.render = window.__probeDraw;
      const step = seconds => { for (let i=0; i<seconds*20; i++) { a.interactions.update(.05); a.humans.update(.05,a.camera,a.walker.state,.05); a.duties.update(.05); a.days.update(.05); a.houseDoors?.update(.05); a.spacing?.update(.05); } };
      const until = (fn, seconds=180) => { for(let i=0;i<seconds*20&&!fn();i++)step(.05); };
      window.__proof={step,until};step(1);
    });
    for (const person of cases) {
      const entry = await page.evaluate(async person => {
        const a=window.__chicago4d, {step,until}=window.__proof;
        const roster=await fetch('../data/humans/inside_1904.json').then(r=>r.json());
        const entry=roster.people.find(p=>p.person===person); const door=a.days.doors.find(t=>t.door.id===entry.door);
        a.walker.teleport({local_e:door.at[0]+4,local_n:door.at[1]+3,yaw_deg:230});
        const call=a.days.ask(person);if(!call.ok)throw Error(JSON.stringify(call));
        const child=a.days.people.find(p=>p.actor.personId===person);
        window.__proof.child=child;window.__proof.entry=entry;
        if(entry.supervised && (!child.social?.supervised||child.social.members.length!==2))throw Error('No caregiver on door call');
        const pair=child.social?.members??[child];
        until(()=>pair.every(p=>!p.actor.indoors&&!p.actor.path&&!p.passing));step(1);
        if(pair.some(p=>p.actor.indoors||p.actor.disposed))throw Error('Door call did not complete');
        return entry;
      }, person);
      console.log('called',viewport.width,person);
      await page.waitForFunction(()=>{const p=window.__proof.child;return (p.social?.members??[p]).every(m=>m.actor.body);},null,{timeout:150000});
      const result=await page.evaluate(()=>{
        const a=window.__chicago4d,{step,until,child,entry}=window.__proof;
        const pair=child.social?.members??[child];
        until(()=>pair.every(p=>!p.actor.indoors&&!p.actor.path&&!p.passing));step(1);
        if(child.actor.variation.age!==entry.age_1904)throw Error('Wrong age '+child.actor.variation.age);
        if(child.actor.instance.appearance.asset_id!==entry.asset_id)throw Error('Wrong child body');
        if(!child.actor.root.visible)throw Error('Child not visible');
        const walk=a.days.outdoorActivities(child.id).find(x=>x.span.activity==='walk');
        if(!a.days.request(child.id,walk.id).ok)throw Error('Walk refused');
        until(()=>pair.every(p=>p.mode==='out'));
        const at=pair.map(p=>[p.actor.e,p.actor.n]), moved=pair.map(()=>false);let maxGap=0;
        for(let i=0;i<280;i++){step(.05);if(pair.length===2)maxGap=Math.max(maxGap,Math.hypot(pair[0].actor.e-pair[1].actor.e,pair[0].actor.n-pair[1].actor.n));pair.forEach((p,j)=>{if(Math.hypot(p.actor.e-at[j][0],p.actor.n-at[j][1])>.2)moved[j]=true;});}
        if(moved.some(x=>!x))throw Error('Outing did not move both participants');
        if(entry.supervised && maxGap>2.5)throw Error('Caregiver did not stay near: '+JSON.stringify(pair.map(p=>({id:p.id,e:p.actor.e,n:p.actor.n,heading:p.actor.heading,path:p.actor.path,mode:p.mode,bases:p.social?.bases}))));
        const release=a.days.attend(child.id);if(!release)throw Error('Cannot hold walking child');
        if(entry.supervised&&!pair.every(p=>p.social===child.social))throw Error('Menu separated caregiver');
        step(2);release();
        a.navigator.dock();
        const clearView=entry.person==='pa1904_shortall_john_l_c1900_margaret_shortall'||entry.asset_id.startsWith('teen_');
        a.walker.teleport({local_e:child.actor.e+3,local_n:child.actor.n+(clearView?-3:3),yaw_deg:clearView?315:225});
        // Settle the full scene's camera-dependent LOD/reach updates after teleport.
        const draw=a.renderer.render;a.renderer.render=(scene,camera)=>camera?.updateMatrixWorld?.();
        a.step();a.step();a.renderer.render=draw;
        a.world.setSun({date:'1904-07-01',time:'10:00'});a.world.follow(a.camera.position);
        a.renderer.render(a.scene3d,a.camera);a.renderer.render(a.scene3d,a.camera);
        const stats=a.stats();
        // These are views of other Prairie households, outside Glessner's close
        // inspection frames. T-3285/T-3286 already declare their Full district
        // allowance in farBudget. Light keeps its ordinary budget; no cap moves.
        const frameBudget=entry.home!=='glessner_house' && stats.farBudget ? stats.farBudget : stats.budget;
        if(stats.drawCalls>frameBudget.drawCalls||stats.triangles>frameBudget.triangles){
          const roots=a.humans.actors.map(p=>({root:p.root,visible:p.root.visible}));
          for(const {root} of roots)root.visible=false;
          a.renderer.render(a.scene3d,a.camera);a.renderer.render(a.scene3d,a.camera);const withoutPeople=a.stats();
          for(const {root,visible} of roots)root.visible=visible;
          throw Error('Render budget exceeded: '+JSON.stringify({stats,withoutPeople,camera:{e:a.walker.state.e,n:a.walker.state.n},glessner:a.structurePosition('glessner_house')}));
        }
        if(a.problems.length)throw Error('App problems: '+JSON.stringify(a.problems));
        return {person:entry.person,age:child.actor.variation.age,asset:entry.asset_id,supervised:!!entry.supervised,company:pair.map(p=>p.actor.personId),height:child.actor.variation.height,maxGap,frameBudget,budgetScope:stats.farBudget&&entry.home!=='glessner_house'?'existing Full district allowance':'ordinary scene allowance',stats};
      });
      console.log('case',viewport.width,JSON.stringify(result));
      await page.screenshot({path:`/workspace/prairie-younger/${person}-${viewport.width}.png`,timeout:120000});
      await page.evaluate(()=>{
        const a=window.__chicago4d,{step,until,child,entry}=window.__proof;
        a.world.setSun({date:'1904-07-01',time:'23:00'});
        const chat=a.days.outdoorActivities(child.id).find(x=>x.span.activity==='talk');
        if(!a.days.request(child.id,chat.id).ok)throw Error('Chat refused');
        window.__proof.pair=child.social.members;
        until(()=>window.__proof.pair.every(p=>p.mode==='out'&&!p.actor.indoors&&!p.passing));step(1);
      });
      await page.waitForFunction(()=>window.__proof.pair.every(p=>p.actor.body),null,{timeout:150000});
      await page.evaluate(()=>{
        const a=window.__chicago4d,{step,until,child,pair}=window.__proof;
        until(()=>pair.every(p=>p.mode==='out'&&!p.actor.indoors&&!p.passing));step(2);
        if(pair.some(p=>!p.social)||Math.hypot(pair[0].actor.e-pair[1].actor.e,pair[0].actor.n-pair[1].actor.n)>2.5)throw Error('Chat never met');
        const nearest=a.days.nearestEntrance(child.id);
        if(!nearest||!a.days.request(child.id,null,{inside:'nearest'}).ok)throw Error('Go inside refused');
        until(()=>pair.every(p=>p.actor.indoors||p.actor.disposed));
        if(pair.some(p=>!p.actor.indoors))throw Error('Both did not go inside');
        for(const p of pair)if(!p.actor.disposed){if(!a.days.request(p.id,null,{inside:'home'}).ok)throw Error('Go home refused');}
        until(()=>pair.every(p=>p.actor.disposed||!p.entry));
        if(!child.actor.disposed)throw Error('Child mesh not retired');
      });
    }
    const infants = await page.evaluate(async()=> (await fetch('../data/humans/inside_1904.json').then(r=>r.json())).care);
    const care=[];
    for (const infant of infants) {
      const status=await page.evaluate(infant=>{
        const a=window.__chicago4d, before=a.days.insideOnly.out;
        const door=a.days.doors.find(t=>t.door.id===infant.door);
        let action;
        for(let i=0;i<10;i++){
          const actions=door.actions.shut; action=actions.find(x=>x.id===`ask:${infant.person}`);
          if(action)break;
          const others=actions.find(x=>x.id==='others'); if(!others)break;
          others.steps[0].run(0);
        }
        if(!action?.label.startsWith('Ask after '))throw Error('No infant door action');
        action.steps[0].run(1);
        if(a.days.insideOnly.out!==before)throw Error('Infant spawned an actor');
        return a.days.careStatus(infant.person);
      },infant);
      await page.waitForFunction(text=>document.body.innerText.includes(text),status.text,{timeout:30000});
      care.push(status);
    }
    await page.waitForFunction(()=>document.body.innerText.includes('infants remain in household care'),null,{timeout:30000});
    await page.locator('.insp-person-story .insp-summary').filter({hasText:'infants remain in household care'}).scrollIntoViewIfNeeded();
    await page.screenshot({path:`/workspace/prairie-younger/infant-care-${viewport.width}.png`,timeout:120000});
    const stats=await page.evaluate(()=>({stats:window.__chicago4d.stats(),problems:window.__chicago4d.problems}));
    assert.deepEqual(errors,[]);assert.deepEqual(stats.problems,[]);assert.equal(stats.stats.withinBudget,true);console.log(JSON.stringify({viewport,care,stats,status:'PASS',pageErrors:errors}));
    await page.close();
  }
} finally { await browser.close(); server.close(); }
