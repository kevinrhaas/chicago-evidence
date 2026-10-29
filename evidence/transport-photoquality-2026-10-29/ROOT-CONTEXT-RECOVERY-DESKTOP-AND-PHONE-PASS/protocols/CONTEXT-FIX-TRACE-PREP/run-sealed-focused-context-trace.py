"""Outside-app owned server and guards; invoking this starts a real GPU diagnostic.

Do not execute until root grants the heavy/GPU slot. The outer transport-supervise
must own this Python process, its Node browser process, and all descendants.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import hashlib, json, subprocess, sys, threading, time

PREP = Path(__file__).resolve().parent
BASE = PREP.parent
REPO = Path('/tmp/chicago-wagon-20261029')
MIRROR = REPO / 'site/4d'
DRIVER = PREP / 'run-focused-native-context-trace.cjs'
assert len(sys.argv) == 3 and sys.argv[1] in ('desktop', 'mobile')
profile, name = sys.argv[1:]
assert name.startswith('RAIL-CONTEXT-ONLY-') and '/' not in name and '..' not in name
OUT = BASE / name
assert not OUT.exists()
pins = json.loads((PREP / 'MANIFEST.json').read_text())
for row in pins['payloads']:
    path = PREP / row['path']
    assert path.stat().st_size == row['bytes']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], row['path']
for row in pins['external_pins']:
    path = Path(row['path'])
    assert path.stat().st_size == row['bytes']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], row['path']
expected = json.loads((BASE / 'RAIL-CONTEXT-FIX-FULL-MIRROR-BEFORE-BROWSER-01.json').read_text())

def guard():
    subprocess.run([sys.executable, str(BASE / 'CONTEXT-RESTORE-FIX-PREP-20261029/check-staged-source-freeze.py')], check=True)
    rows = [dict(path=f.relative_to(MIRROR).as_posix(), bytes=f.stat().st_size,
                 sha256=hashlib.sha256(f.read_bytes()).hexdigest())
            for f in sorted(MIRROR.rglob('*')) if f.is_file()]
    assert rows == expected, 'Full published mirror changed'
    return len(rows)

assert guard() == 5630
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(MIRROR)))
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
start = time.monotonic()
rc = 1
try:
    url = f'http://127.0.0.1:{server.server_address[1]}/1904/'
    print(json.dumps(dict(native_server=url, profile=profile, scope='focused context diagnostic only')), flush=True)
    rc = subprocess.run(['node', str(DRIVER), url, profile, str(OUT)], cwd=REPO / 'chicago/4d').returncode
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=10)
    if thread.is_alive():
        rc = 1
        print('Owned static-server thread failed to close', file=sys.stderr)
    count = guard()
    (BASE / (name + '-GUARD-CLOSED.json')).write_text(json.dumps(dict(
        profile=profile, returncode=rc, seconds=time.monotonic()-start,
        source_paths=53, complete_semantic_index_exact=True,
        published_mirror_files=count, full_mirror_before_after_exact=True,
        driver_sha256=hashlib.sha256(DRIVER.read_bytes()).hexdigest(),
        no_app_edits=True, no_URL_flags=True, no_error_waiver=True,
        full_lifecycle_or_photographic_qualification=False), indent=2)+'\n')
sys.exit(rc)
