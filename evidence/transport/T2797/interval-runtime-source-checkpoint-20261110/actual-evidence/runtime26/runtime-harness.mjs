// SPDX-License-Identifier: GPL-3.0-or-later
// PREPARED ONLY. CPU orchestration fixtures; never installed delivery qualification.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { register } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
const HERE=path.dirname(fileURLToPath(import.meta.url));
const SRC=path.join(HERE,'source74');
const VENDOR='/workspace/.cloud-setup/pages-alias-actual-20261110/site/4d/dev/walk/vendor/three-0.185.1/';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const json=p=>JSON.parse(fs.readFileSync(p));
const read=p=>json(path.join(SRC,p));
for(const row of json(path.join(HERE,'PREPARED-MANIFEST.json')).files)
 assert.equal(hash(fs.readFileSync(path.join(HERE,row.file))),row.sha256,row.file);
const bound=json(path.join(HERE,'SOURCE74-BINDING.json'));
for(const row of bound.files) assert.equal(hash(fs.readFileSync(row.path)),row.sha256,row.git_path);
for(const row of json(path.join(HERE,'VENDOR-BINDING.json')).files)
 assert.equal(hash(fs.readFileSync(row.path)),row.sha256,row.path);
register(`data:text/javascript,${encodeURIComponent(`export function resolve(s,c,next){
 if(s==='three')return{url:${JSON.stringify(pathToFileURL(VENDOR+'three.module.js').href)},shortCircuit:true};
 if(s.startsWith('three/addons/'))return{url:${JSON.stringify(pathToFileURL(VENDOR+'addons/').href)}+s.slice(13),shortCircuit:true};
 return next(s,c);
}`)}`,import.meta.url);
const THREE=await import('three');
const {GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js');
const load=name=>import(pathToFileURL(path.join(SRC,'renderers/web/js',name)).href);
const {HumanActor}=await load('humans.js');
const {createHumanDays,dayOn,spanAt}=await load('human-days.js');
const {createInteractions,createInteractKey}=await load('interact.js');
const {createHouseErrands}=await load('house-errands.js');
const original=await load('brougham-door.js');
const candidate=await import('./brougham-door-lifecycle-proposal.js');
const nearFile='/tmp/T2797-FLOOR-RING-LINK-PRODUCER-STRUCTURE-ATTEMPT1-20261110/results/candidate/near/brougham-door-study.glb';
const midFile='/tmp/T2797-FLOOR-RING-LINK-PRODUCER-STRUCTURE-ATTEMPT1-20261110/results/candidate/mid/brougham-door-study.glb';
const expected={near:'165e6c046d8e00b3ff2dc5db497165f5a759ff75b6dfeca247e0faccfab798aa',mid:'039d2a10e25e2be6319c8d0368851e3eb63a79bb5fba4a4840fda4bcd0c4f3d3'};
const roots=[];
for(const [i,file] of [nearFile,midFile].entries()){
 const raw=fs.readFileSync(file);assert.equal(hash(raw),expected[i?'mid':'near']);
 const doc=JSON.parse(raw.subarray(20,20+raw.readUInt32LE(12)));
 assert.equal(doc.images?.length??0,0,'CPU protocol cannot silently omit actual source image tasks');
 roots.push((await new GLTFLoader().parseAsync(raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength),pathToFileURL(path.dirname(file)+'/').href)).scene);
}
const inst=read('data/humans/instances/1904/hi_pa1904_glessner_john_j_c1900_charles_nelson_1904.json');
const person=read('data/sidecars/1904/people.json').people.find(p=>p.id===inst.person_id);assert(person);
const placements=read('data/transport/parked/placements.json');
const row=placements.scenes['1904'].find(p=>p.id==='prairie_parked_studebaker_brougham');assert(row);
const recipe=read('tools/transport/brougham/door-aperture.json');
assert(Object.values(recipe.qualification).every(v=>v===false),'actual recipe remains unqualified');
const result={schema:'door-controller-fixtures-v1',source_ref:bound.source_ref,status:'RUNNING',
 geometry_or_world_acceptance:false,boarding_enabled:false,driver_passenger_fit:false,
 fixture_only_qualification:true,cases:[],ports:[
 'Real Three/GLTFLoader and exact candidate near/mid meshes; synthetic qualification clone ONLY to reach rig/controller boundary.',
 'Real HumanActor walkPath/followPath/place, with NO loaded human body, mixer, gait, LOD or rendering.',
 'Real createHumanDays/createHouseErrands/createInteractions/createInteractKey; actual Charles identity, four-season record and door table.',
 'Scripted polyline router; constant ground4.33m; dummy household front-door registration; manually controlled visitor/layer ports.',
 'Simulation dt=.1 invokes native interaction, actor followPath, day update in main order; this is NOT a world-clock/render test.'
 ]};
