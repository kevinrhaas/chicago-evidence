# Native stdlib static server + already reviewed native browser adapter, one viewport.
# Outer transport-supervise owns this process and all browser descendants.
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import hashlib,subprocess,threading,sys,json
p=Path(__file__).resolve().parent;r=Path('/tmp/chicago-wagon-20261029')
assert len(sys.argv)==3 and sys.argv[1] in ('desktop','mobile')
viewport,out=sys.argv[1:];assert not Path(out).exists()
assert hashlib.sha256((p/'run-native-railway-lifecycle-v4-settled.cjs').read_bytes()).hexdigest()=='f17e363eb259cb6570fbd6e4c926ced921dd2a92531a279efd9e651af64590cd'
assert hashlib.sha256((p/'observe-native-railway-lifecycle-v4-settled.mjs').read_bytes()).hexdigest()=='6b02fe37be6af663945405ed3598fbbefc70915d2503352f7babb72dda2563cd'
subprocess.run([sys.executable,str(p/'check-staged-source-freeze.py')],check=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(r/'site/4d')))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
rc=1
try:
 url=f'http://127.0.0.1:{server.server_address[1]}/1904/'
 print(json.dumps({'native_server':url,'published_root':str(r/'site/4d'),'viewport':viewport}),flush=True)
 rc=subprocess.run(['node',str(p/'run-native-railway-lifecycle-v4-settled.cjs'),url,viewport,out],cwd=r/'chicago/4d').returncode
finally:
 server.shutdown();server.server_close();thread.join(timeout=10)
 if thread.is_alive():rc=1;print('Owned native static-server thread failed to close',file=sys.stderr)
 subprocess.run([sys.executable,str(p/'check-staged-source-freeze.py')],check=True)
sys.exit(rc)
