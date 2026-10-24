#!/usr/bin/env node
// EXTERNAL TRANSPORT+T3125 FOCUSED NEWS-WRAPPING ACCEPTANCE. Not canonical PART13, all-stage smoke, or confidence persistence.
// COMBINED TRANSPORT/UI CANDIDATE: canonical wait/data/layout predicates unchanged. Root must supply a fresh preflight receipt and committed HEAD; old helpers remain immutable.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import vm from 'node:vm';
const REPO='/workspace/chicago';
const BASE='5d8c495ff8b04f8905cb34679e2b050c93e16101'; // Pre-UI merged transport tree, deliberately not wholesale DEV.
const STAGED_TREE='4b2a7066a039936ddcc65d8c1c891fcf25dd7e5f';
const EXPECTED_APP='43838a949e02a01de4ad064aa859c2d11995524d';
const CSS_SHA='e780623862943720d6d30322423c4f7e3ed886f80064dbfaa2bb6f9aa85c55ce';
const BASE_CSS_SHA='0f60b79eb1ae0bd48c367772811964ed272a36b1609988b52160b374101cdb0f';
const OWNED_FILES=[{"path":"chicago/4d/changelog.d/T-3083.json","sha256":"860e9a30aff1ad5b88135a28e855f8165ca9f028ecb431573c5568ff535d57a0"},{"path":"chicago/4d/docs/ROADMAP.md","sha256":"c38716485531f697d5f0fb06f1fb9154d3948755d2beabc63a24c79047fb4813"},{"path":"chicago/4d/docs/STATUS.md","sha256":"b65304970da28f90ed50a52a5e3ee9071b0061af16cf15d88225754e43628209"},{"path":"chicago/4d/renderers/web/css/walk.css","sha256":"e780623862943720d6d30322423c4f7e3ed886f80064dbfaa2bb6f9aa85c55ce"}];
const PROTECTED_TRANSPORT=[{"path":"chicago/4d/assets/LICENSES.md","mode":"100644","blob":"a2bb95a8f5b11c1124caa8ee61b7c525343a5c03"},{"path":"chicago/4d/assets/authored/transport/horse_standing/ADAPTATION.md","mode":"100644","blob":"871b1c2696bd53431566772aec148dd6bf5141ba"},{"path":"chicago/4d/assets/authored/transport/horse_standing/ATTRIBUTION.md","mode":"100644","blob":"3d3ce5398ed2cd54ae0d7bb554787611919b6535"},{"path":"chicago/4d/assets/authored/transport/horse_standing/SOURCE.json","mode":"100644","blob":"4b1346d5bf5a146cdaa71339e20047fed33e875d"},{"path":"chicago/4d/assets/authored/transport/horse_standing/eye-uv-v1-boundary-receipt.json","mode":"100644","blob":"001e9ebfc6075c231b13c13da1d9f7556c12ab74"},{"path":"chicago/4d/assets/authored/transport/horse_standing/eye-uv-v1-derivation-receipt.json","mode":"100644","blob":"817c930ee5e94e8138ac80bd7ac833d69f8cb9ed"},{"path":"chicago/4d/assets/authored/transport/horse_standing/eye-uv-v1-source-aperture-rays.json","mode":"100644","blob":"3a579f04dfdbe31dd05114f88d557305a208684d"},{"path":"chicago/4d/assets/authored/transport/horse_standing/generate_eye_uv_v1.py","mode":"100644","blob":"a267797c3580fc2bacd8fb7b4ad8f2520335ee0c"},{"path":"chicago/4d/assets/authored/transport/horse_standing/horse-sevket-v16-planted-standing-eye-uv-v1.glb","mode":"100644","blob":"2716a2b5e75a35ff1a13105a73a68192971e6d16"},{"path":"chicago/4d/data/render/anchor_ground_reading.json","mode":"100644","blob":"2d7ec1b8d7fe601008d0b032bedeb9c99ffffcfe"},{"path":"chicago/4d/data/scenes/1835.json","mode":"100644","blob":"e55dd5a2d9d105f4a1b276895185800196473e64"},{"path":"chicago/4d/data/sources/sevketkabatas_2021_horse_model.json","mode":"100644","blob":"c0cc4c113c9c8e173df6e5e0eec9e86840f0cc43"},{"path":"chicago/4d/data/transport/parked/horse-sevket-sidecar.json","mode":"100644","blob":"3061d240a13e8dde7621ab19e8924f16e1051b31"},{"path":"chicago/4d/data/transport/parked/standing-horse-planted/eye-uv-v1-derivation-receipt.json","mode":"100644","blob":"817c930ee5e94e8138ac80bd7ac833d69f8cb9ed"},{"path":"chicago/4d/data/transport/parked/standing-horse-planted/eye-uv-v1-loaded129-result.json","mode":"100644","blob":"21d89ec2ec4f7da3393e8652a5a51d2edf054a2c"},{"path":"chicago/4d/data/transport/parked/standing-horse-planted/eye-uv-v1-loaded129-summary.json","mode":"100644","blob":"287fccdd95c0f211f901ca87db5dd35610c8ced8"},{"path":"chicago/4d/data/transport/parked/standing-horse-planted/eye-uv-v1-loaded129-terminal.json","mode":"100644","blob":"b05d5a4c07828d409a6771d2d5dbd0117ec79f8c"},{"path":"chicago/4d/data/transport/parked/standing-horses.json","mode":"100644","blob":"83d571fe529214f072e72199ff25a3e8961e287d"},{"path":"chicago/4d/renderers/web/js/parked-transport.js","mode":"100644","blob":"d00e0f8d37942179e4a034ed4ac67aaf9f98b5c7"},{"path":"chicago/4d/renderers/web/js/standing-horse-planted-idle.js","mode":"100644","blob":"a587ebe8eca5c7328e122b1b20a1d7ab7a3ca19c"},{"path":"chicago/4d/renderers/web/transport/LICENSES.md","mode":"100644","blob":"8dd2832fb6b1d3a4584bfd70714fe073460bef43"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/BUILD-RECEIPT.json","mode":"100644","blob":"927aa3e40fb10d163e3070565a3c8599346ae29d"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/MID-BUILD-RECEIPT.json","mode":"100644","blob":"ec9b34de37488ac74e08f20525fc4809c5023591"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/brougham-mid-source.glb","mode":"100644","blob":"57e12202394aab605da5d37e0aaa17a00ea89e61"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/brougham-mid.glb","mode":"100644","blob":"f514bf90edc37fb54eec637229cefc3d1dd2a51a"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/brougham-near.glb","mode":"100644","blob":"16a86e19b82a06f4d6b7773a381d2c468ea81ab5"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/brougham-source.glb","mode":"100644","blob":"d4f8a31a386b49d6f5fb42ec8271143df3cd6335"},{"path":"chicago/4d/renderers/web/transport/parked-brougham/brougham.json","mode":"100644","blob":"c2b9ec656f7b00d913ade8be2c947e1917f15b68"},{"path":"chicago/4d/renderers/web/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb","mode":"100644","blob":"2716a2b5e75a35ff1a13105a73a68192971e6d16"},{"path":"chicago/4d/tools/check_brougham_near.py","mode":"100644","blob":"fb95711db3afa704c4867a6cadc5de8163f6e67d"},{"path":"chicago/4d/tools/test_planted_standing_horse_contract.mjs","mode":"100644","blob":"4cb107a3b5f41e2400d90107195dc9c4c0ce3341"},{"path":"chicago/4d/tools/test_standing_horse_eye_uv_boundary.py","mode":"100644","blob":"795b4d7fed224972dfbd7051d5caff978f3c744f"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/BUILD-RECEIPT.json","mode":"100644","blob":"70bbef390695c5a352b4b4c8fa07812799420867"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/MID-BUILD-RECEIPT.json","mode":"100644","blob":"91a8276b58763188ebef294a680d8a3dcc176e4e"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/README.md","mode":"100644","blob":"4213eed3a74233d25cd86031f121164c818c6641"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/brougham.json","mode":"100644","blob":"1df5ae7f7e513acc8fe2492700687bf6828bba4b"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/check_mid.py","mode":"100644","blob":"45b8c5b7e9a49da310403ba08fa443baae4e4b51"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/check_near.py","mode":"100644","blob":"7c2f3ed55437404866210c898675080dc4c3e46b"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/generate.py","mode":"100644","blob":"74d2ec907b37408590488d81c6375233b704b8e4"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/mid-contract.json","mode":"100644","blob":"c33cc2bf64269c7e7b406a774b5081a42dc263b8"},{"path":"chicago/4d/tools/transport/brougham/archive-v17/near-contract.json","mode":"100644","blob":"d2a065546cb2e11c109c7f95bdfd47b207881323"},{"path":"chicago/4d/tools/transport/brougham/archived-khronos/V18-mid-indexed.json","mode":"100644","blob":"34ef06b81f94bdb7ccc76a13f349b220fd60ecbb"},{"path":"chicago/4d/tools/transport/brougham/archived-khronos/V18-mid-raw.json","mode":"100644","blob":"1abea323f314e1c11141f2a2407e6c466a7f6e5d"},{"path":"chicago/4d/tools/transport/brougham/archived-khronos/V18-near-indexed.json","mode":"100644","blob":"4fde101ba265198cbf5755a178c574705bcc9bf1"},{"path":"chicago/4d/tools/transport/brougham/archived-khronos/V18-near-raw.json","mode":"100644","blob":"7d770c9a2761d6d8c9dbe327e7a10159ae9cc3e8"},{"path":"chicago/4d/tools/transport/brougham/check_mid.py","mode":"100644","blob":"9919124f1e192aabaf03a4ed6cb9e4fb8a16a1c9"},{"path":"chicago/4d/tools/transport/brougham/check_near.py","mode":"100644","blob":"7f00df40bf620950f1163166acab2de378ae76e0"},{"path":"chicago/4d/tools/transport/brougham/generate.py","mode":"100644","blob":"70be7a3069db058db5db5535b4444d59c80eb1d8"},{"path":"chicago/4d/tools/transport/brougham/lamp_geometry.py","mode":"100644","blob":"cc1f187c96fe37f6706370ca1c37ba67669ee70f"},{"path":"chicago/4d/tools/transport/brougham/mid-contract.json","mode":"100644","blob":"1790f3e68343048f3da32edf8d5e1d5d0097d1ad"},{"path":"chicago/4d/tools/transport/brougham/near-contract.json","mode":"100644","blob":"10ac4b1594e3ecd0dfac83c88d2c7c02d5817a27"},{"path":"chicago/4d/tools/transport/brougham/test_lod.mjs","mode":"100644","blob":"f9a531178ed7bf49564001ed320515e1d1251575"}];
const ORIGINAL_TRANSPORT_ANCHOR={"title":"Rounder carriage lamps and clearer horse eyes","kind":"change","items":["Rounder coach-lamp heads replace the earlier tall angular ones on the parked 1904 Brougham.","The standing horse has darker, more coherent eyes, with its coat, shape and natural weight shift preserved.","The 1835 viewpoint list now includes the Western Hotel yard, with a direct arrival near its standing horse."]};
const EXPECTED_UI_ITEM="Long links and release notes wrap within What's new at normal and enlarged text sizes, keeping the complete text readable inside the Navigator.";
const NOTES_SHA='b98f18554ed58aee5d7200d1789228e9310e91c5ce08c3cdfcc24d48a22abd5d';
const CANONICAL_SMOKE_SHA='4586e7101000910cde7743048b72b72b3b04f7896417f5fe1a97af14e1e941bd';
const APP=path.join(REPO,'chicago/4d'), SITE=path.join(REPO,'site/4d');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(p);
const git=(...args)=>execFileSync('git',args,{cwd:REPO,encoding:'utf8',maxBuffer:128*1024*1024,env:{...process.env,GIT_OPTIONAL_LOCKS:'0'}});
const arg=k=>{const i=process.argv.indexOf(k);return i<0?null:process.argv[i+1];};
if(!process.argv.includes('--execute-after-gate')||!arg('--output')){
 console.error('Prepared helper only. Root launch after green full preflight: node <helper> --execute-after-gate --expected-head <actualHEAD> --preflight-prefix <actual fresh UI preflight prefix> --output <NEW external output directory>');
 process.exit(2);
}
const EXPECTED_HEAD=arg('--expected-head');
const PREFLIGHT_PREFIX=arg('--preflight-prefix');
if(!PREFLIGHT_PREFIX?.startsWith('/workspace/.cloud-setup/logs/transport-recovery/')||PREFLIGHT_PREFIX.endsWith('/'))throw new Error('Supply the actual fresh final-base UI preflight prefix; no inherited receipt default');
if(!/^[0-9a-f]{40}$/.test(EXPECTED_HEAD))throw new Error('Expected head must be a complete40hexSHA');
const OUTPUT=path.resolve(arg('--output'));
if(!OUTPUT.startsWith('/workspace/.cloud-setup/')||fs.existsSync(OUTPUT))throw new Error('Output must be a NEW external .cloud-setup directory');
fs.mkdirSync(OUTPUT,{recursive:true});
const started=Date.now(), assertions=[], viewportResults=[];
const report={label:'COMBINED TRANSPORT/UI FOCUSED NEWS-WRAPPING ACCEPTANCE ONLY — NOT A NEW FULL PART13 OR FULL GATE',baseline_pre_ui_tree:BASE,expected_head:EXPECTED_HEAD,staged_tree:STAGED_TREE,preflight_prefix:PREFLIGHT_PREFIX,CSS_sha256:CSS_SHA,notes_sha256:NOTES_SHA,canonical_smoke_sha256:CANONICAL_SMOKE_SHA,assertions,viewports:viewportResults,coverage_limits:['Does not re-run other PART13 assertions, confidence persistence, renderer matrices or full gates.','One runtime input changed: news-scoped CSS. Exact seven-line removal restores base CSS; every other runtime input is source-identical. This is news-specific acceptance. Other runtime inputs equal the PRE-UI merged transport tree5d8, including retained transport changes. This focused helper neither proves nor substitutes for the new combined all15/both-viewport renderer matrix. No unchanged whole broad hash is claimed.']};
const cleanUrl=v=>{try{const u=new URL(v);u.search='';u.hash='';u.username='';u.password='';return u.href;}catch{return String(v);}};
const cleanText=s=>String(s).replace(/https?:\/\/[^\s<>"']+/g,cleanUrl);
let collectRuntimeFailures=false,activeComponent='SourceBindings',activeViewport=null;
function check(name,condition,detail=null){const r={name,result:condition?'PASS':'FAIL',component:activeComponent,viewport:activeViewport,seconds:(Date.now()-started)/1000,detail};assertions.push(r);console.log(`${r.result} ${name}${detail===null?'':` ${JSON.stringify(detail)}`}`);if(!condition&&!collectRuntimeFailures)throw new Error(name);}
function saveReport(){report.finished_utc=new Date().toISOString();report.seconds=(Date.now()-started)/1000;fs.writeFileSync(path.join(OUTPUT,'FOCUSED-CURRENT-NOTES-RESULT.json'),JSON.stringify(report,null,2)+'\n');}
function listingRecords(raw,tree=false){return raw.split('\0').filter(Boolean).map(r=>{const [meta,p]=r.split('\t');const fields=meta.split(' ');return [p,fields[0],tree?fields[2]:fields[1],tree?'0':fields[2]].join('\t');}).sort();}
function assertBindings(){
 check('HEAD equals explicitly provided combined transport/UI candidate',git('rev-parse','HEAD').trim()===EXPECTED_HEAD);
 check('committed candidate tree equals validated4b2a706 combined source',git('rev-parse',EXPECTED_HEAD+'^{tree}').trim()===STAGED_TREE);
 check('candidate app subtree equals validated43838a combined source',git('rev-parse',EXPECTED_HEAD+':chicago/4d').trim()===EXPECTED_APP);
 check('actual index equals validated candidate tree without index writes',JSON.stringify(listingRecords(git('ls-files','--stage','-z')))===JSON.stringify(listingRecords(git('ls-tree','-rz',STAGED_TREE),true)));
 check('no unstaged tracked source changes',git('diff','--name-only').trim()==='');
 const expectedPaths=OWNED_FILES.map(r=>r.path).sort();
 check('candidate changes exactly four owned CSS docs entry paths',JSON.stringify(git('diff','--cached','--name-only',BASE).trim().split('\n').sort())===JSON.stringify(expectedPaths));
 for(const f of OWNED_FILES)check('owned file remains pinned: '+f.path,sha(read(path.join(REPO,f.path)))===f.sha256);
 check('canonical smoke and current notes source remain pinned',sha(read(path.join(APP,'tools/smoke_renderer.mjs')))===CANONICAL_SMOKE_SHA&&sha(read(path.join(APP,'renderers/web/js/changelog.js')))===NOTES_SHA);
 const CSS_GROUP="/* T-3125: a long URL in one release must not set every row's minimum width.\n   Keep each nested grid inside the panel and wrap intact text when needed. */\n.wn-list, .wn-entry, .wn-items {\n  min-width: 0;\n  grid-template-columns: minmax(0, 1fr);\n  overflow-wrap: anywhere;\n}\n";
 const css=read(path.join(APP,'renderers/web/css/walk.css')).toString();
 check('news CSS insertion occurs exactly once',css.split(CSS_GROUP).length===2);
 const restored=Buffer.from(css.replace(CSS_GROUP,'')),baseCSS=execFileSync('git',['show',BASE+':chicago/4d/renderers/web/css/walk.css'],{cwd:REPO,maxBuffer:16*1024*1024,env:{...process.env,GIT_OPTIONAL_LOCKS:'0'}});
 check('removing exact seven-line news rule recovers base CSS byte-for-byte',sha(restored)===BASE_CSS_SHA&&restored.equals(baseCSS));
 const runtimePaths=['chicago/4d/renderers','chicago/4d/data','chicago/4d/assets','chicago/4d/tools/smoke_renderer.mjs'];
 const withoutCSS=records=>records.filter(r=>!r.startsWith('chicago/4d/renderers/web/css/walk.css\t'));
 const indexRows=withoutCSS(listingRecords(git('ls-files','--stage','-z','--',...runtimePaths)));
 const baseRows=withoutCSS(listingRecords(git('ls-tree','-rz',BASE,'--',...runtimePaths),true));
 check('every other indexed runtime input equals pre-UI merged transport tree5d8c495',JSON.stringify(indexRows)===JSON.stringify(baseRows));
 const expectedTransport=PROTECTED_TRANSPORT.map(x=>[x.path,x.mode,x.blob,'0'].join('\t')).sort();
 const actualTransport=listingRecords(git('ls-files','--stage','-z','--',...PROTECTED_TRANSPORT.map(x=>x.path)));
 check('all52 non-anchor protected transport files retain exact pre-UI blobs',JSON.stringify(actualTransport)===JSON.stringify(expectedTransport));
 const anchor=JSON.parse(read(path.join(APP,'changelog.d/T-3083.json')));
 check('transport anchor retains original title kind and all three items plus exactly one UI item',JSON.stringify(Object.keys(anchor).sort())===JSON.stringify(Object.keys(ORIGINAL_TRANSPORT_ANCHOR).sort())&&anchor.title===ORIGINAL_TRANSPORT_ANCHOR.title&&anchor.kind===ORIGINAL_TRANSPORT_ANCHOR.kind&&anchor.items.length===ORIGINAL_TRANSPORT_ANCHOR.items.length+1&&JSON.stringify(anchor.items.slice(0,-1))===JSON.stringify(ORIGINAL_TRANSPORT_ANCHOR.items)&&anchor.items.at(-1)===EXPECTED_UI_ITEM);
 check('single pending changelog entry remains the group anchor',JSON.stringify(fs.readdirSync(path.join(APP,'changelog.d')).filter(x=>x.endsWith('.json')).sort())===JSON.stringify(['T-3083.json']));
}
function manifest(root){const files=[];const walk=dir=>{for(const e of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.isFile()){const b=read(p);files.push({path:path.relative(root,p),bytes:b.length,sha256:sha(b)});}else throw new Error('Unexpected published symlink/non-file '+p);}};walk(root);return files;}
const indexBefore=sha(read(path.join(REPO,'.git/index')));
let server=null, activeBrowser=null, beforePublished=null, finalBindingsVerified=false;
try{
 const gate=JSON.parse(read(PREFLIGHT_PREFIX+'.result.json'));
 const gateCleanup=JSON.parse(read(PREFLIGHT_PREFIX+'.cleanup.json'));
 check('actual fresh UI preflight belongs to this clone and owned cleanup completed',gate.cwd===APP&&gate.command.some(x=>String(x).endsWith('tools/preflight.sh'))&&gateCleanup.cleanup_complete===true&&Array.isArray(gateCleanup.remaining_owned_children)&&gateCleanup.remaining_owned_children.length===0,{cwd:gate.cwd,command:gate.command,cleanup_complete:gateCleanup.cleanup_complete,remaining:gateCleanup.remaining_owned_children});
 report.preflight_receipt_sha256=sha(read(PREFLIGHT_PREFIX+'.result.json'));report.preflight_cleanup_sha256=sha(read(PREFLIGHT_PREFIX+'.cleanup.json'));
 check('full preflight completed successfully before this explicit launch',gate.returncode===0&&gate.timed_out===false,{returncode:gate.returncode,timed_out:gate.timed_out});
 assertBindings();
 const publishedBuild=JSON.parse(read(path.join(SITE,'build.json')));
 const expectedVersion=git('rev-parse','--short',EXPECTED_HEAD).trim();
 check('published build.version equals the provided expectedHEAD',publishedBuild.version===expectedVersion,{expected_head:EXPECTED_HEAD,expectedVersion,publishedBuild});report.published_build=publishedBuild;
 const stateSource=read(path.join(APP,'tools/dev-smoke-state.mjs')).toString();
 const array=name=>{const m=stateSource.match(new RegExp('const '+name+' = (\\[[\\s\\S]*?\\]);'));if(!m)throw new Error('Missing canonical hash array '+name);return vm.runInNewContext(m[1]);};
 const inputRows=git('ls-files','-s','--',...array('SMOKE_INPUTS')), notesRows=git('ls-files','-s','--',...array('CHANGELOG_INPUTS'));
 check('current notes index digest remains exact combined2257 notes',sha(Buffer.from(notesRows))==='94ac276fecbcf37bd03536fd445e122188c7d8262d8007954709337a60090f7f');
 const normalizedPage=read(path.join(SITE,'walk/index.html')).toString().replace(/build\s+[0-9a-f]{6,}\s+·[^<\n]*/g,'build <stamp>');
 report.hash_binding={actual_source_index_listing_sha256:sha(Buffer.from(inputRows)),notes_index_sha256:sha(Buffer.from(notesRows)),actual_present_mirror_broad_sha256:sha(Buffer.from(inputRows+'\nsite/4d/walk/index.html\n'+normalizedPage)),normalized_published_page_sha256:sha(Buffer.from(normalizedPage)),source_CSS_changed:true,limitation:'The single news CSS runtime input changed. No unchanged whole broad hash is asserted. Exact old CSS preservation and all other runtime inputs are checked independently; actual published digest is recorded with the real mirror.'};
 const sourceBytes=read(path.join(APP,'renderers/web/js/changelog.js'));
 const source=await import('data:text/javascript;base64,'+sourceBytes.toString('base64'));
 const feed=source.CHANGELOG, newest=feed[0], versions=feed.map(e=>e.v);
 check('actual source newest release is2257 and has predecessor2256',source.LATEST_VERSION===2257&&newest.v===2257&&feed.some(e=>e.v===2256),{newest});
 report.source_newest=newest;report.feed_release_count=feed.length;report.actual_versions=versions;
 const {WALK_SHIM}=await import(pathToFileURL(path.join(APP,'tools/changelog_shim.mjs')).href);
 check('published fleet changelog bytes equal actual source',read(path.join(SITE,'js/changelog.js')).equals(sourceBytes));
 check('published walk file equals canonical re-export stub',read(path.join(SITE,'walk/js/changelog.js')).equals(Buffer.from(WALK_SHIM)));
 beforePublished=manifest(SITE);fs.writeFileSync(path.join(OUTPUT,'PUBLISHED-MANIFEST-BEFORE.json'),JSON.stringify(beforePublished,null,2)+'\n');
 report.published_manifest_digest=sha(Buffer.from(JSON.stringify(beforePublished)));report.published_files=beforePublished.length;
 const MIME={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.wasm':'application/wasm','.glb':'model/gltf-binary','.gltf':'model/gltf+json','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml','.webp':'image/webp','.ico':'image/x-icon','.woff2':'font/woff2','.bin':'application/octet-stream'};
 server=http.createServer((req,res)=>{try{let requested=decodeURIComponent(new URL(req.url,'http://localhost').pathname);let file=path.resolve(SITE,'.'+requested);if(file!==SITE&&!file.startsWith(SITE+path.sep)){res.writeHead(403);res.end();return;}if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');if(!fs.existsSync(file)){res.writeHead(404);res.end('not found');return;}res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);}catch{res.writeHead(400);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`, entry=origin+'/walk/?year=1835&keep-geometry=1';
 let pw;try{pw=await import('playwright');}catch{const root=(process.env.NODE_PATH||execFileSync('npm',['root','-g'],{encoding:'utf8'})).trim().split(path.delimiter)[0];pw=await import(pathToFileURL(path.join(root,'playwright/index.js')).href);}const {chromium}=pw.chromium?pw:pw.default;
 for(const [label,viewport,touch] of [['mobile390x780',{width:390,height:780},true],['desktop1280x800',{width:1280,height:800},false]]){
  const v={label,viewport,hasTouch:touch,started_utc:new Date().toISOString(),errors:[],network:[],screenshots:[],boots:[]};viewportResults.push(v);const viewStart=Date.now();
  activeViewport=label;activeComponent='CanonicalNewsFlow';collectRuntimeFailures=true;
  let diagnosticPage=null;
  const captureFailure=async(p,stem)=>{
   if(!p)return;
   const record={stage:stem,at_seconds:(Date.now()-viewStart)/1000};
   try{record.dom=await p.evaluate(()=>{
    const name=el=>!el?null:`${el.tagName.toLowerCase()}${el.id?'#'+el.id:''}${typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''}`;
    const rect=el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
    const detail=el=>{if(!el)return null;const c=getComputedStyle(el);let a=el.parentElement,scroll=null;while(a){const x=getComputedStyle(a);if(['auto','scroll','hidden','clip'].includes(x.overflowX)||['auto','scroll','hidden','clip'].includes(x.overflowY)){scroll={element:name(a),rect:rect(a),clientWidth:a.clientWidth,scrollWidth:a.scrollWidth,clientHeight:a.clientHeight,scrollHeight:a.scrollHeight,overflowX:x.overflowX,overflowY:x.overflowY};break;}a=a.parentElement;}return {element:name(el),rect:rect(el),clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,clientHeight:el.clientHeight,scrollHeight:el.scrollHeight,hidden:el.hidden,hiddenAncestor:name(el.closest('[hidden]')),display:c.display,visibility:c.visibility,transform:c.transform,position:c.position,overflowX:c.overflowX,overflowY:c.overflowY,width:c.width,minWidth:c.minWidth,maxWidth:c.maxWidth,gridTemplateColumns:c.gridTemplateColumns,paddingLeft:c.paddingLeft,paddingRight:c.paddingRight,zoom:c.zoom,whiteSpace:c.whiteSpace,overflowWrap:c.overflowWrap,wordBreak:c.wordBreak,closestScrollParent:scroll};};
    const selectors=['#navigator','#nav-app-settings','#panel','.panel-scroll','.panel-body[data-panel="whatsnew"]','#whatsnew','.wn-list'];
    return {viewport:{width:innerWidth,height:innerHeight},journey:document.documentElement.dataset.journey,subtab:window.__chicago4d?.hud?.tab,navApp:window.__chicago4d?.navigator?.app,navLevel:window.__chicago4d?.navigator?.level,selectedTabs:[...document.querySelectorAll('#panel .panel-tab[aria-selected="true"]')].map(x=>({tab:x.dataset.tab,hidden:x.hidden})),entries:document.querySelectorAll('#whatsnew .wn-entry').length,hostBusy:document.getElementById('whatsnew')?.getAttribute('aria-busy'),hostTextStart:document.getElementById('whatsnew')?.textContent.slice(0,160),nodes:selectors.map(selector=>({selector,...detail(document.querySelector(selector))}))};
   });}catch(e){record.dom_error=cleanText(e.message||e);}
   try{const filename=`${label}-${stem}-FAILURE.png`;await p.screenshot({path:path.join(OUTPUT,filename)});record.screenshot=filename;v.screenshots.push(filename);}catch(e){record.screenshot_error=cleanText(e.message||e);}
   (v.failure_diagnostics??=[]).push(record);fs.writeFileSync(path.join(OUTPUT,`${label}-${stem}-DIAGNOSTIC.json`),JSON.stringify(record,null,2)+'\n');
  };
  try{
   activeBrowser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--enable-unsafe-swiftshader']});
   const ctx=await activeBrowser.newContext({viewport,hasTouch:touch,isMobile:false,deviceScaleFactor:touch?2:1});const page=await ctx.newPage();diagnosticPage=page;page.setDefaultTimeout(90_000);
   const newsRequests=[];page.on('request',r=>{if(/\/js\/changelog\.js$/.test(new URL(r.url()).pathname))newsRequests.push({path:new URL(r.url()).pathname,at_seconds:(Date.now()-viewStart)/1000});});
   page.on('pageerror',e=>v.errors.push('pageerror: '+cleanText(e.message||e)));page.on('response',r=>{if(r.status()>=400)v.errors.push(`HTTP ${r.status()} ${cleanUrl(r.url())}`);if(/\/js\/changelog\.js$/.test(new URL(r.url()).pathname))v.network.push({path:new URL(r.url()).pathname,status:r.status()});});page.on('requestfailed',r=>{const why=r.failure()?.errorText||'';if(!/ERR_ABORTED/.test(why))v.errors.push(`request failed (${cleanText(why)}) ${cleanUrl(r.url())}`);});page.on('console',m=>{if(m.type()==='error'&&!m.text().startsWith('Failed to load resource'))v.errors.push('console.error: '+cleanText(m.text()));});
  const clickChrome = async (sel) => {
    const why = await page.evaluate(async (s) => {
      const el = document.querySelector(s);
      if (!el) return `nothing matches ${s}`;
      if (el.disabled) return `${s} is disabled`;
      // T-0701: the drawer SLIDES. `#panel[hidden]` keeps its layout and sits at
      // translateX(102%), and opening it is a .24 s transform — so for a quarter
      // of a second after `setPanel(true)` a tab has a real box whose centre is
      // off the right edge of the viewport, and `elementFromPoint` answers
      // `null` for it. A visitor clicks a drawer that has arrived; so does this.
      // Waited for, never assumed: the hit-test below still runs on the settled
      // box, and a control that is genuinely covered still fails here.
      const drawer = el.closest('#panel');
      if (drawer) {
        for (let i = 0; i < 40 && getComputedStyle(drawer).transform !== 'none'; i++) {
          await new Promise((r) => setTimeout(r, 50));
        }
      }
      // The Navigator WIDENS too. On a desktop its open is a .28 s width transition from
      // the 58 px rail to 400 px, and the transition's clock only moves when the page gets
      // to draw; on a runner where a frame of the town takes seconds, a fixed wait can end
      // with the panel still a sliver. T-2622's keyboard check ends on Escape (the panel
      // collapsed to its rail) and T-2630's opens it and clicks Home's Go to after 400 ms:
      // "covered at its own centre by <button class=\"nav-choice\">". Waited for the same
      // way as the drawer: the hit-test still runs, on the settled box.
      const device = el.closest('#navigator');
      if (device?.getAnimations) {
        for (let i = 0; i < 60 && device.getAnimations().some((a) => a.playState === 'running'); i++) {
          await new Promise((r) => setTimeout(r, 50));
        }
      }
      // The same scroll `page.click` would do, in the same round trip as the
      // reading — a result row far down the Go-to list is off the panel's
      // viewport until this runs, and `elementFromPoint` would then answer for
      // whatever is at those coordinates instead.
      el.scrollIntoView({ block: 'center', inline: 'center' });
      const b = el.getBoundingClientRect();
      if (b.width < 1 || b.height < 1) {
        return `${s} has no box (${Math.round(b.width)}x${Math.round(b.height)})`;
      }
      const top = document.elementFromPoint(b.x + b.width / 2, b.y + b.height / 2);
      if (!top || !(top === el || el.contains(top))) {
        const cls = top && typeof top.className === 'string' ? top.className : '';
        // NAME THE OVERLAY, NOT JUST THE TAG IT ENDS IN (T-0369). The first
        // report of this failure said only `<h2>`, and an `<h2>` is a heading
        // inside something — the thing worth naming is the panel that heading
        // belongs to. Walking up to the nearest ancestor carrying an id turns
        // "covered by <h2>" into "covered by <h2> inside #popup", which is the
        // whole diagnosis of a stale overlay left open by an earlier stage.
        let owner = top;
        while (owner && !owner.id && owner !== document.body) owner = owner.parentElement;
        const inside = owner && owner.id && owner !== el ? ` inside #${owner.id}` : '';
        // T-2620: the Navigator covers chrome only when it is open; say which height it was at.
        const nav = top?.closest?.('#navigator');
        const at = nav ? ` (Navigator ${nav.dataset.detent}, app ${window.__chicago4d?.navigator?.app ?? '?'})` : '';
        return `${s} is covered at its own centre by `
          + `<${top ? top.tagName.toLowerCase() : 'nothing'}${cls ? ` class="${cls}"` : ''}>${inside}${at}`;
      }
      // A real mouse press FOCUSES a focusable control, and an untrusted
      // `.click()` does not — which is a difference the suite already depends on
      // and which this helper got wrong on its first run, honestly and visibly.
      // Part 8 closes the panel and then presses `g`, and `g` only reaches the
      // window shortcut if focus has left the Go-to search box first: the shared
      // `isTyping(e.target)` guard swallows it otherwise, which is the whole
      // point of that guard. Without this line the panel stayed shut, `g` did
      // nothing, and the next reading was a result row with a 0x0 box. So this
      // is fidelity to the click being replaced, not a convenience.
      if (typeof el.focus === 'function') el.focus({ preventScroll: true });
      el.click();
      return null;
    }, sel);
    if (why) throw new Error(`clickChrome: ${why}`);
  };
  // T-2620: the drawer and its hamburger are gone; each of the drawer's sections is held by
  // a Navigator app (apps/drawer-host.js). A visitor reaches one by the app's rail icon —
  // on a phone the rail shows once the sheet is open, so the handle comes first — and,
  // where the app holds two sections, by the section's own tab. Each is a hit-tested click.
  const SECTION_APP = { travel: 'move', people: 'people', businesses: 'people',
    controls: 'guide', evidence: 'guide', settings: 'settings', whatsnew: 'settings' };
  const openSection = async (tab) => {
    const opened = () => page.waitForFunction(() => {
      const r = document.getElementById('navigator')?.getBoundingClientRect();
      return r && (innerWidth > 620 ? r.width >= 380 : r.height >= innerHeight * 0.4);
    }, null, { timeout: 60_000, polling: 100 });
    if (touch && await page.evaluate(() => window.__chicago4d.navigator?.level === 0)) {
      await clickChrome('#nav-grip');
      await opened();
    }
    await clickChrome(`#nav-rail [data-app="${SECTION_APP[tab]}"]`);
    await opened();
    await page.waitForFunction(() => { const p = document.getElementById('panel'); return p && !p.hidden && !!p.closest('.nav-screen:not([hidden])'); },
      null, { timeout: 60_000, polling: 100 });
    if (await page.evaluate(() => window.__chicago4d.hud.tab) !== tab) await clickChrome(`.panel-tab[data-tab="${tab}"]`);
  };
  // T-2613: Home appears halfway through the landing's flip, not at ready (the old
  // #gate-btn sat on screen at ready), so a click on #home-roam waits for the journey
  // to land. Bounded, and loud: a landing that never comes fails here by name, with
  // the journey state and the landing phase it stopped in.
  const untilLanded = async (timeout = 90_000) => {
    try {
      await page.waitForFunction(() => document.documentElement.dataset.journey === 'landed',
        null, { timeout, polling: 100 });
    } catch {
      const at = await page.evaluate(() => ({
        journey: document.documentElement.dataset.journey ?? '(none)',
        landing: document.querySelector('.gate-card')?.dataset.landing ?? '(none)',
        gate: document.getElementById('gate')?.dataset.state ?? '(none)',
      })).catch(() => ({}));
      throw new Error(`the landing never reached "landed" within ${timeout / 1000} s after ready — `
        + `journey ${at.journey}, landing phase ${at.landing}, gate ${at.gate}`);
    }
  };

   const bootReady=()=>page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:240_000,polling:1000});
   const boot=async(reload=false)=>{const t=Date.now();if(reload)await page.reload({waitUntil:'domcontentloaded'});else await page.goto(entry,{waitUntil:'domcontentloaded'});await bootReady();await untilLanded();await clickChrome('#home-roam');await page.waitForTimeout(150);await page.evaluate(()=>document.exitPointerLock?.());await page.waitForFunction(()=>document.getElementById('gate')?.hasAttribute('hidden'),null,{timeout:90_000,polling:100});if(await page.evaluate(()=>{const h=document.getElementById('control-help');return !!h&&!h.hasAttribute('hidden');}))await clickChrome('#control-help-gotit');v.boots.push({reload,seconds:(Date.now()-t)/1000,journey:await page.evaluate(()=>document.documentElement.dataset.journey)});};
   const dots=()=>page.evaluate(()=>({chip:!document.getElementById('help-dot')?.hasAttribute('hidden'),tab:!document.getElementById('whatsnew-dot')?.hasAttribute('hidden')}));
   const waitFeed=async()=>{const t=Date.now(),reading={ready:false};await page.waitForFunction(()=>document.querySelector('#whatsnew .wn-entry')&&document.getElementById('help-dot')?.hasAttribute('hidden'),null,{timeout:20_000,polling:100}).then(()=>{reading.ready=true;}).catch(()=>{});reading.seconds=(Date.now()-t)/1000;reading.wait_rejected=!reading.ready;reading.canonical_empty_catch=true;(v.feed_waits??=[]).push(reading);return reading;};
   const snapshot=()=>page.evaluate(()=>{const host=document.getElementById('whatsnew');return {rows:[...host.querySelectorAll('.wn-entry')].map(el=>({title:el.querySelector('.wn-title')?.textContent||'',meta:el.querySelector('.wn-meta')?.textContent||'',items:[...el.querySelectorAll('.wn-items li')].map(x=>x.textContent),isNew:el.classList.contains('is-new')})),cleared:document.getElementById('help-dot')?.hasAttribute('hidden')&&document.getElementById('whatsnew-dot')?.hasAttribute('hidden'),seen:localStorage.getItem('chicago4d.whatsnew.seen')};});
   const screenshot=async name=>{const file=`${label}-${name}.png`;await page.screenshot({path:path.join(OUTPUT,file)});v.screenshots.push(file);};
   const layout=async name=>{
    const result=await page.evaluate(()=>{
     const s=document.querySelector('#nav-app-settings');if(!s||s.hidden)return {error:'no shown Settings/news screen'};
     const box=s.getBoundingClientRect();const hidden=el=>el.closest('.visually-hidden, [aria-hidden="true"]');const all=[...s.querySelectorAll('*')].filter(el=>el.getClientRects().length&&!hidden(el));
     const name=el=>`${el.tagName.toLowerCase()}${el.id?'#'+el.id:''}${typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''}`;
     const past=all.filter(el=>{const r=el.getBoundingClientRect();return r.width>0&&(r.right>box.right+1||r.left<box.left-1);});
     const cut=all.filter(el=>{if(!el.textContent.trim())return false;const cs=getComputedStyle(el);if(['auto','scroll'].includes(cs.overflowX)||['auto','scroll'].includes(cs.overflowY))return false;if(cs.overflowX==='visible'&&cs.overflowY==='visible'&&cs.textOverflow!=='ellipsis')return false;return el.scrollWidth>el.clientWidth+1||el.scrollHeight>el.clientHeight+2;});
     const strips=[s,...all].filter(el=>!el.matches('.insp-swipe')&&['auto','scroll'].includes(getComputedStyle(el).overflowX)&&el.scrollWidth>el.clientWidth+1);
     const rect=el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
     const detail=el=>{const c=getComputedStyle(el);let a=el.parentElement,scroll=null;while(a){const x=getComputedStyle(a);if(['auto','scroll','hidden','clip'].includes(x.overflowX)||['auto','scroll','hidden','clip'].includes(x.overflowY)){scroll={element:name(a),rect:rect(a),clientWidth:a.clientWidth,scrollWidth:a.scrollWidth,clientHeight:a.clientHeight,scrollHeight:a.scrollHeight,overflowX:x.overflowX,overflowY:x.overflowY};break;}a=a.parentElement;}return {element:name(el),rect:rect(el),clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,clientHeight:el.clientHeight,scrollHeight:el.scrollHeight,hiddenAncestor:el.closest('[hidden]')?name(el.closest('[hidden]')):null,display:c.display,visibility:c.visibility,transform:c.transform,width:c.width,minWidth:c.minWidth,gridTemplateColumns:c.gridTemplateColumns,overflowX:c.overflowX,overflowY:c.overflowY,whiteSpace:c.whiteSpace,overflowWrap:c.overflowWrap,wordBreak:c.wordBreak,closestScrollParent:scroll,textStart:el.textContent.slice(0,120)};};
     return {scale:getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim(),stored:JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').textScale,subtab:window.__chicago4d?.hud?.tab,screen:{left:box.left,right:box.right,width:box.width},past_count:past.length,cut_count:cut.length,strips_count:strips.length,past_first8:past.slice(0,8).map(detail),cut_first8:cut.slice(0,8).map(detail),strips_first8:strips.slice(0,8).map(detail)};
    });
    v[name]=result;const pass=!result.error&&result.past_count===0&&result.cut_count===0&&result.strips_count===0;
    if(!pass)await captureFailure(page,name+'-layout');
    check(`${label}: ${name} no horizontal overflow or clipped text`,pass,result);
   };
   await boot();check(`${label}: no changelog network import before first notes open`,newsRequests.length===0,newsRequests);
   const meta=await page.evaluate(()=>document.querySelector('meta[name="c4d-releases"]')?.content||'');const decoded=[];for(const part of meta.split(',')){const m=/^(\d+)(?:-(\d+))?$/.exec(part.trim());if(!m)throw new Error('Invalid release meta '+meta);const lo=Number(m[1]),hi=m[2]?Number(m[2]):lo;if(hi<lo)throw new Error('Descending release meta');for(let n=lo;n<=hi;n++)decoded.push(n);}check(`${label}: published releases meta equals actual source versions`,JSON.stringify(decoded.sort((a,b)=>a-b))===JSON.stringify([...versions].sort((a,b)=>a-b)),{meta,count:decoded.length});
   const unread=await dots();check(`${label}: canonical1 first-time visitor has both unread dots`,unread.chip&&unread.tab,unread);
   await openSection('whatsnew');await waitFeed();const first=await snapshot();const firstNewest=first.rows[0]||{title:'',meta:'',items:[]};v.first={entries:first.rows.length,items:first.rows.reduce((s,r)=>s+r.items.length,0),seen:first.seen,newest:firstNewest};
   check(`${label}: canonical2 feed renders every release`,first.rows.length>=5&&first.rows.reduce((s,r)=>s+r.items.length,0)>=first.rows.length,v.first);
   check(`${label}: canonical3 newest entry has title and CT date`,firstNewest.title.length>4&&/CT$/.test(firstNewest.meta),firstNewest);
   check(`${label}: canonical4 opening clears both dots and stores seen`,first.cleared&&Number(first.seen)>0,{cleared:first.cleared,seen:first.seen});
   check(`${label}: canonical5 first visit has no is-new flags`,first.rows.every(r=>!r.isNew));
   check(`${label}: exact source2257 title items and date rendered`,firstNewest.title===newest.title&&JSON.stringify(firstNewest.items)===JSON.stringify(newest.items)&&firstNewest.meta.endsWith(newest.date)&&Number(first.seen)===source.LATEST_VERSION,firstNewest);
   check(`${label}: complete feed titles/items match actual source in order`,first.rows.length===feed.length&&first.rows.every((r,i)=>r.title===feed[i].title&&JSON.stringify(r.items)===JSON.stringify(feed[i].items||[])));
   v.first_open_lazy_responses=v.network.slice();check(`${label}: real first notes open fetched both re-export chain URLs before diagnostic imports`,['/walk/js/changelog.js','/js/changelog.js'].every(p=>v.first_open_lazy_responses.some(r=>r.path===p&&r.status===200)),v.first_open_lazy_responses);
   const modules=await page.evaluate(async()=>{const a=await import('/walk/js/changelog.js'),b=await import('/js/changelog.js');return {sameArray:a.CHANGELOG===b.CHANGELOG,sameLatest:a.LATEST_VERSION===b.LATEST_VERSION,latest:a.LATEST_VERSION,count:a.CHANGELOG.length};});check(`${label}: actual lazy re-export chain returns identical feed exports`,modules.sameArray&&modules.sameLatest&&modules.latest===source.LATEST_VERSION&&modules.count===feed.length,modules);check(`${label}: both lazy import URLs succeeded`,['/walk/js/changelog.js','/js/changelog.js'].every(p=>v.network.some(r=>r.path===p&&r.status===200)),v.network);
   await page.evaluate(()=>localStorage.setItem('chicago4d.whatsnew.seen','3'));await boot(true);await openSection('whatsnew');await waitFeed();const ret=await snapshot(),flagged=ret.rows.filter(r=>r.isNew).map(r=>r.title),expected=feed.filter(e=>e.v>3).map(e=>e.title);v.returning_seen3={total:ret.rows.length,flagged:flagged.length,expected:expected.length,seen_after:ret.seen};check(`${label}: canonical6 returning seen3 flags exactly every subsequent release`,flagged.length===ret.rows.length-3&&flagged.length>0&&JSON.stringify(flagged)===JSON.stringify(expected)&&ret.cleared&&Number(ret.seen)===source.LATEST_VERSION,v.returning_seen3);
   await page.evaluate(()=>localStorage.setItem('chicago4d.whatsnew.seen','2256'));await boot(true);const beforeAbout=await dots();check(`${label}: seen2256 sees both unread dots for2257`,beforeAbout.chip&&beforeAbout.tab,beforeAbout);await openSection('whatsnew');await waitFeed();
   const delta=await snapshot();const just=delta.rows.filter(r=>r.isNew);v.returning_seen2256={flagged:just,seen_after:delta.seen,cleared:delta.cleared};check(`${label}: seen2256 flags only actual2257 and clears unread state`,just.length===1&&just[0].title===newest.title&&JSON.stringify(just[0].items)===JSON.stringify(newest.items)&&just[0].meta.endsWith(newest.date)&&Number(delta.seen)===2257&&delta.cleared,v.returning_seen2256);
   check(`${label}: news flow has zero page console HTTP and request errors`,v.errors.length===0,v.errors);
   const flowChecks=assertions.filter(r=>r.viewport===label&&r.component==='CanonicalNewsFlow'),canonicalChecks=flowChecks.filter(r=>/\bcanonical[1-6]\b/.test(r.name));
   v.canonical_news_flow={completed:true,result:flowChecks.every(r=>r.result==='PASS')&&canonicalChecks.length===6?'PASS':'FAIL',canonical_checks:canonicalChecks.length,assertions:flowChecks.length,errors_at_completion:[...v.errors]};
   activeComponent='CurrentNotesPresentation';
   await openSection('settings');check(`${label}: actual Settings About news link exists under About`,await page.evaluate(()=>!!document.getElementById('s-open-whatsnew')?.closest('#s-about')));await clickChrome('#s-open-whatsnew');await waitFeed();check(`${label}: Settings About link opens actual news tab`,await page.evaluate(()=>window.__chicago4d.hud.tab==='whatsnew'));
   await layout('normal-news');check(`${label}: normal text size is100percent before preference changes`,v['normal-news'].scale==='1');await screenshot('returning2256-normal');
   await openSection('settings');await page.selectOption('#s-text-size','1.4');await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1.4',null,{timeout:20_000,polling:100});await openSection('whatsnew');await layout('140pct-news');check(`${label}: actual140percent preference applied and stored`,v['140pct-news'].scale==='1.4'&&v['140pct-news'].stored===1.4);await screenshot('returning2256-140pct');await openSection('settings');await page.selectOption('#s-text-size','1');await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1',null,{timeout:20_000,polling:100});check(`${label}: text size restored to100percent and stored`,await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--text-scale').trim()==='1'&&JSON.parse(localStorage.getItem('chicago4d.settings')||'{}').textScale===1));await openSection('whatsnew');
   check(`${label}: zero page console HTTP and request errors`,v.errors.length===0,v.errors);v.result=assertions.filter(r=>r.viewport===label).every(r=>r.result==='PASS')?'PASS':'FAIL';
  }catch(e){if(!v.failure_diagnostics?.length)await captureFailure(diagnosticPage,'other-failure');v.result='FAIL';v.exception=cleanText(e.stack||e);console.error(`${label} FAIL ${v.exception}`);}finally{collectRuntimeFailures=false;activeComponent='SourceBindings';activeViewport=null;v.seconds=(Date.now()-viewStart)/1000;if(activeBrowser){await activeBrowser.close().catch(e=>{v.cleanup_error=cleanText(e);});activeBrowser=null;}}
 }
 activeComponent='OverallRuntime';collectRuntimeFailures=true;check('both required viewport focused proofs passed',viewportResults.length===2&&viewportResults.every(v=>v.result==='PASS'&&!v.cleanup_error),viewportResults.map(v=>({label:v.label,result:v.result,seconds:v.seconds})));
 collectRuntimeFailures=false;activeComponent='SourceBindings';assertBindings();const after=manifest(SITE);fs.writeFileSync(path.join(OUTPUT,'PUBLISHED-MANIFEST-AFTER.json'),JSON.stringify(after,null,2)+'\n');check('published mirror remained byte-identical throughout focused run',JSON.stringify(after)===JSON.stringify(beforePublished));check('real Git index remained byte-identical',sha(read(path.join(REPO,'.git/index')))===indexBefore);finalBindingsVerified=true;report.result=assertions.every(r=>r.result==='PASS')&&viewportResults.length===2&&viewportResults.every(v=>v.result==='PASS')?'PASS':'FAIL';if(report.result==='FAIL')process.exitCode=1;
}catch(e){report.result='FAIL';report.exception=cleanText(e.stack||e);console.error(report.exception);process.exitCode=1;}finally{if(activeBrowser)await activeBrowser.close().catch(()=>{});if(server){server.closeAllConnections?.();await new Promise(r=>server.close(r));}report.index_sha256_before=indexBefore;report.index_sha256_after=sha(read(path.join(REPO,'.git/index')));report.final_bindings_verified=finalBindingsVerified;const sourceOK=finalBindingsVerified&&assertions.filter(r=>r.component==='SourceBindings').every(r=>r.result==='PASS');const finalViewportErrorsVerified=viewportResults.length===2&&viewportResults.every(v=>Array.isArray(v.errors)&&v.errors.length===0&&!v.cleanup_error&&assertions.some(r=>r.viewport===v.label&&r.name===v.label+': zero page console HTTP and request errors'&&r.result==='PASS'));report.final_viewport_errors_verified=finalViewportErrorsVerified;report.components={CanonicalNewsFlow:{result:sourceOK&&finalViewportErrorsVerified&&viewportResults.length===2&&viewportResults.every(v=>v.canonical_news_flow?.completed&&v.canonical_news_flow.result==='PASS')?'PASS':'FAIL',scope:'Only six canonical notes assertions plus source-derived current-entry/meta/lazy/returning flow. Not fullPART13, confidence persistence or global renderer proof.'},CurrentNotesPresentation:{result:sourceOK&&finalViewportErrorsVerified&&viewportResults.length===2&&assertions.some(r=>r.component==='CurrentNotesPresentation')&&viewportResults.every(v=>assertions.some(r=>r.viewport===v.label&&r.component==='CurrentNotesPresentation'))&&assertions.filter(r=>r.component==='CurrentNotesPresentation').every(r=>r.result==='PASS')&&viewportResults.every(v=>!v.exception)?'PASS':'FAIL',scope:'ActualAbout route, unchanged normal/140percent layout predicates, screenshots and final zero errors.'}};saveReport();const files=fs.readdirSync(OUTPUT).filter(n=>fs.statSync(path.join(OUTPUT,n)).isFile()).map(n=>{const b=read(path.join(OUTPUT,n));return{path:n,bytes:b.length,sha256:sha(b)};});fs.writeFileSync(path.join(OUTPUT,'OUTPUT-MANIFEST.json'),JSON.stringify({files},null,2)+'\n');console.log(`${report.result}: COMBINED TRANSPORT/UI FOCUSED WRAPPING ACCEPTANCE ONLY; not a new canonical PART13/full gate; ${(Date.now()-started)/1000}s`);}
