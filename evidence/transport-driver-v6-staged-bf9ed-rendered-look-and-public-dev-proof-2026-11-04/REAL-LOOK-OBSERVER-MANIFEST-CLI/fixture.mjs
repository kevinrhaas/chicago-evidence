import * as T from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createHumanAssets} from '/renderers/web/js/humans.js';
import {createDrivenAssemblyLoader} from '/renderers/web/js/driven-assembly-loader.js';
import {createDraftHitchFactory} from '/renderers/web/js/draft-hitch.js';
import {createTownTransport} from '/renderers/web/js/town-transport.js';
import {teamSupportAt,certifiedHorseSupportDomain} from '/renderers/web/js/transport-support.js';

const need=(v,m)=>{if(!v)throw Error(m);};
const same=(a,b,m)=>need(JSON.stringify(a)===JSON.stringify(b),m);
const json=async url=>{const r=await fetch(url);need(r.ok,`HTTP ${r.status} ${url}`);return r.json();};
const hash=async bytes=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
const q=new URLSearchParams(location.search),sceneId=q.get('scene'),lod=Number(q.get('lod'));
const report=window.lookFixture={ready:false,passed:false,scope:'Controlled technical fixture using real portable assets/driver loader/town controller; no town/walk-up/trusted-UI/gait/photographic acceptance',scene:sceneId,lod,readings:[],controls:[]};
let town,assets,renderer,driver;const scene=new T.Scene();scene.background=new T.Color('#d8dcd5');
const update=()=>{scene.updateMatrixWorld(true);for(const m of driver.body.meshes)m.skeleton.update();};
const sample=()=>{
 update();const bones=driver.body.meshes[0].skeleton.bones;
 const branch=b=>{for(let p=b;p;p=p.parent)if(['head','neck_01'].includes(p.name))return true;return false;};
 const protectedBones=bones.filter(b=>!branch(b));
 const out={time:town.snapshot()[0].assembly_state.driver.time_s,controller:town.snapshot()[0],root:town.roots[0].matrixWorld.toArray(),head:bones.find(b=>b.name==='head')?.matrixWorld.toArray(),neck:bones.find(b=>b.name==='neck_01')?.matrixWorld.toArray(),protectedWorld:protectedBones.map(b=>[b.name,b.matrixWorld.toArray()]),protectedLocal:bones.filter(b=>!['head','neck_01'].includes(b.name)).map(b=>[b.name,b.position.toArray(),b.quaternion.toArray(),b.scale.toArray()]),palms:{},palettes:[]};
 need(out.head&&out.neck,'actual head and neck bones');
 for(const m of driver.body.meshes){const words=new Uint32Array(m.skeleton.boneMatrices.buffer);out.palettes.push([m.name,m.skeleton.bones.flatMap((b,i)=>branch(b)?[]:[b.name,...words.slice(i*16,i*16+16)])]);}
 const bindings=window.actualRow.driver_palm_bindings_by_lod?.[String(lod)];
 for(const [side,b]of Object.entries(bindings??{})){const m=driver.body.meshes.find(m=>m.name===b.actual_body_mesh);need(m,'actual palm mesh');const p=new T.Vector3();for(let i=0;i<3;i++)p.addScaledVector(m.getVertexPosition(b.actual_triangle_indices[i],new T.Vector3()).applyMatrix4(m.matrixWorld),b.barycentric[i]);out.palms[side]=p.toArray();}
 // Otis has no source barycentric palm binding: its actual hand/finger matrices
 // and all protected Float32 palettes are still tested; no invented grip point.
 return out;
};
const protect=(a,b)=>{same(a.root,b.root,'stopped vehicle root changed');same(a.controller.distance_m,b.controller.distance_m,'stopped distance changed');same(a.controller.wheel_rotation_rad,b.controller.wheel_rotation_rad,'stopped wheels changed');same(a.protectedWorld,b.protectedWorld,'protected torso/leg/hand world bones changed');same(a.protectedLocal,b.protectedLocal,'protected local transforms including jaw/eyes changed');same(a.palettes,b.palettes,'protected Float32 skin palettes changed');same(a.palms,b.palms,'actual configured palm surfaces changed');need(b.controller.state==='stopped','real controller not stopped');};
const reading=s=>({time:s.time,state:s.controller.state,distance:s.controller.distance_m,wheels:s.controller.wheel_rotation_rad,root:s.root,head:s.head,neck:s.neck,protected_bones:s.protectedWorld.length,palm_surface_sides:Object.keys(s.palms),palettes:s.palettes.map(([n,p])=>[n,p.length])});
let near,camera;
const tick=(visualDt,flags={})=>{town.update(.25,near,{visualDt,...flags});update();return sample();};
const render=()=>{update();renderer.render(scene,camera);need(renderer.getContext().getError()===0,'WebGL error');return{calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,gl_error:0};};
const pixels=()=>{const gl=renderer.getContext(),out=new Uint8Array(gl.drawingBufferWidth*gl.drawingBufferHeight*4);gl.readPixels(0,0,gl.drawingBufferWidth,gl.drawingBufferHeight,gl.RGBA,gl.UNSIGNED_BYTE,out);need(gl.getError()===0,'actual render pixel read failed');return out;};
window.lookCleanup=()=>{town?.dispose();const remaining=assets?.loaded??[];renderer?.dispose();return report.cleanup={remaining_human_assets:remaining,passed:remaining.length===0};};
window.addEventListener('beforeunload',()=>window.lookCleanup());
try{
 need(['1835','1904'].includes(sceneId)&&[0,3].includes(lod),'exact scene and active LOD required');
 const config=await json('/data/transport/driven/loops.json');
 const rows=config.rows.filter(r=>r.scene===sceneId);need(rows.length===1,'one exact current source driver row');
 const row=window.actualRow=rows[0];need(row.driver_clip==='sit_drive_look_v2','actual selected new look clip');
 const expected=await json('/__private/config.json');
 const assetFile=`assets/humans/web/${row.driver_asset}.lod${lod}.glb`;
 const raw=await(await fetch('/'+assetFile)).arrayBuffer();const assetHash=await hash(raw);need(assetHash===expected.asset_pins[assetFile],'selected actual child bytes differ from ROOT GO');
 const people=(await json(`/data/sidecars/${sceneId}/people.json`)).people;
 const spec=config.horse_models[row.horse_model],domain=certifiedHorseSupportDomain(spec,await json('/data/'+spec.support_domain.certificate_file));
 const loader=new GLTFLoader();
 const makeHitch=createDraftHitchFactory({loadJSON:file=>json('/data/'+file),loadGLTF:file=>loader.loadAsync('/renderers/web/'+file)});
 assets=createHumanAssets({assetBase:new URL('/assets/',location.href)});
 const makeAssembly=createDrivenAssemblyLoader({sceneId,people,profiles:config.profiles??[],humanAssets:assets,heightAt:()=>0,horseSpec:spec,horseSupportDomain:domain,makeHitch,driverLod:lod,moduleBase:new URL('/renderers/web/',location.href),adoptPerson(instance,actor){driver=actor;return()=>{};}});
 const problems=[];
 town=createTownTransport({rows:[row],sceneId,makeAssembly,heightAt:()=>0,clear:()=>true,routeSupport:(r,p)=>teamSupportAt(r,p,()=>0,domain),detail:lod===0?'full':'balanced',problems,onActorsChanged(){scene.add(...town.roots);}});
 await town.ready();need(town.actors.length===1&&driver?.body,`actual native assembly failed ${problems}`);need(driver.clipName==='sit_drive_look_v2','actual actor clip');
 const controller=town.actors[0];near={x:controller.at[0],z:-controller.at[1]};
 town.update(.2,near,{visualDt:.7});need(sample().time===0,'first native visual frame must discard elapsed');
 town.update(.2,near,{visualDt:.75});need(sample().time===.75,'visual interval consumed once, not vehicle substeps');
 need(controller.stop('interaction'),'native Stop failed');
 const start=sample();
 renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(innerWidth,innerHeight);renderer.outputColorSpace=T.SRGBColorSpace;document.body.append(renderer.domElement);
 scene.add(new T.HemisphereLight(0xf0f5ff,0x77684b,2.2));const light=new T.DirectionalLight(0xffefdf,3);light.position.set(3,5,4);scene.add(light);
 const head=new T.Vector3().setFromMatrixPosition(driver.body.meshes[0].skeleton.bones.find(b=>b.name==='head').matrixWorld);
 camera=new T.PerspectiveCamera(32,innerWidth/innerHeight,.03,100);camera.position.copy(head).add(new T.Vector3(1.1,.3,2.2));camera.lookAt(head.clone().add(new T.Vector3(0,-.28,0)));camera.updateMatrixWorld(true);
 document.querySelector('#label').textContent=`${sceneId}: ${driver.person?.name??driver.personId}; ${lod===0?'Full LOD0':'Balanced LOD3'}; real Stop; native look clip. Technical fixture only.`;
 report.asset={file:assetFile,sha256:assetHash,person_id:driver.personId,clip:driver.clipName};report.initial_render=render();const initialPixels=pixels();report.readings.push(reading(start));report.ready=true;
 window.advanceLook=()=>{const end=tick(2);protect(start,end);const delta=Math.max(...start.head.map((x,i)=>Math.abs(x-end.head[i])));need(delta>.001,'actual native head motion absent');need(end.time===start.time+2,'stopped visual interval consumed once');report.max_head_world_delta=delta;report.readings.push(reading(end));report.changed_render=render();const now=pixels();let changed=0;for(let i=0;i<now.length;i+=4)if(now[i]!==initialPixels[i]||now[i+1]!==initialPixels[i+1]||now[i+2]!==initialPixels[i+2])changed++;need(changed>0,'head pose change is not visibly rendered');report.changed_render_pixels=changed;return{passed:true,head_world_delta:delta,changed_render_pixels:changed,time:end.time};};
 window.finishLook=()=>{
  let before=sample();
  for(const flags of[{paused:true},{reducedMotion:true},{hidden:true}]){
   const held=tick(8,flags);protect(before,held);same(before.time,held.time,'held driver advanced');
   const resumed=tick(8);protect(before,resumed);same(before.time,resumed.time,'first resumed frame consumed held time');
   const next=tick(.25);protect(before,next);need(next.time===before.time+.25,'resumed visual clock interval differs');
   report.controls.push({flags,held_time:held.time,resume_first_time:resumed.time,resumed_time:next.time,passed:true});before=next;
  }
  need(problems.length===0,'native assembly problem');report.passed=true;return report;
 };
}catch(error){report.error=String(error.stack??error);window.lookCleanup();throw error;}
