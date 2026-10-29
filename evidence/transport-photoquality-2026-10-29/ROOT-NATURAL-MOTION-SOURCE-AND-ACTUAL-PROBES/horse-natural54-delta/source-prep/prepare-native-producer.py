from pathlib import Path
import hashlib

app = Path('/tmp/chicago-horse-20261029/chicago/4d')
package = app / 'tools/transport/horse_natural_idle_v1'
s = (app / 'tools/transport/horse_eye_smooth_normals_v1/native_normal_child129.mjs').read_text()


def replace(old, new):
    global s
    assert s.count(old) == 1, (old[:100], s.count(old))
    s = s.replace(old, new)


replace('// NEW EXTERNAL bd443 eye-NORMAL child producer; no old certificate transfer.',
        '// First-class NEW8ea natural planted idle producer; exact bd443 parent, no old verdict transfer.')
replace('const action=model.mixer.clipAction(model.animations[clip]);',
        'const selected=model.naturalIdleSelected===true?1:clip;const action=model.mixer.clipAction(model.animations[selected]);')
replace('frames=json(resources.accepted_matrices).frames', 'frames=json(resources.expected_matrices).frames')
replace("status:'NEW_ANATOMY_LOADED129_INCOMPLETE'", "status:'NEW_NATURAL_IDLE_LOADED129_INCOMPLETE'")
replace('walking_enabled:false,head_tail_composed:false,photographic_acceptance:false',
        'walking_enabled:false,head_tail_composed:true,selected_exported_clip_index:1,selected_exported_track_count:17,photographic_acceptance:false')
replace("config.inputs.candidate.sha256==='bd443df87b92d19266284cb9b52d30e791215cddf099876c774e9cfb5f5a79b6'",
        "config.inputs.candidate.sha256==='8ea7748ffba6c5fe17cde91042c6d8b26ed9a0ab77de69cadd4f4fb12e9c09fa'&&config.inputs.idle_parent.sha256==='bd443df87b92d19266284cb9b52d30e791215cddf099876c774e9cfb5f5a79b6'")
replace("staticProof.status==='NORMAL_CHILD_CURRENT_SOURCE_STATIC_ONLY_PASS'&&staticProof.source_admission==='eye_smooth_normals_v1'",
        "staticProof.status==='NATURAL_IDLE_CURRENT_SOURCE_STATIC_ONLY_PASS'&&staticProof.source_admission==='natural_planted_idle_v1'")
replace('staticProof.normal_parent_e49_sha256===config.inputs.normal_parent.sha256',
        'staticProof.motion_parent_bd443_sha256===config.inputs.idle_parent.sha256')
replace('normalChildSourceGuard(normalParentRaw,candidateRaw);',
        'const idleParentRaw=glb(resources.idle_parent);normalChildSourceGuard(normalParentRaw,idleParentRaw);naturalIdleSourceGuard(idleParentRaw,candidateRaw,json(resources.motion_recipe));')
replace("for(const key of ['nodes','skins','animations','materials','images','textures','samplers','scenes'])need(JSON.stringify(parentRaw.doc[key])===JSON.stringify(candidateRaw.doc[key]),'Protected live rig/clip/image/material graph '+key);",
        "for(const key of ['nodes','skins','materials','images','textures','samplers','scenes'])need(JSON.stringify(parentRaw.doc[key])===JSON.stringify(candidateRaw.doc[key]),'Protected live rig/image/material graph '+key);need(JSON.stringify(parentRaw.doc.animations)===JSON.stringify(candidateRaw.doc.animations.slice(0,1)),'Exact retained old13trackclip graph');")
replace("need(source.animations.length===0&&candidate.animations.length===1&&candidate.animations[0].name==='sevket_reconstructed_planted_posture_v1'&&candidate.animations[0].duration===12&&candidate.animations[0].tracks.length===13,'Only actual13track standing clip');\n  for(const track of candidate.animations[0].tracks)need(track.getInterpolation()===T.InterpolateLinear&&track.times.length===65&&track.times.every((t,i)=>t===frames[i].time_s),'Actual imported65 linear key streams');",
        "need(source.animations.length===0&&candidate.animations.length===2&&candidate.animations[0].name==='sevket_reconstructed_planted_posture_v1'&&candidate.animations[0].duration===12&&candidate.animations[0].tracks.length===13&&candidate.animations[1].name==='sevket_reconstructed_natural_planted_idle_v1'&&candidate.animations[1].duration===12&&candidate.animations[1].tracks.length===17,'Explicit retained13track plus actual selected second17track clip');candidate.naturalIdleSelected=true;\n  for(const track of candidate.animations[1].tracks)need(track.getInterpolation()===T.InterpolateLinear&&track.times.length===65&&track.times.every((t,i)=>t===frames[i].time_s),'Actual selected17 imported65 linear key streams');\n  const expectedInput=json(resources.expected_matrices);need(expectedInput.schema==='natural_planted_idle_independent_expected65_v1'&&expectedInput.parent65_sha256===config.inputs.accepted_matrices.sha256&&expectedInput.motion_recipe_sha256===config.inputs.motion_recipe.sha256&&expectedInput.controls26_sha256===config.inputs.controls26.sha256,'Independent new65 expectation binds old65, exact motion recipe and unchanged hierarchy');")
