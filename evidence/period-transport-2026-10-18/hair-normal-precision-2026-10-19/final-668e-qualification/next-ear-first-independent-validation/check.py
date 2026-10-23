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
 # Independently map source first48 head vertices to actual baseline using actual head rest translation.
 head=json.loads((B.parent/'head-source-surface.json').read_text());hn=[n for n in old['nodes']if n.get('name')=='head'];need(len(hn)==1,'head anchor ambiguity');origin=np.array(hn[0]['translation']);p=old['meshes'][0]['primitives'][0];q=d['meshes'][0]['primitives'][0];bp=read(old,ob,p['attributes']['POSITION']);ids=[]
 for v in head['positions'][:48]:
  hits=np.where(np.linalg.norm(bp.astype(float)-(np.array(v)+origin),axis=1)<=2e-7)[0];need(len(hits)==1,'protected source mapping ambiguous');ids.append(int(hits[0]))
 need(len(set(ids))==48,'protected identity duplicate')
 for k in p['attributes']:need(np.array_equal(read(old,ob,p['attributes'][k])[ids],read(d,b,q['attributes'][k])[ids]),'protected48 changed '+k)
 r['protected48_ids']=ids;r['protected48_all_attributes_exact']=True;r['passed']=True
except Exception as e:r['first_failure']=str(e);r['traceback']=traceback.format_exc()
finally:(O/'decoded-receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));raise SystemExit(0 if r['passed'] else 1)
