# SPDX-License-Identifier: GPL-3.0-or-later
"""Original adult dress components on the existing portable source skeleton.

Generated geometry is CC0-1.0. This is disclosed reconstructed authoring, not
a dated pattern, named likeness, canonical export or accepted photographic asset.
The unchanged source anatomy remains present. Skirt skinning is intentionally a
pelvis-bound standing construction: walking/seated cloth deformation is UNQUALIFIED.
"""
from __future__ import annotations
import collections
import copy
import hashlib
import json
import math
from pathlib import Path

from human_source_normals import source_shared_normals
from human_workwear_fit import _clip, _slab_points, fitted_shoes
from human_period_wardrobe import finish_edges

BODY_SHA256 = '3060ee86957ff7c2d70c89e70fe95ff3bc2294a0d7f6a5716b5a2f3f8dd84c72'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def empty(name, material):
    return dict(name=name, material=material, positions_m=[], triangles=[], uvs=[],
                corner_uvs=[], weights=[])


def skin(mapping):
    items = sorted(((k, v) for k, v in mapping.items() if v > 1e-12), key=lambda p: (-p[1], p[0]))
    need(math.fsum(v for _, v in items[4:]) <= .025, 'garment cut discards more than 2.5 percent skin mass')
    items = items[:4]
    total = math.fsum(v for _, v in items)
    need(total > 0, 'empty garment weights')
    return {k: v/total for k, v in items}


