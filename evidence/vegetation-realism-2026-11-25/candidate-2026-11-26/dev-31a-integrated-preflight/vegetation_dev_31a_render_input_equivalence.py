"""Inspect the exact1904 building integration without relabelling old timings."""
import hashlib
import json
import subprocess
from pathlib import Path

from vegetation_roughness_channel_fix_lap_proof import qualify as qualify_lap
from vegetation_dev_31e_render_input_equivalence import qualify as qualify_previous

W = Path('/workspace/work')
PREVIOUS = '31e34c6f395afc466cb4fa7d0eccd8358827c672'
UPSTREAM = '31a350489aa9790c5e1b0ae75ff66e0268b8f7c4'
HOUSES = {'hanford_house_2008_calumet', 'high_house_2021_prairie',
          'house_2125_prairie_coach_house', 'murdoch_house_2130_prairie'}


def qualify(proof):
    r = Path(proof['repo'])

    def raw(*args):
        return subprocess.check_output(['git', *args], cwd=r)

    def body(ref, path):
        return raw('show', ref + ':' + path)

    old = json.loads((W/'vegetation-dev-31e-final-integration-proof.json').read_text())
    prior = qualify_previous(old)
    assert prior['complete'] and qualify_lap(proof)['complete']
    assert old['actual_dev'] == PREVIOUS and proof['actual_dev'] == UPSTREAM
    assert proof['previous_review_head'] == old['final_head']
    assert proof['native_candidate_tree'] == old['native_candidate_tree']
    changed = raw('diff', '--name-only', PREVIOUS, UPSTREAM).decode().splitlines()
    frontend = {p for p in changed if p.startswith('chicago/4d/renderers/web/')}
    assert frontend == {'chicago/4d/renderers/web/js/changelog.js'}, frontend
    main = 'chicago/4d/renderers/web/js/main.js'
    assert body(old['final_tree'], main) == body(proof['final_tree'], main)
    code_changes = {p for p in old['feature_code_sha256']
                    if body(old['final_tree'], p) != body(proof['final_tree'], p)}
    assert code_changes == {'chicago/4d/tools/check.sh',
                            'chicago/4d/tools/step_isolation.json'}, code_changes

    def is_house(key):
        return any(h in key for h in HOUSES)

    registries = []
    for path, key in [('chicago/4d/assets/manifest.json', 'assets'),
                      ('chicago/4d/assets/manifest.web.json', 'masters'),
                      ('chicago/4d/assets/manifest.versions.json', 'assets')]:
        x, y = [json.loads(body(ref, path))
                for ref in (old['final_tree'], proof['final_tree'])]
        assert {k: v for k, v in x.items() if k != key} == {
            k: v for k, v in y.items() if k != key}, path
        stamp_only = []
        geometry = []
        for name in sorted(set(x[key]) | set(y[key])):
            a, b = x[key].get(name), y[key].get(name)
            if a == b:
                continue
            if is_house(name):
                geometry.append(name)
                continue
            # Upstream re-stamped shared archetype inputs without changing the
            # corresponding mesh bytes. Delivery hashes, sizes and all other
            # values must remain identical; do not call these raw JSON files
            # byte-identical when their generator-input stamp changed.
            assert path != 'chicago/4d/assets/manifest.web.json', name
            assert isinstance(a, dict) and isinstance(b, dict), name
            assert {k: v for k, v in a.items() if k != 'inputs_sha256'} == {
                k: v for k, v in b.items() if k != 'inputs_sha256'}, name
            assert a.get('inputs_sha256') != b.get('inputs_sha256'), name
            stamp_only.append(name)
        if path.endswith('manifest.web.json'):
            assert len(geometry) == 5
        registries.append({'path': path,
                           'changed1904_delivery_entries': geometry,
                           'generator_input_stamp_only_entries': stamp_only,
                           'every_other_entry_value_preserved': True})
    asset_paths = [p for p in changed
                   if p.startswith(('chicago/4d/assets/gltf/',
                                    'chicago/4d/assets/web/'))]
    assert len(asset_paths) == 10, asset_paths
    assert all(is_house(p) for p in asset_paths)

    allowed_data = {
        'chicago/4d/data/back_yards/1904.json',
        'chicago/4d/data/components/prairie_1904/draft_prairie_1904.json',
        'chicago/4d/data/components/prairie_1904/k12_coach_house.json',
        'chicago/4d/data/humans/doors_1904.json',
        'chicago/4d/data/humans/inside_1904.json',
        'chicago/4d/data/jaunts/prairie-built-so-far.json',
        'chicago/4d/data/liberties.json',
        'chicago/4d/data/reading/1904.json',
        'chicago/4d/data/sidecars/1835/sources/chicagology_2021_high_photo.json',
        'chicago/4d/data/sidecars/1835/sources/index.json',
        'chicago/4d/data/sidecars/1835/sources/sanborn_1911_chicago_v3_sheet_35.json',
        'chicago/4d/data/sidecars/1904/index.json',
        'chicago/4d/data/sidecars/1904/jaunts/prairie-built-so-far.json',
        'chicago/4d/data/sources/inland_architect_1883_12_hanford_plate.json',
        'chicago/4d/data/street_section/walk_joins_1904.json',
        *{f'chicago/4d/data/{folder}/{house}.json'
          for folder in ('structures', 'sidecars/1904') for house in HOUSES},
    }
    extras = {p for p in changed if p.startswith('chicago/4d/data/')} - allowed_data
    assert all(p.startswith('chicago/4d/data/sources/assets/hanford_2008_plate_t3791/')
               or any(p.startswith('chicago/4d/data/reference_views/'+h+'/')
                      for h in HOUSES) for p in extras), extras
    benchmark = []
    for path in ('chicago/4d/tools/measure_still_frame.mjs',
                 'chicago/4d/tools/still_frame_ceilings.json'):
        a, b = [body(ref, path) for ref in (old['final_tree'], proof['final_tree'])]
        assert a == b, path
        benchmark.append({'path': path, 'sha256': hashlib.sha256(b).hexdigest()})
    return {
        'complete': True,
        'measured_source_tree': proof['native_candidate_tree'],
        'current_integrated_tree': proof['final_tree'],
        'all_default1835_geometry_material_shader_and_benchmark_bytes_unchanged': True,
        'frame_loop_bytes_unchanged_since_previous_review': True,
        'frame_loop_bytes_unchanged_from_original6b': False,
        'actual_default_scene_street_talk_guard': prior['actual_default_scene_street_talk_guard'],
        'inspected_upstream_frontend_paths': sorted(frontend),
        'inspected1904_mesh_paths': sorted(asset_paths),
        'asset_registries': registries,
        'benchmark': benchmark,
        'new_source_timing_execution_claimed': False,
        'scope': (
            'All renderer modules except the official release fold remain byte-identical '
            'to the previous366526 review. The exact Dev31a batch changes four1904 '
            'building deliveries and their dated data, plus maintenance and research '
            'records. Other source registry differences are solely generator-input '
            'stamps: delivery bytes/hashes and all other values remain identical. '
            'The default1835 physical render inputs and timing helper remain unchanged. '
            'Original complete6b Native and actual EPYC7763/4 timings keep their '
            'original identity. The inherited1904-only optional frame call is recorded '
            'by the previous inspection; no new timing execution is claimed here. '
            'Fresh actual combined-head Native, every published browser part at '
            'both viewports, and all stock performance/memory reports remain required.'),
        'previous_input_inspection': prior,
    }
