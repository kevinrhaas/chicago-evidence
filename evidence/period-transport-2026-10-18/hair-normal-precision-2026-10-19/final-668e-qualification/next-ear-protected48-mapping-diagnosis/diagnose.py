import json,struct,hashlib
from pathlib import Path
import numpy as np
P=Path('/workspace/shared/horse-head-groove-coat-next/trial1');O=Path(__file__).parent
raw=(P/'equine_light_harness_skinned_prototype_01.glb').read_bytes();l=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+l]);b=raw[28+l:]
def read(i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];dt=np.dtype({5126:'<f4',5123:'<u2',5125:'<u4',5121:'u1'}[a['componentType']]);k={'VEC3':3,'VEC4':4,'MAT4':16,'SCALAR':1}[a['type']];return np.ndarray((a['count'],k),dtype=dt,buffer=b,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',dt.itemsize*k),dt.itemsize)).copy()
def local(n):
 if 'matrix'in n:return np.array(n['matrix']).reshape(4,4,order='F')
 x,y,z,w=n.get('rotation',[0,0,0,1]);m=np.eye(4);m[:3,:3]=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]])@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);return m
parents={c:i for i,n in enumerate(d['nodes'])for c in n.get('children',[])}
def world(i):return world(parents[i])@local(d['nodes'][i])if i in parents else local(d['nodes'][i])
h=next(i for i,n in enumerate(d['nodes'])if n.get('name')=='head');skin=d['skins'][0];ji=skin['joints'].index(h);ib=read(skin['inverseBindMatrices'])[ji].reshape(4,4,order='F');bind=np.linalg.inv(ib)
head=json.loads((P/'head-source-surface.json').read_text());producer=json.loads((P/'manifest.json').read_text());ranges=[r for r in producer['vertex_ranges']if r['material']==0 and r['joint']=='head'];rr=ranges[0];ids=np.arange(rr['vertex_start'],rr['vertex_start']+rr['vertex_count']);pos=read(d['meshes'][0]['primitives'][0]['attributes']['POSITION']);rows=[]
for i,v in enumerate(head['positions'][:48]):
 row={'source_index':i,'source_coordinate':v}
 for key,m in [('local_translation',local(d['nodes'][h])),('world',world(h)),('inverse_ibm',bind)]:
  target=(m@np.r_[v,1])[:3];hits=np.where(np.linalg.norm(pos.astype(float)-target,axis=1)<=2e-7)[0];row[key]={'target':target.tolist(),'full_coat_hits':hits.tolist(),'semantic_range_hits':np.intersect1d(hits,ids).tolist()}
 rows.append(row)
chain=[];q=h
while True:
 chain.append({'index':q,'name':d['nodes'][q].get('name'),'local':local(d['nodes'][q]).tolist()})
 if q not in parents:break
 q=parents[q]
r={'status':'diagnosis only; not protected48 acceptance','hashes':{n:hashlib.sha256((P/n).read_bytes()).hexdigest()for n in ['manifest.json','head-source-surface.json','equine_light_harness_skinned_prototype_01.glb']},'ancestry_head_to_root':chain,'head_world':world(h).tolist(),'inverse_bind_matrix':ib.tolist(),'inverse_ibm_bind':bind.tolist(),'world_vs_inverse_ibm_max_error':float(np.max(abs(world(h)-bind))),'semantic_head_range':rr,'first_nonunique_local':next((x for x in rows if len(x['local_translation']['full_coat_hits'])!=1),None),'rows':rows}
(O/'diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='rows'}))
