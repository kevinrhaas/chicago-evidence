// SPDX-License-Identifier: GPL-3.0-or-later
// UNEXECUTED diagnostic. Takes an existing prepared/held page; never owns browser/server.
// Caller must establish the same route, mode, camera, detail and animationHold=true.
import fs from 'node:fs/promises';
import path from 'node:path';
export async function compareHeldPage(page, { outdir }) {
 if(!path.isAbsolute(outdir)||!outdir.startsWith('/workspace/shared/'))throw Error('outside shared evidence output directory required');
 const result = await page.evaluate(() => {
  const a=window.__chicago4d,r=a.renderer,flora=a.scene3d.getObjectByName('flora');
  if(!flora)throw Error('actual flora required');
  const wanted=new Set(['flora-mid','flora-far','flora-mid-carry']),cards=[],others=[];
  flora.traverse(o=>{if(!o.isMesh)return;for(const m of[].concat(o.material)){(wanted.has(o.name)?cards:others).push({object:o.name,material:m,geometry:o.geometry});}});
  const materials=[...new Set(cards.map(x=>x.material))];
  if(materials.length!==1||cards.length!==3)throw Error('expected exactly three card meshes sharing one reviewed material');
  if(others.some(x=>materials.includes(x.material)))throw Error('billboard material shared with unreviewed geometry');
  if(materials.some(m=>m.forceSinglePass!==false)||others.some(x=>x.material.forceSinglePass!==false))throw Error('baseline/negative flags differ from reviewed source');
  const saved=materials.map(m=>m.forceSinglePass),originalRender=r.render,originalDirect=r.renderBufferDirect,frames=[];let pixels=null;
  const gl=r.getContext(),w=gl.drawingBufferWidth,h=gl.drawingBufferHeight;
  const state=()=>JSON.stringify({camera:[...a.camera.position,...a.camera.quaternion],detail:a.detail,modes:a.confidence.modes,grade:a.confidence.grade('reconstructed'),geometry:[r.info.memory.geometries,...cards.map(x=>[x.object,x.geometry.uuid,x.geometry.drawRange.start,x.geometry.drawRange.count])],negative:others.map(x=>[x.object,x.material.forceSinglePass])});
  const initial=state();
  // Existing ghost twins can have their own version after side toggles. Dirty
  // the ACTUAL submitted twin too, so runtime A/B matches fresh source setup.
  r.renderBufferDirect=function(camera,scene,geometry,material,object,group){
   if(cards.some(x=>x.object===object.name)&&material.transparent)material.needsUpdate=true;
   return originalDirect.call(this,camera,scene,geometry,material,object,group);
  };
  r.render=function(...args){const out=originalRender.apply(this,args);gl.finish();pixels=new Uint8Array(w*h*4);gl.readPixels(0,0,w,h,gl.RGBA,gl.UNSIGNED_BYTE,pixels);return out;};
  function frame(label,flag){materials.forEach(m=>{m.forceSinglePass=flag;m.needsUpdate=true;});a.step();if(!pixels)throw Error('no actual rendered frame');if(state()!==initial)throw Error('camera/detail/confidence/geometry/negative flags changed');const p=pixels;pixels=null;const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;const context=canvas.getContext('2d'),image=context.createImageData(w,h);for(let y=0;y<h;y++)image.data.set(p.subarray(y*w*4,(y+1)*w*4),(h-1-y)*w*4);context.putImageData(image,0,0);return{label,flag,pixels:p,png:canvas.toDataURL('image/png'),stats:a.stats()};}
  try{
   frames.push(frame('baseline',false),frame('candidate',true),frame('restored',false));
   const delta=(x,y)=>{let sum=0,worst=0,changed=0;for(let i=0;i<x.length;i++){const d=Math.abs(x[i]-y[i]);sum+=d;worst=Math.max(worst,d);if(d)changed++;}return{mean:sum/x.length,worst,changedChannels:changed};};
   return{scope:'Actual same-page held-time full framebuffer on/off/on diagnostic, not historical331 reproduction',width:w,height:h,frames:frames.map(({pixels,...rest})=>rest),candidatePixels:delta(frames[0].pixels,frames[1].pixels),restoredPixels:delta(frames[0].pixels,frames[2].pixels),callsSaved:frames[0].stats.drawCalls-frames[1].stats.drawCalls,restoreCalls:frames[2].stats.drawCalls-frames[0].stats.drawCalls,cardObjects:cards.map(x=>x.object),negativeObjects:others.map(x=>x.object),strict330Unchanged:frames.every(f=>f.stats.budget.drawCalls===330)};
  }finally{materials.forEach((m,i)=>{m.forceSinglePass=saved[i];m.needsUpdate=true;});r.render=originalRender;r.renderBufferDirect=originalDirect;}
 });
 await fs.mkdir(outdir,{recursive:true});
 for(const frame of result.frames){const target=path.join(outdir,frame.label+'.png');await fs.writeFile(target,Buffer.from(frame.png.split(',')[1],'base64'));delete frame.png;frame.png_path=target;}
 await fs.writeFile(path.join(outdir,'comparison.json'),JSON.stringify(result,null,2)+'\n');
 return result;
}
