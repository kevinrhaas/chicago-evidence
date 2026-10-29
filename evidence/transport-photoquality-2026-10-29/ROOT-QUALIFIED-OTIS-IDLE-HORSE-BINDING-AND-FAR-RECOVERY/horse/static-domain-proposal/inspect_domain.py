"""Static source geometry/skin domain proposal; does not generate skin or poses."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

APP = Path('/tmp/chicago-horse-20261029/chicago/4d')
OUT = Path(__file__).resolve().parent
raw = (APP / 'assets/authored/transport/horse_standing/horse-sevket-natural-planted-idle-v1.glb').read_bytes()
n = struct.unpack_from('<I', raw, 12)[0]
d = json.loads(raw[20:20 + n])
binary = raw[28 + n:]
fixtures = APP / 'tools/transport/horse_eye_smooth_normals_v1/fixtures'
reference = json.loads((fixtures / 'cpu-rest-protection.json').read_text())
ancestry = json.loads((fixtures / 'anatomy-r3-full-derivation.json').read_text())['source_boundary']['hoof_refinement']


def accessor(index):
    a = d['accessors'][index]
    v = d['bufferViews'][a['bufferView']]
    count = {'VEC3': 3, 'VEC4': 4, 'SCALAR': 1}[a['type']]
    fmt = {5126: 'f', 5123: 'H', 5125: 'I', 5121: 'B'}[a['componentType']]
    start = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    stride = v.get('byteStride', count * struct.calcsize(fmt))
    return [list(struct.unpack_from('<' + fmt * count, binary, start + row * stride)) for row in range(a['count'])]


meshes = []
for m in d['meshes']:
    p = m['primitives'][0]
    a = p['attributes']
    meshes.append({'positions': accessor(a['POSITION']), 'joints': accessor(a['JOINTS_0']),
                   'weights': accessor(a['WEIGHTS_0']), 'indices': [x[0] for x in accessor(p['indices'])]})
foot = {}
for label, row in reference['contacts'].items():
    faces = [face for old in row['source_triangle_ids'] for face in ancestry['source_face_to_children'][old]]
    foot[label] = sorted({v for face in faces for v in meshes[1]['indices'][3 * face:3 * face + 3]})
footset = {v for ids in foot.values() for v in ids}
tail = set(reference['tail_vertex_ids'])
assert len(tail) == 969
masks = {'BODY_head_neck': [], 'HAIR_head_neck': [], 'BODY_tail_dock': [], 'HAIR_original_tail_component': sorted(tail)}
for mesh, name in [(0, 'HAIR_head_neck'), (1, 'BODY_head_neck')]:
    masks[name] = [i for i, (x, y, z) in enumerate(meshes[mesh]['positions']) if y > 1.04 and z > .28]
masks['BODY_tail_dock'] = [i for i, (x, y, z) in enumerate(meshes[1]['positions']) if abs(x) < .22 and z < -.78 and y > 1.08]
assert not footset.intersection(set(masks['BODY_head_neck']) | set(masks['BODY_tail_dock']))
components = {}
for mesh, m in enumerate(meshes):
    count = len(m['positions'])
    parents = list(range(count))

    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parents[b] = a

    welded = {}
    for i, p in enumerate(m['positions']):
        key = tuple(round(value / 1e-6) for value in p)
        if key in welded:
            union(i, welded[key])
        else:
            welded[key] = i
    for i in range(0, len(m['indices']), 3):
        a, b, c = m['indices'][i:i + 3]
        union(a, b)
        union(a, c)
    groups = {}
    for i in range(count):
        groups.setdefault(find(i), []).append(i)
    rows = []
    for ids in groups.values():
        points = [m['positions'][i] for i in ids]
        rows.append({'vertices': len(ids), 'minimum': [min(p[k] for p in points) for k in range(3)],
                     'maximum': [max(p[k] for p in points) for k in range(3)],
                     'tail_rows': len(set(ids) & tail) if mesh == 0 else 0})
    components[str(mesh)] = {'welded_indexed_component_count': len(rows),
                             'largest_components': sorted(rows, key=lambda r: -r['vertices'])[:12]}
statistics = {}
for name, ids in masks.items():
    mesh = 0 if name.startswith('HAIR') else 1
    points = [meshes[mesh]['positions'][i] for i in ids]
    allowed = {1, 2, 3} if 'head_neck' in name else {1, 4, 5}
    other = [sum(w > 0 and joint not in allowed for joint, w in zip(meshes[mesh]['joints'][i], meshes[mesh]['weights'][i])) for i in ids]
    statistics[name] = {'rows': len(ids), 'bounds_min_m': [min(p[k] for p in points) for k in range(3)],
                        'bounds_max_m': [max(p[k] for p in points) for k in range(3)],
                        'maximum_positive_other_joint_components': max(other),
                        'rows_with_positive_other_joints': sum(n > 0 for n in other)}
neck, head = [0, 1.3, .55], [0, 1.48, 1.03]
axis = [head[k] - neck[k] for k in range(3)]
axis2 = sum(value * value for value in axis)
jaw = []
for vertex in [1300, 1316, 1233]:
    point = meshes[1]['positions'][vertex]
    parameter = sum((point[k] - neck[k]) * axis[k] for k in range(3)) / axis2
    jaw.append({'vertex': vertex, 'position': point, 'head_axis_parameter': parameter,
                'inside_declared_BODY_head_neck_domain': vertex in masks['BODY_head_neck'],
                'old_joint_slots': meshes[1]['joints'][vertex], 'old_weight_slots': meshes[1]['weights'][vertex]})
record = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'STATIC_DOMAIN_PROPOSAL_ONLY_NO_NEW_BINDING_OR_POSES',
          'source_parent_sha256': hashlib.sha256(raw).hexdigest(),
          'source_original_reference925_sha256': '925fac957110b9b57b95c5abfed17fabf29f868b173f38f0569d984dd9999a48',
          'motion_amplitudes_unchanged': True,
          'landmarks': {'body': [0, 1.05, 0], 'neck': neck, 'head': head, 'tail_base': [0, 1.28, -.85], 'tail_tip': [0, .6, -1.1]},
          'allowed_row_masks': masks, 'mask_statistics': statistics,
          'foot_patches_original_counts': {k: len(v) for k, v in foot.items()},
          'all_complete_hoof_patch_rows_excluded': True, 'EYE_rows_change_permitted': False,
          'first_failed_jaw_triangle': jaw, 'welded_source_connected_components': components,
          'mask_definition': {
              'head_neck': 'BODY and HAIR rows y>1.04m,z>0.28m; EYE excluded; delta must taper to zero at fixed domain boundary.',
              'tail_dock': 'BODY rows abs(x)<0.22m,z<-0.78m,y>1.08m and all969 original isolated HAIR tail rows; BODY delta must taper to zero at boundary.',
              'no_unlisted_rows': 'All source joint/weight slots remain byte-identical outside the explicit versioned row lists. Domain does not depend on failing poses or changed acceptance bounds.'},
          'candidate_binding_export': 'UNRUN', 'numerical_pose_evaluation': 'UNRUN', 'new_native129': 'UNRUN', 'source_intake': False}
(OUT / 'STATIC-DOMAIN-PROPOSAL-01.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'mask_statistics': statistics, 'jaw': jaw, 'source_components': components}, indent=2))
