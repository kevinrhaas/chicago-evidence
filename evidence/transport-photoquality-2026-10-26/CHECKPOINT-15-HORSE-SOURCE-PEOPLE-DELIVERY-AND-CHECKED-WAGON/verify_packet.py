#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;m=json.loads((p/'MANIFEST.json').read_text());want={r['path'] for r in m['files']};actual={x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file()};assert actual==want|{'MANIFEST.json'}
for r in m['files']:
 f=p/r['path'];assert f.is_file()and not f.is_symlink()and f.stat().st_size==r['bytes'];h=hashlib.sha256()
 with f.open('rb')as s:
  for b in iter(lambda:s.read(1048576),b''):h.update(b)
 assert h.hexdigest()==r['sha256'],r['path']
print(json.dumps({'state':'PASS','files':len(m['files']),'payload_bytes':sum(r['bytes']for r in m['files']),'manifest_sha256':hashlib.sha256((p/'MANIFEST.json').read_bytes()).hexdigest(),'Git_or_source_access':False}))
