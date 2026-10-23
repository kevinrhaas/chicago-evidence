// SPDX-License-Identifier: GPL-3.0-or-later
// Diagnostic only: existing prepared held page, no browser/server ownership.
import fs from 'node:fs/promises';
import path from 'node:path';
export async function compareHeldPage(page, { outdir }) {
 if(!path.isAbsolute(outdir)||!outdir.startsWith('/workspace/shared/'))throw Error('outside shared evidence output directory required');
 const result=await page.evaluate(()=>{
  const receipt={scope:'Bounded actual held-page billboard diagnostic; not full smoke/historical331 reproduction',ok:false,warmup:[],frames:[],errors:[],stateDifferences:[]};
  const wanted=new Set(['flora-mid','flora-far','flora-mid-carry']);
  let a,r,gl,originalRender,originalDirect,materials=[],saved=[],pixels=null,cards=[],others=[],restoreInstalled=false;
  function collect(){const f=a.scene3d.getObjectByName('flora');if(!f)throw Error('actual flora required');const c=[],o=[];f.traverse(x=>{if(!x.isMesh)return;for(const m of[].concat(x.material))(wanted.has(x.name)?c:o).push({object:x.name,material:m,geometry:x.geometry});});return{cards:c,others:o};}
  const finite=x=>Number.isFinite(x)?x:String(x);
  function state(){const parts=collect();return{camera:[...a.camera.position,...a.camera.quaternion],detail:a.detail,modes:JSON.parse(JSON.stringify(a.confidence.modes)),grade:JSON.parse(JSON.stringify(a.confidence.grade('reconstructed'))),geometry:[r.info.memory.geometries,...parts.cards.map(x=>[x.object,x.geometry.uuid,x.geometry.drawRange.start,finite(x.geometry.drawRange.count)])],negative:parts.others.map(x=>[x.object,x.material.forceSinglePass])};}
  function diff(x,y,p=''){if(JSON.stringify(x)===JSON.stringify(y))return[];if(x&&y&&typeof x==='object'&&typeof y==='object'&&Array.isArray(x)===Array.isArray(y)){return[...new Set([...Object.keys(x),...Object.keys(y)])].flatMap(k=>diff(x[k],y[k],p+'/'+k));}return[{path:p,before:x,after:y}];}
  function grab(label){if(!pixels)throw Error('no actual rendered frame');const p=pixels;pixels=null;const canvas=document.createElement('canvas');canvas.width=receipt.width;canvas.height=receipt.height;const ctx=canvas.getContext('2d'),image=ctx.createImageData(canvas.width,canvas.height);for(let y=0;y<canvas.height;y++)image.data.set(p.subarray(y*canvas.width*4,(y+1)*canvas.width*4),(canvas.height-1-y)*canvas.width*4);ctx.putImageData(image,0,0);return{label,pixels:p,png:canvas.toDataURL('image/png'),stats:a.stats()};}
  const delta=(x,y)=>{if(x.length!==y.length)throw Error('pixel dimensions changed');let sum=0,worst=0,changed=0;for(let i=0;i<x.length;i++){const d=Math.abs(x[i]-y[i]);sum+=d;worst=Math.max(worst,d);if(d)changed++;}return{mean:sum/x.length,worst,changedChannels:changed};};
  try{
   a=window.__chicago4d;r=a.renderer;gl=r.getContext();receipt.width=gl.drawingBufferWidth;receipt.height=gl.drawingBufferHeight;originalRender=r.render;originalDirect=r.renderBufferDirect;
   // Readback is inside the actual frame, before the non-preserved buffer can clear.
   r.render=function(...args){const out=originalRender.apply(this,args);gl.finish();pixels=new Uint8Array(receipt.width*receipt.height*4);gl.readPixels(0,0,receipt.width,receipt.height,gl.RGBA,gl.UNSIGNED_BYTE,pixels);return out;};restoreInstalled=true;
   receipt.initial=state();
   // Baseline preparation is bounded and recorded. No candidate flag is set.
   let previousAfter=null,previousChanges=null,stable=false;
   for(let i=0;i<3;i++){
    const parts=collect();if(parts.cards.some(x=>x.material.forceSinglePass!==false))throw Error('warmup baseline card flag must be false');
    const before=state();a.step();const frame=grab('warmup-'+(i+1));const after=state();const changes=diff(before,after);const fromPrevious=previousAfter?diff(previousAfter,after):null;
    receipt.warmup.push({...frame,before,after,differences:changes,differencesFromPreviousAfter:fromPrevious});
    if(previousAfter&&previousChanges.length===0&&fromPrevious.length===0&&changes.length===0){stable=true;receipt.stableAfter=after;break;}
    previousAfter=after;previousChanges=changes;
   }
   if(!stable)throw Error('baseline did not stabilize across two consecutive actual warmup frames within maximum3');
   // Only after preparation freeze the material/geometry references for the experiment.
   ({cards,others}=collect());materials=[...new Set(cards.map(x=>x.material))];
   if(materials.length!==1||cards.length!==3)throw Error('expected three reviewed card meshes sharing one material');
   if(others.some(x=>materials.includes(x.material)))throw Error('card material shared with unreviewed geometry');
   if(materials.some(m=>m.forceSinglePass!==false)||others.some(x=>x.material.forceSinglePass!==false))throw Error('baseline or negative flags differ from reviewed source');
   saved=materials.map(m=>m.forceSinglePass);const expected=receipt.stableAfter;
   r.renderBufferDirect=function(camera,scene,geometry,material,object,group){if(cards.some(x=>x.object===object.name)&&material.transparent)material.needsUpdate=true;return originalDirect.call(this,camera,scene,geometry,material,object,group);};
   for(const[label,flag]of[['baseline',false],['candidate',true],['restored',false]]){
    materials.forEach(m=>{m.forceSinglePass=flag;m.needsUpdate=true;});const before=state();a.step();const frame=grab(label);
    // Preserve every obtained PNG/stat BEFORE state reads or checks can fail.
    receipt.frames.push({...frame,flag,before});
    const after=state();const changes=diff(expected,after);
    Object.assign(receipt.frames.at(-1),{after,differences:changes});
    receipt.stateDifferences.push({label,differences:changes});
    if(changes.length)throw Error('state changed at '+label+': '+changes.map(x=>x.path).join(', '));
   }
   receipt.candidatePixels=delta(receipt.frames[0].pixels,receipt.frames[1].pixels);receipt.restoredPixels=delta(receipt.frames[0].pixels,receipt.frames[2].pixels);receipt.callsSaved=receipt.frames[0].stats.drawCalls-receipt.frames[1].stats.drawCalls;receipt.restoreCalls=receipt.frames[2].stats.drawCalls-receipt.frames[0].stats.drawCalls;receipt.cardObjects=cards.map(x=>x.object);receipt.negativeObjects=others.map(x=>x.object);receipt.strict330Unchanged=receipt.frames.every(f=>f.stats.budget.drawCalls===330);
   if(!receipt.strict330Unchanged)throw Error('330 budget changed');
   if(receipt.frames.some(f=>f.stats.triangles!==receipt.frames[0].stats.triangles))throw Error('submitted triangle count changed');
   if(receipt.restoredPixels.worst!==0||receipt.restoreCalls!==0)throw Error('restoration pixels/calls changed');
   if(receipt.candidatePixels.worst!==0)throw Error('candidate pixels differ; no equivalence acceptance');
   receipt.ok=true;
  }catch(e){receipt.errors.push(e.stack||String(e));try{receipt.failureState=state();}catch(x){receipt.failureStateError=String(x);}}
  finally{
   for(let i=0;i<materials.length;i++){if(i<saved.length){materials[i].forceSinglePass=saved[i];materials[i].needsUpdate=true;}}
   if(restoreInstalled){r.render=originalRender;r.renderBufferDirect=originalDirect;}
   // Typed arrays are kept only for local comparisons; PNGs/states remain durable.
   for(const f of[...receipt.warmup,...receipt.frames])delete f.pixels;
  }
  return receipt;
 });
 await fs.mkdir(outdir,{recursive:true});
 for(const frame of[...result.warmup,...result.frames]){const target=path.join(outdir,frame.label+'.png');await fs.writeFile(target,Buffer.from(frame.png.split(',')[1],'base64'));delete frame.png;frame.png_path=target;}
 const target=path.join(outdir,'comparison.json');await fs.writeFile(target,JSON.stringify(result,null,2)+'\n');
 if(!result.ok){const error=new Error('Billboard diagnostic failed; partial states/PNGs/stats saved: '+target+'; '+result.errors.join('\n'));error.partialReceipt=result;throw error;}
 return result;
}
