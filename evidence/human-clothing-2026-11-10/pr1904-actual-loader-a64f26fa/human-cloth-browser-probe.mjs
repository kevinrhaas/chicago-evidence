// Task-local read-only integration review. No source, match record or acceptance writes.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);
const opt = (name, fallback = null) => args.includes(name) ? args[args.indexOf(name)+1] : fallback;
const APP = opt('--app', '/tmp/chicago-queue-refresh-20261109/chicago/4d');
const SITE = path.resolve(APP, '../../site/4d');
const mode = opt('--mode'), viewport = opt('--viewport'), output = opt('--out');
const baseline = args.includes('--baseline');
const baselineRef = 'dc998577d76a09a31a5519b7deb0c0c0f6e1f869';
if (!['source', 'published'].includes(mode) || !['desktop', 'phone'].includes(viewport) || !output) {
  throw Error('usage: --mode source|published --viewport desktop|phone --out FRESH_DIR [--baseline]');
}
await fs.mkdir(output, { recursive: false });
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const moduleBase = mode === 'source' ? '/app/renderers/web/' : '/site/walk/';
const assetBase = mode === 'source' ? '/app/assets/' : '/site/data/';
const dataBase = mode === 'source' ? '/app/data/' : '/site/data/';
const tiers = { desktop: ['full', 0], phone: ['light', 2] };
const [tier, lod] = tiers[viewport];
const baselineModule = baseline ? execFileSync('git', ['show', `${baselineRef}:chicago/4d/renderers/web/js/humans.js`], { cwd: APP }) : null;
const currentModule = await fs.readFile(path.join(mode === 'source' ? APP+'/renderers/web' : SITE+'/walk', 'js/humans.js'));
if (baseline && baselineModule.toString().includes('clothHuman(scene)')) throw Error('baseline already contains common cloth integration');
if (!baseline && !currentModule.toString().includes('clothHuman(scene)')) throw Error('current selected mirror lacks common cloth integration');

