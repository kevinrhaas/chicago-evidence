import fs from 'node:fs';import crypto from 'node:crypto';
import * as T from '/tmp/chicago-brick-3341/chicago/4d/renderers/web/vendor/three-0.185.1/three.module.js';
import {parseGlb,readAccessor} from '/tmp/chicago-brick-3341/chicago/4d/tools/k01_contract.mjs';
const app='/tmp/chicago-west-wicket-20261109/chicago/4d',site='/tmp/chicago-west-wicket-20261109/site/4d';
const jobs=[['1812','first_fort_dearborn_magazine','brick'],['1812','first_fort_dearborn_north_range','chimney'],['1812','kinzie_bake_house_1812','chimney'],['1835','lake_house_construction','brick'],['1835','green_tree_tavern','brick'],['1835','miller_house','chimney']];
const out={commit:'cab45145391cccb84ab408123b70207c32634fcc',build:JSON.parse(fs.readFileSync(site+'/build.json')),jobs:[]};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const [year,id,role] of jobs){const s=JSON.parse(fs.readFileSync(`${app}/data/sidecars/${year}/${id}.json`)),g=parseGlb(fs.readFileSync(`${app}/assets/${s.asset}`)),ctx={...g,views:new Map()},prims=[];
 function visit(i,parent){const n=g.json.nodes[i],local=n.matrix?new T.Matrix4().fromArray(n.matrix):new T.Matrix4().compose(new T.Vector3(...n.translation||[0,0,0]),new T.Quaternion(...n.rotation||[0,0,0,1]),new T.Vector3(...n.scale||[1,1,1])),m=parent.clone().multiply(local);
 for(const p of g.json.meshes?.[n.mesh]?.primitives||[]){const mat=g.json.materials[p.material];if(!mat.name.includes(role))continue;const a=readAccessor(ctx,p.attributes.POSITION),v=new T.Vector3(),pts=[];for(let j=0;j<a.length;j+=3)pts.push(v.set(a[j],a[j+1],a[j+2]).applyMatrix4(m).toArray());const idx=p.indices===undefined?pts.map((_,i)=>i):Array.from(readAccessor(ctx,p.indices));prims.push({name:mat.name,pts,idx,mapped:!!mat.pbrMetallicRoughness?.baseColorTexture});}
 for(const c of n.children||[])visit(c,m);}
 for(const n of g.json.scenes[g.json.scene||0].nodes)visit(n,new T.Matrix4());
 if(!prims.length)throw Error(id+' role missing '+role+' '+g.json.materials.map(m=>m.name));
 const parts=[];for(const p of prims){let groups;if(role==='chimney'||id==='green_tree_tavern'){const ts=[];for(let i=0;i<p.idx.length;i+=3){const ids=p.idx.slice(i,i+3);ts.push({ids,lo:[0,1,2].map(k=>Math.min(...ids.map(j=>p.pts[j][k]))),hi:[0,1,2].map(k=>Math.max(...ids.map(j=>p.pts[j][k])))});}const parents=ts.map((_,i)=>i),root=i=>parents[i]===i?i:(parents[i]=root(parents[i]));for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++)if([0,2].every(k=>ts[i].lo[k]<=ts[j].hi[k]+.001&&ts[j].lo[k]<=ts[i].hi[k]+.001))parents[root(i)]=root(j);const m=new Map();ts.forEach((t,i)=>{const k=root(i);m.set(k,[...m.get(k)||[],...t.ids]);});groups=[...m.values()];}else groups=[p.idx];for(const indices of groups){const ps=indices.map(i=>p.pts[i]),lo=[0,1,2].map(k=>Math.min(...ps.map(p=>p[k]))),hi=[0,1,2].map(k=>Math.max(...ps.map(p=>p[k])));parts.push({name:p.name,mapped:p.mapped,lo,hi});}}
 const bytes=fs.readFileSync(`${site}/data/${s.asset}`);out.jobs.push({year,id,role,parts,asset:{path:`data/${s.asset}`,bytes:bytes.length,sha256:hash(bytes)},sidecar:s});
}
fs.writeFileSync('/tmp/nov10-brick-3341/full-review/EXPECTED.json',JSON.stringify(out,null,2));console.log(JSON.stringify(out.jobs.map(j=>({year:j.year,id:j.id,parts:j.parts})),null,2));
