# SPDX-License-Identifier: GPL-3.0-or-later
"""Proposed read-only tests on frozen actual GLB+sidecar; never regenerate fixtures."""
import pathlib,json,struct,hashlib,copy,sys
from surface_metadata import clean_surface_manifest
P=pathlib.Path(sys.argv[1])
raw=(P/'equine_light_harness_skinned_prototype_01.glb').read_bytes();assert hashlib.sha256(raw).hexdigest()=='b880dce59fda746969b7fefe91d8ba0f5478208d73f821e7efa319bdb49ca8d4'
n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);binary=raw[28+n:];q=next(m for m in g['meshes']if m['name']=='skinned_equine_coat')['primitives'][0];a=g['accessors'][q['indices']];v=g['bufferViews'][a['bufferView']];indices=list(struct.unpack_from('<'+{5125:'I',5123:'H'}[a['componentType']]*a['count'],binary,v.get('byteOffset',0)+a.get('byteOffset',0)));manifest=json.loads((P/'manifest.json').read_text());before=copy.deepcopy(manifest);index_before=indices[:]
result=clean_surface_manifest(manifest,indices);assert manifest==before and indices==index_before and (P/'equine_light_harness_skinned_prototype_01.glb').read_bytes()==raw
assert 'vertex_ranges'not in result and result['source_vertex_ranges']==manifest['vertex_ranges'];assert result['surface_metadata_schema_version']==2
study=result['shoulder_join_trial'];assert 'added_face_count'not in study and 'removed_face_count'not in study and isinstance(study['joint_policy'],dict);assert 'JOINTS_0'in study['joint_policy']['final_authority'];counts=study['construction_stage_counts'];assert counts['pre_local_subdivision_added_bridge_triangles']==308 and counts['final_joined_bridge_triangles']==1184 and counts['final_whole_changed_triangles']==1586
# Independent old-consumer simulation demonstrates actual geometry omitted by
# range-only selection; final region must include those real bridge faces.
faces=[indices[i:i+3]for i in range(0,len(indices),3)];omitted=[]
for record in manifest['shoulder_join_trial']['records']:
 r=next(r for r in manifest['vertex_ranges']if r['original_node']==record['label']+'_upper_mesh');legacy={i for i,f in enumerate(faces)if all(r['vertex_start']<=v<r['vertex_start']+r['vertex_count']for v in f)};lost=set(record['new_triangle_indices'])-legacy;assert lost and lost<=set(result['active_surface_regions']['regions'][record['label']+'_upper_joined']);omitted.append(len(lost))
def rejects(m,ix):
 try:clean_surface_manifest(m,ix)
 except AssertionError:return
 raise AssertionError('Invalid actual surface contract accepted')
bad=copy.deepcopy(manifest);bad['shoulder_join_trial']['active_whole_changed_triangle_indices']=bad['shoulder_join_trial']['active_changed_body_triangle_indices'][:];rejects(bad,indices)
bad=copy.deepcopy(manifest);bad['shoulder_join_trial']['records'][0]['active_triangle_indices']=[];rejects(bad,indices)
badix=indices[:];badix[0]=manifest['shoulder_join_trial']['records'][0]['retired_unreferenced_vertices'][0];rejects(manifest,badix)
print({'pass':True,'actual_glb_unchanged':True,'source_inputs_not_mutated':True,'legacy_bridge_faces_omitted':omitted,'negative_cases':3})
