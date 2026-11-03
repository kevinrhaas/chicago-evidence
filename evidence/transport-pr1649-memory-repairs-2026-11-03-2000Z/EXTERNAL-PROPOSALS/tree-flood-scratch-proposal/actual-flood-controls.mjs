import assert from 'node:assert/strict';import {readFile,writeFile} from 'node:fs/promises';import {performance} from 'node:perf_hooks';
const start=performance.now(),dir=new URL('./',import.meta.url),AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
const extract=async file=>{const text=await readFile(new URL(file,dir),'utf8');const a=text.indexOf('  let divideFloorRow = 0;'),b=text.indexOf('  const WEST = div[cellAt(-300, 0)];',a);assert.ok(a>0&&b>a);let body=text.slice(a,b);body=body.replace('  const floodSeparates = (cutRow) => {','  const floodSeparates = (cutRow) => { trace.push(cutRow);');return new AsyncFunction('cols','rows','cellM','originE','originN','data','checkpoint','trace',`const cells=cols*rows,CHANNEL_Y=-.60;${body};return {divideFloorRow,div,labels,st};`);};
const old=await extract('BASE-trees.js'),candidate=await extract('trees.js'),rows=[];
for(const mode of ['separate-from-start','search-required','inseparable','all-water']){
 const cols=65,rowsN=65,cellM=10,originE=-320,originN=-320,data=new Float32Array(cols*rowsN).fill(1);
 for(let r=0;r<rowsN;r++)for(let c=0;c<cols;c++){
  const vertical=c===32, horizontal=r===32&&c>=32;
  const water=mode==='all-water'||(mode!=='inseparable'&&(vertical||horizontal)&&(mode!=='search-required'||r>=10));if(water)data[r*cols+c]=-2;
 }
 const args=[cols,rowsN,cellM,originE,originN,data,()=>null];const ta=[],tb=[],a=await old(...args,ta),b=await candidate(...args,tb);
 assert.deepEqual(ta,tb);assert.equal(a.divideFloorRow,b.divideFloorRow);assert.equal(a.labels,b.labels);assert.deepEqual(a.div,b.div);assert.ok(a.st instanceof Int32Array);assert.equal(b.st,null);
 rows.push({mode,divideFloorRow:a.divideFloorRow,floodCalls:ta,labels:a.labels,exactDivEntries:a.div.length,retainedScratchOld:a.st.byteLength,retainedScratchNew:0});
}
assert.ok(rows.some(r=>r.floodCalls.length>1),'binary search really executed');
const report={result:'PASS',method:'Actual original and candidate flood+division code extracted through cellAt; exact call trace, cut row, labels and all division bytes; candidate retained scratch null',rows,seconds:(performance.now()-start)/1000,applicationMutated:false,browserRun:false};await writeFile(new URL('PURE-ACTUAL-FLOOD-CONTROLS.json',dir),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
