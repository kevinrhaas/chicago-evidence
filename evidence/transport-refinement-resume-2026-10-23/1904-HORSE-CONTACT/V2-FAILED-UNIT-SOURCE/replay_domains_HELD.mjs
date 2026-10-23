// HELD V2: separate reference/domain/host storage-precision CPU diagnostics.
// f64 arithmetic over explicitly F32-stored shader input matrices is NOT GPU
// execution, camera/modelView/projection precision, or fresh scene-graph proof.
import assert from 'node:assert/strict';
export function replayDomains(T,{doc,accessor,reference,loaded,best,row,provider,region}) {
 const temps=[];
 try {
  assert.equal(loaded.status,'LOADED_STANDING65_KEYS64_MIDPOINTS_PASS_ONLY');
  assert.equal(loaded.key_count,65);assert.equal(loaded.midpoint_count,64);assert.equal(loaded.poses.length,129);assert.equal(loaded.failures.length,0);
  const frames=loaded.poses;assert.equal(frames[0].time,0);assert.equal(frames[0].key,0);assert.equal(frames.at(-1).time,12);
  const lim=loaded.original_physical_limits;assert.equal(lim.stance_patch_drift_m,1e-5);
  const meshes=doc.meshes.map(m=>{
   const pr=m.primitives[0],pos=accessor(pr.attributes.POSITION),j=accessor(pr.attributes.JOINTS_0),raw=accessor(pr.attributes.WEIGHTS_0);
   const geo=new T.BufferGeometry();geo.setAttribute('skinWeight',new T.Float32BufferAttribute(raw.slice(),4));
   const temp=new T.SkinnedMesh(geo,new T.MeshBasicMaterial());temps.push(temp);temp.normalizeSkinWeights();
   return{pos,j,w:geo.attributes.skinWeight.array,index:accessor(pr.indices)};
  });
  const body=meshes[1],patches={},additional={},es={fore_l:10,fore_r:15,hind_l:20,hind_r:25};
  const expectedCounts={fore_l:59,fore_r:59,hind_l:13,hind_r:10};
  for(const[label,p]of Object.entries(reference.contacts)){
   patches[label]=new Set(p.source_triangle_ids.flatMap(t=>[body.index[3*t],body.index[3*t+1],body.index[3*t+2]]));
   assert.equal(patches[label].size,expectedCounts[label]);additional[label]=new Set();
  }
  for(let i=0;i<body.pos.length/3;i++)for(const[label,e]of Object.entries(es)){
   const own=[0,1,2,3].every(k=>body.w[4*i+k]===0||body.j[4*i+k]===e)&&[0,1,2,3].some(k=>body.w[4*i+k]>0);
   if(own&&!patches[label].has(i))additional[label].add(i);
  }
  const ib=accessor(doc.skins[0].inverseBindMatrices),inverses=Array.from({length:26},(_,i)=>new T.Matrix4().fromArray(ib,16*i));
  const f32m=m=>new T.Matrix4().fromArray(new Float32Array(m.elements));
  const identity=new T.Matrix4(),yaw=Math.PI-row.bearing_deg*Math.PI/180;
  // Outer placement = translation*Yheading; support is inside it; canonical
  // metres/originzero, source mesh model/bind transforms were identity.
  const H=new T.Matrix4().makeRotationY(yaw).setPosition(row.at_local_enu_m[0],best.base,-row.at_local_enu_m[1])
   .multiply(new T.Matrix4().makeRotationFromQuaternion(new T.Quaternion().fromArray(best.q)));
  const Hinv=H.clone().invert();
  // WebGL uploads each Matrix4 independently through Float32Array: inversion
  // is performed BEFORE uniform-storage cast, never inverse(Float32(H)).
  const modelUniform=f32m(H),inverseUniform=f32m(Hinv);
  const palette=(frame,host)=>frame.world_matrices.map((g,i)=>f32m(new T.Matrix4().multiplyMatrices(host,new T.Matrix4().fromArray(g)).multiply(inverses[i])));
  function shade(mesh,id,bones,bindInverse,model){
   const input=new T.Vector4(mesh.pos[3*id],mesh.pos[3*id+1],mesh.pos[3*id+2],1); // bindMatrix=I
   const weighted=new T.Vector4(0,0,0,0);
   for(let k=0;k<4;k++){const mass=mesh.w[4*id+k];if(mass)weighted.addScaledVector(input.clone().applyMatrix4(bones[mesh.j[4*id+k]]),mass);}
   const local=weighted.applyMatrix4(bindInverse); // retain weighted homogeneous W; NO Vector3 division
   const world=new T.Vector4(local.x,local.y,local.z,1).applyMatrix4(model); // native .xyz then reset W=1
   return new T.Vector3(world.x,world.y,world.z);
  }
  const idealWorld=p=>{const v=new T.Vector4(p.x,p.y,p.z,1).applyMatrix4(H);return new T.Vector3(v.x,v.y,v.z);};
  const groundAt=p=>{const g=provider.heightAt(p.x,-p.z,row.ground_record_id,region.id);assert(Number.isFinite(g),'No exact named top triangle for hosted point');return g;};
  const canonical0=palette(frames[0],identity),hosted0=palette(frames[0],H);
  const c0=new Map(),h0=new Map();
  let canonicalNeutral=0;
  for(let mi=0;mi<meshes.length;mi++){
   assert.equal(reference.rest_points_per_mesh[mi].length,meshes[mi].pos.length/3);
   for(let i=0;i<meshes[mi].pos.length/3;i++){
    const p=shade(meshes[mi],i,canonical0,identity,identity),target=new T.Vector3().fromArray(reference.rest_points_per_mesh[mi][i]);
    canonicalNeutral=Math.max(canonicalNeutral,p.distanceTo(target));if(mi===1)c0.set(i,p);
   }
  }
  for(const groups of[patches,additional])for(const ids of Object.values(groups))for(const i of ids)if(!h0.has(i))h0.set(i,shade(body,i,hosted0,inverseUniform,modelUniform));
  const metrics={
   canonical_original_annotated_patch:{domain_counts:expectedCounts,baseline:'EXACT_PHASE_A_NEUTRAL_SKINNED_REFERENCE',limit_m:lim.stance_patch_drift_m,maximum_error_m:0},
   canonical_additional_e_only_body_vertices:{domain_counts:Object.fromEntries(Object.entries(additional).map(([k,v])=>[k,v.size])),baseline:'OWN_ACCEPTED_KEY0_NORMALIZED_B479_CANONICAL_SKIN',limit_m:lim.stance_patch_drift_m,maximum_error_m:0,original_patch_excluded:true,complete_anatomical_hoof_not_claimed:true},
   hosted_original_annotated_patch:{temporal_baseline:'SAME_HOSTED_KEY0_STORAGE_PRECISION_REPLAY',maximum_temporal_drift_m:0,absolute_baseline:'IDEAL_H_DOUBLE_TIMES_PHASE_A_NEUTRAL_REFERENCE',maximum_absolute_error_m:0,maximum_neutral_absolute_offset_m:0,temporal_limit_m:1e-5,informational_ideal_world_precision_screen_m:1e-5},
   hosted_additional_e_only_body_vertices:{temporal_baseline:'SAME_HOSTED_KEY0_STORAGE_PRECISION_REPLAY',maximum_temporal_drift_m:0,absolute_baseline:'IDEAL_H_DOUBLE_TIMES_OWN_KEY0_CANONICAL_B479_SKIN',maximum_absolute_error_m:0,maximum_neutral_absolute_offset_m:0,temporal_limit_m:1e-5,informational_ideal_world_precision_screen_m:1e-5,original_patch_excluded:true},
   hosted_actual_top_ground:{maximum_per_hoof_minimum_gap_m:-Infinity,minimum_vertex_clearance_m:Infinity,maximum_per_hoof_minimum_gap_limit_m:.001,minimum_vertex_clearance_limit_m:-1e-5},
  };
  const rows=[];
  for(const frame of frames){
   assert.equal(frame.world_matrices.length,26);const can=palette(frame,identity),host=palette(frame,H),perHoof={};
   for(const[label,patch]of Object.entries(patches)){
    let minimum=Infinity;
    for(const[kind,ids]of[['original',patch],['additional',additional[label]]])for(const i of ids){
     const p=shade(body,i,can,identity,identity),world=shade(body,i,host,inverseUniform,modelUniform);
     const target=kind==='original'?new T.Vector3().fromArray(reference.rest_points_per_mesh[1][i]):c0.get(i);
     const cmetric=kind==='original'?metrics.canonical_original_annotated_patch:metrics.canonical_additional_e_only_body_vertices;
     const hmetric=kind==='original'?metrics.hosted_original_annotated_patch:metrics.hosted_additional_e_only_body_vertices;
     cmetric.maximum_error_m=Math.max(cmetric.maximum_error_m,p.distanceTo(target));
     hmetric.maximum_temporal_drift_m=Math.max(hmetric.maximum_temporal_drift_m,world.distanceTo(h0.get(i)));
     hmetric.maximum_absolute_error_m=Math.max(hmetric.maximum_absolute_error_m,world.distanceTo(idealWorld(target)));
     hmetric.maximum_neutral_absolute_offset_m=Math.max(hmetric.maximum_neutral_absolute_offset_m,h0.get(i).distanceTo(idealWorld(target)));
     const gap=world.y-groundAt(world);minimum=Math.min(minimum,gap);metrics.hosted_actual_top_ground.minimum_vertex_clearance_m=Math.min(metrics.hosted_actual_top_ground.minimum_vertex_clearance_m,gap);
    }
    perHoof[label]=minimum;metrics.hosted_actual_top_ground.maximum_per_hoof_minimum_gap_m=Math.max(metrics.hosted_actual_top_ground.maximum_per_hoof_minimum_gap_m,minimum);
   }rows.push({time:frame.time,key:frame.key,minimum_gap_by_union_of_separately_reported_domains_m:perHoof});
  }
  metrics.canonical_full_key0_neutral={baseline:'EXACT_PHASE_A_NEUTRAL_SKINNED_REFERENCE',maximum_error_m:canonicalNeutral,original_limit_m:1e-6,pass:canonicalNeutral<=1e-6};
  for(const m of[metrics.canonical_original_annotated_patch,metrics.canonical_additional_e_only_body_vertices])m.pass=m.maximum_error_m<=m.limit_m;
  for(const m of[metrics.hosted_original_annotated_patch,metrics.hosted_additional_e_only_body_vertices]){m.temporal_pass=m.maximum_temporal_drift_m<=m.temporal_limit_m;m.informational_ideal_world_precision_screen_pass=m.maximum_absolute_error_m<=m.informational_ideal_world_precision_screen_m;}
  const g=metrics.hosted_actual_top_ground;g.pass=g.maximum_per_hoof_minimum_gap_m<=g.maximum_per_hoof_minimum_gap_limit_m&&g.minimum_vertex_clearance_m>=g.minimum_vertex_clearance_limit_m;
  // Independent synthetic precision controls, not altered horse inputs.
  const testH=new T.Matrix4().makeTranslation(2**24,0,0),testG=new T.Matrix4().makeTranslation(1,0,0);
  const ordered=f32m(testH.clone().multiply(testG)).elements[12],wrong=testH.elements[12]+f32m(testG).elements[12];
  assert(Math.abs(ordered-wrong)>.001,'Matrix-storage order control not detected');
  const testMesh={pos:Float32Array.of(4,0,0),j:Uint16Array.of(0,0,0,0),w:Float32Array.of(.75,0,0,0)};
  const smallH=new T.Matrix4().makeTranslation(1024,0,0),testPoint=shade(testMesh,0,[smallH],smallH.clone().invert(),smallH);
  assert.equal(testPoint.x,1027,'WeightedW/drop/reset shader control failed');assert(Math.abs(testPoint.x-1028)>.001);
  const pass=metrics.canonical_full_key0_neutral.pass&&metrics.canonical_original_annotated_patch.pass&&metrics.canonical_additional_e_only_body_vertices.pass
   &&metrics.hosted_original_annotated_patch.temporal_pass
   &&metrics.hosted_additional_e_only_body_vertices.temporal_pass&&g.pass;
  return{status:pass?'V2_CPU_REFERENCE_DOMAIN_HOST_CONTACT_GUARDS_PASS_ONLY':'V2_CPU_REFERENCE_DOMAIN_OR_HOST_CONTACT_GUARD_FAIL',pass,samples:129,metrics,poses:rows,
   informational_ideal_world_precision_screen_affects_pass:false,
   informational_ideal_world_precision_screen_pass:metrics.hosted_original_annotated_patch.informational_ideal_world_precision_screen_pass&&metrics.hosted_additional_e_only_body_vertices.informational_ideal_world_precision_screen_pass,
   arithmetic:{bone_storage:'Float32(Hdouble * recordedCanonicalGdouble * serializedIBfloat)',model_uniform:'Float32(Hdouble)',bind_inverse_uniform:'Float32(inverse(Hdouble)) independently',bind_matrix:'Identity, as accepted canonical source',weighted_vertex:'Vector4 including weighted W through bindInverse; .xyz/dropW/reset1 before modelMatrix',multiply_add:'CPU_FLOAT64_OVER_FLOAT32_STORED_INPUTS_NOT_GPU_FLOAT_ARITHMETIC',scenegraph_association:'H*recordedCanonicalG is a replay model; fresh hosted scenegraph association unverified'},
   negative_controls:{noncommuting_host_float32_storage_order_detected:true,weighted_W_preservation_and_reset_detected:true},
   unchanged_canonical129_proof_replaced:false,host_GPU_or_app_or_camera_or_photo_proof:false,normal_activation:false};
 }finally{for(const mesh of temps){mesh.geometry.dispose();mesh.material.dispose();}}
}
