import fs from 'node:fs';
import {MeshoptDecoder} from '/workspace/chicago/chicago/4d/renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js';
await MeshoptDecoder.ready;
const root='/workspace/chicago/chicago/4d/assets/humans/web/';
for(let lod=0;lod<4;lod++){
 const name=`bardwell_otis_1835.lod${lod}`,b=fs.readFileSync(root+name+'.glb');
 const n=b.readUInt32LE(12),g=JSON.parse(b.subarray(20,20+n).toString()),bin=b.subarray(n+28);
 const out=[],views=[];let offset=0;
 for(const v of g.bufferViews){
  const e=v.extensions?.EXT_meshopt_compression;let chunk;
  if(e){chunk=new Uint8Array(e.count*e.byteStride);MeshoptDecoder.decodeGltfBuffer(chunk,e.count,e.byteStride,bin.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter||'NONE');}
  else chunk=bin.subarray(v.byteOffset||0,(v.byteOffset||0)+v.byteLength);
  views.push({...v,byteOffset:offset,byteLength:chunk.length,extensions:undefined});out.push(chunk);offset+=chunk.length;
 }
 fs.writeFileSync(new URL(name+'.decoded.bin',import.meta.url),Buffer.concat(out));
 fs.writeFileSync(new URL(name+'.decoded-views.json',import.meta.url),JSON.stringify(views));
}
