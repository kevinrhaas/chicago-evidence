from pathlib import Path
import gzip,hashlib,json,tempfile
r=Path(__file__).parent;m=json.loads((r/'MANIFEST.json').read_text())
for x in m['records']:
 with tempfile.TemporaryFile() as assembled:
  h=hashlib.sha256();n=0
  parts=x.get('payload_parts') or [{'path':x['payload'],'bytes':x['encoded_bytes'],'sha256':x['encoded_sha256']}]
  for part in parts:
   ph=hashlib.sha256();pn=0
   with (r/part['path']).open('rb') as f:
    for b in iter(lambda:f.read(1048576),b''):
     h.update(b);n+=len(b);ph.update(b);pn+=len(b);assembled.write(b)
   assert pn==part['bytes'] and ph.hexdigest()==part['sha256'],part['path']
  assert n==x['encoded_bytes'] and h.hexdigest()==x['encoded_sha256'],x['original']
  assembled.seek(0);h=hashlib.sha256();n=0
  with gzip.GzipFile(fileobj=assembled,mode='rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  assert n==x['bytes'] and h.hexdigest()==x['sha256'],x['original']
print('All',len(m['records']),'original records and ordered encoded payloads verify losslessly')
