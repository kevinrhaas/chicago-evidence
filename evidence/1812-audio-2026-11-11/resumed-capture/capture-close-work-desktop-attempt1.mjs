// Supplemental visual evidence only. Does not replace the native audio checks.
// Immutable published bytes, native day/work/actor/camera APIs; no source overlays,
// invented contacts, exposure changes or actor edits. Draws are held only during
// native camera/UI setup and ordinary work-pose waits. Native actor/day logic
// is unchanged; actual renderer is restored before each same-frame canvas image.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {chromium} from '/workspace/audio-tooling/node_modules/playwright/index.mjs';
assert(process.env.C4D_PUBLISHED_ROOT&&process.env.EXPECTED_BUILD_SHA,'Set immutable C4D_PUBLISHED_ROOT and exact EXPECTED_BUILD_SHA');
const published=path.resolve(process.env.C4D_PUBLISHED_ROOT),out=process.env.CLOSE_WORK_REPORT_DIR??'/workspace/audio-1812/review/close-work-results';
await fs.mkdir(out,{recursive:true});
const sha=x=>createHash('sha256').update(x).digest('hex');
const within=async(promise,ms)=>{let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(`Bounded browser operation timed out after ${ms}ms`)),ms);})]);}finally{clearTimeout(timer);}};
const buildBytes=await fs.readFile(path.join(published,'build.json')),build=JSON.parse(buildBytes);
assert.equal(build.sha??build.version,process.env.EXPECTED_BUILD_SHA);
const configRelative='data/humans/work_1812.json',configPath=path.join(published,configRelative);
const configBytes=await fs.readFile(configPath),workConfig=JSON.parse(configBytes);
assert.equal(workConfig.scene,'1812');assert.equal(typeof workConfig.asset,'string');
const dataRoot=path.join(published,'data'),propPath=path.resolve(dataRoot,workConfig.asset);
assert(propPath.startsWith(dataRoot+path.sep),'Work prop path must stay inside published data/');
const propBytes=await fs.readFile(propPath);
assert.equal(sha(propBytes),'64fdcbdffa35e00b0ed4704794993b21ae24286a3947bcb5961cfc1872180e7f','Capture the unchanged reviewed work prop geometry');
const workEvidence={config:{path:configRelative,bytes:configBytes.length,sha256:sha(configBytes)},
  prop:{asset:workConfig.asset,path:path.relative(published,propPath),bytes:propBytes.length,sha256:sha(propBytes)}};
const codeNames=['main.js','human-days.js','human-actions.js','work-activity.js','work-audio.js'];
const codeHashes=async()=>Object.fromEntries(await Promise.all(codeNames.map(async n=>[n,sha(await fs.readFile(path.join(published,'walk/js',n)))])));
const initialHashes=await codeHashes();
const report={kind:'supplemental same-frame native rendered canvas close work views',build,published,
  reviewedSourceTree:process.env.REVIEWED_SOURCE_TREE??null,
  provenanceNote:'Build stamp and caller-supplied reviewed source tree are separate identities.',
  codeHashes:initialHashes,workEvidence,harnessSha256:sha(await fs.readFile(new URL(import.meta.url))),
  exposureChanged:false,rendererHeld:true,rendererHoldScope:'Native arrival, camera/UI setup and waiting for an ordinary primary work pose; native day/actor logic continues unchanged. Original renderer restored immediately for actual same-frame canvas capture.',physicalListening:false,visualQualityReviewed:false,coverage:'Missing desktop Full-detail views only. The two approved phone images remain in close-work-observed-ui-results. One clear native front/oblique view per task; no continuous animation-quality claim.',captureScope:'Canvas-only native renderer observer: original render always runs unchanged, then pixels and pose sampled synchronously. Does not include HUD pixels; UI state is attested. Contact/audio timing is proven separately by the original native checks.',results:[]};
