from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;m=json.loads((p/'MANIFEST.json').read_text());expected={r['path']for r in m['files']};actual={f.relative_to(p).as_posix()for f in p.rglob('*')if f.is_file()};assert actual==expected|{'MANIFEST.json'}
for r in m['files']:
 f=p/r['path'];assert f.is_file()and not f.is_symlink()and f.stat().st_size==r['bytes'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],r['path']
print(json.dumps({'status':'PASS','files':len(m['files']),'payload_bytes':sum(r['bytes']for r in m['files']),'manifest_sha256':hashlib.sha256((p/'MANIFEST.json').read_bytes()).hexdigest(),'Git_or_remote_write':False}))
