"""Independent read-only GLB per-occurrence audit; no producer/checker imports."""
import collections, hashlib, json, struct, subprocess
from pathlib import Path
BASE='e5ed3ff6e5a62f70ae8a1c3c0c88c29e977cf02a'
REPO='/workspace/chicago'
FROZEN=Path('/workspace/chicago-evidence/evidence/transport-refinement-resume-2026-10-23/FINAL-SOURCE-BEFORE-GATE/files/chicago/4d')
def historical(path):
 return subprocess.check_output(['git','-C',REPO,'show',BASE+':chicago/4d/'+path])
def parse(raw):
 assert struct.unpack_from('<III',raw)==(0x46546c67,2,len(raw))
 n,t=struct.unpack_from('<II',raw,12);assert t==0x4e4f534a
 m,t=struct.unpack_from('<II',raw,20+n);assert t==0x004e4942
 return json.loads(raw[20:20+n]),raw[28+n:28+n+m]
def nonlamp(j,b):
 meshes={m['name']:m for m in j['meshes']};counts=collections.Counter();out={}
 for part in j['extras']['parts']:
  identity=(part['name'],part['frame'],part['material']);key=identity+(counts[identity],);counts[identity]+=1
  if part['name'].startswith('lamp_') and part['name']!='lamp_arm':continue
  prim=meshes[f"surface_{part['frame']}_{part['material']}"]['primitives'][0];assert 'indices'not in prim
  streams=[]
  for attr in ['POSITION','NORMAL']:
   accessor=j['accessors'][prim['attributes'][attr]];view=j['bufferViews'][accessor['bufferView']]
   assert accessor['componentType']==5126 and accessor['type']=='VEC3' and not view.get('byteStride')
   offset=view.get('byteOffset',0)+accessor.get('byteOffset',0)+part['triangle_start_in_batch']*36
   data=b[offset:offset+part['triangles']*36];assert len(data)==part['triangles']*36;streams.append(data)
  out[key]=(part['triangles'],streams)
 return out
results=[]
for detail,file,expected in [('near','brougham-source.glb',450),('mid','brougham-mid-source.glb',284)]:
 path='renderers/web/transport/parked-brougham/'+file
 previous=historical(path);current=(FROZEN/path).read_bytes();j,b=parse(previous);k,c=parse(current)
 old,new=nonlamp(j,b),nonlamp(k,c);assert old==new and len(old)==expected
 for key in ['nodes','materials','scenes','scene','extensionsUsed']:assert j.get(key)==k.get(key),key
 results.append({'detail':detail,'nonlamp_occurrences_byte_exact':len(old),'materials_exact':len(k['materials']),'nodes_exact':len(k['nodes']),'old_sha256':hashlib.sha256(previous).hexdigest(),'new_sha256':hashlib.sha256(current).hexdigest(),'triangles':k['extras']['statistics']['triangles']})
archive='tools/transport/brougham/archive-v17/'
for file in ['generate.py','check_near.py','check_mid.py','near-contract.json','mid-contract.json']:
 assert (FROZEN/archive/file).read_bytes()==historical('tools/transport/brougham/'+file),file
for file in ['brougham.json','BUILD-RECEIPT.json','MID-BUILD-RECEIPT.json']:
 assert (FROZEN/archive/file).read_bytes()==historical('renderers/web/transport/parked-brougham/'+file),file
print(json.dumps({'pass':True,'scope':'Read-only serialized non-lamp P/N and baseline archive preservation; no native/material/photographic/world acceptance','baseline':BASE,'results':results,'archived_v17_files_byte_exact':8},indent=2))