function fixture(api){
 const actor=new HumanActor({instance:structuredClone(inst),person,assets:{},heightAt:()=>4.33});
 const humans={actors:[actor],shown:true,isHeld:()=>false};
 const ix=createInteractions();let errands=null,hour=10,date='1904-04-15',busy=false,routeMode='normal',calls=0;
 const router={plan:(a,b)=>{calls++;return routeMode==='none'?null:{points:[[a.e,a.n],[(a.e+b.e)/2,a.n],[b.e+(routeMode==='bad-end'?1:0),b.n]]};}};
 let visitor={e:actor.e,n:actor.n};
 const days=createHumanDays({humans,three:THREE,hour:()=>hour,date:()=>date,doors:read('data/humans/doors_1904.json'),
  visitor:()=>visitor,router,hostRouter:router,held:a=>busy||!!errands?.get(a.id)?.running});
 days.update(.1);
 const group=new THREE.Group();group.position.set(...[row.at_local_enu_m[0],4.33,-row.at_local_enu_m[1]]);
 group.rotation.y=Math.PI-row.bearing_deg*Math.PI/180;
 const [root,midRoot]=roots.map(r=>r.clone(true));group.add(root,midRoot);group.updateWorldMatrix(true,true);
 assert.throws(()=>api.broughamDoorRig({root,midRoot,spec:{door_operation:recipe},vehicleHashes:expected}),/Unqualified/);
 // Deliberately fabricated admission fixture: NEVER written to app or a sidecar.
 const plan={...structuredClone(recipe),schema:'chicago-brougham-qualified-right-door-v1',
  qualification:Object.fromEntries(Object.keys(recipe.qualification).map(k=>[k,true])),
  geometry_proof_sha256:hash('SYNTHETIC UNIT FIXTURE; NO GEOMETRY QUALIFICATION'),
  deliveries:{near:{sha256:expected.near},mid:{sha256:expected.mid}}};
 const door=api.broughamDoorRig({root,midRoot,spec:{door_operation:plan},vehicleHashes:expected});
 const parked={doorsAvailable:true,instances:[{row,group,door}]};
 const actions=api.createCoachmanDoorActions({parkedTransport:parked,humans,days,router,visitor:()=>visitor,interactions:ix});
 const front={id:'glessner_house:front',state:'closed',running:null};
 errands=createHouseErrands({days,humans,houseDoors:{get:id=>id===front.id?front:null},interactions:ix,visitor:()=>visitor,extraActions:actions});
 const thing=errands.get(actor.id);assert(thing,'actual Charles registered through household extraActions');
 const said=[];const key=createInteractKey({interactions:ix,where:()=>visitor,say:s=>said.push(s)});
 let unhosts=0;const unhost=days.unhost;days.unhost=(...args)=>{unhosts++;return unhost(...args);};
 function tick(count=1,{walk=true}={}){for(let i=0;i<count;i++){
  ix.update(.1);if(walk&&humans.shown&&!actor.indoors&&!actor.disposed&&actor.path)actor.followPath(.1);days.update(.1);
 }}
 function until(test,max=800,opts){for(let i=0;i<max&&!test();i++)tick(1,opts);assert(test(),'bounded native sequence reached predicate');}
 return {actor,humans,ix,days,door,parked,group,actions,thing,key,said,router,tick,until,
  get unhosts(){return unhosts;},get calls(){return calls;},get hour(){return hour;},set hour(v){hour=v;},
  set busy(v){busy=v;},set routeMode(v){routeMode=v;},set visitor(v){visitor=v;},
  act:id=>ix.act(thing,id),cleanup(){actions.dispose();key.dispose();actor.stopPath();}};
}
const definitions=[];
const add=(name,fn,originalFailure=false)=>definitions.push({name,fn,originalFailure});
add('unqualified recipe is refused; normal native approach/open/close and exact-once return',f=>{
 assert(f.key.refresh());assert(f.key.choices.includes('carriage:open'));
 assert(f.act('carriage:open').ok);assert(f.days.isHosted(f.actor));
 assert.equal(f.door.fraction,0);assert(f.actor.path);
 // Hosted people are currently removed from the key's nearest domain: disclose this UI gap.
 assert.equal(f.key.refresh(),null);
 f.tick(1);assert.equal(f.door.fraction,0,'one time step cannot stand in for actual arrival');
 f.until(()=>!f.thing.running);assert.equal(f.door.fraction,1);assert.equal(f.unhosts,1);assert(!f.days.isHosted(f.actor));
 assert(f.door.leaves.every(n=>n.rotation.y===recipe.open_angle_deg*Math.PI/180));
 assert(f.act('carriage:close').ok);f.until(()=>!f.thing.running);assert.equal(f.door.fraction,0);assert.equal(f.unhosts,2);
 assert(f.said.some(s=>s.includes('Boarding is not available')));
});
add('other identity never receives the action',f=>assert.deepEqual(f.actions({...f.actor,personId:'glessner_john_j'}),[]));
add('unsafe measured staff stand refuses before native host',f=>{
 const pivot=f.door.leaves[0].getWorldPosition(new THREE.Vector3());
 f.door.plan.staff_stand_local_m=f.parked.instances[0].group.children[0].worldToLocal(pivot.clone()).toArray();
 assert.equal(f.act('carriage:open').ok,false);assert(!f.days.isHosted(f.actor));assert.equal(f.door.fraction,0);
});
for(const mode of ['none','bad-end']) add('route '+mode+' refuses without path or host takeover',f=>{
 f.routeMode=mode;const before=f.actor.path;assert.equal(f.act('carriage:open').ok,false);assert.equal(f.actor.path,before);assert(!f.days.isHosted(f.actor));
});
add('occupied swing refuses; mid-swing entry stops further movement',f=>{
 const p=f.door.leaves[0].getWorldPosition(new THREE.Vector3());f.visitor={e:p.x,n:-p.z};
 assert.equal(f.act('carriage:open').ok,false);assert.equal(f.door.fraction,0);
 f.visitor={e:f.actor.e,n:f.actor.n};assert(f.act('carriage:open').ok);f.until(()=>f.thing.running?.index===1);
 f.tick(2);const stopped=f.door.fraction;f.visitor={e:p.x,n:-p.z};f.tick(20);assert.equal(f.door.fraction,stopped);
 assert(f.said.some(s=>s.includes('swing')));assert.equal(f.unhosts,1);
});
add('real busy-owner host refusal preserves existing callback/path',f=>{
 f.busy=true;const before=f.actor.path;assert.equal(f.act('carriage:open').ok,false);assert.equal(f.actor.path,before);assert(!f.days.isHosted(f.actor));assert.equal(f.unhosts,0);
});
add('timeout never becomes arrival; door remains closed and ownership returns',f=>{
 assert(f.act('carriage:open').ok);f.tick(630,{walk:false});assert.equal(f.door.fraction,0);assert(!f.days.isHosted(f.actor));
 assert(f.said.includes('Charles has not reached the carriage door'));assert.equal(f.unhosts,1);
});
add('hour crosses actual seasonal11:00 break while hosted; release chooses current span',f=>{
 assert(f.act('carriage:open').ok);f.hour=11.1;f.until(()=>!f.thing.running);f.tick();
 const span=spanAt(dayOn(inst.behaviour,'1904-04-15',inst.person_id),11.1);assert.equal(span.knot,'glessner_18th');
 assert(!f.days.isHosted(f.actor));assert.equal(f.days.snapshot()[0].span.from,11);
 assert(f.actor.path,'safe handback uses native route toward current break, not a fixed post');
});
for(const layer of ['people','vehicles']) add('loss of '+layer+' while approaching promptly releases own host',f=>{
 assert(f.act('carriage:open').ok);if(layer==='people')f.humans.shown=false;else f.parked.doorsAvailable=false;
 f.tick();assert(!f.days.isHosted(f.actor),'EXPECTED_LIFECYCLE_HOST_RELEASE');assert.equal(f.unhosts,1);assert.equal(f.door.fraction,0);f.tick(30);assert.equal(f.unhosts,1);
},true);
add('provider disposal prevents retained shared-interact swing closure',f=>{
 assert(f.act('carriage:open').ok);f.until(()=>f.thing.running?.index===1);const angle=f.door.leaves[0].rotation.y;
 f.actions.dispose();assert.equal(f.unhosts,1);f.tick(30);assert.equal(f.door.leaves[0].rotation.y,angle,'EXPECTED_LIFECYCLE_NO_POSTDISPOSE_POSE');assert.equal(f.unhosts,1);assert.deepEqual(f.actions(f.actor),[]);
},true);
add('disposed/indoors actors and hidden people never offer fresh actions',f=>{
 f.actor.disposed=true;assert.deepEqual(f.actions(f.actor),[]);f.actor.disposed=false;f.actor.indoors=true;assert.deepEqual(f.actions(f.actor),[]);
 f.actor.indoors=false;f.humans.shown=false;assert.deepEqual(f.actions(f.actor),[]);
});
for(const [label,api] of [['original74',original],['proposal',candidate]]){
 for(const d of definitions){let f,error=null,stage='fixture';try{f=fixture(api);stage='case';d.fn(f);}catch(e){error={name:e.name,code:e.code,message:e.message,stack:e.stack};}finally{f?.cleanup();}
  const expectedFailure=label==='original74'&&d.originalFailure;
  const reproduced=expectedFailure&&stage==='case'&&error?.code==='ERR_ASSERTION'&&error.message.includes('EXPECTED_LIFECYCLE_');
  result.cases.push({source:label,name:d.name,expected_failure:expectedFailure,actual_error:error,
   failure_stage:error?stage:null,verdict:expectedFailure?(reproduced?'ORIGINAL_COUNTEREXAMPLE_REPRODUCED':error?'NONPASS':'UNEXPECTED_ORIGINAL_SUCCESS'):(error?'NONPASS':'PASS')});
  fs.writeFileSync(path.join(HERE,'PARTIAL-RESULT.json'),JSON.stringify(result,null,2)+'\n');
 }
}
result.status=result.cases.every(c=>['PASS','ORIGINAL_COUNTEREXAMPLE_REPRODUCED'].includes(c.verdict))?'CPU_FIXTURES_ONLY_PASS':'NONPASS';
fs.writeFileSync(path.join(HERE,'RESULT.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,cases:result.cases.length,geometry_or_world_acceptance:false}));
if(result.status==='NONPASS')process.exitCode=1;
