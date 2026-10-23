"""Read-only licensed GLB skin/rest-pose diagnostics. Never export/alter a model."""
import hashlib,json,struct
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
import sys
F=Path(sys.argv[1])
B=F.read_bytes()
N=struct.unpack_from('<I',B,12)[0];G=json.loads(B[20:20+N]);BIN=B[N+28:]
if 'EXT_meshopt_compression'in G.get('extensionsUsed',[]):
 BIN=(P/(F.stem+'.decoded.bin')).read_bytes()
 G['bufferViews']=json.loads((P/(F.stem+'.decoded-views.json')).read_text())
WIDTH={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16};DT={5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}
def acc(i):
 a=G['accessors'][i];v=G['bufferViews'][a['bufferView']];d=np.dtype(DT[a['componentType']]);w=WIDTH[a['type']]
 x=np.ndarray((a['count'],w),dtype=d,buffer=BIN,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',w*d.itemsize),d.itemsize)).copy()
 if a.get('normalized'):
  x=x.astype(float)/np.iinfo(d).max
  if d.kind=='i':x=np.maximum(x,-1)
 return x
def local(node,over):
 if 'matrix'in node:return np.asarray(node['matrix']).reshape((4,4),order='F')
 x,y,z,w=over.get('rotation',node.get('rotation',[0,0,0,1]));r=np.asarray([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
 m=np.eye(4);m[:3,:3]=r@np.diag(over.get('scale',node.get('scale',[1,1,1])));m[:3,3]=over.get('translation',node.get('translation',[0,0,0]));return m
PARENT={kid:i for i,n in enumerate(G['nodes'])for kid in n.get('children',[])}
def worlds(over):
 result={}
 def get(i):
  if i not in result:result[i]=(get(PARENT[i])if i in PARENT else np.eye(4))@local(G['nodes'][i],over.get(i,{}))
  return result[i]
 for i in range(len(G['nodes'])):get(i)
 return result
