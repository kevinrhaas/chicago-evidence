import json,struct
import numpy as np
class Model:
 def __init__(self,p):
  self.raw=p.read_bytes();n=struct.unpack_from('<I',self.raw,12)[0];self.g=json.loads(self.raw[20:20+n]);self.bin=self.raw[28+n:];self.parent={c:i for i,n in enumerate(self.g['nodes'])for c in n.get('children',[])};self.w={}
 def accessor(self,i):
  a=self.g['accessors'][i];v=self.g['bufferViews'][a['bufferView']];dtype=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
  out=np.empty((a['count'],width),dtype=dtype)
  for row in range(a['count']):
   start=v.get('byteOffset',0)+a.get('byteOffset',0)+row*v.get('byteStride',width*dtype.itemsize);out[row]=np.frombuffer(self.bin,dtype=dtype,count=width,offset=start)
  if a.get('normalized'):out=out.astype(float)/np.iinfo(dtype).max
  return out
 def world(self,i):
  if i in self.w:return self.w[i]
  n=self.g['nodes'][i]
  if'matrix'in n:m=np.asarray(n['matrix']).reshape(4,4,order='F')
  else:
   x,y,z,w=n.get('rotation',[0,0,0,1]);v=np.array([x,y,z]);cross=np.array([[0,-z,y],[z,0,-x],[-y,x,0]]);rot=np.eye(3)+2*w*cross+2*cross@cross;m=np.eye(4);m[:3,:3]=rot@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0])
  self.w[i]=(self.world(self.parent[i])if i in self.parent else np.eye(4))@m;return self.w[i]
 def mesh(self,node_id):
  node=self.g['nodes'][node_id];pr=self.g['meshes'][node['mesh']]['primitives'][0];a=pr['attributes'];skin=self.g['skins'][node['skin']];ib=self.accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1);jw=np.array([self.world(i)for i in skin['joints']]);joint=self.accessor(a['JOINTS_0']).astype(int);weights=self.accessor(a['WEIGHTS_0']);matrix=(jw@ib)[joint];position=self.accessor(a['POSITION']);normal=self.accessor(a['NORMAL']);p=np.einsum('nw,nwij,nj->ni',weights,matrix,np.c_[position,np.ones(len(position))])[:,:3];n=np.einsum('nw,nwij,nj->ni',weights,matrix,np.c_[normal,np.zeros(len(normal))])[:,:3];inv=np.linalg.inv(self.world(node_id)[:3,:3]);n=(inv.T@inv@n.T).T;n/=np.linalg.norm(n,axis=1)[:,None];return p,n,joint,weights,pr
