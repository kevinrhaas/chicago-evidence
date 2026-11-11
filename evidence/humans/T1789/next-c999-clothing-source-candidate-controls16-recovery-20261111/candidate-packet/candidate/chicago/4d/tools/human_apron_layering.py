# SPDX-License-Identifier: GPL-3.0-or-later
"""Apron-only source support construction; generated geometry is CC0-1.0.

Preserve the existing reconstructed cuts/ease and the source body/rig. A conforming
source surface reduces avoidable bridges across support triangles. Interpolating
skin weights is not an all-pose guarantee, and independent canonical LOD reduction
still requires native posed triangle-surface validation. No cloth simulation.
"""
from __future__ import annotations
import hashlib
import json
import math
from human_period_wardrobe import finish_edges
from human_workwear_fit import _clip


def _need(ok, why):
    if not ok:
        raise ValueError(why)


def _empty(name, material):
    return dict(name=name, material=material, positions_m=[], triangles=[], uvs=[],
                corner_uvs=[], weights=[], source_basis=[], source_triangle_indices=[])


def _support_receipt(source):
    arrays = {key: source[key] for key in ('positions_m', 'triangles', 'weights')}
    return dict(support_mesh=source['name'],
                support_arrays_sha256=hashlib.sha256(json.dumps(arrays, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
                support_vertex_count=len(source['positions_m']),
                support_triangle_count=len(source['triangles']),
                source_basis='actual support vertex indices and barycentric coefficients; returns inherit outer basis',
                source_triangle_indices='actual support triangle index per outer face; -1 for physical edge returns',
                original_body_rig_clips_materials_unchanged=True,
                walking_turning_seated_native_LOD_or_photo_accepted=False,
                limitation='Boundary skin interpolation and independent canonical LOD decimation are not a proof of posed support; validate actual skinned triangles')


def skirt_patch(dress, *, rows, segments, columns_each_side, last_row_from_hem,
                offset, name, material):
    """Use actual skirt vertices/faces and exact skin weights, without a Y jog.

    The previous panel moved every sample1mm upward before joining it on its
    original source row. Keeping support Y removes that unnecessary longitudinal
    mismatch. Existing radial ease, apron width/length and UV layout are retained.
    """
    _need(rows >= 4 and segments >= 48 and 0 < columns_each_side < segments//2,
          'invalid apron support lattice')
    last = rows-last_row_from_hem
    _need(2 <= last <= rows and .005 <= offset <= .012, 'invalid apron cut/ease')
    columns = list(range(-columns_each_side, columns_each_side+1))
    out = _empty(name, material)
    source_to_output = {}
    for row in range(last):
        for col in columns:
            source = row*segments+col % segments
            p = dress['positions_m'][source]
            radius = math.hypot(p[0], p[2])
            _need(radius > .01, 'invalid apron source radius')
            source_to_output[source] = len(out['positions_m'])
            out['positions_m'].append([p[0]*(1+offset/radius), p[1], p[2]*(1+offset/radius)])
            out['uvs'].append([(col-columns[0])/(columns[-1]-columns[0]), row/(last-1)])
            out['weights'].append(dict(dress['weights'][source]))
            out['source_basis'].append({source: 1.})
    for fi, face in enumerate(dress['triangles']):
        if all(i in source_to_output for i in face):
            out['triangles'].append([source_to_output[i] for i in face])
            out['corner_uvs'].append([list(out['uvs'][source_to_output[i]]) for i in face])
            out['source_triangle_indices'].append(fi)
    _need(len(out['triangles']) == 2*(last-1)*(len(columns)-1), 'apron source patch is incomplete')
    out = finish_edges(out, .0015)
    out['receipt']['apron_layer_support'] = {
        **_support_receipt(dress), 'construction': 'actual skirt triangle patch with its original vertex weights',
        'radial_ease_m': offset, 'support_Y_preserved': True, 'removed_previous_Y_jog_m': .001,
        'columns': len(columns), 'of_segments': segments, 'rows': last}
    return out


def conforming_bib(upper, bones, waist, *, top=.215, half_width=(.118, .098), offset=.007):
    """Clip the existing bodice triangles to the existing apron trapezoid.

    The old independent15x15grid could bridge different bodice support triangles.
    Each emitted outer face now lies over one actual source face in the bind pose.
    Original vertices keep their exact weights; new boundary vertices interpolate
    only within that face, under the existing4-influence/2.5%-discard contract.
    """
    bottom, high = waist+.012, waist+top
    _need(high > bottom and min(half_width) > 0 and .005 <= offset <= .012, 'invalid apron bib cut/ease')
    out = _empty('apron_bib', 'garment_outer__plain_apron')
    ps, ws = upper['positions_m'], upper['weights']
    seen = {}
    clipped_vertices = 0
    def width(y):
        return half_width[0]+(half_width[1]-half_width[0])*(y-bottom)/(high-bottom)
    fields = (lambda v: v['p'][1]-bottom, lambda v: high-v['p'][1],
              lambda v: width(v['p'][1])-v['p'][0], lambda v: width(v['p'][1])+v['p'][0])
    for fi, face in enumerate(upper['triangles']):
        a, b, c = [ps[i] for i in face]
        projected = (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        if abs(projected) <= 1e-14:
            continue
        if min(ps[i][2] for i in face) <= bones['spine_02']['head_m'][2]:
            continue
        poly = [dict(p=list(ps[i]), uv=[0., 0.], n=[0., 0., 1.], w=dict(ws[i]), basis={i: 1.}) for i in face]
        for field in fields:
            poly = _clip(poly, field)
        if len(poly) < 3:
            continue
        indices = []
        for v in poly:
            basis = {i: b for i, b in v['basis'].items() if b > 1e-12}
            items = sorted(((b, w) for b, w in v['w'].items() if w > 1e-12), key=lambda kv: (-kv[1], kv[0]))
            _need(math.fsum(w for _, w in items[4:]) <= .025, 'apron boundary discards more than2.5percent skin mass')
            items = items[:4]; total = math.fsum(w for _, w in items)
            _need(total > 0, 'empty apron boundary skin')
            weights = {b: w/total for b, w in items}
            # Exact source vertices retain the original mapping without renormalization.
            if len(basis) == 1 and next(iter(basis.values())) == 1.:
                weights = dict(ws[next(iter(basis))])
            key = (tuple(v['p']), tuple(sorted(basis.items())))
            if key not in seen:
                seen[key] = len(out['positions_m'])
                x, y, z = v['p']
                out['positions_m'].append([x, y, z+offset])
                out['uvs'].append([.5+x/(2*width(y)), (y-bottom)/(high-bottom)])
                out['weights'].append(weights); out['source_basis'].append(basis)
                clipped_vertices += len(basis) > 1
            indices.append(seen[key])
        for k in range(1, len(indices)-1):
            tri = [indices[0], indices[k], indices[k+1]]
            a, b, c = [out['positions_m'][i] for i in tri]
            u, v = [b[j]-a[j] for j in range(3)], [c[j]-a[j] for j in range(3)]
            if math.hypot(u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) <= 1e-14:
                continue
            out['triangles'].append(tri); out['corner_uvs'].append([list(out['uvs'][i]) for i in tri])
            out['source_triangle_indices'].append(fi)
    _need(bool(out['triangles']), 'no actual bodice surface under apron bib')
    out = finish_edges(out, .0015)
    out['receipt'].update(bib_bottom_y_m=bottom, bib_top_y_m=high, half_width_m=list(half_width),
                          offset_m=offset, skinning='actual bodice triangle support; boundary interpolation remains unqualified', basis='reconstructed')
    out['receipt']['apron_layer_support'] = {
        **_support_receipt(upper), 'construction': 'existing trapezoid clipped per actual bodice triangle; no independent grid bridges',
        'boundary_interpolated_vertices': clipped_vertices, 'front_depth_ease_m': offset}
    return out
