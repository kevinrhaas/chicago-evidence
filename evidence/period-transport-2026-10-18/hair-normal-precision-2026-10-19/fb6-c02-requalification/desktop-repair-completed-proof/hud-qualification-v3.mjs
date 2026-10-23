// SPDX-License-Identifier: GPL-3.0-or-later
// V2 measurement uses carriage_model revised-settle.patch guard/body exactly; initial snapshot and configurable test wall only.
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
export async function measureHudFootprint({timeoutMs=60000}={}) {
      // The hint fades on a timer that only runs between frames, which on a starved runner take
      // seconds: wait for it up to 30 s. A hint still up after that is a passing prompt, not the
      // HUD's steady state, so it is left out like the look tag and reported.
      for (let i = 0; i < 200; i++) {
        if (!document.getElementById('hint')?.classList.contains('on')) break;
        await new Promise((r) => setTimeout(r, 150));
      }
      const hintUp = !!document.getElementById('hint')?.classList.contains('on');
      // dock() updates its detent synchronously, while the actual box still transitions.
      // After the hint wait, require the visible final dock immediately before sampling.
      const nav = document.getElementById('navigator'), deadline = performance.now() + timeoutMs;
      const dockShown = (el) => {
        if (!el?.isConnected) return false;
        for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
          const cs = getComputedStyle(e);
          if (e.hidden || cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return false;
        }
        return true;
      };
      let navigatorDock, initialNavigatorDock;
      do {
        const b = nav?.getBoundingClientRect(); // Flush style before reading native transitions.
        const phone = innerWidth <= 620;
        const animations = nav?.getAnimations?.() ?? [];
        navigatorDock = { detent: window.__chicago4d.navigator?.detent ?? null,
          level: window.__chicago4d.navigator?.level ?? null,
          box: b ? { x: b.x, y: b.y, width: b.width, height: b.height, right: b.right, bottom: b.bottom } : null,
          visible: dockShown(nav),
          running: animations.filter(a => a.playState === 'running' || a.pending).map(a => ({ state: a.playState, pending: a.pending, property: a.transitionProperty ?? null })) };
        initialNavigatorDock ??= structuredClone(navigatorDock);
        navigatorDock.ready = !!b && navigatorDock.visible && b.height > 0
          && b.left >= 0 && b.top >= 0 && b.right <= innerWidth && b.bottom <= innerHeight
          && navigatorDock.level === 0 && navigatorDock.detent === (phone ? 'dock' : 'rail')
          && navigatorDock.running.length === 0
          && (phone ? Math.abs(b.width - 136) <= 1 && Math.abs(b.height - 64) <= 1 : Math.abs(b.width - 58) <= 1);
        if (navigatorDock.ready || performance.now() >= deadline) break;
        await new Promise(resolve => setTimeout(resolve, 100));
      } while (true);
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
  if(!output||!output.endsWith('v3'))throw Error('Fresh explicit outside output subdirectory ending v3 required');
  await mkdir(output,{recursive:false});
  const report={version:3,scope:'Actual visible HUD union; CSS viewport resize in existing context, no genuine touch/phoneGPU/production claim',runs:[],negatives:[],passed:false};
  const save=()=>writeFile(path.join(output,'hud-qualification.json'),JSON.stringify(report,null,2)+'\n');
  const originalViewport=page.viewportSize();
  const original=await page.evaluate(()=>({app:window.__chicago4d.navigator.app,level:window.__chicago4d.navigator.level}));
  const assertDrawsLive=async()=>{if(await page.evaluate(()=>!!window.__smokeHeldDraw))throw Error('HUD measurements require restored actual renderer, not held WebGL');};
  const measure=async timeoutMs=>{await assertDrawsLive();return page.evaluate(measureHudFootprint,{timeoutMs});};
  // Exact existing source smoke holdDraws helper: affects WebGL calls only; CSS/rAF remain live.
  const holdDraws=(on)=>page.evaluate((hold)=>{
    const r=window.__chicago4d.renderer;
    if(hold&&!window.__smokeHeldDraw){window.__smokeHeldDraw=r.render;r.render=()=>{};}
    else if(!hold&&window.__smokeHeldDraw){r.render=window.__smokeHeldDraw;delete window.__smokeHeldDraw;}
  },on);
  const plant=labels=>page.evaluate(ls=>{const row=document.querySelector('.hud-actions');if(!row)throw Error('Missing HUD actions');const box=document.createElement('span');box.id='smoke-t2628-planted';box.style.display='contents';for(const l of ls){const b=document.createElement('button');b.className='chip';b.textContent=l;box.append(b);}row.prepend(box);},labels);
  const unplant=()=>page.evaluate(()=>document.getElementById('smoke-t2628-planted')?.remove());
  await save();
  await assertDrawsLive(); // Refuse pre-held caller state before entering any cleanup scope.
  try {
    for(const viewport of viewports){
      const row={viewport,stage:'viewport',passed:false};report.runs.push(row);await save();
      await page.setViewportSize(viewport);
      row.stage='exact-stage13-lead-in';await save();
      row.lead=await page.evaluate(async()=>{
        const api=window.__chicago4d,n=api.navigator,device=document.getElementById('navigator');
        const inside=async(app,sel)=>{await n.select(app);for(let i=0;i<40;i++){const el=device.querySelector(sel);if(el&&el.getBoundingClientRect().width>0)return true;await new Promise(r=>setTimeout(r,100));}return false;};
        const reach={start:await inside('jaunts','#nav-seg-jaunts'),confidence:await inside('confidence','.nav-preset'),pace:await inside('move','#s-move'),theme:await inside('settings','#s-theme')};
        await n.select('home');n.dock();return{reach};
      });await save();
      if(!Object.values(row.lead.reach).every(Boolean))throw Error('Exact stage13 lead-in app availability failed');
      await page.evaluate(()=>{const a=window.__chicago4d;a.navigator?.dock?.();a.popup?.close?.();a.hud.dismissControlHelp?.({remember:false});});
      row.stage='baseline';row.baseline=await measure(60000);await save();
      // Persist numerical evidence BEFORE potentially expensive capture.
      row.stage='baseline-screenshot';row.screenshot={file:`hud-${viewport.width}x${viewport.height}-baseline.png`,WebGL_held_only_for_capture:true,passed:false};await save();
      try {
        await holdDraws(true);
        await page.screenshot({path:path.join(output,row.screenshot.file),timeout:15000});
        row.screenshot.passed=true;
      }catch(error){row.screenshot.error=String(error.stack||error);}
      finally{await holdDraws(false);row.screenshot.renderer_restored=!(await page.evaluate(()=>!!window.__smokeHeldDraw));await save();}
      row.stage='planted-one';await save();
      await plant(['Extra']);try{row.oneMore=await measure(60000);await save();}finally{await unplant();}
      row.stage='planted-old-row';await save();
      await plant(['Start / Jaunts','Confidence','▾','Walk','◐','≡','Extra']);try{row.oldRow=await measure(60000);await save();}finally{await unplant();}
      const {baseline,oneMore,oldRow}=row;
      row.numeric_passed=baseline.navigatorDock.ready&&oneMore.navigatorDock.ready&&oldRow.navigatorDock.ready&&baseline.pct<=10&&baseline.boxes>0&&oneMore.pct>baseline.pct+.05&&(viewport.width>620||oldRow.pct>10);
      row.passed=row.numeric_passed&&row.screenshot.passed&&row.screenshot.renderer_restored;row.stage='complete';await save();
    }
    const open={name:'actual-open-device',stage:'measuring',passed:false};report.negatives.push(open);await save();
    await page.evaluate(()=>window.__chicago4d.navigator.open());open.measurement=await measure(2000);open.passed=!open.measurement.navigatorDock.ready&&open.measurement.navigatorDock.level>0;open.stage='complete';await save();
    await page.evaluate(()=>window.__chicago4d.navigator.dock());
    report.restored_before_animation=await measure(60000);await save();
    if(!report.restored_before_animation.navigatorDock.ready)throw Error('Could not restore dock before animation refusal');
    const running={name:'nonsettling-native-animation-visible-device',stage:'measuring',passed:false};report.negatives.push(running);await save();
    await page.evaluate(()=>{window.__hudReadinessNegative=document.getElementById('navigator').animate([{opacity:1},{opacity:1}],{duration:10000,iterations:Infinity});});
    try{running.measurement=await measure(2000);running.passed=!running.measurement.navigatorDock.ready&&running.measurement.navigatorDock.running.length>0;running.stage='complete';await save();}
    finally{await page.evaluate(()=>{window.__hudReadinessNegative?.cancel();delete window.__hudReadinessNegative;});}
    report.passed=report.runs.every(r=>r.passed)&&report.negatives.every(r=>r.passed);await save();
    if(!report.passed)throw Error('HUD qualification criteria failed; actual partial receipts preserved');
  }catch(error){report.error=String(error.stack||error);await save();throw error;}
  finally{
    await holdDraws(false).catch(error=>{report.renderer_restore_error=String(error);});
    await unplant().catch(error=>{report.plant_restore_error=String(error);});
    try{await page.evaluate(async state=>{window.__hudReadinessNegative?.cancel();delete window.__hudReadinessNegative;const n=window.__chicago4d.navigator;await n.select(state.app??'home');n.setLevel(state.level??0);},original);}catch(error){report.navigator_restore_error=String(error);}
    if(originalViewport)await page.setViewportSize(originalViewport).catch(error=>{report.viewport_restore_error=String(error);});
    report.restoration_requested={viewport:originalViewport,navigator:original};
    try{report.restoration_observed=await page.evaluate(()=>({heldDraws:!!window.__smokeHeldDraw,negativeAnimation:!!window.__hudReadinessNegative,plant:!!document.getElementById('smoke-t2628-planted'),app:window.__chicago4d.navigator.app,level:window.__chicago4d.navigator.level,viewport:{width:innerWidth,height:innerHeight}}));}catch(error){report.restoration_readback_error=String(error);}
    const restored=report.restoration_observed;
    report.restoration_passed=!!restored&&!restored.heldDraws&&!restored.negativeAnimation&&!restored.plant
      && restored.app===original.app&&restored.level===original.level
      && (!originalViewport||(restored.viewport.width===originalViewport.width&&restored.viewport.height===originalViewport.height))
      && !report.renderer_restore_error&&!report.plant_restore_error&&!report.navigator_restore_error&&!report.viewport_restore_error;
    if(!report.restoration_passed){report.passed=false;report.restoration_failure='Actual restoration receipt failed';}
    await save();
    if(!report.restoration_passed&&!report.error)throw Error('HUD harness state restoration failed; receipt preserved');
  }
  return report;
}