const html = `<!doctype html><meta charset="utf-8"><link rel="icon" href="data:,"><style>html,body{margin:0;overflow:hidden;background:#555}canvas{display:block}</style>
<script type="importmap">${JSON.stringify({ imports: { three: moduleBase+'vendor/three-0.185.1/three.module.js', 'three/addons/': moduleBase+'vendor/three-0.185.1/addons/' } })}</script>
<script type="module">
import * as THREE from 'three';
import { HumanActor, createHumanAssets } from '${moduleBase}js/humans.js';
import { resolveHumanIdentity } from '${moduleBase}js/human-identity.js';
const source = ${JSON.stringify({ assetBase, dataBase, tier, lod, baseline })};
const fetchJSON = async rel => { const r = await fetch(source.dataBase+rel); if(!r.ok) throw Error(r.status+' '+rel); return r.json(); };
const people = await fetchJSON('sidecars/1835/people.json');
const renderer = new THREE.WebGLRenderer({ antialias:true, preserveDrawingBuffer:true });
renderer.setPixelRatio(1); renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.debug.onShaderError = (gl,program,vertex,fragment) => { throw Error('Actual shader compilation failed: '+gl.getProgramInfoLog(program)+' '+gl.getShaderInfoLog(vertex)+' '+gl.getShaderInfoLog(fragment)); };
document.body.append(renderer.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color('#73767a');
scene.add(new THREE.HemisphereLight(0xf0f5ff,0x57524d,1.6));
const key = new THREE.DirectionalLight(0xfff4e8,3); key.position.set(-3,5,5); key.castShadow=true;
key.shadow.mapSize.set(1024,1024); key.shadow.camera.left=-3; key.shadow.camera.right=3;
key.shadow.camera.top=3; key.shadow.camera.bottom=-3; key.shadow.camera.near=.1; key.shadow.camera.far=20; scene.add(key);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0x555554,roughness:.9}));
floor.rotation.x=-Math.PI/2; floor.receiveShadow=true; scene.add(floor);
const camera = new THREE.PerspectiveCamera(38,innerWidth/innerHeight,.05,100);
const draw = () => { renderer.render(scene,camera); renderer.getContext().finish(); };
camera.position.set(1.8,1.2,3.6); camera.lookAt(0,.85,0); draw();
const emptyBaseline = {...renderer.info.memory};
const assets = createHumanAssets({assetBase:new URL(source.assetBase,location.href)});
let actor = null, original = null, compiled = new Map();
const bones = () => Object.fromEntries(actor.body.scene.getObjectsByProperty('isBone',true).filter(b=>['thigh_l','thigh_r','calf_l','calf_r','spine_02'].includes(b.name)).map(b=>[b.name,{q:b.quaternion.toArray(),p:b.position.toArray()}]));
const counters = () => ({draw:{...renderer.info.render},memory:{...renderer.info.memory},programs:renderer.info.programs.map(p=>({key:p.cacheKey,usedTimes:p.usedTimes,diagnostics:p.diagnostics??null}))});
const materials = () => {
 const set = new Set(); actor.body.scene.traverse(o=>{if(o.isMesh)for(const m of Array.isArray(o.material)?o.material:[o.material])set.add(m);});
 return [...set].map(m=>({name:m.name,key:m.customProgramCacheKey(),type:m.type,visible:m.visible,map:m.map?{width:m.map.image?.width,height:m.map.image?.height}:null,compiled:compiled.get(m)??null}));
};
const observeCompilation = () => {
 const seen = new Set(); actor.body.scene.traverse(o=>{if(!o.isMesh)return;for(const m of Array.isArray(o.material)?o.material:[o.material]){
  if(seen.has(m))continue;seen.add(m);const prior=m.onBeforeCompile,actualKey=m.customProgramCacheKey();
  m.customProgramCacheKey=()=>actualKey;
  m.onBeforeCompile=(shader,r)=>{prior.call(m,shader,r);compiled.set(m,{ran:true,key:actualKey,cloth:shader.fragmentShader.includes('float chiFabricH = 0.0'),uniforms:Object.keys(shader.uniforms).filter(k=>k.startsWith('chiFabric')),vertexLength:shader.vertexShader.length,fragmentLength:shader.fragmentShader.length});};
 }});
};
const aim = () => { const y = actor.proxy.scale.y; camera.position.copy(actor.root.position).add(new THREE.Vector3(1.4,y*.64,3.8)); camera.lookAt(actor.root.position.clone().add(new THREE.Vector3(0,y*.48,0))); camera.updateMatrixWorld(true); };
window.probe = {
 async load(id){
  if(actor)throw Error('dispose previous actor first');
  original = await fetchJSON('humans/instances/1835/'+id+'.json');
  const identity = resolveHumanIdentity(original,{sceneId:'1835',people:people.people});
  const instance = structuredClone(original); instance.placement={...instance.placement,local_e:0,local_n:0,heading_deg:180};
  instance.lod={policy:'fixed',fixed:source.lod};
  actor = new HumanActor({instance,identity,person:identity.person,assets,heightAt:()=>0,tier:source.tier});
  scene.add(actor.root);await actor.setLod(source.lod);if(!actor.body||!actor.varied)throw Error('real body/variation pipeline did not finish');
  observeCompilation();aim();actor.update(0,camera.position,0);await renderer.compileAsync(scene,camera);draw();
  return {original,person:{id:identity.person.id,name:identity.person.name},variation:actor.variation,lod:actor.lod,clips:actor.clips,materials:materials(),counters:counters(),bones:bones(),pose:{state:actor.state,clip:actor.clipName,e:actor.e,n:actor.n}};
 },
 async walk(){
  if(!actor.walkPath([{e:0,n:0},{e:0,n:-8}]))throw Error('walkPath refused');
  for(let i=0;i<18;i++){actor.update(1/30,camera.position,1/30);}
  aim();draw(); if(actor.clipName!=='walk'||actor.state!=='walking'||Math.hypot(actor.e,actor.n)<.1)throw Error('actual walking/travel did not start');
  return {materials:materials(),counters:counters(),bones:bones(),pose:{state:actor.state,clip:actor.clipName,e:actor.e,n:actor.n},gaitBound:actor.gait?.bound??false};
 },
 async dispose(){actor.dispose();scene.remove(actor.root);actor=null;original=null;compiled=new Map();await new Promise(r=>setTimeout(r,0));draw();return{counters:counters(),loaded:assets.loaded,emptyBaseline};},
 emptyBaseline,renderingScope:'Controlled HumanActor studio, adopted assets and actual identity/variation pipeline; no town/photo acceptance',
};
</script>`;

