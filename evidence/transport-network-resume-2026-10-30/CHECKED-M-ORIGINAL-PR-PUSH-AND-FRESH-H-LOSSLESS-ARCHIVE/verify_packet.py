from pathlib import Path
import gzip,hashlib,io,json
r=Path(__file__).parent;m=json.loads((r/'MANIFEST.json').read_text())
for x in m['records']:
 if 'payloads'in x:
  blobs=[]
  for p in x['payloads']:
   b=(r/p['payload']).read_bytes();assert len(b)==p['bytes']and hashlib.sha256(b).hexdigest()==p['sha256'],p['payload'];blobs.append(b)
  b=b''.join(blobs)
 else:b=(r/x['payload']).read_bytes()
 assert len(b)==x['encoded_bytes']and hashlib.sha256(b).hexdigest()==x['encoded_sha256'],x['original']
 if x['encoding']=='identity-parts':size=len(b);digest=hashlib.sha256(b).hexdigest()
 else:
  h=hashlib.sha256();size=0
  with gzip.GzipFile(fileobj=io.BytesIO(b))as z:
   while True:
    d=z.read(1024*1024)
    if not d:break
    size+=len(d);h.update(d)
  digest=h.hexdigest()
 assert size==x['bytes']and digest==x['sha256'],x['original']
print('All',len(m['records']),'original records, parts and complete encoded/decoded archives verify losslessly')
