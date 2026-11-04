"""One bounded CURRENT-ad9 curve authoring attempt. No old parent read, no app writes."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import argparse,copy,datetime,hashlib,importlib.util,json,math,resource,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
POLICY='ROOT_AUTHORIZED_ONE_120S_CURRENT_AD9_CURVE_ONLY_STRIDE_020_ATTEMPT'
EXPECTED='ad9dc060f8630d0de04fef97d716e8c82be3ac8bf070684e78107720c5221ec6'
CLIP='reconstructed_bare_current26_inplace_careful_walk_cubic129_v1'
NEWCLIP='reconstructed_bare_current26_inplace_stride020_curve_candidate_v1'
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(path,data):
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n');temp.replace(path)
def load_module(name,file):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();C=json.loads(a.binding.read_text())
 assert C['policy']==POLICY and C['approved']is True and C['template_only']is False
 assert C['authoring_phase_seconds']==120 and C['authoring_approved']is True
 assert not C['gait_acceptance']and not C['world_acceptance']and not C['runtime_adoption']
 assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(C['expires_utc'].replace('Z','+00:00'))
 assert C['target']==dict(cycle_seconds=1.6,stride_m=.20,speed_mps=.125,stance_duty=.75,swing_lift_m=.01,root_y_m=-(.0052360789850354195+.005237669218331575)/2)
 assert C['originalLimits']==json.loads((R/'ORIGINAL-UNCHANGED-LIMITS.json').read_text())
 assert a.out.is_dir()and not(a.out/'AUTHORING.json').exists()
 # Do not import numpy/scipy or parse model until the approved supervisor starts this child.
 resource.setrlimit(resource.RLIMIT_CPU,(115,116));start=time.monotonic();deadline=start+110
 import numpy as np
 from scipy.optimize import minimize
 p=load_module('bounded_curve_source_math',R/'ORIGINAL_produce_current26_walk.py')
 h=load_module('bounded_curve_hinges',R/'ORIGINAL_hinge_solver.py')
 # Execute the frozen original class body, without its old relative imports/parent configuration.
 src=(R/'ORIGINAL_surface_pose_solver.py').read_text();classbody=src[src.index('class PoseSolver:'):]
 current=Path(C['candidate']);assert sha(current.read_bytes())==EXPECTED
 p.SOURCE=current;p.EXPECTED=EXPECTED;p.TRAVEL=.20;p.T=1.6;p.DUTY=.75;p.LIFT=.01;p.ROOT_Y=C['target']['root_y_m']
 ns=dict(p=p,h=h,np=np,math=math,minimize=minimize,FORE_BIAS=p.TRAVEL*p.DUTY/2);exec(compile(classbody,'FROZEN_ORIGINAL_POSESOLVER_CURRENT_PARENT','exec'),ns);s=ns['PoseSolver']()
 raw=s.raw;doc,binary=s.d,s.b
 original_evaluate=s.evaluate
 def evaluate_with_deadline(label,angles):
  if time.monotonic()>deadline:raise TimeoutError('110s internal deadline during optimizer; original120s outer cap retained')
  return original_evaluate(label,angles)
 s.evaluate=evaluate_with_deadline
 assert len(doc['skins'][0]['joints'])==26
 anim=next(x for x in doc['animations']if x['name']==CLIP);tracks={}
 for channel in anim['channels']:
  sampler=anim['samplers'][channel['sampler']];node=channel['target']['node']
  if channel['target']['path']=='rotation':
   assert sampler['interpolation']=='CUBICSPLINE';tracks[node]=(p.accessor(doc,binary,sampler['input'])[:,0].astype(float),p.accessor(doc,binary,sampler['output']).astype(float).reshape(-1,3,4))
 assert len(tracks)==20
 def seed_at(label,t):
  result=[]
  for node in p.CHAINS[label][0][:4]:
   ts,v=tracks[node];k=min(max(0,int(np.searchsorted(ts,t,side='right')-1)),len(ts)-2);dt=ts[k+1]-ts[k];u=(t-ts[k])/dt
   q=(2*u**3-3*u*u+1)*v[k,1]+(u**3-2*u*u+u)*dt*v[k,2]+(-2*u**3+3*u*u)*v[k+1,1]+(u**3-u*u)*dt*v[k+1,0];q/=np.linalg.norm(q);result.append(2*math.atan2(q[0],q[3]))
  return np.array(result)
 rows=[];critical=[];solved={};times=np.linspace(0,p.T,129,dtype='<f4').astype(float)
 report=dict(status='AUTHORING_RUNNING_NO_CANDIDATE_ACCEPTED',parentSHA256=EXPECTED,target=C['target'],method='Frozen original current26 four-hinge surface optimizer, exact sagittal hoof endpoint and counterrotated hoof; current ad9 curves used only as warm-start angles. Two endpoint-nullspace degrees remain available to allocate shoulder/elbow/carpus/fetlock bending against actual unchanged BODY edges.',originalLimits=C['originalLimits'],rows=rows,critical=critical,all_seven_requalified=False,native='UNRUN',float32_dense='UNRUN',hoof_support_domain='UNRUN',full_route='UNRUN',visual_memory='UNRUN',gaitAccepted=False,runtimeAdoption=False)
 def flush():report['seconds']=time.monotonic()-start;save(a.out/'AUTHORING.json',report)
 def refused(reason):
  report['status']='REFUSED_NO_CANDIDATE_LOCAL_SOLVER_OR_BUDGET';report['reason']=reason;report['parentUnchanged']=current.read_bytes()==raw;flush();print(json.dumps({k:report[k]for k in ('status','reason','seconds')}));return 2
 def solve_one(label,t,kind,index=None):
  if time.monotonic()>deadline:raise TimeoutError('110s internal deadline; original120s outer cap retained')
  seed=seed_at(label,t);angles,record=s.solve(label,t,seed=seed)
  record.update(kind=kind,index=index);rows.append(record);flush()
  # Recalculate geometry: success flag/slack alone are never admission.
  tip,edges,areas,negative=s.evaluate(label,angles);goal,_,_=s.target(label,t)
  okay=bool(record['success']and np.linalg.norm(tip-goal)<1e-8 and edges.min()>=C['originalLimits']['minimum_triangle_edge_ratio']and edges.max()<=C['originalLimits']['maximum_triangle_edge_ratio']and areas.min()>=C['originalLimits']['minimum_triangle_area_ratio']and areas.max()<=C['originalLimits']['maximum_triangle_area_ratio']and negative==0)
  record['admittedKnotOnly']=okay;record['currentCurveSeedAngles']=seed.tolist();flush()
  return angles,record,okay
 flush()
 try:
  # Known actual tight phases first; an unsuccessful local search is evidence only,
  # never a proof that every curve-only solution is impossible.
  for label,t in [('fore_r',1.1781249642372131),('fore_r',1.1828124821186066),('fore_l',.3781249642372131),('hind_r',.7781249642372131),('hind_l',1.578124964237213)]:
   _,record,okay=solve_one(label,t,'known_or_phase_related_interface_probe');critical.append(record);flush()
   if not okay:return refused('No admissible unchanged-limit local posture found at first critical probe; no GLB emitted; this is not a global infeasibility proof')
  for label in p.CHAINS:
   for index,t in enumerate(times[:-1]):
    angles,record,okay=solve_one(label,float(t),'authored_knot',index)
    if not okay:return refused('An authored knot violates an original physical surface/endpoint constraint; no GLB emitted')
    solved[label,index]=angles
   solved[label,128]=solved[label,0].copy()
  # Build analytical task velocities. Native dense checks remain separate.
  def task_velocity(label,t):
   _,phase,stance=s.target(label,t)
   if stance:return np.array([0.,-p.TRAVEL/p.T])
   u=(phase-p.DUTY)/(1-p.DUTY);duration=p.T*(1-p.DUTY);stroke=p.TRAVEL*p.DUTY;m=-p.TRAVEL*(1-p.DUTY)
   z=(stroke*(6*u-6*u*u)+m*(6*u*u-6*u+1))/duration
   y=p.LIFT*(2*u*(1-u)**3-3*u*u*(1-u)**2)/(.4**2*.6**3*duration)if label.startswith('fore')else p.LIFT*math.pi*math.sin(2*math.pi*u)/duration
   return np.array([y,z])
  def endpoint_encoding(q,node):
   q=np.asarray(q,dtype='<f4');angle=2*math.atan2(float(q[0]),float(q[3]));ws=[q[3]];lo=hi=q[3]
   for _ in range(16):lo=np.nextafter(lo,np.float32(-np.inf));hi=np.nextafter(hi,np.float32(np.inf));ws.extend([lo,hi])
   candidates=[q.copy()]
   for w in ws:
    if abs(w)>1:continue
    x=np.float32(math.copysign(math.sqrt(max(0,1-float(w)**2)),float(q[0])))
    for xx in (x,np.nextafter(x,np.float32(-np.inf)),np.nextafter(x,np.float32(np.inf))):candidates.append(np.array([xx,0,0,w],dtype='<f4'))
   scored=[]
   for c in candidates:
    v=c.astype(float);err=float(abs(p.rotation(v)-p.rotation(v/np.linalg.norm(v))).max());delta=abs(2*math.atan2(v[0],v[3])-angle)
    if err<=1e-10 and delta<2e-5:scored.append((delta,err,c))
   assert scored,('No endpoint Float32 encoding inside original strict loop matrix bound',node)
   return min(scored,key=lambda x:(x[0],x[1]))[2]
  parts={}
  for label,(chain,_)in p.CHAINS.items():
   values=[];tangents=[]
   for index,t in enumerate(times):
    angles=solved[label,index];points=[s.rest[chain[0]].copy()];phase=0
    for j in range(4):
     phase+=angles[j];v=s.rest[chain[j+1]]-s.rest[chain[j]];c=math.cos(phase);z=math.sin(phase);points.append(points[-1]+[v[0],c*v[1]-z*v[2],z*v[1]+c*v[2]])
    points=np.array(points);J=np.array([[-(points[-1,2]-points[k,2]),points[-1,1]-points[k,1]]for k in range(4)]).T;velocity=task_velocity(label,float(t));adot=J.T@np.linalg.solve(J@J.T+np.eye(2)*1e-14,velocity);assert np.linalg.norm(J@adot-velocity)<1e-10
    values.append([p.polish_quaternion([math.sin(v/2),0,0,math.cos(v/2)])for v in np.r_[angles,-angles.sum()]])
    tangents.append([[.5*r*math.cos(v/2),0,0,-.5*r*math.sin(v/2)]for v,r in zip(np.r_[angles,-angles.sum()],np.r_[adot,-adot.sum()])])
   values=np.asarray(values,dtype='<f4');tangents=np.asarray(tangents,dtype='<f4')
   for k,node in enumerate(chain):values[0,k]=endpoint_encoding(values[0,k],node)
   values[-1]=values[0];tangents[-1]=tangents[0]
   for k,node in enumerate(chain):parts[node]=np.stack([tangents[:,k],values[:,k],tangents[:,k]],axis=1).reshape(-1,4)
  if time.monotonic()>deadline:return refused('Authoring consumed internal110s budget before append-only serialization')
  # Append-only graph: do not compact, overwrite, transplant old BINs, or alter any old clip.
  child=copy.deepcopy(doc);extra=bytearray();view=len(child['bufferViews'])
  def add(v,kind,lo=None,hi=None):
   values=np.asarray(v,dtype='<f4');off=len(extra);extra.extend(values.tobytes());i=len(child['accessors']);entry=dict(bufferView=view,byteOffset=off,componentType=5126,count=len(values),type=kind)
   if lo is not None:entry.update(min=lo,max=hi)
   child['accessors'].append(entry);return i
  ti=add(times.reshape(-1,1),'SCALAR',[0],[float(times[-1])]);new=dict(name=NEWCLIP,samplers=[],channels=[],extras=dict(qualification='UNQUALIFIED_REVIEW_ONLY',parentSHA256=EXPECTED,intendedCycleDistanceM=.20,intendedMeanSpeedMPS=.125,rootTravelInClipM=0,externalTravelRequiredOnce=True,allSevenAndNativeAndWorldAndVisual='UNRUN'))
  def channel(node,path,ti,out,mode):
   index=len(new['samplers']);new['samplers'].append(dict(input=ti,output=out,interpolation=mode));new['channels'].append(dict(sampler=index,target=dict(node=node,path=path)))
  for node,values in parts.items():channel(node,'rotation',ti,add(values,'VEC4'),'CUBICSPLINE')
  rt=add([[0],[float(times[-1])]],'SCALAR',[0],[float(times[-1])]);rv=add([[0,p.ROOT_Y,0],[0,p.ROOT_Y,0]],'VEC3');channel(0,'translation',rt,rv,'LINEAR')
  child['animations'].append(new);child['bufferViews'].append(dict(buffer=0,byteOffset=len(binary),byteLength=len(extra)));child['buffers'][0]['byteLength']=len(binary)+len(extra)
  candidate=p.pack(child,binary+extra);assert len(candidate)<=4194304,('Original4MiB cap',len(candidate))
  cd,cb=p.read(candidate);clean=copy.deepcopy(cd);clean['animations'].pop();clean['bufferViews'].pop();clean['accessors']=clean['accessors'][:len(doc['accessors'])];clean['buffers'][0]['byteLength']=len(binary)
  assert clean==doc and cb[:len(binary)]==binary and current.read_bytes()==raw
  out=a.out/'UNQUALIFIED-REVIEW-ONLY-stride020.glb';assert not out.exists();out.write_bytes(candidate)
  report.update(status='CURVE_ONLY_CANDIDATE_AUTHORED_UNQUALIFIED_REVIEW_ONLY',candidate=str(out),candidateSHA256=sha(candidate),candidateBytes=len(candidate),exactCurrentParentDocumentRecoverable=True,exactCurrentParentBINPrefix=True,allOldAnimationsExact=True,parentUnchanged=True,warning='Only optimizer knot endpoint/edge/area/normal bounds checked. Full serialized source/native Float32 seven predicates, endpoint loops, original fault controls, hoof-support, full-route and visual/memory remain UNRUN.');flush();print(json.dumps({k:report[k]for k in ('status','candidate','candidateSHA256','seconds')}));return 0
 except TimeoutError as ex:return refused(str(ex))
 except BaseException as ex:
  report['status']='REFUSED_EXCEPTION_NO_CANDIDATE_ACCEPTED';report['error']=repr(ex);flush();raise
if __name__=='__main__':raise SystemExit(main())
