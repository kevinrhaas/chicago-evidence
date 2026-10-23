# SPDX-License-Identifier: GPL-3.0-or-later
import sys,json,copy,tempfile,hashlib,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D/'proposed-contact-floor/tools'))
from human_seated_contact_lod import load_policy,garment_ratio
recipe=json.loads((D/'inputs/worker_1835.json').read_text());variant=next(v for v in recipe['proof_variants']if v['id']=='bardwell_otis_1835');profile=D/'proposed-contact-floor/data/humans/poses/w01/resident-driver-bindings.json';policy=load_policy(profile,variant,recipe);assert policy['minimum_ratio']==.6
# No-profile/default behavior and other named residents retain exact original ratios.
for kind in ['body','shirt','waistcoat','trousers','hair','eyes','shoes']:
 for lod,ratio in enumerate(recipe['lod_ratios']):
  assert garment_ratio(kind,lod,ratio,None)==ratio
  assert garment_ratio(kind,lod,ratio,policy)==(.6 if kind=='trousers'and lod in [2,3]else ratio)
for ident in ['dufresne_joseph_1835','flynn_martin_1835']:
 other=next(v for v in recipe['proof_variants']if v['id']==ident);assert load_policy(profile,other,recipe) is None
negatives={}
with tempfile.TemporaryDirectory(dir=D)as temp:
 p=Path(temp);source=json.loads(profile.read_text());pose=profile.parent/'bardwell_otis_1835-triangle-corrected-pose.json';shutil.copy2(pose,p/pose.name)
 for label in ['wrong_scene','wrong_person','different_lod_ratio','changed_target_lods','wrong_pose_hash','unqualified_flag_removed']:
  j=copy.deepcopy(source);v=copy.deepcopy(variant);r=copy.deepcopy(recipe);row=next(x for x in j['resident_bindings']if x['asset_id']=='bardwell_otis_1835')
  if label=='wrong_scene':v['person_reference_scene']='1904'
  if label=='wrong_person':v['person_reference_id']='kinzie_john_elder'
  if label=='different_lod_ratio':r['lod_ratios'][1]=.7
  if label=='changed_target_lods':row['driver_contact_lod']['target_lods']=[0,1,2,3]
  if label=='wrong_pose_hash':row['pose_draft_sha256']='0'*64
  if label=='unqualified_flag_removed':row['driver_contact_lod']['live_driver_qualified']=True
  f=p/'resident-driver-bindings.json';f.write_text(json.dumps(j))
  try:load_policy(f,v,r)
  except ValueError as e:negatives[label]=str(e)
  else:raise AssertionError(label+' accepted')
report={'status':'PASS_CONTACT_FLOOR_SOURCE_POLICY_ONLY','policy':policy,'default_and_other_resident_ratios_exact':True,'only_trousers_lod2_lod3_changed':True,'negative_controls_rejected':negatives,'Blender_execution':False};(D/'CONTACT-FLOOR-SOURCE-TESTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
