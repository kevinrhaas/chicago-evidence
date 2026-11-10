# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only source-bound interval research; NEVER a geometry qualification."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import math
import struct
import sys
import time
import traceback

import numpy as np


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom(path, data):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    temporary.replace(path)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--binding-sha',required=True)
    args=cli.parse_args()
    prep=Path(__file__).parent
    binding_path=prep/'INPUT-BINDING.json'
    assert digest(binding_path)==args.binding_sha
    binding=json.loads(binding_path.read_text())
    output=args.output
    assert not output.exists(),'Fresh owned output required'
    output.mkdir()
    expected={row['path']:row['sha256'] for row in binding['files']}
    def snapshot():
        result={name:digest(Path(name)) for name in expected}
        assert result==expected,'Immutable source/data/helper changed'
        return result
    before=snapshot();atom(output/'PARENTS-BEFORE.json',before)
    sys.path.insert(0,binding['tool_directory'])
    import check_door_aperture as checker
    from check_near import read,world_nodes
    from check_mid import bind_parts

    full=json.loads(Path(binding['full_report']).read_text())
    assert full['PASS'] is False and full['unresolved_continuous_pairs']==42
    closure=json.loads(Path(binding['full_closure']).read_text())
    assert closure['result']['returncode']==1 and closure['result']['timed_out'] is False
    assert closure['resources']['accepted'] and closure['cleanup']['cleanup_complete'] and not closure['cleanup']['remaining_owned_children']
    assert full['interval_counts']=={'moving_triangles_completed':2824,'moving_triangles_total':2824,
        'broadphase_pairs':2100050,'pairs_completed':2100050,'pairs_proven_clear':2100008,'unresolved_or_intersecting_pairs':42}
    assert full['input_sha256']==binding['native_input_sha256']
    assert full['recipe_sha256']==digest(Path(binding['recipe']))
    assert full['source_receipt_sha256']==digest(Path(binding['source_receipt']))
    assert full['interval_helper_sha256']==digest(Path(binding['tool_directory'])/'interval_batch.py')
    assert full['candidate_sha256']==binding['candidate_sha256']
    assert full['checker_sha256']==digest(Path(checker.__file__))
    assert full['max_interval_depth']==12 and full['intersection_tolerance_m']==1e-8
    assert len(full['sampled'])==15 and sum(x['triangle_contacts'] for x in full['sampled'])==0
    recipe=json.loads(Path(binding['recipe']).read_text())
    assert not any(recipe['qualification'].values()) and not recipe['boarding_enabled'] and not recipe['driver_passenger_fit']
    doc,binary=read(Path(binding['candidate']))
    original,original_binary=read(Path(binding['native_input']))
    triangles,moving,labels=checker.decode(doc,binary)
    pivot=np.asarray(recipe['hinge_root_m'])
    mobile,fixed=triangles[moving]-pivot,triangles[~moving]-pivot
    global_mobile,global_fixed=np.flatnonzero(moving),np.flatnonzero(~moving)
    assert len(mobile)==2824 and len(triangles)==54642
    flo,fhi=fixed.min(axis=1),fixed.max(axis=1)
    angle=math.radians(recipe['open_angle_deg'])
    assert angle==math.radians(-65)
    tolerance,depth=1e-8,12

    # Exact native source-order/range exhaustion binder preserves all four
    # repeated hubcap names. Mesh/name is never treated as occurrence identity.
    bindings=bind_parts(doc,binary)
    native_bindings=bind_parts(original,original_binary)
    mesh_offsets=[];cursor=0
    for mesh in doc['meshes']:
        assert len(mesh['primitives'])==1
        primitive=mesh['primitives'][0]
        assert 'indices' not in primitive
        count=doc['accessors'][primitive['attributes']['POSITION']]['count']//3
        mesh_offsets.append(cursor);cursor+=count
    assert cursor==len(triangles)
    part_ids=np.full(cursor,-1,dtype=np.int32)
    local_ids=np.full(cursor,-1,dtype=np.int32)
    for part,row in zip(doc['extras']['parts'],bindings):
        start=mesh_offsets[row['mesh_index']]+part['triangle_start_in_batch']
        end=start+part['triangles']
        assert np.all(part_ids[start:end]==-1)
        part_ids[start:end]=row['part_index'];local_ids[start:end]=np.arange(part['triangles'])
    assert np.all(part_ids>=0) and np.all(local_ids>=0)
    world=world_nodes(doc)
    def occurrence(global_id):
        part_id=int(part_ids[global_id]);triangle_in_part=int(local_ids[global_id])
        part=doc['extras']['parts'][part_id];row=bindings[part_id]
        points=np.frombuffer(row['chunks']['POSITION'],dtype='<f4').reshape((-1,3,3))[triangle_in_part].astype(float)
        points+=np.asarray(world[row['node_path'][-1][0]])
        assert np.array_equal(points,triangles[global_id]),'Triangle occurrence lookup differs from actual decoder'
        source_ids=[]
        for key in ['source_part_index','derived_source_part_index']:
            if key in part:source_ids.append((key,int(part[key])))
        for value in part.get('engineering_source_part_indices',[]):
            source_ids.append(('engineering_source_part_indices',int(value)))
        originals=[]
        for provenance,source_id in source_ids:
            original_part=original['extras']['parts'][source_id]
            originals.append({'relation':provenance,'source_occurrence_id':source_id,
                'source_identity':[original_part[k] for k in ['name','frame','material','triangles']],
                'actual_source_node_path':native_bindings[source_id]['node_path']})
        return {'actual_global_triangle_index':int(global_id),'actual_part_index':part_id,
            'triangle_in_actual_part':triangle_in_part,'actual_part_name':part['name'],'actual_frame':part['frame'],
            'actual_material_index':part['material'],'actual_mesh_index':row['mesh_index'],
            'actual_node_path':row['node_path'],'source_occurrences':originals,
            'new_engineering_without_original_occurrence':not originals,
            'closed_root_triangle_m':points.tolist()}

    # Compile the original recursive AST with ONE observation-only callback
    # immediately after its actual scalar gap. Remove it and require exact AST
    # equality before compiling. No independent reimplementation of its branches.
    source=Path(checker.__file__).read_text()
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='interval_clear')
    authority_ast=ast.dump(node,include_attributes=False)
    index=next(i for i,n in enumerate(node.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='gap' for t in n.targets))
    probe=ast.parse('observe(start,end,depth,middle,radius,displacement,gap)').body[0]
    node.body.insert(index+1,probe)
    removed=node.body.pop(index+1);assert ast.dump(node,include_attributes=False)==authority_ast;node.body.insert(index+1,removed)
    states=[]
    def observe(start,end,remaining,middle,radius,displacement,gap):
        assert len(states)<8191,'Original depth12 complete-tree observation bound exceeded'
        states.append([float(start),float(end),int(remaining),float(middle),float(radius),float(displacement),float(gap)])
    namespace={'np':np,'math':math,'turn':checker.turn,'separation':checker.separation,'observe':observe}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),str(Path(checker.__file__))+' OBSERVER ONLY','exec'),namespace)

    started=time.monotonic();last_update=started
    counts={'moving_triangles_completed':0,'moving_triangles_total':len(mobile),'broadphase_pairs':0,
            'pairs_completed':0,'pairs_proven_clear':0,'nonclear_pairs':0,'scalar_confirmed_contact_pairs':0,'scalar_depth_unresolved_pairs':0}
    totals=checker.interval_batch_counters();witnesses=[];completed=False;failure=None
    progress={'schema':'chicago-t2797-interval-nonclear-research-v1','state':'RUNNING_DIAGNOSTIC_ONLY',
        'original_full_NONPASS_report_sha256':digest(Path(binding['full_report'])),
        'source_binding_sha256':args.binding_sha,'source_checkpoint':'74aea12face3705206cf9fd29ddde46ca967c592',
        'candidate_sha256':binding['candidate_sha256'],'depth':depth,'tolerance_m':tolerance,
        'qualification':False,'PASS':False,'final_PASS':False,'structure_repeated':False,'sampled15_repeated':False,
        'research_selection_only':True,'skipped_moving_triangles':0,'failure_record_cap':64,
        'scalar_authority_AST_sha256':hashlib.sha256(authority_ast.encode()).hexdigest()}
    def save(**updates):
        progress.update(updates);progress.update(elapsed_s=time.monotonic()-started,counts=counts,
            interval_batch_totals=totals,witnesses=witnesses)
        atom(output/'PROGRESS.json',progress)
    save()
    try:
        for mobile_id,triangle in enumerate(mobile):
            radius=float(np.hypot(triangle[:,0],triangle[:,2]).max())
            lo=np.array([-radius,triangle[:,1].min(),-radius])
            hi=np.array([radius,triangle[:,1].max(),radius])
            candidates=np.flatnonzero(np.all(fhi>=lo-tolerance,axis=1)&np.all(flo<=hi+tolerance,axis=1))
            counts['broadphase_pairs']+=len(candidates)
            def chunk(row):
                nonlocal last_update
                if time.monotonic()-last_update>=1:
                    save(current_moving_triangle=mobile_id,current_chunk=row);last_update=time.monotonic()
            for fixed_id,clear,hits in checker.interval_pair_results(triangle,fixed,candidates,0,angle,depth,tolerance,totals,chunk):
                counts['pairs_completed']+=1
                if clear:
                    counts['pairs_proven_clear']+=1
                else:
                    assert len(witnesses)<64,'Diagnostic record cap exceeded; NONPASS remains partial'
                    counts['nonclear_pairs']+=1;states.clear()
                    scalar=namespace['interval_clear'](triangle,fixed[fixed_id],0,angle,depth,tolerance)
                    assert scalar==(clear,hits),'Original scalar and admitted helper disagree'
                    assert states and len(states)<=8191
                    left,right,remaining,middle,radius,displacement,gap=states[-1]
                    if hits==1:
                        assert gap<=tolerance
                        kind='ORIGINAL_SCALAR_CONTACT_OR_TOLERANCE_TOUCH';counts['scalar_confirmed_contact_pairs']+=1
                    else:
                        assert hits==0 and remaining<=0 and gap>tolerance and gap<=displacement+tolerance
                        kind='ORIGINAL_SCALAR_DEPTH_UNRESOLVED_POSITIVE_GAP';counts['scalar_depth_unresolved_pairs']+=1
                    posed=checker.turn(triangle,middle)
                    assert checker.separation(posed,fixed[fixed_id])==gap
                    item={'schema':'chicago-t2797-original-scalar-false-leaf-witness-v1','classification':kind,
                        'batch_result':[bool(clear),int(hits)],'original_scalar_result':[bool(scalar[0]),int(scalar[1])],
                        'moving_subset_index':mobile_id,'fixed_subset_index':int(fixed_id),
                        'moving':occurrence(global_mobile[mobile_id]),'fixed':occurrence(global_fixed[fixed_id]),
                        'actual_decisive_false_leaf':{'start_rad':left,'end_rad':right,'start_deg':math.degrees(left),
                            'end_deg':math.degrees(right),'remaining_depth':remaining,'midpoint_rad':middle,
                            'midpoint_deg':math.degrees(middle),'radius_m':radius,'displacement_bound_m':displacement,
                            'scalar_normalized_SAT_gap_m':gap,'contact_threshold_m':tolerance,'clear_threshold_m':displacement+tolerance,
                            'SAT_gap_is_NOT_MTD':True},
                        'moving_closed_hinge_local_triangle_m':triangle.tolist(),'fixed_hinge_local_triangle_m':fixed[fixed_id].tolist(),
                        'moving_at_witness_hinge_local_triangle_m':posed.tolist(),
                        'moving_at_witness_ROOT_triangle_m':(posed+pivot).tolist(),
                        'fixed_ROOT_triangle_m':(fixed[fixed_id]+pivot).tolist(),
                        'DFS_state_columns':['start_rad','end_rad','remaining_depth','midpoint_rad','radius_m','displacement_bound_m','gap_m'],
                        'original_ordered_DFS_states':states.copy(),'actual_interval_or_geometry_qualification':False}
                    name=f'witness-{len(witnesses)+1:02d}-moving{mobile_id}-fixed{fixed_id}.json'
                    encoded=json.dumps(item,indent=2,allow_nan=False).encode()
                    current_size=sum(f.stat().st_size for f in output.rglob('*') if f.is_file())
                    assert current_size+len(encoded)+2*1024*1024<=128*1024*1024, 'Witness output cap/headroom reached; retain partial NONPASS'
                    atom(output/name,item)
                    witnesses.append({'path':name,'sha256':digest(output/name),'classification':kind,
                        'moving_subset_index':mobile_id,'fixed_subset_index':int(fixed_id),
                        'moving_part':item['moving']['actual_part_name'],'fixed_part':item['fixed']['actual_part_name']})
                    save(current_moving_triangle=mobile_id)
                if time.monotonic()-last_update>=1:
                    save(current_moving_triangle=mobile_id);last_update=time.monotonic()
            counts['moving_triangles_completed']+=1
        assert counts['moving_triangles_completed']==2824
        assert counts['broadphase_pairs']==counts['pairs_completed']==2100050
        assert counts['pairs_proven_clear']==2100008 and counts['nonclear_pairs']==42
        assert len(witnesses)==42 and counts['scalar_confirmed_contact_pairs']+counts['scalar_depth_unresolved_pairs']==42
        completed=True
    except BaseException as error:
        failure={'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc()}
        raise
    finally:
        after=snapshot();atom(output/'PARENTS-AFTER.json',after)
        assert before==after
        size=sum(f.stat().st_size for f in output.rglob('*') if f.is_file())
        assert size<=128*1024*1024,'Owned output cap exceeded; no diagnostic completion'
        save(state='DIAGNOSTIC_COMPLETE_REQUIRES_ENGINEERING_REVIEW' if completed else 'NONPASS_PARTIAL_DIAGNOSTIC',
             failure=failure,all_immutable_parents_unchanged=before==after,owned_output_bytes=size,
             full_proof_rerun=False,geometry_or_flag_changes=False)
        print(json.dumps({'state':progress['state'],'counts':counts,'elapsed_s':progress['elapsed_s'],
            'qualification':False,'PASS':False,'final_PASS':False}),flush=True)


if __name__=='__main__':
    main()
