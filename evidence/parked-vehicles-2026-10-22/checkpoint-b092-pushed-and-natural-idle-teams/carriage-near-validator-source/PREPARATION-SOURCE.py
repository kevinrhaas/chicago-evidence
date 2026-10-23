from pathlib import Path
import json,hashlib,importlib.util,shutil,struct
R=Path('/workspace/shared/brougham-v14-NEAR-VALIDATION-REGISTRATION-HELD-20261022');R.mkdir(exist_ok=True);P=R/'proposed/chicago/4d/tools/transport/brougham';P.mkdir(parents=True,exist_ok=True)
V=Path('/workspace/shared/brougham-v14-footplates-ACTUAL-20261022');OLD=Path('/workspace/shared/brougham-v13-two-joins-ACTUAL-20261022/raw/brougham.glb');reader=Path('/workspace/shared/brougham-v13-portable-intake-20261022/proposed/chicago/4d/tools/transport/brougham/check_portable.py')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('r',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
helpers=reader.read_text();helpers=helpers[helpers.index('def read(path):'):helpers.index('def check(directory):')]
extra='''def raw_stream(j,b,mesh,kind):
    a=j['accessors'][j['meshes'][mesh]['primitives'][0]['attributes'][kind]];v=j['bufferViews'][a['bufferView']]
    assert a['componentType']==5126 and a['type']=='VEC3' and not v.get('byteStride')
    off=v.get('byteOffset',0)+a.get('byteOffset',0);return b[off:off+a['count']*12]

def component(j,b,part,kind):
    name=f"surface_{part['frame']}_{part['material']}";ids=[i for i,x in enumerate(j['meshes']) if x['name']==name];assert ids
    primitive=j['meshes'][ids[0]]['primitives'][0];stream=raw_stream(j,b,ids[0],kind)
    if 'indices' in primitive:
        vertices=values(j,b,primitive['attributes'][kind]);stream=b''.join(struct.pack('<fff',*vertices[i[0]]) for i in values(j,b,primitive['indices']))
    start=part['triangle_start_in_batch']*36;out=stream[start:start+part['triangles']*36];assert len(out)==part['triangles']*36;return out

def protected_signatures(j,b):
    part=hashlib.sha256();count=0
    for i,p in enumerate(j['extras']['parts']):
        if i in [12,27]:continue
        part.update(struct.pack('<I',i));part.update(json.dumps([p['name'],p['frame'],p['material'],p['triangles']],separators=(',',':')).encode())
        for kind in ['POSITION','NORMAL']:part.update(component(j,b,p,kind))
        count+=1
    mesh=hashlib.sha256();streams=0
    for i,row in enumerate(j['meshes']):
        if row['name']=='surface_vehicle_body_4':continue
        mesh.update(struct.pack('<I',i));mesh.update(row['name'].encode())
        for kind in ['POSITION','NORMAL']:mesh.update(raw_stream(j,b,i,kind));streams+=1
    return {'parts':count,'protected_part_PN_sha256':part.hexdigest(),'mesh_streams':streams,'protected_mesh_PN_sha256':mesh.hexdigest()}

def subtree(j,i):
    yield i
    for child in j['nodes'][i].get('children',[]):yield from subtree(j,child)

def points(j,b,world,root):
    out=[]
    for i in subtree(j,root):
        node=j['nodes'][i]
        if 'mesh' not in node:continue
        for p in j['meshes'][node['mesh']]['primitives']:
            vs=values(j,b,p['attributes']['POSITION']);ids=[x[0] for x in values(j,b,p['indices'])] if 'indices' in p else range(len(vs))
            out.extend(tuple(vs[k][a]+world[i][a] for a in range(3)) for k in ids)
    return out

def bounds(ps):return {'min':[min(p[k] for p in ps) for k in range(3)],'max':[max(p[k] for p in ps) for k in range(3)]}

def native_contacts(j,b):
    world=world_nodes(j);wheels=[]
    for i,n in enumerate(j['nodes']):
        if not n['name'].startswith('vehicle_wheel_'):continue
        ps=points(j,b,world,i);low=min(p[1] for p in ps);lowpoints=sorted(set(p for p in ps if abs(p[1]-low)<1e-7))
        wheels.append({'node':n['name'],'center_root_m':world[i],'bounds_root_m':bounds(ps),'lowest_points_root_m':[list(q) for q in lowpoints]})
    pole=next(i for i,n in enumerate(j['nodes']) if n['name']=='vehicle_team_pole');hitch=next(i for i,n in enumerate(j['nodes']) if n['name']=='vehicle_hitch_team')
    shoe=next(p for p in j['extras']['parts'] if p['name']=='parked_pole_ground_shoe');ps=list(struct.iter_unpack('<fff',component(j,b,shoe,'POSITION')))
    return {'wheels':wheels,'full_fixed_pole_bounds_root_m':bounds(points(j,b,world,pole)),'shoe_bounds_root_m':bounds(ps),'shoe_bottom_corners_root_m':[list(q) for q in sorted(set(p for p in ps if abs(p[1])<1e-7))],'parked_hitch_root_m':world[hitch],'has_tongue_hinge':any(n['name']=='vehicle_tongue' for n in j['nodes'])}
'''
ns={};exec('from pathlib import Path\nimport json,hashlib,math,struct\n'+helpers+extra,ns)
g,b=m.read(V/'raw/brougham.glb');og,ob=m.read(OLD);prot=ns['protected_signatures'](g,b);assert prot==ns['protected_signatures'](og,ob) and prot['parts']==464 and prot['mesh_streams']==46
contacts=ns['native_contacts'](g,b);near,nb=m.read(V/'portable-near/brougham-near.glb');assert ns['native_contacts'](near,nb)==contacts
reports=P/'archived-khronos';reports.mkdir(exist_ok=True)
for name in ['KHRONOS-RAW.json','KHRONOS-NEAR.json']:shutil.copyfile(V/name,reports/name)
contract={'scope':'V14 exact NEAR ONLY native source/delivery contract; not terrain, image, public, mid/far, occupied or photographic acceptance','raw_sha256':h(V/'raw/brougham.glb'),'near_sha256':h(V/'portable-near/brougham-near.glb'),'raw_bytes':(V/'raw/brougham.glb').stat().st_size,'near_bytes':(V/'portable-near/brougham-near.glb').stat().st_size,'triangles':32830,'expanded_PN_sha256':m.expanded(g,b)[0],'bounds_m':m.decoded_bounds(g,b,m.world_nodes(g)),'protected_V13_streams':prot,'native_contacts':contacts,'source_files':{name:h(V/'source'/name) for name in ['generate.py','source_details.py','index_streams.py','static_master.py','parameters.json','lods.json','LICENSE']},'delivery_metadata_files':{name:h(V/'portable-near'/name) for name in ['brougham.json','BUILD-RECEIPT.json','LICENSE']},'archived_khronos':[{'report':name,'report_sha256':h(V/name),'bound_file':'brougham-source.glb' if 'RAW' in name else 'brougham-near.glb','actual_input_sha256':h(V/'raw/brougham.glb') if 'RAW' in name else h(V/'portable-near/brougham-near.glb'),'scope':'Actual archived V14 run_once.py read these paths; original report URI label brougham-v12.glb is historical tool text, not file identity. This gate validates immutable archived evidence, not a fresh Khronos execution.'} for name in ['KHRONOS-RAW.json','KHRONOS-NEAR.json']],'scene_eligibility':json.loads((V/'portable-near/brougham.json').read_text())['scene_eligibility'],'reference_sha256':'b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe','protected_baseline_raw_sha256':h(OLD),'baseline_compared_at_preparation_only':True}
(P/'near-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
body='''def check_near(directory,source_directory):
    here=Path(__file__).resolve().parent;contract_path=here/'near-contract.json'
    assert hashlib.sha256(contract_path.read_bytes()).hexdigest()==EXPECTED_CONTRACT,'Exact reviewed near contract changed'
    c=json.loads(contract_path.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    master=directory/'brougham-source.glb';near=directory/'brougham-near.glb'
    assert sha(master)==c['raw_sha256'] and master.stat().st_size==c['raw_bytes'],'Exact V14 rawmaster'
    assert sha(near)==c['near_sha256'] and near.stat().st_size==c['near_bytes'],'Exact V14 indexednear'
    for name,digest in c['source_files'].items():assert sha(source_directory/name)==digest,'Exact reviewed producer/source/recipe/license '+name
    for name,digest in c['delivery_metadata_files'].items():assert sha(directory/name)==digest,'Exact delivery metadata/license '+name
    j,b=read(master);d,db=read(near);signature,tri=expanded(j,b);near_signature,near_tri=expanded(d,db)
    assert tri==near_tri==c['triangles']==32830 and signature==near_signature==c['expanded_PN_sha256'],'Actual near expanded triangles/P-N'
    for key in ['nodes','materials','scenes','scene','extras','extensionsUsed']:assert j.get(key)==d.get(key),'Preserved raw/near '+key
    assert len(j['nodes'])==41 and len(j['meshes'])==24 and len(j['materials'])==6 and len(j['extras']['parts'])==466
    assert not any(j.get(k) or d.get(k) for k in ['images','textures','skins','animations']) and all('uri' not in q for doc in [j,d] for q in doc['buffers'])
    for doc,bin in [(j,b),(d,db)]:assert decoded_bounds(doc,bin,world_nodes(doc))==c['bounds_m'],'Actual full native envelope'
    assert protected_signatures(j,b)==c['protected_V13_streams'],'464part/46mesh protected baseline streams'
    params=json.loads((source_directory/'parameters.json').read_text());extra=j['extras'];assert extra['parameters']==params
    assert extra['license']=='GPL-3.0-or-later' and extra['units']=='m' and extra['up_axis']=='+Y' and extra['forward_axis']=='+Z' and extra['root_datum']=='ground midpoint between axles'
    assert extra['source_id']=='studebaker_1893_illustrated_souvenir' and extra['source_reference']['scan_leaf']=='0095' and extra['source_reference']['sha256']==c['reference_sha256']
    assert all(extra[k] is False for k in ['door_interaction_enabled','boarding_enabled','traffic_enabled','occupants'])
    side=json.loads((directory/'brougham.json').read_text());assert side['source_master_sha256']==c['raw_sha256'] and side['parameters_sha256']==c['source_files']['parameters.json']
    assert side['grade']=='reconstructed' and side['license']=='GPL-3.0-or-later' and side['scene_eligibility']==c['scene_eligibility'] and extra['scene_year']==1904
    assert len(side['lods'])==1 and side['lods'][0]['detail']=='near' and side['lods'][0]['indexed_sha256']==c['near_sha256'] and side['lod_runtime_selection_enabled'] is False
    world=world_nodes(j);assert len(side['anchors'])==13
    for anchor in side['anchors']:assert anchor['node']==j['nodes'][anchor['node_index']]['name'] and anchor['translation_root_m']==world[anchor['node_index']] and anchor['rotation_xyzw']==[0,0,0,1] and anchor['scale']==[1,1,1] and anchor['dynamic_binding_supported'] is False
    assert side['static_master']['frame']=={'units':'m','up':'+Y','forward':'+Z','root':'vehicle_root'} and all(x is False for x in side['static_master']['capabilities'].values())
    assert len(side['static_master']['named_targets'])==8 and len(side['static_master']['collision_proxy']['components'])==9 and side['static_master']['collision_proxy']['runtime_enabled'] is False
    measured=native_contacts(j,b);assert measured==native_contacts(d,db)==c['native_contacts'],'Actual complete wheel/shoe/pole/hitch readback'
    assert len(measured['wheels'])==4 and measured['has_tongue_hinge'] is False
    for wheel in measured['wheels']:
        center=wheel['center_root_m'];assert len(wheel['lowest_points_root_m'])==1 and abs(wheel['lowest_points_root_m'][0][1])<1e-6
        assert abs(wheel['lowest_points_root_m'][0][0]-center[0])<1e-6 and abs(wheel['lowest_points_root_m'][0][2]-center[2])<1e-6
    assert side['wheel_contacts_root_m']==[[-.67,0,-1.15],[.67,0,-1.15],[-.67,0,1.15],[.67,0,1.15]]
    assert len(measured['shoe_bottom_corners_root_m'])==4
    for point in side['static_pole_ground_shoe_contact_root_m']:assert any(max(abs(a-b) for a,b in zip(point,q))<1e-6 for q in measured['shoe_bottom_corners_root_m'])
    conformance=[]
    for row in c['archived_khronos']:
        report=here/'archived-khronos'/row['report'];assert sha(report)==row['report_sha256'] and sha(directory/row['bound_file'])==row['actual_input_sha256']
        report=json.loads(report.read_text());issues=report['issues'];assert report['validatorVersion']=='2.0.0-dev.3.10' and issues['numErrors']==issues['numWarnings']==0 and issues['numInfos']==4 and not issues['truncated']
        assert sorted((x['code'],x['pointer']) for x in issues['messages'])==[('NODE_EMPTY','/nodes/'+str(i)) for i in [13,14,15,16]]
        assert report['info']['totalTriangleCount']==32830 and report['info']['drawCallCount']==24 and report['info']['hasSkins'] is False and report['info']['hasTextures'] is False
        conformance.append({'file':row['bound_file'],'archived_conformance':'PASS','fresh_execution':False})
    return {'pass':True,'scope':c['scope'],'raw_sha256':c['raw_sha256'],'near_sha256':c['near_sha256'],'triangles':tri,'protected_baseline_streams':c['protected_V13_streams'],'native_contacts':measured,'archived_khronos':conformance,'terrain_world_clearance_verified':False,'visual_or_photographic_acceptance':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--directory',type=Path,required=True);ap.add_argument('--source-directory',type=Path,default=Path(__file__).resolve().parent);a=ap.parse_args();print(json.dumps(check_near(a.directory,a.source_directory)))
'''
header='# SPDX-License-Identifier: GPL-3.0-or-later\n"""V14 NEAR-ONLY original delivery gate. Existing decoded algorithms; no terrain/image/wholeLOD acceptance."""\nfrom pathlib import Path\nimport argparse,hashlib,json,math,struct\nEXPECTED_CONTRACT='+repr(h(P/'near-contract.json'))+'\n\n'
(P/'check_near.py').write_text(header+helpers+extra+body)
print(json.dumps({'prepared':str(R),'checker':str(P/'check_near.py'),'contract_sha256':h(P/'near-contract.json'),'protected':prot,'native':contacts},indent=2))
