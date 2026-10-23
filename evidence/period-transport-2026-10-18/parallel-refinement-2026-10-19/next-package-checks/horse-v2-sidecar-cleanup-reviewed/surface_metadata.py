# SPDX-License-Identifier: CC0-1.0
"""Manifest-only cleanup. Never changes mesh, positions, indices, weights or GLB."""
import copy


def require(condition, message):
    if not condition:
        raise ValueError(message)

def clean_surface_manifest(manifest,coat_indices):
    result=copy.deepcopy(manifest)
    require(len(coat_indices)>0 and len(coat_indices)%3==0, "Invalid coat triangle index count")
    require(all(isinstance(v,int) and not isinstance(v,bool) and v>=0 for v in coat_indices), "Invalid coat vertex index")
    faces=[coat_indices[i:i+3]for i in range(0,len(coat_indices),3)];count=len(faces)
    source=result.pop('vertex_ranges')  # Fail closed in obsolete range-only consumers.
    result['source_vertex_ranges']=source
    result['source_vertex_ranges_purpose']='Construction audit only; may include retired unreferenced vertices. Never an active surface selector.'
    study=result['shoulder_join_trial']
    def ids(values):
        require(isinstance(values,list) and all(isinstance(i,int)and not isinstance(i,bool)and 0<=i<count for i in values),'Invalid active coat triangle ID')
        require(len(values)==len(set(values)),'Duplicate active triangle ID')
        return sorted(values)
    changed=ids(study['active_whole_changed_triangle_indices']);changed_body=ids(study['active_changed_body_triangle_indices']);bridges=ids(study['new_triangle_indices'])
    require(set(changed)==set(changed_body)|set(bridges),'Missing changed body or bridge coverage')
    require(not set(changed_body)&set(bridges),'Body/bridge origin tags overlap')
    records=study['records']
    require(isinstance(records,list) and len(records)==2 and {r['label'] for r in records}=={'fore_l','fore_r'}, 'Require exactly unique fore_l/fore_r records')
    referenced={v for face in faces for v in face}
    bridge_union=set()
    active_union=set()
    for record in study['records']:
        require(not referenced.intersection(record['retired_unreferenced_vertices']),'Retired cap unexpectedly rendered')
    body=next(r for r in source if r['original_node']=='continuous_body_neck');start=body['vertex_start'];end=start+body['vertex_count']
    torso=ids(sorted({i for i,face in enumerate(faces)if all(start<=v<end for v in face)}|set(changed_body)))
    regions={'torso_body_neck':torso,'forechest_changed':changed}
    for record in study['records']:
        active=ids(record['active_triangle_indices']);new=ids(record['new_triangle_indices'])
        require(bool(active) and bool(new),'Empty joined active/bridge surface')
        require(set(new)<=set(active),'Joined region omits bridge faces')
        require(not set(new)&bridge_union, 'Per-record bridge ownership overlap')
        require(not set(active)&active_union, 'Appendage ownership overlap')
        bridge_union.update(new)
        active_union.update(active)
        declared_vertices=record['active_surface_vertex_indices']
        require(isinstance(declared_vertices,list) and declared_vertices and all(isinstance(v,int) and not isinstance(v,bool) and v>=0 for v in declared_vertices) and len(declared_vertices)==len(set(declared_vertices)), 'Invalid active surface vertex table')
        vertices=set(declared_vertices)
        expected={i for i,face in enumerate(faces) if set(face)<=vertices}
        require(set(active)==expected,'Active face table disagrees with current coat and declared surface vertices')
        require({v for i in active for v in faces[i]}==vertices,'Active surface vertices disagree with actual face coverage')
        require(not set(active)&set(torso),'Torso and appendage face ownership overlap')
        regions[record['label']+'_upper_joined']=active
    require(bridge_union==set(bridges),'Per-record/global bridge tables disagree')
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
