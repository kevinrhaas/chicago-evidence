import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require('playwright');
const w='/workspace/work',web=w+'/better-trees-integration/chicago/4d/renderers/web';
const original=fs.readFileSync(web+'/js/leaf-light.js','utf8');
const variant=fs.readFileSync(w+'/vegetation-zero-light-diagnostic/leaf-light.variant.js','utf8');
const server=http.createServer((req,res)=>{
  if(req.url==='/') {res.setHeader('Content-Type','text/html');res.end('<link rel="icon" href="data:,"><script type="importmap">{"imports":{"three":"/vendor/three-0.185.1/three.module.js"}}</script>');return;}
  res.setHeader('Content-Type','text/javascript');
  if(req.url==='/js/original-leaf.js')return res.end(original);
  if(req.url==='/js/zero-leaf.js')return res.end(variant);
  const file=path.join(web,req.url.split('?')[0]);
  if(!fs.existsSync(file)){res.writeHead(404);return res.end();}fs.createReadStream(file).pipe(res);
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE,args:['--no-sandbox','--enable-unsafe-swiftshader']});
try {
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
  const result=await page.evaluate(async()=>{
    const THREE=await import('three');
    const a=(await import('/js/original-leaf.js')).patchLeafLight,b=(await import('/js/zero-leaf.js')).patchLeafLight;
    const {LEAF_SKY}=await import('/js/time-of-day.js');
    const renderer=new THREE.WebGLRenderer();renderer.setSize(64,64);renderer.shadowMap.enabled=true;
    const target=new THREE.WebGLRenderTarget(64,64);renderer.setRenderTarget(target);
    const camera=new THREE.PerspectiveCamera(35,1,.1,20);camera.position.z=3;
    const scene=new THREE.Scene(),light=new THREE.DirectionalLight(0xffffff,2),point=new THREE.PointLight(0xffcc88,0,1);
    light.castShadow=true;Object.assign(light.shadow.camera,{left:-2,right:2,top:2,bottom:-2,near:.1,far:10});light.shadow.bias=-.0001;
    point.position.set(0,0,10);scene.add(light,point);
    const plane=new THREE.Mesh(new THREE.PlaneGeometry(2,2));plane.receiveShadow=true;scene.add(plane);
    const blocker=new THREE.Mesh(new THREE.PlaneGeometry(2,2),new THREE.MeshBasicMaterial({side:THREE.DoubleSide}));blocker.position.z=-1;blocker.castShadow=true;scene.add(blocker);
    const ccMap=new THREE.DataTexture(new Uint8Array([255,128,40,255]),1,1);ccMap.needsUpdate=true;
    const rows=[];
    for(const lowSpec of [false,true])for(const kind of ['standard','clearcoat'])for(const mask of ['1.0','0.0']) {
      const C=kind==='standard'?THREE.MeshStandardMaterial:THREE.MeshPhysicalMaterial;
      const options={color:0x80cc40,side:THREE.DoubleSide,roughness:.6,metalness:.1};
      if(kind==='clearcoat')Object.assign(options,{clearcoat:1,clearcoatNormalMap:ccMap,clearcoatNormalScale:new THREE.Vector2(3,3)});
      const ma=new C(options),mb=new C(options);a(ma,{lowSpec,mask});b(mb,{lowSpec,mask});
      for(const pose of ['front','back','grazing','shadow','zero-light','sky-only','point-out-of-range','point-visible']) {
        light.position.set(pose==='grazing'?4:0,0,pose==='back'||pose==='shadow'?-4:4);
        light.intensity=['zero-light','sky-only','point-out-of-range','point-visible'].includes(pose)?0:2;
        LEAF_SKY.value=pose==='sky-only'?.22:0;blocker.visible=pose==='shadow';
        point.intensity=pose.startsWith('point-')?5:0;point.distance=pose==='point-visible'?20:1;
        const read=material=>{plane.material=material;renderer.render(scene,camera);const pixels=new Uint8Array(64*64*4);renderer.readRenderTargetPixels(target,0,0,64,64,pixels);return pixels;};
        const before=read(ma),after=read(mb);let maxDelta=0,changedChannels=0;
        for(let i=0;i<before.length;i++){const d=Math.abs(before[i]-after[i]);if(d)changedChannels++;maxDelta=Math.max(maxDelta,d);}
        rows.push({lowSpec,kind,mask,pose,maxDelta,changedChannels,channels:before.length});
      }
      ma.dispose();mb.dispose();
    }
    const runnable=renderer.info.programs.every(p=>p.diagnostics?.runnable!==false);
    renderer.dispose();target.dispose();ccMap.dispose();return{rows,runnable};
  });
  assert(!errors.length,errors.join('\n'));assert(result.runnable);
  assert(result.rows.length===64);assert(result.rows.every(r=>r.maxDelta===0),JSON.stringify(result.rows.filter(r=>r.maxDelta)));
  const {createHash}=await import('node:crypto');
  const receipt={complete:true,exactPixelEquality:true,cases:result.rows.length,originalShaderSHA256:createHash('sha256').update(original).digest('hex'),variantShaderSHA256:createHash('sha256').update(variant).digest('hex'),errors,rows:result.rows};
  fs.writeFileSync(w+'/vegetation-zero-light-pixel-equality.json',JSON.stringify(receipt,null,2)+'\n');
  console.log('ZERO LIGHT PIXEL PASS — all64 actual WebGL cases pixel-identical: standard/clearcoat, both lighting variants, leaf/wood masks, front/back/grazing/shadow, zero light/sky and point attenuation.');
} finally {await browser.close();server.close();}
