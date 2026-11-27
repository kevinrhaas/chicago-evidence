const {chromium}=require('playwright'),fs=require('node:fs'),crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 assert.equal(cp.spawnSync('git',['diff','--quiet']).status,0);
 const tree=cp.execFileSync('git',['write-tree'],{encoding:'utf8'}).trim();
 const parent=cp.execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
 const ids={'william-grey':'pa1904_grey_w_l','sarah-grey':'pa1904_grey_mrs_w_l'};
 const protectedFiles={};
 for(const id of Object.values(ids))for(const path of [
  `data/humans/variation/fits/${id}.json`,`data/humans/variation/skins/${id}.json`,
  `assets/humans/web/likeness/${id}_skin.jpg`,`assets/humans/web/likeness/${id}_front.jpg`,
 ]){
  const current=fs.readFileSync(path),baseline=cp.execFileSync('git',['show','b085e2e5b3:'+path.replace(/^/,'chicago/4d/')],{maxBuffer:8*1024*1024});
  assert.equal(sha(current),sha(baseline),'original Grey mapping retained: '+path);protectedFiles[path]=sha(current);
 }
 const b=await chromium.launch({headless:true,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const p=await b.newPage({viewport:{width:1024,height:768}}),errors=[];
  p.on('pageerror',e=>{errors.push(e.message);console.log('PAGEERROR',e.message);});p.setDefaultTimeout(120000);
  await p.addInitScript(()=>{
   localStorage.setItem('chicago4d.settings',JSON.stringify({detail:'balanced'}));
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
  const moduleHashes=await p.evaluate(async()=>{
   const out={};for(const name of ['human-skin','human-variation','human-hair','human-spectacles','photo-face-pages','humans','visitor-person','person-settings','main']){
    const r=await fetch('./js/'+name+'.js');if(!r.ok)throw Error('Missing renderer '+name);
    out[name]=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',await r.arrayBuffer()))).map(x=>x.toString(16).padStart(2,'0')).join('');
   }return out;
  });
  for(const[name,hash]of Object.entries(moduleHashes))assert.equal(hash,sha(fs.readFileSync('renderers/web/js/'+name+'.js')));
  const capture=require('./capture-stirling-frame.cjs'),out='work/grey-original-mappings-native',records=[];fs.mkdirSync(out,{recursive:true});
  for(const[key,id]of Object.entries(ids)){
   const mapping=await p.evaluate(async id=>{
    const skin=await import('./js/human-skin.js'),a=window.__chicago4d;
    a.setTravelMode('teleport');await a.findPerson(id);const x=a.humans.get(id);if(!x)throw Error('Missing original Grey actor '+id);
    a.camera.position.set(x.root.position.x+5,x.root.position.y+1.6,x.root.position.z);a.camera.lookAt(x.root.position);a.camera.updateMatrixWorld();
    a.world.follow(a.camera.position);a.terrain.updateGroundReach(a.camera.position);a.humans.update(0,a.camera,a.walker.state,0);await x.setLod(1);
    for(let i=0;i<1600;i++){a.humans.update(.05,a.camera,a.walker.state,.05);a.days.update(.05);if(i>80&&!x.indoors&&!a.days.doorway(id))break;}
    if(x.indoors)throw Error('Grey actor did not come outside '+id);
    a.days.pause(a.days.people.find(q=>q.actor===x)?.id??x.id);x.setState('standing');
    const like=x.body.scene.userData.chiLikenessSkin;
    if(!like?.url?.endsWith('/'+id+'_skin.jpg')||!like.front?.url?.endsWith('/'+id+'_front.jpg'))throw Error('Wrong original Grey photo mapping '+id);
    if(x.body.scene.userData.chiPhotoFace)throw Error('Generic face overwrote the Grey mapping '+id);
    const files={};for(const url of [like.url,like.front.url]){
     const r=await fetch(url);if(!r.ok)throw Error('Missing original skin '+url);
     files[url.split('/').at(-1)]=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',await r.arrayBuffer()))).map(x=>x.toString(16).padStart(2,'0')).join('');
    }
    await skin.likenessSheetsReady();return {personId:id,skinUrl:like.url,frontUrl:like.front.url,servedFiles:files,genericPhotoOverride:false};
   },id);
   for(const[name,hash]of Object.entries(mapping.servedFiles))assert.equal(hash,sha(fs.readFileSync('assets/humans/web/likeness/'+name)));
   for(const[frame,side]of [['whole',1],['face',0]]){
    const file=await capture({p,ids,key,frame,side}),name=file.split('/').at(-1),meta=JSON.parse(fs.readFileSync(file+'.json'));
    assert.equal(meta.personId,id);assert.equal(meta.photoId,null);fs.copyFileSync(file,out+'/'+name);
    fs.writeFileSync(out+'/'+name+'.json',JSON.stringify({...meta,originalMapping:mapping,candidateTree:tree,moduleHashes},null,2)+'\n');
    records.push({personId:id,file:name,frame,sha256:sha(fs.readFileSync(file)),originalMapping:mapping});
   }
  }
  assert.equal(errors.length,0,errors.join('\n'));assert.equal(cp.execFileSync('git',['write-tree'],{encoding:'utf8'}).trim(),tree);assert.equal(cp.spawnSync('git',['diff','--quiet']).status,0);
  fs.writeFileSync(out+'/receipt.json',JSON.stringify({candidateTree:tree,parentAtCapture:parent,at:new Date().toISOString(),renderer:'Native published app; original fitted heads and full photo skins; camera framed for review; no material injection',preparation:'Only untimed onscreen boot draws held; native offscreen and all final draws preserved. Not GPU timing evidence.',viewport:[1024,768],hardware:'Chromium SwiftShader',moduleHashes,protectedFiles,records,errors},null,2)+'\n');
  console.log('PASS: both original Grey mappings are applied in the native app; four current face/full-figure captures, original fit/skin hashes preserved, zero page errors');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exit(1);});
