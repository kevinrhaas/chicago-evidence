// Original inspection code; third-party source model/textures retain CC BY4.0.
import * as T from 'three';
import { createStandingHorses } from '/runtime/standing-horses.js';
import { createConfidenceView } from '/runtime/confidence.js';
const variant = new URLSearchParams(location.search).get('variant');
if (!['source_native', 'organic_dielectric_v1'].includes(variant)) throw Error('Explicit material option required');
const renderer = new T.WebGLRenderer({antialias:true});renderer.setSize(1280,800);renderer.setPixelRatio(1);
renderer.outputColorSpace=T.SRGBColorSpace;renderer.shadowMap.enabled=true;document.body.append(renderer.domElement);
const scene=new T.Scene();scene.background=new T.Color('#d5d5d5');
const center=new T.Vector3(-127.5,0,296),camera=new T.PerspectiveCamera(38,1.6,.01,100);
scene.add(new T.HemisphereLight(0xffffff,0x888888,2));
const sun=new T.DirectionalLight(0xffffff,2.5);sun.position.copy(center).add(new T.Vector3(6,12,8));
sun.target.position.copy(center);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);
Object.assign(sun.shadow.camera,{left:-8,right:8,top:9,bottom:-9});sun.shadow.normalBias=.004;
scene.add(sun,sun.target);
const floor=new T.Mesh(new T.PlaneGeometry(20,20),new T.MeshStandardMaterial({color:0xaaaaaa,roughness:1}));
floor.rotation.x=-Math.PI/2;floor.position.copy(center);floor.receiveShadow=true;scene.add(floor);
const views={side:[4.7,1.4,.2],'three-quarter':[3.8,1.8,4.5]};
function setView(name){if(!views[name])throw Error('Unknown fixed camera');camera.position.copy(center).add(new T.Vector3(...views[name]));camera.lookAt(center.clone().add(new T.Vector3(0,.89,.2)));camera.updateMatrixWorld(true);}
setView('side');
const problems=[],confidence=createConfidenceView();
const layer=await createStandingHorses({dataBase:new URL(`/case/${variant}/data/`,location.href),sceneId:'1835',confidence,detail:'full',problems,
  // Declared FLAT inspection fixture, not a claim of actual yard integration.
  groundHeight:()=>0});
scene.add(layer.group);layer.update(camera);await layer.ready;
if(problems.length||layer.instances.length!==1)throw Error('Actual normalized source consumer failed: '+problems.join('; '));
document.querySelector('#variant').textContent=variant+' · flat inspection plane · original rig, no playback';
window.fixture={ready:true,renderer,scene,camera,layer,confidence,problems,variant,setView,views,center,
  sourcePose:'Exact unanimated source hierarchy; uniform1.55m proxy normalization and declared whole-root support only',
  sourceClips:layer.instances[0].asset.animations.map(c=>c.name)};
function tick(){requestAnimationFrame(tick);layer.update(camera);renderer.render(scene,camera);}requestAnimationFrame(tick);
