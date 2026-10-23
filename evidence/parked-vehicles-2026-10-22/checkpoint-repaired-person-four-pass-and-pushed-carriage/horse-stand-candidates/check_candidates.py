"""Finite source-plan footprint screening; not drawn-ground or browser acceptance."""
import hashlib, json, math, subprocess
from pathlib import Path

REPO = '/workspace/chicago-waistcoat'
HEAD = 'a086cd7dab31935f52adcb1ca8494a12726f9f27'
OUT = Path(__file__).resolve().parent
pins = {}
def data(path):
    raw = subprocess.check_output(['git', '-C', REPO, 'show', HEAD + ':chicago/4d/' + path])
    pins[path] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)

def segment_distance(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    den = dx*dx+dy*dy
    t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
    return math.hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dy)
def inside(p, poly):
    yes = False
    for a, b in zip(poly, poly[1:]+poly[:1]):
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < (b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]: yes = not yes
    return yes
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def intersects(a,b,c,d):
    return cross(a,b,c)*cross(a,b,d) <= 0 and cross(c,d,a)*cross(c,d,b) <= 0 and max(min(a[0],b[0]),min(c[0],d[0])) <= min(max(a[0],b[0]),max(c[0],d[0])) and max(min(a[1],b[1]),min(c[1],d[1])) <= min(max(a[1],b[1]),max(c[1],d[1]))
def gap(poly, other):
    edges = list(zip(poly,poly[1:]+poly[:1])); others = list(zip(other,other[1:]+other[:1]))
    if any(inside(p,other) for p in poly) or any(inside(p,poly) for p in other) or any(intersects(a,b,c,d) for a,b in edges for c,d in others): return 0
    return min([segment_distance(p,a,b) for p in poly for a,b in others]+[segment_distance(p,a,b) for p in other for a,b in edges])
def rectangle(bounds, position, bearing, pad=0):
    # Canonical horse X / forward Z -> ENU, using the production yaw convention.
    yaw=math.pi-math.radians(bearing);co,si=math.cos(yaw),math.sin(yaw)
    return [[position[0]+co*x+si*z,position[1]+si*x-co*z] for x,z in [(bounds[0][0]-pad,bounds[0][2]-pad),(bounds[1][0]+pad,bounds[0][2]-pad),(bounds[1][0]+pad,bounds[1][2]+pad),(bounds[0][0]-pad,bounds[1][2]+pad)]]
def structure_poly(record):
    local=record.get('footprint',{}).get('polygon',[]);p=record.get('placement',{})
    if len(local)<3 or not all(k in p for k in ['local_e','local_n','rotation_deg']):return None
    co=math.cos(math.radians(p['rotation_deg']));si=math.sin(math.radians(p['rotation_deg']))
    return [[p['local_e']+co*x+si*y,p['local_n']-si*x+co*y] for x,y in local]

spec=data('data/transport/parked/horse-sevket-sidecar.json')
plan={
 '1812':{'id':'first_fort_stable_north_standing_horse_01','position':[1067.5,144.0],'bearing':0,'host':'first_fort_outer_stable_north'},
 '1904':{'id':'prairie_eighteenth_standing_horse_01','position':[1397.5,-3221.2],'bearing':178.99,'host':None},
}
for year, row in plan.items():
    scene=data('data/scenes/'+year+'.json');idx=data('data/sidecars/'+year+'/index.json')
    box=rectangle(spec['canonical_upright_bounds_m'],row['position'],row['bearing'],.15)
    obstacles=[]
    for item in idx['structures']:
        record=data('data/'+item['sidecar']);poly=structure_poly(record)
        if poly:obstacles.append({'id':item['id'],'gap_m':gap(box,poly)})
    row.update({'scene_date':scene['target_date'],'spawn_distance_m':math.dist(row['position'],[scene['spawn']['local_e'],scene['spawn']['local_n']]),'upright_source_aabb_plus_150mm_plan_box':box,'nearest_source_footprints':sorted(obstacles,key=lambda x:x['gap_m'])[:5],'all_source_footprints_nonoverlapping':all(x['gap_m']>0 for x in obstacles),'full_reach_at_spawn':math.dist(row['position'],[scene['spawn']['local_e'],scene['spawn']['local_n']])<70,'balanced_reach_at_spawn':math.dist(row['position'],[scene['spawn']['local_e'],scene['spawn']['local_n']])<40})
    if year=='1904':
        grid=data('data/street_grid/1904.json');roads=[(c['id'],q) for c in grid['carriageways'] for q in c.get('quads_local_m',[])]
        containing=[{'id':ident,'minimum_plan_box_corner_to_quad_edge_m':min(segment_distance(p,a,b) for p in box for a,b in zip(q,q[1:]+q[:1]))} for ident,q in roads if all(inside(p,q) for p in box)]
        row['containing_carriageway_quads']=containing
        trees=data('data/street_trees/1904.json')['trees'];row['nearest_tree_centres']=[{'id':t['id'],'distance_from_box_m':min(segment_distance([t['e'],t['n']],a,b) for a,b in zip(box,box[1:]+box[:1])),'kind':t['kind'],'scale':t['scale']} for t in sorted(trees,key=lambda t:math.dist(row['position'],[t['e'],t['n']]))[:3]]
        placements=data('data/transport/parked/placements.json')['scenes']['1904'];row['existing_vehicle_root_distances_m']={p['id']:math.dist(row['position'],p['at_local_enu_m']) for p in placements}
report={'source_head':HEAD,'scope':'Future placement source screening only. No actual drawn triangles, rig-envelope, ground support fit, flora/canopy collision, camera visibility or native/browser qualification. The150mm expansion is a disclosed planning cushion, not a measured full idle sweep.','planned_rows':plan,'input_sha256':pins,'activation':False}
(OUT/'SOURCE-SCREEN.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({year:{k:v for k,v in row.items() if k not in ['upright_source_aabb_plus_150mm_plan_box']} for year,row in plan.items()},indent=2))
