// SPDX-License-Identifier: GPL-3.0-or-later
import * as T from 'three';
import {GLTFLoader} from '../../vendor/three-0.185.1/addons/loaders/GLTFLoader.js';
const canvas=document.querySelector('canvas');
const renderer=new T.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;
renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.3;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
const scene=new T.Scene();scene.background=new T.Color('#e9e7df');
scene.add(new T.HemisphereLight(0xe5f1ff,0x8d7b57,2.6));
const sun=new T.DirectionalLight(0xfff3d7,3.8);sun.position.set(4,8,5);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.bias=-.0002;scene.add(sun);
const floor=new T.Mesh(new T.PlaneGeometry(100,100),new T.MeshStandardMaterial({color:0xc9c7b9,roughness:1}));
floor.rotation.x=-Math.PI/2;floor.position.y=-.004;floor.receiveShadow=true;scene.add(floor);
const hypothesis=await(await fetch('./camera-hypothesis.json')).json();
const response=await fetch('./brougham.glb');if(!response.ok)throw Error('BroughamHTTP'+response.status);
const buffer=await response.arrayBuffer();const gltf=await new GLTFLoader().parseAsync(buffer,'');
const model=gltf.scene.getObjectByName('vehicle_root');scene.add(model);
model.traverse(n=>{if(n.isMesh){n.castShadow=true;n.receiveShadow=true;}});model.updateMatrixWorld(true);
const pole=model.getObjectByName('vehicle_team_pole');
const full=new T.Box3().setFromObject(model,true);pole.visible=false;
const body=new T.Box3();
model.traverse(n=>{if(!n.isMesh)return;let a=n;while(a&&a!==pole)a=a.parent;if(a===pole)return;body.union(new T.Box3().setFromObject(n,true));});
pole.visible=true;
const corners=b=>{const out=[];for(const x of[b.min.x,b.max.x])for(const y of[b.min.y,b.max.y])for(const z of[b.min.z,b.max.z])out.push(new T.Vector3(x,y,z));return out;};
scene.updateMatrixWorld(true);sun.shadow.updateMatrices(sun);
const caster=corners(full),ray=sun.position.clone().normalize().multiplyScalar(-1);
const floorPoints=caster.map(p=>{const d=(floor.position.y-p.y)/ray.y;return p.clone().addScaledVector(ray,d);});
const lightPoints=[...caster,...floorPoints].map(p=>p.clone().applyMatrix4(sun.shadow.camera.matrixWorldInverse));
Object.assign(sun.shadow.camera,{left:Math.min(...lightPoints.map(p=>p.x))-.15,right:Math.max(...lightPoints.map(p=>p.x))+.15,bottom:Math.min(...lightPoints.map(p=>p.y))-.15,top:Math.max(...lightPoints.map(p=>p.y))+.15,near:Math.max(.01,Math.min(...lightPoints.map(p=>-p.z))-.25),far:Math.max(...lightPoints.map(p=>-p.z))+.25});
sun.shadow.camera.updateProjectionMatrix();sun.shadow.updateMatrices(sun);
const ortho=new T.OrthographicCamera(-2,2,2,-2,.05,100),perspective=new T.PerspectiveCamera(40,1,.05,100);
let activeCamera=ortho,current='reference',disposed=false;
function fit(name){
  current=name;const reference=name==='reference';pole.visible=!reference;
  const selected=reference?body:full,center=selected.getCenter(new T.Vector3());
  const direction=new T.Vector3(...(reference?[1,.20,-.484]:name==='side'?[1,.12,0]:[.7,.18,1])).normalize();
  const w=canvas.clientWidth,h=canvas.clientHeight,aspect=w/h;renderer.setSize(w,h,false);
  const camera=perspective;activeCamera=camera;if(!reference)camera.fov=40;
  camera.position.copy(center).addScaledVector(direction,10);camera.lookAt(center);camera.updateMatrixWorld(true);
  const inv=camera.quaternion.clone().invert(),local=corners(selected).map(p=>p.clone().sub(center).applyQuaternion(inv));
  if(reference){const halfY=Math.max(...local.map(p=>Math.abs(p.y))),halfX=Math.max(...local.map(p=>Math.abs(p.x)));const half=Math.max(halfY,halfX/aspect)/.86;Object.assign(camera,{left:-half*aspect,right:half*aspect,top:half,bottom:-half});}
  else{camera.aspect=aspect;const tanV=Math.tan(T.MathUtils.degToRad(camera.fov/2)),tanH=tanV*aspect;let distance=0;for(const p of local)distance=Math.max(distance,p.z+Math.abs(p.x)/(tanH*.86),p.z+Math.abs(p.y)/(tanV*.86));camera.position.copy(center).addScaledVector(direction,distance);camera.lookAt(center);}
  let referenceFit=null;let actualTarget=center.clone();
  if(reference){
    const pp=gltf.parser.json.extras.parameters;
    const hh=hypothesis.fit,d=new T.Vector3(...hh.basis.towardCamera),right=new T.Vector3(...hh.basis.right),up=new T.Vector3(...hh.basis.up);
    const sourceCrop=[650,430,1470,1000],cropScale=Math.min(w/(sourceCrop[2]-sourceCrop[0]),h/(sourceCrop[3]-sourceCrop[1]));
    const padX=(w-(sourceCrop[2]-sourceCrop[0])*cropScale)/2,padY=(h-(sourceCrop[3]-sourceCrop[1])*cropScale)/2;
    const map=([x,y])=>[padX+(x-sourceCrop[0])*cropScale,padY+(y-sourceCrop[1])*cropScale];
    const desiredRear=map([1277,795]),desiredFront=map([810,820]),pixelsPerMetre=hh.focal_px/hh.distance_m*cropScale;
    const hubFaceOffset=.079+Math.max(...pp.hub_button_profile_axial_radial_m.map(p=>p[0]));
    const rear=model.getObjectByName('vehicle_wheel_rear_left').localToWorld(new T.Vector3(hubFaceOffset,0,0));
    const front=model.getObjectByName('vehicle_wheel_front_left').localToWorld(new T.Vector3(hubFaceOffset,0,0));
    camera.position.copy(d).multiplyScalar(hh.distance_m);camera.lookAt(0,0,0);actualTarget.set(0,0,0);
    camera.aspect=w/h;camera.fov=2*Math.atan(h/(2*hh.focal_px*cropScale))*180/Math.PI;camera.far=Math.max(1000,hh.distance_m+100);
    const principal=map(hh.principal_px);camera.filmOffset=0;camera.clearViewOffset();
    camera.updateProjectionMatrix();
    camera.projectionMatrix.elements[8]=1-2*principal[0]/w;
    camera.projectionMatrix.elements[9]=2*principal[1]/h-1;
    camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
    camera.updateMatrixWorld(true);
    const project=p=>{const q=p.clone().project(camera);return[(q.x+1)*w/2,(1-q.y)*h/2];};
    const actualRear=project(rear),actualFront=project(front);
    referenceFit={primaryImage:'studebaker-brougham-cdn.jpg',primarySHA256:'b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe',
      sourceCrop,sourceCropScale:cropScale,paddingPx:[padX,padY],sourceNearRear:[1277,795],sourceNearFront:[810,820],desiredRear,desiredFront,actualRear,actualFront,
      rearResidualPx:Math.hypot(...actualRear.map((x,i)=>x-desiredRear[i])),frontResidualPx:Math.hypot(...actualFront.map((x,i)=>x-desiredFront[i])),
      basis:{right:right.toArray(),up:up.toArray(),towardCamera:d.toArray()},hubFaceOffsetM:hubFaceOffset,sourceUncertainty:{frontCenter:3,rearCenter:4,frontRadius:5,rearRadius:5,kind:"manual informal pixel estimates; far hubs at least +/-15px, not certified bounds"},sourceRadiusRearPx:137,sourceRadiusFrontPx:106,
      azimuthDeg:hh.azimuth_front_deg,elevationDeg:hh.elevation_deg,pixelsPerMetre,
      perspectiveFocalSourcePx:hh.focal_px,distanceM:hh.distance_m,principalSourcePx:hh.principal_px,allFourPredictions:hypothesis.predictions,
      scope:'Positive-Z front-oblique weighted perspective hypothesis fitted to four manual hub-face controls plus visible rim radii. Loose far controls, illustration inconsistency, model radius residuals disclosed; not calibrated or photo accepted.'};
  }
  if(!reference)camera.updateProjectionMatrix();camera.updateMatrixWorld(true);renderer.render(scene,camera);
  const projected=corners(selected).map(p=>p.clone().project(camera)),lo=[0,1,2].map(k=>Math.min(...projected.map(p=>p.getComponent(k)))),hi=[0,1,2].map(k=>Math.max(...projected.map(p=>p.getComponent(k))));
  return{previewShadow:{normalBiasM:sun.shadow.normalBias,bias:sun.shadow.bias,camera:[sun.shadow.camera.left,sun.shadow.camera.right,sun.shadow.camera.top,sun.shadow.camera.bottom,sun.shadow.camera.near,sun.shadow.camera.far],scope:'Isolated fixture diagnostic only; not app appearance acceptance'},referenceFit,name,scope:reference?'Referencebodyandwheels;longparkedteamPoleexplicitlyhidden':'Wholecarriageincludingparkedcentralpole',camera:{position:camera.position.toArray(),target:actualTarget.toArray(),kind:camera.type},framing:{ndcMin:lo,ndcMax:hi,entireSelectedBoundsInside:lo.every(v=>v>=-1)&&hi.every(v=>v<=1)},bounds:{min:selected.min.toArray(),max:selected.max.toArray()},drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,sourceTriangles:gltf.parser.json.extras.statistics.triangles,sourceBytes:buffer.byteLength,glError:renderer.getContext().getError()};
}
window.setView=fit;window.setPreviewNormalBias=v=>{sun.shadow.normalBias=v;return fit(current);};
window.projectBroughamPoint=p=>{const q=new T.Vector3(...p).project(activeCamera);return{ndc:q.toArray(),canvas:[(q.x+1)*canvas.clientWidth/2,(1-q.y)*canvas.clientHeight/2]};};
window.disposeBrougham=()=>{
 if(disposed)return;disposed=true;
 const gs=new Set(),ms=new Set();scene.traverse(n=>{if(n.geometry)gs.add(n.geometry);for(const m of Array.isArray(n.material)?n.material:[n.material])if(m)ms.add(m);});
 // This isolated page owns one renderer. Retain its actual internal PBR LUT before properties.clear.
 const dfgs=new Set();for(const m of ms){const t=renderer.properties.get(m).uniforms?.dfgLUT?.value;if(t)dfgs.add(t);}
 const gl=renderer.getContext();const trace=window.broughamCleanupReceipt={source:'PinnedThree0.185.1 internal getDFGLUT/physicaluniform;single-renderer fixture owns GPU allocation',beforeTextures:renderer.info.memory.textures,dfg:[],stages:[]};
 if(dfgs.size!==1)throw Error('Expected exactly one actual renderer DFG LUT');
 const t=[...dfgs][0],handle=renderer.properties.get(t).__webglTexture;
 if(t.name!=='DFG_LUT'||!t.isDataTexture||t.image.width!==16||t.image.height!==16||t.format!==T.RGFormat||t.type!==T.HalfFloatType||!handle||!gl.isTexture(handle))throw Error('Unexpected DFG resource identity');
 let dfgDisposals=0;t.addEventListener('dispose',()=>dfgDisposals++);
 trace.dfg.push({name:t.name,uuid:t.uuid,width:t.image.width,height:t.image.height,format:t.format,type:t.type,liveBefore:gl.isTexture(handle)});
 gs.forEach(g=>g.dispose());ms.forEach(m=>m.dispose());
 trace.stages.push({stage:'after-model-geometry-materials',textures:renderer.info.memory.textures,dfgLive:gl.isTexture(handle)});
 // LightShadow.dispose owns both map/depth attachments and optional mapPass; do not substitute a budget/guard waiver.
 sun.shadow.dispose();
 trace.stages.push({stage:'after-owned-shadow',textures:renderer.info.memory.textures,dfgLive:gl.isTexture(handle)});
 if(renderer.info.memory.textures!==1||!gl.isTexture(handle))throw Error('Remaining texture attribution is not exactly the actual DFG LUT');
 t.dispose();
 trace.stages.push({stage:'after-explicit-DFG-dispose',textures:renderer.info.memory.textures,dfgLive:gl.isTexture(handle),dfgDisposals});
 if(renderer.info.memory.textures!==0||gl.isTexture(handle)||dfgDisposals!==1)throw Error('Actual DFG deallocation guard');
 renderer.dispose();scene.clear();
 trace.stages.push({stage:'after-renderer-dispose',textures:renderer.info.memory.textures,geometries:renderer.info.memory.geometries,sceneChildren:scene.children.length});
};
window.addEventListener('resize',()=>{if(!disposed)fit(current);});window.addEventListener('pagehide',e=>{if(!e.persisted)window.disposeBrougham();});


