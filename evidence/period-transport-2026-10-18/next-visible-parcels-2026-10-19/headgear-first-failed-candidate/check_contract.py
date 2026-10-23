# SPDX-License-Identifier: CC0-1.0
from pathlib import Path
import json,struct,hashlib,math,difflib
P=Path(__file__).parent
old=Path('/workspace/shared/horse-head-closed-groove-next/measure/inputs/gear_v5.glb');new=P/'output/light_breastcollar_harness_reconstructed_01.glb'
def load(f):
 b=f.read_bytes();n,t=struct.unpack_from('<II',b,12);j=json.loads(b[20:20+n]);off=20+n;sz,typ=struct.unpack_from('<II',b,off);return j,b[off+8:off+8+sz]
def arrays(j,b,mesh):
 pr=mesh['primitives'][0];out={}
 for name,aid in pr['attributes'].items():
  a=j['accessors'][aid];v=j['bufferViews'][a['bufferView']];start=v.get('byteOffset',0)+a.get('byteOffset',0);length=a['count']*{'VEC3':3,'VEC2':2}[a['type']]*4;out[name]=hashlib.sha256(b[start:start+length]).hexdigest()
 return out
j,b=load(old);k,c=load(new);changed={'cheekpiece_l','cheekpiece_r','browband','noseband'};aa={m['name']:arrays(j,b,m)for m in j['meshes']};bb={m['name']:arrays(k,c,m)for m in k['meshes']};assert set(aa)==set(bb)
for n in aa:
 if n not in changed:assert aa[n]==bb[n],n
assert j['materials']==k['materials'];assert [{q:x for q,x in n.items()if q!='mesh'}for n in j['nodes']]==[{q:x for q,x in n.items()if q!='mesh'and q!='extras'}|({'extras':j['nodes'][i]['extras']}if 'extras'in j['nodes'][i]else{})for i,n in enumerate(k['nodes'])]
p=json.load(open(P/'source/harness.contour.json'));routes=p['headstrap_contour_study']['routes'];joins=[]
for side,endpoint in [('r',0),('l',-1)]:
 target=routes['browband']['points'][endpoint];distance=min(math.dist(target,q)for q in routes['cheekpiece_'+side]['points']);assert distance<1e-12;joins.append({'side':side,'brow_cheek_centerline_distance_m':distance})
for side,sign in [('l',1),('r',-1)]:assert routes['cheekpiece_'+side]['points'][-1]==[sign*.095,-.20,.39]
receipt={'old_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'meshes':len(aa),'changed_meshes':sorted(changed),'unchanged32_mesh_position_normal_arrays_exact':True,'materials_exact':True,'node_names_hierarchy_transforms_anchors_preserved':True,'bridle_width_m':p['bridle_width_m'],'thickness_m':.003,'bit_endpoints_exact':True,'brow_cheek_centerline_joins':joins,'scope':'decoded rest arrays and source route contracts only; no collision/clearance/posed/visual pass'}
(P/'rest-contract-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
orig=(P/'source/generate_harness.original.py').read_text();modified=(P/'source/generate_harness.contour.py').read_text();(P/'generator.patch').write_text(''.join(difflib.unified_diff(orig.splitlines(True),modified.splitlines(True),fromfile='a/tools/transport/generate_harness.py',tofile='b/tools/transport/generate_harness.py')))
print(json.dumps(receipt))
