// Outside-app launch adapter. Uses unchanged approved native observer and Playwright defaults.
// Browser launch occurs only when root explicitly releases the heavy slot.
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require('/workspace/.cloud-setup/npm/node_modules/playwright');
const [url,viewport,out]=process.argv.slice(2);
if(!url||!['desktop','mobile'].includes(viewport)||!out)throw Error('usage: node run-native-railway-lifecycle.cjs URL desktop|mobile NEW_OUTSIDE_OUTPUT');
const address=new URL(url);
if(address.protocol!=='http:'||address.hostname!=='127.0.0.1'||address.pathname!=='/1904/'||address.search||address.hash||address.username||address.password)throw Error('Use clean actual local published /1904/ URL without query/hash/credentials');
if(fs.existsSync(out))throw Error('Fresh outside-app output directory required');
if(!path.resolve(out).startsWith('/workspace/.cloud-setup/logs/transport-recovery/'))throw Error('Output must stay in persistent recovery packet');
(async()=>{
 let browser,context,rc=1;const started=Date.now();
 try{
  browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined});
  context=await browser.newContext(viewport==='desktop'?{viewport:{width:1280,height:800},deviceScaleFactor:1,isMobile:false,hasTouch:false}:{viewport:{width:390,height:780},deviceScaleFactor:3,isMobile:true,hasTouch:true});
  const page=await context.newPage(),bootErrors=[],bootConsoleErrors=[];
  page.on('pageerror',e=>bootErrors.push(e.message));
  page.on('console',e=>{if(e.type()==='error')bootConsoleErrors.push(e.text());});
  await page.goto(address.href,{waitUntil:'load'});
  await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:420000});
  if(bootErrors.length||bootConsoleErrors.length)throw Error(JSON.stringify({bootErrors,bootConsoleErrors}));
  console.log(JSON.stringify({stage:'native-boot',viewport,actual:await page.evaluate(()=>({year:window.__chicago4d.year,detail:window.__chicago4d.detail,pixelRatio:window.__chicago4d.renderer.getPixelRatio(),welcome:window.__chicago4d.welcome.state}))}));
  const {observeNativeRailwayLifecycle}=await import(pathToFileURL(path.join(__dirname,'observe-native-railway-lifecycle-v4-settled.mjs')).href);
  const result=await observeNativeRailwayLifecycle(page,path.resolve(out));
  if(bootErrors.length||bootConsoleErrors.length)throw Error(JSON.stringify({bootErrors,bootConsoleErrors}));
  console.log(JSON.stringify({status:'Native lifecycle checks returned; inspect saved frames; full smoke still pending',viewport,seconds:(Date.now()-started)/1000,rows:result.rows.length}));rc=0;
 }catch(error){console.error(error.stack||String(error));}
 finally{
  const closeErrors=[];
  if(context)try{await context.close();}catch(error){closeErrors.push({stage:'context.close',error:error.stack||String(error)});rc=1;}
  if(browser)try{await browser.close();}catch(error){closeErrors.push({stage:'browser.close',error:error.stack||String(error)});rc=1;}
  if(closeErrors.length)console.error(JSON.stringify({closeErrors}));
  process.exitCode=rc;
 }
})();
