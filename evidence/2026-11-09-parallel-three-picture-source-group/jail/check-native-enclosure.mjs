import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
const own='/tmp/nov9-group-log_jail/chicago/4d';
const full='/tmp/chicago-resume-20261109/chicago/4d';
const web=full+'/renderers/web';
const three=pathToFileURL(web+'/vendor/three-0.185.1/three.module.js').href;
const THREE=await import(three);
const fileURL=n=>pathToFileURL(web+'/js/'+n).href;
const moduleURL=s=>'data:text/javascript;base64,'+Buffer.from(s).toString('base64');
const ownSource=fs.readFileSync(own+'/renderers/web/js/enclosures.js','utf8');
assert.equal(ownSource,fs.readFileSync(web+'/js/enclosures.js','utf8'));
const gpu=moduleURL(fs.readFileSync(web+'/js/gpu-pick.js','utf8').replace("from 'three'",`from '${three}'`).replace("from './compact-streams.js'",`from '${fileURL('compact-streams.js')}'`));
const {createEnclosures}=await import(moduleURL(ownSource.replace("from 'three'",`from '${three}'`).replace("from './gates.js'",`from '${fileURL('gates.js')}'`).replace("from './gpu-pick.js'",`from '${gpu}'`).replace("from './compact-streams.js'",`from '${fileURL('compact-streams.js')}'`)));
const file='data/enclosures/log_jail_palisade.json';
const before=JSON.parse(execFileSync('git',['show','HEAD:chicago/4d/'+file],{cwd:own,encoding:'utf8'}));
const after=JSON.parse(fs.readFileSync(own+'/'+file));
const keeper=JSON.parse(fs.readFileSync(own+'/data/enclosures/log_jail_keeper_link.json'));
let selected;
const previousFetch=globalThis.fetch;
globalThis.fetch=async url=>new Response(JSON.stringify(String(url).endsWith('index.json')?{enclosures:[{id:selected.id,file:'one.json'}]}:selected),{status:200});
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
async function build(record,detail){selected=record;const problems=[];const layer=await createEnclosures({dataBase:new URL('https://fixture.invalid/data/'),terrain:{surfaceHeight:()=>0,isWater:()=>false},detail,problems});assert.deepEqual(problems,[]);layer.group.updateMatrixWorld(true);return layer;}
function snapshot(layer){const rows=[];let n=0;layer.group.traverse(o=>{if(!o.isMesh)return;const p=o.geometry.getAttribute('position');const positions=[];for(let i=0;i<p.count;i++){const v=new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld);positions.push(v.x,v.y,v.z);}const attrs={};for(const [name,a] of Object.entries(o.geometry.attributes))if(name!=='position')attrs[name]=hash(Buffer.from(a.array.buffer,a.array.byteOffset,a.array.byteLength));rows.push({positions,attrs,material:{color:o.material.color.getHex(),roughness:o.material.roughness},vertices:p.count});n+=p.count;});return {rows,n,census:{...layer.census},bounds:new THREE.Box3().setFromObject(layer.group)};}
const coreBytes=fs.readFileSync(full+'/assets/gltf/log_jail__log_1833.glb');const jsonLength=coreBytes.readUInt32LE(12);const doc=JSON.parse(coreBytes.subarray(20,20+jsonLength).toString());const binStart=20+jsonLength+8;
function accessor(i){const a=doc.accessors[i],v=doc.bufferViews[a.bufferView];const comps={SCALAR:1,VEC3:3}[a.type];const componentSize={5123:2,5125:4,5126:4}[a.componentType];assert(comps&&componentSize);const start=binStart+(v.byteOffset??0)+(a.byteOffset??0),stride=v.byteStride??comps*componentSize;const rows=[];for(let n=0;n<a.count;n++){const row=[];for(let k=0;k<comps;k++){const off=start+n*stride+k*componentSize;row.push(a.componentType===5126?coreBytes.readFloatLE(off):a.componentType===5123?coreBytes.readUInt16LE(off):coreBytes.readUInt32LE(off));}rows.push(row);}return rows;}
const roof=[];
for(const p of doc.meshes[0].primitives){if(doc.materials[p.material].name!=='roof_board')continue;const positions=accessor(p.attributes.POSITION);const indices=p.indices===undefined?positions.map((_,i)=>i):accessor(p.indices).map(r=>r[0]);for(let i=0;i<indices.length;i+=3){const vs=indices.slice(i,i+3).map(j=>new THREE.Vector3(...positions[j]));const c=vs.reduce((a,v)=>a.add(v),new THREE.Vector3()).multiplyScalar(1/3);c.x+=465.51;c.z+=275.87;roof.push(c);}}
assert(roof.length>0);
const eye=new THREE.Vector3(465.51-12,1.7,275.87-18);
function roofOcclusion(layer){let clear=0;for(const target of roof){const ray=new THREE.Raycaster(eye,target.clone().sub(eye).normalize(),0,eye.distanceTo(target)-0.002);if(!ray.intersectObject(layer.group,true).length)clear++;}return {sample_triangles:roof.length,unobstructed_from_held_Gale_eye:clear,scope:'Actual native core roof triangle-centroid rays against native enclosure on the common flat review plane, not image acceptance or actual terrain.'};}
const receipts=[];
try{for(const detail of ['light','balanced','full']){const a=await build(before,detail),b=await build(after,detail);const sa=snapshot(a),sb=snapshot(b);assert.equal(sa.n,sb.n);assert.deepEqual(sa.census,sb.census);assert.equal(sa.rows.length,sb.rows.length);assert(Math.abs(sa.bounds.max.y-3.05)<0.001);assert(Math.abs(sb.bounds.max.y-2.44)<0.001);let maxXZ=0,changedY=0;for(let i=0;i<sa.rows.length;i++){assert.deepEqual(sa.rows[i].attrs,sb.rows[i].attrs);assert.deepEqual(sa.rows[i].material,sb.rows[i].material);for(let j=0;j<sa.rows[i].positions.length;j+=3){maxXZ=Math.max(maxXZ,Math.abs(sa.rows[i].positions[j]-sb.rows[i].positions[j]),Math.abs(sa.rows[i].positions[j+2]-sb.rows[i].positions[j+2]));if(Math.abs(sa.rows[i].positions[j+1]-sb.rows[i].positions[j+1])>.002)changedY++;}}assert(maxXZ<.002);const oldVisibility=roofOcclusion(a),newVisibility=roofOcclusion(b);assert(newVisibility.unobstructed_from_held_Gale_eye>oldVisibility.unobstructed_from_held_Gale_eye);a.dispose();b.dispose();const ka=await build(keeper,detail),kb=await build(keeper,detail);const sk1=snapshot(ka),sk2=snapshot(kb);assert.deepEqual(sk1,sk2);ka.dispose();kb.dispose();receipts.push({detail,vertices:sa.n,census:sa.census,old_height:sa.bounds.max.y,new_height:sb.bounds.max.y,max_abs_world_xz_delta:maxXZ,changed_world_y_vertices:changedY,all_nonposition_attributes_identical:true,material_and_grade_identical:true,keeper_link_exact_control:true,old_roof_visibility:oldVisibility,new_roof_visibility:newVisibility});}}
finally{globalThis.fetch=previousFetch;}
const receipt={status:'PASS_ACTUAL_CONSUMER_HEIGHT_TRIAL_NOT_BROWSER_OR_IMAGE_ACCEPTANCE',renderer_sha256:hash(ownSource),core_master_sha256:hash(coreBytes),old_record_sha256:hash(Buffer.from(execFileSync('git',['show','HEAD:chicago/4d/'+file],{cwd:own}))),new_record_sha256:hash(fs.readFileSync(own+'/'+file)),rows:receipts};fs.writeFileSync('/tmp/nov9-log-jail-group/CONSUMER-PASS.json',JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
