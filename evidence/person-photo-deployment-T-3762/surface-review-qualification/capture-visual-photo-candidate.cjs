const {chromium}=require('playwright'),fs=require('node:fs'),crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 assert.equal(cp.spawnSync('git',['diff','--quiet']).status,0,'stage and freeze every source change before capture');
 const tree=cp.execFileSync('git',['write-tree'],{encoding:'utf8'}).trim();
 const base=cp.execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
 const b=await chromium.launch({headless:true,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const p=await b.newPage({viewport:{width:1024,height:768}}),errors=[];
  p.on('pageerror',e=>{errors.push(e.message);console.log('PAGEERROR',e.message);});
  p.setDefaultTimeout(120000);
  await p.addInitScript(()=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail:'balanced'})));
  await p.addInitScript(()=>{
   let app;Object.defineProperty(window,'__chicago4d',{configurable:true,get:()=>app,set(value){
    app=value;let renderer=value.renderer;
    Object.defineProperty(value,'renderer',{configurable:true,enumerable:true,get:()=>renderer,set(next){
     renderer=next;if(!next)return;window.__appRender=next.render.bind(next);
     next.render=(scene,camera)=>next.getRenderTarget()?window.__appRender(scene,camera):camera?.updateMatrixWorld?.();
    }});if(renderer)value.renderer=renderer;
   }});
  });
  await p.goto('http://127.0.0.1:3005/4d/walk/?year=1904&warm=0&firstupload=0',{waitUntil:'domcontentloaded',timeout:180000});
  await p.waitForFunction(()=>window.__chicago4d?.ready,null,{timeout:240000});
  await p.waitForFunction(()=>window.__chicago4d.welcome.state==='welcome',null,{timeout:120000});
  await p.evaluate(()=>document.getElementById('home-roam').click());
  await p.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:120000});
  await p.evaluate(()=>{const a=window.__chicago4d;a.renderer.setAnimationLoop(null);a.navigator.dock();document.exitPointerLock?.();});
  const hashes=await p.evaluate(async()=>{
   const out={};for(const name of ['human-skin','human-variation','human-hair','human-spectacles','photo-face-pages','humans','visitor-person','person-settings','main']){
    const r=await fetch('./js/'+name+'.js');if(!r.ok)throw Error('Missing renderer '+name);
    out[name]=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',await r.arrayBuffer()))).map(x=>x.toString(16).padStart(2,'0')).join('');
   }return out;
  });
  for(const [name,hash]of Object.entries(hashes))assert.equal(hash,digest(fs.readFileSync('renderers/web/js/'+name+'.js')),'served renderer '+name);
  const libraries=await p.evaluate(async()=>{const out={};for(const name of ['pilot','children','historical'])out[name]=await(await fetch('../data/humans/web/photo_faces/'+name+'/review.json')).json();return out;});
  for(const [name,lib]of Object.entries(libraries))assert.deepEqual(lib,JSON.parse(fs.readFileSync('assets/humans/web/photo_faces/'+name+'/review.json')),'served catalog '+name);
  console.log('NATIVE CANDIDATE READY',JSON.stringify({tree,modules:hashes,libraries:Object.fromEntries(Object.entries(libraries).map(([k,l])=>[k,l.faces.length]))}));
  const prepare=async id=>p.evaluate(async id=>{
   const a=window.__chicago4d;a.setTravelMode('teleport');await a.findPerson(id);const x=a.humans.get(id);
   if(!x)throw Error('Missing native actor '+id);
   a.camera.position.set(x.root.position.x+5,x.root.position.y+1.6,x.root.position.z);a.camera.lookAt(x.root.position);a.camera.updateMatrixWorld();
   a.world.follow(a.camera.position);a.terrain.updateGroundReach(a.camera.position);a.humans.update(0,a.camera,a.walker.state,0);await x.setLod(1);
   for(let i=0;i<1600;i++){a.humans.update(.05,a.camera,a.walker.state,.05);a.days.update(.05);if(i>80&&!x.indoors&&!a.days.doorway(id))break;}
   if(x.indoors)throw Error('Native actor did not finish coming outside '+id);
   a.days.pause(a.days.people.find(q=>q.actor===x)?.id??x.id);x.setState('standing');
  },id);
  const capture=require('./capture-stirling-frame.cjs'),files=[];
  const daughters={dorothy:'pa1904_stirling_william_r_c1900_dorothy_sterling',alice:'pa1904_stirling_william_r_c1900_alice_m_sterling'};
  for(const [key,id]of Object.entries(daughters)){
   await prepare(id);
   files.push(await capture({p,ids:{[key]:id},key,frame:'whole',side:1}));
   files.push(await capture({p,ids:{[key]:id},key,frame:'face'}));
  }
  const generic=await require('./capture-generic-inapp.cjs')({p});
  assert.equal(generic.length,4);assert(generic.every(r=>r.status==='captured'));
  for(const r of generic){files.push(r.file);if(r.whole)files.push(r.whole);}
  for(const r of JSON.parse(fs.readFileSync('work/historical-inapp/oblique-captures.json')))files.push(r.file);
  const william='pa1904_grey_w_l';await prepare(william);files.push(await capture({p,ids:{william},key:'william',frame:'face'}));
  assert.equal(errors.length,0,errors.join('\n'));
  assert.equal(cp.spawnSync('git',['diff','--quiet']).status,0,'source changed during capture');
  assert.equal(cp.execFileSync('git',['write-tree'],{encoding:'utf8'}).trim(),tree);
  const out='work/visual-photo-native';fs.mkdirSync(out,{recursive:true});const records=[];
  const context={candidateTree:tree,parentAtCapture:base,moduleHashes:hashes,catalogHashes:Object.fromEntries(Object.entries(libraries).map(([k,l])=>[k,digest(JSON.stringify(l))])),
   renderer:'Published native 1904 town; default assignments, materials and lighting; camera framed for review; no material injection',
   preparation:'Only untimed onscreen boot draws held; every offscreen pass and final frame uses original renderer. Optional warm-up/pre-upload disabled.',viewport:[1024,768],hardware:'Chromium SwiftShader; not hardware FPS evidence'};
  for(const file of files){
   const name=file.split('/').at(-1),meta=JSON.parse(fs.readFileSync(file+'.json'));assert(!meta.diagnosticOnly);
   if(meta.photoId){
    const found=Object.entries(libraries).find(([,lib])=>lib.faces.some(f=>f.id===meta.photoId));assert(found,'assigned photo belongs to the served catalogs');
    const [library,lib]=found,face=lib.faces.find(f=>f.id===meta.photoId);
    assert(meta.photoPages.page.endsWith('/'+library+'/page_'+String(face.page).padStart(2,'0')+'_face_full.jpg'),'the assigned face has its own admitted nearby page');
    assert.equal(meta.photoPages.residentPages,1);assert.equal(meta.photoPages.pendingPages,0);
   }
   fs.copyFileSync(file,out+'/'+name);fs.writeFileSync(out+'/'+name+'.json',JSON.stringify({...meta,captureContext:context},null,2)+'\n');
   records.push({personId:meta.personId,photoId:meta.photoId,frame:meta.frame,sideOffset:meta.sideOffset,file:name,sha256:digest(fs.readFileSync(file))});
  }
  fs.writeFileSync(out+'/receipt.json',JSON.stringify({...context,records,errors},null,2)+'\n');
  console.log('PASS: '+records.length+' native candidate captures, exact frozen tree and served renderer/catalogs, zero page errors');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exit(1);});
