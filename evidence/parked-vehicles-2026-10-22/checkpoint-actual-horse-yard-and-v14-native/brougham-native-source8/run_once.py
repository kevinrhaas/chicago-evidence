"""Finite fixed-source-camera caller: explicit root release; eight matched normal screenshots only."""
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from threading import Thread,Lock
import json,argparse,hashlib,mimetypes,subprocess,os,signal,time,datetime
START=time.monotonic();HERE=Path(__file__).parent.resolve();served=[];lock=Lock()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--release',type=Path,required=True);args=p.parse_args()
release=json.loads(args.release.read_text());inputs=json.loads((HERE/'INPUTS.json').read_text());prepared=json.loads((HERE/'PREPARED-CALLER.json').read_text())
need(release.get('authorization_owner')=='root' and release.get('release_preview') is True and release.get('human_fullgate_lane_closed') is True and release.get('local_cpu_lane_free') is True,'Root release after fullgate/CPU lane closes required')
need(release.get('inputs_manifest_sha256')==sha(HERE/'INPUTS.json') and release.get('prepared_manifest_sha256')==sha(HERE/'PREPARED-CALLER.json'),'Root release must bind both exact manifests')
for row in inputs['files']+prepared['caller_files']:
 file=(HERE/row['path']).resolve();need(file.is_relative_to(HERE) and file.is_file() and file.stat().st_size==row['bytes'] and sha(file)==row['sha256'],'Prepared byte mismatch: '+row['path'])
for row in inputs['runtime_binaries']:
 file=Path(row['absolute_path']);need(file.stat().st_size==row['bytes'] and sha(file)==row['sha256'],'Pinned runtime binary drift')
need(not(HERE/'RUN-INTENT.json').exists() and not(HERE/'actual').exists(),'One intent/output exists; do not blindly replay')
with(HERE/'RUN-INTENT.json').open('x') as f:json.dump({'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release':release,'absolute_owner_budget_seconds':175,'browser_budget_seconds':165},f,indent=2)
files={row['path'][len('fixture/'):]:row for row in inputs['files'] if row['path'].startswith('fixture/')}
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  name=self.path.split('?',1)[0].lstrip('/');name=name+'index.html' if name.endswith('/') else name
  row=files.get(name)
  if row is None:self.send_error(404);return
  path=HERE/row['path'];data=path.read_bytes();actual=hashlib.sha256(data).hexdigest()
  if actual!=row['sha256']:self.send_error(503,'Pinned fixture byte drift');return
  with lock:served.append({'url_path':self.path,'bytes':len(data),'sha256':actual})
  self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.daemon_threads=True;thread=Thread(target=server.serve_forever,daemon=True);thread.start();process=None;error=None
try:
 remaining=175-(time.monotonic()-START)-3;need(remaining>0,'Owner preparation deadline exhausted')
 process=subprocess.Popen(['/opt/codex/runtimes/codex-primary-runtime/dependencies/node/bin/node',str(HERE/'capture.cjs'),str(server.server_address[1])],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:stdout,stderr=process.communicate(timeout=remaining)
 except subprocess.TimeoutExpired:
  os.killpg(process.pid,signal.SIGKILL);stdout,stderr=process.communicate(timeout=2);error='175second owner deadline;owned process group killed'
 (HERE/'stdout.log').write_text(stdout);(HERE/'stderr.log').write_text(stderr)
 if error is None and process.returncode!=0:error='Browser caller failed; inspect durable receipt/stderr'
finally:
 server.shutdown();server.server_close();thread.join(timeout=1)
 (HERE/'SERVER-CLOSED.json').write_text(json.dumps({'closed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner_seconds':time.monotonic()-START,'process_returncode':None if process is None else process.returncode,'error':error,'served_pinned_files':served},indent=2)+'\n')
need(error is None,error)
print('Finite once-only owner complete;browser result in actual/receipt.json;server closed.')
