from pathlib import Path
import hashlib,json,math,sys
import numpy as np

SOURCE=Path('/tmp/chicago-t2795-brougham-door-foundation-20261110/chicago/4d/tools/transport/brougham')
sys.path.insert(0,str(SOURCE))
from check_near import read,world_nodes
from check_mid import bind_parts
from check_top_fit import point_triangle_distance,POSITION_TOLERANCE

output=Path(sys.argv[1]);assert not output.exists()
assert POSITION_TOLERANCE==2e-7
old=Path('/tmp/T2797-DOOR-PRODUCER-PREP-20261110/inputs')
candidates=Path('/tmp/T2797-ORDINARY-TOP-FIT-PRODUCER-STRUCTURE-ATTEMPT1-20261110/results/candidate')
diagnosis=Path('/tmp/T2797-TOP-FIT-POINT-DIAG-ATTEMPT2-20261110/results/RESULT.json')
assert hashlib.sha256(diagnosis.read_bytes()).hexdigest()=='0a7468b137c2c044bbb5f8d82bba353303f177062ff212dcc1e49df12f545f79'
expected=json.loads(diagnosis.read_text());rows=[];count=0;old_rejected=0
for detail,filename in [('near','brougham-source.glb'),('mid','brougham-mid-source.glb')]:
    original,binary=read(old/filename);doc,data=read(candidates/detail/'brougham-door-study.glb')
    original_bind=bind_parts(original,binary);target_bind=bind_parts(doc,data)
    original_world=world_nodes(original);target_world=world_nodes(doc)
    receipt=json.loads((candidates/detail/'DOOR-SOURCE-RECEIPT.json').read_text())
    for report in receipt['top_fit_parts']:
        sid=report['source_occurrence_id']
        target,=[i for i,p in enumerate(doc['extras']['parts'])if p['name']==report['name']and p['frame']=='vehicle_door_right']
        assert any(name=='vehicle_door_right'for _,name in target_bind[target]['node_path'])
        def geometry(binding,world):
            local=np.frombuffer(binding['chunks']['POSITION'],dtype='<f4').reshape((-1,3)).astype(float)
            return (local+world[binding['node_path'][-1][0]]).reshape((-1,3,3))
        src=geometry(original_bind[sid],original_world);actual=geometry(target_bind[target],target_world)
        ids=np.asarray(report['original_source_triangle_for_retained'],dtype=int)
        distance=point_triangle_distance(actual.reshape((-1,3)),np.repeat(src[ids],3,axis=0))
        reference,=[r for r in expected['rows']if r['detail']==detail and r['part']==report['name']]
        assert len(distance)==reference['actual_corners'] and np.all(distance<=POSITION_TOLERANCE)
        assert abs(float(distance.max())-reference['max_all_corners_nearest_world_distance_m'])<1e-14
        count+=len(distance);old_rejected+=reference['current_barycentric_rejected_corners']
        rows.append({'case':detail+' '+report['name'],'actual_corners':len(distance),
            'maximum_world_distance_m':float(distance.max()),'result':'EXPECTED_NATIVE_ROUNDTRIP_ACCEPTANCE'})
assert count==3558 and old_rejected==404

# The first actual thin source facet demonstrates the original false rejection.
example=expected['rows'][0]['rejected_corners'][0]
p=np.asarray(example['actual_ROOT_point']);tri=np.asarray(example['original_ROOT_triangle'])
s,t=example['failing_gram_barycentric_s_t'];slack=example['old_dimensionless_slack']
assert not(s>=-slack and t>=-slack and s+t<=1+slack)
assert example['actual_equals_original_vertex_roundtrip'] is True
actual=float(point_triangle_distance(p[None],tri[None])[0]);assert actual<=POSITION_TOLERANCE
assert abs(actual-example['closest_world_distance_m'])<1e-14
rows.append({'case':'actual long-thin source facet Float32 corner roundtrip','old_guard_falsely_rejects':True,
    'world_distance_m':actual,'result':'EXPECTED_THIN_TRIANGLE_ACCEPTANCE'})

# Exact face, finite-edge and vertex Voronoi regions: each point just beyond
# the unchanged world bound must reject. Interior plane-only or infinite-edge
# substitutes fail these cases. Same-distance inside points must accept.
triangle=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
for label,d,accept in [('inside',2e-7*(1-1e-4),True),('outside',2e-7*(1+1e-4),False)]:
    points=np.array([[.25,.25,d],[.5,-d,0.],[-d/math.sqrt(2),-d/math.sqrt(2),0.]])
    distances=point_triangle_distance(points,np.repeat(triangle[None],3,axis=0))
    assert np.all(np.abs(distances-d)<1e-15)
    assert np.all((distances<=POSITION_TOLERANCE)==accept)
    for region,dist in zip(['plane','edge','vertex'],distances):
        rows.append({'case':region+' '+label+' unchanged WORLD bound','world_distance_m':float(dist),
            'expected_acceptance':accept,'result':'EXPECTED_ACCEPTANCE'if accept else'EXPECTED_DISTANCE_REJECTION'})
normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);normal/=np.linalg.norm(normal)
escaped=tri.mean(axis=0)+normal*(POSITION_TOLERANCE*(1+1e-4))
distance=float(point_triangle_distance(escaped[None],tri[None])[0])
assert distance>POSITION_TOLERANCE
rows.append({'case':'actual thin facet strictly over-bound plane displacement','world_distance_m':distance,'result':'EXPECTED_DISTANCE_REJECTION'})
result={'schema':'chicago-t2797-top-fit-world-distance-controls-v1','result':'FOCUSED_DISTANCE_CONTROLS_PASS',
    'unchanged_position_tolerance_m':POSITION_TOLERANCE,'native_corners':count,'old_false_rejected_corners':old_rejected,
    'rows':rows,'qualification':False,'geometry_or_recipe_modified':False}
output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result),flush=True)
