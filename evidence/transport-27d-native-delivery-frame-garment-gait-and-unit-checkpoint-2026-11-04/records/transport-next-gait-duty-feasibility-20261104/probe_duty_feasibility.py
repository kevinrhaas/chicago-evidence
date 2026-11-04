"""24 fixed analytical source-pose probes; no GLB, curves, native decode or application writes."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import argparse,datetime,hashlib,importlib.util,json,math,resource,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
POLICY='ROOT_AUTHORIZED_ONE_120S_CURRENT_AD9_STRIDE016_DUTY78_FIXED24_SOURCE_PROBES_ONLY'
EXPECTED='ad9dc060f8630d0de04fef97d716e8c82be3ac8bf070684e78107720c5221ec6'
CLIP='reconstructed_bare_current26_inplace_careful_walk_cubic129_v1'
TARGET=dict(cycle_seconds=1.6,stride_m=.16,speed_mps=.1,stance_duty=78/128,fore_bias_m=.050625,swing_lift_m=.01,root_y_m=-(.0052360789850354195+.005237669218331575)/2)
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(path,data):
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n');temp.replace(path)
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();C=json.loads(a.binding.read_text())
 assert C['policy']==POLICY and C['approved']is True and C['template_only']is False
 assert C['source_phase_seconds']==120 and C['source_probe_approved']is True and C['target']==TARGET
 assert C['probe_count']==24 and C['max_solver_calls']==96 and not C['generation_approved']
 assert not C['gait_acceptance']and not C['world_acceptance']and not C['runtime_adoption']
 assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(C['expires_utc'].replace('Z','+00:00'))
 limits=json.loads((R/'ORIGINAL-UNCHANGED-LIMITS.json').read_text());assert C['originalLimits']==limits
 schedule_raw=(R/'FIXED-24-PROBES.json').read_bytes();assert sha(schedule_raw)==C['schedule_sha256'];schedule=json.loads(schedule_raw);assert len(schedule['probes'])==24 and schedule['target']==TARGET
 assert a.out.is_dir()and not(a.out/'FEASIBILITY.json').exists()
 # Numpy/scipy/model loading starts only inside the explicitly approved supervised child.
 resource.setrlimit(resource.RLIMIT_CPU,(115,116));started=time.monotonic();deadline=started+110
 import numpy as np
 from scipy.optimize import minimize
 p=module('duty_probe_frozen_math',R/'ORIGINAL_produce_current26_walk.py');h=module('duty_probe_frozen_hinges',R/'ORIGINAL_hinge_solver.py')
 current=Path(C['candidate']);raw=current.read_bytes();assert sha(raw)==EXPECTED==C['candidate_sha256']
 p.SOURCE=current;p.EXPECTED=EXPECTED;p.TRAVEL=.16;p.T=1.6;p.DUTY=78/128;p.LIFT=.01;p.ROOT_Y=TARGET['root_y_m']
 src=(R/'ORIGINAL_surface_pose_solver.py').read_text();ns=dict(p=p,h=h,np=np,math=math,minimize=minimize,FORE_BIAS=.050625)
 exec(compile(src[src.index('class PoseSolver:'):],'FROZEN_ORIGINAL_CLASS_REBOUND_TO_CURRENT_AD9','exec'),ns);s=ns['PoseSolver']();doc,binary=s.d,s.b
 original_evaluate=s.evaluate
 def check_time():
  if time.monotonic()>deadline:raise TimeoutError('110s internal wall deadline, original120s supervisor cap unchanged')
 def evaluate(label,angles):check_time();return original_evaluate(label,angles)
 s.evaluate=evaluate
 assert len(doc['skins'][0]['joints'])==26
 anim=next(x for x in doc['animations']if x['name']==CLIP);tracks={}
 for c in anim['channels']:
  sampler=anim['samplers'][c['sampler']]
  if c['target']['path']=='rotation':
   assert sampler['interpolation']=='CUBICSPLINE';tracks[c['target']['node']]=(p.accessor(doc,binary,sampler['input'])[:,0].astype(float),p.accessor(doc,binary,sampler['output']).astype(float).reshape(-1,3,4))
 assert len(tracks)==20
 def seed_at(label,t):
  # Match normalized stance/swing progress to the CURRENT clip; do not scale angles.
  _,offset=p.CHAINS[label];phase=(t/p.T-offset)%1
  old_phase=.75*phase/p.DUTY if phase<p.DUTY else .75+.25*(phase-p.DUTY)/(1-p.DUTY)
  old_t=((offset+old_phase)%1)*p.T;angles=[]
  for node in p.CHAINS[label][0][:4]:
   ts,v=tracks[node];k=min(max(0,int(np.searchsorted(ts,old_t,side='right')-1)),len(ts)-2);dt=ts[k+1]-ts[k];u=(old_t-ts[k])/dt
   q=(2*u**3-3*u*u+1)*v[k,1]+(u**3-2*u*u+u)*dt*v[k,2]+(-2*u**3+3*u*u)*v[k+1,1]+(u**3-u*u)*dt*v[k+1,0];q/=np.linalg.norm(q);angles.append(2*math.atan2(q[0],q[3]))
  return np.array(angles),old_t
 # Exact original meshes and loader-normalized weights; no image decode or geometry edits.
 meshes=[];classes={};offsets=[0]
 for mi,mesh in enumerate(doc['meshes']):
  assert len(mesh['primitives'])==1;prim=mesh['primitives'][0];attrs=prim['attributes'];P=p.accessor(doc,binary,attrs['POSITION']).astype(float);J=p.accessor(doc,binary,attrs['JOINTS_0']).astype(int);W=p.accessor(doc,binary,attrs['WEIGHTS_0']).astype(float);W=(W/abs(W).sum(1)[:,None]).astype(np.float32).astype(float);tri=p.accessor(doc,binary,prim['indices']).reshape(-1,3);v=P[tri];normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);A=np.linalg.norm(normal,axis=1);edges=np.unique(np.sort(np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[0,2]]]),axis=1),axis=0);L=np.linalg.norm(P[edges[:,1]]-P[edges[:,0]],axis=1);edges=edges[L>1e-8];L=L[L>1e-8]
  meshes.append(dict(P=P,J=J,W=W,tri=tri,N=normal,A=A,edges=edges,L=L))
  for vi,point in enumerate(P):classes.setdefault(tuple(np.rint(point/1e-6).astype(int)),[]).append(offsets[-1]+vi)
  offsets.append(offsets[-1]+len(P))
 pairs=np.array([(rows[0],other)for rows in classes.values()for other in rows[1:]],dtype=int).reshape(-1,2)
 body=meshes[1];contact={};sole={}
 for label,(chain,_)in p.CHAINS.items():
  mass=np.where(body['J']==chain[-1],body['W'],0).sum(1);contact[label]=np.flatnonzero(mass==1);assert len(contact[label])>20;sole[label]=float(body['P'][contact[label],1].min())
 report=dict(status='SOURCE_PROBES_RUNNING_NO_GENERATION_OR_ACCEPTANCE',parentSHA256=EXPECTED,target=TARGET,probe_count=24,max_solver_calls=96,completed_probes=0,completed_solver_calls=0,originalLimits=limits,probes=[],generation=False,native='UNRUN',float32_skinning='UNRUN',serialized_curves='NOT_PRODUCED',dense_all_seven_requalified=False,endpoint_loops='UNRUN',three_original_fault_controls='UNRUN',hoof_support_domain='UNRUN',full_route='UNRUN',visual_memory='UNRUN',gaitAccepted=False,runtimeAdoption=False,support_notice='Duty changes three stance feet to alternating two/three; count and target envelope do not establish support stability or natural gait.')
 def flush():report['seconds']=time.monotonic()-started;save(a.out/'FEASIBILITY.json',report)
 def finish(status,reason,code):
  report.update(status=status,reason=reason,parentUnchanged=current.read_bytes()==raw);assert not list(a.out.glob('*.glb'));flush();print(json.dumps(dict(status=status,reason=reason,completed_probes=report['completed_probes'],completed_solver_calls=report['completed_solver_calls'],seconds=report['seconds'])));return code
 def audit(qs,t):
  root=np.array([0.,p.ROOT_Y,p.TRAVEL*t/p.T]);world=p.fk(doc,qs,root);skin=world@s.ibm;posed=[];surfaces=[];edge_min=area_min=1.;edge_max=area_max=1.;negative=0;minimum_y=float('inf')
  for mi,m in enumerate(meshes):
   out=np.zeros_like(m['P'])
   for slot in range(4):
    M=skin[m['J'][:,slot]];out+=(np.einsum('nij,nj->ni',M[:,:3,:3],m['P'])+M[:,:3,3])*m['W'][:,slot,None]
   posed.append(out);v=out[m['tri']];N=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);ratios=np.linalg.norm(out[m['edges'][:,1]]-out[m['edges'][:,0]],axis=1)/m['L'];areas=np.linalg.norm(N,axis=1)[m['A']>1e-12]/m['A'][m['A']>1e-12];n=int((np.einsum('ij,ij->i',N,m['N'])<0).sum());row=dict(mesh=mi,edgeMin=float(ratios.min()),edgeMax=float(ratios.max()),areaMin=float(areas.min()),areaMax=float(areas.max()),normalNegative=n,minimumY=float(out[:,1].min()));surfaces.append(row);edge_min=min(edge_min,row['edgeMin']);edge_max=max(edge_max,row['edgeMax']);area_min=min(area_min,row['areaMin']);area_max=max(area_max,row['areaMax']);negative+=n;minimum_y=min(minimum_y,row['minimumY'])
  segment=0.;stance=0.;stance_rows=[]
  for label,(chain,offset)in p.CHAINS.items():
   segment=max(segment,float(abs(np.linalg.norm(np.diff(world[chain,:3,3],axis=0),axis=1)-np.linalg.norm(np.diff(s.rest[chain],axis=0),axis=1)).max()));phase=(t/p.T-offset)%1
   if phase<p.DUTY:
    anchor=body['P'][contact[label]].copy();anchor[:,1]-=sole[label];anchor[:,2]+=p.TRAVEL*(math.floor(t/p.T-offset)+offset)+p.TRAVEL*p.DUTY/2+(.050625 if label.startswith('fore')else 0)
    error=np.linalg.norm(posed[1][contact[label]]-anchor,axis=1);worst=int(error.argmax());stance=max(stance,float(error[worst]));stance_rows.append(dict(limb=label,phase=float(phase),patchVertices=len(contact[label]),maxDriftM=float(error[worst]),worstVertex=int(contact[label][worst])))
  points=np.concatenate(posed);seam=float(np.linalg.norm(points[pairs[:,0]]-points[pairs[:,1]],axis=1).max())if len(pairs)else 0.
  checks=dict(originalStancePatchDrift=stance<=limits['stance_patch_drift_m'],originalSegmentLengthError=segment<=limits['segment_length_error_m'],originalEdgeRatioBounds=edge_min>=limits['minimum_triangle_edge_ratio']and edge_max<=limits['maximum_triangle_edge_ratio'],originalAreaRatioBounds=area_min>=limits['minimum_triangle_area_ratio']and area_max<=limits['maximum_triangle_area_ratio'],originalNormalSign=negative==limits['allowed_rest_relative_triangle_normal_dot_negative'],originalGroundMinimum=minimum_y>=limits['minimum_all_surface_y_m'],originalSeamGap=seam<=limits['minimum_seam_gap_tolerance_m'])
  return dict(checks=checks,failures=[k for k,v in checks.items()if not v],maxStanceM=stance,maxSegmentM=segment,edgeMin=edge_min,edgeMax=edge_max,areaMin=area_min,areaMax=area_max,normalNegative=negative,minY=minimum_y,maxSeamM=seam,surfaces=surfaces,stance=stance_rows,stance_count=len(stance_rows),customFloat64PosedSHA256=sha(points.astype('<f8').tobytes()),method='Unserialized double quaternion FK/LBS with actual inverse-bind matrices and loader-normalized Float32 weights, virtual external +Z travel exactly once; custom source arithmetic only, no native loader/mixer/palette claims')
 flush()
 try:
  for probe in schedule['probes']:
   check_time();row=dict(probe=probe,solutions=[]);report['probes'].append(row);flush();t=probe['time_seconds'];qs={}
   # A probe names one limb phase, but all four limbs must be posed for valid full-surface ground/seam/contact checks. At most96 fixed solves; no additional parameter trials.
   order=[probe['limb']]+[label for label in p.CHAINS if label!=probe['limb']]
   for label in order:
    check_time();seed,seed_t=seed_at(label,t);angles,record=s.solve(label,t,seed=seed);tip,edges,areas,negative=s.evaluate(label,angles);goal,_,_=s.target(label,t)
    endpoint=float(np.linalg.norm(tip-goal));record.update(currentCurvePhaseRemappedSeedTimeSeconds=seed_t,currentCurveSeedAngles=seed.tolist(),target=goal.tolist(),endpointResidualM=endpoint)
    record['local_prefilter']=bool(record['success']and endpoint<1e-8 and edges.min()>=limits['minimum_triangle_edge_ratio']and edges.max()<=limits['maximum_triangle_edge_ratio']and areas.min()>=limits['minimum_triangle_area_ratio']and areas.max()<=limits['maximum_triangle_area_ratio']and negative==limits['allowed_rest_relative_triangle_normal_dot_negative']);row['solutions'].append(record);report['completed_solver_calls']+=1;flush()
    if not record['local_prefilter']:return finish('REFUSED_FIXED_PROBE_SOURCE_CONSTRAINT','First local endpoint/surface or solver failure; no GLB; not a global infeasibility proof',2)
    chain,_=p.CHAINS[label]
    for node,angle in zip(chain,np.r_[angles,-angles.sum()]):qs[node]=np.array([math.sin(angle/2),0,0,math.cos(angle/2)])
   check_time();row['whole_pose_source_audit']=audit(qs,t);report['completed_probes']+=1;flush()
   if row['whole_pose_source_audit']['failures']:return finish('REFUSED_FIXED_PROBE_SOURCE_CONSTRAINT','First whole-pose original seven-predicate source failure; no GLB; no thresholds changed',2)
  report['all_seven_at_all_24_unserialized_source_probes']=True
  return finish('FIXED24_SOURCE_PROBES_COMPLETE_NOT_GAIT_OR_NATIVE_ACCEPTANCE','All24 finite source poses pass original seven limits; dense curves/native/controls/support/route/visual remain unqualified; no GLB',0)
 except TimeoutError as ex:return finish('REFUSED_FIXED_PROBE_BUDGET',str(ex),2)
 except BaseException as ex:
  report.update(status='REFUSED_EXCEPTION_NO_GENERATION_OR_ACCEPTANCE',error=repr(ex));flush();raise
if __name__=='__main__':raise SystemExit(main())