replace("need(candidate.animations.length===1&&parent.animations.length===1,'Same native standing clip inventory');",
        "need(candidate.animations.length===2&&candidate.animations[1].name==='sevket_reconstructed_natural_planted_idle_v1'&&candidate.animations[1].tracks.length===17&&parent.animations.length===1,'Explicit new17 clip and unchanged925 reference inventory');candidate.naturalIdleSelected=true;")
helper = """// Exact animation-only admission. The old NORMAL admission above remains genuine.
function naturalIdleSourceGuard(parent,child,recipe){
 need(child.bin.length===parent.bin.length+4160&&bytesEqual(parent.bin,child.bin.subarray(0,parent.bin.length)),'Entire bd443 BIN prefix exact, exactly4new quaternion streams');
 need(recipe.source_parent_sha256==='bd443df87b92d19266284cb9b52d30e791215cddf099876c774e9cfb5f5a79b6'&&recipe.candidate_clip==='sevket_reconstructed_natural_planted_idle_v1','Explicit actual reconstructed natural-idle recipe');
 need(child.doc.animations.length===2&&child.doc.animations[1].channels.length===17&&child.doc.animations[1].samplers.length===17,'Exact two-clip/new17channel inventory');
 const old=parent.doc.animations[0],clip=child.doc.animations[1],targets=[2,3,4,5],input=old.samplers[0].input;
 need(JSON.stringify(clip.channels.slice(0,13))===JSON.stringify(old.channels)&&JSON.stringify(clip.samplers.slice(0,13))===JSON.stringify(old.samplers),'All old13 selected tracks exact');
 for(let k=0;k<4;k++){
  const output=parent.doc.accessors.length+k,view=parent.doc.bufferViews.length+k;
  need(JSON.stringify(clip.channels[13+k])===JSON.stringify({sampler:13+k,target:{node:targets[k],path:'rotation'}}),'Only new declared4rotation targets');
  need(JSON.stringify(clip.samplers[13+k])===JSON.stringify({input,output,interpolation:'LINEAR'}),'Exact new4selected sampler bindings');
  const a=child.doc.accessors[output],v=child.doc.bufferViews[view];need(a.bufferView===view&&a.componentType===5126&&a.count===65&&a.type==='VEC4'&&v.buffer===0&&v.byteOffset===parent.bin.length+1040*k&&v.byteLength===1040,'Exact4new65FLOAT output views');
  const values=new Float32Array(child.bin.buffer,child.bin.byteOffset+v.byteOffset,260);for(let i=0;i<65;i++)need(Math.abs(Math.hypot(...values.slice(4*i,4*i+4))-1)<1e-6,'Unit actual new quaternion');
 }
 const restored=structuredClone(child.doc);restored.accessors=restored.accessors.slice(0,parent.doc.accessors.length);restored.bufferViews=restored.bufferViews.slice(0,parent.doc.bufferViews.length);restored.animations=restored.animations.slice(0,1);restored.buffers[0].byteLength=parent.doc.buffers[0].byteLength;delete restored.asset.extras.chicago4d_natural_planted_idle_v1;
 need(JSON.stringify(restored)===JSON.stringify(parent.doc),'Every unlisted bd443 document field exact');
}
"""
replace('window.compare=async()=>{', helper + 'window.compare=async()=>{')
scope_wrapper = """// The entire9176B original metric block above, including its historical scope
// label, remains byte-exact. Transparently report the new admitted second clip;
// no Three/native renderer method or measured numerical value is changed here.
const compareOriginalPhysicalMetric=window.compare;
window.compare=async()=>{const report=await compareOriginalPhysicalMetric();report.metric_loop_historical_scope=report.scope;report.scope='Actual native GLTFLoader/SkeletonUtils/AnimationMixer second exported17track natural planted clip at65keys+64midpoints; unchanged original physical limits/metric loop. No world/GPU/continuous collision/photographic/walk/rider acceptance.';report.selected_exported_clip='sevket_reconstructed_natural_planted_idle_v1';report.old_certificate_transferred=false;return report;};

"""
replace('// Distinct external capture only.', scope_wrapper + '// Distinct external capture only.')
metric = (app / 'tools/transport/horse_socket_interface_v1/fixtures/UNCHANGED-PHYSICAL-METRIC-LOOP.mjs.txt').read_text()
assert s.count(metric) == 1
assert hashlib.sha256(metric.encode()).hexdigest() == 'a8515b35e18a058673fe330a127eba129851f324915858971e3b683bc4d259a1'
(package / 'native_natural_idle129.mjs').write_text(s)
print('New producer prepared; entire original9176B physical metric block remains exact')