const proxyUrl=process.env.HTTPS_PROXY||process.env.HTTP_PROXY||process.env.https_proxy||process.env.http_proxy;
const u=proxyUrl?new URL(proxyUrl):null;
const proxy=u?{server:u.origin,...(u.username?{username:decodeURIComponent(u.username),password:decodeURIComponent(u.password)}:{})}:undefined;
const base='https://chicago.polecat.live/4d/';
const mime={'.js':'text/javascript','.json':'application/json','.html':'text/html','.css':'text/css','.wasm':'application/wasm',
  '.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.svg':'image/svg+xml','.glb':'model/gltf-binary'};
const widths=[1280];
for(const width of widths){
  console.log(new Date().toISOString(), "Boot close work", width);
  const detail=width===390?'light':'full',row={width,detail,errors:[],missing:[],views:[]};report.results.push(row);
  const browser=await chromium.launch({proxy,executablePath:process.env.PW_EXECUTABLE??'/usr/bin/chromium',headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});
  let page;
  try{
    const context=await browser.newContext({viewport:{width,height:width===390?780:800},hasTouch:width===390,serviceWorkers:'block'});
    await context.route(base+'**',async route=>{
      const rel=decodeURIComponent(new URL(route.request().url()).pathname).replace(/^\/4d\//,'');
      let file=path.resolve(published,rel);if(!file.startsWith(published+path.sep))return route.fulfill({status:403});
      try{if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');await route.fulfill({body:await fs.readFile(file),contentType:mime[path.extname(file)]??'application/octet-stream'});}
      catch{row.missing.push(rel);await route.fulfill({status:404,body:rel});}
    });
    page=await context.newPage();page.setDefaultTimeout(90000);page.on('pageerror',e=>row.errors.push(e.message));page.on('console',m=>{if(m.text().startsWith('[close-work]'))console.log(new Date().toISOString(),m.text());});
    await page.addInitScript(detail=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail,soundMaster:0,soundAmbience:0,soundMusic:0,soundEffects:1,timeOfDay:'15:00'})),detail);
    await page.goto(base+'walk/?year=1812&keep-geometry=1',{waitUntil:'domcontentloaded',timeout:60000});
    await page.waitForFunction(()=>window.__chicago4d?.ready&&__chicago4d.welcome?.state==='welcome',null,{timeout:240000,polling:500});
    row.stage='native scene ready';console.log(new Date().toISOString(),row.stage,width);
    const hold=async(on,scope)=>{
      const receipt=await page.evaluate(({on,scope})=>{
        const a=__chicago4d;
        if(on&&!window.__closeWorkRender){window.__closeWorkRender=a.renderer.render;a.renderer.render=(s,c)=>c?.updateMatrixWorld?.();}
        else if(!on&&window.__closeWorkRender){a.renderer.render=window.__closeWorkRender;delete window.__closeWorkRender;}
        return{on,scope,frame:a.renderer.info.render.frame,at:performance.now()};
      },{on,scope});
      (row.rendererHolds??=[]).push(receipt);return receipt.frame;
    };
    await hold(true,'native arrival buttons');
    row.arrivalControl=await page.evaluate(()=>{
      const nodes=document.querySelectorAll('#arrival-sound'),el=nodes[0],r=el?.getBoundingClientRect();
      return{count:nodes.length,rect:r?.toJSON(),hidden:el?.hidden,display:el?getComputedStyle(el).display:null,visibility:el?getComputedStyle(el).visibility:null};
    });
    assert.equal(row.arrivalControl.count,1);assert(row.arrivalControl.rect.width>0&&row.arrivalControl.rect.height>0);
    console.log(new Date().toISOString(),'Actual arrival control',width,JSON.stringify(row.arrivalControl));
    await page.locator('#arrival-sound').click({noWaitAfter:true,timeout:30000});
    await page.locator('#home-roam').click({noWaitAfter:true,timeout:30000});
    await page.waitForFunction(()=>__chicago4d.welcome.state==='world'&&__chicago4d.journey.state==='exploring',null,{timeout:90000});
    await page.waitForFunction(()=>__chicago4d.sound?.state.context==='running',null,{timeout:90000,polling:100});
    // Keep setup draws held; native actor/day logic continues normally.
    row.stage='native town entered';console.log(new Date().toISOString(),row.stage,width);
    await page.evaluate(()=>document.exitPointerLock?.());await page.mouse.move(2,2);
    assert.equal(await page.evaluate(()=>__chicago4d.detail),detail);
    const closeUi=async()=>{
      row.stage='await Home then close drawer';
      await hold(true,'await Home then close drawer');
      const closed=await page.evaluate(async()=>{
        const a=__chicago4d;
        // closeApp starts selection without awaiting it. Await the real Home
        // mount first, then close/dock so a late app mount cannot reopen it.
        await a.navigator.select('home');
        a.hud.setPanel(false);a.navigator.dock();document.exitPointerLock?.();
        return{panelHidden:document.getElementById('panel')?.hidden,level:a.navigator.level,app:a.navigator.app};
      });
      row.lastCloseUi=closed;console.log(new Date().toISOString(),'Native close result',width,JSON.stringify(closed));
      await page.mouse.move(2,2);
      await page.waitForFunction(()=>document.getElementById('panel')?.hidden&&__chicago4d.navigator.level===0,null,{timeout:30000,polling:100});
      // Restore only when the native capture observer is ready.
      row.stage='drawer closed';console.log(new Date().toISOString(),row.stage,width,row.currentTask,row.currentSide);
    };
    const proof=()=>page.evaluate(()=>{
      const a=__chicago4d,id='hi_town_chicago_militia_unnamed_4_1812',actor=a.humans.get(id),g=a.workActivity.group;
      const position=p=>({x:p.x,y:p.y,z:p.z});
      const project=o=>{const p=o.getWorldPosition(o.position.clone()),ndc=p.clone().project(a.camera);return{world:position(p),ndc:position(ndc),pixel:{x:(ndc.x+1)*innerWidth/2,y:(1-ndc.y)*innerHeight/2}};};
      const markers=Object.fromEntries(['work_contact','hammer_strike','work_chest','work_hammer'].map(n=>[n,project(g.getObjectByName(n))]));
      return{work:a.workActivity.state,audio:a.sound.state.recorded.work,naturalWork:a.days.workSource(id),markers,
        actor:{id:actor.id,state:actor.state,heading:actor.heading,lod:actor.lod,visible:actor.root.visible,bodyLoaded:!!actor.body,counters:{...actor.counters}},
        camera:position(a.camera.position),walker:{e:a.walker.state.e,n:a.walker.state.n,flying:a.walker.state.flying},
        time:a.timeOfDay.current,season:a.season.current,renderFrame:a.renderer.info.render.frame,
        panelHidden:document.getElementById('panel').hidden,navigatorLevel:a.navigator.level,rendererHeld:!!window.__closeWorkRender};
    });
    for(const task of [
      {id:'militia-packing-chest',season:'summer',date:'1812-08-14',hour:'15:00',e:1082,n:165,heading:270},
      {id:'militia-piazza-repair',season:'spring',date:'1812-04-15',hour:'10:00',e:1072.5,n:177,heading:90},
    ]){
      await hold(true,'camera/UI setup and native work wait');
      row.currentTask=task.id;row.stage='set native task date and approach';
      console.log(new Date().toISOString(),row.stage,width,task.id,task.date,task.hour);
      await page.evaluate(async task=>{
        const a=__chicago4d;await a.season.set(task.season);await a.timeOfDay.set(task.hour);
        if(a.timeOfDay.current.date!==task.date)throw Error('Native work date mismatch');
        a.walker.teleport({local_e:task.e+6,local_n:task.n-7,yaw_deg:320});
      },task);
      await page.waitForFunction(id=>{const a=__chicago4d;return a.workActivity?.state.active&&a.workActivity.state.taskId===id&&a.days.workSource('hi_town_chicago_militia_unnamed_4_1812')?.active;},task.id,{timeout:150000,polling:100});
      row.stage='actual work active';console.log(new Date().toISOString(),row.stage,width,task.id);
      for(const side of [0]){
        row.currentSide=side;row.stage='wait actual primary work for front-side ground';
        await page.waitForFunction(id=>{const a=__chicago4d;return a.workActivity?.state.active&&a.workActivity.state.taskId===id&&a.days.workSource('hi_town_chicago_militia_unnamed_4_1812')?.active;},task.id,{timeout:240000,polling:100});
        row.stage='choose close front-side ground';
        console.log(new Date().toISOString(), "Capture", width, task.id, side);
        const poseHandle=await page.waitForFunction(({side,task})=>{
          const a=__chicago4d,id='hi_town_chicago_militia_unnamed_4_1812',source=a.days.workSource(id),actor=a.humans.get(id),t=a.terrain;
          if(!source?.active)return false;
          const r=source.heading*Math.PI/180,forward={e:Math.sin(r),n:Math.cos(r)},right={e:Math.cos(r),n:-Math.sin(r)};
          const candidates=[];
          for(const radius of [3.5,4,4.5,5,5.5,6,6.5,7,7.5,8])for(const angle of [0,-15,15,-30,30,-45,45,-60,60,-75,75]){
            const q=(source.heading+angle)*Math.PI/180,e=source.at.e+Math.sin(q)*radius,n=source.at.n+Math.cos(q)*radius;
            const ground=t.surfaceHeight(e,n),inside=t.heightfield.contains(e,n),water=t.isWater(e,n);
            const blocked=a.router?.built&&a.router.blockedAt(e,n);
            const neighbours=a.humans.actors.filter(x=>x.root?.visible&&!x.indoors).map(x=>({id:x.id,distance:Math.hypot(x.e-e,x.n-n),radius:x.instance.interaction?.radius_m??0})).sort((a,b)=>a.distance-b.distance).slice(0,8);
            const safeApproach=a.humans.actors.filter(x=>x.root?.visible&&!x.indoors).every(x=>Math.hypot(x.e-e,x.n-n)>(x.id===id?(x.instance.interaction?.radius_m??0)+.4:.75));
            const de=source.at.e-e,dn=source.at.n-n,len2=de*de+dn*dn;
            const occluders=a.humans.actors.filter(x=>x.id!==id&&x.root?.visible&&!x.indoors).filter(x=>{const t=((x.e-e)*de+(x.n-n)*dn)/len2;return t>0&&t<1.12&&Math.hypot(x.e-(e+t*de),x.n-(n+t*dn))<.95;}).map(x=>x.id);
            candidates.push({e,n,radius,angle,inside,water,blocked:!!blocked,safeApproach,occluders});
            if(!inside||water||!Number.isFinite(ground)||blocked||!safeApproach||occluders.length)continue;
            const target={e:source.at.e+forward.e*.35,n:source.at.n+forward.n*.35,y:actor.root.position.y+1.0};
            const yaw=Math.atan2(target.e-e,target.n-n)*180/Math.PI;
            a.walker.teleport({local_e:e,local_n:n,yaw_deg:yaw});
            const eye=a.walker.state.eyeY,range=Math.hypot(target.e-e,target.n-n);
            const pitch=Math.atan2(target.y-eye,range)*180/Math.PI;
            a.walker.teleport({local_e:e,local_n:n,yaw_deg:yaw,pitch_deg:pitch});
            return{task:task.id,side,angle,source,target,e,n,ground,yaw,pitch,distance:Math.hypot(e-source.at.e,n-source.at.n),neighbours,candidateCount:candidates.length,candidates:candidates.slice(0,16)};
          }
          return false; // Wait for ordinary crowd motion to open a native view.
        },{side,task},{timeout:240000,polling:500});
        const pose=await poseHandle.jsonValue();await poseHandle.dispose();
        row.lastPose=pose;console.log(new Date().toISOString(),'Native close pose',width,task.id,side,JSON.stringify({e:pose.e,n:pose.n,yaw:pose.yaw,pitch:pose.pitch,distance:pose.distance}));
        await closeUi();
        row.stage='wait native document fonts';
        const fonts=await within(page.evaluate(async()=>{
          const before=document.fonts?.status??'unsupported';if(document.fonts)await document.fonts.ready;
          return{before,after:document.fonts?.status??'unsupported'};
        }),30000);
        row.lastFonts=fonts;console.log(new Date().toISOString(),'Native fonts ready',width,JSON.stringify(fonts));
        row.stage='wait ordinary early work pose under setup-only draw hold';
        await page.waitForFunction(id=>{const w=__chicago4d.workActivity.state;return w.active&&w.taskId===id&&w.phase<.2&&w.handError<=.08;},task.id,{timeout:120000,polling:50});
        row.stage='observe next native rendered active work canvas';
        const captured=await within(page.evaluate(taskId=>new Promise((resolve,reject)=>{
          const a=__chicago4d,renderer=a.renderer,original=window.__closeWorkRender??renderer.render;
          // Atomically restore the native renderer while installing a call-through observer.
          const setupHoldRestored=!!window.__closeWorkRender;delete window.__closeWorkRender;
          const initialFrame=renderer.info.render.frame;
          let done=false;const stats={frames:0,uiCloses:0,rejections:{},last:null};window.__closeWorkObserverStats=stats;
          const rejectFrame=(reason,extra={})=>{stats.rejections[reason]=(stats.rejections[reason]??0)+1;stats.last={reason,...extra};if(stats.frames%20===0)console.log('[close-work] '+JSON.stringify(stats));};
          const restore=()=>{if(renderer.render===observer)renderer.render=original;clearTimeout(timer);};
          const timer=setTimeout(()=>{if(!done){done=true;restore();reject(Error('No eligible native rendered work pose within 240s'));}},240000);
          function observer(...args){
            // Always render the actual scene with the unmodified native function.
            // Reading pixels directly afterwards avoids a cross-frame pose race.
            let result;
            try{result=original.apply(this,args);}catch(error){done=true;restore();reject(error);throw error;}
            if(done)return result;
            try{
              stats.frames++;
              if(!document.getElementById('panel')?.hidden||a.navigator.level!==0){a.hud.setPanel(false);a.navigator.dock();stats.uiCloses++;}
              const id='hi_town_chicago_militia_unnamed_4_1812',actor=a.humans.get(id),work=a.workActivity.state;
              if(window.__closeWorkRender||renderer.info.render.frame<=initialFrame||!work.active||work.taskId!==taskId
                ||work.handError>.08||!actor?.root.visible||actor.state!=='working'||!a.workActivity.group.visible
                ||!document.getElementById('panel')?.hidden||a.navigator.level!==0){rejectFrame('native-work-or-ui',{active:work.active,task:work.taskId,phase:work.phase,level:a.navigator.level,frame:renderer.info.render.frame});return result;}
              const e=a.camera.position.x,n=-a.camera.position.z,de=actor.e-e,dn=actor.n-n,len2=de*de+dn*dn;
              const occluders=a.humans.actors.filter(x=>x.id!==id&&x.root?.visible&&!x.indoors).filter(x=>{const t=((x.e-e)*de+(x.n-n)*dn)/len2;return t>0&&t<1.12&&Math.hypot(x.e-(e+t*de),x.n-(n+t*dn))<.95;});
              // .95m corridor is a conservative screening heuristic, not pixel visibility.
              // Save such a frame truthfully as provisional for visual inspection.
              const position=p=>({x:p.x,y:p.y,z:p.z});
              const project=o=>{const p=o.getWorldPosition(o.position.clone()),ndc=p.clone().project(a.camera);return{world:position(p),ndc:position(ndc),pixel:{x:(ndc.x+1)*innerWidth/2,y:(1-ndc.y)*innerHeight/2}};};
              const markers=Object.fromEntries(['work_contact','hammer_strike','work_chest','work_hammer'].map(n=>[n,project(a.workActivity.group.getObjectByName(n))]));
              const focus=markers.work_contact.ndc;
              if(Math.abs(focus.x)>=.8||Math.abs(focus.y)>=.8||focus.z<=-1||focus.z>=1){rejectFrame('framing',{focus});return result;}
              const state={corridorHeuristicM:.95,provisionalVisibility:occluders.length>0,corridorActors:occluders.map(x=>({id:x.id,e:x.e,n:x.n})),setupHoldRestored,work,audio:a.sound.state.recorded.work,naturalWork:a.days.workSource(id),markers,
                actor:{id:actor.id,state:actor.state,heading:actor.heading,lod:actor.lod,visible:actor.root.visible,bodyLoaded:!!actor.body,counters:{...actor.counters}},
                camera:position(a.camera.position),walker:{e:a.walker.state.e,n:a.walker.state.n,flying:a.walker.state.flying},
                time:a.timeOfDay.current,season:a.season.current,renderFrame:renderer.info.render.frame,
                panelHidden:document.getElementById('panel').hidden,navigatorLevel:a.navigator.level,rendererHeld:false,
                canvas:{width:renderer.domElement.width,height:renderer.domElement.height,cssWidth:innerWidth,cssHeight:innerHeight},
                captureAt:performance.now()};
              const png=renderer.domElement.toDataURL('image/png');
              done=true;restore();resolve({state,png,initialFrame,restored:renderer.render===original,stats});
            }catch(error){done=true;restore();reject(error);}
            return result;
          }
          renderer.render=observer;
        }),task.id),250000);
        row.rendererHolds.push({on:false,scope:'atomic native renderer restoration for canvas observation',frame:captured.initialFrame});
        const before=captured.state;row.lastBeforeCapture=before;
        assert(before.setupHoldRestored,'Observer must restore the held native renderer before its actual draw');
        assert(captured.restored&&!before.rendererHeld&&before.renderFrame>captured.initialFrame);
        assert(before.work.active&&before.work.taskId===task.id&&before.naturalWork?.active);
        assert(before.work.handError<=.08&&before.actor.visible&&before.actor.state==='working');
        assert(before.panelHidden&&before.navigatorLevel===0&&!before.walker.flying);
        assert.deepEqual(before.work.errors,[]);assert.deepEqual(before.audio.errors,[]);
        assert(captured.png.startsWith('data:image/png;base64,'));
        const bytes=Buffer.from(captured.png.split(',')[1],'base64');assert(bytes.length>1000);
        const file=path.join(out,`${width}-${task.id}-front-oblique.png`);
        await fs.writeFile(file,bytes);
        console.log(new Date().toISOString(), "Captured native canvas", file, 'frame',before.renderFrame,'phase',before.work.phase);
        row.views.push({file,pose,before,fonts,pngBytes:bytes.length,pngSha256:sha(bytes),observerRestored:captured.restored,observerStats:captured.stats,
          note:'Canvas pixels and active native work pose captured synchronously after the same actual native render following setup/wait draw hold. No HUD pixels; closed UI attested. Any corridor heuristic flag requires image review. This proves a rendered pose, not continuous animation, exact impact timing or physical listening.'});
      }
    }
    assert.deepEqual(row.errors,[]);assert.deepEqual(row.missing,[]);
    assert.deepEqual(await fs.readFile(path.join(published,'build.json')),buildBytes);assert.deepEqual(await codeHashes(),initialHashes);
    assert.deepEqual(await fs.readFile(configPath),configBytes,'Published work config must remain unchanged');
    assert.deepEqual(await fs.readFile(propPath),propBytes,'Published work prop must remain unchanged');
    row.passed=true;
  }catch(e){
    row.error=e.stack;
    console.error(new Date().toISOString(),'Close work failed',width,row.stage,String(e));
    const deadline=Date.now()+30000;
    const bounded=async(promise,ms)=>{let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(`Diagnostic timeout after ${ms}ms`)),ms);})]);}finally{clearTimeout(timer);}};
    if(page&&!page.isClosed()){
      try{
        row.failureDiagnostic=await bounded(page.evaluate(()=>{
          const a=window.__chicago4d,id='hi_town_chicago_militia_unnamed_4_1812';
          const cap=(v,d=0)=>{
            if(v==null||typeof v==='number'||typeof v==='boolean')return v;
            if(typeof v==='string')return v.slice(0,1200);
            if(d>=5)return '[depth limit]';
            if(Array.isArray(v))return v.slice(0,24).map(x=>cap(x,d+1));
            if(typeof v==='object')return Object.fromEntries(Object.entries(v).slice(0,32).map(([k,x])=>[k,cap(x,d+1)]));
            return String(v).slice(0,120);
          };
          const read=fn=>{try{return cap(fn());}catch(error){return{diagnosticError:String(error).slice(0,500)};}};
          const panel=document.getElementById('panel');
          return{
            ready:a?.ready,error:a?.error,detail:a?.detail,season:a?.season?.current,fontsStatus:document.fonts?.status,rendererHeld:!!window.__closeWorkRender,
            observer:read(()=>window.__closeWorkObserverStats),arrivalControl:read(()=>({count:document.querySelectorAll('#arrival-sound').length,rect:document.getElementById('arrival-sound')?.getBoundingClientRect().toJSON()})),
            date:read(()=>a?.timeOfDay?.current),journey:a?.journey?.state,welcome:a?.welcome?.state,
            work:read(()=>a?.workActivity?.state),naturalWork:read(()=>a?.days?.workSource?.(id)),
            actor:read(()=>{const x=a?.humans?.get?.(id);return x?{id:x.id,state:x.state,e:x.e,n:x.n,heading:x.heading,
              inRange:x.inRange,distance:x.distance,lod:x.lod,visible:x.root?.visible,body:!!x.body,indoors:x.indoors,
              path:!!x.path,route:!!x.route,counters:x.counters,clip:x.clipName,actionTime:x.body?.action?.time}:null;}),
            hud:read(()=>({panelHidden:panel?.hidden,panelHasHidden:panel?.hasAttribute('hidden'),
              panelDisplay:panel?getComputedStyle(panel).display:null,panelRect:panel?.getBoundingClientRect().toJSON(),
              panelParent:panel?.parentElement?.id,panelOpen:a?.hud?.panelOpen?.(),tab:a?.hud?.tab,
              navigatorLevel:a?.navigator?.level,navigatorApp:a?.navigator?.app,detent:a?.navigator?.detent,
              activeElement:document.activeElement?.id,settings:a?.hud?.settings})),
            audio:read(()=>a?.sound?.state),problems:read(()=>a?.problems),
          };
        }),20000);
      }catch(error){row.failureDiagnosticError=String(error);}
      const remaining=deadline-Date.now();
      if(remaining>250){
        const file=path.join(out,`${width}-failure.png`);
        try{await bounded(page.screenshot({path:file,timeout:remaining-100}),remaining);row.failureScreenshot=file;}
        catch(error){row.failureScreenshotError=String(error);}
      }
    }
    throw e;
  }
  finally{await browser.close();await fs.writeFile(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');}
}
console.log('CLOSE WORK CAPTURE COMPLETE: same-frame native rendered canvas front-side views; visual quality requires inspection.');
