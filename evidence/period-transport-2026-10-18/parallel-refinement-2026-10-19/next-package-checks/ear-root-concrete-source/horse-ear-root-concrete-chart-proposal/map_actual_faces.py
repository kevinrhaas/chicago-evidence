# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import json,struct
import numpy as np
P=Path(__file__).parent;B=Path('/workspace/shared/horse-head-groove-coat-next');raw=(B/'trial1/equine_light_harness_skinned_prototype_01.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n]);b=raw[28+n:];s=json.loads((B/'trial1/head-source-surface.json').read_text());r=json.loads((P/'CONCRETE-CHART.json').read_text())
def read(i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];return np.frombuffer(b,{5126:'<f4',5123:'<u2',5125:'<u4'}[a['componentType']],count=a['count']*{'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']],offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(a['count'],-1)
manifest=json.loads((B/'trial1/manifest.json').read_text());hr=next(x for x in manifest['vertex_ranges']if x['joint']=='head'and x['material']==0);start=hr['vertex_start'];end=start+hr['vertex_count']
pr=d['meshes'][0]['primitives'][0];pos=read(pr['attributes']['POSITION']);idx=read(pr['indices']).ravel().reshape(-1,3);result=[]
for row in r['rows']:
 for fi in row['boundary_split_source_faces']:
  expected=np.asarray(s['positions'])[s['faces'][fi]]+[0,1.88,.8];vv=[]
  for q in expected:
   dd=np.linalg.norm(pos[start:end]-q,axis=1);j=int(dd.argmin());assert dd[j]<2e-7;vv.append(start+j)
  matches=[i for i,t in enumerate(idx)if set(t)==set(vv)];assert len(matches)==1
  result.append({'side':row['side'],'source_head_face':fi,'source_head_vertices':s['faces'][fi],'mesh':d['meshes'][0]['name'],'primitive':0,'primitive_triangle':matches[0],'global_triangle':matches[0],'primitive_vertices':idx[matches[0]].tolist(),'action_proposed':'split planar complement around interior cut; all original vertices/attributes retained; no whole original triangle deletion without complement'})
(P/'ACTUAL-FACE-COHORTS.json').write_text(json.dumps({'status':'source-only mapping','rows':result},indent=2)+'\n');print(result)
