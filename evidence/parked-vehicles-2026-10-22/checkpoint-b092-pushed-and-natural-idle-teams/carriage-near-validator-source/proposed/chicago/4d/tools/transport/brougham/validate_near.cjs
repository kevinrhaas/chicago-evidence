// SPDX-License-Identifier: GPL-3.0-or-later
// Optional independent Khronos run, same existing validateBytes API. No browser/network/install.
// Existing external gltf-validator@2.0.0-dev.3.10 is supplied through NODE_PATH.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const validator=require('gltf-validator'),version=require('gltf-validator/package.json').version;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 if(process.argv.length!==3)throw Error('Expected exact asset directory');
 if(version!=='2.0.0-dev.3.10')throw Error('Reviewed validator version required');
 const contract=JSON.parse(fs.readFileSync(path.join(__dirname,'near-contract.json'))),rows=[];
 for(const[name,key]of[['brougham-source.glb','raw_sha256'],['brougham-near.glb','near_sha256']]){
  const bytes=fs.readFileSync(path.join(path.resolve(process.argv[2]),name));if(sha(bytes)!==contract[key])throw Error('Exact V14 file required '+name);
  const report=await validator.validateBytes(new Uint8Array(bytes),{uri:name});
  const q=report.issues;if(q.numErrors||q.numWarnings||q.truncated||q.numInfos!==4||q.messages.length!==4||q.messages.some(m=>m.code!=='NODE_EMPTY'||m.severity!==2)||JSON.stringify(q.messages.map(m=>m.pointer).sort())!==JSON.stringify([13,14,15,16].map(i=>'/nodes/'+i).sort()))throw Error('Unexpected actual Khronos result '+name+' '+JSON.stringify(q));
  rows.push({file:name,actual_sha256:sha(bytes),bytes:bytes.length,report});
 }
 console.log(JSON.stringify({pass:true,scope:'Fresh actual V14 raw and indexednear Khronos conformance only; no visual/world/occupied or fullLOD acceptance',validator_version:version,rows}));
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
