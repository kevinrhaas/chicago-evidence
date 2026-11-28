"""Inspect a functional upstream renderer integration without old timing claims."""
import hashlib
import json
import subprocess
from pathlib import Path

from vegetation_roughness_channel_fix_lap_proof import qualify as qualify_lap

W = Path('/workspace/work')
UPSTREAM = '976557fd7511aadb2b1dc3e9815ff9a88b295f92'
PREVIOUS = '5d1d9d2bd06dce649969770c1f6053a989dadb42'


def qualify(proof):
    r = Path(proof['repo'])

    def raw(*args):
        return subprocess.check_output(['git', *args], cwd=r)

    def body(ref, path):
        return raw('show', ref + ':' + path)

    old = json.loads((W/'vegetation-dev-5d1-final-integration-proof.json').read_text())
    assert proof['actual_dev'] == UPSTREAM and old['actual_dev'] == PREVIOUS
    assert proof['previous_review_head'] == old['final_head']
    assert proof['native_candidate_tree'] == old['native_candidate_tree']
    assert qualify_lap(proof)['complete']
    assert 'manual_source_equivalence' not in proof
    assert proof['manual_source_equivalence_retired']
    assert proof['functional_upstream_changes_require_fresh_scene_CI']
    changes = raw('diff', '--name-only', PREVIOUS, UPSTREAM).decode().splitlines()
    frontend = sorted(p for p in changes if p.startswith('chicago/4d/renderers/web/'))
    changed_feature_paths = {
        p for p in old['feature_code_sha256']
        if body(old['final_tree'], p) != body(proof['final_tree'], p)
    }
    expected = {'chicago/4d/renderers/web/js/main.js',
                'chicago/4d/renderers/web/js/city-context.js',
                'chicago/4d/tools/check.sh',
                'chicago/4d/tools/step_isolation.json',
                'chicago/4d/renderers/web/js/driven-assembly-loader.js',
                'chicago/4d/renderers/web/js/humans.js',
                'chicago/4d/tools/smoke_budget.mjs'}
    assert changed_feature_paths == expected, changed_feature_paths
    assert {'chicago/4d/renderers/web/js/main.js',
            'chicago/4d/renderers/web/js/city-context.js'} <= changed_feature_paths
    for path in frontend:
        if path not in proof['feature_code_sha256']:
            assert body(proof['final_tree'], path) == body(UPSTREAM, path), path
    benchmark = []
    for path in ('chicago/4d/tools/measure_still_frame.mjs',
                 'chicago/4d/tools/still_frame_ceilings.json',
                 'chicago/4d/tools/measure_memory.mjs',
                 'chicago/4d/tools/memory_ceilings.json'):
        a, b = [body(ref, path) for ref in (old['final_tree'], proof['final_tree'])]
        assert a == b, path
        benchmark.append({'path': path, 'sha256': hashlib.sha256(b).hexdigest()})
    return {
        'complete': True,
        'original_qualified_feature_tree': proof['native_candidate_tree'],
        'current_integrated_tree': proof['final_tree'],
        'actual_dev': UPSTREAM,
        'all_original_feature_edits_independently_preserved': True,
        'no_manual_source_equivalence_to_preceding_scene_claimed': True,
        'current_default1835_input_equivalence_claimed': False,
        'old_calibrated_timings_relabelled_as_current': False,
        'new_source_timing_execution_claimed': False,
        'changed_feature_paths_from_exact_upstream_integration': sorted(changed_feature_paths),
        'inspected_upstream_frontend_paths': frontend,
        'inspected_upstream_data_paths': sorted(p for p in changes if p.startswith('chicago/4d/data/')),
        'benchmark_helpers_and_original_limits_unchanged': benchmark,
        'fresh_complete_scene_CI_required': True,
        'scope': (
            'Dev2420 changes shared human/visitor/creator rendering and1871 '
            'signs, flames and staged carrying. It is a functional source change; '
            'the previous exact-fold scene-test alias is explicitly retired. '
            'Every original tree feature edit is independently applied/reversed '
            'over this immutable upstream tree, and all untouched feature modules '
            'retain their exact bytes. Original6b full Native and eligible actual '
            'EPYC7763/4 timings remain historical pre-authorship feature evidence. '
            'No unchanged default-scene or current timing claim is made from them. '
            'Fresh current-head full Native, all published parts at both viewports, '
            'humans/moving/upload and the complete stock frame/memory grid must '
            'qualify the integrated source at the original limits.'),
    }
