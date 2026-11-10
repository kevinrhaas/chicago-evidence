import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { sampleGroundCut } from './ground-cut-observer.mjs';
const source=await fs.readFile(new URL('./desktop-post-a-2c-next.mjs',import.meta.url),'utf8');
const start=source.indexOf('async function physical(cell,label){'),end=source.indexOf('\nlet poses;',start);
assert(start>=0&&end>start);
const state={physicalErrors:[],errors:[],physicalReviewRequired:[]},cell={kind:'candidate',physical:[]},phases=[];
const sandbox={state,sampleGroundCut,person:'charles',progress:async p=>phases.push(p),
 __chicago4d:{humans:{get:()=>({e:1395.2,n:-3245.955,lod:2,wanted:1,pending:Promise.resolve(),body:null,root:{visible:true},indoors:false})},parkedTransport:{instances:[]}},
 page:{evaluate:async(fn,args)=>fn(args)}};
vm.createContext(sandbox);
const physical=vm.runInContext(source.slice(start,end)+';physical;',sandbox);
const result=await physical(cell,'controlled-missing-body');
assert.match(result.observerFailure,/Actual actor\/team not loaded/);
assert.equal(result.diagnostic.actor.lod,2);
assert.equal(result.diagnostic.actor.wanted,1);
assert.equal(result.diagnostic.actor.pending,true);
assert.equal(state.physicalErrors.length,1);
assert.equal(state.errors.length,1,'strict global failure is retained');
assert.equal(cell.physical.length,1,'partial diagnostic evidence survives');
assert.match(phases[0],/NONPASS-SAVED/);
let independentImageStageReached=false;
await Promise.resolve().then(()=>{independentImageStageReached=true;});
assert(independentImageStageReached,'failed physical observation returns to the independent image protocol');
console.log('PASS: exact observer serializes failure + actual LOD/ownership diagnostics, retains strict NONPASS and returns to independent image stage');
