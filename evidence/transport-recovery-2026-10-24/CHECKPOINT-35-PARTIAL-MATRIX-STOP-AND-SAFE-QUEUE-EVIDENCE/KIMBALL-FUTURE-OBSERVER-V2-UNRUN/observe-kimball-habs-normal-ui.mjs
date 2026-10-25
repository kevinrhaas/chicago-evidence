#!/usr/bin/env node
// UNRUN. Requires a future actual committed, base-integrated and normally published source.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import http from 'node:http';
import {execFileSync} from 'node:child_process';
import {pathToFileURL,fileURLToPath} from 'node:url';
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const argv=process.argv.slice(2),opt=k=>{const i=argv.indexOf(k);need(i>=0&&argv[i+1]&&!argv[i+1].startsWith('--'),'Missing '+k);return argv[i+1];};
need(argv.includes('--execute-authorized-normal-ui'),'Static preparation only; future root authorization and all actual source receipts required.');
const ROOT=fs.realpathSync(opt('--repo')),H=opt('--head'),B=opt('--base'),OUT=path.resolve(opt('--out'));
const bindingFile=path.resolve(opt('--source-binding')),bindingSHA=opt('--source-binding-sha256');
const PRIMARY_H=opt('--accepted-primary-source-head'),PRIMARY_M=opt('--accepted-primary-merge-head');
const prefix=path.resolve(opt('--publisher-prefix')),MIRROR=fs.realpathSync(opt('--mirror'));
const playwrightModule=path.resolve(opt('--playwright-module'));
need([H,B,PRIMARY_H,PRIMARY_M].every(x=>/^[0-9a-f]{40}$/.test(x)),'Supply actual complete future HEAD, accepted BASE, qualified primary source and normal DEV merge.');
need(H!=='74718ae5165db49c232227c7677228ca44b3aaa4','Historical H747 has not taken the future accepted primary DEV intake; it cannot execute this observer.');
need(OUT.startsWith('/workspace/.cloud-setup/')&&!fs.existsSync(OUT)&&!OUT.startsWith(ROOT+'/'),'Use a new external output directory.');
need(MIRROR===path.join(ROOT,'site/4d'),'Use this own repository normal published mirror.');
need(ROOT!=='/workspace/chicago','This owned PR1278 observer must never run in the frozen primary checkout.');
const git=(...args)=>execFileSync('git',args,{cwd:ROOT,env:{...process.env,GIT_OPTIONAL_LOCKS:'0'},stdio:['ignore','pipe','pipe']});
const gt=(...args)=>git(...args).toString().trim();
const rawBinding=fs.readFileSync(bindingFile);need(sha(rawBinding)===bindingSHA,'Source binding bytes changed.');
const binding=JSON.parse(rawBinding);
need(binding.schema==='pr1278-normal-ui-actual-source-v1'&&binding.head===H&&binding.base===B,'Actual binding schema/head/base required.');
need(binding.primary_integration?.source_head===PRIMARY_H&&binding.primary_integration?.merge_head===PRIMARY_M,'Require actual accepted primary source/DEV-merge binding.');
function boundArtifact(ref){need(ref&&typeof ref.path==='string'&&/^[0-9a-f]{64}$/.test(ref.sha256||''),'Actual artifact path/hash missing');const raw=fs.readFileSync(path.resolve(ref.path));need(sha(raw)===ref.sha256,'Actual merge artifact bytes changed');return JSON.parse(raw);}
function verifyPrimaryReceipt(){
 const raw=fs.readFileSync(path.resolve(binding.primary_integration.normal_merge_receipt_file));need(sha(raw)===binding.primary_integration.normal_merge_receipt_sha256,'Actual primary normal-merge receipt changed.');const r=JSON.parse(raw);
 need(r.schema==='chicago-pr1279-sha-pinned-squash-70b-h3-v1'&&r.state==='actual_service_receipts'&&r.repository==='kevinrhaas/chicago'&&r.pr===1279&&r.tested_head===PRIMARY_H&&r.merge_commit===PRIMARY_M,'Canonical primary normal-merge schema/repository/PR/H/M/state mismatch');
 need(/^[0-9a-f]{40}$/.test(r.accepted_base||'')&&r.initial_M_APP_exactly_H===true&&r.initial_M_entire_tree_exactly_H===true&&r.M_sole_parent_B===true&&r.H_ancestor_M_required===false,'Actual squash identity/parent proof required');
 const a=r.artifacts;need(a&&a.merge_request&&a.merge_result&&a.postmerge_pr,'Actual normal service request/result/PR artifact references required');
 const request=boundArtifact(a.merge_request),result=boundArtifact(a.merge_result),post=boundArtifact(a.postmerge_pr),commit=boundArtifact(r.actual_postmerge_commit);
 need(request.sha===PRIMARY_H&&request.merge_method==='squash'&&result.merged===true&&result.sha===PRIMARY_M,'Actual SHA-pinned normal squash request/result mismatch');
 need(post.number===1279&&post.state==='closed'&&post.merged===true&&typeof post.merged_at==='string'&&post.merged_at.length>0&&post.merge_commit_sha===PRIMARY_M&&post.head?.sha===PRIMARY_H&&post.base?.repo?.full_name==='kevinrhaas/chicago','Actual postmerge PR does not bind accepted Chicago1279 H/M');
 need(commit.sha===PRIMARY_M&&commit.tree?.sha===r.actual_M_tree&&commit.parents?.length===1&&commit.parents[0].sha===r.accepted_base,'Actual service merge commit parent/tree mismatch');
 need(gt('rev-parse',PRIMARY_M+'^{tree}')===r.actual_M_tree&&gt('rev-parse',PRIMARY_H+'^{tree}')===r.actual_M_tree&&gt('rev-parse',PRIMARY_M+':chicago/4d')===r.actual_M_app_subtree,'Actual native H/M trees differ from canonical receipt');
 return {schema:r.schema,repository:r.repository,pr:r.pr,state:r.state,tested_head:r.tested_head,merge_commit:r.merge_commit,accepted_base:r.accepted_base};
}
const primaryReceiptSummary=verifyPrimaryReceipt();
need(binding.publisher?.head===H&&binding.publisher.prefix===prefix,'Publisher must be bound to this actual committed head.');
const pubRaw=fs.readFileSync(prefix+'.result.json'),cleanupRaw=fs.readFileSync(prefix+'.cleanup.json');
need(sha(pubRaw)===binding.publisher.result_sha256&&sha(cleanupRaw)===binding.publisher.cleanup_sha256,'Publisher receipts differ.');
const pub=JSON.parse(pubRaw),cleanup=JSON.parse(cleanupRaw);
need(pub.returncode===0&&!pub.timed_out&&cleanup.cleanup_complete===true&&cleanup.remaining_owned_children.length===0,'Normal publisher must actually close0/cleanup0.');
need(pub.cwd===path.join(ROOT,'chicago/4d')&&Array.isArray(pub.command)&&pub.command.some(x=>x==='tools/publish.sh'||x.endsWith('/tools/publish.sh')),'Require this clone normal publish.sh command receipt.');
const index=path.resolve(ROOT,gt('rev-parse','--git-path','index'));
const PH='chicago/4d/data/reference_views/kimball_house_1801_prairie/';
const expected={
 [PH+'habs_1965_01_southwest.json']:'f46ae16fefb6fcc9978291adbe19363723815faa4c42f16927fd46e51084a5bc',
 [PH+'habs_1965_01_southwest.match.json']:'e8b96539b8ca5b58f2d25022806ebec31007d645677974789803f40073026f02',
 'chicago/prairie_1904_v1/research/public/kimball-habs-photo-01.jpg':'be2d21b595907011c7fe29c3e3765f754486cee1acdd321fed62f683ae6e0cbf'
};
const cleanURL=s=>{try{const u=new URL(s);u.search='';u.hash='';u.username='';u.password='';return u.href;}catch{return String(s);}};
const cleanText=s=>String(s).replace(/https?:\/\/[^\s<>"']+/g,cleanURL).slice(0,2000);
function fileRows(root){const rows=[];function walk(rel){for(const e of fs.readdirSync(path.join(root,rel),{withFileTypes:true})){const r=path.posix.join(rel,e.name);need(!e.isSymbolicLink(),'No symlink in mirror');if(e.isDirectory())walk(r);else if(e.isFile())rows.push(r);}}walk('');return rows.sort();}
function verifyRows(root,rows,paths){need(Array.isArray(rows)&&rows.length>0,'Complete hash journal required.');need(JSON.stringify(rows.map(x=>x.path).sort())===JSON.stringify(paths.slice().sort()),'Hash journal must cover every actual path.');for(const r of rows){need(!path.isAbsolute(r.path)&&!r.path.split('/').includes('..'),'Unsafe journal path');const f=path.join(root,r.path);need(!fs.lstatSync(f).isSymbolicLink(),'No source symlinks');const b=fs.readFileSync(f);need(b.length===r.bytes&&sha(b)===r.sha256,'Source/mirror byte changed: '+r.path);}}
function guard(){
 need(sha(fs.readFileSync(index))===binding.index_sha256,'Physical index changed.');
 need(gt('rev-parse','HEAD')===H&&gt('rev-parse','HEAD^{tree}')===binding.tree&&gt('rev-parse','HEAD:chicago/4d')===binding.app_subtree,'Actual current source head/tree/APP differs.');
 git('merge-base','--is-ancestor',B,H);git('merge-base','--is-ancestor',PRIMARY_M,B);
 need(gt('rev-parse',PRIMARY_M+':chicago/4d')===gt('rev-parse',PRIMARY_H+':chicago/4d'),'Primary merge APP must preserve its qualified source before later base intake.');
 verifyPrimaryReceipt();
 const entries=git('ls-files','--stage','-z').toString().split('\0').filter(Boolean).map(s=>{const [meta,p]=s.split('\t'),[mode,oid,stage]=meta.split(' ');need(stage==='0','Unmerged index entry');return {mode,oid,path:p};});
 const headEntries=git('ls-tree','-r','-z',H).toString().split('\0').filter(Boolean).map(s=>{const [meta,p]=s.split('\t'),[mode,type,oid]=meta.split(' ');need(type==='blob','Only normal tracked files are supported');return {mode,oid,path:p};});
 const sorted=v=>v.sort((a,b)=>a.path<b.path?-1:a.path>b.path?1:0);need(JSON.stringify(sorted(entries))===JSON.stringify(sorted(headEntries)),'Index is not exactly actual committed HEAD.');
 const paths=entries.map(x=>x.path);verifyRows(ROOT,binding.source_files,paths);
 for(const e of entries){const b=fs.readFileSync(path.join(ROOT,e.path));const oid=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');need(oid===e.oid,'Working source differs from actual committed blob: '+e.path);}
verifyRows(MIRROR,binding.mirror_files,fileRows(MIRROR));
 for(const [p,s]of Object.entries(expected))need(sha(fs.readFileSync(path.join(ROOT,p)))===s&&sha(git('show',H+':'+p))===s,'Existing photo/camera/DIFFERS record changed; new review required: '+p);
 need(sha(fs.readFileSync(index))===binding.index_sha256,'Read-only guards changed physical index.');
 const build=JSON.parse(fs.readFileSync(path.join(MIRROR,'build.json')));need(typeof build.sha==='string'&&build.sha.length>=7&&H.startsWith(build.sha),'Mirror build metadata is not the actual future committed head.');
 return {head:H,base:B,tree:binding.tree,app:binding.app_subtree,index_sha256:binding.index_sha256,source_files:paths.length,mirror_files:binding.mirror_files.length,build};
}
const before=guard();
const picsBytes=fs.readFileSync(path.join(MIRROR,'data/pictures/1904.json')),pics=JSON.parse(picsBytes),id='kimball_house_1801_prairie',imageID='a18-kimball-habs-photo-01';
const p=pics.by_structure[id].find(x=>x.id===imageID);need(p?.held?.f&&p.held.t&&p.creator==='Harold Allen for HABS'&&/Library of Congress/.test(p.holder),'Real held HABS1 picture and credit required.');
const storePins={full:{file:'a18-kimball-habs-photo-01.jpg',bytes:168302,sha256:'ae3fe937b81c338273f33039a27e5222c6bb2cc3e87f15a1e263eac6e3713da3',width:1024,height:776},thumb:{file:'a18-kimball-habs-photo-01-thumb.jpg',bytes:38057,sha256:'8fa581ac098c387f88723d4637c98ecd0f2844cd921ddb4022f9ca933ff5fdf8',width:480,height:364}};
need(p.held.f===storePins.full.file&&p.held.t===storePins.thumb.file&&pics.image_store.base_url==='https://kevinrhaas.github.io/chicago-images/prairie-1904/files/','Expected actual registered HABS1 store representations required');
const fullURL=new URL(p.held.f,pics.image_store.base_url).href,thumbURL=new URL(p.held.t,pics.image_store.base_url).href;
const match=JSON.parse(fs.readFileSync(path.join(ROOT,PH+'habs_1965_01_southwest.match.json')));need(match.verdict==='differs'&&match.differences.filter(d=>d.status==='open').length===12,'Keep existing DIFFERS/12OPEN.');
fs.mkdirSync(OUT);
const report={state:'RUNNING',started_utc:new Date().toISOString(),head:H,base:B,accepted_primary_source_head:PRIMARY_H,accepted_primary_merge_head:PRIMARY_M,normal_primary_merge_receipt_sha256:binding.primary_integration.normal_merge_receipt_sha256,primary_receipt_semantics:primaryReceiptSummary,image_store_pins:storePins,photo_match_reference_sha256:expected['chicago/prairie_1904_v1/research/public/kimball-habs-photo-01.jpg'],before,source_binding_sha256:bindingSHA,helper_sha256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),viewport:{width:390,height:780},actual_normal_tab_label:'Photos',legacy_requirement:'T2389 Images; normal Inspect Photos reads same pictures index and same full viewer',photo_id:imageID,photo_match_verdict:'differs',photo_match_open:12,photographic_MATCH:false,full_renderer_gate:false,visual_review_required:true,visual_reviewed:false,errors:[],actions:[],screenshots:[],assertions:[],network:[],cleanup:{browser_closed:false,server_closed:false}};
const save=()=>fs.writeFileSync(path.join(OUT,'OBSERVATION.json'),JSON.stringify(report,null,2)+'\n');
const check=(name,ok,data=null)=>{report.assertions.push({name,result:ok?'PASS':'FAIL',data});save();need(ok,name);};
let browser=null,context=null,server=null,activePage=null,bodyTasks=[];const pendingBodyTasks=new Set();let success=false;
async function tap(page,s){await page.waitForSelector(s,{state:'visible'});const q=await page.evaluate(async s=>{const e=document.querySelector(s);if(!e||e.disabled)throw Error('Missing control '+s);const nav=e.closest('#navigator');if(nav?.getAnimations)for(let i=0;i<60&&nav.getAnimations().some(a=>a.playState==='running');i++)await new Promise(r=>setTimeout(r,50));e.scrollIntoView({block:'center',inline:'center'});await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const b=e.getBoundingClientRect(),x=b.x+b.width/2,y=b.y+b.height/2,t=document.elementFromPoint(x,y);if(!e.checkVisibility()||b.width<1||b.height<1||x<0||y<0||x>=innerWidth||y>=innerHeight||!(t===e||e.contains(t)))throw Error('Control not hit-testable '+s);return {selector:s,x,y,text:e.textContent.trim()};},s);report.actions.push(q);await page.touchscreen.tap(q.x,q.y);save();}
async function screenshot(page,name){const f=path.join(OUT,name);await page.screenshot({path:f,timeout:90000});const b=fs.readFileSync(f);need(b.length>10000,'Screenshot unexpectedly empty');report.screenshots.push({file:name,bytes:b.length,sha256:sha(b)});save();}
try{
 const site=path.join(ROOT,'site');server=http.createServer((req,res)=>{try{const u=new URL(req.url,'http://127.0.0.1');let f=path.resolve(site,'.'+decodeURIComponent(u.pathname));need(f.startsWith(site+'/'),'Path outside normal published site');if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');const type={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.wasm':'application/wasm','.jpg':'image/jpeg','.png':'image/png','.glb':'model/gltf-binary'}[path.extname(f)]||'application/octet-stream';res.writeHead(200,{'Content-Type':type,'Cache-Control':'no-store'});fs.createReadStream(f).pipe(res);}catch{res.writeHead(404);res.end('Not found');}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url=`http://127.0.0.1:${server.address().port}/4d/1904/`;report.entry=url;
 const pw=await import(pathToFileURL(playwrightModule).href);const chromium=pw.chromium||pw.default?.chromium;need(chromium,'Configured Playwright module required.');
 browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader']});context=await browser.newContext({viewport:{width:390,height:780},hasTouch:true,isMobile:false,deviceScaleFactor:1});const page=await context.newPage();activePage=page;page.setDefaultTimeout(90000);
 page.on('pageerror',e=>report.errors.push({kind:'pageerror',text:cleanText(e.message)}));page.on('console',m=>{if(m.type()==='error')report.errors.push({kind:'console',text:cleanText(m.text())});});page.on('requestfailed',r=>report.errors.push({kind:'requestfailed',url:cleanURL(r.url()),text:cleanText(r.failure()?.errorText)}));
 page.on('response',r=>{if(r.status()>=400)report.errors.push({kind:'HTTP',url:cleanURL(r.url()),status:r.status()});if([fullURL,thumbURL,url.replace('/1904/','/data/pictures/1904.json')].includes(r.url())){let task;task=(async()=>{const b=await r.body();report.network.push({url:cleanURL(r.url()),status:r.status(),bytes:b.length,sha256:sha(b)});})().catch(e=>report.errors.push({kind:'response-body',text:cleanText(e.message)})).finally(()=>pendingBodyTasks.delete(task));pendingBodyTasks.add(task);bodyTasks.push(task);}});
 const response=await page.goto(url,{waitUntil:'domcontentloaded'});check('normal1904frontdoorHTTP200',response?.status()===200);await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000});await page.waitForFunction(()=>document.documentElement.dataset.journey==='landed');
 await tap(page,'#home-roam');await page.waitForFunction(()=>window.__chicago4d?.welcome?.state==='world'&&document.getElementById('gate')?.hidden);report.frame_after_roam=await page.evaluate(()=>window.__chicago4d.renderer.info.render.frame);
 if(await page.evaluate(()=>window.__chicago4d.navigator.level===0))await tap(page,'#nav-grip');await page.waitForFunction(()=>document.getElementById('navigator').getBoundingClientRect().height>innerHeight*.4);
 await tap(page,'#nav-tab-home');await tap(page,'#nav-home .nav-choice[data-segment="goto"]');await page.waitForSelector('#welcome-search',{state:'visible'});await tap(page,'#welcome-search');await page.fill('#welcome-search','Kimball');report.actions.push({kind:'normal_input',selector:'#welcome-search',value:'Kimball'});
 await tap(page,'#welcome-results .welcome-destination[data-kind="structure"][data-id="kimball_house_1801_prairie"]');await page.waitForFunction(()=>document.getElementById('nav-app-inspect')?.dataset.structure==='kimball_house_1801_prairie');
 await tap(page,'#nav-app-inspect [data-insp-tab="photos"]');await page.waitForFunction(()=>document.querySelector('#nav-app-inspect [data-insp-pane="photos"]')?.checkVisibility());
 const item='#nav-app-inspect [data-photo="a18-kimball-habs-photo-01"]';if(!await page.locator(item).count())await tap(page,'#nav-app-inspect .ph-all');await page.waitForSelector(item,{state:'visible'});
 await page.locator(item).scrollIntoViewIfNeeded();await page.waitForFunction(s=>{const e=document.querySelector(s),i=e?.querySelector('img');return i?.complete&&i.naturalWidth>0&&!!e.querySelector('.ph-credit')?.textContent.trim();},item);
 const tile=await page.locator(item).evaluate(e=>{const visible=x=>{const b=x.getBoundingClientRect();return x.checkVisibility()&&b.x>=0&&b.y>=0&&b.right<=innerWidth&&b.bottom<=innerHeight;};return {credit:e.querySelector('.ph-credit')?.textContent.trim(),credit_entirely_visible:visible(e.querySelector('.ph-credit')),thumbnail_entirely_visible:visible(e.querySelector('img')),src:e.querySelector('img')?.currentSrc,width:e.querySelector('img')?.naturalWidth,height:e.querySelector('img')?.naturalHeight,year:e.querySelector('.ph-year')?.textContent};});check('HABS1thumbnaildecodedwithcredit',tile.credit_entirely_visible&&tile.thumbnail_entirely_visible&&tile.credit==='Harold Allen for HABS'&&tile.src===thumbURL&&tile.width===storePins.thumb.width&&tile.height===storePins.thumb.height&&tile.year==='1965',tile);await screenshot(page,'01-Kimball-Photos-HABS1-tile-390x780.png');
 await tap(page,item+' .ph-tile');await page.waitForFunction(({full,width,height})=>{const v=document.querySelector('.pic-viewer:not([hidden])'),i=v?.querySelector('[data-pv-img]');return i?.currentSrc===full&&i.complete&&i.naturalWidth===width&&i.naturalHeight===height;},{full:fullURL,width:storePins.full.width,height:storePins.full.height},{timeout:180000});await page.locator('.pic-viewer [data-pv-img]').evaluate(async i=>{await i.decode();});
 const view=await page.evaluate(()=>{const v=document.querySelector('.pic-viewer:not([hidden])'),i=v?.querySelector('[data-pv-img]'),c=v?.querySelector('[data-pv-credit]');const bounds=e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,width:b.width,height:b.height,entirely_in_view:e.checkVisibility()&&b.x>=0&&b.y>=0&&b.right<=innerWidth&&b.bottom<=innerHeight};};return {photo:bounds(i),credit:bounds(c),creditText:c?.innerText,src:i?.currentSrc,naturalWidth:i?.naturalWidth,naturalHeight:i?.naturalHeight};});
 check('fullRegistered1024x776HABSphotoandwholecreditvisibleTogether',view.photo.entirely_in_view&&view.credit.entirely_in_view&&view.creditText.includes('Harold Allen for HABS')&&view.creditText.includes('Library of Congress')&&view.creditText.includes('NO KNOWN RESTRICTIONS'),view);await screenshot(page,'02-HABS1-full-photo-credit-390x780.png');
 await tap(page,'.pic-viewer [data-pv-close]');await page.waitForFunction(()=>document.querySelector('.pic-viewer')?.hidden===true);await Promise.allSettled(bodyTasks);
 report.runtime=await page.evaluate(()=>{const a=window.__chicago4d;return {ready:a?.ready,error:a?.error??null,problems:[...(a?.problems||[])],scene:a?.scene?.id,frame:a?.renderer?.info?.render?.frame,draw_calls:a?.renderer?.info?.render?.calls,triangles:a?.renderer?.info?.render?.triangles,selected:document.getElementById('nav-app-inspect')?.dataset.structure};});
 check('actual1904Kimballruntimehealthy',report.runtime.ready&&report.runtime.scene==='1904'&&report.runtime.selected===id&&!report.runtime.error&&report.runtime.problems.length===0&&report.runtime.frame>report.frame_after_roam,report.runtime);
 check('actualbrowserreceivedexactRegisteredFullAndThumbBytes',[['full',fullURL],['thumb',thumbURL]].every(([kind,url])=>report.network.some(r=>r.url===url&&r.status===200&&r.bytes===storePins[kind].bytes&&r.sha256===storePins[kind].sha256)));
 success=true;
}catch(e){report.error=cleanText(e.stack||e);report.state='FAIL';if(activePage&&!activePage.isClosed())try{await screenshot(activePage,'FAILED-observation-390x780.png');}catch(x){report.failure_screenshot_error=cleanText(x.message);}}
finally{
 try{if(context)await context.close();if(browser)await browser.close();report.cleanup.browser_closed=true;}catch(e){report.errors.push({kind:'browser-close',text:cleanText(e.message)});success=false;}
 try{if(server){server.closeAllConnections();await new Promise((resolve,reject)=>server.close(e=>e?reject(e):resolve()));}report.cleanup.server_closed=true;}catch(e){report.errors.push({kind:'server-close',text:cleanText(e.message)});success=false;}
 // Context/browser are closed before the last verdict. Drain every tracked body callback,
 // including work delivered while closure was in flight, before final error/PASS evaluation.
 while(pendingBodyTasks.size)await Promise.allSettled([...pendingBodyTasks]);
 report.pending_body_tasks_after_browser_close=pendingBodyTasks.size;
 if(!report.cleanup.browser_closed||!report.cleanup.server_closed||pendingBodyTasks.size!==0)success=false;
 try{report.after=guard();need(sha(fs.readFileSync(bindingFile))===bindingSHA,'Source binding changed during observation.');need(sha(fs.readFileSync(prefix+'.result.json'))===binding.publisher.result_sha256&&sha(fs.readFileSync(prefix+'.cleanup.json'))===binding.publisher.cleanup_sha256,'Publisher receipt changed during observation.');}catch(e){report.errors.push({kind:'final-source-mirror-guard',text:cleanText(e.message)});success=false;}
 if(report.errors.length)success=false;report.state=success?'PASS: normal Photos HABS1 decode+credit observation; visual review and full renderer remain separate':'FAIL';report.ended_utc=new Date().toISOString();save();
}
console.log(JSON.stringify({state:report.state,output:OUT,errors:report.errors.length,screenshots:report.screenshots.length,visual_reviewed:false,photographic_MATCH:false}));if(!success)process.exitCode=1;
