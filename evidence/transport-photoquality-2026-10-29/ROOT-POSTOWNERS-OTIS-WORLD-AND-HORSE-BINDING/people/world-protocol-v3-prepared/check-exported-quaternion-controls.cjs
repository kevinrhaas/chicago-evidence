// Light data-only numerical controls; no browser, renderer, actor or native test.
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict'),path=require('node:path');
const {quaternionMotion}=require('./quaternion-metrics.cjs');
const source='/tmp/chicago-transport-resume-20261029/chicago/4d/assets/humans/bardwell_otis_1835.lod0.glb',raw=fs.readFileSync(source),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(sha(raw),'821d771462b6ff583c27ccc00fbcde3604dc34d24b4512c5d5ba92dba331589f');
const length=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+length)),binary=raw.subarray(28+length),clip=doc.animations.find(c=>c.name==='idle_natural_v1');
const examples=[];for(const channel of clip.channels){const name=doc.nodes[channel.target.node].name;if(!['head','neck_01','spine_02'].includes(name)||channel.target.path!=='rotation')continue;
 const sampler=clip.samplers[channel.sampler],accessor=doc.accessors[sampler.output],view=doc.bufferViews[accessor.bufferView];assert.equal(accessor.componentType,5126);assert.equal(accessor.type,'VEC4');
 const at=i=>Array.from({length:4},(_,k)=>binary.readFloatLE((view.byteOffset||0)+(accessor.byteOffset||0)+i*(view.byteStride||16)+k*4));
 for(let i=0;i<accessor.count;i++){const q=at(i),metric=quaternionMotion(q,q),rawAngle=2*Math.acos(Math.min(1,Math.abs(q.reduce((s,x)=>s+x*x,0))));assert.equal(metric.changed,false);assert.equal(metric.maximumComponentDelta,0);assert.equal(metric.normalizedAngleRadians,0);
  if(rawAngle>1e-7&&examples.length<3)examples.push({bone:name,outputAccessor:sampler.output,sample:i,actualExportedFloat32Quaternion:q,oldRawDotAngleRadians:rawAngle,correctedUnchangedMetric:metric});
 }
 const first=at(0),changed=Array.from({length:accessor.count},(_,i)=>({sample:i,metric:quaternionMotion(first,at(i))})).find(x=>x.metric.changed);assert.ok(changed,`Genuine exported ${name} varying keys detected`);
}
assert.ok(examples.length>0,'A genuine unchanged exported Float32 quaternion exposes old raw-dot false motion');
const result={created_utc:new Date().toISOString(),status:'EXPORTED_FLOAT32_NUMERICAL_NEGATIVE_AND_POSITIVE_CONTROLS_PASS_ONLY',source,source_sha256:sha(raw),old_unchanged_raw_angle_false_positive_examples:examples,changed_exported_head_neck_spine_detected:true,scope:'Data-only controls of observation arithmetic, using genuine pinned exported Float32 values. No browser, world window, native animation rerun, new asset qualification or photographic acceptance.'};
fs.writeFileSync(path.join(__dirname,'EXPORTED-FLOAT32-QUATERNION-CONTROLS.json'),JSON.stringify(result,null,2)+'\n');process.stdout.write(JSON.stringify({status:result.status,unchangedFalsePositiveExamples:examples.length})+'\n');
