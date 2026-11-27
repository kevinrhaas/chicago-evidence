// Evaluated through functions.exec, where connected GitHub tools are available.
const app='/workspace/work/chicago-historical-photo-deployment/chicago/4d';
const unpack=r=>r.structuredContent??JSON.parse(r.content.find(c=>c.type==='text').text);
const read=await tools.exec_command({cmd:'cat work/visual-photo-combined-dispatch.json',workdir:app,max_output_tokens:8000});
if(read.exit_code!==0)throw Error(read.output);
const d=JSON.parse(read.output),gate=d.auxiliary_runs.find(r=>r.name==='Chicago 4D — gate');
const selected=[{kind:'gate',...gate},...d.coverage.map(c=>({kind:'smoke',...c})),...d.auxiliary_runs.filter(r=>r.run_id!==gate.run_id).map(r=>({kind:'aux',...r}))];
const pathResult=await tools.exec_command({cmd:"python3 - <<'PY'\nfrom pathlib import Path\nimport json\nprint(json.dumps([p.name for p in Path('work/visual-photo-hosted').glob('*.log')]))\nPY",workdir:app,max_output_tokens:8000});
if(pathResult.exit_code!==0)throw Error(pathResult.output);
const existing=new Set(JSON.parse(pathResult.output));
const queried=await Promise.allSettled(selected.map(async r=>{
 const raw=unpack(await tools.mcp__codex_apps__github_fetch_workflow_run_jobs({repo_full_name:'kevinrhaas/chicago',run_id:r.run_id}));
 if(!Array.isArray(raw.jobs))throw Error('Missing jobs '+r.run_id);return {...r,jobs:raw.jobs};
}));
for(const r of queried)if(r.status!=='fulfilled')throw r.reason;
const runs=queried.map(r=>r.value),wanted=[];
for(const r of runs)for(const j of r.jobs){
 if(j.conclusion!=='success')continue;
 let file;
 if(r.kind==='gate'){
  const m=/^gate part (\d+)\/8$/.exec(j.name);
  if(m)file=`gate-part-${m[1]}-of8-run-${r.run_id}-job-${j.id}.log`;
  else if(j.name==='gate')file=`gate-aggregate-run-${r.run_id}-job-${j.id}.log`;
 }else if(r.kind==='smoke'&&j.name==='smoke')file=`smoke-${r.viewport}-${r.stage}-run-${r.run_id}-job-${j.id}.log`;
 else if(r.kind==='aux'&&['humans','moving-frames','upload-release'].includes(j.name))file=`aux-${j.name}-run-${r.run_id}-job-${j.id}.log`;
 if(file&&!existing.has(file))wanted.push({file,job:j.id});
}
const downloaded=await Promise.allSettled(wanted.map(async r=>{
 const raw=unpack(await tools.mcp__codex_apps__github_fetch_workflow_job_logs({repo_full_name:'kevinrhaas/chicago',job_id:r.job}));
 if(typeof raw.content!=='string')throw Error('Missing log '+r.job);return {...r,log:raw.content};
}));
for(const r of downloaded)if(r.status!=='fulfilled')throw r.reason;
async function save(path,body){
 const result=await tools.apply_patch('*** Begin Patch\n*** Add File: '+app+'/'+path+'\n'+body.split('\n').map(l=>'+'+l).join('\n')+'\n*** End Patch');
 if(result?.isError)throw Error('Cannot save '+path);
}
for(const r of downloaded){const {file,log}=r.value;await save('work/visual-photo-hosted/'+file,log);}
const stamp={source_sha:d.source_sha,source_tree:d.source_tree,at:new Date().toISOString()};
await save('work/visual-photo-combined-gate-jobs.json',JSON.stringify({...stamp,run_id:gate.run_id,jobs:runs.find(r=>r.kind==='gate').jobs},null,2)+'\n');
await save('work/visual-photo-hosted-jobs.json',JSON.stringify({...stamp,runs:runs.filter(r=>r.kind==='smoke').map(({run_id,viewport,stage,jobs})=>({run_id,viewport,stage,jobs}))},null,2)+'\n');
await save('work/visual-photo-combined-auxiliary-jobs.json',JSON.stringify({...stamp,runs:runs.filter(r=>r.kind==='aux').map(({run_id,name,jobs})=>({run_id,name,jobs}))},null,2)+'\n');
text({logs_saved:downloaded.length,runs:runs.map(r=>({kind:r.kind,run_id:r.run_id,viewport:r.viewport,stage:r.stage,jobs:r.jobs.filter(j=>['gate','smoke','humans','moving-frames','upload-release'].includes(j.name)||j.name.startsWith('gate part')).map(j=>({name:j.name,status:j.status,conclusion:j.conclusion}))}))});
