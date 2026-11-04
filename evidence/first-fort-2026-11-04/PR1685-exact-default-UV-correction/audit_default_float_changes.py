from pathlib import Path
import os,subprocess,json,struct,numpy as np,hashlib
P=Path(__file__).parent;R=Path('/workspace/chicago-bridge-increment-20261102');B='42b9c601d51d8a93cde2706e1773f0bd00fadfbe';H='c8562a164f1df66a42f33457ac4ff65e1ed6111b';E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
def git(*a):return subprocess.check_output(['/usr/local/bin/git','-C',str(R),*a],env=E)
def glb(raw):
 assert raw[:4]==b'glTF';off=12;d=None;data=None
 while off<len(raw):
  n,k=struct.unpack_from('<II',raw,off);part=raw[off+8:off+8+n]
  if k==0x4e4f534a:d=json.loads(part)
  elif k==0x004e4942:data=part
  off+=8+n
 assert d and data is not None;return d,data
shape={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT2':4,'MAT3':9,'MAT4':16};dtype={5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}
def accessor(d,data,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];t=np.dtype(dtype[a['componentType']]);n=shape[a['type']];stride=v.get('byteStride',t.itemsize*n);return np.ndarray((a['count'],n),dtype=t,buffer=data,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(stride,t.itemsize))
def same_json(a,b,path=''):
 if isinstance(a,dict)and isinstance(b,dict):
  assert a.keys()==b.keys(),path
  for k in a:same_json(a[k],b[k],path+'/'+k)
 elif isinstance(a,list)and isinstance(b,list):
  assert len(a)==len(b),path
  for i,(x,y)in enumerate(zip(a,b)):same_json(x,y,path+'/'+str(i))
 elif isinstance(a,(int,float))and isinstance(b,(int,float)):
  if '/accessors/'in path and('/min/'in path or'/max/'in path):assert abs(a-b)<0.001,(path,a,b)
  else:assert a==b,(path,a,b)
 else:assert a==b,(path,a,b)
paths=git('diff','--name-only',B,H,'--','chicago/4d/assets/gltf').decode().splitlines();assert len(paths)==180;rows=[]
for p in paths:
 if Path(p).name=='first_fort_dearborn_small_house_ne__first_fort_1803.glb':continue
 old=git('show',B+':'+p);new=git('show',H+':'+p);a,x=glb(old);b,y=glb(new);same_json(a,b);maxpos=0.;maxfloat=0.;integer=0; changedattrs=[];semantics={}
 for mesh in a['meshes']:
  for prim in mesh['primitives']:
   for semantic,index in prim['attributes'].items():semantics.setdefault(index,set()).add(semantic)
 pos={prim['attributes']['POSITION']for mesh in a['meshes']for prim in mesh['primitives']}
 for i,ac in enumerate(a['accessors']):
  v=accessor(a,x,i);w=accessor(b,y,i);assert v.shape==w.shape
  if ac['componentType']==5126:
   assert np.isfinite(v).all()and np.isfinite(w).all();delta=float(np.max(np.abs(v.astype(np.float64)-w.astype(np.float64))))if v.size else 0.;maxfloat=max(maxfloat,delta)
   if i in pos:maxpos=max(maxpos,delta)
   if delta:changedattrs.append({'index':i,'semantics':sorted(semantics.get(i,[])),'max_delta':delta})
  else:assert np.array_equal(v,w),(p,i);integer+=1
 assert maxpos<0.001,(p,maxpos,maxfloat)
 rows.append({'path':p,'old_sha256':hashlib.sha256(old).hexdigest(),'native_sha256':hashlib.sha256(new).hexdigest(),'max_position_delta_m':maxpos,'max_any_float_accessor_delta':maxfloat,'changed_float_attributes':changedattrs,'integer_accessors_exact':integer,'json_semantics_exact_except_submm_accessor_bounds':True})
assert len(rows)==179
out={'default_masters':len(rows),'all_positions_under_1mm':True,'max_position_delta_m':max(x['max_position_delta_m']for x in rows),'max_float_delta':max(x['max_any_float_accessor_delta']for x in rows),'material_mesh_node_topology_integer_accessors_exact':True,'rows':rows};(P/'DEFAULT179-FLOAT-SEMANTICS-EXACT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='rows'}))
