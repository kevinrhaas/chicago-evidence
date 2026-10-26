#!/usr/bin/env node
// UNRUN preparation. Targeted current-DEV normal UI observation after an EXTERNAL merge.
// No old H3 or whole-current-APP/full-renderer qualification is asserted or imported.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';


const HERE=path.dirname(fileURLToPath(import.meta.url));
const ROOT='/workspace/chicago';
const LOG='/workspace/.cloud-setup/logs/transport-recovery';
const DEV='https://chicago.polecat.live/4d/dev/';
const ENTRY=DEV+'1835/';
const EXTERNAL_H='dd1f9028060839da8cc170b16c984a15a2c718bd';
const EXTERNAL_M='e03404d2cc275acfa06316835e088a1892289ab8';
const DONOR_SHA='0dc3818f8822487c416dfc92505b9eba9e708c0d550f66f0767e00800158e4ef';
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
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const need=(v,m)=>{if(!v)throw Error(m);};
const canon=v=>JSON.stringify(v&&typeof v==='object'?Array.isArray(v)?v.map(x=>JSON.parse(canon(x))):Object.fromEntries(Object.keys(v).sort().map(k=>[k,JSON.parse(canon(v[k]))])):v);
const cleanUrl=s=>{try{const u=new URL(s);u.search='';u.hash='';u.username='';u.password='';return u.href;}catch{return String(s);}};
const cleanText=s=>String(s).replace(/https?:\/\/[^\s<>"']+/g,u=>cleanUrl(u)).slice(0,3000);
const cli=process.argv.slice(2);
const opt=k=>{const i=cli.indexOf(k);need(i>=0&&cli[i+1]&&!cli[i+1].startsWith('--'),'Missing '+k);return cli[i+1];};
need(cli.includes('--execute-read-only-current-dev-yard'),'ROOT explicit targeted current-DEV observational execution required.');
const D=opt('--expected-deployed-head');
need(/^[0-9a-f]{40}$/.test(D),'An explicit full actual deployed-D commit is required');
const receiptFile=path.resolve(opt('--current-http-receipt')),receiptSHA=opt('--current-http-receipt-sha256');
const inputFile=path.resolve(opt('--yard-input-binding')),inputSHA=opt('--yard-input-binding-sha256');
const OUTPUT=path.resolve(opt('--out'));
need(/^[0-9a-f]{64}$/.test(receiptSHA)&&/^[0-9a-f]{64}$/.test(inputSHA),'Supply complete actual ROOT-retained current-D HTTP and external-merge input SHA256 values.');
need(OUTPUT.startsWith(LOG+'/')&&!fs.existsSync(OUTPUT),'Use a NEW external result directory.');
const retainedFiles=new Map();
function retained(file,hash,size){
  file=path.resolve(file);need(file.startsWith(LOG+'/')&&/^[0-9a-f]{64}$/.test(hash),'Actual retained external evidence path/SHA required');
  need(fs.lstatSync(file).isFile()&&!fs.lstatSync(file).isSymbolicLink(),'Retained evidence must be a regular file');
  const bytes=fs.readFileSync(file);need(sha(bytes)===hash&&(size===undefined||bytes.length===size),'Retained actual current-D artifact changed: '+file);
  const previous=retainedFiles.get(file);need(!previous||(previous.sha256===hash&&previous.bytes===bytes.length),'Contradictory retained artifact identity');
  retainedFiles.set(file,{path:file,sha256:hash,bytes:bytes.length});return bytes;
}
const originalReceipt=retained(receiptFile,receiptSHA),proof=JSON.parse(originalReceipt);
const inputBytes=retained(inputFile,inputSHA),input=JSON.parse(inputBytes);
need(input.schema==='chicago-current-dev-external-merge-yard-input-v1'&&input.current_dev===D,'Actual current-D external-merge observation input required');
need(input.http_receipt?.path===receiptFile&&input.http_receipt.sha256===receiptSHA&&input.http_receipt.bytes===originalReceipt.length,'Input must name this exact immutable raw HTTP receipt');
need(proof.schema==='chicago-current-dev-external-merge-selected-http-v1'&&proof.result==='PASS'&&proof.current_dev===D&&proof.external_transport_M===EXTERNAL_M&&proof.all_12_served_bytes_match_actual_D===true,'Actual current-D selected HTTP14 PASS required; no historical full-renderer proof substitution');
const observedPR=input.external_pr1279,prRef=observedPR?.native_receipt;
need(observedPR?.number===1279&&observedPR.head===EXTERNAL_H&&observedPR.merge_commit===EXTERNAL_M&&observedPR.merged===true&&typeof observedPR.merged_at==='string'&&prRef,'Actual external merged PR1279 identity required');
const nativePR=JSON.parse(retained(prRef.path,prRef.sha256,prRef.bytes));
need(nativePR.number===1279&&nativePR.state==='closed'&&nativePR.merged===true&&nativePR.merged_at===observedPR.merged_at&&nativePR.head?.sha===EXTERNAL_H&&nativePR.merge_commit_sha===EXTERNAL_M&&nativePR.base?.ref==='dev'&&nativePR.head?.repo?.full_name==='kevinrhaas/chicago'&&nativePR.base?.repo?.full_name==='kevinrhaas/chicago','Native observed service metadata must show the actual external merge, not a fabricated own squash receipt');
need(Array.isArray(proof.http_checks)&&proof.http_checks.length===14&&proof.selected&&canon(Object.keys(proof.selected).sort())===canon(Object.keys(TARGETS).sort()),'Exactly fourteen actual HTTP checks/twelve selected current-D targets required');
const receiptBodies=new Map(),receiptBuilds=[],sourceContracts=[];
for(const row of proof.http_checks){
  need(row.status==='200'&&row.returncode===0&&Number.isSafeInteger(row.bytes)&&row.bytes>0&&/^[0-9a-f]{64}$/.test(row.sha256||''),'Incomplete actual HTTP200/normal-TLS result');
  need(row.url===DEV+row.path&&(row.path==='build.json'||Object.hasOwn(TARGETS,row.path)),'Unexpected actual HTTP target');
  const bytes=retained(row.body,row.sha256,row.bytes);
  if(row.path==='build.json')receiptBuilds.push(bytes);
  else{
    need(!receiptBodies.has(row.path),'Duplicate selected target');
    const source=proof.selected[row.path];
    need(source.source_path===TARGETS[row.path]&&source.body===row.body&&source.bytes===row.bytes&&source.sha256===row.sha256&&/^[0-9a-f]{40}$/.test(source.source_git_blob||'')&&gitBlob(bytes)===source.source_git_blob,'Retained served bytes/native actual-D source-blob binding differs: '+row.path);
    receiptBodies.set(row.path,bytes);sourceContracts.push({public_path:row.path,source_commit:D,source_path:source.source_path,source_git_blob:source.source_git_blob,bytes:source.bytes,sha256:source.sha256});
  }
}
need(receiptBuilds.length===2&&receiptBuilds[0].equals(receiptBuilds[1])&&receiptBodies.size===12,'Missing/changed retained actual build/selected bodies');
const responsiveDevCSS=receiptBodies.get('walk/css/walk.css');
need(sha(responsiveDevCSS)==='e780623862943720d6d30322423c4f7e3ed886f80064dbfaa2bb6f9aa85c55ce'&&responsiveDevCSS.toString('utf8').includes("@media (max-width: 620px) {\n  #__dev { display: none !important; }\n  #__devpill { display: inline-block !important; }\n}"),'Actual current-D source must retain its documented T2785 responsive DEV indicator contract');
const sourceScene=JSON.parse(receiptBodies.get('data/scenes/1835.json'));
const anchor=sourceScene.anchors.find(x=>x.id==='western_hotel_yard');
need(sourceScene.anchors.length===19&&anchor?.local_e===-124&&anchor.local_n===-292&&anchor.yaw_deg===221.19&&canon(proof.yard_anchor)===canon(anchor),'Actual served yard anchor/inventory changed');
const groundRef=input.supporting_source_files?.ground_reading;
need(groundRef?.source_commit===D&&groundRef.source_path==='chicago/4d/data/render/anchor_ground_reading.json'&&/^[0-9a-f]{40}$/.test(groundRef.source_git_blob||''),'Actual D native ground-reading source binding required');
const groundBytes=retained(groundRef.path,groundRef.sha256,groundRef.bytes);need(gitBlob(groundBytes)===groundRef.source_git_blob,'Retained current-D ground source blob differs');
const groundDoc=JSON.parse(groundBytes),groundRow=groundDoc.anchors.find(x=>x.id===anchor.id);
need(groundRow?.inside===true&&groundRow.dry===true&&groundRow.inside_a_roof===null&&groundRow.local_e===anchor.local_e&&groundRow.local_n===anchor.local_n,'Actual D ground source must be dry/outside roofs');
const horseManifest=JSON.parse(receiptBodies.get('data/transport/parked/standing-horses.json'));
const expectedHorse=horseManifest.scenes['1835'].find(x=>x.id===HORSE_ID);
const horseSpec=JSON.parse(receiptBodies.get('data/transport/parked/horse-sevket-sidecar.json'));
need(expectedHorse&&horseSpec.runtime_asset.sha256===HORSE_SHA&&sha(receiptBodies.get(HORSE_REL))===HORSE_SHA&&receiptBodies.get(HORSE_REL).length===3784176,'Actual selected standing-horse d454 representation differs');
const committedAt=proof.build_before?.committedAt;
function verifyBuild(bytes){
  const build=JSON.parse(bytes);need(build.tier==='dev'&&build.ref==='refs/heads/dev'&&build.app==='chicago/4d'&&/^[0-9a-f]{7,40}$/.test(build.sha||'')&&D.startsWith(build.sha)&&typeof committedAt==='string'&&build.committedAt===committedAt&&canon(build)===canon(proof.build_before),'Public build does not identify the same actual current D');return build;
}
verifyBuild(receiptBuilds[0]);need(canon(proof.build_before)===canon(proof.build_after)&&canon(proof.build_before)===canon(JSON.parse(receiptBuilds[0])),'Retained HTTP build-before/after identities differ');
function verifyCurrentBinding(){
  for(const ref of retainedFiles.values()){
    const bytes=fs.readFileSync(ref.path);need(bytes.length===ref.bytes&&sha(bytes)===ref.sha256,'Actual external-merge/current-D evidence drift: '+ref.path);
  }
  need(sha(fs.readFileSync(receiptFile))===receiptSHA&&sha(fs.readFileSync(inputFile))===inputSHA,'Actual immutable input receipts drifted');
  return true;
}
const REVIEW_INPUT=path.resolve(opt('--review-annotation-contract'));
const REVIEW_INPUT_SHA=opt('--review-annotation-contract-sha256');
need(/^[0-9a-f]{64}$/.test(REVIEW_INPUT_SHA),'Complete actual current-D native review-annotation contract SHA256 required');
const reviewContract=JSON.parse(retained(REVIEW_INPUT,REVIEW_INPUT_SHA));
const REVIEW_MESSAGE_SUFFIX=': review_required is set — review annotation retained; this flag does not block scene release';
need(reviewContract.schema==='chicago-current-D-exact-nonblocking-review-annotations-v1'&&reviewContract.current_dev===D&&Array.isArray(reviewContract.expected_ids)&&reviewContract.expected_ids.length===14&&new Set(reviewContract.expected_ids).size===14&&Array.isArray(reviewContract.records)&&reviewContract.records.length===14,'Actual native current-D fourteen-review-annotation contract required');
const REVIEW_IDS=[...reviewContract.expected_ids].sort();
const REVIEW_MESSAGES=REVIEW_IDS.map(id=>id+REVIEW_MESSAGE_SUFFIX).sort();
need(canon(reviewContract.expected_ids)===canon(REVIEW_IDS)&&canon(reviewContract.expected_messages)===canon(REVIEW_MESSAGES)&&canon(reviewContract.records.map(r=>r.id).sort())===canon(REVIEW_IDS),'Pinned sidecar IDs/messages must match exactly, without duplicates');
for(const row of reviewContract.records){
  const bytes=retained(row.path,row.sha256,row.bytes),sidecar=JSON.parse(bytes);
  need(row.source_commit===D&&row.source_path==='chicago/4d/data/sidecars/1835/'+row.id+'.json'&&gitBlob(bytes)===row.source_git_blob&&row.review_required===true&&sidecar.id===row.id&&sidecar.review_required===true&&row.expected_message===row.id+REVIEW_MESSAGE_SUFFIX,'Actual declared current-D review sidecar differs: '+row.id);
}
need(Array.isArray(reviewContract.native_contracts)&&reviewContract.native_contracts.length===2,'Native loader and canonical-smoke annotation contracts required');
for(const row of reviewContract.native_contracts){
  need(row.source_commit===D&&/^[0-9a-f]{40}$/.test(row.source_git_blob||'')&&/^[0-9a-f]{64}$/.test(row.whole_source_sha256||'')&&['chicago/4d/renderers/web/js/scene-loader.js','chicago/4d/tools/smoke_renderer.mjs'].includes(row.source_path),'Native current-D annotation source identity differs');
  retained(row.excerpt_path,row.excerpt_sha256);
}
function exactReviewStatus(pose){
  const r=pose.reviewAnnotations;
  return !!r&&Array.isArray(r.expectedIDs)&&r.expectedIDs.length>0&&canon(r.expectedIDs)===canon(REVIEW_IDS)&&canon(r.reportedIDs)===canon(REVIEW_IDS)&&r.reportedMessages.length===14&&canon([...r.reportedMessages].sort())===canon(REVIEW_MESSAGES)&&Array.isArray(pose.hardProblems)&&pose.hardProblems.length===0;
}
verifyCurrentBinding();
fs.mkdirSync(OUTPUT);
const started=Date.now();
const report={schema:'chicago-current-dev-external-merge-yard-observation-v1',result:'RUNNING',scope:'Targeted current-D normal published yard UI, pose, d454 horse telemetry and two real screenshots after an externally observed PR1279 merge. No whole-current-APP/all24 qualification, photographic/native/gait approval or folded-news verification.',current_dev:D,selected_source_commit:D,external_transport_head:EXTERNAL_H,external_transport_M:EXTERNAL_M,external_merge_observation:observedPR,http_receipt:{path:receiptFile,bytes:originalReceipt.length,sha256:receiptSHA},yard_input_binding:{path:inputFile,bytes:inputBytes.length,sha256:inputSHA},source_contracts:sourceContracts,ground_source_contract:groundRef,helper_sha256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),normal_ui_runtime_donor_sha256:DONOR_SHA,source_anchor:anchor,source_ground_contract:groundRow,assertions:[],viewports:[],visual_review_required:true,visual_reviewed:false,photographic_approval:false,native_approval:false,gait_approval:false,whole_current_APP_qualified:false,all24_current_APP_qualified:false,historical_H3_coverage_transferred:false,merge_performed_by_this_observer:false};
Object.assign(report,{observer_version:2,prior_attempt:{"path":"/workspace/.cloud-setup/logs/transport-recovery/current-D-external-merge-yard-observation1-output/POST-DEV-YARD-NORMAL-UI.json","sha256":"582a4dd6467dc6ddfa4cb89c9b78c0e64b1012b9747ef9d338714d5d30c12995","result":"NONPASS: observer1 wrongly required desktop DEV full banner on mobile; original failure preserved","failure_screenshot":{"path":"/workspace/.cloud-setup/logs/transport-recovery/current-D-external-merge-yard-observation1-output/mobile390x780-FAILURE.png","bytes":797320,"sha256":"2d5717ef07d03da0748037ac6491db5dd73cc9cdb57a54c834246e01561303c9"},"page_errors":[],"build_before_after_unchanged":true,"before_Roam":true,"root_visual_review":"ROOT reported existing visible DEV pill in actual failure screenshot"},responsive_dev_contract:{source_css_sha256:'e780623862943720d6d30322423c4f7e3ed886f80064dbfaa2bb6f9aa85c55ce',breakpoint_max_width_px:620,mobile:'full banner hidden; DEV pill visible with DEV label',desktop:'full banner visible; DEV pill hidden in fresh context'}});
Object.assign(report,{observer_version:3,prior_observer2:{"path":"/workspace/.cloud-setup/logs/transport-recovery/current-D-external-merge-yard-observation2-output/POST-DEV-YARD-NORMAL-UI.json","sha256":"568842734258640e0d8735bd520a306f85aeecfb0b88a32454712ddb5aa4d96a","result":"NONPASS: observer2 incorrectly classified exact native review annotations as loader errors; original result retained","all_page_errors":[],"api_error":null,"reported_review_annotations":14,"mobile_yard_screenshot":{"path":"/workspace/.cloud-setup/logs/transport-recovery/current-D-external-merge-yard-observation2-output/mobile390x780-actual-DEV-Western-Hotel-yard.png","bytes":600627,"sha256":"b2cb8f851187c4723b5be8977e275fee356ab0e55c2648cd0e910ac7f9714389"},"root_visual_review_statement":"ROOT reported the actual mobile screenshot shows the horse head, body and all legs clearly visible, with fence foreground; new run and desktop still require visual review"},review_annotation_contract:{path:REVIEW_INPUT,sha256:REVIEW_INPUT_SHA,current_dev:D,expected_ids:REVIEW_IDS,expected_messages:REVIEW_MESSAGES,source_records:reviewContract.records,native_contracts:reviewContract.native_contracts},review_annotations_retained:true,only_exact_declared_review_messages_are_nonblocking:true,other_loader_problems_are_hard_errors:true});
Object.assign(report,{observer_version:4,expected_deployed_head:D,deployment_input_profile:{http_receipt:{path:receiptFile,sha256:receiptSHA},yard_input_binding:{path:inputFile,sha256:inputSHA},review_annotation_contract:{path:REVIEW_INPUT,sha256:REVIEW_INPUT_SHA}},deployment_stability_required:true,full_current_APP_or_all24_qualification:false});
Object.assign(report,{observer_version:5,detail_precondition:'Explicit native Balanced choice at both widths through Settings/#s-detail whenever runtime or stored native setting is not already balanced; all original detail equality/placement/support/error assertions remain',prior_observer5:{"path":"/workspace/.cloud-setup/logs/transport-recovery/deployed-D3-yard-observation5-output/POST-DEV-YARD-NORMAL-UI.json","sha256":"a3b34bb4bd0c8ab4b9cbce264f21ca1fa6c98004d4b2778566a944170f575314","result":"NONPASS: initial desktop AUTO native setting is empty while its resolved runtime tier is full; prior strict detail-equality assertion retained as failed","mobile_result":"PASS: normal UI, pose, selected horse and real screenshot captured; visual review pending","desktop_initial_runtime":"full","desktop_initial_native_setting":"","all_page_errors":[[],[]],"root_visual_review_statement":"ROOT reported the actual desktop failure screenshot clearly shows the horse; source/runtime observation remains NONPASS until new controlled profile is verified"}});
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
  if(typeof a.registry?.values!=='function')throw Error('Read-only registry review declarations are unavailable');
  const allProblems=[...(a.problems||[])],reviewSuffix=': review_required is set — review annotation retained; this flag does not block scene release';
  const expectedReviewIDs=[...a.registry.values()].filter(r=>r.sidecar?.review_required).map(r=>r.sidecar.id).sort();
  const declaredReviewMessages=new Set(expectedReviewIDs.map(id=>id+reviewSuffix));
  const reportedReviewMessages=allProblems.filter(p=>declaredReviewMessages.has(p));
  const reportedReviewIDs=reportedReviewMessages.map(p=>p.slice(0,-reviewSuffix.length)).sort();
  const hardProblems=allProblems.filter(p=>!declaredReviewMessages.has(p));
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
  return {ready:a.ready,error:a.error,problems:allProblems,reviewAnnotations:{expectedIDs:expectedReviewIDs,reportedIDs:reportedReviewIDs,reportedMessages:reportedReviewMessages},hardProblems,scene:a.scene?.id,anchors:a.scene?.anchors,entry:location.href,base:document.baseURI,journey:document.documentElement.dataset.journey,welcome:a.welcome?.state,gateHidden:document.getElementById('gate')?.hidden,detail:a.detail,detailSetting:a.hud?.settings?.detail,travelMode:a.hud?.settings?.travelMode,navigator:{level:a.navigator?.level,app:a.navigator?.app},walker:{e:s.e,n:s.n,groundY:s.groundY,eyeY:s.eyeY,flying:s.flying,blocked:s.blocked,bearingDeg:a.walker.bearingDeg},camera:{world:world.toArray(),bearingDeg:cameraBearing,quaternion:a.camera.quaternion.toArray(),projection:a.camera.projectionMatrix.toArray()},ground:{height:a.terrain.surfaceHeight(s.e,s.n),water:a.terrain.isWater(s.e,s.n),roofIds:hitRoofs,footprints:a.footprints.length},render:{frame:a.renderer.info.render.frame,calls:a.renderer.info.render.calls,triangles:a.renderer.info.render.triangles},horse:instance?{row:instance.row,receipt:instance.receipt,idle:instance.idle?.status,groupVisible:visible&&instance.group.visible,groupPosition:instance.group.position.toArray(),supportQuaternion:instance.group.children[0]?.quaternion.toArray(),meshCount,meshVisibility,visibleFrustumSamples,allMeshesVisible:meshVisibility.length>0&&meshVisibility.every(m=>m.ownVisible&&m.ancestorsVisible),sampledSkinnedVertices:samples.length,insideFrustum,projectedSamples:samples,materials:(()=>{const v=[];instance.root.traverse(n=>{if(n.isMesh)v.push({name:n.material?.name,metalness:n.material?.metalness,visible:n.visible});});return v;})()}:null};
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
    const banner=await page.evaluate(()=>{const e=document.getElementById('__dev'),b=e?.getBoundingClientRect(),pill=document.getElementById('__devpill'),p=pill?.getBoundingClientRect();return {text:e?.textContent,visible:!!b&&b.width>0&&b.height>0,bounds:b?{x:b.x,y:b.y,width:b.width,height:b.height}:null,pill:{text:pill?.textContent?.trim(),visible:!!p&&p.width>0&&p.height>0,bounds:p?{x:p.x,y:p.y,width:p.width,height:p.height}:null},stamp:document.getElementById('gate-build')?.textContent,robots:document.querySelector('meta[name="robots"]')?.content,entry:location.href,base:document.baseURI};});
    const responsiveDevIndicator=item.viewport.width<=620?banner.visible===false&&banner.pill.visible===true&&banner.pill.text==='DEV':banner.visible===true&&banner.pill.visible===false;
    v.banner=banner;check(item.label+': actual responsive DEV indicator/stamp and normal entry',responsiveDevIndicator&&banner.text.includes('DEV PREVIEW')&&banner.text.includes('dev@'+before.build.sha)&&banner.stamp.includes('DEV PREVIEW')&&banner.stamp.includes('dev@'+before.build.sha)&&banner.entry===ENTRY&&banner.base.startsWith(DEV+'walk/')&&/noindex/.test(banner.robots||''),banner);
    await click(page,'#home-roam',item.touch);await page.waitForFunction(()=>window.__chicago4d?.welcome?.state==='world'&&document.getElementById('gate')?.hidden,null,{timeout:90000,polling:200});
    v.initialDetail=await page.evaluate(()=>window.__chicago4d.detail);
    v.initialHUDDetailSetting=await page.evaluate(()=>window.__chicago4d.hud?.settings?.detail);
    v.observationDetailProfile={requested:'balanced',initial_runtime:v.initialDetail,initial_native_setting:v.initialHUDDetailSetting,control:'#s-detail',method:'normal Settings UI selectOption; no API state setter'};
    check(item.label+': fresh normal Go-to travel choice is instant',await page.evaluate(()=>window.__chicago4d.hud.settings.travelMode==='instantly'));
    if(v.initialDetail!=='balanced'||v.initialHUDDetailSetting!=='balanced'){
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
    check(item.label+': exact fourteen native review annotations retained and no hard loader problems',exactReviewStatus(first),{registry:first.reviewAnnotations,allProblems:first.problems,hardProblems:first.hardProblems});
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
    check(item.label+': zero page/console/HTTP/non-aborted request/loader errors',v.errors.length===0&&v.finalPose.error===null&&exactReviewStatus(v.finalPose),{errors:v.errors,loader:v.finalPose.problems,hardLoader:v.finalPose.hardProblems,reviewAnnotations:v.finalPose.reviewAnnotations,aborted:v.aborted_requests});
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
  try{verifyCurrentBinding();report.final_current_observation_inputs_verified=true;}catch(e){report.final_current_observation_inputs_verified=false;report.current_observation_final_guard_error=cleanText(e.message);report.result='FAIL: retained actual current-D/external-merge evidence guard';process.exitCode=1;}
  if(sha(fs.readFileSync(receiptFile))!==receiptSHA){report.result='FAIL: source HTTP proof drift';process.exitCode=1;}
  report.seconds=(Date.now()-started)/1000;save();const files=[];for(const name of fs.readdirSync(OUTPUT).sort()){const p=path.join(OUTPUT,name);if(fs.statSync(p).isFile()){const b=fs.readFileSync(p);files.push({path:name,bytes:b.length,sha256:sha(b)});}}
  fs.writeFileSync(path.join(OUTPUT,'OUTPUT-MANIFEST.json'),JSON.stringify({files},null,2)+'\n');console.log(JSON.stringify({result:report.result,out:OUTPUT,seconds:report.seconds}));
}
