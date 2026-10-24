#!/usr/bin/env node
// Exact H3/base70b source preparation. UNRUN; full24/merge/deployment/HTTP receipts and image review still required.
// UNEXECUTED v2 preparation; final closed-browser error and actual mesh-visibility guards. Explicit future D/M/H and actual v2 selected-byte proof are mandatory.
// Uses normal hit-tested controls; reads existing telemetry only. No API camera/navigation setters.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';

const HERE=path.dirname(fileURLToPath(import.meta.url));
const ROOT='/workspace/chicago';
const DEV='https://chicago.polecat.live/4d/dev/';
const ENTRY=DEV+'1835/';
const UNBOUND_PREPARATION=false; // Actual H3/source binding exists; all future execution prerequisites still apply.
const TESTED_H='1b70cdbd85b18c124870d6274d2ffffd4ca5979b';
const TESTED_TREE='9fa9511eabff9a0e42da32410edf09a8e3608889';
const TESTED_APP='da9f71f6749ebf52e09ad51f673a9e4debbf4478';
const BINDING_SHA='949516de77917485ac808dafb9f39129ce3c8234eb0ecf215ff4f7d2625aaf25';
const HTTP_PASS='PASS: public DEV D and twelve selected representations verified; folded notes/UI yard remain separately unverified';
const HORSE_REL='walk/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb';
const HORSE_SHA='d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914';
const HORSE_ID='western_hotel_yard_standing_horse_01';
const TARGETS={
  'walk/transport/parked-brougham/brougham-near.glb':'chicago/4d/renderers/web/transport/parked-brougham/brougham-near.glb',
  'walk/transport/parked-brougham/brougham-mid.glb':'chicago/4d/renderers/web/transport/parked-brougham/brougham-mid.glb',
  'walk/transport/parked-brougham/brougham.json':'chicago/4d/renderers/web/transport/parked-brougham/brougham.json',
  'data/transport/parked/placements.json':'chicago/4d/data/transport/parked/placements.json',
  'data/transport/parked/standing-horses.json':'chicago/4d/data/transport/parked/standing-horses.json',
  'data/transport/parked/horse-sevket-sidecar.json':'chicago/4d/data/transport/parked/horse-sevket-sidecar.json',
  [HORSE_REL]:'chicago/4d/renderers/web/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb',
  'walk/js/standing-horses.js':'chicago/4d/renderers/web/js/standing-horses.js',
  'walk/js/standing-horse-planted-idle.js':'chicago/4d/renderers/web/js/standing-horse-planted-idle.js',
  'walk/js/parked-transport.js':'chicago/4d/renderers/web/js/parked-transport.js',
  'walk/css/walk.css':'chicago/4d/renderers/web/css/walk.css',
  'data/scenes/1835.json':'chicago/4d/data/scenes/1835.json'
};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const need=(v,m)=>{if(!v)throw Error(m);};
need(!UNBOUND_PREPARATION,'UNBOUND preparation: actual H3/source binding required before execution');
const canon=v=>JSON.stringify(v&&typeof v==='object'?Array.isArray(v)?v.map(x=>JSON.parse(canon(x))):Object.fromEntries(Object.keys(v).sort().map(k=>[k,JSON.parse(canon(v[k]))])):v);
const git=(...args)=>execFileSync('git',args,{cwd:ROOT,env:{...process.env,GIT_OPTIONAL_LOCKS:'0'},stdio:['ignore','pipe','pipe']});
const gitText=(...args)=>git(...args).toString().trim();
const cleanUrl=s=>{try{const u=new URL(s);u.search='';u.hash='';u.username='';u.password='';return u.href;}catch{return String(s);}};
const cleanText=s=>String(s).replace(/https?:\/\/[^\s<>"']+/g,u=>cleanUrl(u)).slice(0,3000);
const cli=process.argv.slice(2);
const opt=k=>{const i=cli.indexOf(k);need(i>=0&&cli[i+1]&&!cli[i+1].startsWith('--'),'Missing '+k);return cli[i+1];};
need(cli.includes('--execute-read-only-dev-yard'),'Preparation only. Root must explicitly authorize this future read-only DEV verification.');
const H=opt('--source-head'),M=opt('--merge-head'),D=opt('--deployed-head');
const receiptFile=path.resolve(opt('--http-receipt'));
const receiptSHA=opt('--http-receipt-sha256');
const OUTPUT=path.resolve(opt('--out'));
need([H,M,D].every(x=>/^[0-9a-f]{40}$/.test(x)),'Supply actual full H/M/D commit SHAs');
need(H===TESTED_H,'Another tested source needs a newly reviewed helper/binding');
need(/^[0-9a-f]{64}$/.test(receiptSHA),'Supply complete actual HTTP receipt SHA256');
need(OUTPUT.startsWith('/workspace/.cloud-setup/')&&!fs.existsSync(OUTPUT),'Use a NEW external output directory');
const bindingBytes=fs.readFileSync(path.join(HERE,'PREPARATION-BINDING.json'));
need(sha(bindingBytes)===BINDING_SHA,'Prepared source binding changed');
const binding=JSON.parse(bindingBytes);
need(binding.tested_source_head===H&&binding.tested_tree===TESTED_TREE&&binding.tested_app===TESTED_APP&&binding.accepted_base==='70bcc4366a455a15f1e54e3edfce50c046c0ddce'&&Array.isArray(binding.source_contract_files)&&binding.source_contract_files.length===17&&new Set(binding.source_contract_files.map(r=>r.path)).size===17,'Exact actual H3/70b metadata and seventeen distinct source-contract rows are required');
for(const head of [H,M,D])need(gitText('rev-parse',head+'^{commit}')===head,'Root must supply actual local commit objects before execution');
need(gitText('rev-parse',H+'^{tree}')===TESTED_TREE&&gitText('rev-parse',H+':chicago/4d')===TESTED_APP,'Tested H changed');
const sourceContracts=[];
for(const row of binding.source_contract_files){
  const h=git('show',H+':'+row.path),d=git('show',D+':'+row.path);
  need(sha(h)===row.sha256&&h.length===row.bytes&&d.equals(h),'UI/runtime/source contract changed: '+row.path);
  sourceContracts.push({...row,deployed_equals_tested:true});
}
const originalReceipt=fs.readFileSync(receiptFile);
need(sha(originalReceipt)===receiptSHA,'Actual selected-byte proof changed');
const proof=JSON.parse(originalReceipt);
need(proof.result===HTTP_PASS&&!proof.error,'A complete actual selected-byte PASS is required');
need(proof.tested_source_head===H&&proof.merge_head===M&&proof.deployed_head===D,'HTTP proof H/M/D pins differ');
need(proof.tested_tree===TESTED_TREE&&proof.tested_app===TESTED_APP&&proof.initial_M_app_exactly_H===true&&proof.initial_M_entire_tree_exactly_H===true&&proof.M_sole_parent_B===true&&proof.accepted_base==='70bcc4366a455a15f1e54e3edfce50c046c0ddce','Actual squash source identity proof missing');
need(/^[0-9a-f]{64}$/.test(proof.source_complete_proof_sha256||'')&&/^[0-9a-f]{64}$/.test(proof.normal_merge_receipt_sha256||''),'Missing complete-matrix or normal-merge provenance');
need(Array.isArray(proof.http_checks)&&proof.http_checks.length===14,'Require twelve asset responses and both build responses');
const receiptBodies=new Map(),receiptBuilds=[];
for(const row of proof.http_checks){
  need(row.http_status==='200'&&row.curl_returncode===0&&Number.isSafeInteger(row.bytes)&&/^[0-9a-f]{64}$/.test(row.sha256||''),'Incomplete HTTP response proof');
  const u=new URL(row.url);need(u.href===DEV+'build.json'||Object.keys(TARGETS).some(rel=>u.href===DEV+rel),'Unexpected target in selected-byte proof');
  need(typeof row.body_file==='string'&&path.basename(row.body_file)===row.body_file,'Body file must be the actual verifier basename');
  const bytes=fs.readFileSync(path.join(path.dirname(receiptFile),row.body_file));
  need(bytes.length===row.bytes&&sha(bytes)===row.sha256,'Retained HTTP response body changed: '+row.body_file);
  if(u.href===DEV+'build.json')receiptBuilds.push(bytes);
  else{const rel=u.href.slice(DEV.length);need(!receiptBodies.has(rel),'Duplicate selected target');receiptBodies.set(rel,bytes);}
}
need(receiptBuilds.length===2&&receiptBuilds[0].equals(receiptBuilds[1])&&receiptBodies.size===12,'Incomplete/changed selected HTTP proof');
for(const [rel,src]of Object.entries(TARGETS)){
  const bytes=receiptBodies.get(rel);need(bytes&&bytes.equals(git('show',H+':'+src))&&bytes.equals(git('show',M+':'+src))&&bytes.equals(git('show',D+':'+src)),'Selected served H/M/D source differs: '+rel);
}
const sourceScene=JSON.parse(receiptBodies.get('data/scenes/1835.json'));
const anchor=sourceScene.anchors.find(x=>x.id==='western_hotel_yard');
need(sourceScene.anchors.length===19&&anchor?.local_e===-124&&anchor.local_n===-292&&anchor.yaw_deg===221.19,'Reviewed yard anchor/inventory changed');
const groundDoc=JSON.parse(git('show',H+':chicago/4d/data/render/anchor_ground_reading.json'));
const groundRow=groundDoc.anchors.find(x=>x.id===anchor.id);
need(groundRow?.inside===true&&groundRow.dry===true&&groundRow.inside_a_roof===null&&groundRow.local_e===anchor.local_e&&groundRow.local_n===anchor.local_n,'Source anchor contract is not dry/outside roofs');
const horseManifest=JSON.parse(receiptBodies.get('data/transport/parked/standing-horses.json'));
const expectedHorse=horseManifest.scenes['1835'].find(x=>x.id===HORSE_ID);
const horseSpec=JSON.parse(receiptBodies.get('data/transport/parked/horse-sevket-sidecar.json'));
need(expectedHorse&&horseSpec.runtime_asset.sha256===HORSE_SHA&&sha(receiptBodies.get(HORSE_REL))===HORSE_SHA,'Reviewed horse selection differs');
const committedAt=gitText('show','-s','--format=%cI',D);
function verifyBuild(bytes){
  const b=JSON.parse(bytes);need(b.tier==='dev'&&b.ref==='refs/heads/dev'&&b.app==='chicago/4d'&&/^[0-9a-f]{7,40}$/.test(b.sha||'')&&D.startsWith(b.sha)&&b.committedAt===committedAt,'Public build does not identify supplied actual DEV D');return b;
}
verifyBuild(receiptBuilds[0]);need(canon(proof.build_before)===canon(proof.build_after)&&canon(proof.build_before)===canon(JSON.parse(receiptBuilds[0])),'HTTP proof build objects differ');
fs.mkdirSync(OUTPUT);
const started=Date.now();
const report={result:'RUNNING',scope:'Normal published DEV yard route, actual pose/selected horse telemetry and two real screenshots. This is not a new full renderer gate, photographic/native/gait approval or folded-news verification.',source_head:H,merge_head:M,deployed_head:D,tested_tree:TESTED_TREE,tested_app:TESTED_APP,http_receipt_sha256:receiptSHA,source_contracts:sourceContracts,preparation_binding_sha256:BINDING_SHA,helper_sha256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),source_anchor:anchor,source_ground_contract:groundRow,assertions:[],viewports:[],visual_review_required:true,visual_reviewed:false,photographic_approval:false,native_approval:false,gait_approval:false};
let browser=null,activePage=null,activeView=null,firstBuildBytes=null;
const pendingBodyTasks=new Set();
const save=()=>fs.writeFileSync(path.join(OUTPUT,'POST-DEV-YARD-NORMAL-UI.json'),JSON.stringify(report,null,2)+'\n');
const check=(name,ok,details=null)=>{report.assertions.push({name,result:ok?'PASS':'FAIL',details});save();need(ok,name);};
function fetchBuild(stem){
  const dest=path.join(OUTPUT,stem+'.body'),headers=path.join(OUTPUT,stem+'.headers');
  const cmd=['--silent','--show-error','--compressed','--proto','=https','--connect-timeout','15','--max-time','90','--header','Cache-Control: no-cache','--dump-header',headers,'--output',dest,'--write-out','%{http_code}',DEV+'build.json'];
  const status=execFileSync('curl',cmd,{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();need(status==='200','DEV build failed/redirected: '+status);const bytes=fs.readFileSync(dest);return {bytes,build:verifyBuild(bytes),status,sha256:sha(bytes)};
}
async function hitTest(page,selector){
  const p=await page.evaluate(async s=>{
    const el=document.querySelector(s);if(!el||el.disabled)throw Error('Missing/disabled control '+s);
    const nav=el.closest('#navigator');if(nav?.getAnimations)for(let i=0;i<60&&nav.getAnimations().some(a=>a.playState==='running');i++)await new Promise(r=>setTimeout(r,50));
    el.scrollIntoView({block:'center',inline:'center'});const b=el.getBoundingClientRect();const x=b.x+b.width/2,y=b.y+b.height/2,top=document.elementFromPoint(x,y);
    if(b.width<1||b.height<1||x<0||y<0||x>=innerWidth||y>=innerHeight||!top||!(top===el||el.contains(top)))throw Error('Control is not hit-testable: '+s+' covered by '+(top?.closest('[id]')?.id||top?.tagName||'nothing'));
    return {selector:s,x,y,width:b.width,height:b.height,tag:el.tagName,text:el.textContent?.trim().slice(0,120)};
  },selector);activeView.ui_actions.push({...p,kind:'hit_test'});return p;
}
async function click(page,selector,touch){const p=await hitTest(page,selector);if(touch)await page.touchscreen.tap(p.x,p.y);else await page.mouse.click(p.x,p.y);activeView.ui_actions.push({selector,kind:touch?'trusted_touch_tap':'trusted_mouse_click'});}
async function openNav(page,touch){
  if(await page.evaluate(()=>window.__chicago4d.navigator.level===0))await click(page,touch?'#nav-grip':'#nav-collapse',touch);
  await page.waitForFunction(()=>{const r=document.getElementById('navigator')?.getBoundingClientRect();return r&&(innerWidth>620?r.width>=380:r.height>=innerHeight*.4);},null,{timeout:90000,polling:200});
}
async function screenshot(page,name){const file=path.join(OUTPUT,name);await page.screenshot({path:file,timeout:180000});need(fs.statSync(file).size>10000,'Screenshot is unexpectedly empty');activeView.screenshots.push({path:name,bytes:fs.statSync(file).size,sha256:sha(fs.readFileSync(file))});}
function observeYard(){
  const a=window.__chicago4d;if(!a?.ready||!a.walker?.state||!a.camera||!a.terrain||!Array.isArray(a.footprints))throw Error('Required existing read-only yard telemetry unavailable');
  const s=a.walker.state,world=a.camera.getWorldPosition(a.camera.position.clone()),direction=a.camera.getWorldDirection(a.camera.position.clone());
  const cameraBearing=(Math.atan2(direction.x,-direction.z)*180/Math.PI+360)%360;
  const inPoly=([e,n],poly)=>{let inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const[ei,ni]=poly[i],[ej,nj]=poly[j];if((ni>n)!==(nj>n)&&e<(ej-ei)*(n-ni)/(nj-ni)+ei)inside=!inside;}return inside;};
  const hitRoofs=a.footprints.filter(f=>Array.isArray(f.pts)&&inPoly([s.e,s.n],f.pts)).map(f=>f.id);
  const instance=a.standingHorses?.instances?.[0];const samples=[],meshVisibility=[];let meshCount=0,insideFrustum=0,visibleFrustumSamples=0,visible=true;
  if(instance){for(let n=instance.group;n;n=n.parent)visible&&=n.visible;instance.root.traverse(node=>{
    if(!node.isMesh)return;meshCount++;const p=node.geometry?.attributes?.position;const scratch=node.position.clone();let nodeVisible=true;for(let n=node;n;n=n.parent)nodeVisible&&=n.visible;const mesh={name:node.name,skinned:node.isSkinnedMesh===true,ownVisible:node.visible,ancestorsVisible:nodeVisible,sampled:0,inFrustum:0};meshVisibility.push(mesh);
    if(!p||typeof node.getVertexPosition!=='function')throw Error('Existing mesh vertex reading unavailable');
    for(let i=0;i<p.count;i+=Math.max(1,Math.floor(p.count/48))){node.getVertexPosition(i,scratch);scratch.applyMatrix4(node.matrixWorld).project(a.camera);const point={x:scratch.x,y:scratch.y,z:scratch.z};samples.push(point);mesh.sampled++;if(Math.abs(point.x)<=1&&Math.abs(point.y)<=1&&point.z>-1&&point.z<1){insideFrustum++;mesh.inFrustum++;if(nodeVisible&&visible)visibleFrustumSamples++;}}
  });}
  return {ready:a.ready,error:a.error,problems:[...(a.problems||[])],scene:a.scene?.id,anchors:a.scene?.anchors,entry:location.href,base:document.baseURI,journey:document.documentElement.dataset.journey,welcome:a.welcome?.state,gateHidden:document.getElementById('gate')?.hidden,detail:a.detail,detailSetting:a.hud?.settings?.detail,travelMode:a.hud?.settings?.travelMode,navigator:{level:a.navigator?.level,app:a.navigator?.app},walker:{e:s.e,n:s.n,groundY:s.groundY,eyeY:s.eyeY,flying:s.flying,blocked:s.blocked,bearingDeg:a.walker.bearingDeg},camera:{world:world.toArray(),bearingDeg:cameraBearing,quaternion:a.camera.quaternion.toArray(),projection:a.camera.projectionMatrix.toArray()},ground:{height:a.terrain.surfaceHeight(s.e,s.n),water:a.terrain.isWater(s.e,s.n),roofIds:hitRoofs,footprints:a.footprints.length},render:{frame:a.renderer.info.render.frame,calls:a.renderer.info.render.calls,triangles:a.renderer.info.render.triangles},horse:instance?{row:instance.row,receipt:instance.receipt,idle:instance.idle?.status,groupVisible:visible&&instance.group.visible,groupPosition:instance.group.position.toArray(),supportQuaternion:instance.group.children[0]?.quaternion.toArray(),meshCount,meshVisibility,visibleFrustumSamples,allMeshesVisible:meshVisibility.length>0&&meshVisibility.every(m=>m.ownVisible&&m.ancestorsVisible),sampledSkinnedVertices:samples.length,insideFrustum,projectedSamples:samples,materials:(()=>{const v=[];instance.root.traverse(n=>{if(n.isMesh)v.push({name:n.material?.name,metalness:n.material?.metalness,visible:n.visible});});return v;})()}:null};
}
try{
  const before=fetchBuild('browser-build-before');firstBuildBytes=before.bytes;report.build_before=before.build;check('actual DEV D build before normal UI',true,{sha256:before.sha256});
  const require=createRequire(path.join(ROOT,'chicago/4d/tools/qa.mjs'));const{chromium}=require('playwright');
  const executable=process.env.PW_EXECUTABLE||process.env.PW_CHROMIUM||'/usr/bin/chromium';report.browser_executable=executable;
  browser=await chromium.launch({executablePath:executable,headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader']});
  for(const item of[{label:'mobile390x780',viewport:{width:390,height:780},touch:true},{label:'desktop1280x800',viewport:{width:1280,height:800},touch:false}]){
    const v={...item,result:'RUNNING',ui_actions:[],errors:[],aborted_requests:[],network:[],protected_browser_responses:[],pending_protected_body_reads:0,screenshots:[]};report.viewports.push(v);activeView=v;
    const context=await browser.newContext({viewport:item.viewport,hasTouch:item.touch,isMobile:false,deviceScaleFactor:item.touch?2:1});const page=await context.newPage();activePage=page;page.setDefaultTimeout(90000);const bodies=[];
    page.on('pageerror',e=>v.errors.push('pageerror: '+cleanText(e.message||e)));
    page.on('console',m=>{if(m.type()==='error'&&!m.text().startsWith('Failed to load resource'))v.errors.push('console: '+cleanText(m.text()));});
    page.on('requestfailed',r=>{const why=r.failure()?.errorText||'';const value={url:cleanUrl(r.url()),reason:cleanText(why)};if(/ERR_ABORTED/.test(why))v.aborted_requests.push(value);else v.errors.push('request failed '+JSON.stringify(value));});
    page.on('response',r=>{const url=cleanUrl(r.url());v.network.push({url,status:r.status()});if(r.status()>=400)v.errors.push('HTTP '+r.status()+' '+url);const rel=url.startsWith(DEV)?url.slice(DEV.length):null;if(rel&&Object.hasOwn(TARGETS,rel)){v.pending_protected_body_reads++;let task;task=(async()=>{const b=await r.body();v.protected_browser_responses.push({path:rel,status:r.status(),bytes:b.length,sha256:sha(b)});})().catch(e=>v.errors.push('selected body read '+rel+': '+cleanText(e.message))).finally(()=>{v.pending_protected_body_reads--;pendingBodyTasks.delete(task);});pendingBodyTasks.add(task);bodies.push(task);}});
    const response=await page.goto(ENTRY,{waitUntil:'domcontentloaded'});check(item.label+': real year door HTTP200',response?.status()===200);
    await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000,polling:1000});
    await page.waitForFunction(()=>document.documentElement.dataset.journey==='landed',null,{timeout:90000,polling:200});
    const banner=await page.evaluate(()=>{const e=document.getElementById('__dev'),b=e?.getBoundingClientRect();return {text:e?.textContent,visible:!!b&&b.width>0&&b.height>0,stamp:document.getElementById('gate-build')?.textContent,robots:document.querySelector('meta[name="robots"]')?.content,entry:location.href,base:document.baseURI};});
    v.banner=banner;check(item.label+': actual DEV banner/stamp and normal entry',banner.visible&&banner.text.includes('DEV PREVIEW')&&banner.text.includes('dev@'+before.build.sha)&&banner.stamp.includes('DEV PREVIEW')&&banner.entry===ENTRY&&banner.base.startsWith(DEV+'walk/')&&/noindex/.test(banner.robots||''),banner);
    await click(page,'#home-roam',item.touch);await page.waitForFunction(()=>window.__chicago4d?.welcome?.state==='world'&&document.getElementById('gate')?.hidden,null,{timeout:90000,polling:200});
    v.initialDetail=await page.evaluate(()=>window.__chicago4d.detail);
    check(item.label+': fresh normal Go-to travel choice is instant',await page.evaluate(()=>window.__chicago4d.hud.settings.travelMode==='instantly'));
    if(v.initialDetail==='light'){
      await openNav(page,item.touch);await click(page,'#nav-tab-settings',item.touch);
      await page.waitForFunction(()=>{const p=document.querySelector('[data-panel="settings"]');return window.__chicago4d.navigator.app==='settings'&&p&&!p.hidden&&p.closest('.nav-screen:not([hidden])');},null,{timeout:90000,polling:200});
      await hitTest(page,'#s-detail');await page.selectOption('#s-detail','balanced');v.ui_actions.push({selector:'#s-detail',kind:'normal_select_input_change',value:'balanced'});
      await page.waitForFunction(()=>window.__chicago4d.detail==='balanced'&&document.getElementById('s-detail')?.value==='balanced',null,{timeout:180000,polling:500});
    }
    await openNav(page,item.touch);await click(page,'#nav-tab-home',item.touch);await page.waitForFunction(()=>window.__chicago4d.navigator.app==='home',null,{timeout:90000,polling:200});
    await click(page,'#nav-home .nav-choice[data-segment="goto"]',item.touch);await page.waitForFunction(()=>window.__chicago4d.navigator.app==='jaunts'&&document.getElementById('welcome-search')?.getClientRects().length>0,null,{timeout:90000,polling:200});
    await click(page,'#welcome-search',item.touch);await page.fill('#welcome-search','Western Hotel yard');v.ui_actions.push({selector:'#welcome-search',kind:'normal_input',value:'Western Hotel yard'});
    const target='#welcome-results .welcome-destination[data-kind="anchor"][data-id="western_hotel_yard"]';
    await page.waitForSelector(target,{state:'visible',timeout:90000});v.selectedRow=await page.locator(target).textContent();await click(page,target,item.touch);
    await page.waitForFunction(()=>{const a=window.__chicago4d,s=a?.walker?.state;return s&&Math.hypot(s.e+124,s.n+292)<.02;},null,{timeout:90000,polling:200});
    if(await page.evaluate(()=>window.__chicago4d.navigator.level>0))await click(page,'#nav-close',item.touch);
    await page.waitForFunction(()=>window.__chicago4d.standingHorses?.instances?.length===1,null,{timeout:180000,polling:500});
    await page.evaluate(async()=>{await window.__chicago4d.standingHorses.ready;});
    const first=await page.evaluate(observeYard);v.arrival=first;
    const angleDiff=(a,b)=>Math.abs(((a-b+540)%360)-180);
    check(item.label+': actual walker and camera arrive at authored E/N/yaw',Math.hypot(first.walker.e-anchor.local_e,first.walker.n-anchor.local_n)<.02&&angleDiff(first.walker.bearingDeg,anchor.yaw_deg)<.05&&Math.abs(first.camera.world[0]-anchor.local_e)<.02&&Math.abs(-first.camera.world[2]-anchor.local_n)<.02&&angleDiff(first.camera.bearingDeg,anchor.yaw_deg)<.05&&!first.walker.flying,first);
    check(item.label+': actual dry ground and no runtime roof footprint',first.ground.water===false&&first.ground.height>0&&first.ground.roofIds.length===0&&first.ground.footprints>0,{runtime:first.ground,source:groundRow});
    check(item.label+': runtime scene contains exact nineteen authored anchors',first.scene==='1835'&&canon(first.anchors)===canon(sourceScene.anchors));
    check(item.label+': actual horse-enabled detail tier and placement/support',first.horse&&['balanced','full'].includes(first.detail)&&first.detail===first.detailSetting&&Math.abs(first.horse.groupPosition[0]-expectedHorse.at_local_enu_m[0])<1e-6&&Math.abs(-first.horse.groupPosition[2]-expectedHorse.at_local_enu_m[1])<1e-6&&Math.abs(first.horse.groupPosition[1]-first.horse.receipt.root_y_m)<1e-6&&first.horse.supportQuaternion?.every((q,i)=>Math.abs(q-expectedHorse.support_quaternion_xyzw[i])<1e-10),{detail:first.detail,setting:first.detailSetting,placement:first.horse?.groupPosition,support:first.horse?.supportQuaternion});
    check(item.label+': selected standing instance and organic material/one planted clip',first.horse&&canon(first.horse.row)===canon(expectedHorse)&&first.horse.groupVisible&&first.horse.receipt.material_variant==='organic_dielectric_v1'&&first.horse.receipt.mixer_count===1&&first.horse.receipt.original_six_autoplay===false&&first.horse.receipt.idle_clip===expectedHorse.animation.clip&&first.horse.idle?.clip===expectedHorse.animation.clip&&first.horse.idle.mixer_count===1&&first.horse.materials.every(m=>m.metalness===0),first.horse);
    check(item.label+': actual horse skin has projected vertices in the live view',first.horse.meshCount>0&&first.horse.sampledSkinnedVertices>0&&first.horse.insideFrustum>0&&first.horse.allMeshesVisible&&first.horse.visibleFrustumSamples>0,{meshCount:first.horse.meshCount,samples:first.horse.sampledSkinnedVertices,inFrustum:first.horse.insideFrustum,visibleFrustumSamples:first.horse.visibleFrustumSamples,meshVisibility:first.horse.meshVisibility,limitation:'Frustum/visibility telemetry does not prove every horse pixel is unoccluded; real screenshot requires root visual review.'});
    await page.waitForFunction(frame=>window.__chicago4d.renderer.info.render.frame>frame,first.render.frame,{timeout:90000,polling:200});
    await screenshot(page,item.label+'-actual-DEV-Western-Hotel-yard.png');
    await Promise.all(bodies);v.finalPose=await page.evaluate(observeYard);
    const horseResponse=v.protected_browser_responses.find(x=>x.path===HORSE_REL&&x.status===200&&x.bytes===3784176&&x.sha256===HORSE_SHA);
    check(item.label+': actual browser fetched the selected d454 horse bytes',!!horseResponse,v.protected_browser_responses);
    for(const resource of v.protected_browser_responses)check(item.label+': observed protected browser bytes '+resource.path,resource.status===200&&sha(receiptBodies.get(resource.path))===resource.sha256&&receiptBodies.get(resource.path).length===resource.bytes);
    check(item.label+': pose retained and actual draw completed for yard screenshot',Math.hypot(v.finalPose.walker.e-anchor.local_e,v.finalPose.walker.n-anchor.local_n)<.02&&angleDiff(v.finalPose.camera.bearingDeg,anchor.yaw_deg)<.05&&v.finalPose.render.frame>first.render.frame&&v.finalPose.render.calls>0&&v.screenshots.length===1,{final:v.finalPose.render,screenshot:v.screenshots[0]});
    check(item.label+': zero page/console/HTTP/non-aborted request/loader errors',v.errors.length===0&&v.finalPose.error===null&&v.finalPose.problems.length===0,{errors:v.errors,loader:v.finalPose.problems,aborted:v.aborted_requests});
    await context.close();v.context_closed=true;await Promise.all(bodies);
    check(item.label+': no errors or unfinished selected-body reads after context close',v.errors.length===0&&v.pending_protected_body_reads===0,{errors:v.errors,pending:v.pending_protected_body_reads});
    v.result='PASS: normal UI, pose, selected horse and real screenshot captured; visual review pending';
    activePage=null;activeView=null;save();
  }
  check('both required viewports completed',report.viewports.length===2&&report.viewports.every(v=>v.result.startsWith('PASS:')&&v.context_closed));
  report.result='PASS: both normal-UI DEV yard observations and screenshots complete; root visual review still required';
}catch(error){report.result='FAIL: inspect actual yard evidence';report.error=cleanText(error.stack||error);if(activeView){activeView.result='FAIL';if(activePage)await screenshot(activePage,activeView.label+'-FAILURE.png').catch(e=>{activeView.failure_screenshot_error=cleanText(e.message);});}process.exitCode=1;}
finally{
  if(browser){try{await browser.close();report.browser_closed=true;}catch(e){report.browser_closed=false;report.cleanup_error=cleanText(e.message);report.result='FAIL: browser cleanup failed';process.exitCode=1;}}
  try{const after=fetchBuild('browser-build-after');report.build_after=after.build;check('actual DEV D build unchanged after all browser observations',!!firstBuildBytes&&after.bytes.equals(firstBuildBytes),{sha256:after.sha256});}catch(e){report.result='FAIL: DEV build changed/unavailable';report.build_after_error=cleanText(e.message);process.exitCode=1;}
  // The browser is closed before the final verdict. Drain all tracked body callbacks,
  // including work delivered while a context or the browser was closing.
  while(pendingBodyTasks.size)await Promise.all([...pendingBodyTasks]);
  report.pending_protected_body_reads_final=pendingBodyTasks.size;
  try{check('final closed-browser verdict has both successful viewports and zero late errors or pending body work',report.browser_closed===true&&report.viewports.length===2&&pendingBodyTasks.size===0&&report.viewports.every(v=>v.context_closed===true&&v.result.startsWith('PASS:')&&v.errors.length===0&&v.pending_protected_body_reads===0),{browser_closed:report.browser_closed,pending_tasks:pendingBodyTasks.size,viewports:report.viewports.map(v=>({label:v.label,result:v.result,context_closed:v.context_closed,errors:v.errors,pending:v.pending_protected_body_reads}))});}catch(e){report.final_guard_error=cleanText(e.message);report.result='FAIL: final closed-browser error/cleanup guard';process.exitCode=1;}
  if(sha(fs.readFileSync(receiptFile))!==receiptSHA){report.result='FAIL: source HTTP proof drift';process.exitCode=1;}
  report.seconds=(Date.now()-started)/1000;save();const files=[];for(const name of fs.readdirSync(OUTPUT).sort()){const p=path.join(OUTPUT,name);if(fs.statSync(p).isFile()){const b=fs.readFileSync(p);files.push({path:name,bytes:b.length,sha256:sha(b)});}}
  fs.writeFileSync(path.join(OUTPUT,'OUTPUT-MANIFEST.json'),JSON.stringify({files},null,2)+'\n');console.log(JSON.stringify({result:report.result,out:OUTPUT,seconds:report.seconds}));
}
