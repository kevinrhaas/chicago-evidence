# SPDX-License-Identifier: GPL-3.0-or-later
import sys,json,hashlib,copy
from pathlib import Path
from frozen_human_seated_study import load_study
D=Path(__file__).resolve().parent;R=Path('/workspace/chicago-waistcoat/chicago/4d')
recipe=json.loads((D/'inputs/worker_1835.json').read_text());v=next(x for x in recipe['proof_variants']if x['id']=='bardwell_otis_1835');body=R/'assets/authored/humans/makehuman_hm08/prepared_adult_25.json';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();b0=h(body)
profile=D/'proposed/data/humans/poses/w01/resident-driver-bindings.json';pose,meta=load_study(profile,v,body,1,D/'inputs/wagon-driver-sidecar.json');assert pose==json.loads((D/'inputs/corrected-source-pose.json').read_text())['bone_global_head_rotation'];old=json.loads((D/'exact-preimages/data/humans/poses/w01/resident-driver-bindings.json').read_text());new=json.loads(profile.read_text());assert [x for x in old['resident_bindings']if x['asset_id']!='bardwell_otis_1835']==[x for x in new['resident_bindings']if x['asset_id']!='bardwell_otis_1835'];assert h(body)==b0
errors={}
for label,variant,scale in [('wrong_scene',{**v,'person_reference_scene':'1904'},1),('scaled_body',v,1.01),('wrong_person',{**v,'person_reference_id':'kinzie_john_elder'},1)]:
 try:load_study(profile,variant,body,scale,D/'inputs/wagon-driver-sidecar.json')
 except ValueError as e:errors[label]=str(e)
 else:raise AssertionError(label+' negative control accepted')
report={'status':'PASS_EXISTING_CANONICAL_SOURCE_LOADER','actual_source_body_sha256':b0,'pose_sha256':h(profile.parent/'bardwell_otis_1835-triangle-corrected-pose.json'),'profile_sha256':h(profile),'other_residents_exact':True,'actual_existing_source_loader_metadata':meta,'negative_controls_rejected':errors,'canonical_Blender_execution':False,'scene_driver_enable':False};(D/'CANONICAL-SOURCE-LOADER-READBACK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
