from pathlib import Path
import hashlib,json,sys
import numpy as np

SOURCE=Path('/tmp/chicago-t2795-brougham-door-foundation-20261110/chicago/4d/tools/transport/brougham')
sys.path.insert(0,str(SOURCE))
from top_fit import edge_caps
from check_top_fit import verify_caps

output=Path(sys.argv[1]);assert not output.exists()
readback=Path('/workspace/.cloud-setup/queue-refresh-20261109/ROOT-CAP-LOCAL-PN-READBACK-20261110.json')
record=json.loads(readback.read_text());rows=[]
cases=[(row['detail'],np.asarray(bad['node_local_P'],dtype=float))
       for row in record for bad in row['bad_winding_or_area']]
assert len(cases)==2
cases.append(('synthetic exactly zero-width strip end',np.array([[0.,1.,0.],[1.,1.,1.],[-1.,1.,1.]])))
for name,triangle in cases:
    a,b,c=triangle
    assert b[2]==c[2] and a[2]<b[2]
    profile=[[float(a[2]),float(a[1])],[float(b[2]),float(b[1])]]
    # The real failure's low-Z quad has identical first two corners. Keep that
    # source topology; don't fix it by dropping its surviving actual triangle.
    quad=np.array([a,a,b,c]);assert np.array_equal(quad[0],quad[1])
    assert np.array_equal(np.cross(quad[1]-quad[0],quad[2]-quad[0]),np.zeros(3))
    skins=np.asarray([[a,b,b-[0.,.01,0.]],[a,c,c-[0.,.01,0.]]])
    encoded=np.concatenate([skins,np.zeros_like(skins)],axis=2)
    caps,report=edge_caps(encoded,np.zeros(3),profile)
    assert len(caps)==1,'Zero-width end must retain its one real closure facet'
    positions=caps[:,:,:3];normals=caps[:,:,3:]
    assert sorted(map(tuple,positions[0]))==sorted(map(tuple,triangle)), 'Actual encoded geometric triangle changed'
    cross=np.cross(positions[:,1]-positions[:,0],positions[:,2]-positions[:,0]);length=np.linalg.norm(cross,axis=1)
    assert np.all(length>1e-12) and np.all(cross[:,1]>0)
    assert np.abs(normals-cross[:,None]/length[:,None,None]).max()<1e-14
    positive=verify_caps(skins,positions,normals,profile)
    negative=positions[:,[0,2,1]].copy()
    neg_cross=np.cross(negative[:,1]-negative[:,0],negative[:,2]-negative[:,0])
    neg_normals=np.repeat((neg_cross/np.linalg.norm(neg_cross,axis=1)[:,None])[:,None],3,axis=1)
    error=None
    try:verify_caps(skins,negative,neg_normals,profile)
    except AssertionError as exc:error=str(exc)
    assert error=='Top-fit cap winding/area changed','Known inverted actual cap must reject even with matching actual normals'
    rows.append({'case':name,'source_zero_width_quad_first_cross_exactly_zero':True,
        'original_recorded_crossY':float(np.cross(b-a,c-a)[1]),
        'actual_corrected_crossY':float(cross[0,1]),'actual_cross_length':float(length[0]),
        'unordered_encoded_POSITION_and_triangle_area_unchanged':True,
        'actual_producer_ceiling_caps':report,'positive_actual_guard':positive,
        'known_downward_cap_with_true_normals_expected_rejection':error})
result={'schema':'chicago-t2797-encoded-ceiling-cap-orientation-controls-v1',
    'result':'CAP_ORIENTATION_CONTROLS_PASS','actual_recorded_bad_cases':2,
    'synthetic_collapsed_width_cases':1,'actual_inverted_negative_controls':3,
    'unchanged_cross_length_minimum':1e-12,'qualification':False,
    'recorded_readback_sha256':hashlib.sha256(readback.read_bytes()).hexdigest(),'rows':rows}
output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)
