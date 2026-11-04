from pathlib import Path
import json,struct,collections,hashlib,datetime,math
p=Path(__file__).resolve().parent;old=p/'baseline59ec';new=p/'checkpoint-source/chicago/chicago/4d'
def glb(path):
 b=path.read_bytes();magic,version,n=struct.unpack_from('<III',b);assert magic==0x46546c67 and version==2 and n==len(b);off=12;doc=None;binary=None
 while off<len(b):
  n,t=struct.unpack_from('<II',b,off);off+=8;c=b[off:off+n];off+=n
  if t==0x4e4f534a:doc=json.loads(c)
  elif t==0x004e4942:binary=c
 return doc,binary
def data(doc,bin,i):
 a=doc['accessors'][i];assert not a.get('sparse');v=doc['bufferViews'][a['bufferView']];assert v.get('buffer',0)==0;n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];t={5120:'b',5121:'B',5122:'h',5123:'H',5125:'I',5126:'f'}[a['componentType']];fmt='<'+t*n;size=struct.calcsize(fmt);stride=v.get('byteStride',size);start=v.get('byteOffset',0)+a.get('byteOffset',0);return [struct.unpack_from(fmt,bin,start+k*stride)for k in range(a['count'])]
a,ab=glb(old/'assets/gltf/sauganash_hotel__frame_1831.glb');b,bb=glb(new/'assets/gltf/sauganash_hotel__frame_1831.glb');assert len(a['meshes'])==len(b['meshes'])==1;ap=a['meshes'][0]['primitives'];bp=b['meshes'][0]['primitives'];assert len(ap)==len(bp)==7;out=[];position_deltas=collections.Counter();other=[]
for i,(x,y)in enumerate(zip(ap,bp)):
 assert x.get('material')==y.get('material')and set(x['attributes'])==set(y['attributes']);r={'primitive':i,'material':a['materials'][x['material']]['name'],'attributes':{}}
 for attr in x['attributes']:
  av=data(a,ab,x['attributes'][attr]);bv=data(b,bb,y['attributes'][attr]);assert len(av)==len(bv);changed=[j for j,(u,v)in enumerate(zip(av,bv))if u!=v];detail={'count':len(av),'changed_rows':len(changed),'exact_values':not changed}
  if attr=='POSITION':
   ds=collections.Counter(tuple(round(v-u,7)for u,v in zip(av[j],bv[j]))for j in changed);detail['deltas']=[{'delta':k,'count':v}for k,v in ds.items()];position_deltas.update(ds)
  elif changed:
   detail['max_absolute_component_delta']=max(abs(u-v) for j in changed for u,v in zip(av[j],bv[j]))
   detail['changed_row_indices']=changed[:30]
   if attr=='_CONFIDENCE':detail['value_changes']=list({(av[j],bv[j])for j in changed})
   else:other.append({'primitive':i,'attribute':attr,'changed':len(changed)})
  r['attributes'][attr]=detail
 if'indices'in x:assert data(a,ab,x['indices'])==data(b,bb,y['indices']);r['indices_exact']=True
 out.append(r)
assert a.get('materials')==b.get('materials')and a.get('nodes')==b.get('nodes')and a.get('scenes')==b.get('scenes')
# Recipe scope and unchanged foreign registry values, independent of raw JSON row order.
m0=json.loads((old/'assets/manifest.json').read_text())['assets'];m1=json.loads((new/'assets/manifest.json').read_text())['assets'];w0=json.loads((old/'assets/manifest.web.json').read_text())['masters'];w1=json.loads((new/'assets/manifest.web.json').read_text())['masters'];recipe_changes=[k for k in set(m0)|set(m1)if m0.get(k)!=m1.get(k)];web_changes=[k for k in set(w0)|set(w1)if w0.get(k)!=w1.get(k)];assert recipe_changes==web_changes==['sauganash_hotel__frame_1831.glb'];assert len(m0)==len(m1)==1035
# Only the approved attribute was inserted in the source record.
r0=json.loads((old/'data/structures/sauganash_hotel.json').read_text());r1=json.loads((new/'data/structures/sauganash_hotel.json').read_text());delta=r1['phases'][1]['form'].pop('chimney_placement');assert delta['value']=='gable_ends'and delta['confidence']=='reconstructed';assert r0==r1
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':'59ec08a37e269eba6f4fc22a7697453e6f453fe5','candidate':'7819ad07cae4dc7ceed1de3db61fd26721ea7e24','positions_deltas':[{'delta':k,'count':v}for k,v in position_deltas.items()],'other_attribute_changes_besides_confidence':other,'primitive_audit':out,'all_materials_nodes_scenes_exact':True,'textures_and_images':{'before':[len(a.get('textures',[])),len(a.get('images',[]))],'after':[len(b.get('textures',[])),len(b.get('images',[]))]},'only_approved_record_attribute_added':delta,'manifest_rows':[len(m0),len(m1)],'recipe_changes':recipe_changes,'web_master_changes':web_changes,'all1034_foreign_recipe_and_master_hash_rows_exact':True,'no_producer_code_paths_in_commit':not any('/generators/'in x['filename']for x in json.loads((p/'APP-CHECKPOINT-COMMIT.json').read_text())['files']),'native_execution_rawSDK_pending':True,'read_only':True};(p/'INDEPENDENT-GEOMETRY-AND-REGISTRY-AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in['primitive_audit','only_approved_record_attribute_added']},indent=2))
