// Offline only. Execute the exact pinned application's reaimAfterCard body with
// the recorded aim and an explicit framing/focus stub; no DOM/browser or app writes.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {Quaternion,Euler} from '/workspace/shared/parked-2979-paired-overlay-PREPARED-HELD-v3/mirror/walk/vendor/three-0.185.1/three.core.js';
const base='/workspace/shared/parked-2979-paired-overlay-PREPARED-HELD-v3';
const mainPath=base+'/mirror/walk/js/main.js';
const receiptPath='/workspace/shared/parked-2979-paired-overlay-ACTUAL-v3/receipt.json';
const main=fs.readFileSync(mainPath,'utf8'),r=JSON.parse(fs.readFileSync(receiptPath)),a=r.arms[0],p=a.pose,s=a.samples[0],D=Math.PI/180;
const body=main.slice(main.indexOf('  function reaimAfterCard() {'),main.indexOf('  new MutationObserver(',main.indexOf('  function reaimAfterCard() {')));
if(!body.includes('framing(id, { card: false })')||!body.includes('walker.teleport'))throw Error('Pinned extraction failed');
function run({moved=false,flying=false}={}){
 const calls=[];
 const walker={state:{e:p.teleport.local_e+(moved?1:0),n:p.teleport.local_n,eyeY:p.state.eyeY,flying},teleport:v=>calls.push(v)};
 const framingCalls=[];
 const framing=(id,opts)=>{framingCalls.push({id,opts});return {aim:p.framing.aim};};
 new Function('walker','framing','focusPoint','DEG','arrival',`let lastArrival=arrival;${body};reaimAfterCard();`)(walker,framing,()=>{throw Error('Unexpected fallback');},D,{id:'hogan_store',e:p.teleport.local_e,n:p.teleport.local_n});
 return {calls,framingCalls};
}
const positive=run(),moved=run({moved:true}),flying=run({flying:true});
if(positive.calls.length!==1||moved.calls.length||flying.calls.length)throw Error('Source branch controls failed');
const t=positive.calls[0],q=new Quaternion().setFromEuler(new Euler(t.pitch_deg*D,-t.yaw_deg*D,0,'YXZ')),actual=new Quaternion().fromArray(s.pose.quaternion),before=new Quaternion().fromArray(p.camera.quaternion);
const maxComponentError=Math.min(...[1,-1].map(sign=>Math.max(...actual.toArray().map((v,i)=>Math.abs(v-sign*q.toArray()[i])))));
if(maxComponentError!==0)throw Error('Prediction differs from actual');
const sha=path=>crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
console.log(JSON.stringify({PASS:true,browser_launches:0,scope:'Exact reaimAfterCard source body; framing is an explicit recorded-aim stub, not a browser or full framing execution',main_sha256:sha(mainPath),receipt_sha256:sha(receiptPath),three_core_sha256:sha(base+'/mirror/walk/vendor/three-0.185.1/three.core.js'),positive,movedControl:moved,flyingControl:flying,predictedQuaternion:q.toArray(),actualQuaternion:actual.toArray(),maxComponentError,observedPhysicalRotationDegrees:before.angleTo(actual)/D,beforeBearingDegrees:p.teleport.yaw_deg,afterBearingDegrees:t.yaw_deg,beforePitchDegrees:p.teleport.pitch_deg,afterPitchDegrees:t.pitch_deg,yawChangeDegrees:((t.yaw_deg-p.teleport.yaw_deg+540)%360)-180,limit:'Actual MutationObserver invocation/time was not recorded. Exact arithmetic prediction matches actual; this does not measure CI camera or CI failures.'},null,2));
