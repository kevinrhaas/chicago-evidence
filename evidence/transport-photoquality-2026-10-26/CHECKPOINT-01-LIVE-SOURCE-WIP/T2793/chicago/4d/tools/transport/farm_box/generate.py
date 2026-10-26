#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build a versioned original farm-box master; never rewrite the placed W01.

Existing measured W01 envelopes are retained. Board/grain construction, shaped
wheel sections, hubs, axle retention and load-bearing frame are reconstructed.
No third-party mesh is copied. Modern CC0 wood pixels retain their existing
source attribution; they do not date a wagon or identify a timber species.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

from mesh import Mesh, cross, sub

ROOT = Path(__file__).resolve().parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def wood_source():
    """Read only the three credited native wood maps from the authored capsule."""
    root = ROOT/'assets/authored/transport/wagon_parked_fine_wood'
    index_raw = (root/'surface.json').read_bytes()
    index = json.loads(index_raw)
    payload = (root/'surface.bin').read_bytes()
    if sha(payload) != index['payload_sha256']:
        raise ValueError('Changed original CC0 wood capsule')
    views = index['append_buffer_views']
    base = 110  # The existing append capsule's explicit first bufferView index.
    images = []
    for image in index['images'][:3]:
        v = views[image['bufferView']-base]
        offset = v['byteOffset']-index['parent_binary_bytes']
        raw = payload[offset:offset+v['byteLength']]
        if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Wood capsule image bounds')
        images.append(raw)
    return images, {'source': 'Rob Tuytel, fine_grained_wood, Poly Haven, CC0-1.0',
                    'capsule_sha256': sha(payload), 'index_sha256': sha(index_raw),
                    'image_sha256': [sha(x) for x in images],
                    'scope': 'Modern optical analogy; no historical species/coating claim'}


def spoke(mesh, name, frame, angle, radius, sides, material):
    """An oval tapered timber, with real lengthwise grain and explicit tenons."""
    vertices, uv, faces = [], [], []
    stations = [(.075, .026, .023), (.14, .030, .027),
                (radius-.10, .020, .022), (radius-.055, .017, .018)]
    for distance, width, depth in stations:
        for j in range(sides):
            a = math.tau*(j+.5)/sides
            x, tangent = width/2*math.cos(a), depth/2*math.sin(a)
            vertices.append((x, distance*math.cos(angle)-tangent*math.sin(angle),
                             distance*math.sin(angle)+tangent*math.cos(angle)))
            uv.append((distance/2.24, j/sides*.18))
    faces.append(tuple(range(sides-1, -1, -1)))
    faces.append(tuple(range((len(stations)-1)*sides, len(stations)*sides)))
    for row in range(len(stations)-1):
        for j in range(sides):
            k = (j+1) % sides
            faces.append((row*sides+j, row*sides+k, (row+1)*sides+k, (row+1)*sides+j))
    # Determine outward winding from the timber's own centre, not screen space.
    centre = (0, math.fsum(s[0] for s in stations)/len(stations)*math.cos(angle),
              math.fsum(s[0] for s in stations)/len(stations)*math.sin(angle))
    for i, face in enumerate(faces):
        a, b, c = [vertices[k] for k in face[:3]]
        normal = cross(sub(b, a), sub(c, a))
        midpoint = tuple(math.fsum(vertices[k][axis] for k in face)/len(face)-centre[axis] for axis in range(3))
        if math.fsum(x*y for x, y in zip(normal, midpoint)) < 0:
            faces[i] = tuple(reversed(face))
    mesh.surface(name, frame, material, vertices, faces, uv)


