#!/usr/bin/env node
// PREPARED ONLY. A targeted current-DEV observation, never legacy H3 qualification.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';

const HERE=path.dirname(fileURLToPath(import.meta.url));
const LOG='/workspace/.cloud-setup/logs/transport-recovery';
const M='e03404d2cc275acfa06316835e088a1892289ab8';
const REVIEW_SUFFIX=': review_required is set — review annotation retained; this flag does not block scene release';
const DEV='https://chicago.polecat.live/4d/dev/',ENTRY=DEV+'1835/';
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const cleanURL=s=>{try{const u=new URL(s);u.search='';u.hash='';u.username='';u.password='';return u.href;}catch{return String(s);}};
const cleanText=s=>String(s).replace(/https?:\/\/[^\s<>"']+/g,cleanURL).slice(0,3000);
const args=process.argv.slice(2),at=args.indexOf('--out');
const opt=flag=>{const i=args.indexOf(flag);need(i>=0&&args[i+1]&&!args[i+1].startsWith('--'),'Missing '+flag);return args[i+1];};
const D=opt('--expected-deployed-head');
const INPUT=path.resolve(opt('--input-binding')),INPUT_SHA=opt('--input-binding-sha256');
const REVIEW_CONTRACT=path.resolve(opt('--review-contract')),REVIEW_CONTRACT_SHA=opt('--review-contract-sha256');
need(/^[0-9a-f]{40}$/.test(D),'Exact actually deployed full40 commit required; never guess latest branch.');
need([INPUT_SHA,REVIEW_CONTRACT_SHA].every(h=>/^[0-9a-f]{64}$/.test(h)),'Exact reviewed input/review artifact SHA256 required.');
need(args.includes('--execute-current-dev-notes-observation'),'ROOT must explicitly authorize this read-only current-DEV observation.');
need(at>=0&&args[at+1]&&!args[at+1].startsWith('--'),'A fresh --out directory is required.');
const OUT=path.resolve(args[at+1]);
need(OUT.startsWith(LOG+'/')&&!fs.existsSync(OUT),'Use a NEW external output directory; preserve earlier attempts.');
const inputBytes=fs.readFileSync(INPUT);need(sha(inputBytes)===INPUT_SHA,'Reviewed current-DEV input binding changed.');
const binding=JSON.parse(inputBytes),refs=[{path:INPUT,sha256:INPUT_SHA}];
need(binding.schema==='chicago-current-dev-targeted-folded-notes-input-v1'&&binding.current_dev===D&&binding.external_transport_merge===M,'Current D/external merge identity differs.');
need(binding.native_review_annotation_contract?.path===REVIEW_CONTRACT&&binding.native_review_annotation_contract.sha256===REVIEW_CONTRACT_SHA,'Input binding must pin the exact supplied native-D review contract.');
function bound(r){const b=fs.readFileSync(r.path);need(sha(b)===r.sha256&&(r.bytes===undefined||b.length===r.bytes),'Bound artifact changed: '+r.path);refs.push({path:r.path,sha256:r.sha256});return b;}
const http=JSON.parse(bound(binding.http_receipt)),service=JSON.parse(bound(binding.external_PR1279_service));
need(http.schema==='chicago-current-dev-external-merge-selected-http-v1'&&http.result==='PASS'&&http.current_dev===D&&http.external_transport_M===M&&http.all_12_served_bytes_match_actual_D===true,'Actual targeted current-DEV HTTP receipt is required.');
need(service.number===1279&&service.merged===true&&service.state==='closed'&&service.merge_commit_sha===M&&service.merged_at,'Actual external already-merged PR1279 service fact differs.');
need(typeof binding.source_repository==='string'&&path.resolve(binding.source_repository).startsWith('/workspace/.cloud-setup/')&&binding.source_repository.endsWith('.git'),'Only the separately materialized bare audit repository is allowed; no primary Git.');
const git=(...a)=>execFileSync('git',['--git-dir',binding.source_repository,...a],{cwd:'/workspace',env:{...process.env,GIT_OPTIONAL_LOCKS:'0'},stdio:['ignore','pipe','pipe'],maxBuffer:32*1024*1024});
need(git('rev-parse','--is-bare-repository').toString().trim()==='true','Source audit repository must actually be bare.');
need(git('rev-parse',D+'^{commit}').toString().trim()===D,'Actual native current-D commit is absent.');
git('merge-base','--is-ancestor',M,D);
const reviewContract=JSON.parse(bound({path:REVIEW_CONTRACT,sha256:REVIEW_CONTRACT_SHA}));
need(reviewContract.schema==='chicago-current-D-exact-nonblocking-review-annotations-v1'&&reviewContract.current_dev===D,'Actual native current-D review annotation contract differs.');
const expectedReviewIDs=reviewContract.expected_ids,expectedReviewMessages=reviewContract.expected_messages;
need(Array.isArray(expectedReviewIDs)&&expectedReviewIDs.length===14&&new Set(expectedReviewIDs).size===14&&same(expectedReviewIDs,[...expectedReviewIDs].sort())&&expectedReviewIDs.every(id=>typeof id==='string'&&/^[a-z0-9_]+$/.test(id)),'Exactly fourteen nonempty unique sorted native review IDs required.');
need(same(expectedReviewMessages,expectedReviewIDs.map(id=>id+REVIEW_SUFFIX))&&reviewContract.records.length===14,'Exact native whole review messages/records differ.');
need(same(reviewContract.records.map(r=>r.id).sort(),expectedReviewIDs),'Native annotation sidecar records differ from exact IDs.');
for(const r of reviewContract.records){const raw=bound(r),sidecar=JSON.parse(raw),blob=git('rev-parse',D+':'+r.source_path).toString().trim();need(r.source_commit===D&&r.source_path==='chicago/4d/data/sidecars/1835/'+r.id+'.json'&&r.review_required===true&&sidecar.id===r.id&&sidecar.review_required===true&&r.expected_message===r.id+REVIEW_SUFFIX&&blob===r.source_git_blob&&git('cat-file','blob',blob).equals(raw),'Actual declared review sidecar/Git blob differs: '+r.id);}
need(reviewContract.native_contracts.length===2,'Exact native loader and canonical smoke excerpts required.');
for(const r of reviewContract.native_contracts){const blob=git('rev-parse',D+':'+r.source_path).toString().trim(),raw=git('cat-file','blob',blob),excerpt=bound({path:r.excerpt_path,sha256:r.excerpt_sha256});need(r.source_commit===D&&blob===r.source_git_blob&&sha(raw)===r.whole_source_sha256&&raw.toString().includes(excerpt.toString()),'Native loader/smoke review contract changed: '+r.source_path);}

const expectedCurrentSourcePaths=['chicago/4d/renderers/web/js/changelog.js','chicago/4d/tools/changelog_shim.mjs',...['whatsnew.js','settings-app.js','apps/settings.js','apps/drawer-host.js','navigator.js','about.js'].map(n=>'chicago/4d/renderers/web/js/'+n),'chicago/4d/renderers/web/css/walk.css','.github/chicago-4d-dev-preview.mjs'];
need(binding.source_files.length===11&&new Set(binding.source_files.map(r=>r.path)).size===11&&same(binding.source_files.filter(r=>r.revision===D).map(r=>r.path).sort(),expectedCurrentSourcePaths.sort())&&binding.source_files.filter(r=>r.revision!==D).length===1&&binding.source_files.some(r=>r.revision===M&&r.path==='chicago/4d/changelog.d/T-3083.json'),'Require all ten native current-D UI/publisher sources and the actual external-M pending entry.');
for(const r of binding.source_files){const blob=git('rev-parse',r.revision+':'+r.path).toString().trim(),b=git('cat-file','blob',blob);need(blob===r.git_blob&&b.length===r.bytes&&sha(b)===r.sha256,'Actual pinned native source differs: '+r.path);}
const files=Object.fromEntries(Object.entries(binding.files).map(([n,r])=>[n,bound(r)]));
const TARGET=JSON.parse(files['TARGET-ENTRY.json']),pending=JSON.parse(files['M-PENDING-T-3083.json']);
need(files['M-PENDING-T-3083.json'].equals(git('show',M+':chicago/4d/changelog.d/T-3083.json')),'Retained pending bytes differ from the actual external-M native entry.');
need(TARGET.title==='Rounder carriage lamps and clearer horse eyes'&&TARGET.items.length===4&&same({title:TARGET.title,kind:TARGET.kind,items:TARGET.items},pending)&&same(pending,JSON.parse(files['OLD-PENDING-T-3083.json'])),'The original four-item visitor entry changed.');
need(same(TARGET,binding.target)&&files['D-CHANGELOG.js'].toString().includes(files['TARGET-ENTRY-LITERAL.txt'].toString()),'Actual D folded-entry source excerpt differs.');
const countWords=s=>s.trim().split(/\s+/).filter(Boolean).length;
need(countWords(TARGET.title)<=12&&TARGET.items.length<=6&&TARGET.items.reduce((n,s)=>n+countWords(s),0)<=450,'Visitor entry exceeds the native notes budget.');
const ct=new Date(TARGET.ts).toLocaleString('en-US',{timeZone:'America/Chicago',month:'short',day:'numeric',year:'numeric',hour:'numeric',minute:'2-digit'})+' CT';
need(!Number.isNaN(Date.parse(TARGET.ts))&&TARGET.date===ct,'Actual folded entry CT date does not match its timestamp.');
need(http.http_checks.length===14,'HTTP prerequisite needs its actual two builds and twelve selected responses.');
const oldBuilds=[];
for(const r of http.http_checks){need(r.status==='200'&&r.returncode===0,'An actual HTTP prerequisite failed.');const bytes=bound({path:r.body,bytes:r.bytes,sha256:r.sha256});if(r.path==='build.json')oldBuilds.push(bytes);}
need(oldBuilds.length===2&&oldBuilds[0].equals(oldBuilds[1]),'Retained official build-before/build-after bytes differ.');
const baselineBuild=JSON.parse(oldBuilds[0]);
need(baselineBuild.tier==='dev'&&baselineBuild.app==='chicago/4d'&&baselineBuild.ref==='refs/heads/dev'&&D.startsWith(baselineBuild.sha)&&baselineBuild.sha.length>=8,'Retained public build does not identify D.');
const notesSource=binding.source_files.find(r=>r.path==='chicago/4d/renderers/web/js/changelog.js'&&r.revision===D);
need(notesSource&&sha(files['D-CHANGELOG.js'])===notesSource.sha256,'Expected official changelog bytes are not actual D source.');
const shimSource=git('show',D+':chicago/4d/tools/changelog_shim.mjs').toString();
const shimMatch=/export const WALK_SHIM = `([\s\S]*?)`;\s*$/.exec(shimSource);
need(shimMatch&&files['D-WALK-CHANGELOG-SHIM.js'].equals(Buffer.from(shimMatch[1])),'Expected normal lazy-import shim differs from native D publisher source.');
const targets=new Map([[DEV+'js/changelog.js',files['D-CHANGELOG.js']],[DEV+'walk/js/changelog.js',files['D-WALK-CHANGELOG-SHIM.js']]]);
const primaryIndex='/workspace/chicago/.git/index',indexBefore=sha(fs.readFileSync(primaryIndex));
fs.mkdirSync(OUT);
const started=Date.now(),report={schema:'chicago-current-dev-targeted-folded-notes-ui-v3',result:'RUNNING',scope:'Targeted current DEV delivered four-item entry and normal Settings/About/news presentation only. No legacy H3/all24/whole-APP/canonical own-merge qualification, yard/photo/native/gait or PROD acceptance.',current_dev:D,native_review_annotation_contract:{path:REVIEW_CONTRACT,sha256:REVIEW_CONTRACT_SHA},expected_review_ids:expectedReviewIDs,loader_policy:'Only exact native whole review messages for declared registry IDs are informational; every other loader problem fails',external_transport_merge:M,external_PR1279_head:service.head.sha,http_receipt:binding.http_receipt,input_binding:{path:INPUT,sha256:INPUT_SHA},helper_sha256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),entry:TARGET,source_files:binding.source_files,started_utc:new Date(started).toISOString(),input_artifacts:refs,assertions:[],viewports:[],builds:[],folded_entry_observed:false,visual_review_required:true,visual_reviewed:false,primary_index_unchanged:false};
const save=()=>fs.writeFileSync(path.join(OUT,'RESULT.json'),JSON.stringify(report,null,2)+'\n');
const check=(name,value,data=null)=>{report.assertions.push({name,result:value?'PASS':'FAIL',data});save();need(value,name);};
let browser=null,activeView=null,failed=false;
const pendingTasks=new Set();
async function tap(page,selector,touch,activate=true){
 await page.waitForSelector(selector,{state:'visible'});
 const p=await page.evaluate(async selector=>{const e=document.querySelector(selector);if(!e||e.disabled)throw Error('Unavailable native control: '+selector);const nav=e.closest('#navigator');if(nav?.getAnimations)for(let i=0;i<60&&nav.getAnimations().some(a=>a.playState==='running');i++)await new Promise(r=>setTimeout(r,50));e.scrollIntoView({block:'center',inline:'center'});await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const q=e.getBoundingClientRect(),x=q.x+q.width/2,y=q.y+q.height/2,top=document.elementFromPoint(x,y);if(!e.checkVisibility()||q.width<1||q.height<1||x<0||y<0||x>=innerWidth||y>=innerHeight||!(top===e||e.contains(top)))throw Error('Native control not hit-testable: '+selector);return {selector,x,y,text:e.textContent.trim()};},selector);
 activeView.actions.push({...p,action:activate?'trusted-pointer':'hit-test-before-native-select'});save();
 if(activate){if(touch)await page.touchscreen.tap(p.x,p.y);else await page.mouse.click(p.x,p.y);}
}
async function screenshot(page,name){const file=activeView.label+'-'+name+'.png';await page.screenshot({path:path.join(OUT,file),timeout:90000});const b=fs.readFileSync(path.join(OUT,file));need(b.length>10000,'Empty screenshot');activeView.screenshots.push({file,bytes:b.length,sha256:sha(b)});save();}
async function publicBuild(page){
 const index=report.builds.length,stem='official-build-'+String(index).padStart(2,'0');
 const bodyFile=stem+'.body',headersFile=stem+'.headers',statusFile=stem+'.status',commandFile=stem+'.command.json';
 const bodyPath=path.join(OUT,bodyFile),headersPath=path.join(OUT,headersFile),statusPath=path.join(OUT,statusFile);
 for(const file of [bodyPath,headersPath,statusPath,path.join(OUT,commandFile)])need(!fs.existsSync(file),'Never overwrite a prior official build observation');
 const curlArgs=['--silent','--show-error','--no-insecure','--no-location','--proto','=https','--proto-redir','=https','--max-redirs','0','--connect-timeout','20','--max-time','60','--header','Cache-Control: no-cache','--output',bodyPath,'--dump-header',headersPath,'--write-out','%{http_code}',DEV+'build.json'];
 const row={observation_index:index,url:DEV+'build.json',route:'Normal curl with inherited proxy environment, HTTPS verification and no redirects',result:'RUNNING'},began=Date.now();
 report.builds.push(row);save();let stdout='',stderr='',returncode=0;
 try{stdout=execFileSync('curl',curlArgs,{cwd:'/workspace',env:process.env,stdio:['ignore','pipe','pipe'],encoding:'utf8',maxBuffer:1024*1024});}
 catch(e){returncode=Number.isInteger(e.status)?e.status:-1;stdout=e.stdout?.toString()||'';stderr=cleanText(e.stderr?.toString()||e.message);}
 fs.writeFileSync(statusPath,stdout);
 const fileProof=(file,name)=>fs.existsSync(file)?{file:name,bytes:fs.statSync(file).size,sha256:sha(fs.readFileSync(file))}:{file:name,present:false};
 row.status=Number(stdout.trim());row.curl_status_raw=stdout;row.curl_returncode=returncode;row.seconds=(Date.now()-began)/1000;row.body_file=fileProof(bodyPath,bodyFile);row.headers_file=fileProof(headersPath,headersFile);row.status_file=fileProof(statusPath,statusFile);row.stderr=stderr;row.result='FAIL';
 fs.writeFileSync(path.join(OUT,commandFile),JSON.stringify({program:'curl',arguments:curlArgs,cwd:'/workspace',inherited_proxy_environment_preserved:true,TLS_verification_enabled:true,redirects_followed:false,returncode,http_status_raw:stdout,stderr,body:row.body_file,headers:row.headers_file,status:row.status_file},null,2)+'\n');
 row.command_file=fileProof(path.join(OUT,commandFile),commandFile);save();
 need(returncode===0,'Official DEV build normal inherited-proxy curl failed');
 need(stdout.trim()==='200','Official DEV build failed/redirected');
 const b=fs.readFileSync(bodyPath);need(b.equals(oldBuilds[0]),'Public DEV moved since the actual selected-byte receipt');
 row.bytes=b.length;row.sha256=sha(b);row.build=JSON.parse(b);row.result='PASS';save();
}
async function drain(){while(pendingTasks.size)await Promise.allSettled([...pendingTasks]);}
try{
 const require=createRequire('/workspace/.cloud-setup/npm/package.json'),{chromium}=require('playwright');
 browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
 for(const [label,viewport,touch]of [['mobile390x780',{width:390,height:780},true],['desktop1280x800',{width:1280,height:800},false]]){
  const v={label,viewport,errors:[],actions:[],network:[],screenshots:[],scales:[],pending_body_tasks:0,context_closed:false,result:'RUNNING'},began=Date.now();report.viewports.push(v);activeView=v;let context=null,page=null;
  try{
   context=await browser.newContext({viewport,hasTouch:touch,isMobile:false,deviceScaleFactor:touch?2:1});page=await context.newPage();page.setDefaultTimeout(90000);
   page.on('pageerror',e=>v.errors.push({kind:'pageerror',text:cleanText(e.message)}));
   page.on('console',m=>{if(m.type()==='error')v.errors.push({kind:'console',text:cleanText(m.text())});});
   page.on('requestfailed',r=>v.errors.push({kind:'requestfailed',url:cleanURL(r.url()),text:cleanText(r.failure()?.errorText)}));
   page.on('response',r=>{if(r.status()>=400)v.errors.push({kind:'HTTP',url:cleanURL(r.url()),status:r.status()});if(targets.has(r.url())){let task;v.pending_body_tasks++;task=(async()=>{const b=await r.body();need(r.status()===200&&b.equals(targets.get(r.url())),'Real normal lazy-import bytes differ from actual D');const file=label+'-notes-response-'+v.network.length+'.body';fs.writeFileSync(path.join(OUT,file),b);v.network.push({url:cleanURL(r.url()),status:r.status(),bytes:b.length,sha256:sha(b),body_file:file});})().catch(e=>v.errors.push({kind:'body-read',text:cleanText(e.message)})).finally(()=>{v.pending_body_tasks--;pendingTasks.delete(task);});pendingTasks.add(task);}});
   await publicBuild(page);
   const navigation=await page.goto(ENTRY,{waitUntil:'domcontentloaded'});need(navigation?.status()===200&&page.url()===ENTRY,'Normal official DEV1835 frontdoor identity differs');
   await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240000,polling:1000});
   await page.waitForFunction(()=>document.documentElement.dataset.journey==='landed',null,{timeout:90000});
   const preview=await page.evaluate(()=>{const banner=document.getElementById('__dev'),pill=document.getElementById('__devpill');return {banner_text:banner?.textContent||'',banner_visible:banner?.checkVisibility()===true,pill_text:pill?.textContent||'',pill_visible:pill?.checkVisibility()===true,gate_stamp:document.getElementById('gate-build')?.textContent||'',robots:document.querySelector('meta[name="robots"]')?.content||'',entry:location.href,base:document.baseURI};});
   const responsive=viewport.width<=620?preview.pill_visible&&!preview.banner_visible&&preview.pill_text.trim()==='DEV':preview.banner_visible&&!preview.pill_visible;
   check(label+': actual responsive DEV preview identity',responsive&&preview.banner_text.includes('DEV PREVIEW')&&preview.banner_text.includes('dev@'+baselineBuild.sha)&&preview.gate_stamp.includes('DEV PREVIEW')&&preview.gate_stamp.includes('dev@'+baselineBuild.sha)&&preview.entry===ENTRY&&preview.base.startsWith(DEV+'walk/')&&/noindex/.test(preview.robots),preview);
   await tap(page,'#home-roam',touch);await page.waitForFunction(()=>document.getElementById('gate')?.hidden===true);
   if(await page.evaluate(()=>{const e=document.getElementById('control-help');return !!e&&!e.hidden;}))await tap(page,'#control-help-gotit',touch);
   const boot=await page.evaluate(()=>{const a=window.__chicago4d;return {ready:a?.ready,scene:a?.scene?.id,error:a?.error??null,problems:[...(a?.problems||[])],review_required_registry_ids:[...(a?.registry?.values()||[])].filter(r=>r.sidecar?.review_required).map(r=>r.sidecar.id).sort(),frame:a?.renderer?.info?.render?.frame};});
   const registryReviewIDs=boot.review_required_registry_ids,reportedReviewMessages=boot.problems.filter(p=>typeof p==='string'&&p.includes('review_required is set')).sort(),reportedReviewIDs=reportedReviewMessages.map(p=>p.split(':',1)[0]).sort();
   const declaredAllowedMessages=new Set(registryReviewIDs.filter(id=>expectedReviewIDs.includes(id)).map(id=>id+REVIEW_SUFFIX));
   boot.reported_review_ids=reportedReviewIDs;boot.reported_review_messages=reportedReviewMessages;boot.informational_review_annotations=boot.problems.filter(p=>declaredAllowedMessages.has(p));boot.hard_problems=boot.problems.filter(p=>!declaredAllowedMessages.has(p));
   check(label+': exact native declared and reported review annotations',registryReviewIDs.length>0&&new Set(registryReviewIDs).size===registryReviewIDs.length&&new Set(reportedReviewIDs).size===reportedReviewIDs.length&&same(registryReviewIDs,expectedReviewIDs)&&same(reportedReviewIDs,expectedReviewIDs)&&same(reportedReviewMessages,[...expectedReviewMessages].sort()),boot);
   check(label+': healthy normal1835 entry with annotations retained',boot.ready&&boot.scene==='1835'&&!boot.error&&boot.hard_problems.length===0&&boot.frame>0,boot);
   const open=async tab=>{if(touch&&await page.evaluate(()=>window.__chicago4d.navigator?.level===0))await tap(page,'#nav-grip',touch);await tap(page,'#nav-rail [data-app="settings"]',touch);await page.waitForFunction(()=>{const r=document.getElementById('navigator')?.getBoundingClientRect();return r&&(innerWidth>620?r.width>=380:r.height>=innerHeight*.4);});await page.waitForFunction(()=>{const p=document.getElementById('panel');return p&&!p.hidden&&!!p.closest('.nav-screen:not([hidden])');});if(await page.evaluate(()=>window.__chicago4d.hud.tab)!==tab)await tap(page,'.panel-tab[data-tab="'+tab+'"]',touch);};
   await open('settings');
   v.observationDetailProfile={requested:'balanced',control:'#s-detail',method:'ordinary native Settings selectOption; no API state setter',before:await page.evaluate(()=>({runtime:window.__chicago4d?.detail,nativeChoice:window.__chicago4d?.hud?.settings?.detail,control:document.getElementById('s-detail')?.value}))};save();
   await tap(page,'#s-detail',touch,false);await page.selectOption('#s-detail','balanced');v.actions.push({selector:'#s-detail',action:'normal-select-input-change',value:'balanced'});save();
   await page.waitForFunction(()=>window.__chicago4d?.detail==='balanced'&&window.__chicago4d?.hud?.settings?.detail==='balanced'&&document.getElementById('s-detail')?.value==='balanced'&&JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').detail==='balanced',null,{timeout:180000,polling:500});
   v.observationDetailProfile.after=await page.evaluate(()=>({runtime:window.__chicago4d?.detail,nativeChoice:window.__chicago4d?.hud?.settings?.detail,storedChoice:JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').detail,control:document.getElementById('s-detail')?.value}));save();
   check(label+': native About contains its news link',await page.evaluate(()=>!!document.getElementById('s-open-whatsnew')?.closest('#s-about')));
   await tap(page,'#s-open-whatsnew',touch);
   const waitTarget=()=>page.waitForFunction(title=>[...document.querySelectorAll('#whatsnew .wn-entry .wn-title')].some(e=>e.textContent===title),TARGET.title,{timeout:90000,polling:250});
   await waitTarget();
   check(label+': About opened the actual news panel',await page.evaluate(()=>window.__chicago4d.hud.tab==='whatsnew'));
   const target=page.locator('#whatsnew .wn-entry').filter({has:page.locator('.wn-title',{hasText:TARGET.title})});
   check(label+': one target folded entry exists',await target.count()===1);
   const expectedMeta=(TARGET.kind==='feature'?'Added':TARGET.kind==='fix'?'Fixed':TARGET.kind==='polish'?'Polish':TARGET.kind)+' · '+TARGET.date;
   const exactTarget=async()=>{const row=await target.evaluate(e=>({title:e.querySelector('.wn-title')?.textContent,meta:e.querySelector('.wn-meta')?.textContent,items:[...e.querySelectorAll('.wn-items li')].map(x=>x.textContent)}));check(label+': exact target title/date/four ordered items',row.title===TARGET.title&&row.meta===expectedMeta&&same(row.items,TARGET.items),row);};
   await exactTarget();await drain();
   check(label+': normal lazy imports equal native D fleet notes and shim',[...targets.keys()].every(u=>v.network.some(r=>r.url===u&&r.status===200)),v.network);
   const observeScale=async(scale,name)=>{
    const state=await page.evaluate(()=>({scale:getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim(),stored:JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').textScale}));
    check(label+': '+name+' actual text scale',state.scale===String(scale)&&(scale===1?state.stored===undefined||state.stored===1:state.stored===scale),state);
    await exactTarget();const parts=target.locator('.wn-title,.wn-meta,.wn-items li');check(label+': '+name+' exactly title/date/four visitor fields',await parts.count()===6);const fields=[];
    for(let i=0;i<6;i++){
     await parts.nth(i).scrollIntoViewIfNeeded();
     const d=await parts.nth(i).evaluate(e=>{const r=e.getBoundingClientRect(),screen=e.closest('#nav-app-settings'),box=screen?.getBoundingClientRect();if(!box)throw Error('Actual settings/news screen missing');let top=0,bottom=innerHeight,left=0,right=innerWidth;for(let a=e.parentElement;a;a=a.parentElement){const c=getComputedStyle(a),q=a.getBoundingClientRect();if(['auto','scroll','hidden','clip'].includes(c.overflowY)){top=Math.max(top,q.top);bottom=Math.min(bottom,q.bottom);}if(['auto','scroll','hidden','clip'].includes(c.overflowX)){left=Math.max(left,q.left);right=Math.min(right,q.right);}}const c=getComputedStyle(e),range=document.createRange();range.selectNodeContents(e);const lines=[...range.getClientRects()].filter(q=>q.width>.1&&q.height>.1).map(q=>({left:q.left,right:q.right,top:q.top,bottom:q.bottom}));const x=r.x+r.width/2,y=r.y+r.height/2,hit=document.elementFromPoint(x,y);return {text:e.textContent,visible:e.checkVisibility(),left:r.left,right:r.right,top:r.top,bottom:r.bottom,clip:{left,right,top,bottom},fully_in_clip:r.left>=left-1&&r.right<=right+1&&r.top>=top-1&&r.bottom<=bottom+1,inside_settings:r.left>=box.left-1&&r.right<=box.right+1,uncovered:hit===e||e.contains(hit),text_fits:e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+2&&c.textOverflow!=='ellipsis',line_bounds_fit:lines.every(q=>q.left>=left-1&&q.right<=right+1),lines};});
     check(label+': '+name+' complete visible field'+i,d.visible&&d.fully_in_clip&&d.inside_settings&&d.uncovered&&d.text_fits&&d.line_bounds_fit,d);fields.push(d);await screenshot(page,name+'-field'+i);
    }
    v.scales.push({scale,state,fields});await target.locator('.wn-title').scrollIntoViewIfNeeded();await screenshot(page,name+'-entry');
   };
   await observeScale(1,'normal100');
   await open('settings');await tap(page,'#s-text-size',touch,false);await page.selectOption('#s-text-size','1.4');await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1.4');await open('whatsnew');await waitTarget();await observeScale(1.4,'enlarged140');
   await open('settings');await tap(page,'#s-text-size',touch,false);await page.selectOption('#s-text-size','1');await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1');
   check(label+': native text preference restored',await page.evaluate(()=>JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').textScale===1));
   await publicBuild(page);await drain();check(label+': zero errors before context closure',v.errors.length===0,v.errors);v.result='PENDING_FINAL_CLOSE';
  }catch(e){failed=true;v.result='FAIL';v.error=cleanText(e.stack||e);if(page&&!page.isClosed())try{await screenshot(page,'FAILURE');}catch(x){v.failure_screenshot_error=cleanText(x.message);}}
  finally{try{if(context)await context.close();v.context_closed=true;}catch(e){failed=true;v.errors.push({kind:'context-close',text:cleanText(e.message)});}await drain();v.pending_body_tasks_after_close=v.pending_body_tasks;v.result=v.result==='PENDING_FINAL_CLOSE'&&v.context_closed&&v.pending_body_tasks===0&&v.errors.length===0?'PASS':'FAIL';if(v.result!=='PASS')failed=true;v.seconds=(Date.now()-began)/1000;save();activeView=null;}
 }
}catch(e){failed=true;report.error=cleanText(e.stack||e);}
finally{
 try{if(browser)await browser.close();report.browser_closed=true;}catch(e){failed=true;report.browser_close_error=cleanText(e.message);}
 await drain();report.pending_body_tasks_final=pendingTasks.size;
 try{for(const r of refs)need(sha(fs.readFileSync(r.path))===r.sha256,'An observational input changed during the run');need(sha(fs.readFileSync(primaryIndex))===indexBefore,'Primary physical index changed during external observation');report.primary_index_unchanged=true;report.final_input_hashes_verified=true;}catch(e){failed=true;report.final_guard_error=cleanText(e.message);}
 for(const v of report.viewports)if(!v.context_closed||v.errors.length||v.pending_body_tasks)v.result='FAIL';
 if(!report.browser_closed||pendingTasks.size||report.viewports.length!==2||!report.final_input_hashes_verified||report.viewports.some(v=>v.result!=='PASS'||v.scales.length!==2||!v.context_closed||v.errors.length||v.pending_body_tasks))failed=true;
 report.result=failed?'FAIL':'PASS';report.folded_entry_observed=!failed;report.completed_utc=new Date().toISOString();report.seconds=(Date.now()-started)/1000;save();
 const files=fs.readdirSync(OUT).filter(n=>fs.statSync(path.join(OUT,n)).isFile()).map(n=>{const b=fs.readFileSync(path.join(OUT,n));return {path:n,bytes:b.length,sha256:sha(b)};});fs.writeFileSync(path.join(OUT,'OUTPUT-MANIFEST.json'),JSON.stringify({files},null,2)+'\n');
}
console.log(JSON.stringify({result:report.result,output:OUT,folded_entry_observed:report.folded_entry_observed,visual_reviewed:false}));if(failed)process.exitCode=1;