const types = {'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.wasm':'application/wasm','.bin':'application/octet-stream','.glb':'model/gltf-binary','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.ktx2':'image/ktx2'};
const server = http.createServer(async(req,res)=>{
 try{
  const pathname=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(pathname==='/probe.html'){res.writeHead(200,{'content-type':'text/html'}).end(html);return;}
  const root=pathname.startsWith('/app/')?APP:pathname.startsWith('/site/')?SITE:null;
  if(!root){res.writeHead(404).end();return;}
  const file=path.resolve(root,pathname.slice(pathname.startsWith('/app/')?5:6));
  if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  const body=baseline&&pathname===moduleBase+'js/humans.js'?baselineModule:await fs.readFile(file);
  res.writeHead(200,{'content-type':types[path.extname(file)]??'application/octet-stream'}).end(body);
 }catch(error){res.writeHead(404).end(String(error));}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const globalRoot=(process.env.NODE_PATH??execFileSync('npm',['root','-g'],{encoding:'utf8'}).trim()).split(path.delimiter)[0];
const require=createRequire(path.join(APP,'tools/qa.mjs'));
let chromium;try{({chromium}=require('playwright'));}catch{({chromium}=await import(path.join(globalRoot,'playwright/index.js')));}
const records=[],errors=[],requests=[];
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:viewport==='desktop'?{width:1280,height:800}:{width:390,height:780},deviceScaleFactor:1});
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 page.on('response',r=>{requests.push({url:r.url(),status:r.status()});if(r.status()>=400)errors.push('HTTP '+r.status()+' '+r.url());});
 page.on('requestfailed',r=>errors.push('requestfailed '+r.url()+' '+r.failure()?.errorText));
 await page.goto('http://127.0.0.1:'+server.address().port+'/probe.html');
 await page.waitForFunction(()=>window.probe,null,{timeout:90000});
 for(const id of ['hi_rc_bardwell_otis_1835','hi_peck_philip_1835']){
  const standing=await page.evaluate(id=>window.probe.load(id),id);
  const clothes=standing.materials.filter(m=>m.name.startsWith('garment_'));
  if(!clothes.length||clothes.some(m=>!m.compiled?.ran||m.compiled.cloth===baseline))throw Error('actual garment shader did not compile in expected baseline/current mode');
  const file=id+'-standing.png';await page.screenshot({path:path.join(output,file),timeout:90000});
  const walking=await page.evaluate(()=>window.probe.walk());
  if(JSON.stringify(standing.bones)===JSON.stringify(walking.bones))throw Error('walking bones did not change');
  const walkFile=id+'-walking.png';await page.screenshot({path:path.join(output,walkFile),timeout:90000});
  const disposal=await page.evaluate(()=>window.probe.dispose());
  if(disposal.loaded.length)throw Error('actor assets not released');
  records.push({id,standing,walking,disposal,images:[file,walkFile]});
 }
 if(errors.length)throw Error(errors.join('\n'));
}catch(error){
 errors.push('Probe failed: '+error.message);throw error;
}finally{
 if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));
 const files=await fs.readdir(output);const images=[];for(const file of files.filter(f=>f.endsWith('.png'))){const raw=await fs.readFile(path.join(output,file));images.push({file,bytes:raw.length,sha256:sha(raw)});}
 const receipt={mode,viewport,tier,lod,baseline,baselineRef:baseline?baselineRef:null,scope:'Actual HumanActor loader integration in controlled studio; no town, photographic, garment fit or canonical PBR acceptance',actualModuleSha256:sha(baselineModule??currentModule),currentModuleSha256:sha(currentModule),records,errors,requests,images};
 await fs.writeFile(path.join(output,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');
}
console.log(JSON.stringify({mode,viewport,baseline,residents:records.length,errors:errors.length,out:output}));
