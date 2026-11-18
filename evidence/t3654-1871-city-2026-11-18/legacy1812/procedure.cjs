const fs=require('fs'),http=require('http'),path=require('path');
const {chromium}=require('playwright');
(async()=>{
 const root=path.resolve(process.env.SMOKE_ROOT),out=process.env.QA_OUT||'/tmp/1812-legacy-probe';fs.mkdirSync(out,{recursive:true});
 const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.wasm':'application/wasm','.glb':'model/gltf-binary','.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.ktx2':'image/ktx2'};
 const server=http.createServer((req,res)=>{let p=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));try{if(!p.startsWith(root+path.sep))throw Error('path');if(fs.statSync(p).isDirectory())p=path.join(p,'index.html');res.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(res);}catch{res.writeHead(404);res.end('missing');}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});const reports=[];
 try{for(const viewport of['mobile','desktop']){
  const context=await browser.newContext({viewport:viewport==='mobile'?{width:390,height:780}:{width:1280,height:800},deviceScaleFactor:1,isMobile:viewport==='mobile',hasTouch:viewport==='mobile'});
  await context.addInitScript(()=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail:'light',quality:1})));
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));const start=Date.now();
  await page.goto(`http://127.0.0.1:${server.address().port}/1812/`,{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:300000,polling:500});
  const boot=await page.evaluate(()=>({ready:__chicago4d.ready,error:__chicago4d.error}));if(!boot.ready||boot.error)throw Error(JSON.stringify(boot));
  await page.waitForFunction(()=>__chicago4d.welcome.state==='welcome',null,{timeout:90000,polling:300});
  await page.evaluate(()=>__chicago4d.welcome.enter('spawn'));
  await page.waitForFunction(()=>__chicago4d.welcome.state==='world',null,{timeout:90000,polling:300});
  const result=await page.evaluate(()=>{
   const a=__chicago4d;document.exitPointerLock?.();a.renderer.setAnimationLoop(null);a.setFly(false);a.walker.teleport({local_e:1112,local_n:180,yaw_deg:225});
   const before={...a.walker.enu};const intent={forward:1,strafe:0,rise:0,sprint:false,flying:false,yawDelta:0,pitchDelta:0,clearLook(){}};
   for(let i=0;i<60;i++)a.walker.update(1/60,intent);
   const after={...a.walker.enu};a.world.follow(a.camera.position);a.world.aim(a.camera);a.renderer.render(a.scene3d,a.camera);
   const gl=a.renderer.getContext(),w=gl.drawingBufferWidth,h=gl.drawingBufferHeight,px=new Uint8Array(w*h*4);gl.readPixels(0,0,w,h,gl.RGBA,gl.UNSIGNED_BYTE,px);let sum=0,lit=0;
   for(let i=0;i<px.length;i+=4){const v=.2126*px[i]+.7152*px[i+1]+.0722*px[i+2];sum+=v;if(v>5)lit++;}
   return{year:a.scene?.id??'1812',before,after,moved:Math.hypot(after.e-before.e,after.n-before.n),meanLuminance:sum/(w*h),nonblackFraction:lit/(w*h),sun:a.world.sun,draws:a.renderer.info.render.calls};
  });
  const pass=errors.length===0&&result.moved>.3&&result.meanLuminance>5&&result.nonblackFraction>.5;
  await page.screenshot({path:path.join(out,viewport+'.png')});reports.push({viewport,pass,seconds:(Date.now()-start)/1000,errors,...result});console.log(JSON.stringify(reports.at(-1)));await context.close();
 }}finally{await browser.close();server.close();fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(reports,null,2)+'\n');}
 if(reports.length!==2||reports.some(r=>!r.pass))process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
