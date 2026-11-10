// CPU-only independent domain count from the unchanged, actually served glTF assets.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const base='/workspace/.cloud-setup/pages-alias-actual-20261110/site/4d/dev/data/humans/web/';
const site='/workspace/.cloud-setup/pages-alias-actual-20261110/site';
const catalogue=JSON.parse(await fs.readFile(site+'/4d/dev/asset-aliases.0cfb7ae413cd729d035ca2487f314eb7a01f8e5fbd6623b61c4de59d6b91a97f.json','utf8'));
async function readSheet(uri){const rel='data/humans/web/'+uri,alias=catalogue.aliases[rel],p=alias?site+alias.source:base+uri,b=await fs.readFile(p);if(alias){assert.equal(b.length,alias.bytes);assert.equal(crypto.createHash('sha256').update(b).digest('hex'),alias.sha256);}return b;}
const { MeshoptDecoder } = await import('/workspace/.cloud-setup/pages-alias-actual-20261110/site/4d/dev/walk/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js');
await MeshoptDecoder.ready;
const result=[];
for(const lod of [1,2,3]){
 const b=await fs.readFile(base+`nelson_charles_1904_coachman.lod${lod}.glb`);
 assert.equal(b.readUInt32LE(0),0x46546c67);assert.equal(b.readUInt32LE(4),2);
 const jsonLength=b.readUInt32LE(12),g=JSON.parse(b.subarray(20,20+jsonLength).toString());
 const bin=b.subarray(28+jsonLength);
 const buffers=await Promise.all(g.buffers.map(async (r,i)=>i===0?bin:r.uri?readSheet(r.uri):null)),views=new Map();
 const view=(id)=>{if(views.has(id))return views.get(id);const v=g.bufferViews[id],x=v.extensions?.EXT_meshopt_compression;let data;
  if(x){data=Buffer.alloc(x.count*x.byteStride);MeshoptDecoder.decodeGltfBuffer(data,x.count,x.byteStride,buffers[x.buffer].subarray(x.byteOffset??0,(x.byteOffset??0)+x.byteLength),x.mode,x.filter??'NONE');}
  else data=buffers[v.buffer].subarray(v.byteOffset??0,(v.byteOffset??0)+v.byteLength);
  views.set(id,data);return data;};
 const read=(id)=>{const a=g.accessors[id],v=g.bufferViews[a.bufferView],data=view(a.bufferView),sizes={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16},bytes={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4},get={5120:'readInt8',5121:'readUInt8',5122:'readInt16LE',5123:'readUInt16LE',5125:'readUInt32LE',5126:'readFloatLE'};assert(!a.sparse);const size=sizes[a.type],step=bytes[a.componentType],stride=v.byteStride??size*step,start=a.byteOffset??0;return Array.from({length:a.count},(_,i)=>Array.from({length:size},(_,j)=>data[get[a.componentType]](start+i*stride+j*step)));};
 const domains={l:0,r:0},meshes=[];
 for(const node of g.nodes){if(node.skin===undefined||node.mesh===undefined)continue;const joints=g.skins[node.skin].joints.map(id=>g.nodes[id].name);
  for(const [pi,p]of g.meshes[node.mesh].primitives.entries()){if(p.attributes.JOINTS_0===undefined)continue;assert(p.mode===undefined||p.mode===4);const index=p.indices===undefined?Array.from({length:g.accessors[p.attributes.POSITION].count},(_,i)=>i):read(p.indices).flat(),skin=read(p.attributes.JOINTS_0),weight=read(p.attributes.WEIGHTS_0),counts={};
   for(const side of ['l','r']){const seed=new Set();for(let i=0;i<skin.length;i++)for(let j=0;j<4;j++)if(weight[i][j]>0&&[`foot_${side}`,`ball_${side}`].includes(joints[skin[i][j]]))seed.add(i);const all=new Set(seed);for(let i=0;i<index.length;i+=3){const tri=index.slice(i,i+3);if(tri.some(id=>seed.has(id)))for(const id of tri)all.add(id);}counts[side]=all.size;domains[side]+=all.size;}
   meshes.push({name:node.name,primitive:pi,vertices:g.accessors[p.attributes.POSITION].count,counts});
  }
 }
 result.push({lod,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),domains,meshes});
}
console.log(JSON.stringify(result,null,2));
