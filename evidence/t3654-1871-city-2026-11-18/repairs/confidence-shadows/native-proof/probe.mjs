import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
const require=createRequire('/workspace/chicago/probe.cjs'),{chromium}=require('playwright');
const ROOT='/tmp/t3654-shadow-candidate',OUT='/tmp/t3654-shadow-proof';
const manifest=JSON.parse(fs.readFileSync('/tmp/t3654-shadow-inputs.json','utf8'));
const sha=b=>createHash('sha256').update(b).digest('hex');
const verify=()=>Object.entries(manifest.sha256).every(([rel,hash])=>sha(fs.readFileSync(path.join(ROOT,rel)))===hash);
assert(verify(),'all candidate input hashes match');
fs.copyFileSync('/tmp/t3654-shadow-inputs.json',path.join(OUT,'inputs.json'));
const report={started:new Date().toISOString(),manifest,viewport:{width:1280,height:800},detail:'full',frames:[],errors:[],consoleErrors:[],networkErrors:[],failures:[],method:'Actual immutable published 1871 app with only the approved context depth-material patch. Native desktop Full PCF shadow-depth texture sampled at 512x512 texel centers by a small GPU comparison pass, outside the app frame. Same frozen pose/mode is compared with its depth owners temporarily removed (old native fallback), then restored. GPU shaders and live uniforms read immediately after actual caster calls. SwiftShader is software rendering; no hardware FPS/GPU memory claim.'};
const check=(condition,message)=>{console.log(`${condition?'PASS':'FAIL'} ${message}`);if(!condition)report.failures.push(message);};
const types={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.glb':'model/gltf-binary','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{try{let p=path.resolve(ROOT,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!p.startsWith(ROOT+'/'))throw Error('outside');if(fs.statSync(p).isDirectory())p=path.join(p,'index.html');res.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(res);}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:report.viewport,deviceScaleFactor:1,reducedMotion:'reduce'});
 const page=await context.newPage();page.setDefaultTimeout(90000);
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.consoleErrors.push(m.text());});
 page.on('response',r=>{if(r.status()>=400)report.networkErrors.push({url:r.url(),status:r.status()});});
 page.on('requestfailed',r=>report.networkErrors.push({url:r.url(),failure:r.failure()}));
 const boot=Date.now();console.log('Loading actual published 1871 Full viewer');
 await page.goto(`http://127.0.0.1:${server.address().port}/1871/?detail=full&seed=3654`,{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240000});
 await page.waitForFunction(()=>['welcome','world'].includes(window.__chicago4d?.welcome?.state),null,{timeout:90000});
 await page.evaluate(async()=>{const a=window.__chicago4d;if(a.error)throw Error(a.error);if(a.welcome.state==='welcome')a.welcome.enter('spawn');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.renderer.setAnimationLoop(null);a.setAnimationHold(true);await a.setDetail('full');});
 report.bootMs=Date.now()-boot;console.log(`Boot complete ${report.bootMs} ms`);
 report.setup=await page.evaluate(async()=>{
  const THREE=await import('/walk/vendor/three-0.185.1/three.module.js'),a=window.__chicago4d,r=a.renderer,gl=r.getContext();
  let sun;a.scene3d.traverse(o=>{if(o.isDirectionalLight&&o.castShadow)sun=o;});if(!sun)throw Error('No actual sun shadow caster');
  const probe={a,r,gl,THREE,sun,casters:[],programs:{},calls:[],shadowUniforms:[],sources:{},originalUpdate:a.contextCity.update};
  a.contextCity.group.traverse(o=>{if(!o.isMesh)return;const kind=o.userData.contextTier==='near'?(o.userData.treeCount?'tree':'building'):o.userData.layers?.includes('bridges')?'bridge':null;if(!kind)return;
   probe.casters.push({o,kind,depth:o.customDepthMaterial});const original=o.onAfterShadow;
   o.onAfterShadow=function(renderer,obj,camera,shadowCamera,geometry,depth,group){original.call(this,renderer,obj,camera,shadowCamera,geometry,depth,group);const p=renderer.properties.get(depth).currentProgram;if(!p)throw Error('Actual shadow material has no GPU program');
    probe.calls.push({kind,name:o.name,owned:depth===o.customDepthMaterial&&!!o.customDepthMaterial,program:p.id,depth:depth.uuid,instanced:!!o.isInstancedMesh});
    if(!probe.programs[p.id]){const vs=gl.getShaderSource(p.vertexShader),fs=gl.getShaderSource(p.fragmentShader);probe.sources[p.id]={vertex:vs,fragment:fs};probe.programs[p.id]={id:p.id,vertexCompiled:gl.getShaderParameter(p.vertexShader,gl.COMPILE_STATUS),fragmentCompiled:gl.getShaderParameter(p.fragmentShader,gl.COMPILE_STATUS),linked:gl.getProgramParameter(p.program,gl.LINK_STATUS),info:gl.getProgramInfoLog(p.program),confidence:vs.includes('_confidence')&&fs.includes('uHideLevel'),instanced:vs.includes('#define USE_INSTANCING'),depthPacking:fs.match(/#define DEPTH_PACKING \d+/)?.[0]};}
    const uniform=name=>{const loc=gl.getUniformLocation(p.program,name);if(loc===null)return null;const v=gl.getUniform(p.program,loc);return ArrayBuffer.isView(v)?Array.from(v):v;};
    if(!probe.shadowUniforms.some(v=>v.kind===kind&&v.program===p.id))probe.shadowUniforms.push({kind,program:p.id,mode:uniform('uConfMode'),hide:uniform('uHideLevel'),gradeMode:uniform('uGradeMode'),gradeOpacity:uniform('uGradeOpacity')});
   };
  });
  const quadScene=new THREE.Scene(),quadCamera=new THREE.Camera(),target=new THREE.WebGLRenderTarget(512,512,{depthBuffer:false,stencilBuffer:false});
  const material=new THREE.ShaderMaterial({glslVersion:THREE.GLSL3,depthTest:false,depthWrite:false,toneMapped:false,uniforms:{shadowDepth:{value:null},crop:{value:new THREE.Vector4()},mapSize:{value:new THREE.Vector2()}},vertexShader:'in vec3 position; void main(){gl_Position=vec4(position,1.0);}',fragmentShader:'precision highp float; precision highp sampler2DShadow; uniform sampler2DShadow shadowDepth; uniform vec4 crop; uniform vec2 mapSize; out vec4 result; void main(){vec2 uv=(crop.xy+gl_FragCoord.xy)/mapSize; float open=texture(shadowDepth,vec3(uv,0.99999)); result=vec4(vec3(open),1.0);}'});
  // RawShaderMaterial avoids duplicate standard declarations in this independent readback pass.
  const raw=new THREE.RawShaderMaterial({glslVersion:THREE.GLSL3,depthTest:false,depthWrite:false,toneMapped:false,uniforms:material.uniforms,vertexShader:'precision highp float; in vec3 position; void main(){gl_Position=vec4(position,1.0);}',fragmentShader:material.fragmentShader});material.dispose();
  quadScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),raw));Object.assign(probe,{quadScene,quadCamera,target,raw});
  probe.frame=(pose,mode,fallback)=>{
   a.setFly(true);const eye=pose.eye,t=pose.target;
   a.walker.teleport({local_e:eye[0],local_n:eye[1],altitude_m:eye[2],yaw_deg:Math.atan2(t[0]-eye[0],t[1]-eye[1])*180/Math.PI,pitch_deg:Math.atan2(t[2]-eye[2],Math.hypot(t[0]-eye[0],t[1]-eye[1]))*180/Math.PI});
   a.confidence.setHidden('reconstructed',mode==='hidden');a.confidence.set(mode==='dither');a.confidence.setGrade('reconstructed',{mode:'dither',opacity:.34});
   for(const {o,depth} of probe.casters)o.customDepthMaterial=fallback?undefined:depth;
   probe.calls=[];probe.shadowUniforms=[];r.shadowMap.autoUpdate=true;r.shadowMap.needsUpdate=true;sun.shadow.needsUpdate=true;a.step();
   const stats=a.stats(),png=r.domElement.toDataURL('image/png');
   const projected=new THREE.Vector3(t[0],3.2+t[2],-t[1]).applyMatrix4(sun.shadow.matrix),map=sun.shadow.map;
   const x=Math.max(0,Math.min(map.width-512,Math.round(projected.x*map.width-256))),y=Math.max(0,Math.min(map.height-512,Math.round(projected.y*map.height-256)));
   raw.uniforms.shadowDepth.value=map.depthTexture;raw.uniforms.crop.value.set(x,y,512,512);raw.uniforms.mapSize.value.set(map.width,map.height);
   const oldTarget=r.getRenderTarget();r.shadowMap.autoUpdate=false;r.setRenderTarget(target);r.render(quadScene,quadCamera);const pixels=new Uint8Array(512*512*4);r.readRenderTargetPixels(target,0,0,512,512,pixels);r.setRenderTarget(oldTarget);r.shadowMap.autoUpdate=true;
   let occupied=0,fractional=0,hash=2166136261;for(let i=0;i<pixels.length;i+=4){if(pixels[i]<128)occupied++;if(pixels[i]>0&&pixels[i]<255)fractional++;hash=Math.imul(hash^pixels[i],16777619)>>>0;}
   const err=gl.getError();return{pose:pose.name,mode,fallback,stats,camera:{e:a.camera.position.x,n:-a.camera.position.z,y:a.camera.position.y},shadow:{width:map.width,height:map.height,crop:[x,y,512,512],occupied,fractional,hash:hash.toString(16)},calls:probe.calls,uniforms:probe.shadowUniforms,glError:err,png};
  };window.__shadowProbe=probe;
  return{scene:a.scene.id,date:a.scene.target_date,detail:a.detail,renderer:gl.getParameter(gl.RENDERER),version:gl.getParameter(gl.VERSION),casters:probe.casters.reduce((m,x)=>(m[x.kind]=(m[x.kind]??0)+1,m),{}),owned:probe.casters.filter(x=>x.depth?.isMeshDepthMaterial).length};
 });
 check(report.setup.owned===Object.values(report.setup.casters).reduce((a,b)=>a+b,0),'every potential building/tree/bridge caster owns its patched depth material');
 const poses=[{name:'commercial',kind:'building',eye:[61.221,-90.6336,2.1],target:[93.08,-77.89,4.85]},
  {name:'bridge',kind:'bridge',eye:[723.1,-20.55,80],target:[843.1,69.45,0]},
  {name:'tree',kind:'tree',eye:[182.34,960.61,7],target:[207.34,975.61,5.15]}];
 for(const pose of poses)for(const mode of ['off','dither','hidden']){
  console.log(`Rendering ${pose.name} / ${mode} candidate and old-depth negative control`);
  const candidate=await page.evaluate(({pose,mode})=>window.__shadowProbe.frame(pose,mode,false),{pose,mode});
  fs.writeFileSync(path.join(OUT,`${pose.name}-${mode}.png`),Buffer.from(candidate.png.split(',')[1],'base64'));delete candidate.png;
  const old=await page.evaluate(({pose,mode})=>window.__shadowProbe.frame(pose,mode,true),{pose,mode});delete old.png;
  const frame={candidate,fallback:old};report.frames.push(frame);
  check(candidate.calls.some(c=>c.kind===pose.kind&&c.owned),`${pose.name}/${mode}: actual ${pose.kind} caster used its owned depth on GPU`);
  check(candidate.glError===0&&old.glError===0,`${pose.name}/${mode}: zero WebGL errors`);
  check(candidate.calls.every(c=>c.owned),`${pose.name}/${mode}: every context shadow call uses its owner`);
  if(mode==='off')check(candidate.shadow.hash===old.shadow.hash&&candidate.shadow.occupied>0,`${pose.name}: normal shadows unchanged against native fallback (${candidate.shadow.occupied} occupied samples)`);
  if(mode==='dither')check(candidate.shadow.occupied<old.shadow.occupied&&candidate.shadow.occupied>0,`${pose.name}: dither reduces actual shadow coverage (${candidate.shadow.occupied} < ${old.shadow.occupied})`);
  if(mode==='hidden')check(candidate.shadow.occupied===0&&old.shadow.occupied>0,`${pose.name}: hidden geometry leaves no shadow (${candidate.shadow.occupied} vs fallback ${old.shadow.occupied})`);
  for(const u of candidate.uniforms){check(u.mode===(mode==='dither'?1:0)&&u.hide?.[2]===(mode==='hidden'?1:0),`${pose.name}/${mode}: ${u.kind} GPU hide/view uniform values`);if(mode==='dither')check(u.gradeMode?.[2]===2&&Math.abs(u.gradeOpacity?.[2]-.34)<1e-6,`${pose.name}/${mode}: ${u.kind} GPU dither settings`);}
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
 }
 const final=await page.evaluate(()=>{const p=window.__shadowProbe;for(const{ o,depth }of p.casters)o.customDepthMaterial=depth;p.a.confidence.setHidden('reconstructed',false);p.a.confidence.set(false);return{programs:p.programs,sources:p.sources,problems:p.a.problems};});
 report.programs=Object.values(final.programs);report.problems=final.problems;
 for(const[id,src]of Object.entries(final.sources)){fs.writeFileSync(path.join(OUT,`depth-${id}.vert.glsl`),src.vertex);fs.writeFileSync(path.join(OUT,`depth-${id}.frag.glsl`),src.fragment);const row=report.programs.find(p=>p.id===Number(id));row.vertexSha256=sha(src.vertex);row.fragmentSha256=sha(src.fragment);}
 check(report.programs.every(p=>p.vertexCompiled&&p.fragmentCompiled&&p.linked),'every actual native depth program compiles and links');
 check(report.programs.some(p=>p.confidence&&p.instanced)&&report.programs.some(p=>p.confidence&&!p.instanced),'both near-instanced and bridge-batch GPU depth shaders contain confidence controls');
 check(report.errors.length===0&&report.consoleErrors.length===0&&report.networkErrors.length===0&&report.problems.length===0,'zero page, console/GLSL, network or application problems');
 check(verify(),'candidate source and data input hashes unchanged after proof');
} catch(e){report.failures.push(e.stack);console.error(e.stack);}finally{await browser.close();await new Promise(r=>server.close(r));report.finished=new Date().toISOString();report.pass=report.failures.length===0;fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(report.pass?'NATIVE CONFIDENCE SHADOW PROOF PASS':'NATIVE CONFIDENCE SHADOW PROOF FAIL');}
if(!report.pass)process.exitCode=1;
