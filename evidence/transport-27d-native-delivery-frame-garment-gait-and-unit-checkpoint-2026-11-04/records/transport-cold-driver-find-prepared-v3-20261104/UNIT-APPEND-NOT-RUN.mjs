
// Cold named-driver rendezvous: actual town/loop/main/Travel/Interact behavior.
// Append to the existing test_driven_assembly.mjs; no new gate declaration.
{
  const { createInteractions } = await import('../renderers/web/js/interact.js');
  const { registerTransportInteraction } = await import('../renderers/web/js/transport-interactions.js');
  const { createTravel } = await import('../renderers/web/js/travel.js');
  const config = JSON.parse(readFileSync(new URL('../data/transport/driven/loops.json', import.meta.url)));
  const main = readFileSync(new URL('../renderers/web/js/main.js', import.meta.url), 'utf8');
  const start = main.indexOf('  function goToTarget(target) {');
  const end = main.indexOf('  /** The future welcome picker', start);
  assert(start >= 0 && end > start);
  const actualGo = main.slice(start, end);
  const pending = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return {promise, resolve, reject}; };
  const fixture = (sourceRow, options = {}) => {
    const loads = [], publications = [], problems = [], disposed = [], poses = [], visual = [];
    const rows = options.rows ?? [sourceRow];
    let liveClear = options.liveClear ?? true;
    const town = createTownTransport({ rows, sceneId: options.sceneId ?? sourceRow.scene,
      detail: options.detail ?? 'full', heightAt: options.heightAt ?? (() => 0),
      routeClear: () => true, routeSupport: () => ({ valid: true }),
      clear: () => liveClear, problems,
      makeAssembly(row) {
        const gate = pending(), number = loads.length;
        const assembly = { root: new THREE.Group(), pose(p) { poses.push([number, p]); }, advance() {}, visible() {}, stop() {},
          updateVisual(dt) { visual.push(dt); }, dispose() { disposed.push(number); } };
        const load = { row, assembly, gate }; loads.push(load); return gate.promise;
      },
      onActorsChanged(actors) { publications.push(actors.map(a => ({ id:a.id, personId:a.personId, state:a.state, reason:a.snapshot().reason }))); },
    });
    const anchor = town.driverAnchorForPerson(sourceRow.person_id);
    const camera = anchor ? { x:anchor.at[0], z:-anchor.at[1] } : { x:0, z:0 };
    town.update(0, camera); // Existing lastUpdate path, not a fake source mutation.
    const load = async number => { await until(() => loads.length > number); return loads[number]; };
    return {town, loads, publications, problems, disposed, poses, visual, camera,
      setClear(value) { liveClear = value; }, load,
    };
  };
  const settle = async (f, loadNumber = 0) => {
    const ready = f.town.ready(), load = await f.load(loadNumber);
    load.gate.resolve(load.assembly); await ready; return f.town.actors[0];
  };
  const makeGo = (town, travel, options = {}) => Function('api','jauntRuntime','travel','router','hud','destinations',
    'openBusiness','openBuilding','supportsTownTransport','YEAR','draws','openPersonCard', actualGo + '\nreturn goToTarget;')(
    { townTransport:town, humans:{ external:() => null } }, null, travel,
    { blockedAt:options.blockedAt ?? (() => false) }, { say(){}, setPanel(){}, selectTab(){} },
    { resolve:options.resolve ?? (() => null), byId:() => null }, () => {}, () => {}, () => true, '1835', () => true, () => {});
  const target = row => ({kind:'person', id:row.person_id, label:row.name});
  const assertStopped = (actor, row) => {
    assert.equal(actor.id, row.id); assert.equal(actor.personId, row.person_id);
    assert.equal(actor.state, 'stopped'); assert.equal(actor.snapshot().reason, 'approach');
  };

  // Both actual configured identities: no load at request, stop before publication,
  // no later automatic resume, and no change to the route/seat side-stand owner.
  for (const row of config.rows) {
    const f = fixture(row), original = JSON.stringify(row), visits = [];
    const cold = f.town.driverAnchorForPerson(row.person_id);
    const go = makeGo(f.town, { go(destination, callbacks) { visits.push({destination, callbacks}); return true; } });
    assert.equal(go(target(row)), true); assert.equal(f.loads.length, 0); assert.equal(f.town.actors.length, 0);
    assert.equal(visits[0].destination.local_e, cold.at[0] + Math.cos(cold.yaw_rad) * 4);
    assert.equal(visits[0].destination.local_n, cold.at[1] + Math.sin(cold.yaw_rad) * 4);
    assert.equal(JSON.stringify(row), original);
    const actor = await settle(f); assertStopped(actor, row);
    assert.deepEqual(f.publications.at(-1), [{id:row.id,personId:row.person_id,state:'stopped',reason:'approach'}]);
    const saved = actor.snapshot();
    for (let i=0;i<8;i++) f.town.update(.25, f.camera, {visualDt:.25});
    assert.equal(actor.snapshot().total_distance_m, saved.total_distance_m);
    assert.deepEqual(actor.snapshot().wheel_rotation_rad, saved.wheel_rotation_rad);
    visits[0].callbacks.onStop({reason:'input'}); assertStopped(actor,row);
    f.town.dispose(); assert.equal(f.disposed.length,1);
  }

  const row = config.rows.find(r => r.scene === '1835');
  // Cancellation is observable through the subsequently admitted actor state.
  {
    const f = fixture(row); const request = f.town.requestDriverApproach(row.person_id);
    assert(request); request.cancel(); request.cancel();
    const actor = await settle(f); assert.equal(actor.state,'moving','Canceled intent is idempotent');
    f.town.dispose();
  }
  for (const outcome of ['false','throw']) {
    const f=fixture(row); const go=makeGo(f.town,{go(){if(outcome==='throw')throw Error('planned travel refusal');return false;}});
    if(outcome==='throw')assert.throws(()=>go(target(row)),/planned travel refusal/);else assert.equal(go(target(row)),false);
    const actor=await settle(f);assert.equal(actor.state,'moving');f.town.dispose();
  }
  // Actual Travel onStop wiring, including the real manual-input branch.
  for (const reason of ['input','button','unreachable','replaced']) {
    const f=fixture(row), walker={state:{e:0,n:0,yaw:0,pitch:0,altitude:0,flying:false,speed:0,bob:0},resettle(){}};
    const intent={flying:false,moving:false,yawDelta:0,pitchDelta:0};
    const travel=createTravel({walker,intent,router:{plan:()=>reason==='unreachable'?null:{points:[[1,1],[2,2]]}},hud:{},settings:{}});
    travel.setMode('walk');const go=makeGo(f.town,travel);
    assert.equal(go(target(row)),reason!=='unreachable');
    if(reason==='input'){intent.moving=true;travel.update(.1,intent);}else if(reason==='button')travel.stop('button');
    else if(reason==='replaced'){assert(travel.go({kind:'intersection',local_e:3,local_n:4}));travel.stop('button');}
    const actor=await settle(f);assert.equal(actor.state,'moving');f.town.dispose();
  }
  // Native instant arrival retains rendezvous intent; the real Move Stop callback
  // cancels it even though the instant Travel controller is already idle.
  for(const cancelAfterInstantArrival of [false,true]){
    const f=fixture(row), visits=[], walker={state:{e:0,n:0,flying:false},resettle(){}};
    const travel=createTravel({walker,intent:{flying:false},settings:{},teleport:p=>visits.push(p),setFly(){}});
    assert.equal(makeGo(f.town,travel)(target(row)),true);assert.equal(visits.length,1);
    if(cancelAfterInstantArrival){
      const match=main.match(/onTravelStop: \(\) => \{ ([^\n]+) \},/);assert(match,'Actual Move Stop callback missing');
      Function('api','travel',match[1])({townTransport:f.town},travel);
    }
    const actor=await settle(f);assert.equal(actor.state,cancelAfterInstantArrival?'moving':'stopped');f.town.dispose();
  }
  // A second real Find installs its new token before native Travel replaces the
  // old ride; the old onStop closure must not remove that new rendezvous.
  {
    const f=fixture(row),walker={state:{e:0,n:0,yaw:0,pitch:0,altitude:0,flying:false,speed:0,bob:0},resettle(){}};
    const travel=createTravel({walker,intent:{flying:false},settings:{},router:{plan:()=>({points:[[1,1],[2,2]]})}});
    travel.setMode('walk');const go=makeGo(f.town,travel);assert(go(target(row)));assert(go(target(row)));
    assertStopped(await settle(f),row);travel.stop('button');assertStopped(f.town.actors[0],row);f.town.dispose();
  }
  // Actual fatal-row refusal is transactional: it cannot replace a still-valid
  // cold Find or its real Travel ride. The older actor must stop after load.
  {
    const failedRow=structuredClone(row);failedRow.id='fixture-terminal-row';failedRow.person_id='fixture-terminal-person';
    failedRow.name='Fixture terminal driver';failedRow.driver_instance.person_id=failedRow.person_id;
    const f=fixture(row,{rows:[failedRow,row]});const loading=f.town.ready(),bad=await f.load(0);
    bad.gate.reject(Error('planned terminal row refusal'));const oldLoad=await f.load(1);
    const walker={state:{e:0,n:0,yaw:0,pitch:0,altitude:0,flying:false,speed:0,bob:0},resettle(){}};
    const travel=createTravel({walker,intent:{flying:false},settings:{},router:{plan:()=>({points:[[1,1],[2,2]]})}});
    travel.setMode('walk');const go=makeGo(f.town,travel);assert(go(target(row)));
    const oldRide=travel.state,oldRoute=travel.routeAhead();assert.equal(go(target(failedRow)),false);
    assert.equal(travel.state.phase,oldRide.phase);assert.equal(travel.state.dest,oldRide.dest);assert.deepEqual(travel.routeAhead(),oldRoute);
    oldLoad.gate.resolve(oldLoad.assembly);await loading;assertStopped(f.town.driverForPerson(row.person_id),row);
    travel.stop('button');assertStopped(f.town.driverForPerson(row.person_id),row);f.town.dispose();
  }

  // The old handle cannot cancel a newer request for the same identity.
  {
    const f=fixture(row), old=f.town.requestDriverApproach(row.person_id);
    const current=f.town.requestDriverApproach(row.person_id);old.cancel();
    const actor=await settle(f);assertStopped(actor,row);current.cancel();assertStopped(actor,row);
    const interactions=createInteractions(), handle=registerTransportInteraction(interactions,actor);
    f.setClear(false);assert.equal(handle.thing.actions.stopped[0].id,'give-room');
    assert.equal(interactions.act(handle.thing.id,'continue').ok,false);assert.equal(actor.state,'stopped');
    f.setClear(true);assert.equal(interactions.act(handle.thing.id,'continue').ok,true);interactions.update(0);
    assert.equal(actor.state,'moving');f.town.update(.1,f.camera);assert.equal(actor.state,'moving');
    assert.equal(interactions.act(handle.thing.id,'stop').ok,true);interactions.update(0);assert.equal(actor.state,'stopped');
    current.cancel();assert.equal(actor.state,'stopped');handle.dispose();f.town.dispose();
  }
  // A namespaced synthetic second metadata row exercises map-key isolation only;
  // no assertion here qualifies that fixture identity/asset for a historical scene.
  {
    const other=structuredClone(row);other.id='fixture-other-route';other.person_id='fixture-other-person';
    other.driver_instance.person_id=other.person_id;
    const f=fixture(row,{rows:[row,other]});const first=f.town.requestDriverApproach(row.person_id);
    f.town.requestDriverApproach(other.person_id);first.cancel();
    const loading=f.town.ready(), a=await f.load(0);a.gate.resolve(a.assembly);
    const b=await f.load(1);b.gate.resolve(b.assembly);await loading;
    assert.equal(f.town.driverForPerson(row.person_id).state,'moving');
    assertStopped(f.town.driverForPerson(other.person_id),other);f.town.dispose();
  }
  // Blocked/invalid proposed destinations preserve current pending intent; a new
  // valid coordinate destination cancels unresolved intent, never fulfilled Stop.
  {
    const f=fixture(row);f.town.requestDriverApproach(row.person_id);
    assert.equal(makeGo(f.town,{go(){throw Error('blocked target must not navigate');}},{blockedAt:()=>true})(target(row)),false);
    assert.equal(makeGo(f.town,{go(){throw Error('invalid target must not navigate');}})({kind:'person',id:'unknown'}),false);
    assertStopped(await settle(f),row);f.town.dispose();
    const g=fixture(row);g.town.requestDriverApproach(row.person_id);
    assert.equal(makeGo(g.town,{go:()=>true})({kind:'intersection',local_e:12,local_n:34}),true);
    assert.equal((await settle(g)).state,'moving');g.town.dispose();
  }
  // Identity/date/eligibility/Light guards remain lazy metadata operations.
  for (const variant of ['unknown','wrongyear','mismatch','unselectable','missingasset','light']) {
    const changed=structuredClone(row);if(variant==='mismatch')changed.driver_instance.person_id='someone-else';
    if(variant==='unselectable')changed.driver_instance.interaction.selectable=false;
    if(variant==='missingasset')delete changed.driver_asset;
    const f=fixture(changed,{sceneId:variant==='wrongyear'?'1904':changed.scene,detail:variant==='light'?'light':'full'});
    assert.equal(f.town.requestDriverApproach(variant==='unknown'?'unknown':changed.person_id),null);
    assert.equal(f.loads.length,0);f.town.dispose();
  }
  // Fulfilled Stop remains the saved native journey through Light restoration.
  {
    const f=fixture(row);const request=f.town.requestDriverApproach(row.person_id);const actor=await settle(f);assertStopped(actor,row);
    const saved=actor.snapshot(),savedPose=f.poses.at(-1)[1];
    await f.town.setTier('light');assert.equal(f.town.actors.length,0);assert.equal(f.disposed.length,1);
    const restoring=f.town.setTier('full'), next=await f.load(1);next.gate.resolve(next.assembly);await restoring;
    const restored=f.town.actors[0];assert.equal(restored.id,row.id);assert.equal(restored.personId,row.person_id);
    assert.equal(restored.state,'stopped');assert.equal(restored.snapshot().reason,null,'Existing Light serialization preserves stopped state, not its diagnostic reason');
    assert.equal(restored.snapshot().total_distance_m,saved.total_distance_m);assert.equal(restored.snapshot().distance_m,saved.distance_m);
    assert.deepEqual(restored.snapshot().wheel_rotation_rad,saved.wheel_rotation_rad);assert.deepEqual(f.poses.at(-1)[1],savedPose);
    request.cancel();f.town.update(8,f.camera);assert.equal(restored.state,'stopped');
    assert.equal(restored.snapshot().total_distance_m,saved.total_distance_m);assert.deepEqual(f.poses.at(-1)[1],savedPose);
    f.setClear(false);assert.equal(restored.canResume(),false);assert.equal(restored.resume(),false);assert.equal(restored.state,'stopped');
    f.setClear(true);assert(restored.resume());f.town.update(.1,f.camera);
    assert.equal(restored.state,'moving');assert(restored.snapshot().total_distance_m>saved.total_distance_m);
    assert.equal(restored.id,row.id);assert.equal(restored.personId,row.person_id);f.town.dispose();
  }
  // Retired generation cannot consume active intent; cancel while Light removes it.
  for(const cancelWhileLight of [false,true]){
    const f=fixture(row), request=f.town.requestDriverApproach(row.person_id), firstReady=f.town.ready(), old=await f.load(0);
    const light=f.town.setTier('light');if(cancelWhileLight)request.cancel();
    const full=f.town.setTier('full'), next=await f.load(1);
    old.gate.resolve(old.assembly);await firstReady;await light;assert.deepEqual(f.disposed,[0]);
    next.gate.resolve(next.assembly);await full;
    assert.equal(f.town.actors.length,1);assert.equal(f.town.actors[0].state,cancelWhileLight?'moving':'stopped');
    assert.equal(f.publications.filter(p=>p.some(a=>a.id===row.id)).length,1);f.town.dispose();
  }
  // Disposed layer callbacks cannot touch a same-person request in another layer.
  {
    const old=fixture(row), oldRequest=old.town.requestDriverApproach(row.person_id), oldReady=old.town.ready(), load=await old.load(0);
    old.town.dispose();const current=fixture(row);current.town.requestDriverApproach(row.person_id);oldRequest.cancel();
    load.gate.resolve(load.assembly);await oldReady;assert.equal(old.town.actors.length,0);assert.deepEqual(old.disposed,[0]);
    assertStopped(await settle(current),row);current.town.dispose();
  }
  // Real recoverable post-asset spawn error retains intent; fatal factory failure
  // clears it and retains the original no-automatic-retry row owner.
  {
    const f=fixture(row);f.town.requestDriverApproach(row.person_id);f.setClear(false);
    await settle(f);assert.equal(f.town.actors.length,0);assert.deepEqual(f.disposed,[0]);assert.equal(f.problems.length,0);
    await f.town.ready();assert.equal(f.loads.length,1);
    f.setClear(true);assertStopped(await settle(f,1),row);f.town.dispose();
    const g=fixture(row);g.town.requestDriverApproach(row.person_id);const loading=g.town.ready(), failed=await g.load(0);
    failed.gate.reject(Error('actual fatal fixture factory refusal'));await loading;assert.equal(g.problems.length,1);
    await g.town.ready();assert.equal(g.loads.length,1);
    assert.equal(g.town.requestDriverApproach(row.person_id),null,'Known terminal failed row cannot acquire an unfulfillable new request');
    await g.town.setTier('light');const restoring=g.town.setTier('full'), next=await g.load(1);next.gate.resolve(next.assembly);await restoring;
    assert.equal(g.town.actors[0].state,'moving','Fatal row removed its old intent before a later explicit tier reset');g.town.dispose();
    const ground=fixture(row,{heightAt:()=>null});ground.town.requestDriverApproach(row.person_id);await ground.town.ready();
    assert.equal(ground.loads.length,0,'Fatal actual route-ground refusal must precede any model acquisition');
    assert.equal(ground.problems.length,1);assert.equal(ground.town.requestDriverApproach(row.person_id),null);ground.town.dispose();
  }
  console.log('cold named-driver Find: exact configured identities, stop-before-publication, real Travel cancellation, stale tokens, shared Continue, Light/generation/dispose and recoverable/fatal ownership PASS');
}
