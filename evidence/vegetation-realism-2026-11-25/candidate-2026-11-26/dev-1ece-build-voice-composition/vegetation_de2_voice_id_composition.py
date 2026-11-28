"""Prove one exact, build-only voice correction plus official release folds."""
import datetime
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from vegetation_exact_note_folds import verify_folds
from vegetation_note_fold_composition import qualify_composition as original_composition

W = Path('/workspace/work')
BASE = '976557fd7511aadb2b1dc3e9815ff9a88b295f92'
FIX = '1ece2a1fd8c238b54e3b0cbbdf97fc64570dda51'
HEAD = '33fbecd13db916be592c7474d1d44cd8c7e76a5e'
VOICE = 'chicago/4d/data/narration/voices.json'


def verify_trees(repo, before, after):
    def raw(*args, **kw):
        return subprocess.check_output(['git', *args], cwd=repo, **kw)
    receipt = json.loads((W/'vegetation-dev-de2-upstream-voice-id-native.json').read_text())
    assert receipt['complete'] and receipt['exit_code'] == 0
    assert receipt['base'] == BASE and receipt['upstream_voice_fix'] == FIX
    assert receipt['head'] == HEAD
    assert hashlib.sha256(Path(receipt['log']).read_bytes()).hexdigest() == receipt['log_sha256']
    assert 'NARRATION PASS' in Path(receipt['log']).read_text()
    reader_file = W/'vegetation-dev-de2-upstream-voice-reader-checks.json'
    readers = json.loads(reader_file.read_text())
    assert readers['complete'] and readers['all_generated_street_and_jaunt_outputs_current']
    assert readers['voice_native_receipt_sha256'] == hashlib.sha256((W/'vegetation-dev-de2-upstream-voice-id-native.json').read_bytes()).hexdigest()
    assert {x['name'] for x in readers['checks']} == {'street-talk', 'jaunt-cards', 'compiled-jaunts'}
    for check in readers['checks']:
        assert check['exit_code'] == 0
        assert hashlib.sha256(Path(check['log']).read_bytes()).hexdigest() == check['log_sha256']
    a, b = (raw('show', ref+':'+VOICE) for ref in (BASE, FIX))
    assert a.count(b'"street:young_lady": "EXAVITQu4vr4xnSz7DtE"') == 1
    assert a.replace(b'"street:young_lady": "EXAVITQu4vr4xnSz7DtE"',
                     b'"street:young_lady": "EXAVITQu4vr4xnSDxMaL"') == b
    assert raw('diff', '--name-only', BASE, FIX).decode().splitlines() == [VOICE]
    assert hashlib.sha256(a).hexdigest() == receipt['before_sha256']
    assert hashlib.sha256(b).hexdigest() == receipt['after_sha256']
    x, y = (raw('show', ref+':'+VOICE) for ref in (before, after))
    assert x in (a, b) and y == b
    assert hashlib.sha256(raw('show', after+':chicago/4d/tools/test_narration.mjs')).hexdigest() == receipt['unchanged_test_sha256']
    adjusted = before
    if x != y:
        entry = raw('ls-tree', after, '--', VOICE).decode().split()
        assert entry[:2] == ['100644', 'blob'] and entry[3] == VOICE
        with tempfile.TemporaryDirectory(prefix='vegetation-voice-delta-', dir=W) as temp:
            env = {**os.environ, 'GIT_INDEX_FILE': str(Path(temp)/'index')}
            subprocess.run(['git', 'read-tree', before], cwd=repo, env=env, check=True)
            subprocess.run(['git', 'update-index', '--cacheinfo',
                            '100644,'+entry[2]+','+VOICE], cwd=repo, env=env, check=True)
            adjusted = raw('write-tree', env=env).decode().strip()
    folds = verify_folds(repo, adjusted, after)
    return {'complete': True, 'before': before, 'after': after,
            'one_exact_build_voice_id_correction': x != y,
            'voice_correction_commit': FIX, 'path': VOICE,
            'targeted_unchanged_narration_regression': receipt,
            'targeted_unchanged_config_readers': readers,
            'every_other_repository_path_identical_except_exact_official_folds': folds,
            'published_renderer_scene_asset_and_audio_bytes_identical': True}


def qualify_composition(phase, proof):
    assert proof['actual_dev'] == BASE and proof['final_head'] == HEAD
    repo = Path(proof['repo'])
    def raw(*args, **kw):
        return subprocess.check_output(['git', *args], cwd=repo, **kw)
    live = raw('ls-remote', 'origin', 'refs/heads/dev').decode().split()[0]
    if live == BASE:
        return original_composition(phase, proof)
    exists = subprocess.run(['git', 'cat-file', '-e', live+'^{commit}'], cwd=repo,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if exists.returncode:
        subprocess.run(['git', 'fetch', '--quiet', '--no-write-fetch-head',
                        '--refmap=', 'origin', live], cwd=repo, check=True)
    subprocess.run(['git', 'merge-base', '--is-ancestor', FIX, live], cwd=repo, check=True)
    verify_trees(repo, BASE, live)
    patch = raw('diff', '--binary', BASE, HEAD)
    own = set(proof['source_sha256'])
    assert VOICE not in own
    assert set(raw('diff', '--name-only', BASE, HEAD).decode().splitlines()) == own
    with tempfile.TemporaryDirectory(prefix='vegetation-voice-composition-', dir=W) as temp:
        env = {**os.environ, 'GIT_INDEX_FILE': str(Path(temp)/'index')}
        subprocess.run(['git', 'read-tree', live], cwd=repo, env=env, check=True)
        subprocess.run(['git', 'apply', '--cached', '--check'], input=patch, cwd=repo, env=env, check=True)
        subprocess.run(['git', 'apply', '--cached'], input=patch, cwd=repo, env=env, check=True)
        tree = raw('write-tree', env=env).decode().strip()
        for path, h in proof['source_sha256'].items():
            assert hashlib.sha256(raw('show', tree+':'+path)).hexdigest() == h
        assert set(raw('diff', '--name-only', live, tree).decode().splitlines()) == own
        subprocess.run(['git', 'apply', '--cached', '--reverse'], input=patch, cwd=repo, env=env, check=True)
        assert raw('write-tree', env=env).strip() == raw('rev-parse', live+'^{tree}').strip()
    assert raw('merge-tree', '--write-tree', HEAD, live).decode().splitlines()[0] == tree
    bridge = verify_trees(repo, proof['final_tree'], tree)
    out = {'complete': True, 'phase': phase, 'base': BASE, 'head': HEAD,
           'live_dev': live, 'composition_tree': tree,
           'exact_build_voice_id_bridge': bridge,
           'every_feature_byte_unchanged': True, 'entire_live_dev_preserved': True,
           'reverse_complete_feature_patch_recovers_entire_live_dev': True,
           'git_actual_merge_tree_matches_independent_composition': True,
           'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (W/'vegetation-dev-de2-live-build-voice-composition.json').write_text(json.dumps(out, indent=2)+'\n')
    return out
