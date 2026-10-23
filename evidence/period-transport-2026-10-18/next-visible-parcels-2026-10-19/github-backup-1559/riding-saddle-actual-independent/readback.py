# SPDX-License-Identifier: CC0-1.0
from pathlib import Path
import json,struct,hashlib,collections
import numpy as np
OLD=Path('/workspace/shared/riding-rein-skin-next/candidate-v2.glb');NEW=Path('/workspace/shared/riding-saddle-refinement-1835-source-next/candidate-one/candidate.glb');OUT=Path(__file__).parent
CHANGED={'seat_jockey','jockey_l','jockey_r','quarter_l','quarter_r'}
def need(x,msg):
 if not x:raise ValueError(msg)
def load(p):
 raw=p.read_bytes();n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n]);return d,raw[28+n:],raw
def arr(d,b,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];need('sparse'not in a and'byteStride'not in v,'plainaccessor');dt={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];size={'VEC3':3,'VEC4':4,'MAT4':16,'SCALAR':1}[a['type']];return np.frombuffer(b,dtype=dt,count=a['count']*size,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(a['count'],size)
a,ab,ar=load(OLD);b,bb,br=load(NEW);need(hashlib.sha256(ar).hexdigest()=='a457874a81b624f5e9642d3296b1350eb49b17d21d38099fbe66080711c17021','oldpin');need(hashlib.sha256(br).hexdigest()=='b683f00dc726c023d03369997edafc9b9e6fe4a01d7a2d02db75af2edf2eef04','newpin');need(bb[:len(ab)]==ab,'entireoldBINprefix');need(b['accessors'][:len(a['accessors'])]==a['accessors']and b['bufferViews'][:len(a['bufferViews'])]==a['bufferViews'],'oldstoragerefsexact')
for k in ['nodes','skins','animations','materials','scenes','scene']:need(a.get(k)==b.get(k),'exact'+k)
need(len(a['meshes'])==len(b['meshes'])==29,'29meshes');rows=[];protected=[];total=0
for old,new in zip(a['meshes'],b['meshes']):
 name=old['name'];need(name==new['name'],'name/order');
 for pr in new['primitives']:total+=(len(arr(b,bb,pr['indices']))if'indices'in pr else len(arr(b,bb,pr['attributes']['POSITION'])))//3
 if name not in CHANGED:need(old==new,'protectedmeshdef');protected.append(name);continue
 need(len(new['primitives'])==1,'oneprimitive');pr=new['primitives'][0];need(set(pr['attributes'])=={'POSITION','NORMAL'},'selectedrigidattrs');need(pr['material']==old['primitives'][0]['material'],'selectedmaterialexact');P=arr(b,bb,pr['attributes']['POSITION']).astype(float);N=arr(b,bb,pr['attributes']['NORMAL']).astype(float);F=arr(b,bb,pr['indices']).reshape(-1,3);need(np.isfinite(P).all()and np.isfinite(N).all(),'finite');norm=np.linalg.norm(N,axis=1);need(float(abs(norm-1).max())<1e-6,'unitN');need(int(F.max())<len(P),'indexbounds');edges=collections.defaultdict(list);adj=collections.defaultdict(set)
 for f in F:
  need(len(set(f))==3,'distinctids')
  for u,v in zip(f,np.roll(f,-1)):edges[tuple(sorted((int(u),int(v))))].append((int(u),int(v)));adj[int(u)].add(int(v));adj[int(v)].add(int(u))
 need(all(len(e)==2 and e[0]==e[1][::-1]for e in edges.values()),'twooppositeedges');seen=set();todo=[0]
 while todo:
  i=todo.pop()
  if i not in seen:seen.add(i);todo.extend(adj[i]-seen)
 need(len(seen)==len(P),'connectedallverts');need(len(P)-len(edges)+len(F)==2,'Euler2');T=P[F];area=np.linalg.norm(np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]),axis=1)/2;need(float(area.min())>1e-12,'nondegenerateactual');volume=float(np.einsum('ij,ij->i',T[:,0],np.cross(T[:,1],T[:,2])).sum()/6);need(volume>0,'positiveoutwardvolume');rows.append({'name':name,'vertices':len(P),'triangles':len(F),'Euler':2,'minimum_area_m2':float(area.min()),'volume_m3':volume,'maximum_normal_length_error':float(abs(norm-1).max())})
need(len(rows)==5 and len(protected)==24,'5+24');r={'PASS':True,'scope':'Independent actual GLB readback only; no regeneration/fit/GPU/browser','candidate_sha256':hashlib.sha256(br).hexdigest(),'old_BIN_prefix_bytes':len(ab),'old_BIN_prefix_exact':True,'protected_meshes':protected,'nodes_skins_materials_animations_scene_exact':True,'source_mesh_primitives':sum(len(m['primitives'])for m in b['meshes']),'actual_triangles':total,'new_five':rows,'limitations':['29 source mesh primitives is not a measured GPU draw count','No selfintersection/horse fit/pressure/motion/ab70/rider/photo acceptance']};(OUT/'readback.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
