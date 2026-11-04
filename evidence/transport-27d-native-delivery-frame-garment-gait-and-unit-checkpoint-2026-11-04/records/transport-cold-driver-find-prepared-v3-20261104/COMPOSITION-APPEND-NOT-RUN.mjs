
// Optional composed-parcel acceptance: requires BOTH motion V2 and cold Find.
// Exercise the actual createDrivenAssembly adapter, town and loop together.
{
  const config=JSON.parse(readFileSync(new URL('../data/transport/driven/loops.json',import.meta.url)));
  const row=config.rows.find(r=>r.scene==='1835');let phase=0;const calls=[];let town;
  town=createTownTransport({rows:[row],sceneId:row.scene,heightAt:()=>0,clear:()=>true,routeSupport:()=>({valid:true}),
    makeAssembly:async liveRow=>createDrivenAssembly({vehicle:vehicle.clone(true),
      driver:{root:new THREE.Group(),updateVisual(dt){phase+=dt;calls.push(dt);},snapshot(){return{time_s:phase};}},
      horse:{root:new THREE.Group(),advance(){},stop(){}},driverSeat_m:row.driver_seat_node_m,
      horseOffset_m:row.horse_offset_m,disposeVehicle(){}}),
    onActorsChanged(actors){for(const actor of actors)assert.equal(actor.state,'stopped','Cold Find owns stop before publication and synthetic replay');}});
  const anchor=town.driverAnchorForPerson(row.person_id),camera={x:anchor.at[0],z:-anchor.at[1]};
  town.update(0,camera,{elapsedFrame:true,visualDt:0});const request=town.requestDriverApproach(row.person_id);await town.ready();
  assert.equal(calls.length,0,'Motion V2 synthetic admission cannot prime the independent driver visual clock');
  let actor=town.driverForPerson(row.person_id);assert.equal(actor.state,'stopped');assert.equal(actor.personId,row.person_id);
  const frame=dt=>town.update(dt,camera,{elapsedFrame:true,visualDt:dt});
  frame(8);assert.equal(phase,0);assert.equal(actor.snapshot().total_distance_m,0);
  frame(.5);assert.equal(phase,.5);request.cancel();assert.equal(actor.state,'stopped');
  const saved=actor.snapshot(),savedPhase=phase;
  await town.setTier('light');await town.setTier('full');actor=town.driverForPerson(row.person_id);
  assert.equal(actor.id,row.id);assert.equal(actor.personId,row.person_id);assert.equal(actor.state,'stopped');assert.equal(actor.snapshot().reason,null);
  assert.equal(actor.snapshot().distance_m,saved.distance_m);assert.equal(actor.snapshot().total_distance_m,saved.total_distance_m);
  assert.deepEqual(actor.snapshot().wheel_rotation_rad,saved.wheel_rotation_rad);
  frame(8);assert.equal(phase,savedPhase,'First actual restored visual clock rejects the unseen interval');
  assert.equal(actor.snapshot().total_distance_m,saved.total_distance_m);assert.deepEqual(actor.snapshot().wheel_rotation_rad,saved.wheel_rotation_rad);
  frame(.125);assert.equal(phase,savedPhase+.125);assert.equal(actor.state,'stopped');request.cancel();assert.equal(actor.state,'stopped');
  const before=actor.snapshot(),beforeContinuePhase=phase;assert(actor.resume());frame(8);
  assert.equal(actor.snapshot().total_distance_m,before.total_distance_m,'Continue consumes no pre-action interval');
  assert.deepEqual(actor.snapshot().wheel_rotation_rad,before.wheel_rotation_rad);
  assert.equal(phase,beforeContinuePhase+8,'Qualified independent look continues during a journey-only Stop/Continue');
  frame(.5);assert(Math.abs(actor.snapshot().total_distance_m-row.speed_m_s*.5)<1e-9);
  assert.equal(actor.state,'moving','Fulfilled/canceled Find intent cannot stop a resumed native journey again');
  town.dispose();console.log('composed motionV2+cold Find: actual assembly publication/visual admission, fulfilled Stop, native Continue zero and configured next-frame pace PASS');
}
