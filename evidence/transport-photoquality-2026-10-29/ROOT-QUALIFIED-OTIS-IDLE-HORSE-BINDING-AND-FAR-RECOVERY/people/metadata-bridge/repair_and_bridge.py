import copy, datetime, hashlib, importlib.util, json, sys
from pathlib import Path
APP=Path('/tmp/chicago-transport-resume-20261029/chicago/4d')
BASE=Path('/workspace/.cloud-setup/logs/transport-recovery')
OUT=Path(__file__).parent
ARCHIVE=BASE/'HUMAN-NATURAL-STANDING-QUALIFIED-SOURCE-FINAL'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.APP=APP;return mod
old=load('old_generator',ARCHIVE/'source/tools/human_natural_idle.py')
new=load('new_generator',APP/'tools/human_natural_idle.py')
summary_raw=(ARCHIVE/'HUMAN-NATURAL-STANDING-EXACT-EIGHT-NATIVE-SUMMARY.json').read_bytes()
assert sha(summary_raw)=='6887f4a45a769d6a70e73f12170c358c9c61a740cc49df11668009d89a9e5488'
summary=json.loads(summary_raw)
assert sha((ARCHIVE/'source/tools/human_natural_idle.py').read_bytes())==summary['implementation_and_parent_pins']['tools/human_natural_idle.py']
recipe_raw=(APP/'data/humans/animations/natural-standing-v1.json').read_bytes()
assert sha(recipe_raw)==summary['implementation_and_parent_pins']['data/humans/animations/natural-standing-v1.json']
recipe=json.loads(recipe_raw)
pose_parent=recipe['parents'][0]['sha256']
bases=old.source_pose(*old.parse(old.parent_bytes(recipe['parents'][0],recipe)))
def equivalent(old_raw,new_raw,parent_sha):
 a,abin=old.parse(old_raw); b,bbin=new.parse(new_raw)
 assert abin==bbin,'entire BIN differs'
 assert a['animations'][-1]['name']==b['animations'][-1]['name']=='idle_natural_v1'
 assert a['animations'][-1]['extras']['canonical_parent_sha256']==parent_sha
 assert b['animations'][-1]['extras']['canonical_rig_pose_parent_sha256']==pose_parent
 expected=copy.deepcopy(a)
 e=expected['animations'][-1]['extras'];del e['canonical_parent_sha256'];e['canonical_rig_pose_parent_sha256']=pose_parent
 assert b==expected,'decoded JSON change outside exact declared metadata replacement'
 return {'entire_bin_sha256':sha(abin),'entire_bin_bytes':len(abin),'entire_bin_exact':True,'all_other_json_values_exact':True,'geometry_skin_inverse_binds_images_materials_uv_nodes_old_clips_exact':True,'new_clip_channels_samplers_times_and_values_exact':True}
rows=[];writes=[];derivations=[]
for row in recipe['parents']:
 parent=old.parent_bytes(row,recipe)
 prior,_=old.append_clip(parent,row['sha256'],bases,recipe)
 assert sha(prior)==summary['candidate_pins'][row['file']]
 assert (APP/row['file']).read_bytes()==prior,'current selected bytes differ from tested candidates'
 repaired,derivation=new.append_clip(parent,row['sha256'],bases,recipe)
 proof=equivalent(prior,repaired,row['sha256'])
 rows.append(dict(file=row['file'],canonical_parent_sha256=row['sha256'],tested_sha256=sha(prior),metadata_repaired_sha256=sha(repaired),tested_bytes=len(prior),metadata_repaired_bytes=len(repaired),**proof))
 writes.append((APP/row['file'],repaired));derivations.append(dict(file=row['file'],**derivation))
 # Real corrupted data or unrelated clip metadata must fail this same bridge.
 d,bin_data=new.parse(repaired)
 for label,bad in [('BIN',new.encode(d,bytes([bin_data[0]^1])+bin_data[1:])),('sampler',None),('unrelated_metadata',None)]:
  if label=='sampler':
   bad_doc=copy.deepcopy(d);bad_doc['animations'][-1]['samplers'][0]['interpolation']='LINEAR' if bad_doc['animations'][-1]['samplers'][0].get('interpolation','LINEAR')!='LINEAR' else 'STEP';bad=new.encode(bad_doc,bin_data)
  if label=='unrelated_metadata':
   bad_doc=copy.deepcopy(d);bad_doc['animations'][-1]['extras']['cycle_duration_s']=9;bad=new.encode(bad_doc,bin_data)
  try:equivalent(prior,bad,row['sha256'])
  except AssertionError:pass
  else:raise AssertionError('bridge failed corruption control '+label)
receipt={'schema':'human_natural_idle_metadata_bridge_v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_BIN_AND_DECODED_ANIMATION_EQUIVALENCE_PASS','original_actual_native_summary_sha256':sha(summary_raw),'original_actual_native_summary_preserved':True,'original_tested_generator_sha256':summary['implementation_and_parent_pins']['tools/human_natural_idle.py'],'metadata_repaired_generator_sha256':sha((APP/'tools/human_natural_idle.py').read_bytes()),'allowed_change_only':'animations[-1].extras.canonical_parent_sha256 replaced by canonical_rig_pose_parent_sha256 naming common master-LOD0 rig pose source','producer_notices_changed':False,'files':rows,'actual_corruption_controls_rejected':24,'scope':'Explicit equivalence to the eight finite native-129 tested assets. This is not a fresh native-129 run, browser render measurement, continuous fit or photographic acceptance. Original certificate retains its original source and asset SHAs.','new_native_129_rerun':False,'browser_cost_measured':False,'published_world_visual_accepted':False}
(OUT/'BRIDGE.json').write_text(json.dumps(receipt,indent=2)+'\n')
(OUT/'ORIGINAL-EXACT-EIGHT-NATIVE-SUMMARY.json').write_bytes(summary_raw)
(OUT/'ORIGINAL-TESTED-GENERATOR.py').write_bytes((ARCHIVE/'source/tools/human_natural_idle.py').read_bytes())
for path,raw in writes:path.write_bytes(raw)
derivation={'schema':'human_natural_idle_derivation_v1','recipe_sha256':sha(recipe_raw),'generator_sha256':receipt['metadata_repaired_generator_sha256'],'files':derivations,'scope':'Generated animation derivative; exact-BIN metadata bridge to original finite native-129 assets recorded separately. Actual browser measurements and world visual acceptance pending.','actual_native_qualified':False,'photographic_accepted':False}
(APP/'data/humans/animations/natural-standing-v1.derivation.json').write_text(json.dumps(derivation,indent=2)+'\n')
(APP/'data/humans/animations/natural-standing-v1.metadata-bridge.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'bridged_exact_assets':len(rows),'controls_rejected':24,'bridge_sha256':sha((OUT/'BRIDGE.json').read_bytes())}))
