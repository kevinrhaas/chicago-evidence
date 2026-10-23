"""HELD V18 native differential/readback; no model generation, browser or app writes."""
from pathlib import Path
import argparse,collections,copy,hashlib,json,math,struct,sys,time,traceback
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'source'))
from check_mid import bind_parts
from check_near import read,expanded,world_nodes,decoded_bounds,native_contacts,raw_stream
from static_master import static_master_contract
from index_streams import write_indexed
OLD={'lamp_glass','lamp_frame_ring','lamp_corner_stile','lamp_pitched_cap','lamp_finial'}
NEW={'lamp_rounded_upper_shell','lamp_hidden_inner_back','lamp_outward_oval_bright_surround',
 'lamp_outward_oval_reveal','lamp_outward_oval_glass','lamp_forward_oval_bright_surround',
 'lamp_forward_oval_reveal','lamp_forward_oval_glass','lamp_narrow_lower_glass',
 'lamp_lower_corner_stile','lamp_lower_base','lamp_finial'}
EXPECTED={'near':(33374,480,450),'mid':(11706,314,284)}
EXPECTED_OWNED={name:(8 if name=='lamp_lower_corner_stile'else 2)for name in NEW}
EXPECTED_MATERIAL={name:(3 if name.endswith('bright_surround')or name=='lamp_finial'else 5 if name.endswith('glass')else 4)for name in NEW}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise AssertionError(why)
def keyed(j,b):
 counts=collections.Counter();out={}
 for row in bind_parts(j,b):
  base=tuple(row['identity'][:3]);key=base+(counts[base],);counts[base]+=1
  require(key not in out,'Duplicate occurrence identity');out[key]=row
 return out
def protected(rows,owned):return {k:v for k,v in rows.items()if k[0]not in owned}
def assert_protected(before,after,n):
 a,c=protected(before,OLD),protected(after,NEW)
 require(len(a)==len(c)==n and list(a)==list(c),'Protected occurrence inventory/order changed')
 for key in a:
  require(a[key]['identity']==c[key]['identity']and a[key]['node_path']==c[key]['node_path']and a[key]['chunks']==c[key]['chunks'],'Protected actual P/N/role changed: '+repr(key))
 return a,c
def digest_rows(rows):
 h=hashlib.sha256()
 for key,row in rows.items():
  h.update(json.dumps(key,separators=(',',':')).encode())
  for a in ['POSITION','NORMAL']:h.update(row['chunks'][a])
 return h.hexdigest()
def assert_shared(a,c):
 for key in ['asset','nodes','meshes','materials','scenes','scene','extensionsUsed']:
  require(a.get(key)==c.get(key),'Shared document changed: '+key)
 require(len(c['nodes'])==42 and len(c['meshes'])==25 and len(c['materials'])==7,'Native inventory changed')
 require({k:v for k,v in a['extras'].items()if k not in ['parts','statistics']}=={k:v for k,v in c['extras'].items()if k not in ['parts','statistics']},'Non-owned source extras/params/capabilities changed')
 for doc in [a,c]:
  require(not any(doc.get(k)for k in ['images','textures','skins','animations']),'Unexpected external/material/motion resource')
  require(all('uri'not in q for q in doc['buffers']),'External model buffer')
def shape(j,b,detail):
 signature,triangles=expanded(j,b) # Retains original 1e-4 unit-normal /1e-20 squared-area guards, including tiny caps.
 require(triangles==EXPECTED[detail][0]and j['extras']['statistics']['triangles']==triangles,'Wrong actual V18 variant/count')
 require(len(j['extras']['parts'])==EXPECTED[detail][1],'Wrong actual part count')
 require(j['extras']['statistics']=={'triangles':triangles,'meshes':25,'nodes':42},'Exact measured statistics required')
 return signature,triangles
def material_counts(j):
 c=collections.Counter()
 for p in j['extras']['parts']:c[p['material']]+=p['triangles']
 return c