// Frozen catalogue camera and original light rig; only crop window and depth interval differ.
const sourceResponse=await fetch('./plate0095.jpg');if(!sourceResponse.ok)throw Error('Source image HTTP');
const sourceBytes=await sourceResponse.arrayBuffer();
const digest=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b))).map(x=>x.toString(16).padStart(2,'0')).join('');
window.sourceInputHash=()=>digest(sourceBytes);
window.setSourceComparison=name=>{
 if(disposed||!['detail','fullquarter'].includes(name))throw Error('Invalid finite source view');
 const crop=name==='detail'?[900,450,1300,875]:[100,400,1500,1000],nearClip=100;
 pole.visible=true;
 const hiddenModelNodes=[];model.traverse(n=>{if(!n.visible)hiddenModelNodes.push(n.name)});if(hiddenModelNodes.length)throw Error('All model parts must remain visible');
 const w=canvas.clientWidth,h=canvas.clientHeight,cw=crop[2]-crop[0],ch=crop[3]-crop[1],s=Math.min(w/cw,h/ch),padding=[(w-cw*s)/2,(h-ch*s)/2];
 const panel=document.querySelector('#reference'),im=panel.querySelector('img'),clip=panel.querySelector('#crop');
 if(panel.clientWidth!==w||panel.clientHeight!==h)throw Error('Source/render panel dimensions differ');
 Object.assign(clip.style,{width:(cw*s)+'px',height:(ch*s)+'px',left:padding[0]+'px',top:padding[1]+'px'});
 Object.assign(im.style,{width:(1556*s)+'px',height:(1145*s)+'px',left:(-crop[0]*s)+'px',top:(-crop[1]*s)+'px'});
 const hh=hypothesis.fit,map=([x,y])=>[padding[0]+(x-crop[0])*s,padding[1]+(y-crop[1])*s];
 const camera=perspective;activeCamera=camera;renderer.setSize(w,h,false);camera.position.fromArray(hh.basis.towardCamera).multiplyScalar(hh.distance_m);camera.lookAt(0,0,0);
 camera.aspect=w/h;camera.near=.05;camera.far=1000;camera.filmOffset=0;camera.clearViewOffset();camera.fov=2*Math.atan(h/(2*hh.focal_px*s))*180/Math.PI;camera.updateProjectionMatrix();
 const pp=map(hh.principal_px);camera.projectionMatrix.elements[8]=1-2*pp[0]/w;camera.projectionMatrix.elements[9]=2*pp[1]/h-1;
 const originalProjection=camera.projectionMatrix.toArray();camera.near=nearClip;camera.updateProjectionMatrix();
 for(let i=0;i<16;i++)if(i!==10&&i!==14)camera.projectionMatrix.elements[i]=originalProjection[i];
 if(camera.projectionMatrix.toArray().some((v,i)=>i!==10&&i!==14&&v!==originalProjection[i]))throw Error('Source xy projection drift');
 camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();camera.updateMatrixWorld(true);renderer.render(scene,camera);
 const checks=[[0,0,0],[.67,.55,1.15],[.67,.72,-1.15],[0,2,0]].map(p=>{const v=new T.Vector3(...p),depth=hh.distance_m-v.dot(new T.Vector3(...hh.basis.towardCamera)),native=[hh.principal_px[0]+hh.focal_px*v.dot(new T.Vector3(...hh.basis.right))/depth,hh.principal_px[1]-hh.focal_px*v.dot(new T.Vector3(...hh.basis.up))/depth],expected=map(native),q=v.clone().project(camera),actual=[(q.x+1)*w/2,(1-q.y)*h/2];return{point:p,native,expected,actual,errorPx:Math.hypot(actual[0]-expected[0],actual[1]-expected[1])}});
 if(checks.some(x=>x.errorPx>1e-6))throw Error('Source projection formula mismatch');
 const points=[...corners(full),...[-50,50].flatMap(x=>[-50,50].map(z=>new T.Vector3(x,-.004,z)))],clipDistances=points.map(p=>-p.clone().applyMatrix4(camera.matrixWorldInverse).z),clipGuard={fullModelAndOriginalFloorInside:clipDistances.every(z=>z>camera.near&&z<camera.far),minDistance:Math.min(...clipDistances),maxDistance:Math.max(...clipDistances)};if(!clipGuard.fullModelAndOriginalFloorInside)throw Error('Depth interval clips original scene geometry');
 const projected=corners(full).map(p=>p.clone().project(camera)),ndcMin=[0,1,2].map(k=>Math.min(...projected.map(p=>p.getComponent(k)))),ndcMax=[0,1,2].map(k=>Math.max(...projected.map(p=>p.getComponent(k)))),fullFraming={ndcMin,ndcMax,entireFullBoundsInside:ndcMin.every(x=>x>=-1)&&ndcMax.every(x=>x<=1)};
 const actualGL=renderer.getContext(),defaultFramebuffer=renderer.getRenderTarget()===null&&actualGL.getParameter(actualGL.FRAMEBUFFER_BINDING)===null;if(!defaultFramebuffer)throw Error('Actual default framebuffer required for depth readback');
 const rect=n=>document.querySelector(n).getBoundingClientRect().toJSON();
 return{name,nearClip,depthBits:actualGL.getParameter(actualGL.DEPTH_BITS),defaultFramebuffer,clipGuard,crop,scale:s,paddingPx:padding,panel:[w,h],camera:{position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),fov:camera.fov,aspect:camera.aspect,near:camera.near,far:camera.far,projection:camera.projectionMatrix.toArray(),world:camera.matrixWorld.toArray()},originalNear005Projection:originalProjection,nondepthProjectionExact:true,fixedFit:hh,projectionChecks:checks,fullBounds:{min:full.min.toArray(),max:full.max.toArray()},fullFraming,poleVisible:pole.visible,hiddenModelNodes,sourceTriangles:gltf.parser.json.extras.statistics.triangles,sourceBytes:buffer.byteLength,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,glError:actualGL.getError(),lighting:{outputColorSpace:renderer.outputColorSpace,toneMapping:renderer.toneMapping,exposure:renderer.toneMappingExposure,shadowsEnabled:renderer.shadowMap.enabled,shadowType:renderer.shadowMap.type,background:scene.background.getHex(),hemisphere:scene.children.filter(x=>x.isHemisphereLight).map(x=>({color:x.color.getHex(),groundColor:x.groundColor.getHex(),intensity:x.intensity})),sun:{color:sun.color.getHex(),position:sun.position.toArray(),intensity:sun.intensity,bias:sun.shadow.bias,normalBias:sun.shadow.normalBias,mapSize:sun.shadow.mapSize.toArray(),camera:[sun.shadow.camera.left,sun.shadow.camera.right,sun.shadow.camera.top,sun.shadow.camera.bottom,sun.shadow.camera.near,sun.shadow.camera.far]}},dom:{canvas:rect('canvas'),reference:rect('#reference'),header:rect('header'),viewport:[innerWidth,innerHeight]},scope:name==='fullquarter'?'Full-carriage catalogue-direction view including inferred static pole; fixed crop, not physical source pole-pose attestation or clearance':'Source detail window; all geometry enabled but naturally cropped; hidden/opposite-side parts remain unqualified'};
};

