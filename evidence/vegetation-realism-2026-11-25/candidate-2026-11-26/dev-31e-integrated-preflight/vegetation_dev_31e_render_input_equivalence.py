"""Keep original timing identity while inspecting the exact upstream audio delta."""
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from vegetation_roughness_channel_fix_lap_proof import qualify as qualify_lap
from vegetation_dev_445_render_input_equivalence import qualify as qualify_previous

W = Path('/workspace/work')
PREVIOUS = '445b43c924dbe4594a88244bb23633829aa3a6e3'
UPSTREAM = '31e34c6f395afc466cb4fa7d0eccd8358827c672'
MAIN = 'chicago/4d/renderers/web/js/main.js'
AUDIO_MAIN_PATCH_SHA256 = '986851e2b21f6738b2b56a25dfdbe5be7ee531d09a1bb816d6828813ce9eb94c'


def qualify(proof):
    r = Path(proof['repo'])

    def raw(*args):
        return subprocess.check_output(['git', *args], cwd=r)

    def body(ref, path):
        return raw('show', ref + ':' + path)

    old = json.loads((W/'vegetation-dev-445-final-integration-proof.json').read_text())
    prior = qualify_previous(old)
    assert prior['complete'] and qualify_lap(proof)['complete']
    assert old['actual_dev'] == PREVIOUS and proof['actual_dev'] == UPSTREAM
    assert proof['previous_review_head'] == old['final_head']
    assert proof['native_candidate_tree'] == old['native_candidate_tree']

    changed = raw('diff', '--name-only', PREVIOUS, UPSTREAM).decode().splitlines()
    frontend = {p for p in changed if p.startswith('chicago/4d/renderers/web/')}
    assert MAIN in frontend
    talk = 'chicago/4d/renderers/web/js/street-talk.js'
    assert talk in frontend
    assert all(p.startswith('chicago/4d/renderers/web/audio/')
               for p in frontend - {MAIN, talk})
    for path in frontend - {MAIN}:
        assert body(proof['final_tree'], path) == body(UPSTREAM, path), path

    allowed_data = {
        'chicago/4d/data/liberties.json',
        'chicago/4d/data/music/jaunts.json',
        'chicago/4d/data/music/make.json',
        'chicago/4d/data/music/score.json',
        'chicago/4d/data/narration/direction/the-great-fire.json',
        'chicago/4d/data/narration/street/1904.json',
        'chicago/4d/data/narration/voices.json',
        *{f'chicago/4d/data/sidecars/{year}/jaunts/catalog.json'
          for year in (1812, 1835, 1871, 1904)},
    }
    assert {p for p in changed if p.startswith('chicago/4d/data/')} <= allowed_data
    assert all(p == 'chicago/4d/assets/LICENSES.md'
               or p.startswith('chicago/4d/assets/audio/')
               for p in changed if p.startswith('chicago/4d/assets/'))
    code_changes = {p for p in old['feature_code_sha256']
                    if body(old['final_tree'], p) != body(proof['final_tree'], p)}
    native_paths = {'chicago/4d/tools/check.sh',
                    'chicago/4d/tools/step_isolation.json'}
    assert code_changes == {MAIN} | native_paths, code_changes
    # These two files carry the upstream street-talk validation step and its
    # isolation declaration. The independent feature-patch proof above verifies
    # that every original tree gate edit is preserved over those exact inputs.
    assert native_paths <= set(changed)
    for path in ('chicago/4d/assets/manifest.json',
                 'chicago/4d/assets/manifest.web.json',
                 'chicago/4d/tools/measure_still_frame.mjs',
                 'chicago/4d/tools/still_frame_ceilings.json'):
        assert body(old['final_tree'], path) == body(proof['final_tree'], path), path

    patch = raw('diff', '--binary', PREVIOUS, UPSTREAM, '--', MAIN)
    assert hashlib.sha256(patch).hexdigest() == AUDIO_MAIN_PATCH_SHA256
    with tempfile.TemporaryDirectory(prefix='vegetation-31e-main-', dir=W) as d:
        env = {**os.environ, 'GIT_INDEX_FILE': d + '/index'}
        subprocess.run(['git', 'read-tree', proof['final_tree']], cwd=r, env=env,
                       check=True)
        subprocess.run(['git', 'apply', '--cached', '--reverse'], input=patch,
                       cwd=r, env=env, check=True)
        recovered = subprocess.check_output(['git', 'write-tree'], cwd=r,
                                            env=env).decode().strip()
        assert body(recovered, MAIN) == body(old['final_tree'], MAIN)

    main = body(proof['final_tree'], MAIN).decode()
    start = main.index("    if (daysScene === '1904') {\n      void import('./street-talk.js')")
    end = main.index('    // The kit is generated from its dated work record;', start)
    guard = main[start:end]
    assert guard.count('api.streetTalk = createStreetTalk(') == 1
    assert guard.count('api.streetTalk = null') == 1
    assert main.count('api.streetTalk =') == 2
    call = 'api.streetTalk?.update(frameDt);'
    assert main.count(call) == 1 and main.count('api.streetTalk?.greet(') == 1
    # Execute the exact imported-controller guard and optional frame call on the
    # benchmark's1835 scene. The1904-only import cannot run, and no controller
    # or controller update is added to that scene. This is an explicit source change,
    # not a claim that the frame-loop bytes stayed identical.
    probe = "const daysScene='1835';const api={};const frameDt=1/60;\n" + guard + call
    probe += "\nif(Object.hasOwn(api,'streetTalk'))throw Error('1835 gained street talk');console.log(JSON.stringify({scene:daysScene,streetTalkPresent:false,exactOptionalFrameCallExecuted:true}));"
    guards = json.loads(subprocess.check_output(
        [str(W/'node22/bin/node'), '--input-type=module', '-e', probe],
        cwd=r/'chicago/4d', text=True))

    return {
        'complete': True,
        'measured_source_tree': proof['native_candidate_tree'],
        'current_integrated_tree': proof['final_tree'],
        'all_default1835_geometry_material_shader_and_benchmark_bytes_unchanged': True,
        'frame_loop_bytes_unchanged': False,
        'upstream_audio_main_patch_sha256': AUDIO_MAIN_PATCH_SHA256,
        'reverse_exact_audio_patch_recovers_complete_previously_qualified_main': True,
        'anonymous_cloud_benchmark_guards': prior['anonymous_benchmark_guards'],
        'actual_default_scene_street_talk_guard': guards,
        'inspected_upstream_frontend_paths': sorted(frontend),
        'inspected_upstream_data_paths': sorted(set(changed) & allowed_data),
        'inspected_upstream_native_paths': sorted(native_paths),
        'new_source_timing_execution_claimed': False,
        'scope': (
            'The original complete6b Native and actual EPYC7763/4 timing readings '
            'keep their original source identity. Dev31e adds music, narration '
            'and1904 street talk. The exact main patch reverses to the complete '
            'previously inspected module; geometry, materials, shaders, asset '
            'registries and benchmark helpers remain unchanged. The frame-loop '
            'source does change: a1904-only optional street-talk call is proven '
            'not to invoke a controller in the default1835 benchmark. Audio and jaunt data '
            'are preserved as upstream data, not relabelled as timed inputs. '
            'Fresh current-head Native, all published browser parts at both '
            'viewports, and all stock performance/memory reports remain required.'),
        'previous_default_input_inspection': prior,
    }
