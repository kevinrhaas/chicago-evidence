# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent emitted-array checks and targeted broken-geometry controls."""
from pathlib import Path
import copy
import hashlib
import json
import math
import sys

BODY = Path('/tmp/T1789-female-base-preparation-20261026/prepared_adult_female_25.json')
OUTPUT = Path(__file__).with_name('dress-source-v2.json')


def need(test, message):
    if not test:
        raise ValueError(message)


def validate(data, body):
    names = {b['name'] for b in body['skeleton']}
    need(data['skeleton'] == body['skeleton'] and len(names) == 56, 'shared skeleton changed')
    need(data['body_sha256'] == hashlib.sha256(BODY.read_bytes()).hexdigest(), 'body pin changed')
    semantic = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    need(data['body_semantic_sha256'] == semantic, 'body anatomy/UV/weights changed')
    need(len(data['materials']) == 4, 'material slots unexpectedly expanded')
    result = []
    for mesh in data['meshes']:
        count = len(mesh['positions_m'])
        need(count == len(mesh['uvs']) == len(mesh['weights']) and count > 0, 'incomplete mesh arrays')
        need(mesh['material'] in data['materials'], 'unknown material')
        for p, uv, weights in zip(mesh['positions_m'], mesh['uvs'], mesh['weights']):
            need(len(p) == 3 and all(math.isfinite(x) for x in p), 'nonfinite position')
            need(len(uv) == 2 and all(math.isfinite(x) for x in uv), 'nonfinite UV')
            need(1 <= len(weights) <= 4 and not(set(weights)-names), 'unknown/excess skin joints')
            # The native fitted-shoe helper retains explicit zero-valued
            # influences. The portable source contract permits nonnegative
            # normalized weights; all-zero or negative maps still fail.
            need(all(math.isfinite(w) and w >= 0 for w in weights.values()) and abs(math.fsum(weights.values())-1) < 1e-10,
                 'unnormalized skin weights')
        minarea = minuv = math.inf
        radial_min = math.inf
        flat = set(mesh.get('flat_face_indices', []))
        for fi, f in enumerate(mesh['triangles']):
            need(len(f) == len(set(f)) == 3 and all(type(i) is int and 0 <= i < count for i in f), 'invalid triangle')
            a, b, c = [mesh['positions_m'][i] for i in f]
            u, v = [[p[j]-a[j] for j in range(3)] for p in (b, c)]
            n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
            area = math.hypot(*n)
            need(area > 1e-15, 'degenerate geometry triangle')
            minarea = min(minarea, area/2)
            uv = mesh['corner_uvs'][fi] if 'corner_uvs' in mesh else [mesh['uvs'][i] for i in f]
            uvarea = abs((uv[1][0]-uv[0][0])*(uv[2][1]-uv[0][1])-(uv[1][1]-uv[0][1])*(uv[2][0]-uv[0][0]))/2
            need(uvarea > 1e-16, 'degenerate UV triangle')
            minuv = min(minuv, uvarea)
            if mesh['name'] in ('gathered_ankle_skirt', 'separate_plain_apron') and fi not in flat:
                radial = n[0]*(a[0]+b[0]+c[0])+n[2]*(a[2]+b[2]+c[2])
                need(radial > 0, 'outward cloth winding reversed')
                radial_min = min(radial_min, radial)
        if mesh['name'] == 'gathered_ankle_skirt':
            # The source support proof applies only to the unposed complete
            # core; physical1.5mm hem returns retain a conservative deduction.
            receipt = mesh['receipt']
            need(receipt['standing_body_core_clearance_m']-.0015 >= .015, 'skirt source support margin consumed')
            need(receipt['minimum_fold_panel_margin_m'] >= -1e-10, 'folds enter body core')
            need(all(w == {'pelvis': 1.} for w in mesh['weights']), 'unqualified dynamic skirt skinning')
            need(receipt['walking_or_seated_accepted'] is False, 'standing source relabelled as moving cloth')
        result.append(dict(name=mesh['name'], vertices=count, triangles=len(mesh['triangles']),
                           minimum_triangle_area_m2=minarea, minimum_uv_area=minuv,
                           outward_radial_min=None if radial_min == math.inf else radial_min))
    return result


if __name__ == '__main__':
    data = json.loads(OUTPUT.read_bytes()); body = json.loads(BODY.read_bytes())
    rows = validate(data, body)
    controls = {}
    for name, mutation, error in [
        ('reversed_skirt_winding', lambda a: a['meshes'][1]['triangles'][0].reverse(), 'winding'),
        ('collapsed_cloth_triangle', lambda a: a['meshes'][2]['positions_m'].__setitem__(a['meshes'][2]['triangles'][0][0], list(a['meshes'][2]['positions_m'][a['meshes'][2]['triangles'][0][1]])), 'degenerate'),
        ('zero_UV_cloth', lambda a: a['meshes'][2]['corner_uvs'].__setitem__(0, [[0, 0]]*3), 'UV'),
        ('foreign_skin_joint', lambda a: a['meshes'][0]['weights'].__setitem__(0, {'fake_joint': 1}), 'joints'),
        ('changed_source_anatomy_binding', lambda a: a.__setitem__('body_semantic_sha256', '0'*64), 'anatomy'),
        ('false_walking_acceptance', lambda a: a['meshes'][1]['receipt'].__setitem__('walking_or_seated_accepted', True), 'moving cloth')]:
        broken = copy.deepcopy(data); mutation(broken)
        try:
            validate(broken, body)
        except ValueError as e:
            need(error in str(e), 'wrong negative-control failure: '+str(e)); controls[name] = dict(detected=True, actual_error=str(e))
        else:
            raise ValueError('Broken geometry/source control escaped: '+name)
    receipt = dict(actual_emitted_arrays_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), components=rows,
                   negative_controls=controls, pass_checks=True,
                   photo_canonical_all_pose_or_period_pattern_acceptance=False)
    Path(__file__).with_name('ACTUAL-ARRAY-CHECKS.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt))
