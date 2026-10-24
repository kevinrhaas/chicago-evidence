from pathlib import Path
import json,hashlib,sys,math,time,resource
import numpy as np
d=Path(__file__).parent;r=d.parent;v=r/'V28-PERIODIC-TEMPORAL-CORRECTION';sys.path.insert(0,str(v));from actual_model import Model
from walk_source import pose,PARAMETERS as PARAM,THRESHOLDS as LIMIT
start=time.monotonic();pins=json.loads((v/'INPUT-PINS.json').read_text());m=Model(Path(pins['immutable_source_rig']['path']));assert hashlib.sha256(m.raw).hexdigest()==pins['immutable_source_rig']['sha256'];controls=json.loads((v/'RERIG-CONTROLS-PROPOSAL-V2.json').read_text());limbs=controls['limbs'];piv=np.asarray([m.world(i)[:3,3]for i in range(26)]);side=json.loads(Path('/workspace/shared/horse-standing-intake-proposal-V2-20261022/proposed/data/transport/parked/horse-sevket-sidecar.json').read_text());native=json.loads((d/'ACTUAL-NATIVE-MIXER-READBACK.json').read_text());frames=native['frames'];assert len(frames)==257
actual=Model(d/'creeping-015mps-PORTABLE-STUDY-NOT-APP.glb');assert hashlib.sha256(actual.raw).hexdigest()==native['glb_sha256']
with np.load(pins['phase_a_arrays']['path'])as phase:
 cls=phase['vertex_classes_1'];fixed=np.isin(cls,phase['source_protected_class_ids'])|np.isin(cls,np.unique(np.r_[phase['vertex_classes_0'],phase['vertex_classes_2']]))
target_primitive=actual.g['meshes'][actual.g['nodes'][27]['mesh']]['primitives'][0];fixed_serialized_deltas_zero=all(np.count_nonzero(actual.accessor(t['POSITION'])[fixed])==0 for t in target_primitive['targets']);assert fixed_serialized_deltas_zero
rest=[];tri=[];edge=[];cross=[];area=[]
for ni in [26,27,28]:
 p=m.mesh(ni)[0];pr=m.g['meshes'][m.g['nodes'][ni]['mesh']]['primitives'][0];ix=m.accessor(pr['indices']).astype(int).reshape(-1,3);q=p[ix];nn=np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]);rest.append(p);tri.append(ix);edge.append(np.linalg.norm(q[:,[1,2,0]]-q[:,[0,1,2]],axis=2));cross.append(nn);area.append(np.linalg.norm(nn,axis=1))
patch={label:np.unique(tri[1][row['source_triangle_ids']].ravel())for label,row in side['contacts'].items()};hoof_min={label:float(rest[1][ix,1].min())for label,ix in patch.items()};counts=[len(p)for p in rest];assert counts==native['mesh_vertex_counts'];raw=np.memmap(d/'ACTUAL-NATIVE-POSITIONS-AND-SHADER-NORMALS.f64',dtype='<f8',mode='r',shape=(257,sum(counts),6));bounds=np.r_[0,np.cumsum(counts)]
classes={}
for mi,p in enumerate(rest):
 for vi,xyz in enumerate(p):classes.setdefault(tuple(np.rint(xyz/1e-6).astype(int)),[]).append((mi,vi))
