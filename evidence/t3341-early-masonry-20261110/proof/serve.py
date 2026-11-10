from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import mimetypes
W=Path('/tmp/chicago-brick-3341/chicago/4d');R=Path('/tmp/chicago-west-wicket-20261109/chicago/4d')
class H(SimpleHTTPRequestHandler):
 def do_GET(self):
  path=self.path.split('?',1)[0]
  if path=='/favicon.ico':self.send_response(204);self.end_headers();return
  if path=='/':p=Path('/tmp/nov10-brick-3341/proof/index.html')
  elif path.startswith('/js/'):p=W/'renderers/web'/path[1:]
  elif path.startswith('/vendor/'):p=R/'renderers/web'/path[1:]
  elif path.startswith('/assets/'):p=W/path[1:]
  else:self.send_error(404);return
  if not p.is_file():self.send_error(404);return
  b=p.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(str(p))[0] or 'application/octet-stream');self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b)
ThreadingHTTPServer(('127.0.0.1',4211),H).serve_forever()
