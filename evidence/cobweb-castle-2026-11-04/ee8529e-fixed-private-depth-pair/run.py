"""External-only, fixed-input Cobweb depth-fix diagnostic; no canonical verdict."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, tempfile, time

P = Path(__file__).resolve().parent
F = P / 'fixture'
W = Path('/tmp/wolf-poster-source-20261103/chicago/4d')
OLD = Path('/tmp/native-pr1690-review-20261104')
FIX = Path('/tmp/native-pr1690-depth-fix-ee8529e-20261104')
SRC = Path('/tmp/cobweb-face-correspondence-review-20261104')
CAMERA = SRC / 'camera/agency_1831_private.json'
PHOTO = SRC / 'source/original-full-panorama.jpg'
GLBS = {'before': OLD / 'after-gltf.glb', 'after': FIX / 'source/assets/gltf/cobweb_castle__log_1820.glb'}
EXPECTED = {'camera': '07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977',
            'source': '624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f',
            'before': '4f42207be5fcb2391fda58672ce8442b02aba9510f3096db8c2934b695fe7bea',
            'after': '1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82'}
HISTORY = OLD / 'private-controlled-pair'
REAPER = Path('/workspace/shared/run-with-reaping.py')

def dump(name, value):
    (P / name).write_text(json.dumps(value, indent=2) + '\n')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def metadata(p):
    s = p.stat()
    return {'sha256': digest(p), 'bytes': s.st_size, 'mtime_ns': s.st_mtime_ns, 'inode': s.st_ino}

def stock_paths():
    paths = [W / ('tools/' + n) for n in ['photo_match.mjs', 'photo_match_group.mjs', 'photo_match_flora.mjs', 'photo_match_enclosures.mjs']]
    paths += [W / 'renderers/web/js/keith-stone.js']
    paths += [p for p in (W / 'renderers/web/vendor/three-0.185.1').rglob('*') if p.is_file()]
    return sorted(paths)

def tool_guard():
    return {str(p): {'sha256': digest(p), 'bytes': p.stat().st_size} for p in stock_paths()}

def helper_guard():
    return {str(p): digest(p) for p in [Path(__file__).resolve(), P / 'run.sh', P / 'analysis_crops.py', REAPER]}

def input_guard():
    files = {'camera_original': CAMERA, 'source_original': PHOTO, **GLBS,
             'before_camera': F / 'camera-before/agency_1831_private.json',
             'after_camera': F / 'camera-after/agency_1831_private.json'}
    return {name: {'path': str(p), **metadata(p)} for name, p in files.items()}

def floor():
    free = {name: shutil.disk_usage(name).free for name in ['/workspace', '/tmp']}
    assert free['/workspace'] >= 536870912 and free['/tmp'] >= 1800000000, free
    return free

def link(p, target):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.is_symlink():
        assert p.resolve() == target.resolve()
    else:
        assert not p.exists(), str(p)
        p.symlink_to(target, target_is_directory=target.is_dir())

def guard(plan):
    assert tool_guard() == plan['stock_tool_vendor_sources'], 'Stock tool/vendor drift'
    assert helper_guard() == plan['helpers'], 'Helper/reaper drift'
    assert input_guard() == plan['inputs'], 'Actual GLB/camera/source metadata drift'
    assert {str(p): digest(p) for p in HISTORY.glob('FIRST-SOCKET-FAILURE-*')} == plan['preserved_socket_failure'], 'Historical failure changed'
    floor()

args = argparse.ArgumentParser()
args.add_argument('--prepare', action='store_true')
q = args.parse_args()
if q.prepare:
    assert not (P / 'PLAN.json').exists(), 'Refuse to replace a frozen preparation'
    assert digest(CAMERA) == EXPECTED['camera'] and digest(PHOTO) == EXPECTED['source']
    for label, glb in GLBS.items():
        assert digest(glb) == EXPECTED[label]
    binding = json.loads((FIX / 'BINDING.json').read_bytes())
    actual = next(r for r in binding['files'] if r['path'] == 'assets/gltf/cobweb_castle__log_1820.glb')
    assert actual['sha256'] == EXPECTED['after'] and actual['bytes'] == GLBS['after'].stat().st_size
    audit = json.loads((FIX / 'INDEPENDENT-DEPTH-GEOMETRY.json').read_bytes())
    assert audit['before_sha256'] == EXPECTED['before'] and audit['after_sha256'] == EXPECTED['after']
    link(F / 'renderers', W / 'renderers')
    link(F / 'tools', W / 'tools')
    link(F / 'node_modules', Path('/workspace/shared/node/node_modules'))
    link(F / 'chicago/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg', PHOTO)
    for label, glb in GLBS.items():
        link(F / (label + '.glb'), glb)
        cam = F / ('camera-' + label) / 'agency_1831_private.json'
        cam.parent.mkdir(exist_ok=True)
        assert not cam.exists()
        cam.write_bytes(CAMERA.read_bytes())
    plan = {'status': 'PREPARED_NOT_RENDERED_UNREVIEWED', 'expected': EXPECTED,
            'inputs': input_guard(), 'stock_tool_vendor_sources': tool_guard(), 'helpers': helper_guard(),
            'preserved_socket_failure': {str(p): digest(p) for p in HISTORY.glob('FIRST-SOCKET-FAILURE-*')},
            'actual_after_binding': actual, 'actual_after_head': binding['head'],
            'crop': [1380, 330, 1500, 420], 'analysis_scale': 8,
            'scope': 'External-only private fixed-camera depth diagnostic. No canonical camera, grade, calibration, RMS improvement, match or original-ticket closure claim.',
            'budgets_seconds': {'each_render': 260, 'outer_pair': 600}, 'expected_pair_seconds': [60, 120]}
    assert len(plan['preserved_socket_failure']) == 3
    dump('PLAN.json', plan)
    dump('GPU-LEASE.template.json', {'root_explicit_release': False, 'scope': 'Cobweb1690 corrected ee fixed private pair', 'helper_sha256': digest(Path(__file__).resolve())})
    guard(plan)
    print(json.dumps({'prepared': True, 'no_render_started': True, 'stock_source_files': len(plan['stock_tool_vendor_sources']), 'expected_pair_seconds': [60, 120]}), flush=True)
    raise SystemExit(0)

plan = json.loads((P / 'PLAN.json').read_bytes())
lease = json.loads((P / 'GPU-LEASE.json').read_bytes())
assert lease['root_explicit_release'] is True and lease['helper_sha256'] == digest(Path(__file__).resolve()), 'Explicit root GPU lease required'
assert not (P / 'RESULTS.json').exists(), 'No implicit retry'
guard(plan)
E = dict(os.environ)
for k in list(E):
    if k.startswith('SMOKE_') or k in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES']:
        E.pop(k, None)
scratch = Path(tempfile.mkdtemp(prefix='cee-', dir='/tmp'))
E.update(TMPDIR=str(scratch), TMP=str(scratch), TEMP=str(scratch), PW_EXECUTABLE='/usr/bin/chromium',
         PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1', PYTHONDONTWRITEBYTECODE='1',
         OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
rows = []
started = time.monotonic()
try:
    for label in ['before', 'after']:
        guard(plan)
        cam = F / ('camera-' + label) / 'agency_1831_private.json'
        assert not cam.with_suffix('.match.json').exists(), 'Fresh UNREVIEWED record only'
        out = P / ('out-' + label)
        assert not out.exists(), 'Fresh output only'
        receipt = P / (label + '-REAPER.json')
        cmd = ['python', str(REAPER), str(receipt), '--', 'timeout', '--signal=TERM', '--kill-after=15s', '260s',
               'nice', '-n', '19', 'taskset', '-c', '0-4', 'node', str(W / 'tools/photo_match.mjs'), str(cam),
               '--glb', label + '.glb', '--out', str(out)]
        tick = time.monotonic()
        print(json.dumps({'starting': label, 'at_seconds': tick - started, 'inner_bound_seconds': 260}), flush=True)
        with (P / (label + '.log')).open('xb') as log:
            r = subprocess.Popen(cmd, cwd=F, env=E, stdout=log, stderr=subprocess.STDOUT)
            while r.poll() is None:
                try:
                    r.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    print(json.dumps({'running': label, 'seconds': time.monotonic() - tick, 'inner_bound_seconds': 260}), flush=True)
        rr = json.loads(receipt.read_bytes())
        row = {'label': label, 'exit': r.returncode, 'seconds': time.monotonic() - tick, 'command': cmd, 'reaper': rr}
        rows.append(row)
        dump('RESULTS.json', rows)
        assert r.returncode == rr['command_exit'] == 0 and rr['all_children_reaped'] and not rr['leftover_cleanup'] and rr['interrupted_signal'] is None, row
        guard(plan)
        rec = json.loads(cam.with_suffix('.match.json').read_bytes())
        assert rec['camera_sha256'] == EXPECTED['camera'] and rec['photo_sha256'] == EXPECTED['source'] and rec['glb_sha256'] == EXPECTED[label]
        assert rec['verdict'] == 'unreviewed'
        # Stock tool reports its fresh lossless bare render in the second log line.
        candidates = [Path(line.strip()) for line in (P / (label + '.log')).read_text().splitlines() if line.strip().endswith('-render.png')]
        assert len(candidates) == 1 and candidates[0].is_file()
        bare = P / (label + '-bare-render.png')
        shutil.copyfile(candidates[0], bare)
        row['artifacts'] = {'bare_render': {'path': str(bare), **metadata(bare)},
                            'side_by_side': {'path': str(out / 'agency_1831_private-side-by-side.jpg'), **metadata(out / 'agency_1831_private-side-by-side.jpg')},
                            'match_record': {'path': str(cam.with_suffix('.match.json')), 'sha256': digest(cam.with_suffix('.match.json')), 'verdict': rec['verdict']}}
        dump('RESULTS.json', rows)
        print(json.dumps({'finished': label, 'seconds': row['seconds'], 'verdict': rec['verdict']}), flush=True)
    guard(plan)
    dump('FINAL-GUARD.json', {'status': 'ACTUAL_EXTERNAL_PAIR_RENDERED_UNREVIEWED', 'all_inputs_tools_vendor_helpers_exact': True,
                             'only_glb_changed_between_fixed_camera_passes': True, 'results': rows,
                             'camera_or_source_modified': False, 'canonical_or_app_writes': False, 'grade_or_camera_or_match_claim': False})
finally:
    guard(plan)
    print(json.dumps({'final_input_guard': 'PASS', 'seconds': time.monotonic() - started, 'resources': floor()}), flush=True)
