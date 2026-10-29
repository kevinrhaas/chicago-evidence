"""Outside-checkout read-only source/index/mirror guard and owned native HTTP server.

UNRUN. Launch only after root releases the one browser slot; wrap with the normal
transport supervisor at the unchanged600-second per-profile outer bound.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import datetime, hashlib, json, os, shutil, subprocess, sys, threading, time

PREP = Path(__file__).resolve().parent
APP = Path('/tmp/chicago-transport-resume-20261029/chicago/4d')
MIRROR = APP.parents[1] / 'site/4d'
RECOVERY = Path('/workspace/.cloud-setup/logs/transport-recovery')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', str(APP), *args])

def semantic_index():
    rows = []
    # Read from the repository root, including paths outside chicago/4d/.
    for raw in subprocess.check_output(['git', '-C', str(APP.parents[1]), 'ls-files', '--stage', '-z']).split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        mode, object_id, stage = meta.decode().split(' ')
        rows.append(dict(mode=mode, object=object_id, stage=int(stage), path=name.decode()))
    return rows

def mirror_rows():
    return [dict(path=f.relative_to(MIRROR).as_posix(), bytes=f.stat().st_size,
                 sha256=sha(f.read_bytes())) for f in sorted(MIRROR.rglob('*')) if f.is_file()]

def resource_guard():
    GiB = 1024**3
    maximum = int(Path('/sys/fs/cgroup/memory.max').read_text())
    current = int(Path('/sys/fs/cgroup/memory.current').read_text())
    free = {p: shutil.disk_usage(p).free for p in ('/workspace', '/tmp')}
    active = []
    for process in Path('/proc').iterdir():
        if not process.name.isdigit():
            continue
        try:
            if process.joinpath('stat').read_text().rsplit(')', 1)[1].split()[0] == 'Z':
                continue
            tokens = process.joinpath('cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace').split()
        except (OSError, ValueError, IndexError):
            continue
        browser = bool(tokens) and Path(tokens[0]).name in ('chromium', 'chrome', 'chrome-headless-shell')
        owner = any(Path(t).name in ('rederive.mjs', 'preflight.sh', 'check.sh', 'publish.sh', 'smoke_renderer.mjs') for t in tokens[:5])
        if browser or owner:
            active.append(dict(pid=int(process.name), command=' '.join(tokens[:6])))
    receipt = dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   memory_current_bytes=current, memory_max_bytes=maximum,
                   memory_headroom_bytes=maximum-current, free_disk_bytes=free,
                   active_browser_or_heavy_owners=active, minimum_memory_headroom_bytes=4*GiB,
                   minimum_workspace_free_bytes=512*1024**2, minimum_tmp_free_bytes=GiB)
    return receipt, maximum-current >= 4*GiB and free['/workspace'] >= 512*1024**2 and free['/tmp'] >= GiB and not active

def check_guard(expected):
    assert expected['schema'] == 'human_world_motion_guard_v1'
    assert git('rev-parse', 'HEAD').decode().strip() == expected['head']
    actual_index = semantic_index()
    assert actual_index == expected['semantic_index'], 'Complete semantic index changed'
    tree_rows = []
    for raw in subprocess.check_output(['git', '-C', str(APP.parents[1]), 'ls-tree', '-r', '-z', '--full-tree', expected['tree']]).split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        mode, kind, object_id = meta.decode().split(' ')
        tree_rows.append(dict(mode=mode, object=object_id, stage=0, path=name.decode()))
    assert actual_index == tree_rows, 'Whole TREE identity must describe the complete actual index'
    assert git('rev-parse', expected['tree']+':chicago/4d').decode().strip() == expected['app_tree']
    pins = expected['source_files']
    assert len([r for r in pins if r['path'].endswith('.glb')]) == 16, 'All16 current human master/web assets required'
    assert len([r for r in pins if not r['path'].endswith('.glb')]) >= 31, 'At least31 actual source pins required'
    assert {'renderers/web/js/main.js', 'renderers/web/js/humans.js', 'renderers/web/js/scene-loader.js',
            'renderers/web/vendor/three-0.185.1/addons/utils/SkeletonUtils.js'} <= {r['path'] for r in pins}
    for row in pins:
        rel = Path(row['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        f = APP / rel
        assert f.is_file() and not f.is_symlink()
        raw = f.read_bytes()
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], row['path']
    actual = mirror_rows()
    assert actual == expected['published_files'], 'Complete published mirror changed'
    assert len(actual) >= 5630, 'Complete native mirror required'
    return dict(head=expected['head'], tree=expected['tree'], app_tree=expected['app_tree'],
                source_files=len(pins), asset_files=16, semantic_index_entries=len(expected['semantic_index']),
                published_files=len(actual), complete_semantic_index_exact=True, full_published_mirror_exact=True)

def main():
    assert len(sys.argv) == 4 and sys.argv[1] in ('desktop', 'mobile'), 'profile fresh_output guard_manifest'
    profile, name, guard_path = sys.argv[1:]
    output = Path(name).resolve()
    assert output.is_relative_to(RECOVERY) and not output.exists(), 'Fresh outside output required'
    raw = Path(guard_path).read_bytes()
    expected = json.loads(raw)
    resources, okay = resource_guard()
    resource_path = output.with_name(output.name+'-LAUNCH-RESOURCES.json')
    resource_path.write_text(json.dumps(resources, indent=2)+'\n')
    assert okay, 'Resource guard refused; do not start browser or change thresholds'
    before = check_guard(expected)
    manifest = json.loads(PREP.joinpath('PROTOCOL-MANIFEST.json').read_text())
    for row in manifest['files']:
        f = PREP/row['file']; b = f.read_bytes()
        assert len(b) == row['bytes'] and sha(b) == row['sha256'], row['file']
    for row in manifest['external_tools']:
        f = Path(row['path']); b = f.read_bytes()
        assert len(b) == row['bytes'] and sha(b) == row['sha256'], row['path']
    video_tool = PREP/'native-tools/ffmpeg-1011/ffmpeg-linux'
    assert video_tool.is_symlink() and video_tool.resolve() == Path('/usr/bin/ffmpeg')
    handler = partial(SimpleHTTPRequestHandler, directory=str(MIRROR))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start(); rc = 1; began = time.monotonic(); closure_errors = []
    try:
        address = f'http://127.0.0.1:{server.server_address[1]}/1835/'
        print(json.dumps(dict(native_server=address, profile=profile, source_guard=before)), flush=True)
        child_environment = os.environ.copy()
        child_environment['PLAYWRIGHT_BROWSERS_PATH'] = str(PREP/'native-tools')
        child_environment['PW_EXECUTABLE'] = '/usr/bin/chromium'
        rc = subprocess.run(['node', str(PREP/'observe-human-world.cjs'), address, profile,
                             str(output), str(Path(guard_path).resolve())], cwd=APP, env=child_environment).returncode
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=10)
        if thread.is_alive():
            closure_errors.append('Owned static-server thread did not close')
            rc = 1
        try:
            after = check_guard(expected)
            assert before == after
        except BaseException as error:
            closure_errors.append(str(error)); rc = 1; after = None
        output.with_name(output.name+'-GUARD-CLOSED.json').write_text(json.dumps(dict(
            created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), returncode=rc,
            seconds=time.monotonic()-began, profile=profile, guard_manifest_sha256=sha(raw),
            before=before, after=after, closure_errors=closure_errors,
            outer_supervisor_required_seconds=600, browser_script_executed=True), indent=2)+'\n')
    return rc

if __name__ == '__main__':
    sys.exit(main())
