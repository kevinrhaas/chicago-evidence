# SPDX-License-Identifier: CC0-1.0
"""Manifest-only cleanup. Never changes mesh, positions, indices, weights or GLB."""
import copy

def clean_surface_manifest(manifest,coat_indices):
    result=copy.deepcopy(manifest)
    assert len(coat_indices)%3==0
    faces=[coat_indices[i:i+3]for i in range(0,len(coat_indices),3)];count=len(faces)
    source=result.pop('vertex_ranges')  # Fail closed in obsolete range-only consumers.
    result['source_vertex_ranges']=source
    result['source_vertex_ranges_purpose']='Construction audit only; may include retired unreferenced vertices. Never an active surface selector.'
    study=result['shoulder_join_trial']
    def ids(values):
        assert all(isinstance(i,int)and not isinstance(i,bool)and 0<=i<count for i in values),'Invalid active coat triangle ID'
        assert len(values)==len(set(values)),'Duplicate active triangle ID'
        return sorted(values)
    changed=ids(study['active_whole_changed_triangle_indices']);changed_body=ids(study['active_changed_body_triangle_indices']);bridges=ids(study['new_triangle_indices'])
    assert set(changed)==set(changed_body)|set(bridges),'Missing changed body or bridge coverage'
    assert not set(changed_body)&set(bridges),'Body/bridge origin tags overlap'
    referenced={v for face in faces for v in face}
    for record in study['records']:
        assert not referenced.intersection(record['retired_unreferenced_vertices']),'Retired cap unexpectedly rendered'
    body=next(r for r in source if r['original_node']=='continuous_body_neck');start=body['vertex_start'];end=start+body['vertex_count']
    torso=ids(sorted({i for i,face in enumerate(faces)if all(start<=v<end for v in face)}|set(changed_body)))
    regions={'torso_body_neck':torso,'forechest_changed':changed}
    for record in study['records']:
        active=ids(record['active_triangle_indices']);new=ids(record['new_triangle_indices'])
        assert set(new)<=set(active),'Joined region omits bridge faces'
        assert not set(active)&set(torso),'Torso and appendage face ownership overlap'
        regions[record['label']+'_upper_joined']=active
    result['active_surface_regions']={'schema_version':1,'mesh':'skinned_equine_coat','index_space':'triangle ordinal in current exported coat primitive index accessor, not source vertex ordinal','regions':regions}
    study['construction_stage_counts']={
        'pre_local_subdivision_removed_source_coat_triangles':study.pop('removed_face_count'),
        'pre_local_subdivision_added_bridge_triangles':study.pop('added_face_count'),
        'final_active_coat_triangles':count,
        'final_changed_body_triangles':len(changed_body),
        'final_joined_bridge_triangles':len(bridges),
        'final_whole_changed_triangles':len(changed),
    }
    study['joint_policy']={
        'final_authority':'Exported normalized JOINTS_0/WEIGHTS_0, plus declared changed-original-weight mask; do not infer final weights from construction ring recipes.',
        'construction':'Root/upper bridge ring weights are subsequently mixed by one local subdivision pass.',
        'interface':'Actual shared vertex indices share final positions, weights and normals; body boundary must not be described as retaining original root-only weights.',
        'protected':'Bones, inverse binds, clips, head/neck row7+, original distal boundary and lower/sole vertices remain separately validated.',
    }
    result['surface_metadata_schema_version']=2
    return result
