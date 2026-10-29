// Explicit neutral RAW source study. Never loads the application or replaces a production route.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),http=require('node:http'),os=require('node:os'),assert=require('node:assert/strict');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const [repoArg,outArg]=process.argv.slice(2);
assert.equal(process.argv.length,4,'node run-source-study.cjs EXISTING_H_WORKER FRESH_OUTSIDE_OUTPUT');
const prep=__dirname,repo=path.resolve(repoArg),out=path.resolve(outArg),manifestPath=path.join(prep,'VIEW-MANIFEST.json');
const manifest=JSON.parse(fs.readFileSync(manifestPath));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.ok(out!==repo&&!out.startsWith(repo+'/')&&out!==prep&&!out.startsWith(prep+'/'),'Output outside app/preparation');
assert.ok(!fs.existsSync(out),'Fresh output required');
const vendor=path.join(repo,'chicago/4d/renderers/web/vendor/three-0.185.1');
const study=manifest.study_directory;
assert.ok(out!==study&&!out.startsWith(study+'/'),'Immutable prototype directory is never an output');
const scratch=os.tmpdir();assert.ok(process.env.TMPDIR&&path.isAbsolute(scratch)&&scratch.length<=35&&!scratch.startsWith(repo+'/'),'Explicit short owned TMPDIR outside app required');
const scratchStat=fs.lstatSync(scratch);assert.ok(scratchStat.isDirectory()&&!scratchStat.isSymbolicLink()&&scratchStat.uid===process.getuid()&&fs.readdirSync(scratch).length===0,'Fresh empty owned browser TMPDIR required');
function resolved(pin){
  const base=pin.base==='prep'?prep:pin.base==='vendor'?vendor:pin.base==='study'?study:repo;
  const file=path.resolve(base,pin.path);assert.ok(file.startsWith(base+'/'),'Pinned file containment');
  const stat=fs.lstatSync(file);assert.ok(stat.isFile()&&!stat.isSymbolicLink(),'Ordinary pinned file');
  const raw=fs.readFileSync(file);assert.equal(raw.length,pin.bytes,pin.path);assert.equal(sha(raw),pin.sha256,pin.path);return raw;
}
function verify(){return manifest.files.map(pin=>({base:pin.base,path:pin.path,sha256:sha(resolved(pin))}));}
const before=verify();fs.mkdirSync(out);const save=(name,x)=>fs.writeFileSync(path.join(out,name),JSON.stringify(x,null,2)+'\n');
save('BEFORE.json',{scope:manifest.scope,manifest_sha256:sha(fs.readFileSync(manifestPath)),pins:before});
const routes=new Map();
for(const pin of manifest.files)if(pin.url){assert.ok(!routes.has(pin.url),'Unique study route');routes.set(pin.url,pin);}
routes.set('/',routes.get('/index.html'));
const responses=[],errors=[],warnings=[],rows=[];let server,browser,context;
const config=Buffer.from(JSON.stringify(manifest.browser_config));
const types={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.glb':'model/gltf-binary'};
(async()=>{try{
  server=http.createServer((req,res)=>{
    const url=new URL(req.url,'http://study');
    if(url.pathname==='/config.json'){
      responses.push({path:url.pathname,bytes:config.length,sha256:sha(config),status:200});res.writeHead(200,{'content-type':'application/json'});res.end(config);return;
    }
    const pin=routes.get(url.pathname);
    if(!pin){errors.push({kind:'unlisted-study-HTTP-request',path:url.pathname});res.writeHead(404);res.end('Unlisted source-study resource');return;}
    try{const raw=resolved(pin);responses.push({path:url.pathname,status:200,bytes:raw.length,sha256:sha(raw)});res.writeHead(200,{'content-type':types[path.extname(pin.path)]||'application/octet-stream','content-length':raw.length,'cache-control':'no-store'});res.end(raw);}
    catch(e){errors.push({kind:'pinned-resource',message:String(e)});res.writeHead(500);res.end('Pinned study resource failure');}
  });await new Promise(r=>server.listen(0,'127.0.0.1',r));
  browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
  context=await browser.newContext({viewport:{width:1024,height:1060},deviceScaleFactor:1,isMobile:false,hasTouch:false});
  const page=await context.newPage();page.setDefaultTimeout(120000);
  page.on('pageerror',e=>errors.push({kind:'pageerror',message:String(e)}));
  page.on('console',m=>{if(m.type()==='error')errors.push({kind:'console',message:m.text()});else if(m.type()==='warning')warnings.push(m.text());});
  page.on('requestfailed',r=>errors.push({kind:'requestfailed',url:r.url(),failure:r.failure()}));
  await page.goto('http://127.0.0.1:'+server.address().port+'/index.html',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.sourceEyeStudy?.ready===true,null,{timeout:180000});
  save('ACTUAL-LOADED-SOURCE.json',await page.evaluate(()=>({scope:window.sourceEyeStudy.scope,summaries:window.sourceEyeStudy.summaries})));
  for(const view of ['head-profile','head-oblique','eye-profile','eye-oblique']){
    const pair=[];
    for(const label of ['parent','candidate']){
      const row=await page.evaluate(({label,view})=>window.sourceEyeStudy.render(label,view),{label,view});
      assert.equal(row.sourceSHA256,manifest.browser_config.assets[label].sha256);
      assert.equal(row.glError,0);assert.equal(row.contextLost,false);
      assert.equal(row.rendererDPR,1);assert.deepEqual(row.drawingBuffer,[1024,1024]);
      assert.ok(row.renderInfo.triangles>0,'Actual whole-source scene rendered');
      const file=`RAW-SOURCE-STUDY-${view}-${label}.png`;
      await page.locator('canvas').screenshot({path:path.join(out,file)});
      const png=fs.readFileSync(path.join(out,file));
      assert.equal(png.readUInt32BE(16),1024);assert.equal(png.readUInt32BE(20),1024);
      row.png={path:file,bytes:png.length,sha256:sha(png)};rows.push(row);pair.push(row);
      save('PROGRESS.json',{scope:manifest.scope,rows,errors,warnings,responses});
    }
    for(const key of ['camera','target','distance','exposure','toneMapping','outputColorSpace','rendererDPR','drawingBuffer'])assert.deepEqual(pair[0][key],pair[1][key],`Matched source-study ${view}/${key}`);
    for(const key of ['calls','triangles','lines','points'])assert.equal(pair[0].renderInfo[key],pair[1].renderInfo[key],`Matched actual draw counter ${view}/${key}`);
  }
  assert.equal(rows.length,8);assert.equal(errors.length,0,'All real study errors remain fatal');
  for(const pin of manifest.files.filter(x=>x.url))assert.ok(responses.some(x=>x.path===pin.url&&x.sha256===pin.sha256),'Actual pinned HTTP source/vendor/module '+pin.url);
}catch(e){errors.push({kind:'study-fatal',message:String(e),stack:e.stack});}
finally{
  if(context)try{await context.close();}catch(e){errors.push({kind:'context-close',message:String(e)});}
  if(browser)try{await browser.close();}catch(e){errors.push({kind:'browser-close',message:String(e)});}
  if(server)await new Promise(r=>server.close(r));
  try{const after=verify();assert.deepEqual(after,before);save('AFTER.json',{pins:after,source_study_files_unchanged:true});}catch(e){errors.push({kind:'after-source-check',message:String(e)});}
  const passed=rows.length===8&&errors.length===0;
  save('RESULT.json',{state:passed?'MATCHED_RAW_SOURCE_OBSERVATION_COMPLETE_UNQUALIFIED':'NONPASS_RAW_SOURCE_STUDY',scope:manifest.scope,rows,errors,warnings,responses,personal_image_review:'REQUIRED; no visible improvement asserted by this result',native_world_organic_variant_used:false,published_gate_or_physical_qualification:false,adopted:false});process.exitCode=passed?0:1;
}})().catch(e=>{console.error(e);process.exitCode=1;});
