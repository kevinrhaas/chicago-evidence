/** Replays only recorded actual texels, never asserts a reconstructed full mask. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { definitelyCutByRedMask } from '/tmp/chicago-pedestrian-ground-2c9-20261110/chicago/4d/renderers/web/js/pedestrian-ground.js';
const input='/workspace/.cloud-setup/coachman-placement-plan-20261110/desktop-post-a-06/browser/PHYSICAL-FIRST-IMMUTABLE.json';
const bytes=fs.readFileSync(input),p=JSON.parse(bytes),texture=p.groundCut.texture,uniforms=p.groundCut.groundUniforms;
const sha=value=>createHash('sha256').update(value).digest('hex');
assert.equal(texture.sha256,'ef7c5c8e3044c87b3e8e9840aab362e12743e73214f8eeea9f2d658a0c32aab9');
assert.equal(uniforms.length,2);
const boxValues=uniforms[0].box,box={x:boxValues[0],y:boxValues[1],z:boxValues[2],w:boxValues[3]};
for(const g of uniforms){assert.equal(g.on,1);assert.deepEqual(g.box,boxValues);}
const w=texture.width,h=texture.height,known=new Map();
const indices=(u,v)=>{const x=Math.floor(u*w-.5),y=Math.floor(v*h-.5),cx=a=>Math.max(0,Math.min(w-1,a)),cy=a=>Math.max(0,Math.min(h-1,a));return[cy(y)*w+cx(x),cy(y)*w+cx(x+1),cy(y+1)*w+cx(x),cy(y+1)*w+cx(x+1)];};
const vertices=Object.values(p.feet).flatMap(foot=>foot.allVertices);
for(const v of vertices){assert.equal(v.terrainDiscardedInAllMaterials,true);assert.equal(v.mask.length,2);
  for(const sample of v.mask){assert(sample.discarded&&sample.inside);indices(sample.u,sample.v).forEach((i,k)=>{const value=sample.texels[k]*255;assert(Number.isInteger(value));if(known.has(i))assert.equal(known.get(i),value);known.set(i,value);});}}
// Unknown pixels stay zero, so this sparse sample fixture can only refuse more
// points than the actual texture. It cannot invent positive mask coverage.
const data=new Uint8Array(w*h);for(const[i,value]of known)data[i]=value;
const mask={image:{data,width:w,height:h},flipY:false};
let sampleCellChanges=0,maxUvDelta=0;
for(const v of vertices){const f=Math.fround,u=f(f(f(v.e)-f(box.x))*f(box.z)),vv=f(f(f(-v.n)-f(box.y))*f(box.w));
  maxUvDelta=Math.max(maxUvDelta,Math.abs(u-v.mask[0].u),Math.abs(vv-v.mask[0].v));
  if(JSON.stringify(indices(u,vv))!==JSON.stringify(indices(v.mask[0].u,v.mask[0].v)))sampleCellChanges++;
  assert(definitelyCutByRedMask(mask,box,v.e,v.n),'new admission uses only actual recorded covered pixels');}
assert(definitelyCutByRedMask(mask,box,1395.2,-3245.955),'actor centre also covered by actual recorded texels');
assert(!definitelyCutByRedMask(mask,box,box.x+1,-box.y-1),'unrecorded pixels remain unqualified');
const start=performance.now();for(let i=0;i<10000;i++)assert(definitelyCutByRedMask(mask,box,1395.2,-3245.955));
console.log(JSON.stringify({status:'PASS',input,inputSha256:sha(bytes),actualTextureSha256:texture.sha256,
  actualUniformBox:boxValues,vertices:vertices.length,knownPixels:known.size,sampleCellChanges,maxUvDelta,mask10000QueriesMs:performance.now()-start,
  qualification:'Only actual recorded06 texels reused. Sparse CPU mask is not the full original GPU texture and its hash is not substituted. Same foot-domain and centre coverage after explicit Float32 UV arithmetic; post-change contact remains unmeasured.'}));
