/** External five-building published QA pin. Read only; run after qualified native + publish. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import cp from 'node:child_process';
const opts=Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
for(const key of ['root','published-root','source-sha','native-run','build-prefix','out'])assert(opts[key],`--${key} required`);
assert(/^[a-f0-9]{40}$/.test(opts['source-sha']));assert(/^\d+$/.test(opts['native-run']));
const root=path.resolve(opts.root),published=path.resolve(opts['published-root']);
const targets=JSON.parse(fs.readFileSync(opts.targets??new URL('./targets.json',import.meta.url)));
assert.equal(targets.length,5);assert.equal(new Set(targets.map(t=>t.id)).size,5);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const bind=(file)=>{const b=fs.readFileSync(file);return {path:file,bytes:b.length,sha256:hash(b)};};
const exactMirror=(source,mirror)=>{const a=bind(source),b=bind(mirror);assert.equal(a.sha256,b.sha256,`published bytes differ: ${mirror}`);return {source:a,published:b};};
const manifest=read('assets/manifest.json'),web=read('assets/manifest.web.json');
const build=JSON.parse(fs.readFileSync(path.join(published,'build.json'),'utf8'));
assert(String(build.version).startsWith(opts['build-prefix']),'published build not the explicit parent pin');
const pictures=read('data/pictures/1835.json'),libs=read('data/liberties.json');
const expected={kind:'PARENT_QUALIFIED_NATIVE_AND_PUBLISHED_FIVE_TARGET_PIN_NOT_EXECUTED_QA',
 source_sha:opts['source-sha'],native_run:opts['native-run'],native_url:`https://github.com/kevinrhaas/chicago/actions/runs/${opts['native-run']}`,
 prepared_from:root,published_root:published,prepared_head:cp.execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),
 build_prefix:opts['build-prefix'],build,targets,assets:{},sidecars:{},pictures:{},liberties:{},manifests:{
 master:bind(path.join(root,'assets/manifest.json')),web:bind(path.join(root,'assets/manifest.web.json'))},
 publishedDocuments:{build:bind(path.join(published,'build.json')),
 pictures:exactMirror(path.join(root,'data/pictures/1835.json'),path.join(published,'data/pictures/1835.json')),
 liberties:exactMirror(path.join(root,'data/liberties.json'),path.join(published,'data/liberties.json'))}};
expected.publishedDocuments.woodpiles=exactMirror(path.join(root,'data/yard/town_woodpiles.json'),path.join(published,'data/yard/town_woodpiles.json'));
expected.cobwebWoodpile=read('data/yard/town_woodpiles.json').lots.find(l=>l.structure_id==='cobweb_castle');assert(expected.cobwebWoodpile);
const assetIds=[...new Set(targets.flatMap(t=>[t.id,...(t.contextAssets??[])]))];
for(const id of assetIds){
 const sidecar=read(`data/sidecars/1835/${id}.json`);assert.equal(sidecar.id,id);assert.equal(sidecar.scene,'1835');assert.equal(sidecar.target_date,'1835-07-01');
 assert(/^gltf\/[^/]+\.glb$/.test(sidecar.asset));const key=path.basename(sidecar.asset);assert.equal(manifest.assets[key]?.structure_id,id);
 assert(web.masters[key],`native WEB manifest entry missing: ${key}`);
 const files=exactMirror(path.join(root,'assets/web',key),path.join(published,'data/gltf',key));
 expected.assets[id]={asset:key,master:bind(path.join(root,'assets/gltf',key)),web:files.source,published:files.published,
 masterRegistry:manifest.assets[key],webRegistry:web.masters[key]};
 const publishedSidecarPath=path.join(published,`data/sidecars/1835/${id}.json`),publishedSidecar=JSON.parse(fs.readFileSync(publishedSidecarPath));
 for(const field of ['id','phase','scene','target_date','asset','grade','placement','footprint','attributes','citations'])assert.deepEqual(publishedSidecar[field],sidecar[field],`published sidecar invariant differs: ${id}/${field}`);
 expected.sidecars[id]={document:publishedSidecar,source_document:sidecar,files:{source:bind(path.join(root,`data/sidecars/1835/${id}.json`)),published:bind(publishedSidecarPath)}};
}
for(const target of targets){
 const sidecar=expected.sidecars[target.id].document;
 for(const attr of target.requiredAttributes??[])assert(sidecar.attributes[attr]?.value!=null,`final field absent: ${target.id}.${attr}`);
 const liberty=libs.liberties.find(l=>l.id===target.liberty);assert(liberty,`final liberty absent: ${target.liberty}`);
 assert(liberty.subjects.includes(target.id),`liberty not bound to target card: ${target.liberty}`);
 const text=JSON.stringify(liberty).toLowerCase();for(const word of target.libertyWords)assert(text.includes(word),`liberty lacks expected text: ${target.liberty}/${word}`);
 expected.liberties[target.id]=liberty;expected.pictures[target.id]=pictures.by_structure[target.id]??[];
}
assert.equal(expected.sidecars.cobweb_castle.document.attributes.compound_clapboard_height_m.value,1.3);
assert.deepEqual(expected.sidecars.cobweb_castle.document.attributes.compound_eave_heights_m.value,[2.6,2,2,2.6,2.6]);
assert.deepEqual(expected.sidecars.cobweb_castle.document.attributes.compound_ridge_stacks.value,[[0,.35,.8]]);
assert.deepEqual(expected.pictures.cobweb_castle.map(p=>p.id).sort(),['kinzie_1857_chicago_1831_panorama','kinzie_waubun_1831_unkeyed_panorama'].sort(),'both actual held-picture source records must reach the card');
assert(expected.pictures.cobweb_castle.every(p=>!p.spot),'illustrative cameras must withhold invented historic spots');
expected.review_ids=fs.readdirSync(path.join(root,'data/sidecars/1835')).filter(f=>f.endsWith('.json')).map(f=>read(`data/sidecars/1835/${f}`)).filter(d=>d.review_required===true).map(d=>{assert.equal(d.scene,'1835');return d.id;}).sort();
assert.equal(new Set(expected.review_ids).size,expected.review_ids.length);
fs.mkdirSync(path.dirname(path.resolve(opts.out)),{recursive:true});fs.writeFileSync(opts.out,JSON.stringify(expected,null,2)+'\n');
console.log(JSON.stringify({status:'PIN_PREPARED_QA_NOT_RUN',out:opts.out,targets:targets.length,assets:assetIds.length,native_run:expected.native_run,build:expected.build}));
