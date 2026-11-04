#!/usr/bin/env python3
"""Outside-app reconstructed current26 bare WALK specimen; never native/world/gait acceptance."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[key]='1'
import copy,hashlib,json,math,struct,time,resource,sys
from pathlib import Path
import numpy as np
SOURCE=Path('/workspace/chicago-horse-delivery-20261030/chicago/4d/renderers/web/transport/standing-horse/horse-sevket-quiet-head-neck-idle-v6.glb')
EXPECTED='7ce84d43445e930eecc6d9f69e97ed7ade0fe0b3fc44a9a753c25d88b3f548e1'
LIMITS=Path('/workspace/chicago-horse-delivery-20261030/chicago/4d/tools/transport/horse_socket_interface_v1/fixtures/ORIGINAL-PHYSICAL-LIMITS.json')
OUT=Path(__file__).resolve().parent;NAME='reconstructed_bare_current26_walk_contact_specimen_v4';T=1.6;TRAVEL=.24;DUTY=.75;LIFT=.045;ROOT_Y=-.03;KEYS=97
CHAINS={'hind_l':([16,17,18,19,20],0.),'fore_l':([6,7,8,9,10],.25),'hind_r':([21,22,23,24,25],.5),'fore_r':([11,12,13,14,15],.75)}
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
def read(raw):
 n=struct.unpack_from('<I',raw,12)[0];return json.loads(raw[20:20+n]),raw[28+n:]
def pack(d,b):
 s=json.dumps(d,separators=(',',':'),ensure_ascii=False).encode();s+=b' '*(-len(s)%4);return struct.pack('<5I',0x46546c67,2,28+len(s)+len(b),len(s),0x4e4f534a)+s+struct.pack('<2I',len(b),0x004e4942)+b
def accessor(d,b,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];w={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);assert not a.get('sparse')and not a.get('normalized');return np.ndarray((a['count'],w),dt,b,v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',w*dt.itemsize),dt.itemsize)).copy()
def rotation(q):
 x,y,z,w=q;return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def mul(a,b):
 x,y,z,w=a;X,Y,Z,W=b;return np.array([w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z])
def inv(q):return q*np.array([-1,-1,-1,1])
def fromto(a,b):
 a=a/np.linalg.norm(a);b=b/np.linalg.norm(b);q=np.r_[np.cross(a,b),1+np.dot(a,b)];assert np.linalg.norm(q)>1e-8;return q/np.linalg.norm(q)
def slerp(a,b,u):
 if u==0:return a.copy()
 if u==1:return b.copy()
 b=b.copy();c=float(a@b)
 if c<0:b=-b;c=-c
 if c>=1:return a.copy()
 sq=1-c*c
 if sq<=np.finfo(float).eps:
  q=(1-u)*a+u*b;return q/np.linalg.norm(q)
 theta=math.atan2(math.sqrt(sq),c);return a*(math.sin((1-u)*theta)/math.sin(theta))+b*(math.sin(u*theta)/math.sin(theta))
def fk(doc,qs,root):
 world=[]
 for i,node in enumerate(doc['nodes'][:26]):
  m=np.eye(4);m[:3,:3]=rotation(qs.get(i,np.array([0.,0.,0.,1.])));m[:3,3]=node.get('translation',[0,0,0]);
  if i==0:m[:3,3]=root
  world.append(m if PARENT[i]is None else world[PARENT[i]]@m)
 return np.array(world)
def goal(rest,t,offset,soleY):
 phase=(t/T-offset)%1;stroke=TRAVEL*DUTY
 if phase<DUTY:z=stroke*.5-TRAVEL*phase;y=-soleY-ROOT_Y;stance=True
 else:
  u=(phase-DUTY)/(1-DUTY);h=3*u*u-2*u*u*u;m=-TRAVEL*(1-DUTY);z=-stroke*.5+stroke*h+m*(2*u*u*u-3*u*u+u);y=-soleY-ROOT_Y+LIFT*math.sin(math.pi*u)**2;stance=False
 return rest+np.array([0.,y,z]),phase,stance

def solve(rest,target):
 # Explicit bounded cause correction: distal carpus/hock->fetlock->hoof keeps its
 # source world orientation. Solve the two proximal links around the actual rest pole.
 endpoint=target-(rest[4]-rest[2]);v=endpoint-rest[0];distance=np.linalg.norm(v);direction=v/distance
 l0=np.linalg.norm(rest[1]-rest[0]);l1=np.linalg.norm(rest[2]-rest[1]);assert abs(l0-l1)<distance<l0+l1
 axial=(l0*l0-l1*l1+distance*distance)/(2*distance);height=math.sqrt(max(0,l0*l0-axial*axial))
 restAxis=rest[2]-rest[0];restAxis/=np.linalg.norm(restAxis);pole=rest[1]-rest[0];pole-=restAxis*np.dot(pole,restAxis);pole-=direction*np.dot(pole,direction);assert np.linalg.norm(pole)>1e-8;pole/=np.linalg.norm(pole)
 elbow=rest[0]+direction*axial+pole*height
 first=fromto(rest[1]-rest[0],elbow-rest[0]);second=fromto(rest[2]-rest[1],endpoint-elbow)
 q={0:first,1:mul(inv(first),second),2:inv(second),3:np.array([0.,0.,0.,1.]),4:np.array([0.,0.,0.,1.])}
 for j in q:q[j]/=np.linalg.norm(q[j])
 return q,float(abs(np.linalg.norm(elbow-endpoint)-l1))

def polish_quaternion(q):
 # Deterministic nearby Float32 encoding search, not angular/motion reduction.
 # Tune only nonzero vector component ULPs with w at its nearest and adjacent values.
 base=np.asarray(q,dtype='<f4');best=base.copy();error=abs(float(base.astype(float)@base.astype(float))-1)
 wchoices=[base[3],np.nextafter(base[3],np.float32(-np.inf)),np.nextafter(base[3],np.float32(np.inf))]
 for axis in range(3):
  if abs(base[axis])<1e-8:continue
  values=[base[axis]];lo=hi=base[axis]
  for _ in range(12):lo=np.nextafter(lo,np.float32(-np.inf));hi=np.nextafter(hi,np.float32(np.inf));values.extend([lo,hi])
  for w in wchoices:
   candidates=np.tile(base,(len(values),1));candidates[:,axis]=values;candidates[:,3]=w;errors=np.abs(np.einsum('ij,ij->i',candidates.astype(float),candidates.astype(float))-1);k=int(errors.argmin())
   if errors[k]<error:best=candidates[k].copy();error=float(errors[k])
 return best

def refine_body_weights(doc,binary,meshes):
 m=meshes[1];P=m['p'];original=np.zeros((len(P),26))
 for slot in range(4):np.add.at(original,(np.arange(len(P)),m['j'][:,slot]),m['w'][:,slot])
 groups={}
 for i,p in enumerate(P):groups.setdefault(tuple(np.rint(p/1e-6).astype(int)),[]).append(i)
 rows=list(groups.values());classOf=np.empty(len(P),dtype=int)
 for ci,ids in enumerate(rows):classOf[ids]=ci
 points=np.array([P[ids].mean(0)for ids in rows]);source=np.array([original[ids].mean(0)for ids in rows]);legnodes=[v[0]for v in CHAINS.values()];mass=np.stack([source[:,chain].sum(1)for chain in legnodes],1);labels=mass.argmax(1);legMass=mass.max(1)
 mask=(points[:,1]>.4)&(points[:,1]<1.1)&(legMass>1e-6);taper=np.clip(np.minimum((points[:,1]-.4)/.08,(1.1-points[:,1])/.08),0,1)*mask
 pairs=set()
 for f in m['tri']:
  for a,b in [(f[0],f[1]),(f[1],f[2]),(f[2],f[0])]:
   a,b=sorted((int(classOf[a]),int(classOf[b])))
   if a!=b:pairs.add((a,b))
 edges=np.array(sorted(pairs));a=np.r_[edges[:,0],edges[:,1]];b=np.r_[edges[:,1],edges[:,0]];keep=(labels[a]==labels[b])|(legMass[b]<=1e-6);a=a[keep];b=b[keep];conductance=1/np.maximum(np.linalg.norm(points[a]-points[b],axis=1),1e-4);den=np.bincount(a,conductance,minlength=len(rows));values=source.copy()
 for _ in range(24):
  total=np.zeros_like(values);np.add.at(total,a,values[b]*conductance[:,None]);avg=total/np.maximum(den[:,None],1e-20);values=(1-.90*taper[:,None])*source+.90*taper[:,None]*avg
 # Native four-weight format retained; no joint outside this actual limb and original body.
 output=bytearray(binary);prim=doc['meshes'][1]['primitives'][0];changed=[];maxDropped=0.;maximumSemanticDelta=0.
 for ci,ids in enumerate(rows):
  if not mask[ci]:continue
  dense=values[ci].copy();allowed=set(legnodes[labels[ci]])|{1};dense[[j for j in range(26)if j not in allowed]]=0;order=np.argsort(-dense,kind='stable');maxDropped=max(maxDropped,float(dense[order[4:]].sum()));chosen=order[:4];weights=(dense[chosen]/dense[chosen].sum()).astype('<f4');joints=chosen.astype('<u2');newdense=np.zeros(26);newdense[chosen]=weights.astype(float);maximumSemanticDelta=max(maximumSemanticDelta,float(np.abs(newdense-source[ci]).sum()))
  for i in ids:
   for name,data in [('JOINTS_0',joints.tobytes()),('WEIGHTS_0',weights.tobytes())]:
    acc=doc['accessors'][prim['attributes'][name]];view=doc['bufferViews'][acc['bufferView']];width=8 if name=='JOINTS_0' else 16;offset=view.get('byteOffset',0)+acc.get('byteOffset',0)+i*view.get('byteStride',width);output[offset:offset+width]=data
   changed.append(i)
 report={'status':'EXPLICIT_LOCAL_CURRENT26_BODY_SKIN_REFINEMENT_NOT_NATIVE_ACCEPTANCE','witnessBasis':'Specimen03 BODYfaces4995/4754/4727 and adjacent high-gradient body/limb blends; distal IK and rest-pole causes fixed first','changedBODYRows':len(changed),'changedWeldClasses':int(mask.sum()),'changedVertexIDs':changed,'domain':'BODY only, existing actual current26 limb influence, restY0.4–1.1m; endpoints tapered over0.08m; no hoof/contact row, geometry, UV, material, texture, normal, rest or IBM edit','method':'24 deterministic inverse-edge-length semantic weight smoothing steps,0.90 neighbor coefficient with source prior and endpoint taper; same-limb/body neighbors only; whole coincident-rest classes share tuples; strongest4 normalized actual current26 influences retained','maximumDiscardedSmoothedMassBeforeRenormalization':maxDropped,'maximumSemanticL1Delta':maximumSemanticDelta,'legacyDonors':False,'quietOriginalBoundsMustBeMeasuredFresh':True}
 save('EXPLICIT-LOCAL-BODY-SKIN-REFINEMENT.json',report);return bytes(output),report

def main():
 global PARENT
 resource.setrlimit(resource.RLIMIT_CPU,(4,5));started=time.monotonic();assert not (OUT/'candidate-current26-bare-walk.glb').exists(),'No blind repeat'
 raw=SOURCE.read_bytes();assert sha(raw)==EXPECTED;d,b=read(raw);assert len(d['skins'][0]['joints'])==26 and len(d['animations'])==1
 PARENT={i:None for i in range(26)}
 for i,n in enumerate(d['nodes'][:26]):
  for child in n.get('children',[]):
   if child<26:PARENT[child]=i
 restW=fk(d,{},np.zeros(3));restP=restW[:,:3,3];ibm=accessor(d,b,d['skins'][0]['inverseBindMatrices']).reshape(26,4,4).transpose(0,2,1).astype(float)
 assert np.max(np.abs(restW@ibm-np.eye(4)))<1e-6
 meshes=[]
 for mi,m in enumerate(d['meshes']):
  p=m['primitives'][0];attrs=p['attributes'];pos=accessor(d,b,attrs['POSITION']).astype(float);J=accessor(d,b,attrs['JOINTS_0']).astype(int);W=accessor(d,b,attrs['WEIGHTS_0']).astype(float);W=(W/np.abs(W).sum(1)[:,None]).astype(np.float32).astype(float);tri=accessor(d,b,p['indices']).reshape(-1,3);meshes.append({'p':pos,'j':J,'w':W,'tri':tri})
 body=meshes[1];contact={};sole={}
 for label,(chain,_)in CHAINS.items():
  hoof=chain[-1];mass=np.where(body['j']==hoof,body['w'],0).sum(1);ids=np.flatnonzero(mass==1);assert len(ids)>20;contact[label]=ids;sole[label]=float(body['p'][ids,1].min())
 times=np.linspace(0,T,KEYS,dtype='<f4');tracks={j:[]for chain,_ in CHAINS.values()for j in chain[:3]};maxIK=0
 for time_s in times.astype(float):
  for label,(chain,offset)in CHAINS.items():
   target,phase,stance=goal(restP[chain[-1]],time_s,offset,sole[label]);qs,residual=solve(restP[chain],target);maxIK=max(maxIK,residual)
   for k,j in enumerate(chain[:3]):tracks[j].append(qs[k])
 for j in tracks:tracks[j]=np.array([polish_quaternion(q)for q in tracks[j]],dtype='<f4')
 # Appended floats and a single shared view/accessor offsets keep original 4MiB cap; all nondeclared original bytes remain exact.
 child=copy.deepcopy(d);extra=bytearray();vi=len(child['bufferViews'])
 def add(values,kind,minimum=None,maximum=None):
  off=len(extra);a=np.asarray(values,dtype='<f4');extra.extend(a.tobytes());index=len(child['accessors']);entry={'bufferView':vi,'byteOffset':off,'componentType':5126,'count':len(a),'type':kind}
  if minimum is not None:entry.update(min=minimum,max=maximum)
  child['accessors'].append(entry);return index
 ti=add(times.reshape(-1,1),'SCALAR',[0],[float(times[-1])]);anim={'name':NAME,'samplers':[],'channels':[]}
 def channel(node,path,output):
  sampler=len(anim['samplers']);anim['samplers'].append({'input':ti,'output':output,'interpolation':'LINEAR'});anim['channels'].append({'sampler':sampler,'target':{'node':node,'path':path}})
 for j,values in tracks.items():channel(j,'rotation',add(values,'VEC4'))
 root=np.zeros((KEYS,3),dtype='<f4');root[:,1]=ROOT_Y;root[:,2]=TRAVEL*times/T;channel(0,'translation',add(root,'VEC3'))
 child['animations'].append(anim);child['bufferViews'].append({'buffer':0,'byteOffset':len(b),'byteLength':len(extra)});child['buffers'][0]['byteLength']=len(b)+len(extra);child['asset'].setdefault('extras',{})['bare_walk_specimen']={'parent':EXPECTED,'scope':'reconstructed bare current26 one cycle; UNQUALIFIED; quiet clip retained','native_and_world':'UNRUN'}
 refined,skinReport=refine_body_weights(d,b,meshes);candidate=pack(child,refined+extra);assert len(candidate)<=4*1024**2,('4MiB cap',len(candidate));(OUT/'candidate-current26-bare-walk.glb').write_bytes(candidate)
 # Verify preserved physical/appearance graph and all original stream/quiet bytes independently of new curves.
 cd,cb=read(candidate);clean=copy.deepcopy(cd);clean['asset']['extras'].pop('bare_walk_specimen');clean['animations'].pop();clean['accessors']=clean['accessors'][:len(d['accessors'])];clean['bufferViews']=clean['bufferViews'][:len(d['bufferViews'])];clean['buffers'][0]['byteLength']=len(b);assert clean==d;allowed=np.zeros(len(b),dtype=bool)
 for row in skinReport['changedVertexIDs']:
  for name,width in [('JOINTS_0',8),('WEIGHTS_0',16)]:
   acc=d['accessors'][d['meshes'][1]['primitives'][0]['attributes'][name]];view=d['bufferViews'][acc['bufferView']];off=view.get('byteOffset',0)+acc.get('byteOffset',0)+row*view.get('byteStride',width);allowed[off:off+width]=True
 changed=np.flatnonzero(np.frombuffer(b,dtype='u1')!=np.frombuffer(cb[:len(b)],dtype='u1'));assert allowed[changed].all()
 params={'status':'RECONSTRUCTED_BARE_WALK_SPECIMEN_NOT_GAIT_ACCEPTANCE','parentSHA256':EXPECTED,'candidateSHA256':sha(candidate),'candidateBytes':len(candidate),'unchanged4MiBCap':4*1024**2,'remainingByteHeadroom':4*1024**2-len(candidate),'selectedQuietClipPreservedExact':True,'newClip':NAME,'newChannels':len(tracks)+1,'controlledCauseCorrection':'Specimen01 unconstrained FABRIK caused97degree fetlocks and86degree counter-hooves. This revision preserves the two distal rest directions and solves only actual proximal links using the measured current rest pole; geometry and skin remain exact.','failedSpecimen01Preserved':True,'failedSpecimen02Preserved':True,'fixedMeasuredRestPole':'Rest elbow/stifle residual projected first against the immutable rest endpoint direction, then transported against the current target direction; prevents foreleg bend-plane flips.','keys':KEYS,'cycleSeconds':T,'rootTravelMetres':TRAVEL,'meanRootSpeedMetresPerSecond':TRAVEL/T,'constantRootHeightOffsetMetres':ROOT_Y,'heightOffsetReason':'Reconstructed 30mm crouch within the new animation only permits current near-straight foreleg chain reach over the declared step; rest nodes and all geometry stay exact. No anatomical certification.','quietComposition':'Original quiet curve bytes retained exact, not composed with WALK; localized skin requires fresh quiet metrics.','stanceDutyFraction':DUTY,'localStanceStrokeMetres':TRAVEL*DUTY,'swingLiftMetres':LIFT,'fourBeatContactOrder':['hind_l','fore_l','hind_r','fore_r'],'phaseOffsetCycles':{label:offset for label,(_,offset)in CHAINS.items()},'rootMotionScope':'One nonlooping prototype cycle; relative limb pose periodic. Root translation resets if blindly looped; route/root-motion extraction NOT implemented.','perHoofRestSoleMinimumYMetres':sole,'contactPatchDefinition':'Every actual BODY vertex with exact normalized semantic hoof weight1; includes whole rigid hoof witnesses, not just joint heads. Ground witness is each measured minimum. Blend-boundary and continuous collision remain unqualified.','rigidHoofVertexCounts':{label:len(ids)for label,ids in contact.items()},'maximumTwoLinkTargetResidualMetres':maxIK,'geometryRestIBMMaterialsImagesTexturesAndOriginalQuietCurveGraphExact':True,'skinOnlyExplicitLocalBODYRowsChanged':True,'serializedQuaternionEncoding':'Nearby Float32 ULP search improves unit-norm encoding without reducing the authored angular excursion.','legacy15DonorsRead':False,'nativeMixer':'UNRUN','nativePosedSurface':'UNRUN','publishedUnheldWorld':'UNRUN','gaitAccepted':False,'runtimeAdoption':False}
 save('AUTHORED-SPECIMEN-CONTRACT.json',params)

 assert SOURCE.read_bytes()==raw
 save('CLOSED-LIGHT-AUTHOR-ONLY.json',{'status':'OUTSIDE_APP_LOCAL_SKIN_AND_WALK_AUTHORED_DIAGNOSTICS_UNRUN','candidateSHA256':sha(candidate),'candidateBytes':len(candidate),'sourceSHA256':EXPECTED,'sourceFileUnchanged':True,'seconds':time.monotonic()-started,'nativeMixer':'UNRUN','quietNewSkinBounds':'UNRUN','WALKNewSkinBounds':'UNRUN','runtimeAdoption':False})
 print(json.dumps({'candidateBytes':len(candidate),'authorSeconds':time.monotonic()-started,'sourceChanged':False,'diagnostics':'UNRUN'}))
if __name__=='__main__':main()
