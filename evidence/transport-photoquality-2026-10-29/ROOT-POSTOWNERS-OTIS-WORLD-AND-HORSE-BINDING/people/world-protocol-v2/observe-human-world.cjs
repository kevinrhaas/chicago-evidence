// Outside-checkout observer. UNRUN until root releases the native browser slot.
// The actor's clock, actions, pose, materials, renderer and animation loop are never written.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict'),{execFileSync}=require('node:child_process');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const [url,profile,out,guardPath]=process.argv.slice(2),CAP=32*1024*1024;
assert.ok(['desktop','mobile'].includes(profile));
const address=new URL(url);assert.equal(address.protocol,'http:');assert.equal(address.hostname,'127.0.0.1');assert.equal(address.pathname,'/1835/');assert.equal(address.search+address.hash+address.username+address.password,'');
assert.ok(path.resolve(out).startsWith('/workspace/.cloud-setup/logs/transport-recovery/'));assert.ok(!fs.existsSync(out),'Fresh output required');
const guard=JSON.parse(fs.readFileSync(guardPath)),expectedAssets=new Map(guard.published_files.filter(r=>r.path.includes('humans/')&&r.path.endsWith('.glb')).map(r=>['/'+r.path,r]));
fs.mkdirSync(out,{recursive:true});fs.mkdirSync(path.join(out,'video'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),write=(name,value)=>fs.writeFileSync(path.join(out,name),JSON.stringify(value,null,2)+'\n');
const errors={page:[],console:[],http:[],requests:[],body:[],closure:[],integrity:[]},assetResponses=[],responseJobs=[],rows=[];
let browser,context,page,videoPath,mediaFailure=null,timer,rc=1,video;
function mediaFiles(){const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.join(d,e.name)]);return walk(out).filter(f=>/\.(png|webm|mp4)$/i.test(f));}
function mediaCheck(){const bytes=mediaFiles().reduce((s,f)=>s+fs.statSync(f).size,0);if(bytes>CAP)throw Error(`Actual media ${bytes} exceeds ${CAP}-byte cap`);return bytes;}
// A new function read by page.evaluate; this never replaces or wraps a native function.
function inspectActor(){
 const a=window.__chicago4d,h=a.humans.get('rc_bardwell_otis');if(!h?.body)throw Error('Native Otis body absent');
 const V=a.camera.position.constructor,body=h.body,points=[],min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 for(const m of body.meshes){const p=m.geometry.getAttribute('position');for(let i=0;i<p.count;i++){const v=m.getVertexPosition(i,new V()).applyMatrix4(m.matrixWorld);for(let k=0;k<3;k++){min[k]=Math.min(min[k],v.getComponent(k));max[k]=Math.max(max[k],v.getComponent(k));}const q=v.clone().project(a.camera);points.push(q.toArray());}}
 const ndc={min:[Infinity,Infinity,Infinity],max:[-Infinity,-Infinity,-Infinity]};for(const p of points)for(let k=0;k<3;k++){ndc.min[k]=Math.min(ndc.min[k],p[k]);ndc.max[k]=Math.max(ndc.max[k],p[k]);}
 const target=min.map((v,i)=>(v+max[i])/2),q=new V(...target).project(a.camera),pick=a.humans.pickAt({x:q.x,y:q.y},a.camera);
 return {year:a.year,ready:a.ready,error:a.error,detail:a.detail,pixelRatio:a.renderer.getPixelRatio(),welcome:a.welcome.state,actorId:h.id,personId:h.personId,lod:h.lod,wanted:h.wanted,pending:!!h.pending,clip:h.clipName,actionClip:body.action?.getClip().name,actionPaused:body.action?.paused,actionEnabled:body.action?.enabled,mixerTime:body.mixer.time,actionTime:body.action?.time,counters:{...h.counters},costs:h.costsNow,position:h.position,state:h.state,worldBounds:{min,max},projectedBounds:ndc,target,targetNDC:q.toArray(),readOnlyPick:pick?.personId??null,camera:a.camera.position.toArray(),cameraQuaternion:a.camera.quaternion.toArray(),meshNames:body.meshes.map(m=>({name:m.name,material:m.material?.name,vertices:m.geometry.getAttribute('position').count})),glError:a.renderer.getContext().getError(),draw:{...a.renderer.info.render},pendingResidency:a.residency?.pending??0};
}
async function closeNativePanel(){
 // Approach naturally opens the resident card inside 3m. Close it with the visible native UI.
 const open=await page.evaluate(()=>window.__chicago4d.navigator?.level>0||document.querySelector('#hud')?.classList.contains('panel-open'));if(!open)return;
 for(const selector of ['#nav-close','#panel-close']){const control=page.locator(selector);if(await control.isVisible()){if(profile==='mobile')await control.tap();else await control.click();await page.waitForTimeout(250);break;}}
 assert.equal(await page.evaluate(()=>window.__chicago4d.navigator?.level??0),0,'Actual native panel docked before observing town');
}
async function settle(lod){
 await page.waitForFunction(expected=>{const h=window.__chicago4d?.humans.get('rc_bardwell_otis');return h?.body&&!h.pending&&h.lod===expected&&h.clipName==='idle_natural_v1'&&h.body.action?.enabled&&!h.body.action?.paused;},lod,{timeout:120000});
 await page.evaluate(async()=>{for(let i=0;i<3;i++)await new Promise(requestAnimationFrame);});
}
function assertView(r,lod){
 assert.equal(r.year,'1835');assert.equal(r.ready,true);assert.equal(r.error,null);assert.equal(r.welcome,'world');assert.equal(r.detail,profile==='desktop'?'full':'light');assert.equal(r.pixelRatio,1);assert.equal(r.lod,lod);assert.equal(r.pending,false);assert.equal(r.clip,'idle_natural_v1');assert.equal(r.actionClip,'idle_natural_v1');assert.equal(r.actionPaused,false);assert.equal(r.actionEnabled,true);assert.equal(r.state,'standing');assert.equal(r.personId,'rc_bardwell_otis');assert.equal(r.glError,0);assert.ok(r.costs.drawn&&r.costs.animates);assert.ok(r.draw.calls>0&&r.draw.triangles>0);
 assert.ok(r.projectedBounds.min[0]>-.98&&r.projectedBounds.max[0]<.98&&r.projectedBounds.min[1]>-.98&&r.projectedBounds.max[1]<.98,'Actual posed full figure fits camera');assert.ok(r.projectedBounds.min[2]>-1&&r.projectedBounds.max[2]<1);assert.ok(Math.abs(r.targetNDC[0])<.025&&Math.abs(r.targetNDC[1])<.025,'Actual figure center in native camera');assert.equal(r.readOnlyPick,'rc_bardwell_otis');
}
async function stand(label,e,pitch,lod){
 await page.evaluate(({e,pitch})=>window.__chicago4d.walker.teleport({local_e:e,local_n:-36.5,yaw_deg:270,pitch_deg:pitch}),{e,pitch});await settle(lod);await closeNativePanel();
 let r=await page.evaluate(inspectActor);write(`${label}-initial-camera-readback.json`,r);
 // Only the native walker authors camera orientation. Aim at the actual posed-body center.
 const de=r.target[0]-r.camera[0],dn=-r.target[2]+r.camera[2],dy=r.target[1]-r.camera[1],yaw=Math.atan2(de,dn)*180/Math.PI,aimPitch=Math.atan2(dy,Math.hypot(de,dn))*180/Math.PI;
 await page.evaluate(({e,yaw,aimPitch})=>window.__chicago4d.walker.teleport({local_e:e,local_n:-36.5,yaw_deg:yaw,pitch_deg:aimPitch}),{e,yaw,aimPitch});await settle(lod);r=await page.evaluate(inspectActor);write(`${label}-camera.json`,{requested_e:e,requested_n:-36.5,derived_yaw:yaw,derived_pitch:aimPitch,actual:r});assertView(r,lod);return r;
}
async function motion(label,lod){
 const before=await page.evaluate(inspectActor);write(`${label}-before-readback.json`,before);assertView(before,lod);await page.screenshot({path:path.join(out,`${label}-before.png`),timeout:90000});mediaCheck();
 const observed=await page.evaluate(async()=>{
  const a=window.__chicago4d,h=a.humans.get('rc_bardwell_otis'),body=h.body,V=a.camera.position.constructor,names=['head','neck_01','spine_01','spine_02','spine_03'],bones=Object.fromEntries(names.map(n=>[n,body.scene.getObjectByName(n)]));if(Object.values(bones).some(b=>!b))throw Error('Expected native bones missing');
  const shoes=body.meshes.filter(m=>(Array.isArray(m.material)?m.material:[m.material]).some(x=>x?.name==='footwear__closed_leather_shoes'));if(shoes.length!==1)throw Error('Expected one exact native footwear mesh');
  const footwear=()=>shoes.map(m=>({mesh:m.name,count:m.geometry.getAttribute('position').count,positions:Array.from({length:m.geometry.getAttribute('position').count},(_,i)=>m.getVertexPosition(i,new V()).applyMatrix4(m.matrixWorld).toArray())}));
  const frames=[],firstShoes=footwear(),start=performance.now(),initialCamera=[...a.camera.position.toArray(),...a.camera.quaternion.toArray()];
  do{await new Promise(requestAnimationFrame);if(h.body!==body)throw Error('Native body changed during observation');frames.push({performance_ms:performance.now(),mixer_time:body.mixer.time,action_time:body.action.time,animated:h.counters.animated,updates:h.counters.updates,clip:h.clipName,lod:h.lod,distance:h.distance,bones:Object.fromEntries(names.map(n=>[n,bones[n].quaternion.toArray()])),camera:[...a.camera.position.toArray(),...a.camera.quaternion.toArray()]});}while(performance.now()-start<8000);
  const lastShoes=footwear(),end=performance.now();return {real_start_ms:start,real_end_ms:end,elapsed_ms:end-start,frames,firstShoes,lastShoes,initialCamera,glError:a.renderer.getContext().getError()};
 });
 write(`${label}-motion.json`,observed);assert.ok(observed.elapsed_ms>=8000);assert.ok(observed.frames.length>=2);const f=observed.frames[0],last=observed.frames.at(-1);assert.ok(last.mixer_time>f.mixer_time&&last.animated>f.animated,'Native time and frames actually advance');assert.equal(observed.glError,0);
 assert.ok(observed.frames.every(x=>x.lod===lod&&x.clip==='idle_natural_v1'));assert.ok(observed.frames.every(x=>x.camera.every((v,i)=>Math.abs(v-observed.initialCamera[i])<1e-6)),'Native observer camera remained standing');
 const angles={};for(const name of ['head','neck_01','spine_02']){const q=f.bones[name];angles[name]=Math.max(...observed.frames.map(x=>2*Math.acos(Math.min(1,Math.abs(q.reduce((s,v,i)=>s+v*x.bones[name][i],0))))));assert.ok(angles[name]>1e-7,`Native ${name} quaternion changed`);}
 let drift=0;for(let m=0;m<observed.firstShoes.length;m++){assert.equal(observed.firstShoes[m].count,observed.lastShoes[m].count);for(let i=0;i<observed.firstShoes[m].count;i++)drift=Math.max(drift,Math.hypot(...observed.firstShoes[m].positions[i].map((v,k)=>v-observed.lastShoes[m].positions[i][k])));}assert.ok(drift<=1e-5,'All full footwear vertices remain planted within10micrometre numerical bound');
 const slow=observed.frames.slice(1).map((x,i)=>x.performance_ms-observed.frames[i].performance_ms).filter(x=>x>50),after=await page.evaluate(inspectActor);write(`${label}-after-readback.json`,after);assertView(after,lod);await page.screenshot({path:path.join(out,`${label}-after.png`),timeout:90000});mediaCheck();
 const row={label,lod,realElapsedMs:observed.elapsed_ms,observedFrames:observed.frames.length,mixerDelta:last.mixer_time-f.mixer_time,animatedDelta:last.animated-f.animated,slowFrameIntervalsOver50ms:slow,maximumObservedFrameMs:Math.max(0,...observed.frames.slice(1).map((x,i)=>x.performance_ms-observed.frames[i].performance_ms)),boneMaximumAngularChangeRadians:angles,fullFootwearVertexMaximumDriftM:drift,before,after};rows.push(row);write('MOTION-SUMMARY.json',{rows,scope:'Actual native unheld real-time windows; quarter-second native frame cap retained, no assertion of8simseconds per8real seconds'});
}
async function realInteraction(){
 await stand('interaction',-91.2,-10,profile==='desktop'?0:2);await closeNativePanel();
 await page.evaluate(()=>{const a=window.__chicago4d;window.__humanWorldObservedSelects=[];window.__humanWorldSelectListener=e=>window.__humanWorldObservedSelects.push({personId:e.detail.personId,instanceId:e.detail.instanceId,at:performance.now()});a.humans.events.addEventListener('select',window.__humanWorldSelectListener);});
 const frame=await page.evaluate(inspectActor),size=page.viewportSize(),canvas=page.locator('canvas').first();write('REAL-POINTER-FRAME.json',frame);assert.equal(frame.readOnlyPick,'rc_bardwell_otis');
 if(profile==='desktop'){
  // Native desktop inspection uses its locked crosshair; no direct select/pick action.
  await page.mouse.click(size.width/2,size.height/2);await page.waitForFunction(()=>!!document.pointerLockElement,null,{timeout:10000});await page.mouse.click(size.width/2,size.height/2);
 }else{
  const x=(frame.targetNDC[0]+1)*size.width/2+1,y=(1-frame.targetNDC[1])*size.height/2;assert.ok(x>=size.width/2,'Native touch right-half inspect gesture');await page.touchscreen.tap(x,y);
 }
 await page.waitForFunction(()=>window.__chicago4d.people?.state.open==='rc_bardwell_otis'&&window.__humanWorldObservedSelects.some(x=>x.personId==='rc_bardwell_otis'),null,{timeout:30000});await page.locator('#people-card').waitFor({state:'visible',timeout:30000});await page.waitForFunction(()=>document.querySelector('#people-card .people-card-body')?.getAttribute('aria-busy')!=='true',null,{timeout:30000});
 const card=await page.locator('#people-card').innerText();assert.match(card,/Otis\s+Bardwell|Bardwell\s+Otis/i);assert.match(card,/reconstruct|invented identity|no source names/i);const detail=await page.evaluate(()=>({personState:window.__chicago4d.people.state,selects:window.__humanWorldObservedSelects,cardHeading:document.querySelector('#people-card .people-card-name')?.textContent,html:document.querySelector('#people-card')?.outerHTML}));write('REAL-POINTER-RESIDENT-CARD.json',{...detail,text:card,gesture:profile==='desktop'?'native locked crosshair mouse click':'native right-half NDC touch tap',nativeHUDRetained:true});await page.screenshot({path:path.join(out,'resident-card.png'),timeout:90000});mediaCheck();
 await page.evaluate(()=>{window.__chicago4d.humans.events.removeEventListener('select',window.__humanWorldSelectListener);delete window.__humanWorldSelectListener;});
}
(async()=>{
 try{
  browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined});context=await browser.newContext({...profile==='desktop'?{viewport:{width:1280,height:800},deviceScaleFactor:1,isMobile:false,hasTouch:false}:{viewport:{width:390,height:780},deviceScaleFactor:3,isMobile:true,hasTouch:true},recordVideo:{dir:path.join(out,'video'),size:profile==='desktop'?{width:1280,height:800}:{width:390,height:780}}});page=await context.newPage();video=page.video();
  page.on('pageerror',e=>errors.page.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.console.push(m.text());});page.on('requestfailed',r=>errors.requests.push({url:r.url(),failure:r.failure()}));
  page.on('response',response=>{const pathname=new URL(response.url()).pathname;if(response.status()>=400)errors.http.push({url:response.url(),status:response.status()});if(!pathname.includes('/humans/')||!pathname.endsWith('.glb'))return;responseJobs.push((async()=>{try{const expected=expectedAssets.get(pathname);assert.ok(expected,'Actual human HTTP URL has pinned published bytes');assert.equal(response.status(),200);const bytes=await response.body(),row={url:response.url(),status:response.status(),bytes:bytes.length,sha256:sha(bytes),expectedSha256:expected.sha256};assetResponses.push(row);assert.equal(bytes.length,expected.bytes);assert.equal(row.sha256,expected.sha256);}catch(e){errors.body.push({url:response.url(),error:String(e)});}})());});
  timer=setInterval(()=>{try{mediaCheck();}catch(e){if(!mediaFailure){mediaFailure=String(e);context.close().catch(e=>errors.closure.push(String(e)));}}},1000);
  await page.goto(address.href,{waitUntil:'load'});await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:300000});
  const boot=await page.evaluate(()=>{const a=window.__chicago4d;return {year:a.year,yearType:typeof a.year,ready:a.ready,error:a.error,detail:a.detail,welcome:a.welcome.state,gateHidden:document.getElementById('gate').hasAttribute('hidden'),camera:a.camera?.position.toArray(),cameraQuaternion:a.camera?.quaternion.toArray(),pixelRatio:a.renderer.getPixelRatio(),performance_ms:performance.now()};});write('BOOT-NATIVE-BEFORE-ENTRY.json',boot);
  // Native smoke_renderer.mjs T2186 enterTown semantics: ready is not enterable.
  // Keep real draws and native animation running; never use neighboring holdDraws helper.
  const entry=await page.evaluate(async()=>{const a=window.__chicago4d,gate=document.getElementById('gate'),states=[],started=Date.now(),deadline=started+90000;let attempts=0;
   if(!gate.hasAttribute('hidden')){const welcome=a.welcome;if(welcome){while(welcome.state!=='world'&&Date.now()<deadline){if(states.at(-1)?.state!==welcome.state)states.push({state:welcome.state,at:Date.now()});if(welcome.state==='welcome'){attempts++;welcome.enter('spawn');}if(welcome.state!=='world')await new Promise(r=>setTimeout(r,100));}}else document.getElementById('home-roam')?.click();await new Promise(r=>setTimeout(r,150));document.exitPointerLock?.();}
   return {started_ms:started,ended_ms:Date.now(),deadline_ms:deadline,attempts,states,finalState:a.welcome.state,gateHidden:gate.hasAttribute('hidden'),native_entry_budget_ms:90000,rendererHeld:false};});write('NATIVE-ENTRY-T2186.json',entry);assert.equal(entry.finalState,'world');assert.equal(entry.gateHidden,true);
  const help=page.locator('#control-help');if(await help.isVisible()){const gotit=page.locator('#control-help-gotit');if(profile==='mobile')await gotit.tap({timeout:90000});else await gotit.click({timeout:90000});}

  for(const [label,e,pitch,lod] of [['near',-91.2,-10,profile==='desktop'?0:2],['mid',-84,-4,profile==='desktop'?1:2]]){await stand(label,e,pitch,lod);await motion(label,lod);}
  await realInteraction();await page.waitForFunction(()=>(window.__chicago4d.residency?.pending??0)===0,null,{timeout:60000});await page.waitForLoadState('networkidle',{timeout:30000});await Promise.all(responseJobs);
  const required=profile==='desktop'?[0,1]:[2];for(const lod of required)assert.ok(assetResponses.some(r=>new URL(r.url).pathname.endsWith(`/humans/web/bardwell_otis_1835.lod${lod}.glb`)),'Actual selected webLOD HTTP bytes verified');assert.equal(mediaFailure,null);assert.ok(Object.values(errors).every(xs=>xs.length===0),JSON.stringify(errors));rc=0;
 }catch(e){errors.integrity.push(e.stack||String(e));console.error(e.stack||String(e));}
 finally{
  if(timer)clearInterval(timer);if(context)try{await context.close();}catch(e){errors.closure.push(String(e));rc=1;}if(video)try{videoPath=await video.path();}catch(e){errors.closure.push(String(e));rc=1;}if(browser)try{await browser.close();}catch(e){errors.closure.push(String(e));rc=1;}await Promise.all(responseJobs);try{mediaCheck();}catch(e){mediaFailure=String(e);rc=1;}if(Object.values(errors).some(xs=>xs.length))rc=1;
  const media=mediaFiles().map(f=>({file:path.relative(out,f),bytes:fs.statSync(f).size,sha256:sha(fs.readFileSync(f))}));let videoFacts=null;
  try{assert.equal(media.filter(r=>r.file.endsWith('.png')).length,5,'Actual near/mid before/after and native card PNGs');assert.ok(videoPath&&fs.statSync(videoPath).size>1000,'Actual native profile video nonempty');videoFacts=JSON.parse(execFileSync('/usr/bin/ffprobe',['-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',videoPath],{encoding:'utf8'}));assert.ok(Number(videoFacts.format?.duration)>=16,'Video includes at least16 real seconds for both8s windows');assert.ok(videoFacts.streams.some(s=>s.codec_name==='vp8'&&s.width===(profile==='desktop'?1280:390)&&s.height===(profile==='desktop'?800:780)),'Actual native viewport video codec and dimensions');}catch(e){errors.integrity.push(String(e));rc=1;}
  write('RESULT.json',{status:rc===0?'NATIVE_WORLD_UNHELD_MOTION_AND_REAL_SELECTION_PASS_REQUIRES_ROOT_VIDEO_REVIEW':'NONPASS',returncode:rc,profile,rows,assetResponses,errors,media,mediaCapBytes:CAP,mediaFailure,videoPath,videoFacts,guard_manifest_sha256:sha(fs.readFileSync(guardPath)),nativeClockOrPoseWritten:false,wholeTicketOrPhotographicAcceptance:false,rootPersonalVideoAndImageReview:'PENDING'});process.exitCode=rc;
 }
})();