window.comparisonInputHash=async()=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',buffer))).map(x=>x.toString(16).padStart(2,'0')).join('');
window.disposeComparison=()=>{
 const gs=new Set(),ms=new Set();scene.traverse(n=>{if(n.geometry)gs.add(n.geometry);for(const m of Array.isArray(n.material)?n.material:[n.material])if(m)ms.add(m);});
 let g=0,m=0;gs.forEach(x=>x.addEventListener('dispose',()=>g++));ms.forEach(x=>x.addEventListener('dispose',()=>m++));
 window.disposeBrougham();const once={geometryEvents:g,materialEvents:m};window.disposeBrougham();
 const row={expectedGeometries:gs.size,expectedMaterials:ms.size,geometryEvents:g,materialEvents:m,idempotent:once.geometryEvents===g&&once.materialEvents===m,sceneChildren:scene.children.length,remainingGeometries:renderer.info.memory.geometries,remainingTextures:renderer.info.memory.textures,disposed,resourceCleanup:window.broughamCleanupReceipt};
 if(g!==gs.size||m!==ms.size||!row.idempotent||row.sceneChildren!==0||row.remainingGeometries!==0||row.remainingTextures!==0||!disposed)throw Error('Actual disposal guard failed '+JSON.stringify(row));return row;
};

window.broughamReady=true;
