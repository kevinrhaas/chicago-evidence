import * as T from '/workspace/chicago-waistcoat/chicago/4d/renderers/web/vendor/three-0.185.1/three.module.js';
import fs from 'node:fs';import assert from 'node:assert/strict';
const here=new URL('.',import.meta.url),j=JSON.parse(fs.readFileSync(new URL('MOBILE-FRAMING.json',here)));
const report={scope:'Pure production Three.js projection arithmetic; no browser/GLB/renderer execution',views:{}};
for(const [name,v]of Object.entries(j.views)){
 const [e,n,bearing,pitch]=v.pose_enu_bearing_pitch,values=[];
 for(const rd of [-.05,.05])for(const ed of [-.25,.25]){
  const c=new T.PerspectiveCamera(62,.5,.1,3000);c.position.set(e,v.default_eye_y_m+ed,-n);c.quaternion.setFromEuler(new T.Euler(pitch*Math.PI/180,-bearing*Math.PI/180,0,'YXZ'));c.updateMatrixWorld(true);
  for(const x of j.actual_flat_source_world_aabb.map(p=>p[0]))for(const y of j.actual_flat_source_world_aabb.map(p=>p[1]))for(const z of j.actual_flat_source_world_aabb.map(p=>p[2]))values.push(new T.Vector3(x,y+j.flat_to_yard_y_translation_m+rd,z).project(c).toArray());
 }
 const min=[0,1].map(k=>Math.min(...values.map(p=>p[k]))),max=[0,1].map(k=>Math.max(...values.map(p=>p[k])));
 const error=Math.max(...[0,1].flatMap(k=>[Math.abs(min[k]-v.conservative_ndc_min[k]),Math.abs(max[k]-v.conservative_ndc_max[k])]));assert(error<1e-12);assert(values.every(p=>Math.abs(p[0])<=.97&&Math.abs(p[1])<=.97&&p[2]>=-1&&p[2]<=1));report.views[name]={corners:values.length,min,max,max_math_error:error,pass:true};
}
fs.writeFileSync(new URL('THREE-PROJECTION-PARITY.json',here),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
