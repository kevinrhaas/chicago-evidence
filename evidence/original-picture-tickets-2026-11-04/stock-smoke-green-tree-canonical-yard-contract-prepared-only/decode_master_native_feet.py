from pathlib import Path
import json,struct,math,hashlib
root=Path('/tmp/wolf-poster-source-20261103/chicago/4d');p=root/'assets/gltf/green_tree_tavern__frame_1833.glb';b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);off=20+n;bn,bt=struct.unpack_from('<II',b,off);assert bt==0x004e4942;bin=b[off+8:off+8+bn]
fmt={5126:('f',4),5125:('I',4),5123:('H',2),5121:('B',1),5122:('h',2),5120:('b',1)};dim={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
def accessor(i):
 a=d['accessors'][i];assert not a.get('sparse');v=d['bufferViews'][a['bufferView']];f,size=fmt[a['componentType']];k=dim[a['type']];stride=v.get('byteStride',size*k);start=v.get('byteOffset',0)+a.get('byteOffset',0)
 return [struct.unpack_from('<'+f*k,bin,start+j*stride)for j in range(a['count'])]
feet={};primitives=[]
def put(x,z):
 key=(math.floor(x/.5+.5),math.floor(z/.5+.5));feet.setdefault(key,[x,z])
def edge(positions,on,a,b):
 if not on[a] or not on[b]:return
 ax,_,az=positions[a];bx,_,bz=positions[b];steps=max(1,math.ceil(math.hypot(bx-ax,bz-az)))
 for s in range(steps+1):put(ax+(bx-ax)*s/steps,az+(bz-az)*s/steps)
for node in d['nodes']:
 assert not any(k in node for k in ['matrix','translation','rotation','scale']),'unhandled nonidentity native node'
 for pr in d['meshes'][node['mesh']]['primitives']:
  assert pr.get('mode',4)==4
  positions=accessor(pr['attributes']['POSITION']);indices=[r[0]for r in accessor(pr['indices'])]if 'indices'in pr else list(range(len(positions)))
  on=[abs(x[1])<=.05 for x in positions]
  for i in range(0,len(indices),3):
   a,c,e=indices[i:i+3];edge(positions,on,a,c);edge(positions,on,c,e);edge(positions,on,e,a)
  primitives.append({'material':pr.get('material'),'positions':len(positions),'triangles':len(indices)//3,'ground_vertices':sum(on)})
scpath=root/'data/sidecars/1835/green_tree_tavern.json';sc=json.loads(scpath.read_text());shoulder=next(x for x in sc['footprint']['additional_polygons']if x['id']=='shoulder');connector=next(x for x in sc['footprint']['additional_polygons']if x['id']=='connector')
u0=min(p[0]for p in shoulder['polygon']);u1=max(p[0]for p in shoulder['polygon']);v0=min(p[1]for p in shoulder['polygon']);end=min(p[1]for p in connector['polygon'])
outer=[p for p in feet.values()if abs(p[0]-u1)<=.05 and -p[1]>v0+.25 and -p[1]<end-.25]
endfeet=[p for p in feet.values()if abs(-p[1]-v0)<=.05 and p[0]>u0+.25 and p[0]<u1-.25]
receipt={'method':'Exact building-feet.js addFeet algorithm replay on actual native MASTER: FOOT_Y=.05/STEP=1.0/CELL=.5, all10 primitives, identicalJSround floor(x+.5), indices/nativeidentitynode. No Blender/GPU/native regeneration.','master':{'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},'owner':{'path':str(root/'renderers/web/js/building-feet.js'),'sha256':hashlib.sha256((root/'renderers/web/js/building-feet.js').read_bytes()).hexdigest()},'sidecar_sha256':hashlib.sha256(scpath.read_bytes()).hexdigest(),'primitives':primitives,'all_feet':list(feet.values()),'outer_exposed_wall_feet':outer,'end_wall_feet':endfeet,'proposed_native_positive_counts':{'shoulderOuterFeet':len(outer),'shoulderEndFeet':len(endfeet)},'result':'PASS nativeMASTER intendedpositive >=2peredge'if len(outer)>=2 and len(endfeet)>=2 else 'RED proposedexpectationnotvalidated','scope':'MASTERprecheckonly; actualpublishedWEB/browserfeetstillmustbeverified. No fullsmokePASS.'}
out=Path('/tmp/smoke-yard-shadow-triage-20261104/ACTUAL-MASTER-NATIVE-FEET-PRECHECK.json');out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:receipt[k]for k in ['master','proposed_native_positive_counts','outer_exposed_wall_feet','end_wall_feet','result']},indent=2))
