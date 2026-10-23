// HELD: one b4791904 static fit + immutable loaded-matrix contact replay only.
import { APP, OUT, HERE, binding, read, reads } from './setup_HELD.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const T=await import('three');
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=p=>JSON.parse(read(p));
const row=json(binding.paths.candidate_manifest).scenes['1904'][0];
const scene=json(binding.paths.scene),spec=json(binding.paths.sidecar);
const report={status:'B479_SINGLE_SITE_INCOMPLETE',world_qualified:false,normal_activation:false,
  runtime_asset_sha256:binding.asset_sha256,scene_id:'1904',target_date:'1904-07-01',
  at_local_enu_m:[1397.5,-3221.2],bearing_deg:178.99,problems:[]};
let layer=null;
const started=performance.now();
try {
 assert.equal(row.enabled,false);assert.equal(row.animation.enabled,false);
 assert.deepEqual(row.at_local_enu_m,[1397.5,-3221.2]);assert.equal(row.bearing_deg,178.99);
 assert.equal(row.ground_record_id,'prairie_18_20');assert.equal(scene.id,'1904');assert.equal(scene.target_date,'1904-07-01');
 assert.equal(spec.runtime_asset.sha256,binding.asset_sha256);assert.equal(spec.runtime_scale_m_per_unit,1);assert.deepEqual(spec.runtime_origin_m,[0,0,0]);
 assert.equal(spec.proposed_static_support_pose.maximum_total_tilt_deg,2);
 const raw=read(binding.paths.asset);assert.equal(raw.length,3783600);assert.equal(sha(raw),binding.asset_sha256);
 const ab=raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength);
 const {validatePlantedStandingHeader}=await import('./modules/standing-horse-planted-idle.js');
 const doc=validatePlantedStandingHeader(ab,spec),view=new DataView(ab),bin=28+view.getUint32(12,true);
 assert.equal(view.getUint32(bin-4,true),0x004e4942);
 const dims={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16},types={5123:Uint16Array,5125:Uint32Array,5126:Float32Array};
 const denseType=(a,v)=>{const C=types[a.componentType];assert(C&&dims[a.type]&&!a.normalized&&!a.sparse,'Expected plain supported accessor');assert(v.byteStride===undefined||v.byteStride===dims[a.type]*C.BYTES_PER_ELEMENT,'Interleaved or mismatched accessor stride');return C;};
 const positionDescriptor=doc.accessors[0],positionView=doc.bufferViews[positionDescriptor.bufferView];
 assert.equal(denseType(positionDescriptor,{...positionView,byteStride:undefined}),Float32Array);
 assert.equal(denseType(positionDescriptor,{...positionView,byteStride:12}),Float32Array);
 assert.throws(()=>denseType(positionDescriptor,{...positionView,byteStride:16}),/Interleaved or mismatched/);
 assert.throws(()=>denseType({...positionDescriptor,normalized:true},positionView),/plain supported/);
 assert.throws(()=>denseType({...positionDescriptor,sparse:{count:1}},positionView),/plain supported/);
 const uvDescriptor=doc.accessors[10],uvView=doc.bufferViews[uvDescriptor.bufferView];
 assert.equal(denseType(uvDescriptor,{...uvView,byteStride:8}),Float32Array);
 assert.throws(()=>denseType(uvDescriptor,{...uvView,byteStride:12}),/Interleaved or mismatched/);
 report.packed_stride_decoder_controls={implicit_packed_accepted:true,explicit_position12_and_uv8_accepted:true,position16_and_uv12_rejected:true,normalized_and_sparse_rejected:true};
 const accessor=id=>{const a=doc.accessors[id],v=doc.bufferViews[a.bufferView],C=denseType(a,v);return new C(ab,bin+(v.byteOffset??0)+(a.byteOffset??0),a.count*dims[a.type]);};
 const ref=json(binding.paths.reference),receipt=json(binding.paths.export_receipt);
 assert.equal(receipt.output_sha256,binding.asset_sha256);assert.equal(receipt.readback_reference_sha256,sha(read(binding.paths.reference)));
 // Correct raw-geometry proof: compare byte-identical semantic streams to
 // immutable03a1 source, not to PhaseA's neutral SKINNED point reference.
 const original=read(binding.paths.original_rig);
 assert.equal(sha(original),receipt.source_rig_sha256);assert.equal(receipt.source_rig_sha256,'03a1f747189ee2457f0fc3dc9720b1d3d288e36c32b7171b5a9976afb7e63c36');
 const origAB=original.buffer.slice(original.byteOffset,original.byteOffset+original.byteLength),ov=new DataView(origAB),origDoc=JSON.parse(new TextDecoder().decode(new Uint8Array(origAB,20,ov.getUint32(12,true)))),origBin=28+ov.getUint32(12,true);
 assert.equal(ov.getUint32(origBin-4,true),0x004e4942);
 const originalAccessor=id=>{const a=origDoc.accessors[id],v=origDoc.bufferViews[a.bufferView],C=denseType(a,v);return new C(origAB,origBin+(v.byteOffset??0)+(a.byteOffset??0),a.count*dims[a.type]);};
 let rawSemanticPairs=0;
 const sameRaw=(candidateId,originalId)=>{
  const a=doc.accessors[candidateId],b=origDoc.accessors[originalId];
  assert.equal(a.componentType,b.componentType);assert.equal(a.type,b.type);assert.equal(a.count,b.count);
  const aa=accessor(candidateId),bb=originalAccessor(originalId);
  assert.deepEqual(new Uint8Array(aa.buffer,aa.byteOffset,aa.byteLength),new Uint8Array(bb.buffer,bb.byteOffset,bb.byteLength));rawSemanticPairs++;
 };
 for(let mi=0;mi<3;mi++){
  const node=doc.nodes[26+mi];assert.equal(node.mesh,mi);assert(doc.scenes[doc.scene??0].nodes.includes(26+mi));
  for(const key of['matrix','translation','rotation','scale'])assert.equal(node[key],undefined);
  const candidate=doc.meshes[mi].primitives[0],source=origDoc.meshes[mi].primitives[0];
  for(const semantic of['POSITION','NORMAL','TEXCOORD_0'])sameRaw(candidate.attributes[semantic],source.attributes[semantic]);sameRaw(candidate.indices,source.indices);
 }
 sameRaw(doc.skins[0].inverseBindMatrices,origDoc.skins[0].inverseBindMatrices);
 for(const patch of Object.values(spec.contacts))assert(new T.Vector3().fromArray(ref.rest_points_per_mesh[1][patch.minimum_vertex_id]).distanceTo(new T.Vector3().fromArray(patch.minimum_vertex_canonical_m))<1e-4,'Original CPU-neutral minimum-anchor reference mismatch');
 Object.assign(report,{raw_geometry_lineage:{source_rig_sha256:receipt.source_rig_sha256,byte_identical_semantic_stream_pairs:rawSemanticPairs,CPU_neutral_reference_is_not_raw_POSITION:true}});
 const {Heightfield}=await import(pathToFileURL(APP+'/renderers/web/js/terrain.js'));
 const meta=json(binding.paths.heightfield_meta),rawHeight=read(binding.paths.heightfield_bin);
 const hf=new Heightfield().adopt(meta,rawHeight.buffer.slice(rawHeight.byteOffset,rawHeight.byteOffset+rawHeight.byteLength));
 const terrain={surfaceHeight:(e,n)=>hf.sample(e,n),setGroundCut:()=>{},protectGroundUnder:()=>{},grid:{cellM:hf.cellM},inBounds:(e,n)=>hf.contains(e,n)};
 const {createStreetGrid}=await import('./modules/street-grid.js');
 const region=json(binding.paths.candidate_scene).static_support_regions[0];
 layer=await createStreetGrid({dataBase:pathToFileURL(APP+'/data/'),assetBase:null,sceneId:'1904',targetDate:scene.target_date,terrain,supportRegions:[region],problems:report.problems});
 const provider=layer.drawnStaticSupport,snapshot=provider?.snapshot(row.ground_record_id,region.id);
 assert(snapshot&&snapshot.triangles<=32&&snapshot.bytes<=4096,'No bounded named carriageway support');
 const triangles=provider.copyTriangles(row.ground_record_id,region.id);assert(triangles?.length&&triangles.byteLength<=4096);
 const bytes=new ArrayBuffer(triangles.byteLength),dv=new DataView(bytes);for(let i=0;i<triangles.length;i++)dv.setFloat64(i*8,triangles[i],true);
 const providerSHA=sha(new Uint8Array(bytes));
 fs.writeFileSync(path.join(OUT,'DRAWN-TRIANGLES.json'),JSON.stringify({snapshot,sha256_f64le_world_xyz:providerSHA,region,triangles_world_xyz:Array.from(triangles)},null,2)+'\n');
 const yaw=Math.PI-row.bearing_deg*Math.PI/180,co=Math.cos(yaw),si=Math.sin(yaw);
 let evaluations=0;
 const height=(p,q)=>{const v=p.clone().applyQuaternion(q);const e=row.at_local_enu_m[0]+co*v.x+si*v.z,n=row.at_local_enu_m[1]+si*v.x-co*v.z;const ground=provider.heightAt(e,n,row.ground_record_id,region.id);assert(Number.isFinite(ground),'No exact named drawn triangle at contact');return{y:v.y,ground};};
 const evaluate=(rx,rz)=>{
  assert(++evaluations<=1024,'Finite fit evaluation cap');const q=new T.Quaternion().setFromEuler(new T.Euler(rx,0,rz,'XYZ'));
  const tilt=new T.Vector3(0,1,0).applyQuaternion(q).angleTo(new T.Vector3(0,1,0))*180/Math.PI;if(tilt>2)return{score:Infinity};
  const patches=Object.fromEntries(Object.entries(spec.contacts).map(([k,p])=>[k,p.samples_m.map(v=>height(new T.Vector3().fromArray(v),q))]));
  const flat=Object.values(patches).flat(),base=Math.max(...flat.map(p=>p.ground-p.y));
  const hoof=Object.fromEntries(Object.entries(patches).map(([k,ps])=>[k,Math.min(...ps.map(p=>base+p.y-p.ground))]));
  const slab=Object.fromEntries(Object.entries(spec.contacts).map(([k,p])=>[k,Math.min(...p.equal_10mm_slab_samples_m.map(v=>{const p=height(new T.Vector3().fromArray(v),q);return base+p.y-p.ground;}))]));
  const minSamples=Math.min(...flat.map(p=>base+p.y-p.ground));
  return{rx,rz,q:q.toArray(),tilt,base,hoof,slab,minSamples,score:Math.max(...Object.values(hoof),.001-.00001-Math.min(...Object.values(slab)))};
 };
 const seed=new T.Euler().setFromQuaternion(new T.Quaternion().fromArray(spec.proposed_static_support_pose.local_quaternion_xyzw));
 let best=[evaluate(0,0),evaluate(seed.x,seed.z)].sort((a,b)=>a.score-b.score)[0];
 const initial=structuredClone(best);
 // Exact existing finite canonical search policy: one site, one fixed search,
 // no changed seed/step/limit rerun on failure. It is not an era/model sweep.
 for(let step=.5*Math.PI/180;step>1e-8;step/=2)for(let repeat=0;repeat<4;repeat++){
  let next=best;for(const dx of[-1,0,1])for(const dz of[-1,0,1]){const v=evaluate(best.rx+dx*step,best.rz+dz*step);if(v.score<next.score)next=v;}
  if(next===best)break;best=next;
 }
 const staticPass=Object.values(best.hoof).every(v=>v<=.001)&&best.minSamples>=-1e-5&&Object.values(best.slab).every(v=>v>=-1e-5);
 assert(staticPass,'b479 static sampled support FAIL; no refit/retry');
 const fit={schema:'standing_horse_drawn_support_fit_b479_v1',status:'SOURCE_CPU_FIT_ONLY',
  scene_id:'1904',target_date:scene.target_date,row_id:row.id,at_local_enu_m:row.at_local_enu_m,bearing_deg:row.bearing_deg,
  record_id:row.ground_record_id,region_id:region.id,surface_kind:'carriageway_triangle',bounds_enu_m:region.bounds_enu_m,
  runtime_asset_sha256:binding.asset_sha256,provider_triangle_sha256:providerSHA,support_quaternion_xyzw:best.q,
  limits:{maximum_total_tilt_deg:2,maximum_per_hoof_minimum_gap_m:.001,minimum_sample_clearance_m:-1e-5},
  measurements:best,solver_evaluations:evaluations,initial_seed:initial,world_qualified:false,normal_activation:false};
 fs.writeFileSync(path.join(OUT,'FIT.json'),JSON.stringify(fit,null,2)+'\n');
 const loaded=json(binding.paths.loaded129);assert.equal(loaded.walking_enabled,false);
 const {replayDomains}=await import('./replay_domains_HELD.mjs');
 const replay=replayDomains(T,{doc,accessor,reference:ref,loaded,best,row,provider,region});
 const contactPass=replay.pass;
 const liftedReject=Math.max(...Object.values(best.hoof))+.003>.001,penetrationReject=best.minSamples-.00002<-1e-5,tiltReject=evaluate(3*Math.PI/180,0).score===Infinity;
 assert(liftedReject&&penetrationReject&&tiltReject,'Physical corruption control not detected');
 Object.assign(report,{status:contactPass?'B479_V2_CURRENT_TOP_REFERENCE_DOMAIN_HOST_REPLAY_PASS_ONLY':'B479_V2_REFERENCE_DOMAIN_OR_HOST_REPLAY_GUARD_FAIL',fit,
  V2_separate_replay_domains:replay,source_loaded129_sha256:binding.inputs[binding.paths.loaded129].sha256,
  prior_V1_source_review_sha256:binding.inputs[binding.paths.V1_review].sha256,
  geometry_source_raw_bytes_exact:true,CPU_neutral_is_separate_skinned_reference:true,model_unchanged:true,
  negative_controls:{three_mm_whole_root_lift_rejected:liftedReject,twenty_micrometre_penetration_rejected:penetrationReject,three_degree_tilt_rejected:tiltReject,...replay.negative_controls},
  qualification_scope:'Fresh exact named TOP static fit; unchanged canonical CPU-reference guards plus separately named additional-domain and hosted shader-input storage-precision CPU replay. Not freshGLTFLoader/Mixer, freshhostedscenegraph, GPUfloat/camera/rendering, app/allbodyclearance/photo or activation. A newhostedguardFAIL is not an actual1835product or oldcanonical129 failure.'});
}catch(error){Object.assign(report,{status:'B479_SINGLE_SITE_FAIL_NO_RETRY',error:String(error.stack??error)});}
finally{
 try{layer?.dispose();}catch(error){report.disposal_error=String(error);report.status='B479_DISPOSAL_FAIL';}
 report.read_inputs=Object.fromEntries([...reads].map(([p,b])=>[p,sha(b)]));
 try {
  report.all_bound_inputs_unchanged=Object.entries(binding.inputs).every(([p,pin])=>sha(fs.readFileSync(p))===pin.sha256);
  report.all_bound_sources_unchanged=Object.entries(binding.source_sha256).every(([p,h])=>sha(fs.readFileSync(path.join(HERE,p)))===h);
  report.inputs_unchanged=report.all_bound_inputs_unchanged&&report.all_bound_sources_unchanged;
 }catch(error){report.inputs_unchanged=false;report.pin_recheck_error=String(error);}
 report.elapsed_ms=performance.now()-started;
 if(!report.inputs_unchanged)report.status='SOURCE_DRIFT_FAIL';
 fs.writeFileSync(path.join(OUT,'READBACK.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}
if(report.status!=='B479_V2_CURRENT_TOP_REFERENCE_DOMAIN_HOST_REPLAY_PASS_ONLY')process.exitCode=2;
