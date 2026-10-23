// CC0-1.0 original inspection caller; model/textures retain CC BY4.0.
import * as T from 'three';
import {GLTFLoader} from '/vendor/three-0.185.1/addons/loaders/GLTFLoader.js';
const scene=new T.Scene();scene.background=new T.Color('#d5d5d5');
const renderer=new T.WebGLRenderer({antialias:true});renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.shadowMap.enabled=true;document.body.append(renderer.domElement);
const camera=new T.PerspectiveCamera(38,innerWidth/innerHeight,0.003644068837311543,36.44068837311543);
scene.add(new T.HemisphereLight(0xffffff,0x888888,2));
const sun=new T.DirectionalLight(0xffffff,2.5);sun.position.set(2.1859439436690042,4.407637660805674,2.9165003391204904);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);sun.shadow.camera.left=-2.915255069849234;sun.shadow.camera.right=2.915255069849234;sun.shadow.camera.top=3.2796619535803884;sun.shadow.camera.bottom=-3.2796619535803884;sun.shadow.normalBias=0.0014576275349246172;sun.target.position.set(-0.0004973587179214991,0.034755056031822704,0.0012452692712562885);scene.add(sun.target);sun.shadow.camera.near=0.18220344186557713;sun.shadow.camera.far=182.20344186557713;scene.add(sun);
const variant=new URLSearchParams(location.search).get('variant');if(!['baseline','candidate'].includes(variant))throw Error('Exact variant required');
const source=await new GLTFLoader().loadAsync('/fixture/'+variant+'.glb');const horse=source.scene;scene.add(horse);
// No mixer, pose()/bind changes, model transform, source light, texture edit; matching runtime organicmetal0,
// visibility override or mesh substitution. Retain the actual native hierarchy.
horse.updateMatrixWorld(true);horse.traverse(o=>{if(o.isSkinnedMesh)o.skeleton.update();if(o.isMesh){o.castShadow=true;o.receiveShadow=true;o.material=o.material.clone();o.material.metalness=0;}});
const nativeBox=new T.Box3();const v=new T.Vector3();let samples=0;const meshes=[];
horse.traverse(o=>{if(!o.isMesh)return;const ids=o.geometry.index?new Set(o.geometry.index.array):Array.from({length:o.geometry.attributes.position.count},(_,i)=>i);for(const i of ids){o.getVertexPosition(i,v).applyMatrix4(o.matrixWorld);nativeBox.expandByPoint(v);samples++;}meshes.push({name:o.name,isSkinnedMesh:!!o.isSkinnedMesh,vertices:o.geometry.attributes.position.count,indexed_vertices:ids.size,bones:o.skeleton?.bones.length??0,material:o.material.name,visible:o.visible});});
const recipe=await fetch('/fixture/cameras.json').then(r=>r.json());
for(let k=0;k<3;k++)if(Math.abs(nativeBox.min.getComponent(k)-recipe.native_bounds[0][k])>1e-4||Math.abs(nativeBox.max.getComponent(k)-recipe.native_bounds[1][k])>1e-4)throw Error('Actual Three native skinned bounds disagree with independent readback; do not fit or repose');
const floor=new T.Mesh(new T.PlaneGeometry(36.44068837311543,36.44068837311543),new T.MeshStandardMaterial({color:0xaaaaaa,roughness:1}));floor.rotation.x=-Math.PI/2;floor.position.y=recipe.native_bounds[0][1]-3.644068837311543e-05;floor.receiveShadow=true;scene.add(floor);
function setView(view){const row=recipe.views.find(x=>x.name===view);if(!row)throw Error('Unknown fixed source view');camera.position.fromArray(row.position);camera.lookAt(new T.Vector3().fromArray(recipe.look_at));camera.updateMatrixWorld(true);}
setView('side');
window.fixture={ready:true,scene,horse,renderer,camera,setView,nativeBox,meshes,indexedSamples:samples,sourceAnimationNames:source.animations.map(x=>x.name),recipe,sourceMaterialJson:source.parser.json.materials};
function tick(){requestAnimationFrame(tick);renderer.render(scene,camera);document.querySelector('#status').textContent=`Native rest · ${meshes.length} source mesh groups · no playback`;}
requestAnimationFrame(tick);
