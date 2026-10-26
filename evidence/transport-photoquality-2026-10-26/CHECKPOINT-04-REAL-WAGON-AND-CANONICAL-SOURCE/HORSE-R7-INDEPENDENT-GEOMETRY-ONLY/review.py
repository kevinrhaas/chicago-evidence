from pathlib import Path
import hashlib, json, math, struct, sys, time
import numpy as np

ROOT = Path(__file__).resolve().parent
CODE = ROOT / 'source/chicago/4d/assets/authored/transport/horse_standing'
sys.path.insert(0, str(CODE))
import generate_anatomy_v2 as generator
import anatomy_profile_qualification as qualification

started = time.monotonic()
binding = json.loads((ROOT / 'BINDING.json').read_bytes())
receipt = json.loads((ROOT / 'DERIVATION-RECEIPT.json').read_bytes())
recipe = json.loads((ROOT / 'recipe.json').read_bytes())
for name, expected in binding['source_hashes'].items():
    assert hashlib.sha256((CODE / name).read_bytes()).hexdigest() == expected
assert hashlib.sha256((ROOT / 'recipe.json').read_bytes()).hexdigest() == binding['recipe_sha256']
app = Path('/tmp/chicago-photo-worker-t3088-20261026/chicago/4d')
parent_bytes = (app / 'assets/authored/transport/horse_standing' / generator.base.PARENT_FILE).read_bytes()
candidate_bytes = Path(binding['candidate_file']).read_bytes()
assert hashlib.sha256(parent_bytes).hexdigest() == receipt['parent_sha256']
assert hashlib.sha256(candidate_bytes).hexdigest() == binding['candidate_sha256']
assert len(candidate_bytes) == receipt['candidate_bytes'] < 4 * 1024 * 1024
parent, parent_bin = generator.base.read_glb(parent_bytes)
candidate, candidate_bin = generator.base.read_glb(candidate_bytes)
assert candidate_bin[:len(parent_bin)] == parent_bin
source = generator.read_attribute(parent, parent_bin, 203)
source_uv = generator.read_attribute(parent, parent_bin, 6)
source_joints = generator.read_attribute(parent, parent_bin, 205)
source_weights = generator.read_attribute(parent, parent_bin, 206)
source_indices = [row[0] for row in generator.read_attribute(parent, parent_bin, 7)]
source_faces = [source_indices[i:i+3] for i in range(0, len(source_indices), 3)]
primitive = candidate['meshes'][1]['primitives'][0]
positions = generator.read_attribute(candidate, candidate_bin, primitive['attributes']['POSITION'])
normals = generator.read_attribute(candidate, candidate_bin, primitive['attributes']['NORMAL'])
uv = generator.read_attribute(candidate, candidate_bin, primitive['attributes']['TEXCOORD_0'])
joints = generator.read_attribute(candidate, candidate_bin, primitive['attributes']['JOINTS_0'])
weights = generator.read_attribute(candidate, candidate_bin, primitive['attributes']['WEIGHTS_0'])
indices = [row[0] for row in generator.read_attribute(candidate, candidate_bin, primitive['indices'])]
faces = [indices[i:i+3] for i in range(0, len(indices), 3)]
assert uv[:len(source)] == source_uv
assert joints[:len(source)] == source_joints
assert weights[:len(source)] == source_weights
restored = json.loads(json.dumps(candidate))
restored['meshes'][1]['primitives'][0] = parent['meshes'][1]['primitives'][0]
restored['buffers'] = parent['buffers']
restored['accessors'] = restored['accessors'][:len(parent['accessors'])]
restored['bufferViews'] = restored['bufferViews'][:len(parent['bufferViews'])]
del restored['asset']['extras']['chicago4d_anatomy_master_v2']
assert restored == parent

topology = receipt['source_boundary']['hoof_refinement']
coefficients = qualification.source_coefficients(len(source), topology['added_vertices'])
assert len(coefficients) == len(positions)
reference = qualification.source_points(source, coefficients)
maximum_shift = max(math.dist(a, b) for a, b in zip(reference, positions))
assert maximum_shift <= recipe['maximum_body_displacement_m'] == .02
for vertex in topology['ground_support_anchor_vertex_ids']:
    assert positions[vertex] == source[vertex]