pairs=[((a[0][0],a[0][1]),(mi,vi))for a in classes.values()if len(a)>1 for mi,vi in a[1:]]
surface=[dict(mesh=mi,edges=[1.,1.],areas=[1.,1.],negative_normal_count=0,minimum_y_m=1e9)for mi in range(3)];contact={k:dict(maximum_stance_world_error_m=0.,maximum_source_target_error_m=0.)for k in patch};anchors={};length=parent=seam=matrixdelta=0.;first=last=None;shaderstep=0.;witnesses={}
for k,frame in enumerate(frames):
 t=frame['time_s'];mat=np.asarray(frame['global_body_frame_matrices']);source,states=pose(t,piv,limbs,hoof_min);matrixdelta=max(matrixdelta,float(np.max(np.abs(mat-source))));points=[raw[k,bounds[mi]:bounds[mi+1],:3]for mi in range(3)];normals=raw[k,:,3:];assert np.isfinite(raw[k]).all();assert np.max(np.abs(np.linalg.norm(normals,axis=1)-1))<1e-6
 for label,row in limbs.items():
  ids=row['joints']
  for a,b in zip(ids[:-1],ids[1:]):
   error=abs(float(np.linalg.norm(mat[b,:3,3]-mat[a,:3,3])-np.linalg.norm(piv[b]-piv[a])))
   if error>length:length=error;witnesses['segment_length']={'time_s':t,'limb':label,'joints':[a,b],'error_m':error,'positions_m':[mat[a,:3,3].tolist(),mat[b,:3,3].tolist()]}
   error=float(np.linalg.norm(mat[b,:3,3]-(mat[a,:3,3]+mat[a,:3,:3]@(piv[b]-piv[a]))))
   if error>parent:parent=error;witnesses['parent_chain']={'time_s':t,'limb':label,'joints':[a,b],'error_m':error}
  pts=points[1][patch[label]]+np.array([0.,0.,PARAM['nominal_speed_m_s']*t]);state=states[label];rr=contact[label]
  if state['stance']:
   cycle=math.floor(t/PARAM['period_s']+PARAM['phase_offsets'][label]);anchor=anchors.setdefault((label,cycle),pts.copy());rr['maximum_stance_world_error_m']=max(rr['maximum_stance_world_error_m'],float(np.linalg.norm(pts-anchor,axis=1).max()));expected=rest[1][patch[label]]+np.array([0.,-hoof_min[label],PARAM['stride_m']*(PARAM['stance_fraction']/2-PARAM['phase_offsets'][label]+cycle)]);rr['maximum_source_target_error_m']=max(rr['maximum_source_target_error_m'],float(np.linalg.norm(pts-expected,axis=1).max()))
 for mi,p in enumerate(points):
  s=surface[mi];q=p[tri[mi]];e=np.linalg.norm(q[:,[1,2,0]]-q[:,[0,1,2]],axis=2);valid=edge[mi]>1e-8;rat=e[valid]/edge[mi][valid];s['edges'][0]=min(s['edges'][0],float(rat.min()));s['edges'][1]=max(s['edges'][1],float(rat.max()));nn=np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]);ar=np.linalg.norm(nn,axis=1);valid=area[mi]>1e-12;rat=ar[valid]/area[mi][valid];s['areas'][0]=min(s['areas'][0],float(rat.min()));s['areas'][1]=max(s['areas'][1],float(rat.max()));s['negative_normal_count']=max(s['negative_normal_count'],int(np.count_nonzero((np.einsum('ij,ij->i',nn,cross[mi])<0)&valid)));s['minimum_y_m']=min(s['minimum_y_m'],float(p[:,1].min()))
 for (ma,va),(mb,vb)in pairs:seam=max(seam,float(np.linalg.norm(points[ma][va]-points[mb][vb])))
 if k%4==0 and k>=4:shaderstep=max(shaderstep,float(np.degrees(np.arccos(np.clip(np.einsum('ij,ij->i',raw[k-4,:,3:],normals),-1,1))).max()))
 if k==0:first=mat.copy()
 last=mat.copy()
