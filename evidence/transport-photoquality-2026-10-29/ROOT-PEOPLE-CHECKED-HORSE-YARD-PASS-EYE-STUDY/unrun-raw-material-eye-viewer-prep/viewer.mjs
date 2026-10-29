import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const need=(v,m)=>{if(!v)throw Error(m);};
const hash=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),x=>x.toString(16).padStart(2,'0')).join('');
const utf=s=>new TextEncoder().encode(s);
const config=await(await fetch('/config.json')).json();
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:false});
renderer.setPixelRatio(1);renderer.setSize(1024,1024);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1;
document.body.append(renderer.domElement);
const camera=new THREE.PerspectiveCamera(35,1,.001,100);
const loaded={};
for(const [label,pin]of Object.entries(config.assets)){
  const response=await fetch(pin.url);need(response.ok,`Study asset HTTP ${label}`);
  const bytes=await response.arrayBuffer();need(bytes.byteLength===pin.bytes&&await hash(bytes)===pin.sha256,`Study asset SHA ${label}`);
  const asset=await new GLTFLoader().parseAsync(bytes,location.origin+'/study-assets/');
  // Preserve ALL source roots, source bind/rest pose and raw imported materials.
  // No mixer, skeleton.pose(), geometry edit, material clone or native variant.
  const scene=new THREE.Scene();scene.background=new THREE.Color(.18,.18,.18);scene.add(asset.scene);
  asset.scene.updateMatrixWorld(true);
  const meshes=[];asset.scene.traverse(o=>{if(o.isSkinnedMesh){o.skeleton.update();meshes.push(o);}});
  need(meshes.length===3,'Whole source three-skinned-mesh inventory');
  const eyes=meshes.find(o=>asset.parser.associations.get(o)?.meshes===2);
  const body=meshes.find(o=>asset.parser.associations.get(o)?.meshes===1);
  need(eyes&&body,'Actual GLTFLoader mesh associations for BODY/EYES');
  const sourceCenter=new THREE.Vector3().fromArray(config.recipe.eyes.negative_x.center_m);
  const skinIndex=eyes.geometry.getAttribute('skinIndex'),skinWeight=eyes.geometry.getAttribute('skinWeight');
  for(let i=0;i<skinIndex.count;i++)need(skinIndex.getX(i)===3&&skinIndex.getY(i)===0&&skinIndex.getZ(i)===0&&skinIndex.getW(i)===0&&skinWeight.getX(i)===1&&skinWeight.getY(i)===0&&skinWeight.getZ(i)===0&&skinWeight.getW(i)===0,'Actual eye source has one shared rigid head-bone influence');
  const eyePoint=v=>eyes.applyBoneTransform(0,v).applyMatrix4(eyes.matrixWorld);
  const center=eyePoint(sourceCenter.clone());
  const sourceDirection=v=>eyePoint(sourceCenter.clone().add(v)).sub(center).normalize();
  const up=sourceDirection(new THREE.Vector3(0,1,0));
  const radius=eyePoint(sourceCenter.clone().add(new THREE.Vector3(config.recipe.eyes.negative_x.radius_mean_m,0,0))).distanceTo(center);
  const headBounds=new THREE.Box3(),wholeBounds=new THREE.Box3(),point=new THREE.Vector3();
  const bodyEyeCenter=new THREE.Vector3().fromArray(config.recipe.eyes.negative_x.center_m);
  const localRadius=config.recipe.eyes.negative_x.radius_mean_m;
  for(const mesh of meshes){
    const positions=mesh.geometry.getAttribute('position');
    for(const index of new Set(mesh.geometry.index.array)){
      const local=new THREE.Vector3().fromBufferAttribute(positions,index);
      mesh.getVertexPosition(index,point);point.applyMatrix4(mesh.matrixWorld);wholeBounds.expandByPoint(point);
      if(mesh===body&&local.y>bodyEyeCenter.y-16*localRadius&&local.z>bodyEyeCenter.z-12*localRadius)headBounds.expandByPoint(point);
    }
  }
  need(!headBounds.isEmpty()&&radius>0,'Measured source head bounds and eye radius');
  const headCenter=headBounds.getCenter(new THREE.Vector3()),headSize=headBounds.getSize(new THREE.Vector3());
  // Fixed neutral lighting, identical measured-center offsets for both sources.
  const hemi=new THREE.HemisphereLight(0xffffff,0x404040,1.2);scene.add(hemi);
  for(const [direction,intensity]of [[[-1,2,2],3],[[1,1,-1],1]]){
    const light=new THREE.DirectionalLight(0xffffff,intensity);
    light.position.copy(center).add(new THREE.Vector3(...direction));light.target.position.copy(center);
    scene.add(light,light.target);
  }
  const geometry={},materials=[],bones=[];
  for(const mesh of meshes){
    const index=asset.parser.associations.get(mesh)?.meshes;
    const attrs={};
    for(const[name,a]of Object.entries(mesh.geometry.attributes))attrs[name]={count:a.count,itemSize:a.itemSize,sha256:await hash(a.array.buffer.slice(a.array.byteOffset,a.array.byteOffset+a.array.byteLength))};
    geometry[index]={name:mesh.name,skinned:mesh.isSkinnedMesh,matrixWorld:mesh.matrixWorld.toArray(),attributes:attrs,indexSHA256:await hash(mesh.geometry.index.array.buffer.slice(mesh.geometry.index.array.byteOffset,mesh.geometry.index.array.byteOffset+mesh.geometry.index.array.byteLength))};
    const material=mesh.material;
    materials.push({mesh:index,name:material.name,type:material.type,color:material.color.toArray(),metalness:material.metalness,roughness:material.roughness,side:material.side,transparent:material.transparent,alphaTest:material.alphaTest,maps:Object.fromEntries(['map','metalnessMap','roughnessMap','normalMap','alphaMap'].map(k=>[k,material[k]?{name:material[k].name,imageWidth:material[k].image?.width,imageHeight:material[k].image?.height,colorSpace:material[k].colorSpace}:null]))});
  }
  // Store one shared skeleton's actual unchanged world matrices, not duplicate UUIDs.
  for(const bone of meshes[0].skeleton.bones)bones.push({name:bone.name,matrixWorld:bone.matrixWorld.toArray()});
  loaded[label]={scene,asset,center,up,radius,headCenter,headSize,eyes,sourceDirection,summary:{sourceSHA256:pin.sha256,wholeBounds:[wholeBounds.min.toArray(),wholeBounds.max.toArray()],headBounds:[headBounds.min.toArray(),headBounds.max.toArray()],eyeWorldCenter:center.toArray(),eyeWorldRadius:radius,geometry,materials,bones,animationClips:asset.animations.map(c=>({name:c.name,duration:c.duration,tracks:c.tracks.length})),pose:'authored GLTF bind/rest state; no animation playback'}};
}
const a=loaded.parent.summary,b=loaded.candidate.summary;
need(JSON.stringify(a.materials)===JSON.stringify(b.materials),'Raw material properties must match');
need(JSON.stringify(a.bones)===JSON.stringify(b.bones),'Actual source skeleton matrices must match');
need(JSON.stringify(a.wholeBounds)===JSON.stringify(b.wholeBounds)&&JSON.stringify(a.headBounds)===JSON.stringify(b.headBounds),'Actual skinned source bounds must match');
for(const index of ['0','1','2']){
  const x=a.geometry[index],y=b.geometry[index];need(x.indexSHA256===y.indexSHA256&&JSON.stringify(x.matrixWorld)===JSON.stringify(y.matrixWorld),'Index and source transforms unchanged');
  for(const[name,attr]of Object.entries(x.attributes))if(!(index==='2'&&name==='normal'))need(JSON.stringify(attr)===JSON.stringify(y.attributes[name]),`Protected actual loaded attribute ${index}/${name}`);
}
need(a.geometry[2].attributes.normal.sha256!==b.geometry[2].attributes.normal.sha256,'Actual loaded eye normals must differ');
window.sourceEyeStudy={ready:true,scope:'RAW_SOURCE_ONLY_UNADOPTED_UNQUALIFIED_NOT_NATIVE_ORGANIC_WORLD',summaries:{parent:a,candidate:b},async render(label,view){
  const item=loaded[label];need(item&&['head-profile','head-oblique','eye-profile','eye-oblique'].includes(view),'Explicit study source/view');
  const eye=view.startsWith('eye-'),oblique=view.endsWith('oblique');
  const target=eye?item.center:item.headCenter;
  const direction=item.sourceDirection(new THREE.Vector3(-1,oblique ? .20 : 0,oblique ? .45 : 0).normalize());
  const distance=eye?item.radius*4:Math.max(...item.headSize.toArray())*1.8;
  camera.up.copy(item.up);camera.position.copy(target).addScaledVector(direction,distance);camera.lookAt(target);camera.updateMatrixWorld(true);
  await renderer.compileAsync(item.scene,camera);renderer.render(item.scene,camera);
  // Genuine second render after a native animation frame; no counters overwritten.
  await new Promise(requestAnimationFrame);renderer.render(item.scene,camera);
  const gl=renderer.getContext(),pixel=new Uint8Array(4);gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,pixel);
  const result={label,view,scope:this.scope,sourceSHA256:item.summary.sourceSHA256,pose:item.summary.pose,camera:{position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),fov:camera.fov,near:camera.near,far:camera.far},target:target.toArray(),distance,exposure:renderer.toneMappingExposure,toneMapping:renderer.toneMapping,outputColorSpace:renderer.outputColorSpace,rendererDPR:renderer.getPixelRatio(),drawingBuffer:[gl.drawingBufferWidth,gl.drawingBufferHeight],glError:gl.getError(),contextLost:gl.isContextLost(),renderInfo:{...renderer.info.render},memoryInfo:{...renderer.info.memory}};
  need(result.glError===0&&!result.contextLost,'Actual study GL status');return result;
}};
