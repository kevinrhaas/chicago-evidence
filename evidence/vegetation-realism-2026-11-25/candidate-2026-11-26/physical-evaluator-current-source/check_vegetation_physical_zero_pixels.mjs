import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
const require=createRequire(import.meta.url),{chromium}=require('playwright');
const w='/workspace/work',web=w+'/better-trees-integration/chicago/4d/renderers/web';
const original=fs.readFileSync(w+'/vegetation-published-m2-18606-current-1871-before/walk/js/leaf-light.js','utf8');
const variant=fs.readFileSync(w+'/vegetation-physical-zero.variant.js','utf8');
const server=http.createServer((req,res)=>{
  if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end('<link rel="icon" href="data:,"><script type="importmap">{"imports":{"three":"/vendor/three-0.185.1/three.module.js"}}</script>');return;}
  res.setHeader('Content-Type','text/javascript');
  if(req.url==='/js/control-leaf.js')return res.end(original);
  if(req.url==='/js/physical-zero-leaf.js')return res.end(variant);
  const file=path.join(web,req.url.split('?')[0]);if(!fs.existsSync(file)){res.writeHead(404);return res.end();}fs.createReadStream(file).pipe(res);
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE,args:['--no-sandbox','--enable-unsafe-swiftshader']});
try {
  const output={};
  for(const mode of ['control','physical-zero']) {
    const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
    await page.goto(`http://127.0.0.1:${server.address().port}/`);
    const result=await page.evaluate(async mode=>{
      const THREE=await import('three');const {patchLeafLight}=await import(mode==='control'?'/js/control-leaf.js':'/js/physical-zero-leaf.js');const {LEAF_SKY}=await import('/js/time-of-day.js');
      const renderer=new THREE.WebGLRenderer();renderer.setSize(64,64);renderer.shadowMap.enabled=true;const gl=renderer.getContext();
      const target=new THREE.WebGLRenderTarget(64,64);renderer.setRenderTarget(target);const camera=new THREE.PerspectiveCamera(35,1,.1,20);camera.position.z=3;
      const scene=new THREE.Scene(),light=new THREE.DirectionalLight(0xffffff,2),point=new THREE.PointLight(0xffcc88,0,1);light.castShadow=true;Object.assign(light.shadow.camera,{left:-2,right:2,top:2,bottom:-2,near:.1,far:10});light.shadow.bias=-.0001;point.position.set(0,0,10);scene.add(light,point);
      const plane=new THREE.Mesh(new THREE.PlaneGeometry(2,2));plane.receiveShadow=true;scene.add(plane);const blocker=new THREE.Mesh(new THREE.PlaneGeometry(2,2),new THREE.MeshBasicMaterial({side:THREE.DoubleSide}));blocker.position.z=-1;blocker.castShadow=true;scene.add(blocker);
      const ccMap=new THREE.DataTexture(new Uint8Array([255,128,40,255]),1,1);ccMap.needsUpdate=true;const rows=[];
      for(const leaf of [true,false])for(const lowSpec of leaf?[false,true]:[false])for(const kind of ['standard','clearcoat'])for(const mask of leaf?['1.0','0.0']:['plain']) {
        const C=kind==='standard'?THREE.MeshStandardMaterial:THREE.MeshPhysicalMaterial;const opts={color:0x80cc40,side:THREE.DoubleSide,roughness:.6,metalness:.1};if(kind==='clearcoat')Object.assign(opts,{clearcoat:1,clearcoatNormalMap:ccMap,clearcoatNormalScale:new THREE.Vector2(3,3)});const material=new C(opts);if(leaf)patchLeafLight(material,{lowSpec,mask});plane.material=material;
        for(const pose of ['front','back','grazing','shadow','zero-light','sky-only','point-out-of-range','point-visible']) {
          light.position.set(pose==='grazing'?4:0,0,pose==='grazing'?0:pose==='back'||pose==='shadow'?-4:4);light.intensity=['zero-light','sky-only','point-out-of-range','point-visible'].includes(pose)?0:2;LEAF_SKY.value=pose==='sky-only'?.22:0;blocker.visible=pose==='shadow';point.intensity=pose.startsWith('point-')?5:0;point.distance=pose==='point-visible'?20:1;
          renderer.render(scene,camera);const pixels=new Uint8Array(64*64*4);renderer.readRenderTargetPixels(target,0,0,64,64,pixels);const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',pixels))).map(b=>b.toString(16).padStart(2,'0')).join('');const physical=renderer.info.programs.map(p=>gl.getShaderSource(p.fragmentShader)||'').filter(s=>s.includes('void RE_Direct_Physical('));
          rows.push({leaf,lowSpec,kind,mask,pose,hash,physicalPrograms:physical.length,guardedPrograms:physical.filter(s=>s.includes('C4D_ZERO_DIRECT_3747')).length});
        }
        material.dispose();
      }
      const runnable=renderer.info.programs.every(p=>p.diagnostics?.runnable!==false);renderer.dispose();target.dispose();ccMap.dispose();return{rows,runnable};
    },mode);
    assert(!errors.length,errors.join('\n'));assert(result.runnable&&result.rows.length===80);assert(result.rows.every(r=>r.physicalPrograms>0));if(mode==='control')assert(result.rows.every(r=>r.guardedPrograms===0));else assert(result.rows.every(r=>r.guardedPrograms===r.physicalPrograms));output[mode]={...result,errors};await page.close();
  }
  const mismatches=output.control.rows.filter((r,i)=>r.hash!==output['physical-zero'].rows[i].hash);assert(!mismatches.length,JSON.stringify(mismatches));
  const receipt={complete:true,all80CasesPixelIdentical:true,separatePageRealms:true,plainPhysicalMaterialsCovered:true,clearcoatIndependentNormalRetained:true,originalShaderSHA256:createHash('sha256').update(original).digest('hex'),candidateShaderSHA256:createHash('sha256').update(variant).digest('hex'),output};fs.writeFileSync(w+'/vegetation-physical-zero-pixel-equality.json',JSON.stringify(receipt,null,2)+'\n');console.log('PHYSICAL ZERO PIXEL PASS — all80actual WebGL cases identical in independent realms; plain and foliage standard/clearcoat, both leaf variants/masks, exactgrazing, front/back/shadow/night/sky/pointattenuation; guarded programs verified.');
} finally {await browser.close();server.close();}
