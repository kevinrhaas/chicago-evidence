// Outside-app observer only. Starts no browser/server; does not replace native methods.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
export async function observeNativeRailwayLifecycle(page, outputDir) {
  await fs.mkdir(outputDir, {recursive:true});
  const errors=[], consoleErrors=[], rows=[], grades=['attested','inferred','reconstructed'];
  page.on('pageerror', e=>errors.push(e.message));
  page.on('console', e=>{if(e.type()==='error')consoleErrors.push(e.text());});
  // Native T-2186 readiness: ready precedes arrival's animation-frame settle.
  // Same bounded 90s welcome-state polling as smoke_renderer.mjs enterTown and measure_memory.mjs.
  // Still require an actual accepted spawn entry and world state; never force welcome/show or DOM.
  const enterSpawn=async()=>{
    const result=await page.evaluate(async()=>{
      const welcome=window.__chicago4d.welcome,deadline=Date.now()+90000;let accepted=false;
      while(welcome.state!=='world'&&Date.now()<deadline){
        if(welcome.state==='welcome')accepted=welcome.enter('spawn');
        if(welcome.state!=='world')await new Promise(r=>setTimeout(r,100));
      }
      return {accepted,state:welcome.state};
    });
    assert.deepEqual(result,{accepted:true,state:'world'},'Native bounded welcome → accepted spawn → world');
  };
  const settlements=[];
  // Native meter: >=3 real draws, then bounded residency drain. Railway.update is synchronous per tick.
  // Also require two consecutive stable native camera/zone/geometry/state samples; never hold or replace draws.
  const settle=async()=>{
    const row=await page.evaluate(async zone=>{
      const a=window.__chicago4d,frame=()=>new Promise(requestAnimationFrame),started=performance.now();
      let frames=0,stableTransitions=0,previous=null,current=null;
      const sample=()=>{
        const selected=[];a.railway.group.traverse(o=>{
          if(o.name!==`railway-rails-z${zone}`&&o.name!==`railway-rails-far-z${zone}`)return;
          selected.push({name:o.name,uuid:o.uuid,geometryUUID:o.geometry?.uuid,visible:o.visible,
            positionCount:o.geometry?.attributes.position?.count??null,indexCount:o.geometry?.index?.count??null,
            keptBytes:Object.values(o.geometry?.attributes??{}).reduce((s,v)=>s+(v.array?.byteLength??0),0)+(o.geometry?.index?.array?.byteLength??0),
            markedForUploadRelease:o.geometry?.userData.uploadReleased===true});
        });selected.sort((x,y)=>x.name.localeCompare(y.name));
        return {camera:[...a.camera.position.toArray(),...a.camera.quaternion.toArray()],detail:a.detail,season:a.season.current,
          welcome:a.welcome.state,census:{...a.railway.census},selected,
          confidence:{enabled:a.confidence.enabled,hidden:{...a.confidence.hidden},modes:{...a.confidence.modes},
            looks:Object.fromEntries(['attested','inferred','reconstructed'].map(g=>[g,a.confidence.grade(g)]))}};
      };
      const tick=async()=>{await frame();frames++;current=sample();const signature=JSON.stringify(current);
        stableTransitions=signature===previous?stableTransitions+1:0;previous=signature;};
      for(let i=0;i<3;i++)await tick();
      const drainStarted=performance.now(),pendingAtRead=a.residency?.pending??0;
      while(((a.residency?.pending??0)>0||stableTransitions<2)&&performance.now()-drainStarted<120000)await tick();
      return {frames,stableTransitions,pendingAtRead,pending:a.residency?.pending??0,
        seconds:(performance.now()-started)/1000,drainSeconds:(performance.now()-drainStarted)/1000,state:current};
    },plan.zone);
    settlements.push(row);await fs.writeFile(`${outputDir}/settlements.json`,JSON.stringify(settlements,null,2));
    assert.ok(row.frames>=3,'At least three actual native animation frames');
    assert.equal(row.pending,0,'Actual native residency upload queue drained');
    assert.ok(row.stableTransitions>=2,'Native selected zone/camera/detail/confidence/season settled across real frames');
    return row;
  };
  assert.equal(await page.evaluate(()=>window.__chicago4d?.year),'1904');
  await enterSpawn();
  await page.evaluate(()=>window.__chicago4d.setDetail('full'));
  // Choose native source points in one middle zone; no pick result is used to select them.
  const plan=await page.evaluate(()=>{
    const a=window.__chicago4d,d=a.railway.data,tracks=d.tracks.filter(t=>t.centreline_local_m?.length>=2);
    const ns=tracks.flatMap(t=>t.centreline_local_m.map(p=>p[1])),nTop=Math.max(...ns),nBottom=Math.min(...ns);
    const zone=Math.floor(Math.ceil((nTop-nBottom)/110)/2),nHi=nTop-zone*110,nLo=nHi-110,nMid=(nHi+nLo)/2;
    const zoneOf=n=>Math.floor((nTop-n)/110);
    const interiors=(st)=>{const out=[];for(let i=0;i+1<st.length;i++){
      const x=st[i],y=st[i+1],quad=[[x[0],x[1]],[y[0],y[1]],[y[2],y[3]],[x[2],x[3]]];
      const e=quad.reduce((s,p)=>s+p[0],0)/4,n=quad.reduce((s,p)=>s+p[1],0)/4;
      if(zoneOf(n)===zone&&n<nHi-10&&n>nLo+10)out.push({e,n,quad,stationPair:[i,i+1]});
    }return out.sort((x,y)=>Math.abs(x.n-nMid)-Math.abs(y.n-nMid));};
    const ground=interiors(d.right_of_way?.cinders??[])[0],edge=interiors(d.lake_edge?.face??[])[0];
    if(!ground||!edge)throw Error('No adjacent-station quad interior in selected native zone');
    let track=null;
    for(const t of tracks){const line=t.centreline_local_m;
      for(let i=0;i+1<line.length;i++){const p=line[i],q=line[i+1];if((p[1]-nMid)*(q[1]-nMid)>0||p[1]===q[1])continue;
        const f=(nMid-p[1])/(q[1]-p[1]),e=p[0]+f*(q[0]-p[0]);
        const expectedId=`railway.${t.id}`;
        if(a.railway.cardFor(e,nMid).id===expectedId){track={e,n:nMid,sourceTrack:t.id,sourceSegment:[p,q],expectedId};break;}
      }if(track)break;
    }
    if(!track)throw Error('No unambiguous source track in selected zone');
    // railwayCard legitimately assigns cinders near a track that track's card (<3.5m).
    ground.expectedId=a.railway.cardFor(ground.e,ground.n).id;
    edge.expectedId='railway.lake_edge'; // native edgeCard(data).id, railway.js1308.
    return {zone,nHi,nLo,targets:{track,ground,edge}};
  });
  await fs.writeFile(`${outputDir}/source-plan.json`,JSON.stringify(plan,null,2));
  const stand=async(e,n)=>{await page.evaluate(({e,n})=>{
    const a=window.__chicago4d;a.setFly(true);
    a.walker.teleport({local_e:e-3,local_n:n-3,altitude_m:8,yaw_deg:45,pitch_deg:-60});
  },{e,n});await settle();};
  const record=async(label)=>{
    await settle();
    const row=await page.evaluate(zone=>{
      const a=window.__chicago4d,geometries=[];
      a.railway.group.traverse(o=>{if(o.geometry)geometries.push({name:o.name,uuid:o.uuid,geometryUUID:o.geometry.uuid,
        parentUUID:o.parent?.uuid,visible:o.visible,positionCount:o.geometry.attributes.position?.count??null,
        indexCount:o.geometry.index?.count??null,keptBytes:Object.values(o.geometry.attributes).reduce((s,v)=>s+(v.array?.byteLength??0),0)+(o.geometry.index?.array?.byteLength??0),
        materials:[].concat(o.material??[]).map(m=>({name:m.name,type:m.type}))});});
      return {year:a.year,detail:a.detail,welcome:a.welcome.state,error:a.error,season:a.season.current,
        confidence:{enabled:a.confidence.enabled,hidden:a.confidence.hidden,modes:a.confidence.modes,
          looks:Object.fromEntries(['attested','inferred','reconstructed'].map(g=>[g,a.confidence.grade(g)]))},
        camera:{x:a.camera.position.x,y:a.camera.position.y,z:a.camera.position.z},
        census:{...a.railway.census},release:{...a.uploadRelease},geometries,
        selected:{near:geometries.find(g=>g.name===`railway-rails-z${zone}`)??null,
          far:geometries.find(g=>g.name===`railway-rails-far-z${zone}`)??null},
        glError:a.renderer.getContext().getError()};
    },plan.zone);
    rows.push({label,...row});await fs.writeFile(`${outputDir}/lifecycle.json`,JSON.stringify({plan,rows,errors,consoleErrors},null,2));
    await page.screenshot({path:`${outputDir}/${label}.png`});
    assert.equal(row.error,null);assert.equal(row.glError,0);assert.equal(errors.length,0);assert.equal(row.welcome,'world');
    return row;
  };
  const picks=async()=>{const results={};for(const[name,target]of Object.entries(plan.targets)){
    await stand(target.e,target.n);
    results[name]=await page.evaluate(({e,n})=>{const a=window.__chicago4d;
      const p=a.project(e,n,a.terrain.surfaceHeight(e,n)+0.024),h=a.railway.pickAt(p,a.camera);
      return {id:h?.id??null,distance:h?.distance??null,point:h?.point?.toArray()??null,ndc:p};},target);
    const hit=results[name];assert.ok(Object.values(hit.ndc).every(Number.isFinite));
    assert.ok(Math.abs(hit.ndc.x)<1&&Math.abs(hit.ndc.y)<1&&hit.ndc.z>-1&&hit.ndc.z<1,`${name}: target in view`);
    assert.equal(hit.id,target.expectedId,`${name}: exact source/native card identity`);
    assert.ok(Number.isFinite(hit.distance)&&hit.distance>0);
  }return results;};
  const initialPicks=await picks(),{e,n}=plan.targets.track;
  await stand(e,n);const near=await record('full-near');
  assert.equal(near.selected.near?.keptBytes,0,'Drawn near rails released CPU arrays after native upload');
  assert.equal(near.detail,'full');assert.ok(near.selected.near?.visible);assert.ok(!near.selected.far?.visible);
  await stand(e,plan.nHi+350);const far=await record('full-far');
  assert.equal(far.selected.near,null);assert.ok(far.selected.far?.visible);
  await stand(e,plan.nHi+1000);const dropped=await record('full-dropped');
  assert.equal(dropped.selected.near,null);assert.equal(dropped.selected.far,null);
  await stand(e,n);const rebuilt=await record('full-near-return');
  assert.equal(rebuilt.selected.near?.keptBytes,0,'Rebuilt near rails released CPU arrays after native upload');
  assert.ok(rebuilt.selected.near?.visible);assert.notEqual(rebuilt.selected.near.uuid,near.selected.near.uuid);
  assert.notEqual(rebuilt.selected.near.geometryUUID,near.selected.near.geometryUUID);
  assert.equal(rebuilt.selected.near.positionCount,near.selected.near.positionCount);
  assert.equal(rebuilt.selected.near.indexCount,near.selected.near.indexCount);
  await stand(e,plan.nHi+350);const farRebuilt=await record('full-far-return');
  assert.ok(farRebuilt.selected.far?.visible);assert.notEqual(farRebuilt.selected.far.uuid,far.selected.far.uuid);
  assert.notEqual(farRebuilt.selected.far.geometryUUID,far.selected.far.geometryUUID);
  assert.equal(farRebuilt.selected.far.positionCount,far.selected.far.positionCount);
  assert.equal(farRebuilt.selected.far.indexCount,far.selected.far.indexCount);await stand(e,n);
  const beforeConfidence=await record('confidence-before');
  for(const mode of ['ghost','hidden','restored']){
    await page.evaluate(({mode,previous})=>{const a=window.__chicago4d;
      a.setConfidenceView(mode==='restored'?previous.enabled:true);
      for(const grade of ['attested','inferred','reconstructed']){
        a.confidence.setHidden(grade,mode==='restored'?previous.hidden[grade]:mode==='hidden');
        a.confidence.setGrade(grade,mode==='restored'?previous.looks[grade]:{mode:mode==='ghost'?'ghost':'tint',opacity:mode==='ghost'?0.4:1});
      }},{mode,previous:beforeConfidence.confidence});
    const row=await record(`confidence-${mode}`);
    if(mode==='restored')assert.deepEqual(row.confidence,beforeConfidence.confidence);
    else{assert.equal(row.confidence.enabled,true);for(const g of grades){assert.equal(row.confidence.hidden[g],mode==='hidden');assert.equal(row.confidence.modes[g],mode==='ghost'?'ghost':'tint');assert.equal(row.confidence.looks[g].opacity,mode==='ghost'?0.4:1);}}
  }
  for(const season of ['winter','summer']){await page.evaluate(s=>window.__chicago4d.season.set(s),season);const row=await record(`season-${season}`);assert.equal(row.season,season);}
  for(const detail of ['balanced','full']){await page.evaluate(d=>window.__chicago4d.setDetail(d),detail);const row=await record(`detail-${detail}`);assert.equal(row.detail,detail);assert.ok(row.selected.near?.visible);}
  const finalPicks=await picks();
  const beforeReload=await page.evaluate(()=>({reloads:window.__chicago4d.crashGuard.reloads,page:window.__chicago4d.blackbox?.box?.page}));
  assert.equal(beforeReload.reloads,0,'Use a fresh native context for ordinary context restore');
  await fs.writeFile(`${outputDir}/picks-before-context.json`,JSON.stringify({plan,initialPicks,finalPicks,beforeReload},null,2));
  const navigation=page.waitForNavigation({waitUntil:'domcontentloaded',timeout:240000});
  await page.evaluate(async()=>{const gl=window.__chicago4d.renderer.getContext(),ext=gl.getExtension('WEBGL_lose_context');
    if(!ext)throw Error('Native context-loss extension unavailable');
    const lost=new Promise(r=>gl.canvas.addEventListener('webglcontextlost',r,{once:true}));
    ext.loseContext();await lost;await new Promise(r=>setTimeout(r,50));ext.restoreContext();});
  await navigation;await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000});
  await enterSpawn();await settle();
  assert.deepEqual(await page.evaluate(()=>({reloads:window.__chicago4d.crashGuard.reloads,welcome:window.__chicago4d.welcome.state,detail:window.__chicago4d.detail})),{reloads:1,welcome:'world',detail:'full'});
  const restoredPicks=await picks();const restored=await record('context-restored');
  assert.equal(restored.detail,'full');
  await fs.writeFile(`${outputDir}/picks-and-context.json`,JSON.stringify({plan,initialPicks,finalPicks,restoredPicks,beforeReload,errors,consoleErrors},null,2));
  assert.equal(consoleErrors.length,0,'Inspect every browser/GL console error');
  return {rows,initialPicks,finalPicks,restoredPicks,errors,consoleErrors};
}
