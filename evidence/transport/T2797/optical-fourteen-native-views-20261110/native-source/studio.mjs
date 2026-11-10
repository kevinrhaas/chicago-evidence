// SPDX-License-Identifier: GPL-3.0-or-later
import * as T from 'three';
import {GLTFLoader} from '/vendor/addons/loaders/GLTFLoader.js';

const config = await (await fetch('/protocol.json')).json();
const canvas = document.querySelector('canvas');
const renderer = new T.WebGLRenderer({canvas, antialias:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(1);
renderer.outputColorSpace = T.SRGBColorSpace;
renderer.toneMapping = T.ACESFilmicToneMapping;
renderer.toneMappingExposure = config.studio.exposure;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = T.PCFSoftShadowMap;
const scene = new T.Scene();
scene.background = new T.Color(config.studio.background);
scene.add(new T.HemisphereLight(...config.studio.hemisphere));
const sun = new T.DirectionalLight(...config.studio.sun.color_intensity);
sun.position.fromArray(config.studio.sun.position);
sun.castShadow = true;
sun.shadow.mapSize.set(...config.studio.sun.shadow_size);
Object.assign(sun.shadow.camera, config.studio.sun.shadow_camera);
sun.shadow.bias = config.studio.sun.shadow_bias;
scene.add(sun);
const floor = new T.Mesh(new T.PlaneGeometry(100,100),
  new T.MeshStandardMaterial({color:config.studio.floor.color, roughness:1}));
floor.rotation.x = -Math.PI/2;
floor.position.y = config.studio.floor.y;
floor.receiveShadow = true;
scene.add(floor);
const models = new Map();
const same = (a,b) => JSON.stringify(a)===JSON.stringify(b);
const must = (value,label) => {if(!value) throw Error(label);};
const digest = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))]
  .map(x=>x.toString(16).padStart(2,'0')).join('');

async function modelFor(key) {
  if(models.has(key)) return models.get(key);
  const input = config.inputs[key], response = await fetch(input.route);
  must(response.ok,'Optical GLB HTTP '+response.status);
  const bytes = await response.arrayBuffer();
  must(bytes.byteLength===input.bytes && await digest(bytes)===input.sha256,'Actual browser optical bytes differ');
  const gltf = await new GLTFLoader().parseAsync(bytes,location.origin+'/');
  must(same(gltf.parser.json.materials,config.optical_materials),'Expected exact thin-sheet material definitions differ');
  const model = gltf.scene;
  model.traverse(node=>{if(node.isMesh){node.castShadow=true;node.receiveShadow=true;}});
  const nativeGlass = new Set();
  model.traverse(node=>{
    for(const material of Array.isArray(node.material)?node.material:[node.material])
      if(material?.name==='thin_sheet_cabin_glass_delivery_reconstruction') nativeGlass.add(material);
  });
  must(nativeGlass.size>0,'Actual native thin-sheet glass material missing');
  const glassReadback=[];
  for(const material of nativeGlass) {
    must(material.transmission===0 && material.opacity===.14 && material.transparent===true
      && material.depthWrite===false && material.ior===1.5 && material.side===T.DoubleSide,
      'Actual native optical material profile differs');
    glassReadback.push({name:material.name,transmission:material.transmission,opacity:material.opacity,
      transparent:material.transparent,depthWrite:material.depthWrite,ior:material.ior,side:material.side});
  }
  const item={gltf,model,glassReadback};models.set(key,item);return item;
}

function rightStepPoints(gltf,model) {
  const doc=gltf.parser.json, selected=[];
  for(const part of doc.extras.parts.filter(p=>p.name==='step_support' && p.frame==='vehicle_body')) {
    const meshes=doc.meshes.map((m,i)=>({m,i})).filter(x=>x.m.name===`surface_${part.frame}_${part.material}`);
    must(meshes.length===1,'Ambiguous actual body-material mesh for detail');
    const nodeIndex=doc.nodes.findIndex(n=>n.mesh===meshes[0].i);
    const matches=[];
    model.traverse(n=>{if(n.isMesh && gltf.parser.associations.get(n)?.nodes===nodeIndex) matches.push(n);});
    must(matches.length===1,'Actual native source part node missing/ambiguous');
    const node=matches[0],position=node.geometry.getAttribute('position'),index=node.geometry.getIndex();
    const points=[];
    for(let i=part.triangle_start_in_batch*3;i<(part.triangle_start_in_batch+part.triangles)*3;i++) {
      const vertex=index?index.getX(i):i;
      must(vertex>=0 && vertex<position.count,'Actual detail source range escaped primitive');
      points.push(new T.Vector3().fromBufferAttribute(position,vertex).applyMatrix4(node.matrixWorld));
    }
    if(Math.max(...points.map(p=>p.x))<0) selected.push({part,points});
  }
  must(selected.length===2,'Detail must bind both actual right step-support occurrences');
  return selected;
}

