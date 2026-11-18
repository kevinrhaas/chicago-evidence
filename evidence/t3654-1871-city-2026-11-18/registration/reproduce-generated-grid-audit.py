#!/usr/bin/env python3
"""Read existing 1871 plan/JSON/GLB; never regenerate or write project files."""
from pathlib import Path
import datetime, hashlib, json, math, struct, subprocess, sys
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
load = lambda p: json.loads((root / p).read_text())
plan = load('data/context/1871/plan.json')
doc = load('data/context/1871.json')
streets = {r['id']: r for r in plan['streets']}
grid = plan['grid']; anchor = grid['anchor']
angle = math.radians(grid['angle_deg']); co, si = math.cos(angle), math.sin(angle)
def uv(p):
    e, n = p[0] - anchor[0], p[1] - anchor[1]
    return (co * e + si * n, -si * e + co * n)
def distance(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    den = dx * dx + dy * dy
    t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
    return math.hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dy)
def poly_distance(p, r):
    return min(distance(p, a, b) for a, b in zip(r['points'], r['points'][1:]))
def crossing(a, b, c, d, epsilon=1e-8):
    ax, ay, bx, by = b[0]-a[0], b[1]-a[1], d[0]-c[0], d[1]-c[1]
    det = ax*by-ay*bx
    if abs(det)<1e-8: return None
    x, y = c[0]-a[0], c[1]-a[1]
    t, u = (x*by-y*bx)/det, (x*ay-y*ax)/det
    if -epsilon<=t<=1+epsilon and -epsilon<=u<=1+epsilon:
        return [a[0]+t*ax, a[1]+t*ay]
def all_crossings(left, right):
    hits=[]
    for a,b in left:
        for c,d in right:
            q=crossing(a,b,c,d)
            if q is not None and not any(math.dist(q,p)<0.0001 for p in hits): hits.append(q)
    return hits
state, madison = streets['state_street'], streets['madison_street']
segments = lambda r: list(zip(r['points'],r['points'][1:]))
map_hits=all_crossings(segments(state),segments(madison))
assert len(map_hits)==1, map_hits
mapped=map_hits[0]
control=next(r for r in plan['map_control']['controls'] if r['id']=='M1')
assert control['local']==anchor
coef=plan['map_control']['coefficients'];px,py=control['pixel']
unrounded=[coef['a']*px+coef['b']*py+coef['c'],coef['d']*px+coef['e']*py+coef['f']]
json_rows=[]
for name in ['state_street','madison_street']:
    current=[s for s in doc['streets'] if s['street_id']==name]
    errs=[poly_distance(p,streets[name]) for s in current for p in [s['a'],s['b']]]
    json_rows.append({'id':name,'generated_segment_count':len(current),'max_rounded_endpoint_off_plan_polyline_m':max(errs),'mapped_crossing_to_generated_segment_m':min(distance(mapped,s['a'],s['b']) for s in current)})
all_mapped=[s for s in doc['streets'] if s.get('alignment')=='mapped_arterial']
all_endpoint_errors=[poly_distance(p,streets[s['street_id']]) for s in all_mapped for p in [s['a'],s['b']]]
# Read native portable GLB road quads. Mesh.ribbon writes four vertices per face:
# a+normal, a-normal, b-normal, b+normal. Opposite-edge averages recover its axis.
raw=(root/'data/context/1871/streets.glb').read_bytes()
assert struct.unpack_from('<4sII',raw)==(b'glTF',2,len(raw))
jslen,jstype=struct.unpack_from('<II',raw,12);assert jstype==0x4e4f534a
model=json.loads(raw[20:20+jslen]); bin_offset=20+jslen
bin_len,bin_type=struct.unpack_from('<II',raw,bin_offset);assert bin_type==0x004e4942
binary=memoryview(raw)[bin_offset+8:bin_offset+8+bin_len]
road_axes=[]
for node in model['nodes']:
    if node.get('extras',{}).get('layer')!='streets': continue
    assert not any(k in node for k in ['matrix','translation','rotation','scale'])
    for primitive in model['meshes'][node['mesh']]['primitives']:
        ac=model['accessors'][primitive['attributes']['POSITION']]
        assert ac['componentType']==5126 and ac['type']=='VEC3' and ac['count']%4==0
        view=model['bufferViews'][ac['bufferView']]
        start=view.get('byteOffset',0)+ac.get('byteOffset',0);stride=view.get('byteStride',12)
        vertices=[struct.unpack_from('<fff',binary,start+i*stride) for i in range(ac['count'])]
        for i in range(0,len(vertices),4):
            a,b,c,d=vertices[i:i+4]
            assert max(abs(p[1]-3.23) for p in [a,b,c,d])<0.00001
            road_axes.append(([(a[0]+b[0])/2,-(a[2]+b[2])/2],[(c[0]+d[0])/2,-(c[2]+d[2])/2]))
