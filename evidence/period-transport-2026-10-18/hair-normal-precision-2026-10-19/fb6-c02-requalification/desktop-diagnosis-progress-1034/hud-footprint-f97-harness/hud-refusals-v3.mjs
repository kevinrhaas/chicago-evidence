// SPDX-License-Identifier: GPL-3.0-or-later
// Refusal-only followup. The V3 numerical measurement is imported without changes.
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {measureHudFootprint} from './hud-qualification-v3.mjs';
export async function runHudRefusals(page,{output}={}) {
  if(!output||!output.endsWith('refusals-v3'))throw Error('Fresh output directory ending refusals-v3 required');
  await mkdir(output,{recursive:false});
  const report={scope:'Actual DOM Navigator refusal controls only; not full positive, touch, phoneGPU, photographic or production qualification',version:3,passed:false,steps:[]};
  const save=()=>writeFile(path.join(output,'hud-refusals.json'),JSON.stringify(report,null,2)+'\n');
  const originalViewport=page.viewportSize();
  const original=await page.evaluate(()=>({app:window.__chicago4d.navigator.app,level:window.__chicago4d.navigator.level,held:!!window.__smokeHeldDraw,animation:!!window.__hudReadinessNegative}));
  report.original={viewport:originalViewport,...original};await save();
  if(original.held||original.animation)throw Error('Require live renderer and no existing diagnostic animation; caller state untouched');
  const measure=async timeoutMs=>{if(await page.evaluate(()=>!!window.__smokeHeldDraw))throw Error('Refusal measurement must use unheld renderer');return page.evaluate(measureHudFootprint,{timeoutMs});};
  const step=async(name,operation)=>{const row={name,stage:'started',passed:false};report.steps.push(row);await save();await operation(row);row.stage='complete';await save();if(!row.passed)throw Error('Refusal control failed: '+name);return row;};
  try {
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(async()=>{const n=window.__chicago4d.navigator;await n.select('home');n.dock();});
    const baseline=await step('actual-baseline-dock',async row=>{row.measurement=await measure(60000);row.passed=row.measurement.navigatorDock.ready&&row.measurement.boxes>0;});
    await step('actual-open-refusal',async row=>{
      await page.evaluate(()=>window.__chicago4d.navigator.open());
      row.measurement=await measure(2000);
      const m=row.measurement,n=m.navigatorDock;
      row.passed=!n.ready&&n.visible&&n.level>0&&m.boxes>0&&m.pct>10;
    });
    const restored=await step('actual-restored-dock',async row=>{await page.evaluate(()=>window.__chicago4d.navigator.dock());row.measurement=await measure(60000);row.passed=row.measurement.navigatorDock.ready&&row.measurement.boxes>0;});
    await step('actual-native-animation-refusal',async row=>{
      const prior=restored.measurement.navigatorDock;
      await page.evaluate(()=>{window.__hudReadinessNegative=document.getElementById('navigator').animate([{opacity:1},{opacity:1}],{duration:10000,iterations:Infinity});});
      try {
        row.measurement=await measure(2000);const n=row.measurement.navigatorDock;
        row.unchanged_dock={semantic:n.level===prior.level&&n.detent===prior.detent,box:JSON.stringify(n.box)===JSON.stringify(prior.box)};
        row.passed=n.visible&&!n.ready&&n.running.length>0&&row.measurement.boxes>0&&row.unchanged_dock.semantic&&row.unchanged_dock.box;
      }finally{await page.evaluate(()=>{window.__hudReadinessNegative?.cancel();delete window.__hudReadinessNegative;});row.cancelled=await page.evaluate(()=>!window.__hudReadinessNegative);await save();}
    });
    await step('actual-animation-cancelled-and-dock-ready',async row=>{row.measurement=await measure(60000);row.animation_absent=await page.evaluate(()=>!window.__hudReadinessNegative);row.passed=row.animation_absent&&row.measurement.navigatorDock.ready;});
    report.controls_passed=report.steps.every(row=>row.passed);await save();
  }catch(error){report.error=String(error.stack||error);await save();throw error;}
  finally{
    try{await page.evaluate(async state=>{window.__hudReadinessNegative?.cancel();delete window.__hudReadinessNegative;const n=window.__chicago4d.navigator;await n.select(state.app);n.setLevel(state.level);},original);}catch(error){report.restore_error=String(error);}
    if(originalViewport)await page.setViewportSize(originalViewport).catch(error=>{report.viewport_restore_error=String(error);});
    try{report.restoration=await page.evaluate(()=>({app:window.__chicago4d.navigator.app,level:window.__chicago4d.navigator.level,held:!!window.__smokeHeldDraw,animation:!!window.__hudReadinessNegative,viewport:{width:innerWidth,height:innerHeight}}));}catch(error){report.readback_error=String(error);}
    const r=report.restoration;
    report.restoration_passed=!!r&&!report.restore_error&&!report.viewport_restore_error&&!r.held&&!r.animation&&r.app===original.app&&r.level===original.level&&(!originalViewport||(r.viewport.width===originalViewport.width&&r.viewport.height===originalViewport.height));
    report.passed=report.controls_passed===true&&report.restoration_passed;await save();
    if(!report.restoration_passed&&!report.error)throw Error('Refusal state restoration failed; receipt preserved');
  }
  if(!report.passed)throw Error('Refusal controls incomplete; receipt preserved');
  return report;
}
