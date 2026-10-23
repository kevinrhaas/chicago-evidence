// Offline scheduling/source-arithmetic and exact caller storage controls. No browser.
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {Quaternion,Euler} from '/workspace/shared/parked-2979-paired-overlay-PREPARED-HELD-v3/mirror/walk/vendor/three-0.185.1/three.core.js';
const root='/workspace/shared/parked-2979-paired-overlay-V4-DELTA-HELD';
const caller=fs.readFileSync(root+'/compare.cjs','utf8');
const main=fs.readFileSync('/workspace/shared/parked-2979-paired-overlay-PREPARED-HELD-v3/mirror/walk/js/main.js','utf8');
const a=JSON.parse(fs.readFileSync('/workspace/shared/parked-2979-paired-overlay-ACTUAL-v3/receipt.json')).arms[0],p=a.pose,D=Math.PI/180;
const start=main.indexOf('  function reaimAfterCard() {');
const reaim=main.slice(start,main.indexOf('  new MutationObserver(',start));
const boundary=caller.match(/await new Promise\(resolve=>setTimeout\(resolve,0\)\);/)?.[0];assert.ok(boundary);
const yieldTask=new Function('return async function(){'+boundary+'}')();
const scheduled={calls:0,quaternion:[...p.camera.quaternion]};
const walker={state:{e:p.teleport.local_e,n:p.teleport.local_n,eyeY:p.state.eyeY,flying:false},teleport(t){scheduled.calls++;scheduled.quaternion=new Quaternion().setFromEuler(new Euler(t.pitch_deg*D,-t.yaw_deg*D,0,'YXZ')).toArray();}};
const fire=new Function('walker','framing','focusPoint','DEG','arrival',`let lastArrival=arrival;${reaim};reaimAfterCard();`);
queueMicrotask(()=>fire(walker,()=>({aim:p.framing.aim}),()=>null,D,{id:'hogan_store',e:p.teleport.local_e,n:p.teleport.local_n}));
// Original ordering: two synchronous operations cannot drain a queued microtask.
const syncStep=()=>[...scheduled.quaternion];syncStep();syncStep();
const originalSnapshot=[...scheduled.quaternion];assert.equal(scheduled.calls,0);assert.notDeepEqual(originalSnapshot,a.samples[0].pose.quaternion);
await yieldTask();assert.equal(scheduled.calls,1);assert.deepEqual(scheduled.quaternion,a.samples[0].pose.quaternion);
const afterDrain=[...scheduled.quaternion];await yieldTask();assert.deepEqual(scheduled.quaternion,afterDrain);assert.equal(scheduled.calls,1);
const keys=JSON.parse(caller.match(/const PERSISTED_RENDER_KEYS=(\[[^;]+\]);/)[1].replaceAll("'",'"'));
function store(values={}){const o={...values};Object.defineProperties(o,{getItem:{value:k=>o[k]??null},setItem:{value:(k,v)=>{o[k]=String(v);}}});return o;}
const excluded=['c4d.blackbox','c4d.boot.timings.v1','c4d.boot.bytes.v1','c4d.boot.pace.v1','c4d.crashmarker','unrelated'];
const input=Object.fromEntries([...keys,...excluded].map(k=>[k,k==='chicago4d.settings'?'{"season":"summer"}':JSON.stringify({test:k})]));
const initialExpression=caller.match(/const initial=await page\.evaluate\((storageKeys=>\{.+?)\},PERSISTED_RENDER_KEYS\);record\.initial/)[1]+'}';
const initial=new Function('window','localStorage','storageKeys','return ('+initialExpression+')(storageKeys);')({__chicago4d:{ready:true,detail:'full',hud:{settings:{}}}},store(input),keys);
assert.deepEqual(Object.keys(initial.storage).sort(),[...keys].sort());assert.deepEqual(initial.storageSelection.excludedKeys,[...excluded].sort());
const initExpression=caller.match(/await ctx\.addInitScript\((\(\{stored,detail,quality,storageKeys\}\)=>\{.+?)\},\{stored:pairedStorage/)[1]+'}';
const destination=store();new Function('localStorage','args','return ('+initExpression+')(args);')(destination,{stored:input,detail:'full',quality:1,storageKeys:keys});
assert.deepEqual(Object.keys(destination).sort(),[...keys].sort());assert.equal(JSON.parse(destination.getItem('chicago4d.settings')).season,'summer');assert.equal(JSON.parse(destination.getItem('chicago4d.settings')).detail,'full');assert.equal(JSON.parse(destination.getItem('chicago4d.settings')).quality,1);
const tail='  // Passive GL commands are counted',v3=fs.readFileSync('/workspace/shared/parked-2979-paired-overlay-PREPARED-HELD-v3/compare.cjs','utf8');assert.equal(caller.slice(caller.indexOf(tail)),v3.slice(v3.indexOf(tail)));
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
console.log(JSON.stringify({PASS:true,browser_launches:0,caller_sha256:sha(caller),queuedMicrotaskOriginalRace:{observedPendingCalls:0,snapshotMatchesActualSettled:false,originalSnapshot},realTaskBoundary:{exactCallerStatement:boundary,appliedSourceReaimCalls:scheduled.calls,settledQuaternion:afterDrain,exactActualQuaternionMatch:true},controlLimit:'Node queued-microtask scheduling model plus exact source reaim body and recorded-aim stub; not a browser MutationObserver/full framing test',storage:{whitelist:keys,includedKeys:initial.storageSelection.includedKeys,excludedKeys:initial.storageSelection.excludedKeys,actualCallerExtractionAndInjectionPASS:true},rawModeAndCounterTailIdentical:true,guards:'600s process group / 240s boot / 30s entry unchanged; supervisor not duplicated or frozen'},null,2));
