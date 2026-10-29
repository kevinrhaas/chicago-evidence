# Native stdlib static server + already reviewed native browser adapter, one viewport.
# Outer transport-supervise owns this process and all browser descendants.
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import hashlib,subprocess,threading,sys,json
p=Path(__file__).resolve().parent;r=Path('/tmp/chicago-wagon-20261029')
assert len(sys.argv)==3 and sys.argv[1] in ('desktop','mobile')
viewport,out=sys.argv[1:];assert not Path(out).exists()
assert hashlib.sha256((p/'run-native-railway-default-far-camera.cjs').read_bytes()).hexdigest()=='69f4eafbfb10b119e7b22fd3b85497c5b7bc235cf898e8212bec332bbd0e922b'
assert hashlib.sha256((p/'observe-native-railway-default-far-camera.mjs').read_bytes()).hexdigest()=='fbf4e30595f49c4283575274586f37a78bcd27334837b462061903b96e14ea3e'
assert hashlib.sha256((p.parent/'RAIL-LIFECYCLE-DESKTOP-03/source-plan.json').read_bytes()).hexdigest()=='7cf78d6f8fceb8927f8c626f8ec77e41d96d688f7c866d7db38fb0dee0f897ea'
subprocess.run([sys.executable,str(p.parent/'CONTEXT-RESTORE-FIX-PREP-20261029/check-staged-source-freeze.py')],check=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(r/'site/4d')))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
rc=1
try:
 url=f'http://127.0.0.1:{server.server_address[1]}/1904/'
 print(json.dumps({'native_server':url,'published_root':str(r/'site/4d'),'viewport':viewport}),flush=True)
 rc=subprocess.run(['node',str(p/'run-native-railway-default-far-camera.cjs'),url,viewport,out],cwd=r/'chicago/4d').returncode
finally:
 server.shutdown();server.server_close();thread.join(timeout=10)
 if thread.is_alive():rc=1;print('Owned native static-server thread failed to close',file=sys.stderr)
 subprocess.run([sys.executable,str(p.parent/'CONTEXT-RESTORE-FIX-PREP-20261029/check-staged-source-freeze.py')],check=True)
sys.exit(rc)
