import json,struct,hashlib,traceback
from pathlib import Path
import numpy as np
O=Path(__file__).parent
C=Path('/workspace/shared/horse-ear-root-exporter-source-reviewed-next/export-trial1/equine_ear_root_candidate.glb');B=Path('/workspace/shared/horse-head-groove-coat-next/trial1/equine_light_harness_skinned_prototype_01.glb')
r={'status':'UNACCEPTED','scope':'decoded rest data only; no posed/gear/render acceptance','passed':False}
def need(x,s):
 if not x: raise ValueError(s)
def load(p):
 raw=p.read_bytes(); n=struct.unpack_from('<I',raw,12)[0]; d=json.loads(raw[20:20+n]); b=raw[28+n:];return d,b,raw
def read(d,b,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];dt=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1',5122:'<i2',5120:'i1'}[a['componentType']]);k={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];off=v.get('byteOffset',0)+a.get('byteOffset',0);return np.ndarray((a['count'],k),dtype=dt,buffer=b,offset=off,strides=(v.get('byteStride',dt.itemsize*k),dt.itemsize)).copy()
try:
 d,b,raw=load(C);old,ob,orr=load(B);r['candidate_sha256']=hashlib.sha256(raw).hexdigest();r['baseline_sha256']=hashlib.sha256(orr).hexdigest();need(r['candidate_sha256']=='26027c225b0c2f3c6ed72543cb2e80238196a86815b7bb910744cbc65cb23ed3','candidate hash');need(r['baseline_sha256']=='090be8fdc2516ee5b5c8f886026f441850cc208f17b6ede71fed9007ab80f12f','baseline hash');need(b[:len(ob)]==ob,'binary prefix changed');r['original_binary_prefix_exact']=True
 active=[]
 def walk(i):
  need(i not in active,'repeated active node');active.append(i)
  for c in d['nodes'][i].get('children',[]):walk(c)
 for i in d['scenes'][d.get('scene',0)]['nodes']:walk(i)
 rows=[]
 for ni in active:
  n=d['nodes'][ni]
  if 'mesh' not in n:continue
  for pi,p in enumerate(d['meshes'][n['mesh']]['primitives']):
   a={k:read(d,b,v)for k,v in p['attributes'].items()};pos=a['POSITION'];ix=read(d,b,p['indices']).ravel();need(len(ix)%3==0 and int(ix.max())<len(pos),'indices out of range');need(all(np.isfinite(v).all()for v in a.values()),'nonfinite attribute');nn=np.linalg.norm(a['NORMAL'].astype(float),axis=1);err=float(np.max(abs(nn-1)));need(err<1e-5,'nonunit normals');ws=float(np.max(abs(a['WEIGHTS_0'].astype(float).sum(axis=1)-1)));need(ws<1e-6,'weight sums');need(np.min(a['WEIGHTS_0'])>=0,'negative weights');palette=len(d['skins'][n['skin']]['joints']);need(int(a['JOINTS_0'].max())<palette,'joint palette overflow');pa=d['accessors'][p['attributes']['POSITION']];need(np.allclose(pos.min(axis=0),pa['min'],rtol=0,atol=1e-7)and np.allclose(pos.max(axis=0),pa['max'],rtol=0,atol=1e-7),'position accessor bounds');rows.append({'mesh':n['mesh'],'primitive':pi,'triangles':len(ix)//3,'vertices':len(pos),'normal_max_error':err,'weight_sum_max_error':ws,'joint_palette':palette})
 r['active_primitives']=rows;r['triangles']=sum(x['triangles']for x in rows);r['meshes']=len(set(x['mesh']for x in rows));r['draws']=len(rows)
 for key in ['nodes','skins','animations','materials','scenes','scene']:
  need(d.get(key)==old.get(key),'protected document changed '+key)
 r['protected_document_exact']=True
 changed=[]
 for mi,m in enumerate(old['meshes']):
  for pi,p in enumerate(m['primitives']):
   q=d['meshes'][mi]['primitives'][pi]
   for k in ['POSITION','JOINTS_0','WEIGHTS_0']:
    x=read(old,ob,p['attributes'][k]);y=read(d,b,q['attributes'][k]);need(np.array_equal(x,y[:len(x)]),'old attribute prefix changed '+str((mi,pi,k)))
 r['all_old_position_joint_weight_prefixes_exact']=True
 # Independent pinned semantic ownership and complete bind/world frame.
 producer_path=B.parent/'manifest.json';head_path=B.parent/'head-source-surface.json'
 need(hashlib.sha256(producer_path.read_bytes()).hexdigest()=='883fb2607a5ccb150c84b41985f62864b26d64db62052446ca45bfda9d99c5e9','producer hash')
 need(hashlib.sha256(head_path.read_bytes()).hexdigest()=='ac4d96ab6ae8d0ef5956686a3a9c213ebce1dd9e76f5e91c4e376b319429b5b3','head source hash')
 kr=json.loads(Path('/workspace/shared/horse-ear-first-independent-validation/khronos.json').read_text());need(kr['sha256']==r['candidate_sha256'] and kr['validator']['issues']['numErrors']==0 and kr['validator']['issues']['numWarnings']==0,'hash-bound Khronos receipt');r['khronos_reused']=kr
 def local(n):
  if 'matrix' in n:return np.array(n['matrix']).reshape(4,4,order='F')
  x,y,z,w=n.get('rotation',[0,0,0,1]);m=np.eye(4);m[:3,:3]=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]])@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);return m
 parents={}
 for i,n in enumerate(old['nodes']):
  for c in n.get('children',[]):need(c not in parents,'multiple parents');parents[c]=i
 def world(i,seen=()):
  need(i not in seen,'ancestry cycle');return world(parents[i],seen+(i,))@local(old['nodes'][i]) if i in parents else local(old['nodes'][i])
 hi=[i for i,n in enumerate(old['nodes'])if n.get('name')=='head'];need(len(hi)==1,'head node ambiguity');hi=hi[0];wm=world(hi)
 skins=[sk for sk in old['skins'] if hi in sk['joints']];need(len(skins)==1,'head skin ambiguity');sk=skins[0];ib=read(old,ob,sk['inverseBindMatrices'])[sk['joints'].index(hi)].reshape(4,4,order='F');bm=np.linalg.inv(ib);err=float(np.max(abs(wm-bm)));need(err<=2e-7,'head world/IBM disagreement');r['head_frame']={'world':wm.tolist(),'inverse_ibm':bm.tolist(),'max_error':err}
 head=json.loads(head_path.read_text());producer=json.loads(producer_path.read_text());ranges=[x for x in producer['vertex_ranges']if x['material']==0 and x['joint']=='head'];need(len(ranges)==1,'semantic head range ambiguity');rr=ranges[0];need(rr['vertex_start']==1025 and rr['vertex_count']==1221,'pinned semantic range changed');semantic=np.arange(1025,2246)
 p=old['meshes'][0]['primitives'][0];q=d['meshes'][0]['primitives'][0];bp=read(old,ob,p['attributes']['POSITION']);ids=[];mappings=[]
 for i,v in enumerate(head['positions'][:48]):
  target=(wm@np.r_[v,1])[:3];hits=np.where(np.linalg.norm(bp.astype(float)-target,axis=1)<=2e-7)[0];owned=np.intersect1d(hits,semantic);mappings.append({'source_index':i,'source_coordinate':v,'world_target':target.tolist(),'full_coat_hits':hits.tolist(),'semantic_hits':owned.tolist()});need(len(owned)==1,'protected semantic mapping ambiguous');ids.append(int(owned[0]))
 r['protected48_mapping']=mappings;need(len(set(ids))==48,'protected identity duplicate')
 for k in p['attributes']:need(np.array_equal(read(old,ob,p['attributes'][k])[ids],read(d,b,q['attributes'][k])[ids]),'protected48 changed '+k)
 normal_diffs=[]
 for mi,m in enumerate(old['meshes']):
  for pi,pn in enumerate(m['primitives']):
   bn=read(old,ob,pn['attributes']['NORMAL']);cn=read(d,b,d['meshes'][mi]['primitives'][pi]['attributes']['NORMAL'])[:len(bn)];changed=np.where(np.any(bn!=cn,axis=1))[0];normal_diffs.append({'mesh':mi,'primitive':pi,'old_vertex_count':len(bn),'changed_old_ids':changed.tolist(),'max_component_delta':float(np.max(abs(bn.astype(float)-cn.astype(float))))})
 r['all_old_normal_differences']=normal_diffs
 r['protected48_ids']=ids;r['protected48_all_attributes_exact']=True;r['passed']=True
except Exception as e:r['first_failure']=str(e);r['traceback']=traceback.format_exc()
finally:(O/'decoded-receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));raise SystemExit(0 if r['passed'] else 1)
