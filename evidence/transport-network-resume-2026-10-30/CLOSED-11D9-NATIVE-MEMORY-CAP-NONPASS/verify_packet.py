from pathlib import Path
import gzip,hashlib,json
r=Path(__file__).parent;m=json.loads((r/'MANIFEST.json').read_text())
for x in m['records']:
 b=(r/x['payload']).read_bytes()
 assert len(b)==x['encoded_bytes'] and hashlib.sha256(b).hexdigest()==x['encoded_sha256'],x['original']
 d=gzip.decompress(b)
 assert len(d)==x['bytes'] and hashlib.sha256(d).hexdigest()==x['sha256'],x['original']
print('All',len(m['records']),'original records and encoded payloads verify losslessly')
