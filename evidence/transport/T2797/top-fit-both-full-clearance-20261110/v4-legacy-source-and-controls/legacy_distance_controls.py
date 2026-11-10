from pathlib import Path
import hashlib,json,math,sys,time
import numpy as np

SOURCE=Path('/tmp/chicago-t2795-brougham-door-foundation-20261110/chicago/4d/tools/transport/brougham')
sys.path.insert(0,str(SOURCE))
from check_near import read,world_nodes
from check_mid import bind_parts
import check_door_aperture as authority

output=Path(sys.argv[1]);assert not output.exists()
old=Path('/tmp/T2797-DOOR-PRODUCER-PREP-20261110/inputs/brougham-source.glb')
candidate=Path('/tmp/T2797-CAP-UP-PRODUCER-STRUCTURE-ATTEMPT1-20261110/results/candidate/near')
original,sb=read(old);doc,tb=read(candidate/'brougham-door-study.glb')
receipt=json.loads((candidate/'DOOR-SOURCE-RECEIPT.json').read_text())
report,=[r for r in receipt['top_fit_parts']if r['name']=='door_transferred_closed_upper_side_header']
sid=report['source_occurrence_id'];tid,=[i for i,p in enumerate(doc['extras']['parts'])if p['name']==report['name']and p['frame']=='vehicle_door_right']
source_bind=bind_parts(original,sb);target_bind=bind_parts(doc,tb)
assert any(name=='vehicle_door_right'for _,name in target_bind[tid]['node_path'])
def geometry(binding,world):
    points=np.frombuffer(binding['chunks']['POSITION'],dtype='<f4').reshape((-1,3)).astype(float)+world[binding['node_path'][-1][0]]
    normals=np.frombuffer(binding['chunks']['NORMAL'],dtype='<f4').reshape((-1,3))
    return points,normals
source,sn=geometry(source_bind[sid],world_nodes(original));actual,an=geometry(target_bind[tid],world_nodes(doc))
triangles=source.reshape((-1,3,3));sn=sn.reshape((-1,3,3));assert len(actual)==1185
partial=Path('/tmp/T2797-HEADER-NORMAL-DIAG-ATTEMPT1-20261110/results/PARTIAL.json')
assert hashlib.sha256(partial.read_bytes()).hexdigest()=='bcc43db74c82e27476851926fdc3cf83745f546bb9c323b6cfaead0ddae5521b'
record,=json.loads(partial.read_text())['rows'];assert record['detail']=='near'and len(record['failures'])==6
counts=[];true_distance=authority.check_top_fit.point_triangle_distance
def observe(points,triangles):
    counts.append(len(triangles))
    return true_distance(points,triangles)
authority.check_top_fit.point_triangle_distance=observe
started=time.monotonic()
try:worst=authority.original_surface_error(actual,an,triangles,sn)
finally:authority.check_top_fit.point_triangle_distance=true_distance
native_seconds=time.monotonic()-started
assert worst<=2e-7 and len(counts)==1185 and max(counts)<=len(triangles)
rows=[{'case':'all1185actualnearheaderPNvertices','maximum_world_distance_m':worst,
       'normal_filtered_facets':{'minimum':min(counts),'maximum':max(counts),'total':sum(counts),'source_facets':len(triangles)},
       'seconds':native_seconds,'result':'EXPECTED_NATIVE_ACCEPTANCE'}]
for failed in record['failures']:
    index=failed['actual_vertex_index'];assert np.array_equal(actual[index],failed['actual_ROOT_point'])
    distance=authority.original_surface_error(actual[index:index+1],an[index:index+1],triangles,sn)
    assert distance<=2e-7 and failed['old_membership_rejects_nominated']is True
    rows.append({'case':'recordedfalsepoint '+str(index),'actual_normal_unchanged':True,
        'world_distance_m':distance,'result':'EXPECTED_RECORDED_FALSE_FAILURE_ACCEPTANCE'})

simple=np.array([[[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]]]);normals=np.array([[[0.,0.,1.]]*3]);normal=np.array([[0.,0.,1.]])
def expected_error(label,point,n,expected):
    caught=None
    try:authority.original_surface_error(np.asarray([point]),np.asarray([n]),simple,normals)
    except AssertionError as exc:caught=str(exc)
    assert caught==expected,(label,caught)
    rows.append({'case':label,'observed_rejection':caught,'result':'EXPECTED_GUARD_REJECTION'})
inside=2e-7*(1-1e-4);outside=2e-7*(1+1e-4)
for d,label in [(inside,'inside'),(outside,'outside')]:
    for region,p in [('plane',[.25,.25,d]),('edge',[.5,-d,0.]),('vertex',[-d/math.sqrt(2),-d/math.sqrt(2),0.])]:
        if label=='inside':
            distance=authority.original_surface_error(np.asarray([p]),normal,simple,normals)
            assert distance<=2e-7;rows.append({'case':region+' justinside unchanged WORLD bound','world_distance_m':distance,'result':'EXPECTED_ACCEPTANCE'})
        else:expected_error(region+' justbeyond unchanged WORLD bound',p,normal[0],'Transferred header/pillar closed-WORLD surface changed')
authority.original_surface_error(np.array([[.25,.25,0.]]),np.array([[inside,0.,1.]]),simple,normals)
rows.append({'case':'normal justinside unchanged component bound','result':'EXPECTED_ACCEPTANCE'})
expected_error('normal justbeyond unchanged component bound',[.25,.25,0.],[outside,0.,1.],'Transferred header/pillar normal is not from an original facet')
expected_error('whole transferred WORLD_SHIFT message retained',[.25,.25,.02],normal[0],'Transferred header/pillar closed-WORLD surface changed')
assert authority.CLOSED_WORLD_POSITION_TOLERANCE_M==2e-7
result={'schema':'chicago-t2797-legacy-world-distance-caller-controls-v1','result':'LEGACY_DISTANCE_CONTROLS_PASS',
    'actual_vertices':1185,'recorded_old_false_failures':6,'world_tolerance_m':2e-7,'normal_component_tolerance':2e-7,
    'rows':rows,'geometry_modified':False,'qualification':False}
output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)
