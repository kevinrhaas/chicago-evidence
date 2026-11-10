/** External final Green Tree B published QA pin. Read only; run after qualified native + publish. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import cp from 'node:child_process';
import {bindPublishedAsset} from '../publisher-binding.mjs';
import {pathToFileURL} from 'node:url';
const opts=Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
for(const key of ['root','published-root','source-sha','native-run','build-prefix','out'])assert(opts[key],`--${key} required`);
assert(/^[a-f0-9]{40}$/.test(opts['source-sha']));assert(/^\d+$/.test(opts['native-run']));
assert(/^[a-f0-9]{40}$/.test(opts['published-source-sha']));assert(/^[a-f0-9]{40}$/.test(opts['native-commit']));
const root=path.resolve(opts.root),published=path.resolve(opts['published-root']);
const targets=JSON.parse(fs.readFileSync(opts.targets??new URL('./targets.json',import.meta.url)));
assert.equal(targets.length,1);assert.equal(targets[0].id,'green_tree_tavern');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const bind=(file)=>{const b=fs.readFileSync(file);return {path:file,bytes:b.length,sha256:hash(b)};};
const exactMirror=(source,mirror)=>{const a=bind(source),b=bind(mirror);assert.equal(a.sha256,b.sha256,`published bytes differ: ${mirror}`);return {source:a,published:b};};
const pinnedBytes=relative=>cp.execFileSync('git',['show',`${opts['published-source-sha']}:chicago/4d/${relative}`],{cwd:root,maxBuffer:32*1024*1024});
const pinned=relative=>JSON.parse(pinnedBytes(relative));
const pinnedMirror=(relative,mirror)=>{const bytes=pinnedBytes(relative),target=bind(mirror);assert.equal(hash(bytes),target.sha256,`actual published bytes differ from immutable source ${relative}`);const stored=path.join(path.dirname(path.resolve(opts.out)),'immutable-published-source',relative);fs.mkdirSync(path.dirname(stored),{recursive:true});fs.writeFileSync(stored,bytes);return {source:bind(stored),published:target,pinned_git:{commit:opts['published-source-sha'],path:`chicago/4d/${relative}`},current_source:bind(path.join(root,relative))};};
const manifest=read('assets/manifest.json'),web=read('assets/manifest.web.json');
const pinnedManifest=pinned('assets/manifest.json'),pinnedWeb=pinned('assets/manifest.web.json');
const build=JSON.parse(fs.readFileSync(path.join(published,'build.json'),'utf8'));
assert(String(build.version).startsWith(opts['build-prefix']),'published build not the explicit parent pin');
const pictures=read('data/pictures/1835.json'),libs=pinned('data/liberties.json'),currentLibs=read('data/liberties.json');
const expected={kind:'FINAL_GREEN_TREE_B_NATIVE_PUBLISHED_AND_ACTUAL_PHOTO_GATE_PIN_NOT_EXECUTED_UI',
 source_sha:opts['source-sha'],published_source_sha:opts['published-source-sha'],native_commit:opts['native-commit'],native_run:opts['native-run'],native_url:`https://github.com/kevinrhaas/chicago/actions/runs/${opts['native-run']}`,
 prepared_from:root,published_root:published,prepared_head:cp.execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),
 build_prefix:opts['build-prefix'],build,targets,assets:{},sidecars:{},pictures:{},liberties:{},manifests:{
 master:bind(path.join(root,'assets/manifest.json')),web:bind(path.join(root,'assets/manifest.web.json'))},
 publishedDocuments:{build:bind(path.join(published,'build.json')),
 pictures:exactMirror(path.join(root,'data/pictures/1835.json'),path.join(published,'data/pictures/1835.json')),
 liberties:pinnedMirror('data/liberties.json',path.join(published,'data/liberties.json'))}};
const assetIds=[...new Set(targets.flatMap(t=>[t.id,...(t.contextAssets??[])]))];
for(const id of assetIds){
 const sidecar=read(`data/sidecars/1835/${id}.json`);assert.equal(sidecar.id,id);assert.equal(sidecar.scene,'1835');assert.equal(sidecar.target_date,'1835-07-01');
 assert(/^gltf\/[^/]+\.glb$/.test(sidecar.asset));const key=path.basename(sidecar.asset);assert.equal(manifest.assets[key]?.structure_id,id);
 assert(web.masters[key],`native WEB manifest entry missing: ${key}`);assert.deepEqual(manifest.assets[key],pinnedManifest.assets[key],'GT master manifest row changed since frozen publish');assert.deepEqual(web.masters[key],pinnedWeb.masters[key],'GT WEB manifest row changed since frozen publish');
 assert(fs.readFileSync(path.join(root,`data/structures/${id}.json`)).equals(pinnedBytes(`data/structures/${id}.json`)),'GT source record changed since frozen publish');assert(fs.readFileSync(path.join(root,`data/sidecars/1835/${id}.json`)).equals(pinnedBytes(`data/sidecars/1835/${id}.json`)),'GT full source sidecar changed since frozen publish');
 const files=await bindPublishedAsset(root,published,path.join(root,'assets/web',key),path.join(published,'data/gltf',key),path.dirname(path.resolve(opts.out)));
 expected.assets[id]={asset:key,master:bind(path.join(root,'assets/gltf',key)),web:files.source,published:files.published,
 masterRegistry:manifest.assets[key],webRegistry:web.masters[key],publisherBinding:files};
 const publishedSidecarPath=path.join(published,`data/sidecars/1835/${id}.json`),publishedSidecar=JSON.parse(fs.readFileSync(publishedSidecarPath));
 for(const field of ['id','phase','scene','target_date','asset','grade','placement','footprint','attributes','citations'])assert.deepEqual(publishedSidecar[field],sidecar[field],`published sidecar invariant differs: ${id}/${field}`);
 expected.sidecars[id]={document:publishedSidecar,source_document:sidecar,files:{source:bind(path.join(root,`data/sidecars/1835/${id}.json`)),published:bind(publishedSidecarPath)}};
}
for(const target of targets){
 const sidecar=expected.sidecars[target.id].document;
 for(const attr of target.requiredAttributes??[])assert(sidecar.attributes[attr]?.value!=null,`final field absent: ${target.id}.${attr}`);
 const liberty=libs.liberties.find(l=>l.id===target.liberty);assert(liberty,`final liberty absent: ${target.liberty}`);
 assert.deepEqual(liberty,currentLibs.liberties.find(l=>l.id===target.liberty),'GT final liberty changed since frozen publish');
 assert(liberty.subjects.includes(target.id),`liberty not bound to target card: ${target.liberty}`);
 const text=JSON.stringify(liberty).toLowerCase();for(const word of target.libertyWords)assert(text.includes(word),`liberty lacks expected text: ${target.liberty}/${word}`);
 expected.liberties[target.id]=liberty;expected.pictures[target.id]=pictures.by_structure[target.id]??[];
}
assert.deepEqual(expected.sidecars.green_tree_tavern.document.attributes.front_upper_layout.value,[.2,.5,.78]);
assert.equal(expected.sidecars.green_tree_tavern.document.attributes.front_upper_layout.confidence,'reconstructed');
const gate=await import(pathToFileURL(path.join(root,'tools/image_gate.mjs')).href);assert.deepEqual(gate.gateFor(['green_tree_tavern']),[],'actual final GT image gate must be fresh/matches');
expected.final_photo_gate=gate.viewsOf('green_tree_tavern').map(v=>({view:v.view,camera:bind(v.cameraFile),match:bind(v.matchFile),record:JSON.parse(fs.readFileSync(v.matchFile))}));
assert.equal(expected.final_photo_gate.length,3);assert(expected.final_photo_gate.every(v=>v.record.verdict==='matches'&&!v.record.differences.some(d=>d.status==='open')));
expected.review_ids=fs.readdirSync(path.join(root,'data/sidecars/1835')).filter(f=>f.endsWith('.json')).map(f=>read(`data/sidecars/1835/${f}`)).filter(d=>d.review_required===true).map(d=>{assert.equal(d.scene,'1835');return d.id;}).sort();
assert.equal(new Set(expected.review_ids).size,expected.review_ids.length);
fs.mkdirSync(path.dirname(path.resolve(opts.out)),{recursive:true});fs.writeFileSync(opts.out,JSON.stringify(expected,null,2)+'\n');
console.log(JSON.stringify({status:'PIN_PREPARED_QA_NOT_RUN',out:opts.out,targets:targets.length,assets:assetIds.length,native_run:expected.native_run,build:expected.build}));
