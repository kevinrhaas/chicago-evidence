from pathlib import Path
import copy,hashlib,json,struct,sys,time,traceback
from types import SimpleNamespace

PREP=Path(__file__).parent
APP=Path('/tmp/chicago-t2795-brougham-door-foundation-20261110/chicago/4d')
SOURCE=APP/'tools/transport/brougham'
OUTPUT=Path(sys.argv[1]);assert not OUTPUT.exists();OUTPUT.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE/'check_door_aperture.py')==sha(PREP/'check_door_aperture.py')=='1fc6d79c1d28c4a8a661b62b6fcae92ecc4764e87eedd61c73d8ccfa2117faf1'
sys.path.insert(0,str(SOURCE))
from check_door_aperture import verify_structure
from check_near import read,component

inputs=Path('/tmp/T2797-DOOR-PRODUCER-PREP-20261110/inputs')
candidates=Path(sys.argv[2])
parents=[SOURCE/'check_door_aperture.py',SOURCE/'door_aperture.py',SOURCE/'door-aperture.json']
for detail,name in [('near','brougham-source.glb'),('mid','brougham-mid-source.glb')]:
    parents.extend([inputs/name,candidates/detail/'brougham-door-study.glb',candidates/detail/'DOOR-SOURCE-RECEIPT.json'])
before={str(p):sha(p) for p in parents};(OUTPUT/'IMMUTABLE-PARENTS-BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')

