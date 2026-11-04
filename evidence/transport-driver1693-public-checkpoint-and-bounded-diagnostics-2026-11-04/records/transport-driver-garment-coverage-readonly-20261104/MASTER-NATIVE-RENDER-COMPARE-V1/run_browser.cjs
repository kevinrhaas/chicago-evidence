const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
if(process.argv[2]==='--help'){console.log('Usage: node run_browser.cjs APP OUT CONFIG\nROOT wrapper only; MASTER parent/prototype; 1280x800 and390x780, complete120s per viewport, original600s outer. Two named people x2native poses x2variants. Original texturedPNG and transient material-IDPNG.');process.exit(0);}
const [app,out,configFile]=process.argv.slice(2);assert(app&&out&&configFile);fs.mkdirSync(out,{recursive:false});const config=JSON.parse(fs.readFileSync(configFile));
assert.equal(config.approved,true);assert.equal(config.policy,'ROOT_AUTHORIZED_MASTER_ONLY_NATIVE_GARMENT_RENDER_COMPARISON');
const report={passed:false,scope:'MASTER ONLY comparison, actual native HumanActor; no production WEB, vehicle/hitch/world, whole garment fit or photographic acceptance',runs:[]};
const save=()=>fs.writeFileSync(path.join(out,'REPORT.json'),JSON.stringify(report,null,2)+'\n');let server,browser;
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.ktx2':'image/ktx2'};
const cap=(promise,ms,label)=>{let timer;return Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' deadline exceeded')),ms);})]).finally(()=>clearTimeout(timer));};
const png=(name,url)=>{assert(url.startsWith('data:image/png;base64,'));fs.writeFileSync(path.join(out,name),Buffer.from(url.split(',')[1],'base64'));};
async function main(){let pw;try{pw=require('playwright');}catch{pw=require(path.join(process.env.NODE_PATH,'playwright'));}
 const masterFiles=new Map();for(const s of config.cases)for(const variant of['parent','prototype'])masterFiles.set(`/__master/${variant}/humans/web/${s.asset}.lod3.glb`,s[variant].path);
 server=http.createServer((req,res)=>{let f;const u=new URL(req.url,'http://fixture');if(u.pathname==='/__private/config.json'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify(config));return;}
 const privateName={'/__private/fixture.html':'fixture.html','/__private/fixture.mjs':'fixture.mjs'}[u.pathname];
 if(privateName)f=path.join(__dirname,privateName);else if(masterFiles.has(u.pathname))f=masterFiles.get(u.pathname);else{f=path.resolve(app,'.'+decodeURIComponent(u.pathname));if(!f.startsWith(path.resolve(app)+path.sep)){res.writeHead(403).end();return;}}
 fs.readFile(f,(e,b)=>{if(e){report.missing??=[];report.missing.push(u.pathname);res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(b);});});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));browser=await pw.chromium.launch({executablePath:config.browser,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 for(const viewport of[{width:1280,height:800},{width:390,height:780}]){
  const started=Date.now(),deadline=started+120000;
  for(const s of config.cases){const row={scene:s.scene,asset:s.asset,person_id:s.person_id,viewport,passed:false,pairs:[]};report.runs.push(row);save();const page=await browser.newPage({viewport});const errors=[];page.on('pageerror',e=>errors.push(e.message));const bounded=(p,label)=>cap(p,Math.max(1,deadline-Date.now()),'120s complete per-viewport '+label);
   try{await bounded(page.goto(`http://127.0.0.1:${server.address().port}/__private/fixture.html?scene=${s.scene}`),'load');await bounded(page.waitForFunction(()=>window.masterCompare?.ready||window.masterCompare?.error,null,{timeout:Math.max(1,deadline-Date.now())}),'ready');row.initial=await bounded(page.evaluate(()=>window.masterCompare),'initial proof');assert(!row.initial.error,row.initial.error);
    for(const time of config.poses_seconds){const pair={time,textured:[]},stem=`MASTER-${s.scene}-${viewport.width}x${viewport.height}-t${String(time).replace('.','p')}`;row.pairs.push(pair);
     for(const variant of['parent','prototype']){const reading=await bounded(page.evaluate(({variant,time})=>window.selectTextured(variant,time),{variant,time}),'native pose original materials');assert.deepEqual(reading.camera,row.initial.camera);const name=`${stem}-${variant}-original-textured.png`;await bounded(page.screenshot({path:path.join(out,name),timeout:Math.min(30000,Math.max(1,deadline-Date.now()))}),'textured PNG');pair.textured.push({variant,png:name,...reading});}
     const ids=await bounded(page.evaluate(t=>window.comparePose(t),time),'native invariants and full-canvas ID census');pair.comparison=ids.row;for(const variant of['parent','prototype']){const name=`${stem}-${variant}-material-ID.png`;png(name,ids[variant+'_id_png']);pair[variant+'_material_ID_png']=name;}
     // Re-render using restored original material references after the transient ID pass.
     pair.original_materials_restored_render=await bounded(page.evaluate(t=>window.selectTextured('prototype',t),time),'original material restoration');
    }
    row.cleanup=await bounded(page.evaluate(()=>window.masterCleanup()),'native asset cleanup');assert(row.cleanup.passed);assert.deepEqual(row.cleanup.assets_remaining,[]);assert.deepEqual(errors,[]);row.passed=true;
   }finally{row.page_errors=errors;await page.close();row.viewport_elapsed_seconds=(Date.now()-started)/1000;save();}
  }
 }
 assert.equal(report.runs.length,4);assert(report.runs.every(r=>r.passed&&r.pairs.length===2));assert.deepEqual(report.missing??[],[]);report.passed=true;
}
main().catch(e=>{report.error=String(e.stack??e);process.exitCode=1;}).finally(async()=>{await browser?.close();if(server?.listening)await new Promise(r=>server.close(r));report.browser_closed=true;report.server_closed=true;save();console.log(JSON.stringify({passed:report.passed,runs:report.runs.length,error:report.error}));});
