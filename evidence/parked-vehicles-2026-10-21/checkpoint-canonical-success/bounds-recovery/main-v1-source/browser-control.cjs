// Adapted from parked-scene-capture-2026-10-21.cjs. Harness-only state is restored.
module.exports = async function installCoveredMain(contract) {
  const a=window.__chicago4d,T=await import('three'),p=a?.parkedTransport;
  const need=(ok,text)=>{if(!ok)throw Error(text);};
  need(a?.ready&&String(a.year)==='1835'&&p&&a.yard,'Actual 1835 main parked/yard APIs required');
  need(a.detail===contract.detail,'Explicit requested detail tier must be active');
  const manifest=await(await fetch(new URL('transport/parked/placements.json',a.dataBase))).json();
  const oldRows=new Map(a.yard.wagons.map(r=>[r.id,r]));
  need(p.instances.length===5,'Expected three existing W01s and exactly two covered instances');
  const targets=new Map(),originalMeshVisibility=new Map();let oldMode=false,current=null;
  const standardFallback=(id,visible)=>a.yard.setReplacementVisible(id,visible);
  const fallback=(id,visible)=>standardFallback(id,oldMode&&current?.cfg.originalId===id?true:visible);
  p.setFallback(fallback);
  function frame(){a.step();a.step();a.renderer.getContext().finish();const s=a.stats();return{
    driverDraws:s.drawCalls,rendererCalls:s.rendererCalls,triangles:s.triangles,budget:s.budget,
    withinBudget:s.withinBudget,geometries:s.geometries,textures:s.textures,glError:a.renderer.getContext().getError()};}
  function goodFrame(s){need(s.withinBudget===true&&s.glError===0,'Actual canonical budget/GL guard failed');return s;}
  function lights(){const list=[];a.scene3d.traverse(n=>{if(n.isLight)list.push({name:n.name,type:n.type,
    intensity:n.intensity,color:n.color?.getHexString(),position:n.position.toArray(),castShadow:n.castShadow,
    shadow:n.shadow?{bias:n.shadow.bias,normalBias:n.shadow.normalBias,mapSize:n.shadow.mapSize.toArray()}:null});});return{
    shadowEnabled:a.renderer.shadowMap.enabled,shadowType:a.renderer.shadowMap.type,toneMapping:a.renderer.toneMapping,
    exposure:a.renderer.toneMappingExposure,list};}
  for(const cfg of contract.targets){
    const i=p.instances.find(i=>i.row.replaces===cfg.originalId),old=oldRows.get(cfg.originalId);
    need(i&&i.row.model===cfg.model&&old?.kind==='covered'&&old.yoke===true,'Exact original covered/yoke identity required');
    need(JSON.stringify(old.at_local_enu_m)===JSON.stringify(cfg.at)&&old.bearing_deg===cfg.bearing,'Original stand/bearing changed');
    need(JSON.stringify(i.row.at_local_enu_m)===JSON.stringify(cfg.at)&&i.row.bearing_deg===cfg.bearing,'Replacement moved');
    need(i.draw_batches===9,'Expected nine actual static material groups');
    const meshes=[];a.yard.group.traverse(n=>{if(n.isMesh)meshes.push(n);});
    a.yard.setReplacementVisible(cfg.originalId,false);const before=meshes.map(n=>n.visible);
    a.yard.setReplacementVisible(cfg.originalId,true);const changed=meshes.filter((n,k)=>n.visible!==before[k]);
    need(changed.length===1,'Original ID must control exactly one real legacy chunk');
    p.update(a.camera);i.group.traverse(n=>{if(n.isMesh)originalMeshVisibility.set(n,n.visible);});
    targets.set(cfg.originalId,{cfg,i,old,oldMesh:changed[0]});
  }
  function select(id,mode='refined'){
    for(const[n,v]of originalMeshVisibility)n.visible=v;
    current=targets.get(id);need(current,'Unknown covered target');oldMode=mode==='legacy';
    if(oldMode)current.i.group.traverse(n=>{if(n.isMesh)n.visible=false;});
    p.update(a.camera);
  }
  const corners=box=>{const out=[];for(const x of[box.min.x,box.max.x])for(const y of[box.min.y,box.max.y])for(const z of[box.min.z,box.max.z])out.push(new T.Vector3(x,y,z));return out;};
  function view(id,angle){
    select(id);const{cfg,i,oldMesh}=current;i.group.updateMatrixWorld(true);oldMesh.updateMatrixWorld(true);
    const whole=new T.Box3().setFromObject(i.group).union(new T.Box3().setFromObject(oldMesh));
    let box=whole.clone();if(angle==='close'){
      box=new T.Box3();for(const x of[-.60,.60])for(const y of[1.4,2.65])for(const z of[-1.70,1.70])box.expandByPoint(new T.Vector3(x,y,z).applyMatrix4(i.group.matrixWorld));
    }
    const centre=box.getCenter(new T.Vector3()),local=angle==='side'?new T.Vector3(1,0,.01):new T.Vector3(.9,0,1);
    local.applyQuaternion(i.group.quaternion).normalize();const right=new T.Vector3().crossVectors(new T.Vector3(0,1,0),local).normalize();
    const tv=Math.tan(a.camera.fov*Math.PI/360),th=tv*a.camera.aspect;let distance=angle==='distant'?45:4;
    for(const v of corners(box)){const q=v.clone().sub(centre),d=q.dot(local);distance=Math.max(distance,d+Math.abs(q.dot(right))/(th*.88),d+Math.abs(q.y)/(tv*.88));}
    let bounds,pose;
    for(let attempt=0;attempt<6;attempt++){
      const eye=centre.clone().addScaledVector(local,distance),e=eye.x,n=-eye.z,yaw=Math.atan2(centre.x-e,-centre.z-n)*180/Math.PI;
      const aerial=angle==='distant';a.setFly(aerial);a.walker.teleport({local_e:e,local_n:n,yaw_deg:yaw,pitch_deg:0,altitude_m:aerial?6:null});
      const pitch=Math.atan2(centre.y-a.walker.state.eyeY,Math.hypot(centre.x-e,centre.z-eye.z))*180/Math.PI;
      a.walker.teleport({local_e:e,local_n:n,yaw_deg:yaw,pitch_deg:pitch,altitude_m:aerial?6:null});goodFrame(frame());
      const pp=corners(box).map(v=>v.project(a.camera));bounds={minX:Math.min(...pp.map(v=>v.x)),maxX:Math.max(...pp.map(v=>v.x)),minY:Math.min(...pp.map(v=>v.y)),maxY:Math.max(...pp.map(v=>v.y)),near:Math.min(...pp.map(v=>v.z)),far:Math.max(...pp.map(v=>v.z))};
      pose={...a.walker.state};if(Math.max(...[bounds.minX,bounds.maxX,bounds.minY,bounds.maxY].map(Math.abs))<.95&&bounds.near>-1&&bounds.far<1)break;
      distance*=1.22;
    }
    need(Math.max(...[bounds.minX,bounds.maxX,bounds.minY,bounds.maxY].map(Math.abs))<.95,'Reference union/crop does not fit view');
    need(i.group.visible,'Refined comparison fell outside actual detail reach');
    return{id,angle,pose,bounds,framing:angle==='close'?'canopy crop; lower vehicle intentionally outside frame':'union of actual old/new whole vehicle including tongue and yoke',aerialInspection:angle==='distant'};
  }
  function capture(id,mode){
    select(id,mode);const draw=goodFrame(frame());const {i,oldMesh}=current;
    need(i.group.visible,'Target group must remain within its production detail reach');
    const anyNew=i.group.children.some(n=>n.isMesh&&n.visible);
    need(mode==='legacy'?(!anyNew&&oldMesh.visible):(anyNew&&!oldMesh.visible),'Old/new duplication or missing fallback');
    return{mode,draw,pose:{...a.walker.state},camera:a.camera.matrixWorld.toArray(),projection:a.camera.projectionMatrix.toArray(),
      lighting:lights(),detail:a.detail,actualCanvas:[a.renderer.domElement.width,a.renderer.domElement.height],
      oldChunk:{uuid:oldMesh.uuid,visible:oldMesh.visible},refined:{id:i.row.id,visible:i.group.visible,anyChildVisible:anyNew,
      batches:i.draw_batches,wheelPlaneSpan_m:i.wheel_clearance_m,parking:i.parking},problems:a.problems};
  }
  async function controls(id){
    select(id);const{cfg,i,oldMesh}=current,normal=goodFrame(frame()),visibility=i.group.children.map(n=>n.visible);let hidden;
    try{i.group.children.forEach(n=>n.visible=false);hidden=goodFrame(frame());}finally{i.group.children.forEach((n,k)=>n.visible=visibility[k]);}
    const restored=goodFrame(frame()),delta={driverDraws:restored.driverDraws-hidden.driverDraws,rendererCalls:restored.rendererCalls-hidden.rendererCalls,triangles:restored.triangles-hidden.triangles};
    need(delta.driverDraws>0,'No actual covered driver-draw contribution at front-quarter view');
    let hit=null,ndc=null;
    for(const mesh of i.group.children){if(!mesh.isMesh||!mesh.material.name.includes('canvas'))continue;const attr=mesh.geometry.getAttribute('position');
      for(let k=0;k<attr.count;k+=Math.max(3,Math.floor(attr.count/24/3)*3)){
        const point=new T.Vector3().fromBufferAttribute(attr,k).applyMatrix4(mesh.matrixWorld),v=point.clone().project(a.camera);if(Math.abs(v.x)>.85||Math.abs(v.y)>.85)continue;
        const localHit=p.pickAt({x:v.x,y:v.y},a.camera);if(localHit?.id!==i.row.id)continue;
        const global=a.pick({x:v.x,y:v.y});if(global?.id===i.row.id){hit=global;ndc={x:v.x,y:v.y};break;}a.popup.close();
      }if(hit)break;
    }
    need(hit?.id===i.row.id,'Actual global scene pick did not reach the visible covered model');
    const root=document.getElementById('popup');let popup;
    try{
      need(a.popup.openId===i.row.id&&!root.hidden,'Actual picked popup is not visible');
      const tab=root.querySelector('[data-pop-tab="evidence"]');need(tab,'Sources tab missing');tab.click();
      for(const button of root.querySelectorAll('#pop-pane-evidence [data-toggle-note]'))button.click();
      const text=root.innerText;const checks={name:text.includes(i.card.sidecar.name),covered:/Covered wagon/.test(text),reconstructed:/reconstructed/i.test(text),
        maker:/Unidentified; type reconstruction/.test(text),empty:/Unoccupied and unhitched/.test(text),ownership:/without a driver, passengers or a claim of ownership/.test(text),
        yoke:/laid-by ox yoke/.test(text),unsupported:/unsupported/.test(text)};
      need(Object.values(checks).every(Boolean),'Actual popup omits covered identity/limitations');
      const liberty=root.querySelector('[data-pop-tab="liberties"]');need(liberty,'Liberties tab missing');liberty.click();
      popup={ndc,globalPickId:hit.id,text,libertiesText:root.innerText,checks};
    }finally{a.popup.close();}need(a.popup.openId===null&&root.hidden,'Popup did not close');
    const confidenceEnabled=a.confidence.enabled,wasHidden=a.confidence.hidden.reconstructed;let confidence;
    try{
      a.setConfidenceView(true);const tinted=goodFrame(frame());a.confidence.setHidden('reconstructed',true);const hiddenDraw=goodFrame(frame());
      const pick=p.pickAt(ndc,a.camera);need(pick===null,'Hidden reconstructed covered prop remains pickable');
      need(i.group.children.every(m=>m.geometry.getAttribute('_confidence')?.array.every(v=>v===1)),'Covered batches lack reconstructed confidence channel');
      confidence={tinted,hidden:hiddenDraw,pickWhenHidden:pick,hiddenUniform:a.confidence.hidden.reconstructed,scope:'Actual confidence shader frames/geometry and hidden pick; no separate confidence screenshot'};
    }finally{a.confidence.setHidden('reconstructed',wasHidden);a.setConfidenceView(confidenceEnabled);}goodFrame(frame());
    const tier=a.detail;await p.setTier('light');const light=goodFrame(frame());need(!i.group.visible&&oldMesh.visible,'Parked Light policy did not restore actual old chunk');
    await p.setTier(tier);goodFrame(frame());need(i.group.visible&&!oldMesh.visible,'Restored detail did not restore refined/old exclusivity');
    const saved={...a.walker.state},yaw=saved.yaw*180/Math.PI; // restore through exact saved camera pose below
    const cameraPose={local_e:saved.e,local_n:saved.n,yaw_deg:-yaw,pitch_deg:saved.pitch*180/Math.PI,altitude_m:saved.flying?saved.altitude:null};
    try{a.walker.teleport({local_e:cfg.at[0]+130,local_n:cfg.at[1],yaw_deg:270,altitude_m:null});const far=goodFrame(frame());need(!i.group.visible&&oldMesh.visible,'Far policy did not restore actual old chunk');
      return{normal,hidden,restored,delta,popup,confidence,light,far,scope:'Light changes parked-module policy only; full app default-Light remains normal smoke scope'};
    }finally{a.setFly(saved.flying);a.walker.teleport(cameraPose);select(id);goodFrame(frame());}
  }
  async function clearance(id){
    select(id);const{cfg,i}=current;goodFrame(frame());
    const raw=await(await fetch(new URL(manifest.models[i.row.model].file,location.href))).arrayBuffer();
    const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',raw))].map(b=>b.toString(16).padStart(2,'0')).join('');need(hash===cfg.glbSha256,'Authoritative covered GLB differs from reviewed model');
    const dv=new DataView(raw),length=dv.getUint32(12,true),g=JSON.parse(new TextDecoder().decode(new Uint8Array(raw,20,length))),bin=28+length;
    need(!g.extensionsUsed?.includes('EXT_meshopt_compression')&&!g.extensionsUsed?.includes('KHR_draco_mesh_compression'),'Compressed geometry requires its actual decoded fixture, not a raw-accessor assumption');
    const nodes=g.nodes.map(n=>{const o=new T.Object3D();o.name=n.name;if(n.matrix)o.applyMatrix4(new T.Matrix4().fromArray(n.matrix));else{if(n.translation)o.position.fromArray(n.translation);if(n.rotation)o.quaternion.fromArray(n.rotation);if(n.scale)o.scale.fromArray(n.scale);}return o;});
    g.nodes.forEach((n,k)=>(n.children||[]).forEach(c=>nodes[k].add(nodes[c])));const scene=new T.Group();for(const root of g.scenes[g.scene||0].nodes)scene.add(nodes[root]);
    const tongue=scene.getObjectByName('vehicle_tongue');need(tongue&&i.parking,'Actual parking articulation missing');tongue.rotation.x=i.parking.angle_rad;scene.updateMatrixWorld(true);i.group.updateMatrixWorld(true);
    const result={glbSha256:hash,parts:{},actualWheelPlaneSpan_m:i.wheel_clearance_m,actualParking:i.parking,projectedPoints:[]},sourceBox=new T.Box3();
    for(let n=0;n<g.nodes.length;n++){const node=g.nodes[n];if(node.mesh===undefined)continue;let part=node.name==='covered_preserved_laid_by_yoke'?'yoke':'gear';for(let q=nodes[n];q;q=q.parent)if(q.name==='vehicle_body')part='body';
      const summary=result.parts[part]||(result.parts[part]={vertices:0,minGroundClearance_m:Infinity});
      const matrix=new T.Matrix4().multiplyMatrices(i.group.matrixWorld,nodes[n].matrixWorld);
      for(const primitive of g.meshes[node.mesh].primitives){const accessor=g.accessors[primitive.attributes.POSITION],bv=g.bufferViews[accessor.bufferView];need(accessor.componentType===5126&&accessor.type==='VEC3'&&!accessor.sparse&&!bv.byteStride,'Actual raw float accessor required');
        const array=new Float32Array(raw,bin+(bv.byteOffset||0)+(accessor.byteOffset||0),accessor.count*3);
        for(let k=0;k<array.length;k+=3){const v=new T.Vector3(array[k],array[k+1],array[k+2]).applyMatrix4(matrix),ground=a.terrain.surfaceHeight(v.x,-v.z);need(Number.isFinite(ground),'Nonfinite actual terrain under source vertex');summary.vertices++;summary.minGroundClearance_m=Math.min(summary.minGroundClearance_m,v.y-ground);sourceBox.expandByPoint(v);result.projectedPoints.push([v.x,-v.z]);}
      }
    }
    const actualBox=new T.Box3().setFromObject(i.group);need(sourceBox.min.distanceTo(actualBox.min)<.0001&&sourceBox.max.distanceTo(actualBox.max)<.0001,'Source partitions do not match actual parked merged world bounds');
    need(result.parts.body?.minGroundClearance_m>=-.00001&&result.parts.yoke?.minGroundClearance_m>=-.00001,'Actual body/yoke vertex penetrates sampled terrain');
    const enclosure=await(await fetch(new URL('enclosures/'+cfg.enclosure+'.json',a.dataBase))).json(),ring=enclosure.ground.interior_local_enu_m;
    const cross=(a,b,c)=>(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
    const sorted=[...new Map(result.projectedPoints.map(p=>[p.join(','),p])).values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]),lo=[],hi=[];
    for(const p of sorted){while(lo.length>1&&cross(lo.at(-2),lo.at(-1),p)<=0)lo.pop();lo.push(p);}for(const p of [...sorted].reverse()){while(hi.length>1&&cross(hi.at(-2),hi.at(-1),p)<=0)hi.pop();hi.push(p);}const hull=lo.slice(0,-1).concat(hi.slice(0,-1));
    const inside=p=>{let yes=false;for(let k=0,j=ring.length-1;k<ring.length;j=k++){const a=ring[k],b=ring[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;};
    const pointDistance=(p,a,b)=>{const dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy||1)));return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy);};
    const segmentDistance=(a,b,c,d)=>{if(cross(a,b,c)*cross(a,b,d)<=0&&cross(c,d,a)*cross(c,d,b)<=0&&Math.max(Math.min(a[0],b[0]),Math.min(c[0],d[0]))<=Math.min(Math.max(a[0],b[0]),Math.max(c[0],d[0]))&&Math.max(Math.min(a[1],b[1]),Math.min(c[1],d[1]))<=Math.min(Math.max(a[1],b[1]),Math.max(c[1],d[1])))return 0;return Math.min(pointDistance(a,c,d),pointDistance(b,c,d),pointDistance(c,a,b),pointDistance(d,a,b));};
    need(hull.every(inside),'Actual whole-vehicle hull leaves its authored yard interior');let boundaryGap=Infinity;
    for(let k=0;k<hull.length;k++)for(let j=0;j<ring.length;j++)boundaryGap=Math.min(boundaryGap,segmentDistance(hull[k],hull[(k+1)%hull.length],ring[j],ring[(j+1)%ring.length]));
    const postEnvelope=(enclosure.form.post_size_m?.value??.14)*Math.SQRT2/2;need(boundaryGap>postEnvelope,'Actual projected vehicle hull reaches yard boundary/post envelope');result.yard={enclosure:cfg.enclosure,minHullBoundaryGap_m:boundaryGap,postEnvelopeRadius_m:postEnvelope,hull};
    const boxes=a.buildings.instanceBounds();result.hosts=[];
    for(const host of enclosure.belongs_to){const bound=boxes[host],position=a.buildings.positionOf(host);need(bound&&position,'Actual rendered host bounds missing '+host);
      const side=await(await fetch(new URL('sidecars/1835/'+host+'.json',a.dataBase))).json(),matrix=new T.Matrix4().compose(position,new T.Quaternion().setFromEuler(new T.Euler(0,-(side.placement.rotation_deg||0)*Math.PI/180,0)),new T.Vector3(1,1,1));
      const box=new T.Box3().setFromPoints(corners(new T.Box3(new T.Vector3().fromArray(bound.min),new T.Vector3().fromArray(bound.max))).map(v=>v.applyMatrix4(matrix)));
      const dx=Math.max(box.min.x-actualBox.max.x,actualBox.min.x-box.max.x,0),dz=Math.max(box.min.z-actualBox.max.z,actualBox.min.z-box.max.z,0),gap=Math.hypot(dx,dz);
      need(gap>0,'Conservative actual host bounds overlap; inspect true geometry before accepting '+host);result.hosts.push({id:host,conservativePlanBoxGap_m:gap,worldMin:box.min.toArray(),worldMax:box.max.toArray()});
    }
    delete result.projectedPoints;result.scope='All authoritative source vertices under actual runtime articulation/world transform; source bounds equal actual merged bounds. Terrain vertex samples plus conservative yard hull/actual rendered host boxes, not an occupied collision interface or a ground-triangle raycast.';return result;
  }
  function cleanup(){for(const[n,v]of originalMeshVisibility)n.visible=v;oldMode=false;p.setFallback(standardFallback);p.update(a.camera);}
  function disposeCheck(){cleanup();p.dispose();const draw=goodFrame(frame());need(p.instances.length===0&&[...targets.values()].every(t=>t.oldMesh.visible),'Actual main disposal did not restore both old chunks');return{draw,instances:p.instances.length,legacyChunks:[...targets.values()].map(t=>({id:t.cfg.originalId,visible:t.oldMesh.visible})),scope:'End-of-page destructive runtime disposal only; browser page closes immediately afterwards'};}
  window.__coveredInspection={view,capture,controls,clearance,cleanup,disposeCheck};
  return{targets:[...targets.values()].map(t=>({original:t.old,id:t.i.row.id,model:t.i.row.model,oldChunkUuid:t.oldMesh.uuid})),lighting:lights(),detail:a.detail};
};