def save_glb(path,doc,binary):
    doc['buffers'][0]['byteLength']=len(binary)
    j=json.dumps(doc,separators=(',',':'),allow_nan=False).encode();j+=b' '*(-len(j)%4)
    binary=bytes(binary)+b'\0'*(-len(binary)%4)
    path.write_bytes(struct.pack('<III',0x46546c67,2,28+len(j)+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary)

def alter(doc,binary,receipt,kind):
    binary=bytearray(binary);parts=doc['extras']['parts']
    def part_for(test):
        matches=[p for p in parts if test(p)];assert matches
        return matches[0]
    def mesh_for(part):
        mi=next(i for i,m in enumerate(doc['meshes']) if m['name']==f"surface_{part['frame']}_{part['material']}")
        return mi,doc['meshes'][mi]['primitives'][0]
    if kind in ['wheel_POSITION','lamp_NORMAL','leaf_closed_WORLD_POSITION']:
        if kind=='wheel_POSITION':part=part_for(lambda p:p['frame'].startswith('vehicle_wheel_'));attribute='POSITION'
        elif kind=='lamp_NORMAL':part=part_for(lambda p:'lamp' in p['name'] or 'lamp' in p['frame']);attribute='NORMAL'
        else:part=part_for(lambda p:p['name']=='deep_U_closed_door' and p['frame']=='vehicle_door_right');attribute='POSITION'
        mi,primitive=mesh_for(part);a=doc['accessors'][primitive['attributes'][attribute]];v=doc['bufferViews'][a['bufferView']]
        offset=v.get('byteOffset',0)+a.get('byteOffset',0)+part['triangle_start_in_batch']*3*12
        old=struct.unpack_from('<f',binary,offset)[0];struct.pack_into('<f',binary,offset,old+.02)
        return doc,binary,{'actual_mutation':kind,'part':part['name'],'attribute':attribute,
            'byte_offset':offset,'old':old,'new':struct.unpack_from('<f',binary,offset)[0]},part['name']
    if kind=='required_glass_misparented_same_WORLD':
        part=part_for(lambda p:p['name']=='side_door_glass' and p['frame']=='vehicle_door_right')
        mi,primitive=mesh_for(part);ni=next(i for i,n in enumerate(doc['nodes']) if n.get('mesh')==mi)
        door=next(i for i,n in enumerate(doc['nodes']) if n['name']=='vehicle_door_right')
        body=next(i for i,n in enumerate(doc['nodes']) if n['name']=='vehicle_body')
        doc['nodes'][door]['children'].remove(ni);doc['nodes'][body].setdefault('children',[]).append(ni)
        doc['nodes'][ni]['translation']=list(doc['nodes'][door]['translation'])
        return doc,binary,{'actual_mutation':kind,'part':part['name'],'closed_world_positions_intentionally_preserved':True},part['name']
    if kind=='step_terminal_ATTACHMENT_POSITION':
        part=part_for(lambda p:p['name']=='step_support' and p['frame']=='vehicle_body')
        mi,primitive=mesh_for(part);positions=list(struct.iter_unpack('<fff',component(doc,binary,part,'POSITION')))
        assert max(q[0] for q in positions)<0
        vertex=next(i for i,q in enumerate(positions) if q[1]>=.735 or q[1]<=.455)
        a=doc['accessors'][primitive['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        offset=v.get('byteOffset',0)+a.get('byteOffset',0)+part['triangle_start_in_batch']*36+vertex*12
        old=struct.unpack_from('<f',binary,offset)[0];struct.pack_into('<f',binary,offset,old+.02)
        return doc,binary,{'actual_mutation':kind,'part':part['name'],'terminal_vertex':vertex,'old':old,'new':struct.unpack_from('<f',binary,offset)[0]},part['name']
    if kind=='transferred_header_closed_WORLD_SHIFT':
        part=part_for(lambda p:p['name']=='door_transferred_closed_upper_side_header')
        mi,primitive=mesh_for(part);a=doc['accessors'][primitive['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        start=v.get('byteOffset',0)+a.get('byteOffset',0)+part['triangle_start_in_batch']*36
        for offset in range(start,start+part['triangles']*36,12):
            old=struct.unpack_from('<f',binary,offset)[0];struct.pack_into('<f',binary,offset,old+.02)
        return doc,binary,{'actual_mutation':kind,'whole_part_translation_x_m':.02,'source_finish_and_normal_stream_unchanged':True},part['name']
    if kind=='hubcap_duplicate_name_collapse':
        caps=[i for i,n in enumerate(doc['nodes']) if n['name']=='hubcap'];assert len(caps)==4
        mesh_children=[next(c for c in doc['nodes'][i]['children'] if 'mesh' in doc['nodes'][c]) for i in caps]
        for parent,child in zip(caps[:-1],mesh_children[:-1]):
            doc['nodes'][parent]['children'].remove(child);doc['nodes'][caps[-1]].setdefault('children',[]).append(child)
        return doc,binary,{'actual_mutation':kind,'four_original_local_PN_streams_unchanged':True,'three_actual_mesh_children_reparented_to_fourth_same_named_hubcap':True},'bright_hubcap_rim'
    if kind in ['untargeted_frame_POSITION','protected_roof_POSITION','top_cap_stock','top_cap_gap']:
        if kind=='untargeted_frame_POSITION':
            part=part_for(lambda p:p['name']=='side_window_frame' and p['frame']=='vehicle_door_right')
        elif kind=='protected_roof_POSITION':
            part=part_for(lambda p:p['name']=='roof_underside' and p['frame']=='vehicle_body')
        else:
            part=part_for(lambda p:p['name']=='door_top_fit_frame_cap')
        _,primitive=mesh_for(part);a=doc['accessors'][primitive['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        start=v.get('byteOffset',0)+a.get('byteOffset',0)+part['triangle_start_in_batch']*36
        points=list(struct.iter_unpack('<fff',component(doc,binary,part,'POSITION')))
        if kind=='untargeted_frame_POSITION':
            vertex=next(i for i,p in enumerate(points)if p[1]<1.8)
            struct.pack_into('<f',binary,start+vertex*12,points[vertex][0]+.002)
            mutation={'actual_mutation':kind,'actual_untargeted_lower_frame_vertex':vertex,'delta_x_m':.002}
        elif kind=='protected_roof_POSITION':
            struct.pack_into('<f',binary,start,points[0][0]+.002)
            mutation={'actual_mutation':kind,'protected_source_roof_vertex_changed_x_m':.002}
        elif kind=='top_cap_stock':
            for i,p in enumerate(points):struct.pack_into('<f',binary,start+i*12+4,p[1]-.010)
            mutation={'actual_mutation':kind,'whole_actual_new_cap_lowered_y_m':.010,'source_roof_glass_and_retained_frame_unchanged':True}
        else:
            assert part['triangles']>=2
            for label in ['POSITION','NORMAL']:
                aa=doc['accessors'][primitive['attributes'][label]];vv=doc['bufferViews'][aa['bufferView']]
                ss=vv.get('byteOffset',0)+aa.get('byteOffset',0)+part['triangle_start_in_batch']*36
                binary[ss:ss+36]=binary[ss+36:ss+72]
            mutation={'actual_mutation':kind,'first_real_top_cap_facet_replaced_by_next_PN':True,'all_inventory_counts_and_source_map_unchanged':True}
        return doc,binary,mutation,part['name']
    if kind in ['backing_below_floor', 'stem_ring_section_distorted', 'fixed_link_detached', 'floor_cap_gap']:
        if kind=='backing_below_floor':
            part=part_for(lambda p:p['name']=='door_original_curved_backing')
        elif kind=='stem_ring_section_distorted':
            part=part_for(lambda p:p['name']=='step_support' and p['frame']=='vehicle_body')
        elif kind=='fixed_link_detached':
            part=part_for(lambda p:p['name']=='fixed_step_floor_carry_link')
        else:
            part=part_for(lambda p:p['name']=='door_backing_floor_edge_cap')
        _,primitive=mesh_for(part);a=doc['accessors'][primitive['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        start=v.get('byteOffset',0)+a.get('byteOffset',0)+part['triangle_start_in_batch']*36
        points=list(struct.iter_unpack('<fff',component(doc,binary,part,'POSITION')))
        if kind=='backing_below_floor':
            vertex=min(range(len(points)),key=lambda i:points[i][1]);offset=start+vertex*12+4
            struct.pack_into('<f',binary,offset,.90)
            mutation={'actual_mutation':kind,'vertex':vertex,'root_y_m':.90}
        elif kind=='stem_ring_section_distorted':
            original=next(p for p in points if .496 < p[1] < .505)
            changed=0
            for i,p in enumerate(points):
                if p==original:
                    struct.pack_into('<f',binary,start+i*12,p[0]+.001);changed+=1
            assert changed>=2
            mutation={'actual_mutation':kind,'one_actual_corner_all_duplicate_occurrences_moved_x_m':.001,'duplicate_occurrences':changed,'original_corner':original}
        elif kind=='fixed_link_detached':
            for i,p in enumerate(points):struct.pack_into('<f',binary,start+i*12,p[0]+.02)
            mutation={'actual_mutation':kind,'whole_actual_link_translation_x_m':.02,'normals_unchanged':True}
        else:
            # Duplicate a real adjoining emitted facet instead of deleting a
            # metadata range. All counts/bindings/normals remain real; the
            # checker must reject actual area/coverage, not stale checksums.
            assert part['triangles']>=2
            for label in ['POSITION','NORMAL']:
                aa=doc['accessors'][primitive['attributes'][label]];vv=doc['bufferViews'][aa['bufferView']]
                ss=vv.get('byteOffset',0)+aa.get('byteOffset',0)+part['triangle_start_in_batch']*36
                binary[ss:ss+36]=binary[ss+36:ss+72]
            mutation={'actual_mutation':kind,'first_real_cap_facet_replaced_by_second':True,'inventory_counts_and_source_bindings_unchanged':True}
        return doc,binary,mutation,part['name']
    assert kind=='fixed_backing_blocks_aperture'
    part=part_for(lambda p:p['name']=='door_original_curved_backing')
    positions=component(doc,binary,part,'POSITION');normals=component(doc,binary,part,'NORMAL')
    door=next(n for n in doc['nodes'] if n['name']=='vehicle_door_right');pivot=door['translation']
    shifted=b''.join(struct.pack('<fff',*(p[k]+pivot[k] for k in range(3))) for p in struct.iter_unpack('<fff',positions))
    attributes={}
    for label,data in [('POSITION',shifted),('NORMAL',normals)]:
        off=len(binary);binary.extend(data);vi=len(doc['bufferViews']);doc['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':len(data),'target':34962})
        pts=list(struct.iter_unpack('<fff',data));ai=len(doc['accessors']);doc['accessors'].append({'bufferView':vi,'componentType':5126,'count':len(pts),'type':'VEC3','min':[min(p[k] for p in pts) for k in range(3)],'max':[max(p[k] for p in pts) for k in range(3)]});attributes[label]=ai
    mi=len(doc['meshes']);doc['meshes'].append({'name':'surface_negative_fixed_backing_0','primitives':[{'attributes':attributes,'material':part['material']}]})
    frame=len(doc['nodes']);ni=frame+1
    doc['nodes'].append({'name':'negative_fixed_backing','children':[ni]});doc['nodes'].append({'name':'surface_negative_fixed_backing_0','mesh':mi})
    body=next(n for n in doc['nodes'] if n['name']=='vehicle_body');body.setdefault('children',[]).append(frame)
    doc['extras']['parts'].append({'name':'negative_fixed_backing','frame':'negative_fixed_backing','frame_node_index':frame,'material':part['material'],'triangle_start_in_batch':0,'triangles':part['triangles']})
    return doc,binary,{'actual_mutation':kind,'added_actual_fixed_triangles':part['triangles'],'original_moving_backing_unchanged':True},'backing'

rows=[];start=time.monotonic()
try:
    for detail,name in [('near','brougham-source.glb'),('mid','brougham-mid-source.glb')]:
        source=inputs/name;candidate=candidates/detail/'brougham-door-study.glb';receipt_path=candidates/detail/'DOOR-SOURCE-RECEIPT.json'
        args=SimpleNamespace(input=source,candidate=candidate,source_receipt=receipt_path,recipe=SOURCE/'door-aperture.json')
        baseline_ok=False
        try:
            summary,_=verify_structure(args);baseline_ok=True
            (OUTPUT/f'{detail}-STRUCTURE-ONLY.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
            rows.append({'detail':detail,'case':'immutable_baseline','result':'STRUCTURE_ONLY_PASS','candidate_sha256':sha(candidate)})
        except Exception as exc:
            rows.append({'detail':detail,'case':'immutable_baseline','result':'STRUCTURE_ONLY_FAIL','exception_type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc()})
            raise
        for kind in ['fixed_backing_blocks_aperture','wheel_POSITION','lamp_NORMAL','required_glass_misparented_same_WORLD','leaf_closed_WORLD_POSITION','hubcap_duplicate_name_collapse','step_terminal_ATTACHMENT_POSITION','transferred_header_closed_WORLD_SHIFT','backing_below_floor','stem_ring_section_distorted','fixed_link_detached','floor_cap_gap','untargeted_frame_POSITION','protected_roof_POSITION','top_cap_stock','top_cap_gap']:
            case=OUTPUT/f'{detail}-{kind}';case.mkdir()
            total=sum(f.stat().st_size for f in OUTPUT.parent.rglob('*') if f.is_file())
            assert total+candidate.stat().st_size+receipt_path.stat().st_size+1024*1024<=128*1024*1024,'Owned128MiBoutputcap reached; retainNONPASS, neveromitcontrols'
            doc,binary=read(candidate);receipt=json.loads(receipt_path.read_text())
            doc,binary,mutation,part_name=alter(doc,binary,receipt,kind)
            mutated=case/'negative.glb';save_glb(mutated,doc,binary)
            receipt.update(output_sha256=sha(mutated),bytes=mutated.stat().st_size)
            rebound=case/'REBOUND-NEGATIVE-SOURCE-RECEIPT.json';rebound.write_text(json.dumps(receipt,indent=2)+'\n')
            negative=SimpleNamespace(input=source,candidate=mutated,source_receipt=rebound,recipe=SOURCE/'door-aperture.json')
            expected={'fixed_backing_blocks_aperture':'fixed wall/trim surface','wheel_POSITION':'POSITION','lamp_NORMAL':'NORMAL','required_glass_misparented_same_WORLD':'not under vehicle_door_right','leaf_closed_WORLD_POSITION':'closed-WORLD POSITION','hubcap_duplicate_name_collapse':'Protected closed-WORLD position changed','step_terminal_ATTACHMENT_POSITION':'Original step terminal attachment moved','transferred_header_closed_WORLD_SHIFT':'Transferred header/pillar closed-WORLD surface changed','backing_below_floor':'Added backing remains below','stem_ring_section_distorted':'Source stem ring is not a rigid translation','fixed_link_detached':'Fixed carry link terminal attachment moved','floor_cap_gap':['Actual backing floor cut is not fully capped','Backing cap has an actual gap/overlap','Backing cap misses actual cut-skin width'],'untargeted_frame_POSITION':['Retained top-fit facet escaped','Retained top-fit closed-WORLD surface changed','Untargeted original frame closed-WORLD POSITION changed'],'protected_roof_POSITION':'POSITION','top_cap_stock':'Top-fit actual crest stock or glass-edge cover is too thin','top_cap_gap':['Top-fit cap has an actual gap/overlap','Top-fit actual cut was left uncapped','Top-fit cap misses original source thickness','Top-fit frame/cap is not closed']}[kind]
            caught=None
            try:verify_structure(negative)
            except Exception as exc:caught={'exception_type':type(exc).__name__,'error':str(exc)}
            good=baseline_ok and caught is not None and caught['exception_type']=='AssertionError' and any(e in caught['error'] for e in (expected if isinstance(expected,list) else [expected]))
            row={'detail':detail,'case':kind,'result':'EXPECTED_GEOMETRY_REJECTION' if good else 'CONTROL_NONPASS',
                 'mutation':mutation,'candidate_sha256':sha(mutated),'receipt_sha256':sha(rebound),
                 'candidate_and_receipt_checksums_refreshed':True,'expected_error_substring':expected,'observed_rejection':caught}
            (case/'CONTROL-RESULT.json').write_text(json.dumps(row,indent=2,allow_nan=False)+'\n');rows.append(row)
            if not good:raise AssertionError('Actual baseline/control failure; no automatic continuation: '+detail+' '+kind)
finally:
    after={str(p):sha(p) for p in parents};(OUTPUT/'IMMUTABLE-PARENTS-AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
    result={'schema':'chicago-brougham-ordinary-top-fit-structure-controls-attempt-v1','phase':'STRUCTURE_ONLY','rows':rows,'elapsed_s':time.monotonic()-start,
        'immutable_parent_hashes_unchanged':before==after,'checker_sha256':sha(SOURCE/'check_door_aperture.py'),
        'sweep_run':False,'qualification_flags_changed':False,'adoption':False,
        'result':'STRUCTURE_ONLY_CONTROLS_PASS' if before==after and len(rows)==34 and all(r['result'] in ['STRUCTURE_ONLY_PASS','EXPECTED_GEOMETRY_REJECTION'] for r in rows) else 'STRUCTURE_ONLY_CONTROLS_NONPASS'}
    (OUTPUT/'STRUCTURE-CONTROLS-RESULT.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)
    assert before==after
assert result['result']=='STRUCTURE_ONLY_CONTROLS_PASS'
