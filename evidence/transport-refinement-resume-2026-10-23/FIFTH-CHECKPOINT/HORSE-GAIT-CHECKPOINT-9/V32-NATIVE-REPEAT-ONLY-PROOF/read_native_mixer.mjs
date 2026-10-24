// Source-only native portable-loader readback. No renderer, app or traffic.
import fs from 'node:fs';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import * as T from '/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/vendor/three.module.js';
import {GLTFLoader} from '/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/vendor/GLTFLoader.mjs';
import {clone} from '/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/vendor/SkeletonUtils.mjs';
const D=new URL('.',import.meta.url),sha=b=>crypto.createHash('sha256').update(b).digest('hex'),read=n=>fs.readFileSync(new URL(n,D)),save=(n,o)=>fs.writeFileSync(new URL(n,D),JSON.stringify(o,null,2)+'\n');
const start=performance.now(),bytes=read('creeping-015mps-PORTABLE-STUDY-NOT-APP.glb'),jsonLength=bytes.readUInt32LE(12),j=JSON.parse(bytes.subarray(20,20+jsonLength));
assert.equal(sha(bytes),'8fc20cf20549d9588c56202d93315dc9f718531fc7a285de2208ce4e36ba9a7b');
const loader=new GLTFLoader();loader.register(()=>({name:'CPU_NO_TEXTURE_LOAD',loadTexture:()=>Promise.resolve(null)}));
const g=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
const scene=clone(g.scene),byName=new Map();scene.traverse(o=>{if(o.isSkinnedMesh){assert(!byName.has(o.name));byName.set(o.name,o);}});
const originals=[];g.scene.traverse(o=>{if(o.isSkinnedMesh)originals.push(o);});
const meshes=[26,27,28].map(ni=>{const original=originals.find(m=>g.parser.associations.get(m)?.nodes===ni);assert(original,`missing node${ni}`);const m=byName.get(original.name);assert(m&&m!==original&&m.skeleton.bones[0]!==original.skeleton.bones[0]);return m;});
const clip=g.animations.find(a=>a.name==='RECONSTRUCTED_CREEPING_015MPS_STUDY_NOT_NATURAL_WALK');assert(clip);const mixer=new T.AnimationMixer(scene),action=mixer.clipAction(clip);action.setLoop(T.LoopRepeat,Infinity);action.clampWhenFinished=false;action.play();
const encodedTimes=clip.tracks.find(t=>t.times.length===129).times,actualTimes=[];for(let k=0;k<128;k++)actualTimes.push(encodedTimes[k],(encodedTimes[k]+encodedTimes[k+1])/2);actualTimes.push(encodedTimes[128]);for(const epsilon of[.001,.0001])actualTimes.push(clip.duration-epsilon,clip.duration+epsilon,epsilon,2*clip.duration-epsilon);const snapshots=new Map();
const fd=fs.openSync(new URL('ACTUAL-NATIVE-POSITIONS-AND-SHADER-NORMALS.f64',D),'w'),frames=[],p=new T.Vector3(),n=new T.Vector3(),tmp=new T.Vector3();let negative=0,minWeight=0,maxWeight=0,minimumFinite=true,signedWeightControl=null;
for(let k=0;k<actualTimes.length;k++){
 const snapshot=[];
 const time=k<=256?1.6*k/256:actualTimes[k]/clip.duration*1.6;mixer.setTime(actualTimes[k]);scene.updateMatrixWorld(true);for(const m of meshes)m.skeleton.update();
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
  fs.writeSync(fd,Buffer.from(out.buffer));if(k===0||k>=256)snapshot.push(out);
  if(m===meshes[1]&&!signedWeightControl&&weights.some(w=>w<-.2)){
   const saved=[...weights];for(let wi=0;wi<weights.length;wi++)weights[wi]=Math.abs(weights[wi]);let changed=0;
   for(let vi=0;vi<a.position.count;vi++){m.getVertexPosition(vi,p).applyMatrix4(m.matrixWorld);changed=Math.max(changed,Math.hypot(p.x-out[vi*6],p.y-out[vi*6+1],p.z-out[vi*6+2]));}
   for(let wi=0;wi<weights.length;wi++)weights[wi]=saved[wi];signedWeightControl={time_s:time,corruption:'replace all signed PCA influences by their absolute values',maximum_native_position_change_m:changed,detected:changed>1e-6};assert(signedWeightControl.detected,'native signedweight negative control not detected');
  }
 }
 if(k===0||k>=256)snapshots.set(k,snapshot);
 frames.push({time_s:time,native_encoded_time_s:actualTimes[k],global_body_frame_matrices:meshes[0].skeleton.bones.map(b=>{const e=b.matrixWorld.elements;return Array.from({length:4},(_,r)=>Array.from({length:4},(_,c)=>e[c*4+r]));}),morph_weights:[...meshes[1].morphTargetInfluences]});
}
fs.closeSync(fd);
function compare(ia,ib){let position=0,normal=0;const aa=snapshots.get(ia),bb=snapshots.get(ib);for(let mi=0;mi<3;mi++)for(let i=0;i<aa[mi].length;i+=6){position=Math.max(position,Math.hypot(aa[mi][i]-bb[mi][i],aa[mi][i+1]-bb[mi][i+1],aa[mi][i+2]-bb[mi][i+2]));normal=Math.max(normal,Math.hypot(aa[mi][i+3]-bb[mi][i+3],aa[mi][i+4]-bb[mi][i+4],aa[mi][i+5]-bb[mi][i+5]));}return{maximum_position_m:position,maximum_shader_normal_vector:normal};}
const wrap=[];for(let wi=0;wi<2;wi++){const epsilon=[.001,.0001][wi],minus=257+4*wi,plus=minus+1,phasePlus=minus+2,previousMinus=minus+3;let curvature=0;for(let mi=0;mi<3;mi++){const a=snapshots.get(minus)[mi],b=snapshots.get(plus)[mi],zero=snapshots.get(0)[mi];for(let i=0;i<a.length;i+=6)curvature=Math.max(curvature,Math.hypot(a[i]+b[i]-2*zero[i],a[i+1]+b[i+1]-2*zero[i+1],a[i+2]+b[i+2]-2*zero[i+2]));}wrap.push({epsilon_s:epsilon,matched_after_wrap_vs_phase_epsilon:compare(plus,phasePlus),matched_before_wrap_vs_previous_cycle:compare(minus,previousMinus),smooth_motion_across_2epsilon:compare(plus,minus),minus_to_zero:compare(minus,0),zero_to_plus:compare(0,plus),symmetric_curvature_residual_m:curvature});}
save('ACTUAL-NATIVE-LOOPREPEAT-WRAP-PROOF.json',{scope:'Native LoopRepeat only; originalLoopOnce clampFAIL and upstreamSVDmemoryFAIL remain unqualified',clip_duration_s:clip.duration,authored_duration_s:1.6,exact_boundary_phase_comparison:compare(0,256),wrap_samples:wrap,normalization_wrapper:false,stop_or_clamp_transition_qualified:false,natural_gait_accepted:false});
assert(negative>0&&minWeight<-.2,'signed morph weights not reproduced');
assert(signedWeightControl?.detected);const result={status:'ACTUAL_GLTFLOADER_SKELETONUTILS_NATIVE_MIXER_READBACK_NOT_YET_PHYSICAL_ACCEPTANCE',glb_sha256:sha(bytes),glb_bytes:bytes.length,frames,mesh_vertex_counts:meshes.map(m=>m.geometry.attributes.position.count),negative_weight_observations:negative,weight_range:[minWeight,maxWeight],signed_weight_negative_control:signedWeightControl,all_finite:minimumFinite,positions:'Native SkinnedMesh.getVertexPosition after GLTFLoader/SkeletonUtils/nativeMixer',normals:'CPU mirrors morphnormal+Float32 bone uniform skin shader; no renderedGPU acceptance',cloned_skeleton_identity_isolated:true,maximum_RSS_bytes:process.resourceUsage().maxRSS*1024,seconds:(performance.now()-start)/1000};save('ACTUAL-NATIVE-MIXER-READBACK.json',result);console.log(JSON.stringify({...result,frames:result.frames.length}));assert(result.maximum_RSS_bytes<=536870912);assert(minimumFinite);
