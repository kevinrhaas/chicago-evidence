const {chromium}=require('playwright');
const fs=require('node:fs');
const ids={dorothy:'pa1904_stirling_william_r_c1900_dorothy_sterling',alice:'pa1904_stirling_william_r_c1900_alice_m_sterling'};
(async()=>{
 const b=await chromium.launch({headless:true,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
 const p=await b.newPage({viewport:{width:1400,height:1000}});const errors=[];
 p.on('pageerror',e=>{errors.push(e.message);console.log('PAGEERROR',e.message);});
 p.setDefaultTimeout(120000);
 await p.addInitScript(()=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail:'balanced'})));
 // This is an untimed still-capture harness. Hold software draws during boot,
 // retaining the renderer's original method for every final native capture.
 // No app module, material, geometry, lighting or assignment is replaced.
 await p.addInitScript(()=>{
  let app;
  Object.defineProperty(window,'__chicago4d',{configurable:true,get:()=>app,set(value){
   app=value;let renderer=value.renderer;
   Object.defineProperty(value,'renderer',{configurable:true,enumerable:true,get:()=>renderer,set(next){
    renderer=next;if(!next)return;
    window.__appRender=next.render.bind(next);
    next.render=(s,c)=>c?.updateMatrixWorld?.();
   }});
   if(renderer)value.renderer=renderer;
  }});
 });
 await p.goto('http://127.0.0.1:3005/4d/walk/?year=1904&warm=0&firstupload=0',{waitUntil:'domcontentloaded',timeout:180000});
 await p.waitForFunction(()=>window.__chicago4d?.ready,null,{timeout:240000});
 console.log('APP READY');
 await p.evaluate(()=>{if(!window.__appRender)throw Error('Native renderer was not retained');});
 await p.waitForFunction(()=>window.__chicago4d.welcome.state==='welcome',null,{timeout:120000});
 await p.evaluate(()=>document.getElementById('home-roam').click());
 await p.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:120000});
 await p.evaluate(()=>{const a=window.__chicago4d;a.renderer.setAnimationLoop(null);a.navigator.dock();document.exitPointerLock?.();});
 console.log('WORLD READY',JSON.stringify(await p.evaluate(ids=>{const a=window.__chicago4d;return Object.fromEntries(Object.entries(ids).map(([k,id])=>{const x=a.humans.get(id);return [k,{actor:x?{id:x.id,personId:x.personId,instance:x.instance,position:x.root.position.toArray(),body:!!x.body,lod:x.lod,indoors:x.indoors}:null,home:a.days?.homeNow?.(id)}];}));},ids)));
 console.log('FINAL NATIVE CAPTURES BEGIN');
 const hashes=await p.evaluate(async()=>{const out={};for(const f of ['human-skin','human-variation','human-hair','human-spectacles','photo-face-pages','humans','visitor-person','person-settings','main']){const r=await fetch('./js/'+f+'.js');if(!r.ok)throw Error('module missing '+f);const bytes=await r.arrayBuffer();out[f]=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('');}return out;});
 const crypto=require('node:crypto');for(const [name,got]of Object.entries(hashes)){const want=crypto.createHash('sha256').update(fs.readFileSync('renderers/web/js/'+name+'.js')).digest('hex');if(got!==want)throw Error('Published module differs: '+name);}
 const active=JSON.parse(fs.readFileSync('assets/humans/web/photo_faces/historical/coverage.json')).people.filter(r=>r.active_cast).map(r=>r.person);
 const previousFile='work/historical-inapp/final-named-captures.json';
 const commitSeconds=Number(require('node:child_process').execFileSync('git',['show','-s','--format=%ct','HEAD'],{encoding:'utf8'}));
 const reusable=(fs.existsSync(previousFile)?JSON.parse(fs.readFileSync(previousFile)):[]).filter(row=>{
  if(row.status!=='captured'||!active.includes(row.id)||!row.file||!fs.existsSync(row.file)||fs.statSync(row.file).mtimeMs<commitSeconds*1000)return false;
  const meta=JSON.parse(fs.readFileSync(row.file+'.json'));
  if(['glessner_john_j','pa1904_grey_w_l'].includes(row.id)&&meta.naturalBlink==null)return false;
  return meta.personId===row.id&&(meta.photoId===row.id||row.identityBasis==='existing_skin'&&meta.photoId==null)&&String(meta.year)==='1904'&&meta.lod===1&&meta.nativeGazeSettledAtCamera&&meta.photoPages.residentPages+meta.photoPages.pendingPages<=1;
 });
 const missing=active.filter(id=>!reusable.some(r=>r.id===id));
 console.log('NATIVE CAPTURE RESUME',JSON.stringify({reused:reusable.length,missing}));
 if(missing.length)await require('./capture-historical-inapp-batch.cjs')({p,only:missing,includeStirling:true,report:'final-named-retries'});
 const retried=missing.length?JSON.parse(fs.readFileSync('work/historical-inapp/final-named-retries.json')):[];
 const fullNamed=active.map(id=>retried.find(r=>r.id===id)||reusable.find(r=>r.id===id));
 fs.writeFileSync(previousFile,JSON.stringify(fullNamed,null,2)+'\n');
 const named=fullNamed.map(r=>({id:r?.id,status:r?.status,label:r?.label}));
 const capture=require('./capture-stirling-frame.cjs');
 for(const key of ['dorothy','alice']){
  await p.evaluate(async id=>{
   const a=window.__chicago4d;a.setTravelMode('teleport');await a.findPerson(id);const x=a.humans.get(id);
   if(!x)throw Error('Missing daughter '+id);
   a.camera.position.set(x.root.position.x+5,x.root.position.y+1.6,x.root.position.z);a.camera.lookAt(x.root.position);a.camera.updateMatrixWorld();
   a.world.follow(a.camera.position);a.terrain.updateGroundReach(a.camera.position);a.humans.update(0,a.camera,a.walker.state,0);await x.setLod(1);
   for(let i=0;i<1600;i++){a.humans.update(.05,a.camera,a.walker.state,.05);a.days.update(.05);if(i>80&&!x.indoors&&!a.days.doorway(id))break;}
   if(x.indoors)throw Error('Daughter has not finished coming outside '+id);
   a.days.pause(a.days.people.find(q=>q.actor===x)?.id??x.id);x.setState('standing');
  },ids[key]);
  await capture({p,ids,key,frame:'whole',side:1});
 }
 const generic=await require('./capture-generic-inapp.cjs')({p});if(generic.length!==4||generic.some(x=>x.status!=='captured'))throw Error('Incomplete generic captures');
 fs.writeFileSync('work/historical-inapp/final-capture-progress.json',JSON.stringify({at:new Date().toISOString(),moduleHashes:hashes,named,generic,errors},null,2)+'\n');
 if(named.length!==28||named.some(x=>x.status!=='captured'))throw Error('Incomplete named captures '+JSON.stringify(named));
 if(errors.length)throw Error(errors.join('\n'));
 const reusedNativeCaptures=reusable.map(r=>({personId:r.id,file:r.file,sha256:crypto.createHash('sha256').update(fs.readFileSync(r.file)).digest('hex'),capturedAfterQualifiedCommit:true}));
 fs.writeFileSync('work/historical-inapp/final-native-capture-receipt.json',JSON.stringify({at:new Date().toISOString(),moduleHashes:hashes,named,generic,errors,reusedNativeCaptures,source:'Published app, standard native person assignment and materials; camera framed for review; no material injection',untimedPreparation:'Boot software draws held; optional shader warm-up and sliced pre-upload disabled. Every final frame uses the original native renderer and unchanged scene/materials. Source-bound stills may be retained across successive sessions of the identical qualified build.'},null,2)+'\n');
 console.log('PASS: final native app captures: 28 named people, four generic adults/children, zero page errors, served modules match source');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exit(1);});