def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]

for i in range(len(source), len(positions)):
    assert uv[i] == tuple(f32(sum(source_uv[j][k] * w for j, w in coefficients[i].items())) for k in range(2))
    expected = {}
    for j, factor in coefficients[i].items():
        for joint, w in zip(source_joints[j], source_weights[j]):
            if w > 0:
                expected[joint] = expected.get(joint, 0.) + factor * w
    active = sorted(expected.items(), key=lambda row: (-row[1], row[0]))
    assert len(active) <= 4
    total = sum(w for _, w in active)
    assert joints[i] == tuple([joint for joint, _ in active] + [0] * (4-len(active)))
    assert weights[i] == tuple([f32(w/total) for _, w in active] + [0.] * (4-len(active)))

controls = qualification.self_test(generator.base.normal_transform)
mapping = topology['source_face_to_children']
assert len(mapping) == len(source_faces)
assert sorted(child for children in mapping for child in children) == list(range(len(faces)))
inside = outside = nonpositive_inside = 0
minimum_area = minimum_cofactor = minimum_jacobian = 1.
for parent_id, children in enumerate(mapping):
    original_ids = set(source_faces[parent_id])
    parent_points = [source[i] for i in source_faces[parent_id]]
    parent_normal = qualification.normal(parent_points)
    source_area_sum = np.zeros(3)
    for child in children:
        ids = faces[child]
        assert all(set(coefficients[i]) <= original_ids for i in ids)
        before, after = [reference[i] for i in ids], [positions[i] for i in ids]
        source_area_sum += qualification.normal(before)
        result = qualification.qualify_child(parent_normal, before, after,
            recipe['upper_lid_refinement']['regions'], lambda p: generator.deformation(p, recipe),
            generator.base.normal_transform, recipe['minimum_local_jacobian'])
        minimum_area = min(minimum_area, result['path']['minimum_area_ratio'])
        if result['region'] is None:
            outside += 1
            assert result['world_normal_dot'] > 0
        else:
            inside += 1
            nonpositive_inside += result['world_normal_dot'] <= 0
            minimum_cofactor = min(minimum_cofactor, result['cofactor_orientation_dot'])
            minimum_jacobian = min(minimum_jacobian, result['determinant'])
    assert np.linalg.norm(source_area_sum - parent_normal) <= max(1e-14, np.linalg.norm(parent_normal)*1e-10)

stored = receipt['source_boundary']['bounded_upper_lid_profile_qualification']
assert inside == stored['inside_lid_children']
assert outside == stored['outside_lid_children']
assert nonpositive_inside == len(stored['world_normal_nonpositive_inside'])
assert abs(minimum_area - stored['minimum_path_area_ratio']) < 1e-12
assert abs(minimum_cofactor - stored['minimum_cofactor_orientation_dot']) < 1e-12
assert abs(minimum_jacobian - stored['minimum_centroid_jacobian']) < 1e-12
assert hashlib.sha256(Path(binding['candidate_file']).read_bytes()).hexdigest() == binding['candidate_sha256']
result = {'status': 'PASS_INDEPENDENT_SERIALIZED_GEOMETRY_AND_SOURCE_REVIEW',
    'candidate_sha256': binding['candidate_sha256'], 'candidate_bytes':len(candidate_bytes),
    'body_children_checked': len(faces), 'inside_lid_children': inside, 'outside_old_guard_children':outside,
    'world_normal_nonpositive_inside': nonpositive_inside, 'minimum_area_ratio':minimum_area,
    'minimum_cofactor_orientation_dot':minimum_cofactor, 'minimum_centroid_jacobian':minimum_jacobian,
    'maximum_all_vertex_shift_m':maximum_shift,
    'parent_BIN_prefix_and_protected_JSON_exact':True,
    'original_UV_skin_rows_exact':True, 'new_UV_skin_rows_verified_from_original_ancestry':True,
    'source_face_children_coverage_area_and_winding_checked':True,
    'synthetic_controls':controls, 'seconds':time.monotonic()-started,
    'unqualified':['proper static crossings', 'fresh loaded129 deformation', 'actual native images',
        'photographic acceptance', 'application adoption/full preflight'],
    'application_edits':'NONE'}
(ROOT / 'INDEPENDENT-REVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