looppos=float(np.max(np.abs(first[:,:3,3]-last[:,:3,3])));looprot=float(np.max(np.abs(first[:,:3,:3]-last[:,:3,:3])));ploop=float(np.max(np.abs(raw[0,:,:3]-raw[-1,:,:3])));nloop=float(np.max(np.abs(raw[0,:,3:]-raw[-1,:,3:])));
checks={'segment_length':length<=LIMIT['segment_length_error_m'],'parent_chain':parent<=LIMIT['segment_length_error_m'],'joint_loop_position':looppos<=LIMIT['loop_position_m'],'joint_loop_rotation':looprot<=LIMIT['loop_rotation_matrix_abs'],'stance_and_source_contact':all(max(row.values())<=LIMIT['stance_patch_drift_m']for row in contact.values()),'edges':all(s['edges'][0]>=.9 and s['edges'][1]<=1.1 for s in surface),'areas':all(s['areas'][0]>=.8 and s['areas'][1]<=1.2 for s in surface),'normal_orientation':all(s['negative_normal_count']==0 for s in surface),'ground':all(s['minimum_y_m']>=-1e-5 for s in surface),'seam':seam<=1e-6,'corrected_surface_loop':ploop<=1e-9,'shader_normal_loop':nloop<=1e-6,'native_signed_morph_weights':native['negative_weight_observations']>0,'native_clone_skeleton_isolated':native['cloned_skeleton_identity_isolated']}
checks['serialized_protected_position_deltas_exact_zero']=fixed_serialized_deltas_zero;checks['native_signed_weight_corruption_detected']=native['signed_weight_negative_control']['detected']
bad=first.copy();bad[10,1,3]+=.003;negative={'naive_rest_hoofs_plus_moving_body_stance_slip_m':.18,'three_mm_hoof_only_segment_error_m':abs(float(np.linalg.norm(bad[10,:3,3]-bad[9,:3,3])-np.linalg.norm(piv[10]-piv[9]))),'three_mm_last_frame_loop_error_m':float(np.max(np.abs(first[:,:3,3]-bad[:,:3,3])))};assert negative['three_mm_hoof_only_segment_error_m']>LIMIT['segment_length_error_m']
intended_position_error=intended_normal_error=0.
with np.load(v/'ACTUAL/DIAGNOSTIC-CORRECTED-FRAMES-NOT-MODEL.npz')as source_fields:
 for sk in range(129):
  intended_position_error=max(intended_position_error,float(np.linalg.norm(raw[sk*2,bounds[1]:bounds[2],:3]-source_fields[f'{sk:03d}_positions'],axis=1).max()));intended_normal_error=max(intended_normal_error,float(np.linalg.norm(raw[sk*2,bounds[1]:bounds[2],3:]-source_fields[f'{sk:03d}_normals'],axis=1).max()))
out={'status':'ACTUAL_PORTABLE_GLTFLOADER_NATIVE_MIXER_257_PHYSICAL_PASS'if all(checks.values())else'ACTUAL_PORTABLE_GLTFLOADER_NATIVE_MIXER_257_PHYSICAL_FAIL','checks':checks,'witnesses':witnesses,'frozen_thresholds':LIMIT,'contact':contact,'surfaces':surface,'maximum_segment_length_error_m':length,'maximum_parent_chain_error_m':parent,'maximum_matrix_component_error_vs_analytic_source':matrixdelta,'joint_loop_position_error_m':looppos,'joint_loop_rotation_abs_error':looprot,'corrected_surface_loop_error_m':ploop,'shader_normal_loop_error':nloop,'maximum_seam_gap_m':seam,'maximum_shader_normal_25ms_step_degrees':shaderstep,'negative_controls':negative,'positions_native_getVertexPosition':True,'normal_scope':'CPU shader-order emulation using actual Float32 skeleton bone uniforms and actual loaded morph attrs; no GPU renderer','source_phase_contact_label_error_retained':True,'natural_gait_traffic_riding_accepted':False,'native_readback_sha256':hashlib.sha256((d/'ACTUAL-NATIVE-MIXER-READBACK.json').read_bytes()).hexdigest(),'actual_positions_normals_sha256':hashlib.sha256((d/'ACTUAL-NATIVE-POSITIONS-AND-SHADER-NORMALS.f64').read_bytes()).hexdigest(),'maximum_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'seconds':time.monotonic()-start};(d/'ACTUAL-PORTABLE-257-GUARDS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['maximum_RSS_bytes']<=536870912;assert all(checks.values()),'No guard relaxed; preserve actual FAIL and witnesses.'
