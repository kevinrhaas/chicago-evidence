import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {performance} from 'node:perf_hooks';
const start=performance.now();
const dir=new URL('./',import.meta.url);
const load=async p=>import('data:text/javascript;base64,'+Buffer.from(await readFile(new URL(p,dir))).toString('base64'));
const original=await load('BASE-planar-occluders.js'),candidate=await load('planar-occluders.js');
const rect=(x0,y0,x1,y1)=>[x0,y0,-5,x1,y0,-5,x1,y1,-5,x0,y0,-5,x1,y1,-5,x0,y1,-5];
const wall=(gap=0)=>[...rect(-10,-10,2,10),...rect(2+gap,-10,4,2),...rect(2+gap,4,4,10),...rect(4,-10,10,10)];
const rows=[];
for(const [name,points,options] of [
 ['existing-opening',wall(),{}],['existing-crack',wall(.01),{}],['existing-hairline',wall(.001),{}],
 ['wide-fallback',rect(-20,-20,20,20),{}],['threshold65535',rect(0,0,257,259),{res:1}],['threshold65536',rect(0,0,258,258),{res:1}],['sparse-large-grid',[...rect(0,0,.5,30),...rect(29.5,0,30,30)],{}],
 ['min-cells-refusal',wall(),{minCells:1e6}],['small-plane-refusal',wall(),{minPlaneArea:500}],
]){
 const a=original.planarCoverPlanes(points,null,options),b=candidate.planarCoverPlanes(points,null,options);
 assert.equal(a.length,b.length);
 for(let j=0;j<a.length;j++){
  const {sat:oldSat,...oldMeta}=a[j],{sat:newSat,...newMeta}=b[j];assert.deepEqual(oldMeta,newMeta);
  assert.equal(oldSat.length,newSat.length);for(let i=0;i<oldSat.length;i++)assert.ok(Object.is(oldSat[i],newSat[i]),name+' prefix '+i);
  assert.equal(newSat.constructor,a[j].cells<=65535?Uint16Array:Int32Array);
  rows.push({name,cells:a[j].cells,grid:[a[j].W,a[j].H],oldBytes:oldSat.byteLength,newBytes:newSat.byteLength,exactEntries:oldSat.length});
 }
}
// Threshold witness: a flat rectangle with 258x258 interior cells exceeds u16.
assert.ok(rows.find(r=>r.name==='wide-fallback').cells>65535);
assert.equal(rows.find(r=>r.name==='threshold65535').cells,65535);
assert.equal(rows.find(r=>r.name==='threshold65536').cells,65536);
assert.ok(rows.find(r=>r.name==='sparse-large-grid').grid.reduce((a,b)=>a*b)>65535);
const report={result:'PASS',method:'Actual original and candidate planarCoverPlanes; every prefix Object.is identical, every remaining plane field deep equal',rows,seconds:(performance.now()-start)/1000,applicationMutated:false,browserRun:false};
await writeFile(new URL('PURE-ORIGINAL-CPU-CONTROLS.json',dir),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
