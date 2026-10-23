const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const{chromium}=require('./node_modules/playwright');const ROOT=__dirname,OUT=path.join(ROOT,'actual'),port=Number(process.argv[2]);
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');const need=(v,m)=>{if(!v)throw Error(m)};
need(fs.existsSync(path.join(ROOT,'RUN-INTENT.json')),'Released owner required');fs.mkdirSync(OUT);let browser=null,activePage=null;
const result={scope:'Eight normal matched indexed-near V17/V18 views: desktop/mobile detail/fullquarter, fixed catalogue camera and original lighting, depth-valid near100/exact originalxy. No photographic acceptance',started:new Date().toISOString(),pass:false,rows:[],attemptedRows:[],errors:[],disposal:[],browserClosed:false,expectedImages:8,inputs_manifest_sha256:hash(path.join(ROOT,'INPUTS.json'))};
const save=()=>fs.writeFileSync(path.join(OUT,'receipt.json'),JSON.stringify(result,null,2));const watchdog=setTimeout(()=>{result.error='165second deadline';save();browser?.close().finally(()=>process.exit(124))},165000);
const expected={"v17":{"hash":"ec2bfc0da49b570429dbcd8db39250aa6f1bbf55587570f0dafad9a42afc4ee5","triangles":33502,"bytes":1249944},"v18":{"hash":"bce1ecc757a7175cb193b1263fc8dbcdf1ce76a263916d3cff5e41dc4a835938","triangles":33374,"bytes":1244652}};
(async()=>{try{
 // SOURCE-ONLY scheduling variant: a real default launch failed before any page.
 // This binding changes launch scheduling only; no FPS/performance equivalence is claimed.
 const released=JSON.parse(fs.readFileSync(path.join(ROOT,'ROOT-RELEASE.json'),'utf8'));
 const fallback=released.launcher_resource_fallback;
 need(released.current_root_resource_variant_release===true&&released.execution_authorized===true&&fallback?.kind==='renderer1-raster1-swift1','Current ROOT-reviewed resource-variant execution required');
 const inputs=JSON.parse(fs.readFileSync(path.join(ROOT,'INPUTS.json'),'utf8'));
 const pinFor=p=>inputs.resource_fallback_inputs.find(row=>row.absolute_path===p);
 const failed=pinFor(fallback.default_launch_failure_receipt);
 need(failed&&hash(failed.absolute_path)===failed.sha256,'Exact original default-launch failure must be pinned');
 const failure=JSON.parse(fs.readFileSync(failed.absolute_path,'utf8'));
 need(failure.pass===false&&failure.rows.length===0&&String(failure.error).includes('pthread_create'),'Observed before-page default thread-exhaustion failure required');
 const iniPath=path.resolve(fallback.swiftshader_ini??''),iniPin=pinFor(iniPath);
 need(iniPath.startsWith('/tmp/')&&path.basename(iniPath)==='SwiftShader.ini'&&fs.realpathSync(iniPath)===iniPath&&!fs.lstatSync(iniPath).isSymbolicLink()&&!fs.lstatSync(path.dirname(iniPath)).isSymbolicLink(),'Private real /tmp SwiftShader.ini required');
 need((fs.statSync(path.dirname(iniPath)).mode&0o077)===0&&(fs.statSync(iniPath).mode&0o077)===0,'Private INI directory/file permissions required');
 need(iniPin&&iniPin.bytes===26&&iniPin.sha256==='228340162de0f5f5ac4ca228a89f6256cc8cc9cdaee81b618ebceec2f1b2dba8'&&hash(iniPath)===iniPin.sha256,'Exact private SwiftShader ThreadCount1 input required');
 process.chdir(path.dirname(iniPath)); // All fixture/caller/output paths above are already absolute.
 result.launcherResourceFallback={kind:fallback.kind,default_launch_failure_receipt:failed.absolute_path,default_launch_failure_sha256:failed.sha256,swiftshader_ini:iniPath,swiftshader_ini_sha256:iniPin.sha256,browserChildCwdRequested:process.cwd(),configuration_effect_observed:false,performance_equivalence_claimed:false};save();
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--renderer-process-limit=1','--num-raster-threads=1'],timeout:15000});const bindings=new Map();
 // Observation only: read this Node child's own descendant tree, never PID1/other agents.
 try{const seen=new Set(),todo=[process.pid],rows=[];while(todo.length&&seen.size<128){const pid=todo.shift();if(seen.has(pid))continue;seen.add(pid);try{const status=fs.readFileSync(`/proc/${pid}/status`,'utf8'),threads=Number(status.match(/^Threads:\s+(\d+)/m)?.[1]??0);rows.push({pid,cwd:fs.readlinkSync(`/proc/${pid}/cwd`),threads});for(const tid of fs.readdirSync(`/proc/${pid}/task`)){try{for(const child of fs.readFileSync(`/proc/${pid}/task/${tid}/children`,'utf8').trim().split(/\s+/).filter(Boolean))todo.push(Number(child))}catch{}}}catch{}}result.launcherResourceFallback.observedOwnProcessInventory=rows;save()}catch(error){result.launcherResourceFallback.observationError=String(error);save()}
 for(const[viewport,width,height]of[['desktop',1280,800],['mobile',390,780]])for(const version of['v17','v18']){
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});activePage=page;
 const note=(kind,message)=>{result.errors.push({viewport,version,kind,message});save()};page.on('pageerror',e=>note('page',e.message));page.on('console',m=>{if(m.type()==='error')note('console',m.text())});page.on('requestfailed',r=>note('request',r.url()+': '+r.failure()?.errorText));page.on('response',r=>{if(r.status()>=400)note('http',r.status()+' '+r.url())});
 await page.route('**/*',r=>{const u=new URL(r.request().url());return ['data:','blob:'].includes(u.protocol)||(u.protocol==='http:'&&u.hostname==='127.0.0.1'&&u.port===String(port))?r.continue():r.abort('blockedbyclient')});
 await page.goto(`http://127.0.0.1:${port}/transport/${version}/`,{waitUntil:'load',timeout:15000});await page.waitForFunction(()=>window.broughamReady&&window.setSourceComparison&&document.querySelector('#reference img').complete,null,{timeout:15000});
 const imageDimensions=await page.evaluate(()=>{const im=document.querySelector('#reference img');return[im.naturalWidth,im.naturalHeight]});need(JSON.stringify(imageDimensions)==='[1556,1145]','Actual source JPEG decode dimensions');
 const modelHash=await page.evaluate(()=>comparisonInputHash()),sourceHash=await page.evaluate(()=>sourceInputHash());need(modelHash===expected[version].hash,'Exact frozen native indexed-near hash');need(sourceHash==='b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe','Actual valid plate hash');
 for(const view of['detail','fullquarter']){
 const row=await page.evaluate(view=>setSourceComparison(view),view);result.attemptedRows.push({viewport,version,...row});save();const key=viewport+':'+view,binding=bindings.get(key);
 if(binding){for(const field of['camera','originalNear005Projection','lighting','crop','dom','fullBounds'])need(JSON.stringify(binding[field])===JSON.stringify(row[field]),'Matched '+field+' mismatch');}else bindings.set(key,row);
 need(row.nearClip===100&&row.camera.far===1000&&row.nondepthProjectionExact&&row.depthBits>0&&row.defaultFramebuffer&&row.clipGuard.fullModelAndOriginalFloorInside,'Depth-valid source projection');
 need(row.poleVisible&&row.hiddenModelNodes.length===0&&row.sourceTriangles===expected[version].triangles&&row.sourceBytes===expected[version].bytes,'Frozen geometry/all-visible guard');need(row.glError===0&&result.errors.length===0,'Actual runtime errors');need(row.lighting.shadowsEnabled&&row.lighting.sun.normalBias===0&&row.lighting.sun.bias===-.0002&&row.lighting.exposure===1.3,'Original lighting');
 if(view==='fullquarter')need(row.fullFraming.entireFullBoundsInside&&row.fullFraming.ndcMin.slice(0,2).every(x=>x>=-.98)&&row.fullFraming.ndcMax.slice(0,2).every(x=>x<=.98),'Full carriage including pole outside frame');
 for(const d of[row.dom.canvas,row.dom.reference])need(d.width>100&&d.height>100&&d.left>=0&&d.top>=row.dom.header.bottom&&d.right<=width+1&&d.bottom<=height+1,'Normal framing guard');
 await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const png=`${viewport}-${version}-source-${view}-near100.png`;await page.screenshot({path:path.join(OUT,png),timeout:10000});result.rows.push({viewport,version,view,png,normalBrowserScreenshot:true,image_sha256:hash(path.join(OUT,png)),loaded_model_sha256:modelHash,source_sha256:sourceHash,sameCameraLightCropBoundsAsV17:version==='v18',...row});save();
 }
 try{result.disposal.push({viewport,version,...await page.evaluate(()=>disposeComparison())})}catch(error){result.disposal.push({viewport,version,error:String(error),resourceCleanup:await page.evaluate(()=>window.broughamCleanupReceipt||null).catch(()=>null)});save();throw error}save();await page.close();activePage=null;
 }
 need(result.rows.length===8&&result.disposal.length===4&&result.errors.length===0,'Eight-frame completeness');result.pass=true;
 }catch(e){result.error=String(e.stack||e);process.exitCode=1}finally{clearTimeout(watchdog);if(activePage&&!activePage.isClosed()){try{result.disposal.push({viewport:'failure-finally',...await activePage.evaluate(()=>disposeComparison())})}catch(error){result.disposal.push({viewport:'failure-finally',error:String(error)})}save()}if(browser){await browser.close();result.browserClosed=true}result.finished=new Date().toISOString();save()}if(!result.pass)throw Error(result.error);console.log('PASS8 matched V17/V18 native indexed-near normal images; owned browser closed; photographic acceptance OPEN.');})().catch(e=>{console.error(e);process.exitCode=1});
