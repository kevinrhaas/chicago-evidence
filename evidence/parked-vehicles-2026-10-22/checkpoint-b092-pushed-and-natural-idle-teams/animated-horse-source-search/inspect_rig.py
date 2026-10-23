"""Bounded native rig/key inspection. No geometry export or gait acceptance."""
import resource
resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
import io, json, hashlib, time
import numpy as np
from PIL import Image
import read_rig as D

started = time.monotonic()
G = D.G
rest = D.worlds({})
skin = G['skins'][0]
feet = {'fore_l': 50, 'fore_r': 56, 'hind_l': 75, 'hind_r': 81}
limbs = {'fore_l': list(range(46, 51)), 'fore_r': list(range(52, 57)),
         'hind_l': list(range(71, 76)), 'hind_r': list(range(77, 82))}
weights = {}
for label, chain in limbs.items():
    counts = []
    for ni in chain:
        si = skin['joints'].index(ni)
        count = 0
        for m in G['meshes']:
            for p in m['primitives']:
                a = p['attributes']
                if 'JOINTS_0' in a:
                    j, w = D.acc(a['JOINTS_0']), D.acc(a['WEIGHTS_0'])
                    count += int(np.any((j == si) & (w > .001), axis=1).sum())
        counts.append({'node': ni, 'name': G['nodes'][ni]['name'], 'weighted_vertices': count,
                       'rest_world_pivot': rest[ni][:3, 3].tolist(),
                       'rest_world_basis_columns': rest[ni][:3, :3].tolist()})
    weights[label] = counts

def qlerp(a, b, f):
    if np.dot(a, b) < 0:
        b = -b
    q = a * (1-f) + b*f
    return q / np.linalg.norm(q)

clips = []
for a in G['animations']:
    channels = []
    summaries = []
    for ch in a['channels']:
        s = a['samplers'][ch['sampler']]
        ts, vs = D.acc(s['input']).ravel(), D.acc(s['output'])
        assert s.get('interpolation', 'LINEAR') in ['LINEAR', 'STEP']
        assert len(ts) == len(vs) and np.isfinite(vs).all() and np.all(np.diff(ts) > 0)
        ni, kind = ch['target']['node'], ch['target']['path']
        channels.append((ni, kind, ts, vs, s.get('interpolation', 'LINEAR')))
        seam = None
        if kind == 'rotation':
            dot = abs(float(vs[0] @ vs[-1] / np.linalg.norm(vs[0]) / np.linalg.norm(vs[-1])))
            seam = float(np.degrees(2*np.arccos(np.clip(dot, -1, 1))))
        summaries.append({'node': ni, 'name': G['nodes'][ni].get('name'), 'property': kind,
                          'key_count': len(ts), 'first_s': float(ts[0]), 'last_s': float(ts[-1]),
                          'xyz_or_quaternion_component_span': np.ptp(vs, axis=0).tolist(),
                          'orientation_loop_seam_deg': seam})
    duration = max(float(x[2][-1]) for x in channels)
    paths = {k: [] for k in feet}
    roots = []
    for t in np.linspace(0, duration, 33):
        over = {}
        for ni, kind, ts, vs, mode in channels:
            i = max(0, min(len(ts)-1, int(np.searchsorted(ts, t, side='right')-1)))
            v = vs[i]
            if i+1 < len(ts) and mode == 'LINEAR':
                f = float((t-ts[i])/(ts[i+1]-ts[i]))
                v = qlerp(v, vs[i+1], f) if kind == 'rotation' else v*(1-f)+vs[i+1]*f
            over.setdefault(ni, {})[kind] = v.tolist()
        w = D.worlds(over)
        roots.append(w[19][:3, 3].tolist())
        for k, ni in feet.items():
            paths[k].append(w[ni][:3, 3].tolist())
    clips.append({'name': a.get('name'), 'duration_s': duration, 'channels': summaries,
                  'root19_world_translation_span': np.ptp(roots, axis=0).tolist(),
                  'foot_bone_pivot_paths_native': paths,
                  'foot_bone_pivot_spans_native': {k: np.ptp(v, axis=0).tolist() for k,v in paths.items()},
                  'foot_bone_pivot_loop_seam_native': {k: float(np.linalg.norm(np.array(v[-1])-v[0])) for k,v in paths.items()}})
textures = []
for im in G.get('images', []):
    v = G['bufferViews'][im['bufferView']]
    b = D.BIN[v.get('byteOffset', 0):v.get('byteOffset', 0)+v['byteLength']]
    image = Image.open(io.BytesIO(b))
    textures.append({'mime': im['mimeType'], 'size_px': image.size, 'mode': image.mode, 'bytes': len(b)})
result = {'scope': 'Actual native GLB bone/key/weight inventory and 33-frame foot-bone-pivot samples. No all-vertex skinning, contact, anatomical gait, intersections, photographic or browser acceptance.',
          'sha256': hashlib.sha256(D.B).hexdigest(), 'bytes': len(D.B),
          'independent_weighted_limb_chains': weights, 'clips': clips, 'textures': textures,
          'materials': G['materials'], 'elapsed_s': time.monotonic()-started}
(D.P/'NATIVE-RIG-WALK-READBACK.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'elapsed_s': result['elapsed_s'], 'textures': textures,
                  'limb_weight_counts': {k: [x['weighted_vertices'] for x in v] for k,v in weights.items()},
                  'clips': [{k:c[k] for k in ['name','duration_s','root19_world_translation_span','foot_bone_pivot_spans_native','foot_bone_pivot_loop_seam_native']} for c in clips]}, indent=2))
