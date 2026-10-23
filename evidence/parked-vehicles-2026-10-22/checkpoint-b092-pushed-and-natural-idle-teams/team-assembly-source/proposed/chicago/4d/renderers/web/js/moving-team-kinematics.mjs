// SPDX-License-Identifier: GPL-3.0-or-later
// Source-only T2795 diagnostic. No fetch, scene mount, new rig, authored gear or live activation.
const finite=(x,name)=>{if(!Number.isFinite(x))throw Error('Finite '+name+' required');return x;};
const wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
export const rotateY=(p,a)=>[Math.cos(a)*p[0]+Math.sin(a)*p[2],p[1],-Math.sin(a)*p[0]+Math.cos(a)*p[2]];
const add=(a,b)=>a.map((x,i)=>x+b[i]);
export function solveTonguePitch(pivotY,length,targetY){
 [pivotY,length,targetY].forEach((x,i)=>finite(x,'tongue parameter '+i));if(length<=0||Math.abs(targetY-pivotY)>=length)throw Error('Unreachable working-height hypothesis');
 return -Math.asin((targetY-pivotY)/length); // Rx maps +Z to negativeY for positive pitch.
}
export function createW01TeamKinematics(contract){
 if(contract.scene!=='1835'||contract.live_activation_allowed!==false)throw Error('Explicit held1835 source contract required');
 const c=contract.vehicle,L=c.wheelbase_m,track=c.track_m,front=c.radius_m.front,rear=c.radius_m.rear;
 if(L!==2.35||track!==1.21||front!==.535||rear!==.685)throw Error('Exact inspected W01 running gear required');
 if(contract.horse.current_walk_approved||contract.horse.certified_harness_or_sockets||contract.horse.old_89b_rig_reusable)throw Error('Do not promote inherited rig/gear claims');
 const pitch=solveTonguePitch(c.tongue_pivot_root_m[1],c.tongue_length_m,contract.fit_hypothesis.working_hitch_height_m);
 let previous=null,angles=[0,0,0,0],horseDistances=[0,0];
 function step(sample,groundHeights){
  for(const k of ['e','n','yaw_rad','distance_m','curvature_m_inv','speed_m_s'])finite(sample[k],k);
  if(sample.scene!=='1835'||sample.speed_m_s<0)throw Error('Forward1835 route state required');
  if(!Array.isArray(groundHeights)||groundHeights.length!==4||!groundHeights.every(Number.isFinite)||Math.max(...groundHeights)-Math.min(...groundHeights)>.03)throw Error('Actual four-wheel ground samples within30mm required; flat0 only explicit CPU fixture');
  const delta=Math.atan(L*sample.curvature_m_inv);if(Math.abs(delta)>c.max_steer_rad+1e-12)throw Error('Existing8degree steering limit');
  const base=Math.max(...groundHeights),vehiclePosition=add([sample.e,base,-sample.n],rotateY([0,0,L/2],sample.yaw_rad));
  const localHitch=add([0,front,L/2],rotateY([0,-c.tongue_length_m*Math.sin(pitch),.35+c.tongue_length_m*Math.cos(pitch)],delta));
  const horses=contract.fit_hypothesis.horse_roots_in_vehicle_rest_xz_m.map(([x,z])=>({position:add(vehiclePosition,rotateY(add([0,0,L/2],rotateY([x,0,z-L/2],delta)),sample.yaw_rad)),yaw_rad:sample.yaw_rad+delta,pose:'rigid source-fit hypothesis only; NOT walking',gaitApproved:false}));
  let ds=0,dyaw=0,ddelta=0;
  if(previous){
   ds=sample.distance_m-previous.distance;dyaw=wrap(sample.yaw_rad-previous.yaw);ddelta=delta-previous.delta;
   if(ds< -1e-10||ds>2)throw Error('Monotone bounded rear-axle distance increments required');
   if((sample.paused||sample.reducedMotion)&&ds>1e-10)throw Error('Paused/reduced-motion route advanced');
   if(ds>1e-10&&Math.abs(ddelta)>1e-8)throw Error('First route contract changes steering only at a stop');
   if(ds>1e-10&&Math.abs(dyaw-sample.curvature_m_inv*ds)>1e-7)throw Error('Route heading/distance/curvature mismatch');
   if(ds<=1e-10&&Math.abs(dyaw)>1e-10)throw Error('Stopped rear axle changed heading');
   // Fifth-wheel: actual front centers rotate with the WHOLE axle. Include counter-roll during stationary steering.
   angles=angles.map((a,i)=>{const x=(i%2===0?1:-1)*track/2;return a+(i<2?ds-x*dyaw:ds/Math.cos(delta)-x*(dyaw+ddelta))/(i<2?rear:front);});
   horseDistances=horses.map((h,i)=>horseDistances[i]+Math.hypot(h.position[0]-previous.horses[i].position[0],h.position[2]-previous.horses[i].position[2]));
  }
  previous={distance:sample.distance_m,yaw:sample.yaw_rad,delta,horses};
  return {diagnosticOnly:true,liveActivationAllowed:false,scope:'W01 rigid kinematics and unaccepted pair layout; NO currenthorse walk/harness/coupling/occupied/world acceptance',vehicle:{position:vehiclePosition,yaw_rad:sample.yaw_rad,steer_rad:delta,tongue_pitch_rad:pitch,wheel_angles_rad:[...angles],wheel_order:['rear_left','rear_right','front_left','front_right']},hitch:{world:add(vehiclePosition,rotateY(localHitch,sample.yaw_rad)),working_height_hypothesis_m:contract.fit_hypothesis.working_hitch_height_m,coupled:false,actual_harness_endpoint_gap_m:null},horses:horses.map((h,i)=>({...h,actual_root_chord_distance_m:horseDistances[i]})),driver:{person_id:contract.driver.person_id,grade:'reconstructed',occupation:'teamster (existing reconstructed record)',clip:'sit_drive',clip_time_s:contract.driver.clip_time_s,position:[...vehiclePosition],yaw_rad:sample.yaw_rad,attachAtSeatAgain:false,garmentSeatPalmReinFitApproved:false},increments:{rear_axle_distance_m:ds,yaw_rad:dyaw,steer_rad:ddelta},liveBlockers:[...contract.live_blockers]};
 }
 return {step,liveActivationAllowed:false};
}
// Apply only to explicitly supplied owned preview objects after separate root browser release.
// Horse objects must be OUTER normalized/source-support wrappers, never native bones or old89b rigs.
// driverRoot must be the sole existing Bardwell actor under an owned motion lease; never duplicate his standing instance.
export function applyDiagnosticPose(pose,{vehicleRoot,horseWrappers,driverRoot}={}){
 if(!pose?.diagnosticOnly||pose.liveActivationAllowed!==false)throw Error('Held source diagnostic required');
 const names=['vehicle_steer_front','vehicle_tongue',...pose.vehicle.wheel_order.map(n=>'vehicle_wheel_'+n)];
 const nodes=names.map(n=>{const v=vehicleRoot?.getObjectByName(n);if(!v)throw Error('Actual rigid W01 node missing '+n);return v;});
 if(!Array.isArray(horseWrappers)||horseWrappers.length!==2||horseWrappers.some(x=>x.userData?.approvedNativeNormalization!==true))throw Error('Two explicit current-native normalization wrappers required');
 vehicleRoot.position.fromArray(pose.vehicle.position);vehicleRoot.rotation.y=pose.vehicle.yaw_rad;nodes[0].rotation.y=pose.vehicle.steer_rad;nodes[1].rotation.x=pose.vehicle.tongue_pitch_rad;
 nodes.slice(2).forEach((n,i)=>{n.rotation.x=pose.vehicle.wheel_angles_rad[i];});
 horseWrappers.forEach((h,i)=>{h.position.fromArray(pose.horses[i].position);h.rotation.y=pose.horses[i].yaw_rad;});
 if(driverRoot){driverRoot.position.fromArray(pose.driver.position);driverRoot.rotation.y=pose.driver.yaw_rad;}
 return {appliedRigidPreviewOnly:true,liveActivationAllowed:false,gearCreated:false,horseAnimationStarted:false};
}