def vector(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def average(points):return tuple(sum(p[k]for p in points)/len(points)for k in range(3))
def point_rows(row):return list(struct.iter_unpack('<fff',row['chunks']['POSITION']))
def native_box(points):return{'min':[min(p[k]for p in points)for k in range(3)],'max':[max(p[k]for p in points)for k in range(3)]}
def contained(a,c):return all(a['min'][k]<=c['min'][k]and c['max'][k]<=a['max'][k]for k in range(3))
def lamp_surfaces(rows,params):
 counts=collections.Counter(k[0]for k in rows if k[0]in NEW)
 require(dict(counts)==EXPECTED_OWNED,'Exact new lamp occurrence families required')
 affine=params['body_vertical_affine'];height=lambda y:y*affine['scale_y']+affine['offset_y_m']
 checked=0
 for key,row in rows.items():
  name=key[0]
  if name not in NEW:continue
  require(row['identity'][1]=='vehicle_body'and row['identity'][2]==EXPECTED_MATERIAL[name],'Unexpected lamp carrier/material')
  ps=point_rows(row);ns=list(struct.iter_unpack('<fff',row['chunks']['NORMAL']));side=1 if average(ps)[0]>0 else-1
  center=(side*.60,height(1.53+.0875),.44)
  if name=='lamp_narrow_lower_glass':center=(side*.60,height(1.53-.0525),.44)
  elif name in ['lamp_lower_corner_stile','lamp_lower_base','lamp_finial']:center=average(ps)
  for i in range(0,len(ps),3):
   tri=ps[i:i+3];normal=cross(vector(tri[1],tri[0]),vector(tri[2],tri[0]));m=math.sqrt(dot(normal,normal))
   require(m*m>1e-20,'Tiny/degenerate lamp triangle not waived');unit=tuple(v/m for v in normal);centroid=average(tri)
   require(all(dot(unit,n)>=1-1e-4 for n in ns[i:i+3]),'Lamp geometric/shading normal disagreement')
   if name.startswith('lamp_outward_oval')and not name.endswith('reveal'):require(unit[0]*side>=1-1e-4,'Outward-side aperture faces inward')
   elif name.startswith('lamp_forward_oval')and not name.endswith('reveal'):require(unit[2]>=1-1e-4,'Forward aperture faces backward')
   elif name=='lamp_hidden_inner_back':require(unit[0]*(-side)>=1-1e-4,'Hidden inner back faces inward')
   elif name.endswith('reveal'):
    inward=list(vector(center,centroid));inward[0 if name.startswith('lamp_outward')else 2]=0.
    require(dot(unit,inward)>0,'Aperture reveal faces into solid case')
   else:require(dot(unit,vector(centroid,center))>0,'Convex lamp shell/stem/cap faces inward')
   checked+=1
 # Check actual serialized shared aperture vertices, including recessed glass joins.
 for prefix in ['lamp_outward_oval','lamp_forward_oval']:
  for ordinal in [0,1]:
   def lookup(suffix):return next(v for k,v in rows.items()if k[0]==prefix+suffix and k[3]==ordinal)
   surround=set(point_rows(lookup('_bright_surround')));reveal=set(point_rows(lookup('_reveal')));glass=set(point_rows(lookup('_glass')))
   require(len(surround)==24 and len(reveal)==24 and len(glass)==12,'Aperture distinct serialized-vertex inventory')
   require(glass<=reveal and len(reveal-glass)==12 and reveal-glass<=surround,'Recessed lens/reveal/surround vertex seam does not meet')
 return checked
def assert_static(a,c):
 a=copy.deepcopy(a);c=copy.deepcopy(c);a['source_master_sha256']=c['source_master_sha256']='0'*64
 require(a==c,'Static references/proxy/contact interfaces changed')
def mutation_rejected(label,call,controls):
 try:call()
 except AssertionError:controls[label]=True
 else:raise AssertionError('Corruption was not rejected: '+label)
def main(actual):
 start=time.monotonic();require(actual.parent==HERE and actual.name=='ACTUAL','Owned actual output only')
 intent=json.loads((actual/'INTENT.json').read_text());require(intent['authorization']=='ONE_ROOT_AUTHORIZED_V18_LAMP_NATIVE_DIAGNOSTIC'and intent['native_readback_authorized']is True,'Explicit native owner required')
 require(not(actual/'NATIVE-RESULT.json').exists(),'One result only; no retry')
 result={'pass':False,'scope':'V18 native geometry candidate ONLY; source8/world/photo remain pending','started_seconds':0,'rows':[],'negative_controls':{},'browser_or_world_accepted':False,'photographic_accepted':False,'production_activation_allowed':False}
 try:
  pins=json.loads((HERE/'INPUT-PINS.json').read_text());params=json.loads((HERE/'source/parameters.json').read_text())
  delivery=actual/'delivery';delivery.mkdir();cached={};contracts=[]
  for detail,oldname in [('near','brougham-source.glb'),('mid','brougham-mid-source.glb')]:
   candidate=actual/(detail+'-A')/'brougham.glb';repeat=actual/(detail+'-B-repeat')/'brougham.glb';baseline=actual/'baseline'/oldname
   require(candidate.read_bytes()==repeat.read_bytes(),'Declared deterministic repeat differs: '+detail)
   require(sha(baseline)==pins['baseline_files'][oldname]['sha256'],'Exact delivered V17 baseline drift')
   oj,ob=read(baseline);nj,nb=read(candidate);before=keyed(oj,ob);after=keyed(nj,nb)
   require(sum(k[0]in OLD for k in before)==18,'Original lamp families/records changed')
   assert_shared(oj,nj);old_protected,new_protected=assert_protected(before,after,EXPECTED[detail][2]);sig,tri=shape(nj,nb,detail)
   checked=lamp_surfaces(after,params)
   # The old and new complete lamp+arm envelope is compared on each side.
   for side in [-1,1]:
    def chosen(rows,names):return[p for k,row in rows.items()if k[0]in names and average(point_rows(row))[0]*side>0 for p in point_rows(row)]
    require(contained(native_box(chosen(before,OLD|{'lamp_arm'})),native_box(chosen(after,NEW|{'lamp_arm'}))),'New lamp escapes its original lamp+arm envelope')
   parents={c:i for i,n in enumerate(nj['nodes'])for c in n.get('children',[])};node_for={n['mesh']:i for i,n in enumerate(nj['nodes'])if'mesh'in n};changed=[];unchanged=0
   for mi,mesh in enumerate(nj['meshes']):
    material=mesh['primitives'][0]['material'];batch=(parents[node_for[mi]],material)
    if batch in [(1,3),(1,4),(1,5)]:changed.append(batch);continue
    require(all(raw_stream(oj,ob,mi,a)==raw_stream(nj,nb,mi,a)for a in ['POSITION','NORMAL']),'Unowned raw mesh stream changed');unchanged+=1
   require(set(changed)=={(1,3),(1,4),(1,5)}and unchanged==22,'Exactly three owned body material batches')
   signed={k:material_counts(nj)[k]-material_counts(oj)[k]for k in range(7)}
   require(signed==({0:0,1:0,2:0,3:96,4:-248,5:24,6:0}if detail=='near'else{0:0,1:0,2:0,3:96,4:-120,5:24,6:0}),'Actual material-triangle redistribution differs')
   ow,nw=world_nodes(oj),world_nodes(nj);require(ow==nw,'Runtime anchor/world translations changed')
   bounds=decoded_bounds(nj,nb,nw);require(bounds==decoded_bounds(oj,ob,ow),'Full native bounds changed')
   contacts=native_contacts(nj,nb);require(contacts==native_contacts(oj,ob),'Native wheel/shoe/pole/hitch changed')
   os=static_master_contract(oj,ob,ow,sha(baseline));ns=static_master_contract(nj,nb,nw,sha(candidate));assert_static(os,ns)
   rawout=delivery/('brougham-source.glb'if detail=='near'else'brougham-mid-source.glb');rawout.write_bytes(candidate.read_bytes())
   indexed=delivery/('brougham-near.glb'if detail=='near'else'brougham-mid.glb');index=write_indexed(rawout,indexed);ij,ib=read(indexed)
   require(expanded(ij,ib)==(sig,tri),'Actual raw/indexed expanded-triangle P/N mismatch')
   for key in ['nodes','materials','scenes','scene','extras','extensionsUsed']:require(nj.get(key)==ij.get(key),'Raw/indexed semantic mismatch '+key)
   require(decoded_bounds(ij,ib,world_nodes(ij))==bounds,'Indexed bounds mismatch')
   row={'detail':detail,'triangles':tri,'parts':len(after),'protected_parts':len(new_protected),'protected_PN_sha256':digest_rows(new_protected),'unchanged_raw_mesh_batches':unchanged,'lamp_triangles_checked':checked,'material_triangle_delta':signed,'changed_batch_bounds':[{'mesh_index':mi,'material':nj['meshes'][mi]['primitives'][0]['material'],'before':native_box(list(struct.iter_unpack('<fff',raw_stream(oj,ob,mi,'POSITION')))),'after':native_box(list(struct.iter_unpack('<fff',raw_stream(nj,nb,mi,'POSITION'))))}for mi in range(25)if (parents[node_for[mi]],nj['meshes'][mi]['primitives'][0]['material'])in [(1,3),(1,4),(1,5)]],'bounds_m':bounds,'native_contacts':contacts,**index}
   result['rows'].append(row);contracts.append({'detail':detail,**row,'static_master':ns});cached[detail]=(oj,ob,nj,nb,before,after,os,ns,rawout,indexed)
  # New head/lower body must be the same actual P/N in near/mid, not a renamed old lamp.
  nearrows,midrows=cached['near'][5],cached['mid'][5]
  for key,row in nearrows.items():
   if key[0]in NEW-{'lamp_finial'}:require(row['chunks']==midrows[key]['chunks'],'Unexpected new lamp near/mid shape divergence')
  oj,ob,nj,nb,before,after,os,ns,rawout,indexed=cached['near'];controls=result['negative_controls']
  # Mutate a real final repeated hub button; occurrence binding must find that exact row.
  protected_rows=protected(after,NEW);target=next(k for k in reversed(after)if k[0]=='solid_bright_hub_button');row=after[target];mut=bytearray(nb);off=row['offsets']['POSITION'];struct.pack_into('<f',mut,off,struct.unpack_from('<f',mut,off)[0]+.001);mutrows=keyed(nj,mut)
  require([k for k in after if after[k]['chunks']!=mutrows[k]['chunks']]==[target],'Repeated final role mutation was not isolated')
  mutation_rejected('actual_repeated_hub_button_1mm',lambda:assert_protected(before,mutrows,450),controls)
  shifted=copy.deepcopy(nj);seat=next(i for i,n in enumerate(shifted['nodes'])if n['name']=='vehicle_seat_driver');shifted['nodes'][seat]['translation'][0]+=.001
  mutation_rejected('actual_anchor_1mm',lambda:assert_shared(oj,shifted),controls)
  material=copy.deepcopy(nj);material['materials'][3]['pbrMetallicRoughness']['roughnessFactor']+=.001
  mutation_rejected('actual_shared_material_changed',lambda:assert_shared(oj,material),controls)
  proxy=copy.deepcopy(ns);proxy['collision_proxy']['components'][0]['bounds_root_m']['max'][0]+=.001
  mutation_rejected('actual_proxy_1mm_growth',lambda:assert_static(os,proxy),controls)
  mutation_rejected('V17_relabelled_as_V18',lambda:shape(oj,ob,'near'),controls)
  mutation_rejected('new_near_copy_as_mid',lambda:shape(nj,nb,'mid'),controls)
  # Reverse one actual forward aperture triangle AND its normals: consistency
  # alone would pass, but the declared outward-facing geometry must reject it.
  target=next(k for k in after if k[0]=='lamp_forward_oval_glass');row=after[target];mut=bytearray(nb);off=row['offsets']['POSITION'];a=bytes(mut[off+12:off+24]);mut[off+12:off+24]=mut[off+24:off+36];mut[off+24:off+36]=a
  off=row['offsets']['NORMAL']
  for i in range(9):struct.pack_into('<f',mut,off+4*i,-struct.unpack_from('<f',mut,off+4*i)[0])
  mutation_rejected('actual_aperture_winding_and_normals_reversed',lambda:lamp_surfaces(keyed(nj,mut),params),controls)
  # Do not waive tiny finial caps: collapse one actual serialized cap triangle.
  row=next(v for k,v in after.items()if k[0]=='lamp_finial');require(len({v[1]for v in point_rows(row)[:3]})==1,'Actual first finial triangle is a cap')
  mut=bytearray(nb);off=row['offsets']['POSITION'];mut[off+12:off+24]=mut[off:off+12]
  mutation_rejected('actual_tiny_finial_cap_zero_area_original_guard',lambda:expanded(nj,mut),controls)
  oldside=json.loads((actual/'baseline/brougham.json').read_text());side=copy.deepcopy(oldside);side['source_master_sha256']=contracts[0]['source_sha256'];side['static_master']=contracts[0]['static_master'];side['previous_V17_visual_evidence']=oldside.get('near_actual_visual_evidence');side['near_actual_visual_evidence']='V18 native source candidate only; matched V17/V18 images not yet run. Previous V17 evidence is baseline only.';side['status']='V18 rounded-lamp native candidate; source comparison, actual world and photographic acceptance pending';side['native_variant']='V18_rounded_lamp_candidate'
  for oldrow,newrow in zip(side['lods'],result['rows']):
   for key in ['triangles','source_bytes','indexed_bytes','expanded_triangle_PN_sha256','source_sha256','indexed_sha256']:oldrow[key]=newrow[key]
   oldrow['expanded_triangle_PN_sha256']=newrow['expanded_triangle_PN_sha256']
  (delivery/'brougham.json').write_text(json.dumps(side,indent=2)+'\n')
  contract={'status':'ACTUAL_NATIVE_CANDIDATE_CONTRACT_FOR_ROOT_REVIEW_NOT_CANONICAL_REGISTRATION','variant':'V18_rounded_lamp','source_manifest_sha256':intent['source_manifest_sha256'],'rows':contracts,'parameters_sha256':sha(HERE/'source/parameters.json'),'source_generator_sha256':sha(HERE/'source/generate.py'),'material_definitions_exact':7,'nodes_exact':42,'raw_batches_exact':25,'new_textures':0,'placement_or_runtime_changes':False,'preview_or_world_or_photo_accepted':False}
  (actual/'V18-CANDIDATE-CONTRACT.json').write_text(json.dumps(contract,indent=2)+'\n');result['pass']=True
 except BaseException as error:
  result['failure']={'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc()}
 finally:
  result['elapsed_seconds']=time.monotonic()-start;(actual/'NATIVE-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result));return 0 if result['pass']else 2
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--actual',type=Path,required=True);args=ap.parse_args();raise SystemExit(main(args.actual.resolve()))
