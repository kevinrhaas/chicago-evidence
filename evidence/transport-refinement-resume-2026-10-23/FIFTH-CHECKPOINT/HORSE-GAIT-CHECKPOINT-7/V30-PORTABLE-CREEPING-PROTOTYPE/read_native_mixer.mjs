// Source-only native portable-loader readback. No renderer, app or traffic.
import fs from 'node:fs';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import * as T from '/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/vendor/three.module.js';
import {GLTFLoader} from '/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/vendor/GLTFLoader.mjs';
import {clone} from '/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/vendor/SkeletonUtils.mjs';
const D=new URL('.',import.meta.url),sha=b=>crypto.createHash('sha256').update(b).digest('hex'),read=n=>fs.readFileSync(new URL(n,D)),save=(n,o)=>fs.writeFileSync(new URL(n,D),JSON.stringify(o,null,2)+'\n');
const start=performance.now(),bytes=read('creeping-015mps-PORTABLE-STUDY-NOT-APP.glb'),jsonLength=bytes.readUInt32LE(12),j=JSON.parse(bytes.subarray(20,20+jsonLength));
const loader=new GLTFLoader();loader.register(()=>({name:'CPU_NO_TEXTURE_LOAD',loadTexture:()=>Promise.resolve(null)}));
const g=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
const scene=clone(g.scene),byName=new Map();scene.traverse(o=>{if(o.isSkinnedMesh){assert(!byName.has(o.name));byName.set(o.name,o);}});
const originals=[];g.scene.traverse(o=>{if(o.isSkinnedMesh)originals.push(o);});
const meshes=[26,27,28].map(ni=>{const original=originals.find(m=>g.parser.associations.get(m)?.nodes===ni);assert(original,`missing node${ni}`);const m=byName.get(original.name);assert(m&&m!==original&&m.skeleton.bones[0]!==original.skeleton.bones[0]);return m;});
const clip=g.animations.find(a=>a.name==='RECONSTRUCTED_CREEPING_015MPS_STUDY_NOT_NATURAL_WALK');assert(clip);const mixer=new T.AnimationMixer(scene),action=mixer.clipAction(clip);action.setLoop(T.LoopOnce,1);action.clampWhenFinished=true;action.play();
const encodedTimes=clip.tracks.find(t=>t.times.length===129).times,actualTimes=[];for(let k=0;k<128;k++)actualTimes.push(encodedTimes[k],(encodedTimes[k]+encodedTimes[k+1])/2);actualTimes.push(encodedTimes[128]);
const fd=fs.openSync(new URL('ACTUAL-NATIVE-POSITIONS-AND-SHADER-NORMALS.f64',D),'w'),frames=[],p=new T.Vector3(),n=new T.Vector3(),tmp=new T.Vector3();let negative=0,minWeight=0,maxWeight=0,minimumFinite=true,signedWeightControl=null;
for(let k=0;k<=256;k++){
 const time=1.6*k/256;mixer.setTime(actualTimes[k]);scene.updateMatrixWorld(true);for(const m of meshes)m.skeleton.update();
 for(const m of meshes){const a=m.geometry.attributes,targets=m.geometry.morphAttributes.normal??[],weights=m.morphTargetInfluences??[],bm=m.skeleton.boneMatrices;assert(m.bindMatrix.equals(new T.Matrix4())&&m.bindMatrixInverse.equals(new T.Matrix4()),'source identity mesh bind required');
  assert(!targets.length||m.geometry.morphTargetsRelative);for(const w of weights){if(w<0)negative++;minWeight=Math.min(minWeight,w);maxWeight=Math.max(maxWeight,w);}
  const out=new Float64Array(a.position.count*6);
  for(let vi=0;vi<a.position.count;vi++){
   m.getVertexPosition(vi,p).applyMatrix4(m.matrixWorld);n.fromBufferAttribute(a.normal,vi);
   for(let ti=0;ti<targets.length;ti++)if(weights[ti]!==0)n.addScaledVector(tmp.fromBufferAttribute(targets[ti],vi),weights[ti]);
   const x=n.x,y=n.y,z=n.z;n.set(0,0,0);
   for(let wi=0;wi<4;wi++){const ji=a.skinIndex.array[vi*4+wi],w=a.skinWeight.array[vi*4+wi],b=ji*16;n.x+=w*(bm[b]*x+bm[b+4]*y+bm[b+8]*z);n.y+=w*(bm[b+1]*x+bm[b+5]*y+bm[b+9]*z);n.z+=w*(bm[b+2]*x+bm[b+6]*y+bm[b+10]*z);}
   n.normalize();out.set([...p.toArray(),...n.toArray()],vi*6);minimumFinite&&=p.toArray().every(Number.isFinite)&&n.toArray().every(Number.isFinite);
  }
  fs.writeSync(fd,Buffer.from(out.buffer));
  if(m===meshes[1]&&!signedWeightControl&&weights.some(w=>w<-.2)){
   const saved=[...weights];for(let wi=0;wi<weights.length;wi++)weights[wi]=Math.abs(weights[wi]);let changed=0;
   for(let vi=0;vi<a.position.count;vi++){m.getVertexPosition(vi,p).applyMatrix4(m.matrixWorld);changed=Math.max(changed,Math.hypot(p.x-out[vi*6],p.y-out[vi*6+1],p.z-out[vi*6+2]));}
   for(let wi=0;wi<weights.length;wi++)weights[wi]=saved[wi];signedWeightControl={time_s:time,corruption:'replace all signed PCA influences by their absolute values',maximum_native_position_change_m:changed,detected:changed>1e-6};assert(signedWeightControl.detected,'native signedweight negative control not detected');
  }
 }
 frames.push({time_s:time,native_encoded_time_s:actualTimes[k],global_body_frame_matrices:meshes[0].skeleton.bones.map(b=>{const e=b.matrixWorld.elements;return Array.from({length:4},(_,r)=>Array.from({length:4},(_,c)=>e[c*4+r]));}),morph_weights:[...meshes[1].morphTargetInfluences]});
}
fs.closeSync(fd);assert(negative>0&&minWeight<-.2,'signed morph weights not reproduced');
assert(signedWeightControl?.detected);const result={status:'ACTUAL_GLTFLOADER_SKELETONUTILS_NATIVE_MIXER_READBACK_NOT_YET_PHYSICAL_ACCEPTANCE',glb_sha256:sha(bytes),glb_bytes:bytes.length,frames,mesh_vertex_counts:meshes.map(m=>m.geometry.attributes.position.count),negative_weight_observations:negative,weight_range:[minWeight,maxWeight],signed_weight_negative_control:signedWeightControl,all_finite:minimumFinite,positions:'Native SkinnedMesh.getVertexPosition after GLTFLoader/SkeletonUtils/nativeMixer',normals:'CPU mirrors morphnormal+Float32 bone uniform skin shader; no renderedGPU acceptance',cloned_skeleton_identity_isolated:true,maximum_RSS_bytes:process.resourceUsage().maxRSS*1024,seconds:(performance.now()-start)/1000};save('ACTUAL-NATIVE-MIXER-READBACK.json',result);console.log(JSON.stringify({...result,frames:result.frames.length}));assert(result.maximum_RSS_bytes<=536870912);assert(minimumFinite);
