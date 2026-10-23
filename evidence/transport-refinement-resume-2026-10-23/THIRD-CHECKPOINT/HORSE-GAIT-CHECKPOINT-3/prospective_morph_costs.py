"""Read-only cost arithmetic before any portable export. No model generation."""
from pathlib import Path
import json,hashlib,math
r=Path(__file__).parent;d=r/'V25-ORIENTED-TRIANGLE-ADMM'
p=d/'ACTUAL/ACTUAL-V25-ORIENTED-TRIANGLE-ADMM-ORIGINAL65-READBACK.json'
j=json.loads(p.read_text());assert j['mechanics_pass']and j['deformation_screen_pass'],'No cost-to-export readiness claim on failed physical unit'
assert j['actual_evaluation']['poses_inclusive']==65
vertices=j['surfaces'][1]['vertices'];assert vertices==4313
vendor=Path('/workspace/chicago-waistcoat/chicago/4d/renderers/web/vendor/three-0.185.1/three.module.js')
rows=[]
for targets in [8,12,16,64]:
 raw=vertices*3*4*2*targets
 gpu=[]
 for cap in [2048,4096,8192,16384]:
  width=vertices*2;height=1
  if width>cap:height=math.ceil(width/cap);width=cap
  gpu.append({'maxTextureSize':cap,'width':width,'height':height,'layers':targets,'FloatRGBA_texture_bytes':width*height*4*4*targets,'separate_CPU_texture_backing_bytes':width*height*4*4*targets})
 rows.append({'targets':targets,'status':'hypothetical compressed basis, NOT implemented or tested'if targets<64 else'64 unique phases, endpoint reuses phase0','additional_dense_POSITION_and_NORMAL_FLOAT_payload_bytes':raw,'morph_weight_key_payload_65_frames_FLOAT_bytes':65*targets*4,'GPU_texture':gpu,'additional_GLTFLoader_dense_CPU_morph_attribute_bytes':raw,'known_B479_base_bytes_plus_dense_morph_payload_before_new_metadata_animation':3783600+raw})
out={'scope':'Prospective payload/texture arithmetic only, no GLB export, no serialized-size/GPU/frame measurement or basis-compression acceptance','physical_unit_pass':True,'physical_result_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'corrective':j['pose_corrective'],'base_vertices':vertices,'unique_phase_samples':64,'semantics':['POSITION','NORMAL'],'component_type':'FLOAT32','baseline_standing_B479_bytes':3783600,'vendor':{'path':str(vendor),'sha256':hashlib.sha256(vendor.read_bytes()).hexdigest(),'version':'0.185.1','allocator':'WebGLMorphtargets width=vertexCount*2; ceil padded height if above maxTextureSize; RGBA Float32 DataArrayTexture; CPU backing allocated separately from geometry attributes'},'rows':rows,'not_approved':['64/65target asset','compressed morph basis','GLB export or app installation','GLTFLoader/Mixer/midpoint contact/normal parity','natural visual gait or photographic acceptance','browser/mobile resource budget'],'next':'Get root review of costs. Prefer a measured small corrective basis and inspect actual posed geometry before any pipeline integration.'}
(r/'PROSPECTIVE-MORPH-COSTS-NOT-EXPORT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'physical_unit_pass':True,'full_dense_target_payload':rows[-1]['additional_dense_POSITION_and_NORMAL_FLOAT_payload_bytes'],'max_correction_m':j['pose_corrective']['maximum_surface_correction_m'],'loop_m':j['pose_corrective']['corrective_loop_position_error_m'],'raw_gpu_texture_per_cap':rows[-1]['GPU_texture']},indent=2))
