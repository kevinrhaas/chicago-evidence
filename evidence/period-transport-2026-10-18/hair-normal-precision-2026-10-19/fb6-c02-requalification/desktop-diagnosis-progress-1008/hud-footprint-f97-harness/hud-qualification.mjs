// SPDX-License-Identifier: GPL-3.0-or-later
// Outside-only actual page measurement derived from unchanged project T2628 union.
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
export async function measureHudFootprint({timeoutMs=60000}={}) {
      // dock() changes the detent synchronously; its visible width/height still transitions.
      // Wait for the actual dock contract and completed CSS motion, never hide/exclude the device.
      const nav = document.getElementById('navigator'), deadline = performance.now() + timeoutMs;
      let navigatorDock, initialNavigatorDock;
      do {
        const b = nav?.getBoundingClientRect(); // Flush style before querying CSS transitions.
        const phone = innerWidth <= 620;
        const animations = nav?.getAnimations?.() ?? [];
        navigatorDock = { detent: window.__chicago4d.navigator?.detent ?? null,
          level: window.__chicago4d.navigator?.level ?? null,
          box: b ? { x: b.x, y: b.y, width: b.width, height: b.height } : null,
          running: animations.filter(a => a.playState === 'running' || a.pending).map(a => ({ state: a.playState, pending: a.pending, property: a.transitionProperty ?? null })) };
        initialNavigatorDock ??= structuredClone(navigatorDock);
        navigatorDock.ready = !!b && navigatorDock.level === 0 && navigatorDock.detent === (phone ? 'dock' : 'rail')
          && navigatorDock.running.length === 0
          && (phone ? Math.abs(b.width - 136) <= 1 && Math.abs(b.height - 64) <= 1 : Math.abs(b.width - 58) <= 1);
        if (navigatorDock.ready || performance.now() >= deadline) break;
        await new Promise(resolve => setTimeout(resolve, 100));
      } while (true);
      // The hint fades on a timer that only runs between frames, which on a starved runner take
      // seconds: wait for it up to 30 s. A hint still up after that is a passing prompt, not the
      // HUD's steady state, so it is left out like the look tag and reported.
      for (let i = 0; i < 200; i++) {
        if (!document.getElementById('hint')?.classList.contains('on')) break;
        await new Promise((r) => setTimeout(r, 150));
      }
      const hintUp = !!document.getElementById('hint')?.classList.contains('on');
      const W = innerWidth, H = innerHeight, cell = 2;
      const cols = Math.ceil(W / cell), rows = Math.ceil(H / cell);
      const grid = new Uint8Array(cols * rows);
      const clear = (c) => !c || c === 'transparent' || /rgba\([^)]*,\s*0(\.0+)?\)$/.test(c);
      const painted = (el, cs) => {
        if (/^(canvas|svg|img)$/i.test(el.tagName)) return true;
        if (!clear(cs.backgroundColor) || cs.backgroundImage !== 'none') return true;
        if (parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none' && !clear(cs.borderTopColor)) return true;
        return [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
      };
      const shown = (el) => {
        for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
          if (e.hidden) return false;
          const cs = getComputedStyle(e);
          if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return false;
        }
        return true;
      };
      const boxes = [];
      for (const root of [document.getElementById('hud'), document.getElementById('navigator')]) {
        if (!root) continue;
        for (const el of [root, ...root.querySelectorAll('*')]) {
          // CLICK TO ENGAGE LOOK (T-2614) is a one-time prompt, not the HUD's steady state: it
          // goes at the first click on the scene and never shows with touch controls (part 6
          // checks both). On the phone leg it can show here only because this run's earlier
          // trusted mouse clicks made pointer lock the live controls (main.js, pointerType).
          if (el.id === 'look-tag') continue;
          if (el.closest('#hint')) continue;
          // T-2741's street readout has its own off switch (#street-toggle, Settings › Show):
          // owner's ruling 2026-10-18 — keep it on by default, measure the budget without it.
          // The switch beside the compass is part of that instrument and goes with it.
          if (el.closest('#street-readout') || el.closest('#street-toggle')) continue;
          // The target tag (T-2627) is a glance, not the HUD's steady state: since T-2736 it
          // holds 3 s and fades, and whether it is up depends on where the reticle happens to
          // rest. A run measured 10.96 % at 390x844 with it up (5,923 px2) and 9.83 % without.
          // Left out like the hint and the look tag, and reported.
          if (el.closest('#target-tag')) continue;
          const r = el.getBoundingClientRect();
          if (r.width < 1 || r.height < 1 || r.right <= 0 || r.bottom <= 0 || r.left >= W || r.top >= H) continue;
          if (!painted(el, getComputedStyle(el)) || !shown(el)) continue;
          boxes.push({ id: el.id || el.className?.baseVal || el.className || el.tagName, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom });
        }
      }
      for (const b of boxes) {
        const c0 = Math.max(0, Math.floor(b.x0 / cell)), c1 = Math.min(cols, Math.ceil(b.x1 / cell));
        const r0 = Math.max(0, Math.floor(b.y0 / cell)), r1 = Math.min(rows, Math.ceil(b.y1 / cell));
        for (let y = r0; y < r1; y++) grid.fill(1, y * cols + c0, y * cols + c1);
      }
      let on = 0;
      for (const v of grid) on += v;
      const pct = (on * cell * cell) / (W * H) * 100;
      const biggest = boxes.map((b) => ({ id: String(b.id).slice(0, 40), a: Math.round((b.x1 - b.x0) * (b.y1 - b.y0)) }))
        .sort((a, b) => b.a - a.a).slice(0, 6);
      const share = (id) => {
        const e = document.getElementById(id);
        const b = e && shown(e) ? e.getBoundingClientRect() : null;
        return b ? (b.width * b.height) / (W * H) * 100 : 0;
      };
      const streetReadout = +(share('street-readout') + share('street-toggle')).toFixed(2);
      const targetTag = +share('target-tag').toFixed(2);
      return { viewport: `${W}x${H}`, pct: +pct.toFixed(2), boxes: boxes.length, biggest, streetReadout, targetTag,
        navigatorDock, initialNavigatorDock, controls: window.__chicago4d.controlBackend, lookTag: !document.getElementById('look-tag')?.hidden, hintUp };
}

