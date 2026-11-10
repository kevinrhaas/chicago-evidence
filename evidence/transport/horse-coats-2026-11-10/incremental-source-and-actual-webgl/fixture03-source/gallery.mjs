// Actual source models, maps and production appearance hook. Bounded studio only.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { clone as cloneSkinned } from 'three/addons/utils/SkeletonUtils.js';
import { applyHorseAppearance, prepareHorseTemplate, horseIdentity } from '/app/renderers/web/js/horse-appearance.js';
import { createConfidenceView } from '/app/renderers/web/js/confidence.js';
const need=(ok,message)=>{if(!ok)throw Error(message);};
const json=async p=>{const r=await fetch('/app/data/'+p);need(r.ok,p+' HTTP'+r.status);return r.json();};
const hash=async bytes=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');
try {
 const recipe=await json('transport/horse-coats.json'),loops=await json('transport/driven/loops.json'),standing=await json('transport/parked/standing-horses.json'),parked=await json('transport/parked/placements.json');
 const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(1024,1024);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1;renderer.info.autoReset=false;document.body.prepend(renderer.domElement);
 const shaderErrors=[];renderer.debug.onShaderError=(gl,p,v,f)=>{shaderErrors.push({program:gl.getProgramInfoLog(p),vertex:gl.getShaderInfoLog(v),fragment:gl.getShaderInfoLog(f)});};
 const confidence=createConfidenceView(),loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder),assets=[],panels=[],sourceMaterials=new Set(),baselineMaterials=new Set();
 const floorGeometry=new THREE.PlaneGeometry(6,6),floorMaterial=new THREE.MeshStandardMaterial({color:0x9e9b96,roughness:.9});
 // Warm the actual r185 renderer-owned DFG lookup with one PBR floor pixel.
 const warmScene=new THREE.Scene(),warmFloor=new THREE.Mesh(floorGeometry,floorMaterial),warmCamera=new THREE.PerspectiveCamera(35,1,.05,30);warmFloor.rotation.x=-Math.PI/2;warmScene.add(warmFloor,new THREE.HemisphereLight(0xffffff,0x555555,2));warmCamera.position.set(0,2,2);warmCamera.lookAt(0,0,0);renderer.setViewport(0,0,1,1);renderer.render(warmScene,warmCamera);renderer.getContext().finish();
 const dfgLUT=renderer.properties.get(floorMaterial).uniforms?.dfgLUT?.value,dfgHandle=dfgLUT&&renderer.properties.get(dfgLUT).__webglTexture;
 need(dfgLUT?.name==='DFG_LUT'&&dfgHandle&&renderer.info.memory.textures===1,'identify actual PBR internal texture before source loading');
 const rendererOwnedBaseline={name:dfgLUT.name,uuid:dfgLUT.uuid,width:dfgLUT.image.width,height:dfgLUT.image.height,textures:renderer.info.memory.textures};warmScene.clear();
 const bodyOf=root=>{const all=[];root.traverse(n=>{if(n.isSkinnedMesh&&n.material.name===recipe.body_material)all.push(n);});need(all.length===1,'exact BODY required');return all[0];};
 const attributeHash=async a=>hash(a.array.buffer.slice(a.array.byteOffset,a.array.byteOffset+a.array.byteLength));
 const makePanel=(root,asset,title,identity=null,appearance=null,ownedMaterials=[])=>{
  const scene=new THREE.Scene();scene.background=new THREE.Color(0xd5d7db);scene.add(new THREE.HemisphereLight(0xf0f5ff,0x59504a,1.8));const key=new THREE.DirectionalLight(0xfff3e5,3);key.position.set(-3,5,4);scene.add(key);scene.add(root);
  const floor=new THREE.Mesh(floorGeometry,floorMaterial);floor.rotation.x=-Math.PI/2;floor.position.y=-.012;scene.add(floor);
  const camera=new THREE.PerspectiveCamera(35,256/224,.05,30);camera.position.set(3.4,1.65,4.2);camera.lookAt(0,.9,.25);
  const clip=asset.animations.find(a=>a.name==='sevket_reconstructed_quiet_head_neck_idle_v1');need(clip&&clip.duration===12,'actual quiet clip');const mixer=new THREE.AnimationMixer(root);mixer.clipAction(clip).play();
  const label=document.createElement('div'),index=panels.length;label.className='label';label.style.left=(index%4*256)+'px';label.style.top=(Math.floor(index/4)*256+224)+'px';label.textContent=title;document.querySelector('#labels').append(label);
  panels.push({root,scene,camera,asset,title,identity,appearance,mixer,ownedMaterials,phase: identity?.key.endsWith(':right') ? .375 : 0,body:bodyOf(root)});
 };
 for(const source of recipe.source_contract){
  const response=await fetch('/app/'+source.file);need(response.ok,'real source download');const bytes=await response.arrayBuffer();need(await hash(bytes)===source.sha256,'actual immutable source hash');const asset=await loader.parseAsync(bytes,new URL('/app/'+source.file,location.href).href);assets.push(asset);asset.scene.traverse(n=>{if(n.isMesh)sourceMaterials.add(n.material);});
  const native=cloneSkinned(asset.scene);native.traverse(n=>{if(n.isMesh){n.material=n.material.clone();baselineMaterials.add(n.material);confidence.patch(n.material);}});makePanel(native,asset,source.file.includes('/driven/')?'DRIVEN original source-native':'STANDING original source-native');
  prepareHorseTemplate(asset,'organic_dielectric_v1');asset.scene.traverse(n=>{if(n.isMesh)sourceMaterials.add(n.material);});
  const organic=cloneSkinned(asset.scene);organic.traverse(n=>{if(n.isMesh){n.material=n.material.clone();baselineMaterials.add(n.material);confidence.patch(n.material);}});makePanel(organic,asset,source.file.includes('/driven/')?'DRIVEN current organic baseline':'STANDING current organic baseline');
 }
 const entries=loops.rows.flatMap(row=>['left','right'].map(individual=>({scene:row.scene,row:row.id,individual,source:0})));
 for(const[scene,rows]of Object.entries(standing.scenes))for(const row of rows)entries.push({scene,row:row.id,individual:'single',source:1});
 for(const[scene,rows]of Object.entries(parked.scenes))for(const row of rows)if(row.stationary_team)for(const individual of['left','right'])entries.push({scene,row:row.id,individual,source:0});
 need(entries.length===11,'all eleven actual configured identities');
 for(const entry of entries){const asset=assets[entry.source],root=cloneSkinned(asset.scene),ownedMaterials=[];root.traverse(n=>{if(!n.isMesh)return;n.frustumCulled=false;if(entry.source===1){n.material=n.material.clone();ownedMaterials.push(n.material);}if(!n.geometry.hasAttribute('_confidence'))n.geometry.setAttribute('_confidence',new THREE.Float32BufferAttribute(new Float32Array(n.geometry.attributes.position.count).fill(1),1));confidence.patch(n.material);});
  const appearance=applyHorseAppearance(root,{recipe,sourceSha:recipe.source_contract[entry.source].sha256,scene:entry.scene,row:entry.row,individual:entry.individual,confidence,ownedMaterials:entry.source===1?new Set(ownedMaterials):null});
  need(JSON.stringify(appearance.identity)===JSON.stringify({...horseIdentity(recipe,entry),source_sha256:recipe.source_contract[entry.source].sha256}),'stable identity through actual hook');
  makePanel(root,asset,`${entry.scene} ${appearance.identity.palette} ${entry.individual}\n${entry.row}`,appearance.identity,appearance,ownedMaterials);
 }
 const originalPositionHashes=await Promise.all(assets.map(a=>attributeHash(bodyOf(a.scene).geometry.attributes.position)));
 for(const row of loops.rows){const pair=panels.filter(p=>p.identity?.key.startsWith(row.scene+':'+row.id+':'));need(pair.length===2&&pair[0].identity.palette===pair[1].identity.palette,'matched palette');need(JSON.stringify([pair[0].identity.blaze,pair[0].identity.socks_m])!==JSON.stringify([pair[1].identity.blaze,pair[1].identity.socks_m]),'actual pair individual marks');}
 const counters=()=>({render:{...renderer.info.render},memory:{...renderer.info.memory},programs:renderer.info.programs.length,gl:window.__memoryMeter?.()??null});
 const sample=async time=>{
  renderer.info.reset();renderer.setScissorTest(false);renderer.setClearColor(0xd5d7db);renderer.clear();renderer.setScissorTest(true);
  for(const[pIndex,p]of panels.entries()){p.mixer.setTime(time+p.phase*12);p.root.updateMatrixWorld(true);p.root.traverse(n=>{if(n.isSkinnedMesh)n.skeleton.update();});const x=pIndex%4*256,y=1024-(Math.floor(pIndex/4)+1)*256+32;renderer.setViewport(x,y,256,224);renderer.setScissor(x,y,256,224);renderer.render(p.scene,p.camera);}
  renderer.getContext().finish();need(shaderErrors.length===0,'actual shader compilation error');
  const materials=[];for(const p of panels)p.root.traverse(n=>{if(!n.isMesh)return;const m=n.material,programs=renderer.properties.get(m).programs;need(programs?.size>0,'actual material program absent');for(const program of programs.values()){const gl=renderer.getContext();need(gl.getProgramParameter(program.program,gl.LINK_STATUS),'actual link failure');const vs=gl.getShaderSource(program.vertexShader)||'';if(m.userData.chicagoHorseCoat)need(vs.indexOf('vChiHorseP=position;')>=0&&vs.indexOf('vChiHorseP=position;')<vs.indexOf('skinVertex = bindMatrix'),'coat bind position must precede skinning');}materials.push({panel:p.title,name:m.name,coat:m.userData.chicagoHorseCoat??null,materialKey:m.customProgramCacheKey(),map:{present:!!m.map,width:m.map?.image?.width,height:m.map?.image?.height},normalMap:!!m.normalMap,roughnessMap:!!m.roughnessMap,metalness:m.metalness,programCount:programs.size});});
  const positionHashes=await Promise.all(assets.map(a=>attributeHash(bodyOf(a.scene).geometry.attributes.position)));need(JSON.stringify(positionHashes)===JSON.stringify(originalPositionHashes),'source bind positions changed');
  return{time_s:time,counters:counters(),materials,panels:panels.map(p=>({title:p.title,identity:p.identity,phase_fraction:p.phase,bodyVertices:p.body.geometry.attributes.position.count,bones:Object.fromEntries(['horse_head','horse_neck'].map(name=>[name,p.root.getObjectByName(name).quaternion.toArray()]))})),sourcePositionHashes:positionHashes,shaderErrors:[...shaderErrors]};
 };
 window.coatProbe={recipe,entries,rendererOwnedBaseline,async sample(time){return sample(time);},
 async closeup(kind,time){
  const row=kind==='glessner'?'1904:prairie_parked_studebaker_brougham:':'1904:prairie_driven_brougham_loop_1904:';
  const pair=panels.filter(p=>p.identity?.key.startsWith(row));need(pair.length===2,'actual requested pair');renderer.setSize(1024,512);document.body.style.height='512px';document.querySelector('#labels').replaceChildren();renderer.info.reset();renderer.setScissorTest(false);renderer.clear();renderer.setScissorTest(true);
  for(const[index,p]of pair.entries()){
   p.mixer.setTime(time+p.phase*12);p.root.updateMatrixWorld(true);p.root.traverse(n=>{if(n.isSkinnedMesh)n.skeleton.update();});const camera=new THREE.PerspectiveCamera(30,512/480,.05,30);
   if(kind==='glessner'){camera.position.set(2.3,1.3,3.6);camera.lookAt(0,.9,.35);}else{camera.position.set(.9,1.65,2.5);camera.lookAt(0,1.48,1.05);}
   renderer.setViewport(index*512,32,512,480);renderer.setScissor(index*512,32,512,480);renderer.render(p.scene,camera);
   const label=document.createElement('div');label.className='label';label.style.left=index*512+'px';label.style.top='480px';label.style.width='506px';label.textContent=p.title+' | quiet '+time+'s';document.querySelector('#labels').append(label);
  }
  renderer.getContext().finish();need(shaderErrors.length===0,'closeup actual shader failure');return{kind,time_s:time,identities:pair.map(p=>p.identity),counters:counters(),scope:kind==='glessner'?'Two actual Glessner individual horses, separately framed; no carriage/hitch factory':'Actual moving grey pair face masks; no full horse or surface qualification'};
 },async dispose(){
  for(const p of panels){p.appearance?.dispose();p.mixer.stopAllAction();p.mixer.uncacheRoot(p.root);const skeletons=new Set();p.root.traverse(n=>{if(n.isSkinnedMesh)skeletons.add(n.skeleton);});for(const s of skeletons)s.dispose();for(const m of p.ownedMaterials)m.dispose();p.scene.clear();}
  const geometry=new Set(),textures=new Set();for(const asset of assets)asset.scene.traverse(n=>{if(n.isMesh)geometry.add(n.geometry);});for(const material of sourceMaterials)for(const value of Object.values(material))if(value?.isTexture)textures.add(value);
  for(const m of baselineMaterials)m.dispose();for(const m of sourceMaterials)m.dispose();for(const g of geometry)g.dispose();for(const t of textures)t.dispose();floorGeometry.dispose();floorMaterial.dispose();renderer.setScissorTest(false);renderer.setViewport(0,0,1024,1024);renderer.render(new THREE.Scene(),new THREE.PerspectiveCamera());renderer.getContext().finish();const after=counters();after.rendererOwnedBaseline=rendererOwnedBaseline;after.sameDFGHandle=renderer.properties.get(dfgLUT).__webglTexture===dfgHandle;window.coatCleanupAfter=after;need(after.memory.geometries===0&&after.memory.textures===rendererOwnedBaseline.textures&&after.sameDFGHandle,'owned geometry/texture remained beyond proven DFG baseline');renderer.dispose();return after;
 }};
}catch(error){window.coatFixtureError=error.stack||String(error);document.body.append(String(error));}
