// Outside-app diagnostic, default published code and profiles. No init scripts, URL flags or overrides.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const [url,profile,out]=process.argv.slice(2),address=new URL(url);
assert(['desktop','mobile'].includes(profile));
assert(address.protocol==='http:'&&address.hostname==='127.0.0.1'&&address.pathname==='/1904/'&&!address.search&&!address.hash&&!address.username&&!address.password);
assert(path.resolve(out).startsWith('/workspace/.cloud-setup/logs/transport-recovery/'));
assert(!fs.existsSync(out));fs.mkdirSync(out,{recursive:true});
const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'../RAIL-LIFECYCLE-DESKTOP-03/source-plan.json'),'utf8'));
let phase='not-launched',navigationSequence=0,browser,context,rc=1,failure=null;
const events=[],pageErrors=[],consoleErrors=[],states=[];
function event(type,payload={}){const row={sequence:events.length,at:new Date().toISOString(),phase,navigationSequence,type,...payload};events.push(row);fs.appendFileSync(path.join(out,'EVENTS.jsonl'),JSON.stringify(row)+'\n');}
function stateFile(){fs.writeFileSync(path.join(out,'STATE.json'),JSON.stringify({profile,plan,states,pageErrors,consoleErrors,failure},null,2)+'\n');}
(async()=>{
 try{
  event('protocol',{profile,URL:address.href,default_code_no_flags:true,native_default_tier:profile==='desktop'?'full':'light',scope:'Focused context-only diagnostic, NOT full lifecycle/photographic qualification'});
  browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined});
  context=await browser.newContext(profile==='desktop'?{viewport:{width:1280,height:800},deviceScaleFactor:1,isMobile:false,hasTouch:false}:{viewport:{width:390,height:780},deviceScaleFactor:3,isMobile:true,hasTouch:true});
  const page=await context.newPage();
  page.on('pageerror',error=>{const row={name:error.name,message:error.message,stack:error.stack,URL:page.url()};pageErrors.push(row);event('pageerror',row);stateFile();});
  page.on('console',message=>{
   const kind=message.type(),text=message.text();
   if(text.startsWith('NATIVE_CONTEXT_TRACE:')){try{event('native-context-event',JSON.parse(text.slice('NATIVE_CONTEXT_TRACE:'.length)));}catch(error){event('context-event-parser-error',{text,error:String(error)});rc=1;}}
   else if(kind==='error'){consoleErrors.push({text,location:message.location()});event('console-error',consoleErrors.at(-1));stateFile();}
  });
  page.on('framenavigated',frame=>{if(frame===page.mainFrame()){navigationSequence++;event('main-frame-navigation',{URL:frame.url()});}});
  page.on('requestfailed',request=>event('request-failed',{URL:request.url(),failure:request.failure()}));
  page.on('response',response=>{if(response.status()>=400)event('HTTP-error',{URL:response.url(),status:response.status()});});
  const snapshot=async label=>{
   const row=await page.evaluate(({label,zone})=>{const a=window.__chicago4d;let near=null,far=null;
    a.railway?.group.traverse(o=>{if(o.name!==`railway-rails-z${zone}`&&o.name!==`railway-rails-far-z${zone}`)return;
     const g=o.geometry,x={name:o.name,uuid:o.uuid,geometryUUID:g.uuid,visible:o.visible,positionCount:g.attributes.position?.count??null,indexCount:g.index?.count??null,
      keptBytes:Object.values(g.attributes).reduce((s,v)=>s+(v.array?.byteLength??0),0)+(g.index?.array?.byteLength??0),markedForUploadRelease:g.userData.uploadReleased===true};
     if(o.name===`railway-rails-z${zone}`)near=x;else far=x;});
    return {label,documentTimeOrigin:performance.timeOrigin,documentNow:performance.now(),blackboxPage:a.blackbox?.box?.page??null,
     ready:a.ready,error:a.error,year:a.year,detail:a.detail,welcome:a.welcome.state,crashGuard:{...a.crashGuard},uploadRelease:{...a.uploadRelease},
     contextLost:a.renderer.getContext().isContextLost(),GLerror:a.renderer.getContext().getError(),pixelRatio:a.renderer.getPixelRatio(),camera:a.camera.position.toArray(),
     pending:a.residency?.pending??0,near,far};},{label,zone:plan.zone});states.push(row);event('native-state',row);stateFile();return row;
  };
  const enter=async()=>{const got=await page.evaluate(async()=>{const w=window.__chicago4d.welcome,deadline=Date.now()+90000;let accepted=false;
    while(w.state!=='world'&&Date.now()<deadline){if(w.state==='welcome')accepted=w.enter('spawn');if(w.state!=='world')await new Promise(r=>setTimeout(r,100));}return {accepted,state:w.state};});assert.deepEqual(got,{accepted:true,state:'world'});};
  const settle=async()=>{const row=await page.evaluate(async zone=>{const a=window.__chicago4d,frame=()=>new Promise(requestAnimationFrame);let previous=null,stable=0,frames=0,state;
    const tick=async()=>{await frame();frames++;let selected=null;a.railway.group.traverse(o=>{if(o.name===`railway-rails-z${zone}`)selected={uuid:o.uuid,geometry:o.geometry.uuid,visible:o.visible,keptBytes:Object.values(o.geometry.attributes).reduce((s,v)=>s+(v.array?.byteLength??0),0)+(o.geometry.index?.array?.byteLength??0)};});
     state={camera:[...a.camera.position.toArray(),...a.camera.quaternion.toArray()],detail:a.detail,selected,census:{...a.railway.census}};const signature=JSON.stringify(state);stable=signature===previous?stable+1:0;previous=signature;};
    const start=performance.now();for(let i=0;i<3;i++)await tick();const drain=performance.now();while(((a.residency?.pending??0)>0||stable<2)&&performance.now()-drain<120000)await tick();
    return {frames,stableTransitions:stable,pending:a.residency?.pending??0,seconds:(performance.now()-start)/1000,state};},plan.zone);event('native-settlement',row);assert.ok(row.frames>=3&&row.stableTransitions>=2);assert.equal(row.pending,0);};
  const stand=async()=>{await page.evaluate(t=>{const a=window.__chicago4d;a.setFly(true);a.walker.teleport({local_e:t.e-3,local_n:t.n-3,altitude_m:8,yaw_deg:45,pitch_deg:-60});},plan.targets.track);await settle();};
  const pick=async()=>{const row=await page.evaluate(t=>{const a=window.__chicago4d,p=a.project(t.e,t.n,a.terrain.surfaceHeight(t.e,t.n)+0.024),hit=a.railway.pickAt(p,a.camera);return {NDC:p,id:hit?.id??null,distance:hit?.distance??null};},plan.targets.track);event('native-analytic-track-pick',row);assert.equal(row.id,plan.targets.track.expectedId);assert.ok(Number.isFinite(row.distance)&&row.distance>0);};
  phase='initial-native-boot';event('phase');await page.goto(address.href,{waitUntil:'load'});
  await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:420000});await snapshot('initial-ready');
  phase='initial-native-enter';event('phase');await enter();assert.equal(await page.evaluate(()=>window.__chicago4d.detail),profile==='desktop'?'full':'light');
  await stand();await pick();const before=await snapshot('before-context-loss');
  assert.equal(before.year,'1904');assert.equal(before.welcome,'world');assert.equal(before.error,null);assert.equal(before.GLerror,0);assert.ok(before.near?.visible);assert.equal(before.near.keptBytes,0);assert.equal(before.crashGuard.reloads,0);assert.equal(pageErrors.length,0);assert.equal(consoleErrors.length,0);
  await page.screenshot({path:path.join(out,'before-context-loss.png')});
  await page.evaluate(()=>{const a=window.__chicago4d,canvas=a.renderer.domElement;
   for(const name of ['webglcontextlost','webglcontextrestored'])canvas.addEventListener(name,e=>console.debug('NATIVE_CONTEXT_TRACE:'+JSON.stringify({nativeEvent:e.type,nativeAt:new Date().toISOString(),documentTimeOrigin:performance.timeOrigin,documentNow:performance.now(),defaultPrevented:e.defaultPrevented,
     ready:a.ready,error:a.error,year:a.year,detail:a.detail,welcome:a.welcome.state,crashGuard:{...a.crashGuard},uploadRelease:{...a.uploadRelease},contextLost:a.renderer.getContext().isContextLost()})));
  });
  phase='request-real-context-loss-and-restore';event('phase');
  const navigation=page.waitForNavigation({waitUntil:'domcontentloaded',timeout:240000});
  await page.evaluate(async()=>{const gl=window.__chicago4d.renderer.getContext(),ext=gl.getExtension('WEBGL_lose_context');if(!ext)throw Error('Native WEBGL_lose_context extension absent');
   const lost=new Promise(r=>gl.canvas.addEventListener('webglcontextlost',r,{once:true}));ext.loseContext();await lost;await new Promise(r=>setTimeout(r,50));ext.restoreContext();});
  phase='await-ordinary-native-navigation';event('phase');await navigation;
  phase='restored-native-boot';event('phase');await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000});await snapshot('restored-ready');await enter();await stand();await pick();const after=await snapshot('after-context-restore');
  assert.equal(after.crashGuard.reloads,1);assert.notEqual(after.documentTimeOrigin,before.documentTimeOrigin);assert.equal(after.detail,profile==='desktop'?'full':'light');assert.equal(after.welcome,'world');assert.equal(after.error,null);assert.equal(after.GLerror,0);assert.ok(after.near?.visible);assert.equal(after.near.keptBytes,0);
  await page.screenshot({path:path.join(out,'after-context-restore.png')});
  phase='strict-final-error-check';event('phase');assert.equal(pageErrors.length,0,'No pageerror is waived, even if native reload recovers');assert.equal(consoleErrors.length,0);rc=0;
 }catch(error){failure={name:error.name,message:error.message,stack:error.stack};event('diagnostic-failure',failure);stateFile();}
 finally{
  phase='owned-close';event('phase');const closeErrors=[];
  if(context)try{await context.close();}catch(error){closeErrors.push({stage:'context.close',stack:error.stack});rc=1;}
  if(browser)try{await browser.close();}catch(error){closeErrors.push({stage:'browser.close',stack:error.stack});rc=1;}
  const result={result:rc===0?'PASS focused native context-only controls; full lifecycle/photographic qualification NOT implied':'NONPASS focused native context-only controls',returncode:rc,profile,default_code_no_flags:true,states,pageErrors,consoleErrors,failure,closeErrors};
  fs.writeFileSync(path.join(out,'RESULT.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({result:result.result,returncode:rc,pageErrors:pageErrors.length,consoleErrors:consoleErrors.length,closeErrors:closeErrors.length}));process.exitCode=rc;
 }
})();
