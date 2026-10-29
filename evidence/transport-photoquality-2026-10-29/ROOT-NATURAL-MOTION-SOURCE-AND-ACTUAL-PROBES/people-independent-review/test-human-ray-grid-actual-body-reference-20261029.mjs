// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only reference on actual canonical BODY source geometry, no pose/browser.
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import * as T from '/tmp/chicago-transport-resume-20261029/chicago/4d/renderers/web/vendor/three-0.185.1/three.module.js';
import {rayTriangleCandidates} from './human-ray-grid-proposal.mjs';
const source='/tmp/chicago-transport-resume-20261029/chicago/4d/assets/humans/bardwell_otis_1835.lod0.glb';
const raw=fs.readFileSync(source),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(sha(raw),'84cdeb6d362aa1a85549b18daef41ae492f18595a19ff5b7e6eff539a3576d04');
const jsonLength=raw.readUInt32LE(12),d=JSON.parse(raw.subarray(20,20+jsonLength)),bin=raw.subarray(28+jsonLength);
const material=d.materials.findIndex(m=>m.name==='skin'),mesh=d.meshes.find(m=>m.primitives.some(p=>p.material===material)),primitive=mesh.primitives.find(p=>p.material===material);
function read(idx,width){
  const a=d.accessors[idx],v=d.bufferViews[a.bufferView],offset=(v.byteOffset??0)+(a.byteOffset??0),size=a.componentType===5123?2:4,values=[];
  assert.equal(v.buffer,0);assert(!v.extensions,'Uncompressed canonical master reference required');
  for(let i=0;i<a.count;i++)for(let j=0;j<width;j++){
    const o=offset+i*(v.byteStride??size*width)+j*size;
    values.push(a.componentType===5126?bin.readFloatLE(o):a.componentType===5123?bin.readUInt16LE(o):bin.readUInt32LE(o));
  }
  return values;
}
const p=read(primitive.attributes.POSITION,3),index=read(primitive.indices,1),minimum=[Infinity,Infinity,Infinity],maximum=[-Infinity,-Infinity,-Infinity];
for(let i=0;i<p.length;i++){minimum[i%3]=Math.min(minimum[i%3],p[i]);maximum[i%3]=Math.max(maximum[i%3],p[i]);}
let checked=0,totalSelected=0,totalFull=0;
for(const cell of [.035,.1,.25]){
  const grid=new Map();
  for(let i=0;i<index.length;i+=3){
    const bounds=[0,1,2].map(a=>[Math.floor(Math.min(p[index[i]*3+a],p[index[i+1]*3+a],p[index[i+2]*3+a])/cell),Math.floor(Math.max(p[index[i]*3+a],p[index[i+1]*3+a],p[index[i+2]*3+a])/cell)]);
    for(let x=bounds[0][0];x<=bounds[0][1];x++)for(let y=bounds[1][0];y<=bounds[1][1];y++)for(let z=bounds[2][0];z<=bounds[2][1];z++){
      const key=`${x},${y},${z}`;if(!grid.has(key))grid.set(key,[]);grid.get(key).push(i);
    }
  }
  const center=minimum.map((v,i)=>(v+maximum[i])/2),boundary=center.map(v=>Math.round(v/cell)*cell);
  const points=[center,maximum.map(v=>v+1),minimum.map(v=>v-1),p.slice(0,3),p.slice(61*3,61*3+3),boundary,[boundary[0],center[1],center[2]],[center[0],boundary[1],center[2]]];
  for(const point of points)for(const ds of [[1,.381,.627],[-.27,1,.431],[.183,-.361,1],[1,0,0],[0,-1,0],[1,1,1],[-1,-1,0]]){
    const ray=new T.Ray(new T.Vector3(...point),new T.Vector3(...ds).normalize()),a=new T.Vector3(),b=new T.Vector3(),c=new T.Vector3(),hit=new T.Vector3();
    function hits(ids){const out=[];for(const i of ids){a.fromArray(p,index[i]*3);b.fromArray(p,index[i+1]*3);c.fromArray(p,index[i+2]*3);if(ray.intersectTriangle(a,b,c,false,hit))out.push(i);}return out.sort((x,y)=>x-y);}
    const ids=rayTriangleCandidates(grid,minimum,maximum,point,ray.direction.toArray(),cell);
    const expected=hits(Array.from({length:index.length/3},(_,i)=>i*3)),actual=hits(ids);
    assert.deepEqual(actual,expected,JSON.stringify({cell,point,ds}));checked++;totalFull+=index.length/3;totalSelected+=ids.length;
  }
}
console.log(JSON.stringify({passed:true,scope:'Actual canonical LOD0 BODY source geometry only; no pose/mixer capture',parent_sha256:sha(raw),body_mesh:mesh.name,body_triangles:index.length/3,cases:checked,full_triangles_tested:totalFull,filtered_candidates:totalSelected,reduction:totalFull/totalSelected,proposal_sha256:sha(fs.readFileSync(new URL('./human-ray-grid-proposal.mjs',import.meta.url)))}));
