"""Small actual-hair array checks only; never imports Blender or renders."""
import collections
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = Path('/tmp/chicago-photo-worker-t1789-20261026/chicago/4d')


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def array_digest(data):
    return digest(json.dumps(data, sort_keys=True, separators=(',', ':')).encode())


def mesh_checks(result):
    points = result['positions_m']
    assert all(math.isfinite(v) for p in points for v in p)
    assert len(points) == len(result['weights']) == len(result['uvs'])
    assert all(w == {'head': 1.} for w in result['weights'])
    assert len(result['triangles']) == len(result['corner_uvs'])
    assert result['material'] == 'headwear__felt_hat'
    edges = collections.defaultdict(list)
    volume = 0.
    for face, uv in zip(result['triangles'], result['corner_uvs']):
        assert len(set(face)) == 3 and all(0 <= i < len(points) for i in face)
        a, b, c = [points[i] for i in face]
        u, v = [b[i]-a[i] for i in range(3)], [c[i]-a[i] for i in range(3)]
        normal = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        assert math.hypot(*normal) > 1e-12
        assert all(math.isfinite(x) and 0 <= x <= 1 for pair in uv for x in pair)
        area = (uv[1][0]-uv[0][0])*(uv[2][1]-uv[0][1])-(uv[1][1]-uv[0][1])*(uv[2][0]-uv[0][0])
        assert abs(area) > 1e-14
        for i, j in zip(face, face[1:]+face[:1]):
            edges[tuple(sorted((i, j)))].append((i, j))
        volume += sum(a[i]*x for i, x in enumerate([
            b[1]*c[2]-b[2]*c[1], b[2]*c[0]-b[0]*c[2], b[0]*c[1]-b[1]*c[0]]))/6
    assert all(len(owners) == 2 and owners[0] == owners[1][::-1] for owners in edges.values())
    assert len(points)-len(edges)+len(result['triangles']) == 2
    assert volume > 0
    return {'vertices': len(points), 'triangles': len(result['triangles']),
            'closed_oriented': True, 'Euler': 2, 'volume_m3': volume}


def run():
    baseline = json.loads((ROOT/'BASELINE.json').read_text())
    source = Path(baseline['path'])
    assert digest(source.read_bytes()) == baseline['sha256']
    original = module(ROOT/'original/tools/human_period_wardrobe.py', 'original_hat')
    proposed = module(ROOT/'proposed/tools/human_period_wardrobe.py', 'finished_hat')
    fitting = module(APP/'tools/human_hair_short04.py', 'unchanged_hair_fit')
    recipe_path = APP/'data/humans/recipes/worker_1835.json'
    recipe_raw = recipe_path.read_bytes()
    recipe = json.loads(recipe_raw)
    results = []
    profiles = {}
    for variant in recipe['proof_variants']:
        profile = recipe['modular_wardrobe']['assemblies'][variant['wardrobe_assembly']]
        if profile.get('hat') is None:
            assert original.work_hat({}, {}, profile, 0) is None
            assert proposed.work_hat({}, {}, profile, 0) is None
            continue
        body_path = APP/variant['body_input']
        body_raw = body_path.read_bytes()
        body = json.loads(body_raw)
        before_body = array_digest(body)
        hair, _, _ = fitting.fit(body, recipe['hair_component'], APP)
        before_hair = array_digest(hair)
        finished_profile = copy.deepcopy(profile)
        finished_profile['hat']['finish'] = 'rounded_felt_v1'
        profiles[variant['wardrobe_assembly']] = finished_profile['hat']
        for lod in range(4):
            old = original.work_hat(hair, {}, profile, lod, recipe.get('height_scale', 1))
            default = proposed.work_hat(hair, {}, profile, lod, recipe.get('height_scale', 1))
            assert default == old
            finished = proposed.work_hat(hair, {}, finished_profile, lod, recipe.get('height_scale', 1))
            assert finished['receipt']['grade'] == 'reconstructed'
            assert finished['receipt']['fit_accepted'] is False
            assert finished['receipt']['body_or_hair_mutated'] is False
            census = mesh_checks(finished)
            for axis in (0, 2):
                for fn in (min, max):
                    assert fn(p[axis] for p in old['positions_m']) == fn(p[axis] for p in finished['positions_m'])
            assert min(p[1] for p in old['positions_m']) == min(p[1] for p in finished['positions_m'])
            rise = max(p[1] for p in finished['positions_m'])-max(p[1] for p in old['positions_m'])
            assert abs(rise*recipe.get('height_scale', 1)-.0012) < 1e-10
            results.append({'variant': variant['id'], 'lod': lod,
                            'default_result_exact': True, 'default_sha256': array_digest(default),
                            'finished_sha256': array_digest(finished), 'old_triangles': len(old['triangles']),
                            **census, 'maximum_brim_extent_exact': True, 'roof_rise_m': rise,
                            'body_sha256': digest(body_raw), 'hair_sha256': before_hair})
        assert array_digest(body) == before_body and array_digest(hair) == before_hair
        assert body_path.read_bytes() == body_raw
        bad = copy.deepcopy(profile)
        bad['hat']['finish'] = 'unknown'
        try:
            proposed.work_hat(hair, {}, bad, 0)
        except ValueError as error:
            assert 'unsupported optional' in str(error)
        else:
            raise AssertionError('Unsupported finish unexpectedly accepted')
    pixels = proposed.felt_roughness_pixels()
    assert pixels == proposed.felt_roughness_pixels()
    assert len(pixels) == 128*128*4
    assert all(.91 <= pixels[i] <= .97 and pixels[i] == pixels[i+1] == pixels[i+2] and pixels[i+3] == 1 for i in range(0, len(pixels), 4))
    for size in (True, 15, 17, 1024):
        try:
            proposed.felt_roughness_pixels(size)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid texture size accepted')
    assert recipe_path.read_bytes() == recipe_raw and digest(source.read_bytes()) == baseline['sha256']
    result = {'status': 'CPU_ARRAY_PROTOTYPE_ONLY_PASS', 'actual_source_hair_fitted': True,
              'two_hatted_variants_four_LODs': results, 'default_no_hat_profile_exact': True,
              'original_body_hair_recipe_generator_bytes_unchanged': True,
              'roughness': {'size': 128, 'range': [min(pixels[::4]), max(pixels[::4])],
                            'color_space': 'Non-Color', 'deterministic': True},
              'Blender_generation': 'UNRUN', 'GLB_export': 'UNRUN', 'visual_acceptance': 'UNRUN',
              'body_rig_identity_or_production_changes': False}
    (ROOT/'CPU-CHECKS.json').write_text(json.dumps(result, indent=2)+'\n')
    (ROOT/'PROFILE-OPT-IN.json').write_text(json.dumps({'external_recipe_copy_only': True,
        'replace_only_these_hat_specs': profiles, 'default_recipe_unchanged': True}, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'variants': 2, 'LODs_checked': len(results),
                      'finished_triangle_counts': [r['triangles'] for r in results]}))


if __name__ == '__main__':
    run()