def build(p, detail):
    mesh = Mesh()
    level = p['details'][detail]
    root = mesh.node('vehicle_root')
    body = mesh.node('vehicle_body', root)
    length, width, height = p['body_m']
    bed = p['bed_top_m']
    track = p['wheel_center_track_m']/2
    materials = [
        {'name': 'oiled_timber', 'pbrMetallicRoughness': {'baseColorFactor': [.77,.71,.61,1], 'metallicFactor': 0, 'roughnessFactor': 1,
          'baseColorTexture': {'index': 0}, 'metallicRoughnessTexture': {'index': 2}}, 'normalTexture': {'index': 1, 'scale': .35}},
        {'name': 'timber_light', 'pbrMetallicRoughness': {'baseColorFactor': [.92,.85,.73,1], 'metallicFactor': 0, 'roughnessFactor': 1,
          'baseColorTexture': {'index': 0}, 'metallicRoughnessTexture': {'index': 2}}, 'normalTexture': {'index': 1, 'scale': .35}},
        {'name': 'aged_green_paint', 'pbrMetallicRoughness': {'baseColorFactor': [.19,.23,.13,1], 'metallicFactor': 0, 'roughnessFactor': .76,
          'baseColorTexture': {'index': 0}}, 'normalTexture': {'index': 1, 'scale': .18}},
        {'name': 'forged_iron', 'pbrMetallicRoughness': {'baseColorFactor': [.105,.115,.12,1], 'metallicFactor': .8, 'roughnessFactor': .58}},
        {'name': 'reconstructed_cut_end', 'pbrMetallicRoughness': {'baseColorFactor': [.30,.21,.12,1], 'metallicFactor': 0, 'roughnessFactor': .9}}
    ]
    floor_count, courses = p['body_boards']['floor'], p['body_boards']['side_courses']
    gap = p['body_boards']['gap_m']
    for i in range(floor_count):
        mesh.box(f'floor_plank_{i}', body, (width/floor_count-gap,.07,length),
                 (-width/2+(i+.5)*width/floor_count,bed-.035,0), i % 2, phase=i*.293)
    for side in [-1, 1]:
        for course in range(courses):
            mesh.box(f'side_{side}_{course}', body, (.035,height/courses-gap,length),
                     (side*width/2,bed+(course+.5)*height/courses,0), course % 2, phase=course*.371+side*.11)
        mesh.box(f'top_rail_{side}',body,(.055,.04,length+.05),(side*width/2,bed+height+.01,0),2)
        for k, z in enumerate([-1.4,-.5,.5,1.4]):
            z *= length/3.05
            mesh.box(f'stake_{side}_{k}',body,(.045,height+.11,.055),(side*(width/2+.03),bed+height/2-.025,z),2,grain_axis=1)
            if level['fasteners']:
                for y in [bed+.09,bed+height-.1]:
                    mesh.box(f'stake_head_{side}_{k}_{y}',body,(.010,.016,.016),(side*(width/2+.057),y,z),3)
        # Sill carries the floor onto the cross-bearers, rather than floating at
        # the top of a rectangular bolster. Exact concealed joints are invented.
        mesh.box(f'body_sill_{side}',body,(.085,.105,length),(side*(width/2-.12),bed-.1225,0),2)
    for end in [-1,1]:
        for course in range(courses):
            mesh.box(f'end_{end}_{course}',body,(width,height/courses-gap,.035),
                     (0,bed+(course+.5)*height/courses,end*length/2),course % 2,grain_axis=0,phase=course*.127)
    frames = {}
    for which in ['rear', 'front']:
        radius = p['wheel_radius_m'][which]
        z = p['axle_stations_z_m'][which]
        frame = mesh.node('vehicle_steer_front' if which == 'front' else 'vehicle_running_gear_rear',root,(0,radius,z))
        frames[which] = frame
        mesh.box(which+'_axle_beam',frame,(2*track+.14,.065,.075),(0,0,0),2,grain_axis=0)
        bearer_y = bed-.175-radius
        mesh.box(which+'_cross_bearer',frame,(width+.12,.09,.15),(0,bearer_y,0),2,grain_axis=0)
        for side in [-1,1]:
            mesh.box(which+f'_bearing_{side}',frame,(.13,max(.035,bearer_y-.045),.12),
                     (side*(width/2-.12),(.0325+bearer_y-.045)/2,0),0,grain_axis=1)
        for side,label in [(1,'left'),(-1,'right')]:
            wheel = mesh.node(f'vehicle_wheel_{which}_{label}',frame,(side*track,0,0))
            n = level['wheel_sides']
            # Rolled tyre edges and rounded timber felloe edges; extrema retain
            # exactly the prior wheel radius and 70 mm total tyre width.
            mesh.lathe_x('iron_tyre',wheel,[(-.035,radius-.004),(-.031,radius),(.031,radius),(.035,radius-.004),
                          (.035,radius-.018),(-.035,radius-.018)],(0,0,0),3,n)
            mesh.lathe_x('timber_felloe',wheel,[(-.031,radius-.021),(-.027,radius-.018),(.027,radius-.018),(.031,radius-.021),
                          (.031,radius-.061),(.027,radius-.065),(-.027,radius-.065),(-.031,radius-.061)],(0,0,0),0,n)
            # Shaped hub barrel, retaining the existing 220 mm width. The axle
            # bore is closed by an actual end cap on the visible outside.
            mesh.lathe_x('shaped_hub',wheel,[(-.11,.063),(-.09,.083),(-.045,.095),(.045,.095),(.09,.083),(.11,.063),
                          (.11,.018),(-.11,.018)],(0,0,0),2,n)
            for axial in [-.087,.087]:
                mesh.lathe_x('hub_band',wheel,[(axial-.009,.087),(axial+.009,.087),(axial+.009,.077),(axial-.009,.077)],
                             (0,0,0),3,n)
            mesh.disc_x('axle_retaining_cap',wheel,.043,side*.112,(0,0,0),3,n,side)
            if level['fasteners']:
                mesh.box('square_axle_nut',wheel,(.014,.029,.029),(side*.119,0,0),3)
            for k in range(p['wheel_spokes']):
                spoke(mesh,f'spoke_{k}',wheel,math.tau*k/p['wheel_spokes'],radius,level['spoke_sides'],0)
    front = frames['front']
    mesh.box('reach',root,(.09,.10,p['axle_stations_z_m']['front']-p['axle_stations_z_m']['rear']+.18),
             (0,.61,-.09),2)
    mesh.box('front_kingbolt',front,(.035,.35,.035),(0,.14,0),3,grain_axis=1)
    for side in [-1,1]:
        mesh.box(f'front_hound_{side}',front,(.07,.15,.86),(side*.08,.10,-.02),2)
    tongue = mesh.node('vehicle_tongue',front,(0,0,.35))
    tongue_length = p['tongue_length_m']
    mesh.box('tongue_timber',tongue,(.055,.055,tongue_length),(0,0,tongue_length/2),0)
    for z in [.10,.30,tongue_length-.10]:
        mesh.box('tongue_strap_'+str(z),tongue,(.062,.063,.025),(0,0,z),3)
    for name,parent,pos in [('vehicle_hitch_team',tongue,(0,0,tongue_length)),
                            ('vehicle_hitch_single',front,(0,0,.35)),
                            ('vehicle_seat_driver',body,(0,1.15,1.10)),
                            ('vehicle_seat_passenger_01',body,(0,1.15,-.45)),
                            ('vehicle_board_left',body,(.85,0,.5)),
                            ('vehicle_board_right',body,(-.85,0,.5)),
                            ('vehicle_camera_ride',body,(0,1.8,.2)),
                            ('vehicle_collision',root,(0,0,0))]:
        mesh.node(name,parent,pos)
    images, credit = wood_source()
    triangle_count = sum(len(v[0])//9 for v in mesh.batches.values())
    sidecar = {'schema': 'chicago_farm_box_master_v1', 'asset_id': p['asset_id'], 'detail': detail,
               'units': 'm', 'up_axis': '+Y', 'forward_axis': '+Z', 'left_axis': '+X',
               'status': p['status'], 'grade': 'reconstructed', 'photographic_acceptance': False,
               'parameters': p, 'parts': mesh.parts, 'material_source': credit,
               'statistics': {'triangles': triangle_count, 'draw_batches': len(mesh.batches), 'frames_and_sockets': len(mesh.nodes)},
               'socket_policy': 'Proposed unloaded interfaces only; no seat, hitch, collision or boarding qualification',
               'source_limits': p['source_limits']}
    return mesh.glb(materials,images,sidecar), sidecar


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--parameters',type=Path,required=True)
    cli.add_argument('--output-dir',type=Path,required=True)
    cli.add_argument('--detail',choices=['near','mid','far','all'],default='all')
    args = cli.parse_args()
    raw = args.parameters.read_bytes()
    recipe = json.loads(raw)
    if recipe['schema'] != 'chicago_farm_box_master_v1':
        raise ValueError('Explicit farm-box recipe required')
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError('Fresh output directory required; existing master is never overwritten')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for detail in recipe['details'] if args.detail == 'all' else [args.detail]:
        glb, sidecar = build(recipe,detail)
        sidecar['recipe_sha256'] = sha(raw)
        sidecar['glb_sha256'] = sha(glb)
        (args.output_dir/f'farm-box-{detail}.glb').write_bytes(glb)
        (args.output_dir/f'farm-box-{detail}.json').write_text(json.dumps(sidecar,indent=2)+'\n')
        print(json.dumps({'detail': detail,'bytes': len(glb),'sha256': sha(glb),**sidecar['statistics']}))


if __name__ == '__main__':
    main()