export async function runHudQualification(page,{output,viewports=[{width:1280,height:800},{width:390,height:780},{width:390,height:844}]}={}) {
  if(!output)throw Error('Explicit outside output directory required');
  await mkdir(output,{recursive:true});
  const report={scope:'Actual page visible HUD union and Navigator readiness; no screenshot/production/phoneGPU claim until observed',runs:[],negatives:[],passed:false};
  const originalViewport=page.viewportSize();
  const original=await page.evaluate(()=>({app:window.__chicago4d.navigator.app,level:window.__chicago4d.navigator.level}));
  const measure=timeoutMs=>page.evaluate(measureHudFootprint,{timeoutMs});
  const plant=labels=>page.evaluate(ls=>{const row=document.querySelector('.hud-actions');if(!row)throw Error('Missing HUD actions');const box=document.createElement('span');box.id='smoke-t2628-planted';box.style.display='contents';for(const l of ls){const b=document.createElement('button');b.className='chip';b.textContent=l;box.append(b);}row.prepend(box);},labels);
  const unplant=()=>page.evaluate(()=>document.getElementById('smoke-t2628-planted')?.remove());
  try {
    for(const viewport of viewports){
      await page.setViewportSize(viewport);
      // Exact T2625 lead-in from stage13: availability polling, sequential app opens, awaited Home then dock.
      const lead=await page.evaluate(async()=>{
        const api=window.__chicago4d,n=api.navigator,device=document.getElementById('navigator');
        const inside=async(app,sel)=>{await n.select(app);for(let i=0;i<40;i++){const el=device.querySelector(sel);if(el&&el.getBoundingClientRect().width>0)return true;await new Promise(r=>setTimeout(r,100));}return false;};
        const reach={start:await inside('jaunts','#nav-seg-jaunts'),confidence:await inside('confidence','.nav-preset'),pace:await inside('move','#s-move'),theme:await inside('settings','#s-theme')};
        await n.select('home');n.dock();
        return{reach};
      });
      if(!Object.values(lead.reach).every(Boolean))throw Error('Exact stage13 lead-in app availability failed');
      // Original T2628 cleanup only; readiness helper never closes/re-docks visible UI.
      await page.evaluate(()=>{const a=window.__chicago4d;a.navigator?.dock?.();a.popup?.close?.();a.hud.dismissControlHelp?.({remember:false});});
      const baseline=await measure(60000);
      await page.screenshot({path:path.join(output,`hud-${viewport.width}x${viewport.height}-baseline.png`)});
      await plant(['Extra']);let oneMore;try{oneMore=await measure(60000);}finally{await unplant();}
      await plant(['Start / Jaunts','Confidence','▾','Walk','◐','≡','Extra']);let oldRow;try{oldRow=await measure(60000);}finally{await unplant();}
      const passed=baseline.navigatorDock.ready&&baseline.pct<=10&&baseline.boxes>0&&oneMore.pct>baseline.pct+.05&&(viewport.width>620||oldRow.pct>10);
      report.runs.push({viewport,lead,baseline,oneMore,oldRow,passed});
    }
    // Deliberately OPEN UI must not be hidden/redocked by readiness or accepted as a steady dock.
    await page.evaluate(()=>window.__chicago4d.navigator.open());
    const open=await measure(2000);
    report.negatives.push({name:'actual-open-device',expected:'ready=false; open UI still measured',measurement:open,passed:!open.navigatorDock.ready&&open.navigatorDock.level>0});
    // A real never-ending native animation (constant opacity1) leaves the device visible.
    // This is a refusal control, not a way to qualify pixels or alter the production UI.
    await page.evaluate(()=>window.__chicago4d.navigator.dock());
    const restored=await measure(60000);
    if(!restored.navigatorDock.ready)throw Error('Could not restore actual dock before animation refusal');
    await page.evaluate(()=>{window.__hudReadinessNegative=document.getElementById('navigator').animate([{opacity:1},{opacity:1}],{duration:10000,iterations:Infinity});});
    try{const running=await measure(2000);report.negatives.push({name:'nonsettling-native-animation-visible-device',measurement:running,passed:!running.navigatorDock.ready&&running.navigatorDock.running.length>0});}
    finally{await page.evaluate(()=>{window.__hudReadinessNegative?.cancel();delete window.__hudReadinessNegative;});}
    report.passed=report.runs.every(r=>r.passed)&&report.negatives.every(r=>r.passed);
    if(!report.passed)throw Error('HUD qualification criteria failed; see preserved report');
  } catch(error){report.error=String(error.stack||error);throw error;}
  finally{
    await unplant().catch(()=>{});
    await page.evaluate(async state=>{window.__hudReadinessNegative?.cancel();delete window.__hudReadinessNegative;const n=window.__chicago4d.navigator;await n.select(state.app??'home');n.setLevel(state.level??0);},original).catch(()=>{});
    if(originalViewport)await page.setViewportSize(originalViewport).catch(()=>{});
    report.restoration_requested={viewport:originalViewport,navigator:original};
    await writeFile(path.join(output,'hud-qualification.json'),JSON.stringify(report,null,2)+'\n');
  }
  return report;
}