def bodice(body, bones, waist, ease=.010):
    """Closed long-sleeve source-fitted bodice with linear neck/waist/cuff cuts."""
    out = empty('plain_closed_bodice', 'garment_upper__plain_dress')
    source = body['meshes'][0]
    positions = source['positions_m']
    normals = source_shared_normals(positions, source['triangles'], source['source_vertex_indices'])
    neck = bones['neck_01']['head_m'][1]
    cuff = abs(bones['hand_l']['head_m'][0])-.012
    cache = {}
    for face in source['triangles']:
        poly = [dict(p=positions[i], uv=source['uvs'][i], w=source['weights'][i], n=normals[i],
                     basis={source['source_vertex_indices'][i]: 1.}) for i in face]
        for field in (lambda v: v['p'][1]-waist, lambda v: neck-v['p'][1],
                      lambda v: cuff-v['p'][0], lambda v: cuff+v['p'][0],
                      lambda v: .025-math.fsum(v['w'].get(k, 0.) for k in ('head', 'jaw'))):
            poly = _clip(poly, field)
        ids = []
        for v in poly:
            normal_length = math.hypot(*v['n'])
            need(normal_length > 1e-12, 'undefined source garment normal')
            n = [x/normal_length for x in v['n']]
            # Ease Y continuously to zero at cut planes; never clamp interior
            # triangles into coplanar folded fans or move/hide the body.
            y_gain = min(1., max(0., min(v['p'][1]-waist, neck-v['p'][1]))/(2*ease))
            p = [v['p'][a]+ease*n[a]*(y_gain if a == 1 else 1.) for a in range(3)]
            weights = skin(v['w'])
            key = (tuple(p), tuple(sorted(weights.items())))
            if key not in cache:
                cache[key] = len(out['positions_m'])
                out['positions_m'].append(p); out['uvs'].append(list(v['uv'])); out['weights'].append(weights)
            ids.append(cache[key])
        for i in range(1, len(ids)-1):
            face = [ids[0], ids[i], ids[i+1]]
            if len(set(face)) < 3:
                continue
            a, b, c = [out['positions_m'][k] for k in face]
            u, v = [[q[j]-a[j] for j in range(3)] for q in (b, c)]
            area = math.hypot(u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
            if area <= 1e-18:
                continue
            out['triangles'].append(face)
            out['corner_uvs'].append([poly[k]['uv'] for k in (0, i, i+1)])
    out = finish_edges(out, .0015)
    out['receipt'].update(source_body_mutated=False, nominal_normal_ease_m=ease,
                          source_body_uvs_reused=True, neckline_y_m=neck, waist_y_m=waist,
                          construction='Long sleeves and closed torso; reconstructed cut, no historical personal outfit')
    return out


def skirt(body, bones, waist, upper_garment=None, segments=96, rows=18, ease=.015, hem=.055):
    """Standing skirt with gathered radial folds around a proven convex core.

    Each core ring encloses the COMPLETE source triangle slabs above and below
    it. Corresponding polygon edges share fixed normals, so each linear loft
    panel bounds its complete source slab. Fold vertices move radially outward;
    all emitted triangles remain outside their own original panel's halfspace.
    This proves standing-body clearance, not cloth mechanics or walking fit.
    """
    need(segments >= 48 and segments % 12 == 0 and rows >= 4 and .01 <= ease <= .03,
         'unsupported skirt discretization/ease')
    levels = [waist+(hem-waist)*i/(rows-1) for i in range(rows)]
    triangles = [[mesh['positions_m'][i] for i in face] for mesh in body['meshes'] for face in mesh['triangles']
                 if min(mesh['positions_m'][i][1] for i in face) <= waist and max(mesh['positions_m'][i][1] for i in face) >= hem]
    normals = [(math.sin(2*math.pi*(k+.5)/segments), math.cos(2*math.pi*(k+.5)/segments)) for k in range(segments)]
    supports = []
    for i, y in enumerate(levels):
        points = _slab_points(triangles, levels[min(rows-1, i+1)], levels[max(0, i-1)])
        need(bool(points), 'empty body skirt band')
        t = i/(rows-1)
        rx, rz = .155+.19*t**.78, .130+.15*t**.78
        supports.append([max(math.hypot(rx*nx, rz*nz), max(nx*p[0]+nz*p[2] for p in points)+ease)
                         for nx, nz in normals])
    out = empty('gathered_ankle_skirt', 'garment_lower__plain_dress')
    core = []
    for i, y in enumerate(levels):
        ring = []
        for k in range(segments):
            nx0, nz0 = normals[(k-1)%segments]; nx1, nz1 = normals[k]
            a, b = supports[i][(k-1)%segments], supports[i][k]
            det = nx0*nz1-nx1*nz0
            x, z = (a*nz1-b*nz0)/det, (nx0*b-nx1*a)/det
            need(x*math.sin(2*math.pi*k/segments)+z*math.cos(2*math.pi*k/segments) > 0,
                 'invalid polar support polygon')
            ring.append((x, y, z))
            # Twelve restrained broad gathers, amplified below the waist.
            gather = (.003+.011*(i/(rows-1))**.6)*(1-math.cos(12*2*math.pi*k/segments))*.5
            r = math.hypot(x, z); factor = 1+gather/r
            out['positions_m'].append([factor*x, y, factor*z]); out['uvs'].append([k/segments, i/(rows-1)])
            out['weights'].append({'pelvis': 1.})
        core.append(ring)
    minimum_panel_margin = math.inf
    for i in range(rows-1):
        for k, (nx, nz) in enumerate(normals):
            n = (k+1)%segments
            faces = [[i*segments+k, (i+1)*segments+n, i*segments+n],
                     [i*segments+k, (i+1)*segments+k, (i+1)*segments+n]]
            for f in faces:
                out['triangles'].append(f)
                uv = [[((v % segments)/segments if v % segments else (1. if k == segments-1 else 0.)), (v//segments)/(rows-1)] for v in f]
                out['corner_uvs'].append(uv)
                for v in f:
                    p = out['positions_m'][v]; t = (p[1]-levels[i])/(levels[i+1]-levels[i])
                    bound = (1-t)*supports[i][k]+t*supports[i+1][k]
                    minimum_panel_margin = min(minimum_panel_margin, nx*p[0]+nz*p[2]-bound)
    need(minimum_panel_margin >= -1e-10, 'fold triangle enters guaranteed body-clearance core')
    minimum_body_clearance = math.inf
    tested = 0
    for i in range(rows-1):
        for p in _slab_points(triangles, levels[i+1], levels[i]):
            t = (p[1]-levels[i])/(levels[i+1]-levels[i])
            for k, (nx, nz) in enumerate(normals):
                bound = (1-t)*supports[i][k]+t*supports[i+1][k]
                minimum_body_clearance = min(minimum_body_clearance, bound-nx*p[0]-nz*p[2])
                tested += 1
    need(minimum_body_clearance >= ease-1e-10, 'standing skirt core intersects source anatomy')
    # Close the top annulus against the ACTUAL emitted bodice, rather than
    # leaving an open gap between a broad skirt and narrower fitted torso.
    # The small1.5mm underlap is a garment-layer construction, not hidden skin.
    need(upper_garment is not None, 'skirt requires an actual upper garment for its waist closure')
    join_y = waist+.014
    sections = []
    for face in upper_garment['triangles']:
        triangle = [upper_garment['positions_m'][i] for i in face]
        if min(p[1] for p in triangle) <= join_y <= max(p[1] for p in triangle):
            points = _slab_points([triangle], join_y, join_y)
            unique = list(dict.fromkeys(tuple(p) for p in points))
            if len(unique) == 2:
                sections.append(unique)
    inner = []
    for k in range(segments):
        dx, dz = math.sin(2*math.pi*k/segments), math.cos(2*math.pi*k/segments)
        radii = []
        for a, b in sections:
            ux, uz = b[0]-a[0], b[2]-a[2]
            denominator = ux*dz-uz*dx
            if abs(denominator) < 1e-14:
                continue
            t = -(a[0]*dz-a[2]*dx)/denominator
            if -1e-10 <= t <= 1+1e-10:
                radius = (a[0]+t*ux)*dx+(a[2]+t*uz)*dz
                if radius > 0:
                    radii.append(radius)
        need(bool(radii), 'waist closure has no actual garment cross-section')
        radius = max(radii)-.0015
        need(radius > .02, 'waist closure underlap exceeds garment radius')
        inner.append(len(out['positions_m']))
        out['positions_m'].append([radius*dx, join_y, radius*dz])
        out['uvs'].append([k/segments, -.025]); out['weights'].append({'pelvis': 1.})
    for k in range(segments):
        n = (k+1)%segments
        for face, uv in (([k, n, inner[n]], [[k/segments, 0], [(k+1)/segments, 0], [(k+1)/segments, -.025]]),
                         ([k, inner[n], inner[k]], [[k/segments, 0], [(k+1)/segments, -.025], [k/segments, -.025]])):
            out['triangles'].append(face); out['corner_uvs'].append(uv)
    out['receipt'] = dict(standing_body_core_clearance_m=minimum_body_clearance,
                          body_panel_samples=tested, minimum_fold_panel_margin_m=minimum_panel_margin,
                          hem_y_m=hem, waist_y_m=waist, skirt_all_around_folds=12,
                          waist_closure=dict(actual_bodice_cross_section_y_m=join_y, radial_underlap_m=.0015,
                                             construction='Closed top annulus tucked1.5mm into actual bodice; no anatomy removed'),
                          source_body_mutated=False, walking_or_seated_accepted=False,
                          skinning='All skirt vertices belong to pelvis; standing authoring only')
    return finish_edges(out, .0015), core


def apron(dress, core, rows=18, segments=96):
    """Optional separate broad front apron, following the existing skirt surface."""
    out = empty('separate_plain_apron', 'garment_outer__plain_apron')
    columns = list(range(-segments//8, segments//8+1))
    for row in range(rows-3):
        for col in columns:
            k = col % segments; base = dress['positions_m'][row*segments+k]
            r = math.hypot(base[0], base[2]); offset = .005
            out['positions_m'].append([base[0]*(1+offset/r), base[1]+.001, base[2]*(1+offset/r)])
            out['uvs'].append([(col-columns[0])/(columns[-1]-columns[0]), row/(rows-4)])
            out['weights'].append({'pelvis': 1.})
    width = len(columns)
    for row in range(rows-4):
        for k in range(width-1):
            a = row*width+k; b = a+1; c = a+width+1; d = a+width
            for face in ([a, c, b], [a, d, c]):
                out['triangles'].append(face); out['corner_uvs'].append([out['uvs'][i] for i in face])
    return finish_edges(out, .0015)


def construct(body):
    before = digest(body)
    bones = {b['name']: b for b in body['skeleton']}
    # Original engineering choice near the actual source waist. This is not a
    # measurement of an1835 garment or a statement about a named resident.
    waist = bones['spine_02']['head_m'][1]
    bodice_mesh = bodice(body, bones, waist-.018)
    skirt_mesh, core = skirt(body, bones, waist, bodice_mesh)
    parts = [bodice_mesh, skirt_mesh, apron(skirt_mesh, core)]
    shoes = fitted_shoes(body, bones, 0, clearance_m=.004)
    shoes['name'] = 'closed_low_shoes'; shoes['material'] = 'footwear__plain_low_shoes'
    parts.append(shoes)
    need(before == digest(body), 'garment constructor mutated source anatomy, rig or UVs')
    return dict(format='chicago4d_original_female_dress_source_v1', license='CC0-1.0',
                units='m', up_axis='+Y', forward_axis='+Z', grade='reconstructed',
                body_sha256=BODY_SHA256, body_semantic_sha256=before,
                source_body_unchanged=True, skeleton=copy.deepcopy(body['skeleton']), meshes=parts,
                materials={'garment_upper__plain_dress': {'base_color_linear': [.095, .12, .15, 1], 'roughness': .9},
                           'garment_lower__plain_dress': {'base_color_linear': [.095, .12, .15, 1], 'roughness': .9},
                           'garment_outer__plain_apron': {'base_color_linear': [.46, .42, .34, 1], 'roughness': .92},
                           'footwear__plain_low_shoes': {'base_color_linear': [.045, .031, .022, 1], 'roughness': .6}},
                limitations=['Unrendered original source construction, no dated cutting pattern or historical garment image used',
                             'Colours, proportions, folds, cloth thickness and outfit combination are conjectural',
                             'No resident model assignment, skin or hair choice; underlying female body is preserved',
                             'Skirt/apron are pelvis-bound standing source; walking/seated cloth is unqualified',
                             'No canonical Blender master/export, LOD, photo, clipping-all-pose or world-placement acceptance'])


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('--body', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); raw = a.body.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BODY_SHA256, 'unreviewed female body source')
    need(not a.output.exists(), 'fresh output required; retain earlier authoring candidates')
    data = construct(json.loads(raw)); a.output.write_text(json.dumps(data, separators=(',', ':'))+'\n')
    print(json.dumps({'output': str(a.output), 'sha256': hashlib.sha256(a.output.read_bytes()).hexdigest(),
                      'meshes': [{'name': m['name'], 'vertices': len(m['positions_m']), 'triangles': len(m['triangles'])} for m in data['meshes']],
                      'source_body_unchanged': data['source_body_unchanged'], 'acceptance': 'SOURCE_ONLY_UNRENDERED'}))
