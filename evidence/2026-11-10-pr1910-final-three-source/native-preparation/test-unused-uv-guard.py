from pathlib import Path
import importlib.util,hashlib,json,struct,subprocess
r=Path(__file__).resolve().parent;repo=Path('/tmp/chicago-west-wicket-20261109');spec=importlib.util.spec_from_file_location('audit',r/'audit-retained.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);key='first_fort_dearborn_magazine__first_fort_1803.glb';base='64a752353bc66fa6bfa58c853b90c32625f7b739';native='9dd9ba7ddd22c6ff87e52522497205f62133fa1f'
def blob(c,kind):return subprocess.check_output(['git','show',f'{c}:chicago/4d/assets/{kind}/{key}'],cwd=repo)
a,b,w=blob(base,'gltf'),blob(native,'gltf'),blob(native,'web');od,ob,oa=m.parse(a);nd,nb,na=m.parse(b)
def pack(doc,binary):
 j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*((-len(j))%4);binary+=b'\0'*((-len(binary))%4);return struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary
actual=m.compare_control(key,a,b,w);assert actual['unused_uv_only_exception']and actual['all_material_consumed_UV_attributes_raw_exact'];assert blob(base,'web')==w
controls=[]
def rejects(name,x,y,role):
 try:m.compare_control(key,x,y,w)
 except AssertionError as e:
  assert 'control active texture coordinates drift: '+role in str(e),(name,str(e));controls.append({'name':name,'rejected':True,'literal_error':str(e)});return
 raise AssertionError(name+' escaped')
uv0=nd['meshes'][0]['primitives'][0]['attributes']['TEXCOORD_0'];_,_,spans=na(uv0);mutated=bytearray(nb);offset=spans[0][0];value=struct.unpack_from('<f',mutated,offset)[0];struct.pack_into('<f',mutated,offset,value+.125);rejects('Changed consumed brick UV0 must refuse',a,pack(nd,bytes(mutated)),'TEXCOORD_0')
for name,info in [('Bind changed roof UV1 directly',{'index':0,'texCoord':1}),('Bind changed roof UV1 through KHR_texture_transform override',{'index':0,'texCoord':0,'extensions':{'KHR_texture_transform':{'texCoord':1}}})]:
 x=json.loads(json.dumps(od));y=json.loads(json.dumps(nd));material=x['meshes'][0]['primitives'][1]['material'];x['materials'][material]['normalTexture']=info;y['materials'][material]['normalTexture']=info;rejects(name,pack(x,ob),pack(y,nb),'TEXCOORD_1')
receipt={'status':'PASS_NARROW_MATERIAL_UV_BINDING_GUARD','actual_control_key':key,'actual_textured_primitive_uses_UV0_and_is_byte_exact':True,'actual_untextured_roof_only_changes_unconsumed_UV1':True,'actual_WEB_bytes_exact':True,'negative_controls':controls,'actual_primitive_details':actual['primitive_attribute_comparison'],'claim_limit':'No blanket textured-MASTER exemption. Actual active channels and all nonUV/image bytes remain strict; fixtures explicitly reject used UV0 and both direct/transform UV1 binding.'};(r/'UNUSED-UV-GUARD-CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS actual unused per-primitive UV1; 3 active-UV negative controls rejected')