selected={name:[(a,b) for a,b in road_axes if max(poly_distance(a,streets[name]),poly_distance(b,streets[name]))<0.01] for name in ['state_street','madison_street']}
native_hits=all_crossings(selected['state_street'],selected['madison_street'])
assert native_hits, 'No native State/Madison crossing found'
native=min(native_hits,key=lambda p:math.dist(p,mapped));assert math.dist(native,mapped)<0.001
bearings=[]
for name in ['fullerton_avenue','madison_street','western_avenue','halsted_street','state_street']:
    r=streets[name];q=[uv(p) for p in r['points']];ns=abs(q[-1][0]-q[0][0])<abs(q[-1][1]-q[0][1]);cross_axis=0 if ns else 1
    vals=sorted(p[cross_axis] for p in q);representative=vals[len(vals)//2]
    de,dn=r['points'][-1][0]-r['points'][0][0],r['points'][-1][1]-r['points'][0][1]
    bearing=math.degrees(math.atan2(dn,de))%180;basis=(grid['angle_deg']+(90 if ns else 0))%180
    bearings.append({'id':name,'endpoint_bearing_mod_180_deg':bearing,'generic_axis_bearing_deg':basis,'bearing_difference_deg':bearing-basis,'max_cross_axis_deviation_from_generic_representative_m':max(abs(v-representative) for v in vals),'interpretation':'Describes a uniform fill-grid convention versus this traced, possibly bent road. It is not an error bound or a displacement applied to the named road.'})
paths=['data/context/1871/plan.json','data/context/1871.json','data/context/1871/streets.glb','generators/city_1871_emit.py','generators/city_context_emit.py','data/datum.json','data/traces/mitchell_1870_reprojection.json']
script=Path(__file__).read_text()
report={
 'id':'T-3654-generated-grid-follow-through','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'scope':'Read-only follow-through from stored geographic controls into existing generated street JSON and decoded native GLB. No generation, fitting, geometry change or browser test.',
 'conclusion':'No overlooked global street-grid shift/rotation bug. Named mapped arterials retain the fitted historical traces, while the uniform ordinary grid remains a declared reconstruction. Modern-dataset agreement must not be described as rendered historical-intersection accuracy.',
 'source_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
 'grid_convention':grid,
 'state_madison':{'control_id':'M1','modern_target_enu_m':anchor,'historical_map_pixel':control['pixel'],'unrounded_affine_projection_enu_m':unrounded,'unrounded_affine_residual_m':math.dist(unrounded,anchor),'mapped_polyline_crossing_enu_m':mapped,'mapped_crossing_distance_from_modern_target_m':math.dist(mapped,anchor),'generated_json':json_rows,'decoded_glb_crossing_enu_m':native,'decoded_glb_crossing_off_mapped_crossing_m':math.dist(native,mapped),'decoded_glb_crossing_distance_from_modern_target_m':math.dist(native,anchor),'decoded_glb_selected_quad_counts':{k:len(v) for k,v in selected.items()}},
 'all_mapped_generated_segments':{'count':len(all_mapped),'road_count':len({s['street_id'] for s in all_mapped}),'max_rounded_endpoint_off_retained_polyline_m':max(all_endpoint_errors),'note':'Measured from generated JSON rounded to centimetres, not an accuracy claim about the historical source. Native GLB State/Madison is decoded separately.'},
 'grid_vs_mapped_bearings':bearings,
 'preservation_rules':{'generator_en_uv':'generators/city_1871_emit.py:54-60','grid_reads_plan':'generators/city_1871_emit.py:304-311','mapped_roads_override_lattice':'generators/city_1871_emit.py:404-451','frontage_follows_mapped_roads':'generators/city_1871_emit.py:453-476','generated_road_and_walk_geometry':'generators/city_1871_emit.py:563-600','native_ribbon_quad_order':'generators/city_1871_emit.py:215-229','plan_grid':'data/context/1871/plan.json:6101','explicit_modern_anchor_convention':'data/context/1871/plan.json:8060'},
 'declared_planning_allowances_m':{k:plan['map_control'][k] for k in ['registration_planning_allowance_m','map_feature_generalization_allowance_m','outside_map_reconstruction_allowance_m']},
 'limitations':['The 22.57 m State/Madison displacement is the existing map-fit residual, not an additional generated-grid error.','The modern City-versus-OSM 2.023 m RMS cross-check concerns modern target consistency only; it does not replace the historical fit/check residuals.','The generic 0.71-degree lattice is a uniform reconstruction convention, not a fit claiming to reproduce every individual street bearing. Named arterial traces and their bridges are not moved onto it.','Peripheral streets beyond the Mitchell sheet remain reconstructed; declared planning allowances are not statistical confidence intervals or surveyed maximum errors.','Decoded GLB road-axis extraction uses the documented ribbon quad vertex order; it is a geometric read of the existing artifact, not a visual camera or walking test.','No older-year Google/Today correction was transplanted, and no coordinates or assets were changed.'],
 'reproduction':{'command':'python3 /tmp/t3654-audit-generated-grid.py /workspace/chicago/chicago/4d > /tmp/t3654-generated-grid-audit.json','prerequisites':'Python 3 standard library, Git, and the source files at the hashes above. No Blender, renderer, raster processing or network required.','script_sha256':hashlib.sha256(script.encode()).hexdigest(),'embedded_script':script}
}
print(json.dumps(report,indent=2,ensure_ascii=False))
