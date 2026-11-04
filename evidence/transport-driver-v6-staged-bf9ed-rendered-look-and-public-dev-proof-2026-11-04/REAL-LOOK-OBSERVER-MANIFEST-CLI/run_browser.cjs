const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const [app,out,configFile]=process.argv.slice(2);
if(process.argv[2]==='--help'){console.log('Usage: node run_browser.cjs APP OUT CONFIG\nROOT wrapper only. Both viewports1280x800/390x780; each viewport complete original120s deadline; four cases per viewport (1835/1904 xLOD0/3); outer600s. Actual PNG pairs, no town/photo claim.');process.exit(0);}
assert(app&&out&&configFile);fs.mkdirSync(out,{recursive:false});const config=JSON.parse(fs.readFileSync(configFile));
const report={passed:false,scope:'Actual native controlled driver rendered-look fixture; no full-town/trusted interaction/walkup/gait/photo acceptance',runs:[]};
const save=()=>fs.writeFileSync(path.join(out,'REPORT.json'),JSON.stringify(report,null,2)+'\n');let server,browser;
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.glb':'model/gltf-binary','.wasm':'application/wasm','.png':'image/png','.jpg':'image/jpeg','.ktx2':'image/ktx2'};
const cap=(promise,ms,label)=>{let timer;return Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' deadline exceeded')),ms);})]).finally(()=>clearTimeout(timer));};
async function main(){let pw;try{pw=require('playwright');}catch{pw=require(path.join(process.env.NODE_PATH,'playwright'));}
 server=http.createServer((req,res)=>{let f;const u=new URL(req.url,'http://fixture');if(u.pathname==='/__private/config.json'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify(config));return;}
 const privateName={'/__private/fixture.html':'fixture.html','/__private/fixture.mjs':'fixture.mjs'}[u.pathname];
 if(privateName)f=path.join(__dirname,privateName);else{f=path.resolve(app,'.'+decodeURIComponent(u.pathname));if(!f.startsWith(path.resolve(app)+path.sep)){res.writeHead(403).end();return;}}
 fs.readFile(f,(e,b)=>{if(e){report.missing??=[];report.missing.push(u.pathname);res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(b);});});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));browser=await pw.chromium.launch({executablePath:config.browser,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 for(const viewport of[{width:1280,height:800},{width:390,height:780}]){
  const started=Date.now(),deadline=started+120000;
  for(const scene of['1835','1904'])for(const lod of[0,3]){
   const row={scene,lod,viewport,passed:false};report.runs.push(row);save();const page=await browser.newPage({viewport});const errors=[];page.on('pageerror',e=>errors.push(e.message));
   const bounded=(p,label)=>cap(p,Math.max(1,deadline-Date.now()),'120s per-viewport '+label);
   try{await bounded(page.goto(`http://127.0.0.1:${server.address().port}/__private/fixture.html?scene=${scene}&lod=${lod}`),'load');
    await bounded(page.waitForFunction(()=>window.lookFixture?.ready||window.lookFixture?.error,null,{timeout:Math.max(1,deadline-Date.now())}),'ready');
    row.before=await bounded(page.evaluate(()=>window.lookFixture),'reading');assert(!row.before.error,row.before.error);
    const stem=`${scene}-lod${lod}-${viewport.width}`;
    row.before_png=stem+'-before.png';await bounded(page.screenshot({path:path.join(out,row.before_png),timeout:Math.min(30000,Math.max(1,deadline-Date.now()))}),'before PNG');
    row.advance=await bounded(page.evaluate(()=>window.advanceLook()),'actual visual advance');assert(row.advance.passed);
    row.after_png=stem+'-after.png';await bounded(page.screenshot({path:path.join(out,row.after_png),timeout:Math.min(30000,Math.max(1,deadline-Date.now()))}),'after PNG');
    row.actual=await bounded(page.evaluate(()=>window.finishLook()),'native controls');assert(row.actual.passed);assert.deepEqual(errors,[]);
    row.cleanup=await bounded(page.evaluate(()=>window.lookCleanup()),'asset cleanup');assert(row.cleanup.passed);assert.deepEqual(row.cleanup.remaining_human_assets,[]);row.passed=true;
   }finally{row.page_errors=errors;await page.close();row.viewport_elapsed_seconds=(Date.now()-started)/1000;save();}
  }
 }
 assert.equal(report.runs.length,8);assert(report.runs.every(r=>r.passed));assert.deepEqual(report.missing??[],[]);report.passed=true;
}
main().catch(e=>{report.error=String(e.stack??e);process.exitCode=1;}).finally(async()=>{await browser?.close();if(server?.listening)await new Promise(r=>server.close(r));report.browser_closed=true;report.server_closed=true;save();console.log(JSON.stringify({passed:report.passed,runs:report.runs.length,error:report.error}));});
