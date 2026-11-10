/** Read qualified integrated native/WEB inputs into an external explicit QA pin.
 * This records the parent's qualified provenance; it does not authenticate a bake.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const o=Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
for(const k of ['root','source-sha','native-run','build-prefix','out'])assert(o[k],`--${k} required`);
assert(/^[a-f0-9]{40}$/.test(o['source-sha']));assert(/^\d+$/.test(o['native-run']));
const root=path.resolve(o.root),hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const expected={kind:'EXPLICIT_PARENT_QUALIFIED_NATIVE_AND_PUBLISHED_BUILD_PIN',source_sha:o['source-sha'],native_run:o['native-run'],build_prefix:o['build-prefix'],prepared_from:root,assets:{}};
for(const id of ['cobweb_castle','green_tree_tavern','log_jail','log_jail_keeper_house']){
 const sc=read(`data/sidecars/1835/${id}.json`);assert(sc.id===id&&sc.scene==='1835'&&sc.target_date==='1835-07-01');
 assert(/^gltf\/[^/]+\.glb$/.test(sc.asset));const file=path.join(root,'assets/web',path.basename(sc.asset)),b=fs.readFileSync(file);
 expected.assets[id]={file,bytes:b.length,sha256:hash(b),placement:sc.placement};
}
const cobweb=read('data/sidecars/1835/cobweb_castle.json'),green=read('data/sidecars/1835/green_tree_tavern.json');
assert.equal(cobweb.attributes.compound_clapboard_height_m.value,1.3);assert.equal(green.attributes.enclosed_left_annex.value.shoulder.roof_high_m,4.6);
const enclosureBytes=fs.readFileSync(path.join(root,'data/enclosures/log_jail_palisade.json')),enclosure=JSON.parse(enclosureBytes);
assert.equal(enclosure.form.height_m.value,2.44);assert.equal(enclosure.form.height_m.confidence,'reconstructed');
expected.enclosure_sha256=hash(enclosureBytes);
expected.review_ids=fs.readdirSync(path.join(root,'data/sidecars/1835')).filter(f=>f.endsWith('.json')).map(f=>read(`data/sidecars/1835/${f}`)).filter(d=>d.review_required===true).map(d=>{assert(d.scene==='1835'&&typeof d.id==='string');return d.id;}).sort();
assert.equal(new Set(expected.review_ids).size,expected.review_ids.length);
fs.mkdirSync(path.dirname(path.resolve(o.out)),{recursive:true});fs.writeFileSync(o.out,JSON.stringify(expected,null,2)+'\n');console.log(o.out);