window.captureOpticalCase = async key => {
  const row=config.cases.find(x=>x.id===key);must(row,'Unknown predeclared optical case');
  const profile=config.profiles[row.profile], c=config.cameras[row.camera];
  must(innerWidth===profile.viewport[0] && innerHeight===profile.viewport[1],'Actual viewport differs');
  renderer.setSize(...profile.viewport,false);
  const camera=new T.OrthographicCamera(c.left,c.right,c.top,c.bottom,c.near,c.far);
  camera.position.fromArray(c.eye);camera.up.fromArray(c.up);
  camera.lookAt(new T.Vector3(...c.target));camera.updateMatrixWorld(true);
  const {gltf,model,glassReadback}=await modelFor(row.input);
  for(const other of models.values()) if(other.model.parent) scene.remove(other.model);
  scene.add(model);
  const doors=[];model.traverse(n=>{if(n.name==='vehicle_door_right') doors.push(n);});
  if(row.variant==='new') {
    must(doors.length===1,'Actual articulated root absent/ambiguous');
    doors[0].rotation.y=T.MathUtils.degToRad(row.angle_deg);
  } else must(doors.length===0,'Old installed specimen unexpectedly articulated');
  model.updateMatrixWorld(true);
  const nodes=[],bounds=new T.Box3(),actualNDC=new T.Box3();let meshes=0,vertices=0,triangles=0;
  model.traverse(node=>{
    const originalIndex=gltf.parser.associations.get(node)?.nodes;
    if(originalIndex!==undefined) {
      const original=gltf.parser.json.nodes[originalIndex];
      must(same(node.position.toArray(),original.translation??[0,0,0]),'Original node translation changed');
      must(same(node.scale.toArray(),original.scale??[1,1,1]),'Original node scale changed');
      if(node!==doors[0]) must(same(node.quaternion.toArray(),original.rotation??[0,0,0,1]),'Original node rotation changed');
      nodes.push({source_node_index:originalIndex,name:original.name,position:node.position.toArray(),
        quaternion:node.quaternion.toArray(),scale:node.scale.toArray()});
    }
    if(!node.isMesh) return;
    meshes++;
    for(let ancestor=node;ancestor;ancestor=ancestor.parent) must(ancestor.visible,'An actual part is hidden');
    const position=node.geometry.getAttribute('position');
    triangles+=(node.geometry.getIndex()?.count??position.count)/3;
    for(let i=0;i<position.count;i++) {
      const point=new T.Vector3().fromBufferAttribute(position,i).applyMatrix4(node.matrixWorld);
      bounds.expandByPoint(point);actualNDC.expandByPoint(point.clone().project(camera));vertices++;
    }
  });
  must(meshes>0 && vertices>0 && triangles===config.inputs[row.input].triangles,'Actual native geometry inventory differs');
  let framingNDC=actualNDC,detailParts=[];
  if(c.bounds_scope==='two_actual_right_step_support_parts') {
    framingNDC=new T.Box3();
    for(const {part,points} of rightStepPoints(gltf,model)) {
      points.forEach(p=>framingNDC.expandByPoint(p.clone().project(camera)));
      detailParts.push({name:part.name,source_part_index:part.source_part_index??null,
        triangle_start_in_batch:part.triangle_start_in_batch,triangles:part.triangles});
    }
  } else must(c.bounds_scope==='whole_model','Undeclared framing scope');
  const min=framingNDC.min.toArray(),max=framingNDC.max.toArray();
  must(min.every(v=>v>=-1) && max.every(v=>v<=1),'Predeclared focus camera clips its actual source domain; no auto-fit');
  renderer.render(scene,camera);
  await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
  renderer.render(scene,camera);
  const glError=renderer.getContext().getError();must(glError===0,'WebGL error '+glError);
  const result={case:row.id,input:row.input,variant:row.variant,profile:row.profile,
    explicit_study_LOD:row.detail,production_tier_selection_run:false,angle_deg:row.angle_deg,
    door_angle_actual_deg:doors[0]?.rotation.y*180/Math.PI??null,viewport:profile.viewport,
    bytes:config.inputs[row.input].bytes,sha256:config.inputs[row.input].sha256,
    materials_json:gltf.parser.json.materials,native_glass:glassReadback,source_nodes:nodes,
    actual_mesh_count:meshes,actual_position_vertices:vertices,actual_source_triangles:triangles,
    world_bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()},
    actual_vertex_ndc:{min:actualNDC.min.toArray(),max:actualNDC.max.toArray()},
    framing_domain_ndc:{min,max},detail_parts:detailParts,
    camera:{...c,matrix_world:camera.matrixWorld.toArray(),projection:camera.projectionMatrix.toArray()},
    renderer:{output_color_space:renderer.outputColorSpace,tone_mapping:renderer.toneMapping,
      exposure:renderer.toneMappingExposure,shadow_enabled:renderer.shadowMap.enabled,
      shadow_type:renderer.shadowMap.type,pixel_ratio:renderer.getPixelRatio(),
      calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,gl_error:glError},
    scope:config.scope,visual_review:'PENDING',photographic_accepted:false,
    near_mid_visual_qualified:false,boarding_enabled:false};
  must(result.renderer.calls>0 && result.renderer.triangles>0,'No actual native draw');return result;
};

window.disposeOpticalStudy = () => {
  const geometries=new Set(),materials=new Set(),textures=new Set();
  for(const {model}of models.values()) model.traverse(n=>{
    if(n.geometry) geometries.add(n.geometry);
    for(const m of Array.isArray(n.material)?n.material:[n.material]) if(m) materials.add(m);
  });
  geometries.add(floor.geometry);materials.add(floor.material);
  for(const m of materials) for(const v of Object.values(m)) if(v?.isTexture) textures.add(v);
  textures.forEach(t=>{t.source?.data?.close?.();t.dispose();});
  materials.forEach(m=>m.dispose());geometries.forEach(g=>g.dispose());
  sun.shadow.map?.dispose();renderer.dispose();scene.clear();models.clear();return {disposed:true};
};
window.opticalStudyReady=true;
