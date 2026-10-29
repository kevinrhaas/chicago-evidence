// Supplemental camera-only native observation. Does not modify the lifecycle protocol or app.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
export async function observeNativeRailwayFarCamera(page, outputDir, { profile }) {
  assert.ok(['desktop','mobile'].includes(profile));
  const nativeDetail=profile==='desktop'?'full':'light',farOffset=profile==='desktop'?350:150;
  await fs.mkdir(outputDir,{recursive:true});
  const planBytes=await fs.readFile(new URL('../RAIL-LIFECYCLE-DESKTOP-03/source-plan.json',import.meta.url));
  const plan=JSON.parse(planBytes),rows=[],settlements=[],errors=[],consoleErrors=[];
  page.on('pageerror',e=>errors.push({message:e.message,stack:e.stack}));page.on('console',e=>{if(e.type()==='error')consoleErrors.push(e.text());});
  assert.equal(await page.evaluate(()=>window.__chicago4d.year),'1904');
  const entered=await page.evaluate(async()=>{const w=window.__chicago4d.welcome,deadline=Date.now()+90000;let accepted=false;
    while(w.state!=='world'&&Date.now()<deadline){if(w.state==='welcome')accepted=w.enter('spawn');if(w.state!=='world')await new Promise(r=>setTimeout(r,100));}
    return {accepted,state:w.state};});assert.deepEqual(entered,{accepted:true,state:'world'});
  assert.equal(await page.evaluate(()=>window.__chicago4d.detail),nativeDetail,'Native default tier is retained; no tier switch');
  const initial=await page.evaluate(zone=>{const a=window.__chicago4d;let near=null;a.railway.group.traverse(o=>{if(o.name===`railway-rails-z${zone}`)near={name:o.name,visible:o.visible};});return {year:a.year,detail:a.detail,pixelRatio:a.renderer.getPixelRatio(),welcome:a.welcome.state,camera:a.camera.position.toArray(),near};},plan.zone);
  await fs.writeFile(`${outputDir}/DEFAULT-FAR-PROTOCOL.json`,JSON.stringify({profile,nativeDetail,farOffset,initial,scope:'Default-profile far visual/drop-rebuild only; real initial1000m native eviction, no near-first or tier switch'},null,2));
  assert.equal(await page.evaluate(t=>window.__chicago4d.railway.cardFor(t.e,t.n).id,plan.targets.track),plan.targets.track.expectedId);
  const settle=async()=>{
    const row=await page.evaluate(async zone=>{const a=window.__chicago4d,frame=()=>new Promise(requestAnimationFrame);let count=0,stable=0,previous=null,state;
      const tick=async()=>{await frame();count++;const selected=[];a.railway.group.traverse(o=>{
        if(o.name===`railway-rails-z${zone}`||o.name===`railway-rails-far-z${zone}`)selected.push({name:o.name,uuid:o.uuid,geometry:o.geometry.uuid,visible:o.visible,
          keptBytes:Object.values(o.geometry.attributes).reduce((s,v)=>s+(v.array?.byteLength??0),0)+(o.geometry.index?.array?.byteLength??0)});
      });selected.sort((x,y)=>x.name.localeCompare(y.name));state={camera:[...a.camera.position.toArray(),...a.camera.quaternion.toArray()],detail:a.detail,selected,census:{...a.railway.census}};
      const sig=JSON.stringify(state);stable=sig===previous?stable+1:0;previous=sig;};
      const start=performance.now();for(let i=0;i<3;i++)await tick();const drain=performance.now();while(((a.residency?.pending??0)>0||stable<2)&&performance.now()-drain<120000)await tick();
      return {frames:count,stableTransitions:stable,pending:a.residency?.pending??0,seconds:(performance.now()-start)/1000,state};},plan.zone);
    settlements.push(row);await fs.writeFile(`${outputDir}/settlements.json`,JSON.stringify(settlements,null,2));assert.ok(row.frames>=3&&row.stableTransitions>=2);assert.equal(row.pending,0);return row;
  };
  const stand=async(n,lookBack)=>{
    const pose=await page.evaluate(({plan,n,lookBack})=>{const a=window.__chicago4d,t=plan.targets.track;a.setFly(true);
      a.walker.teleport({local_e:t.e,local_n:n,altitude_m:8,yaw_deg:45,pitch_deg:-60});
      const from=a.camera.position.toArray(),target=[t.e,a.terrain.surfaceHeight(t.e,t.n)+0.1,-t.n];
      if(lookBack){const de=target[0]-from[0],dn=-target[2]+from[2],dy=target[1]-from[1];
        const yaw_deg=Math.atan2(de,dn)*180/Math.PI,pitch_deg=Math.atan2(dy,Math.hypot(de,dn))*180/Math.PI;
        a.walker.teleport({local_e:t.e,local_n:n,altitude_m:8,yaw_deg,pitch_deg});
        return {from,target,yaw_deg,pitch_deg};}
      return {from,target};},{plan,n,lookBack});await settle();return pose;
  };
  const capture=async(label,pose)=>{
    await settle();const row=await page.evaluate(({plan,pose})=>{const a=window.__chicago4d;let near=null,far=null;
      a.railway.group.traverse(o=>{if(![ `railway-rails-z${plan.zone}`,`railway-rails-far-z${plan.zone}`].includes(o.name))return;
        const g=o.geometry,r={name:o.name,uuid:o.uuid,geometryUUID:g.uuid,visible:o.visible,positionCount:g.attributes.position.count,indexCount:g.index?.count??0,
          keptBytes:Object.values(g.attributes).reduce((s,v)=>s+(v.array?.byteLength??0),0)+(g.index?.array?.byteLength??0),markedForUploadRelease:g.userData.uploadReleased===true};
        if(o.name===`railway-rails-z${plan.zone}`)near=r;else far=r;});
      const p=a.project(pose.target[0],-pose.target[2],pose.target[1]);return {year:a.year,detail:a.detail,welcome:a.welcome.state,error:a.error,
        pixelRatio:a.renderer.getPixelRatio(),camera:a.camera.position.toArray(),pose,targetNDC:p,near,far,
        draw:{...a.renderer.info.render},pending:a.residency?.pending??0,glError:a.renderer.getContext().getError()};},{plan,pose});
    rows.push({label,...row});await fs.writeFile(`${outputDir}/FAR-CAMERA.json`,JSON.stringify({sourcePlanSha256:crypto.createHash('sha256').update(planBytes).digest('hex'),plan,rows,errors,consoleErrors},null,2));
    await page.screenshot({path:`${outputDir}/${label}.png`,timeout:90000});
    assert.equal(row.error,null);assert.equal(row.glError,0);assert.equal(row.pending,0);assert.equal(row.welcome,'world');assert.equal(row.detail,nativeDetail);assert.equal(row.pixelRatio,1);assert.ok(row.camera[1]<=30);assert.ok(Math.abs(row.camera[0]-plan.targets.track.e)<1e-6);assert.ok(Math.abs(row.camera[2]+plan.nHi+farOffset)<1e-6);
    assert.equal(row.near,null);assert.ok(row.far?.visible);assert.ok(row.far.positionCount>0&&row.far.indexCount>0);assert.ok(row.far.markedForUploadRelease);assert.equal(row.far.keptBytes,0,'Actually drawn selected far rails released CPU arrays');
    assert.ok(Object.values(row.targetNDC).every(Number.isFinite));assert.ok(Math.abs(row.targetNDC.x)<0.05&&Math.abs(row.targetNDC.y)<0.05&&row.targetNDC.z>-1&&row.targetNDC.z<1,'Selected source track centered in actual camera view');
    assert.ok(row.draw.calls>0&&row.draw.triangles>0,'Actual native frame drew geometry');assert.equal(errors.length,0);assert.equal(consoleErrors.length,0);return row;
  };
  // Clear any real arrival/boot cache through native reach eviction before the
  // 150m Light leg: final spawn alone does not prove the arrival never built near.
  await stand(plan.nHi+1000,false);
  const initiallyDropped=await page.evaluate(zone=>{let count=0;window.__chicago4d.railway.group.traverse(o=>{if(o.name===`railway-rails-z${zone}`||o.name===`railway-rails-far-z${zone}`)count++;});return count;},plan.zone);
  await fs.writeFile(`${outputDir}/NATIVE-EVICTIONS.json`,JSON.stringify({initial1000mSelectedGeometryCount:initiallyDropped},null,2));
  assert.equal(initiallyDropped,0,'Real initial reach eviction removes both selected near and far geometry before first far capture');
  const far=await capture('far-look-back',await stand(plan.nHi+farOffset,true));
  await stand(plan.nHi+1000,false);
  const dropped=await page.evaluate(zone=>{let count=0;window.__chicago4d.railway.group.traverse(o=>{if(o.name===`railway-rails-z${zone}`||o.name===`railway-rails-far-z${zone}`)count++;});return count;},plan.zone);await fs.writeFile(`${outputDir}/NATIVE-EVICTIONS.json`,JSON.stringify({initial1000mSelectedGeometryCount:initiallyDropped,rebuild1000mSelectedGeometryCount:dropped},null,2));assert.equal(dropped,0,'Selected zone genuinely dropped before rebuild');
  const rebuilt=await capture('far-look-back-rebuilt',await stand(plan.nHi+farOffset,true));
  assert.notEqual(rebuilt.far.uuid,far.far.uuid);assert.notEqual(rebuilt.far.geometryUUID,far.far.geometryUUID);assert.equal(rebuilt.far.positionCount,far.far.positionCount);assert.equal(rebuilt.far.indexCount,far.far.indexCount);
  await fs.writeFile(`${outputDir}/FAR-CAMERA-CLOSED.json`,JSON.stringify({result:'PASS actual default-profile supplemental camera guards; root visual inspection still required',profile,nativeDetail,farOffset,noTierSwitch:true,rows:rows.length,errors,consoleErrors},null,2));return {rows,errors,consoleErrors};
}
