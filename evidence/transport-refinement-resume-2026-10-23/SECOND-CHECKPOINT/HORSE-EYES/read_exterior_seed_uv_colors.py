"""Existing source-ray seed interpolation, immutable JPEG color read only. No image edit/render."""
from pathlib import Path
import hashlib,json,struct,io,math
from PIL import Image
D=Path(__file__).parent;P=Path('/workspace/chicago-waistcoat/chicago/4d/renderers/web/transport/standing-horse/horse-sevket-v16-planted-standing-v1.glb');C=D/'V4-CINF-LINEAR-RESERVE-UV/ACTUAL-ONE-UV-ONLY-CANDIDATE/horse-sevket-v16-planted-standing-ocular-uv-CANDIDATE.glb';rays=json.loads(Path('/workspace/shared/HORSE-B479-OCULAR-FIRST-EXTERIOR-20RAY-SOURCE-20261023/RESULT.json').read_text())
def read(p):
 b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+n]),b[28+n:],hashlib.sha256(b).hexdigest()
j,b,bh=read(P);cj,cb,ch=read(C);iv=j['bufferViews'][j['images'][4]['bufferView']];imagebytes=b[iv['byteOffset']:iv['byteOffset']+iv['byteLength']];im=Image.open(io.BytesIO(imagebytes)).convert('RGB');assert im.size==(256,256)
def uv(B,i):return struct.unpack_from('<ff',B,332984+i*8)
def color(U):
 x,y=U[0]*255,U[1]*255;x0,y0=math.floor(x),math.floor(y);fx,fy=x-x0,y-y0
 return [sum(im.getpixel((min(255,x0+dx),min(255,y0+dy)))[k]*wx*wy for dx,wx in [(0,1-fx),(1,fx)]for dy,wy in [(0,1-fy),(1,fy)])for k in range(3)]
rows=[]
for r in rays['hits']:
 h=r['first_hit']
 if h['material_name']!='Eye_brown':continue
 row={'side':r['side'],'view':r['view'],'sample':r['sample'],'unchanged_source_ray_first_surface_material':'Eye_brown'}
 for name,B in [('baseline',b),('candidate',cb)]:
  U=[sum(uv(B,i)[k]*w for i,w in zip(h['index_triplet'],h['barycentric']))for k in range(2)];row[name]={'uv':U,'source_JPEG_bilinear_RGB':color(U)}
 rows.append(row)
report={'status':'ACTUAL_IMMUTABLE_SOURCE_UV_COLOR_READ_ONLY','baseline_sha256':bh,'candidate_sha256':ch,'source_image4_sha256':hashlib.sha256(imagebytes).hexdigest(),'eye_seed_count':len(rows),'rows':rows,'body_first_hit_count_unchanged':sum(r['first_hit']['material_name']!='Eye_brown'for r in rays['hits']),'scope':'Reuses original rest-pose opaque source-ray hits; source UV interpolation and image RGB only, not GPU/animation/world/photographic appearance acceptance. No image pixels edited; body eyelid/photo region unchanged.'}
(D/'ACTUAL-EXPOSED-SEED-UV-COLOR-READ.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
