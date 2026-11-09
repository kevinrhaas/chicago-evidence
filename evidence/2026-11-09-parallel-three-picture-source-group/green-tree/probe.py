"""Actual accumulator and recipe scope for a data-only Green Tree roof trial."""
from pathlib import Path
import copy, dataclasses, hashlib, json, math, subprocess, sys, types
from unittest.mock import patch

REPO = Path('/tmp/nov9-group-green_tree')
APP = REPO / 'chicago/4d'
OUT = Path('/tmp/nov9-green-tree-group')
sys.path.insert(0, str(APP/'generators'))
sys.modules.setdefault('bpy', types.ModuleType('bpy'))
from archetypes import frame_tavern as builder
from archetypes.frame_tavern_params import from_phase
from common.mesh import MeshBuilder
from mesh_inputs import structure_inputs_doc, structure_inputs_sha

path = 'chicago/4d/data/structures/green_tree_tavern.json'
before = json.loads(subprocess.check_output(['git', 'show', 'HEAD:'+path], cwd=REPO))
after = json.loads((REPO/path).read_bytes())
reverted = copy.deepcopy(after)
reverted['phases'][0]['form']['enclosed_left_annex']['value']['shoulder']['roof_high_m'] = 4.0
reverted['phases'][0]['form']['enclosed_left_annex']['note'] = before['phases'][0]['form']['enclosed_left_annex']['note']
assert reverted == before, 'Only one existing control and its construction note may change'
assert after['phases'][0]['form']['enclosed_left_annex']['note'].startswith(before['phases'][0]['form']['enclosed_left_annex']['note'])
p0, p1 = [from_phase(r['phases'][0], r) for r in (before, after)]
p0.validate(); p1.validate()
d0, d1 = [dataclasses.asdict(p) for p in (p0, p1)]
a0, a1 = d0.pop('enclosed_left_annex'), d1.pop('enclosed_left_annex')
assert d0 == d1
a1 = copy.deepcopy(a1); a1['shoulder']['roof_high_m'] = a0['shoulder']['roof_high_m']
assert a0 == a1
assert p0.left_annex_parts == p1.left_annex_parts, 'Physical consumers keep the same occupied rings and entrance'
with patch.object(MeshBuilder, 'to_object', lambda b, mats=None: (b, mats)), patch.object(builder, 'simple_material', lambda n, *a, **kw: (n, a, kw)):
    b0, m0 = builder.build(p0, 'shoulder-roof-scope')
    b1, m1 = builder.build(p1, 'shoulder-roof-scope')
assert len(b0.verts) == len(b1.verts)
assert (b0.faces, b0.mat_index, b0.conf, b0.named, m0) == (b1.faces, b1.mat_index, b1.conf, b1.named, m1)
changed = [i for i, (v0, v1) in enumerate(zip(b0.verts, b1.verts)) if v0 != v1]
assert changed
for i in changed:
    v0, v1 = b0.verts[i], b1.verts[i]
    assert v0[:2] == v1[:2], 'Only shoulder roof/infill vertical positions change'
    assert 7.37-1e-8 <= v0[0] <= 11.47+1e-8 and 5.34-1e-8 <= v0[1] <= 12.64+1e-8
    assert min(v0[2], v1[2]) >= 2.8
affected_faces = [i for i, face in enumerate(b0.faces) if any(v in changed for v in face)]
affected_materials = sorted({b0.mat_index[i] for i in affected_faces})
assert set(affected_materials) == {builder.M_WALL, builder.M_ROOF}
for i in changed:
    assert b0.conf[i] == b1.conf[i] == 1.0
def bounds(mesh):
    return [[min(v[i] for v in mesh.verts) for i in range(3)], [max(v[i] for v in mesh.verts) for i in range(3)]]
assert bounds(b0) == bounds(b1)
binding = json.loads(Path('/tmp/nov9-sauganash-native-binding.json').read_bytes())
controls = []
for row in binding['affected']:
    if row['structure_id'] == 'green_tree_tavern':
        continue
    record = json.loads((REPO/row['record']['path']).read_bytes())
    phase_id = row['current_inputs_doc']['phase']
    phase = next(p for p in record['phases'] if p['id'] == phase_id)
    actual = structure_inputs_sha(record, phase)
    assert actual == row['current_inputs_sha256'], (row['asset_key'], actual, row['current_inputs_sha256'])
    controls.append({'asset_key': row['asset_key'], 'current_input_sha256': actual})
assert len(controls) == 24
for name, record in [('before', before), ('trial', after)]:
    (OUT/(name+'-inputs.json')).write_text(json.dumps(structure_inputs_doc(record, record['phases'][0]), indent=2)+'\n')
receipt = {
    'status': 'ACTUAL_DATA_SCOPE_PARAMS_ACCUMULATOR_AND_24_FOREIGN_RECIPES_PASS_NOT_NATIVE',
    'base': subprocess.check_output(['git','rev-parse','HEAD'], cwd=REPO).decode().strip(),
    'only_source_file': path,
    'before_inputs_sha256': structure_inputs_sha(before, before['phases'][0]),
    'trial_inputs_sha256': structure_inputs_sha(after, after['phases'][0]),
    'native_scope': {'structure_ids': ['green_tree_tavern'], 'default_outputs': 1, 'versions': 0, 'shared_producer_changed': False},
    'control': {'roof_high_m': [4.0,4.6], 'roof_low_m': [3.2,3.2], 'actual_slope_degrees': [math.degrees(math.atan(.8/3.6)), math.degrees(math.atan(1.4/3.6))]},
    'mesh': {'vertices': len(b0.verts), 'polygons': len(b0.faces), 'triangles': sum(len(f)-2 for f in b0.faces), 'changed_vertices': len(changed), 'changed_face_material_ids': affected_materials, 'unchanged_bounds': bounds(b0), 'topology_confidence_named_materials_identical': True, 'xy_identical_everywhere': True,
             'actual_changed_positions': [{'index': i, 'before': b0.verts[i], 'after': b1.verts[i]} for i in changed]},
    'occupied_frames_and_entrance_exact': True,
    'other_24_frame_recipes_exact': controls,
    'qualification_limits': 'No Blender/export, native readback, picture render, camera fit, current body/yard/terrain/phone/desktop or whole-image acceptance is claimed.'
}
(OUT/'ACTUAL-SCOPE-PASS.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k: receipt[k] for k in ['status','before_inputs_sha256','trial_inputs_sha256','native_scope']}))
print('Accumulator:',len(changed),'vertical-only vertices; topology, confidence, materials, full bounds and physical frames unchanged; all24 other recipes exact')
