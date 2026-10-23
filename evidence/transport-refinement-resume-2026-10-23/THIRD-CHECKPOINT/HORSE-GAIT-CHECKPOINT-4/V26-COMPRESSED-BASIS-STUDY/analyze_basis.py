"""Read saved accepted CPU poses; measure one spectrum, select rank by error budget.

No new motion/corrective solve, GLB export, portable loader or browser execution.
No basis binary is serialized. Actual original65 physical guards are rechecked
once on the selected Float32 basis representation, not on a rank sweep.
"""
from pathlib import Path
import json,sys,hashlib,time,math
import numpy as np
r=Path(__file__).resolve().parent.parent;d=Path(__file__).resolve().parent;v=r/'V25-ORIENTED-TRIANGLE-ADMM';sys.path.insert(0,str(v));from actual_model import Model
start=time.monotonic();report_path=v/'ACTUAL/ACTUAL-V25-ORIENTED-TRIANGLE-ADMM-ORIGINAL65-READBACK.json';j=json.loads(report_path.read_text());assert j['mechanics_pass']and j['deformation_screen_pass']
pins=json.loads((v/'INPUT-PINS.json').read_text());m=Model(Path(pins['immutable_source_rig']['path']));assert hashlib.sha256(m.raw).hexdigest()==pins['immutable_source_rig']['sha256'];assert np.max(np.abs(m.world(27)-np.eye(4)))<1e-12
with np.load(pins['v16_arrays']['path'])as a:joint=a['mesh_1_joints'];weight=a['mesh_1_weights']
with np.load(pins['phase_a_arrays']['path'])as a:
 classes=a['vertex_classes_1'];protected=a['source_protected_class_ids'];other=np.unique(np.r_[a['vertex_classes_0'],a['vertex_classes_2']]);fixed=np.isin(classes,protected)|np.isin(classes,other)
free=~fixed
pr=m.g['meshes'][m.g['nodes'][27]['mesh']]['primitives'][0];position=m.accessor(pr['attributes']['POSITION']).astype(float);normal=m.accessor(pr['attributes']['NORMAL']).astype(float);tri=m.accessor(pr['indices']).astype(int).reshape(-1,3);ib=m.accessor(m.g['skins'][0]['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1);rest=m.mesh(27)[0]
frames=json.loads((v/'ACTUAL/DIAGNOSTIC-ORIGINAL65-POSE-MATRICES.json').read_text())['frames'];assert len(frames)==65
pose_npz=v/'ACTUAL/DIAGNOSTIC-CORRECTED-FRAMES-NOT-MODEL.npz';Q=[];N=[]
with np.load(pose_npz)as a:
 for i in range(65):Q.append(a[f'{i:02d}_positions']);N.append(a[f'{i:02d}_normals'])
Q=np.asarray(Q);N=np.asarray(N);assert np.array_equal(Q[0],Q[-1])and np.array_equal(N[0],N[-1])
B=[];T=[];oldQ=[];Xpos=[];Xnorm=[];Bbound=1.;fixed_error=0.
for k,frame in enumerate(frames):
 matrices=np.asarray(frame['global_body_frame_matrices']);transforms=matrices@ib;blend=np.einsum('nw,nwij->nij',weight,transforms[joint]);b=blend[:,:3,:3];translation=blend[:,:3,3];base=np.einsum('nij,nj->ni',b,position)+translation
 B.append(b);T.append(translation);oldQ.append(base);delta=Q[k]-base;fixed_error=max(fixed_error,float(np.abs(delta[fixed]).max()));assert np.max(np.abs(delta[fixed]))<1e-12
 pre=np.linalg.solve(b,delta[:,:,None])[:,:,0];pre[fixed]=0.
 preNormal=np.linalg.solve(b,N[k,:, :,None])[:,:,0]-normal
 Xpos.append(pre);Xnorm.append(preNormal)
 op=np.sqrt(np.max(np.sum(np.abs(b),axis=1),axis=1)*np.max(np.sum(np.abs(b),axis=2),axis=1));Bbound=max(Bbound,float(op.max()))
B=np.asarray(B);T=np.asarray(T);oldQ=np.asarray(oldQ);Xpos=np.asarray(Xpos);Xnorm=np.asarray(Xnorm)
assert np.max(np.abs(np.einsum('kvij,kvj->kvi',B,position[None]+Xpos)+T-Q))<1e-10
base_tri=rest[tri];rest_edges=np.linalg.norm(base_tri[:,[1,2,0]]-base_tri[:,[0,1,2]],axis=2);rest_cross=np.cross(base_tri[:,1]-base_tri[:,0],base_tri[:,2]-base_tri[:,0]);rest_area=np.linalg.norm(rest_cross,axis=1);active=free[tri].any(axis=1);edge_budget=area_budget=normal_budget=1e9
for q in Q:
 qt=q[tri];edges=np.linalg.norm(qt[:,[1,2,0]]-qt[:,[0,1,2]],axis=2);mask=(rest_edges>1e-8)&active[:,None];margin=np.minimum(edges-.9*rest_edges,1.1*rest_edges-edges);edge_budget=min(edge_budget,float(margin[mask].min()/2))
 cross=np.cross(qt[:,1]-qt[:,0],qt[:,2]-qt[:,0]);area=np.linalg.norm(cross,axis=1);valid=(rest_area>1e-12)&active;amargin=np.minimum(area-.8*rest_area,1.2*rest_area-area);dot=np.einsum('ij,ij->i',cross,rest_cross)/rest_area;s=np.linalg.norm(qt[:,1]-qt[:,0],axis=1)+np.linalg.norm(qt[:,2]-qt[:,0],axis=1)
 for value,key in [(amargin,'area'),(dot,'normal')]:
  eps=value/(np.sqrt(s*s+4*value)+s)
  if key=='area':area_budget=min(area_budget,float(eps[valid].min()))
  else:normal_budget=min(normal_budget,float(eps[valid].min()))
world_budget=.25*min(edge_budget,area_budget,normal_budget);assert world_budget>0
prepos_budget=world_budget/Bbound;prenorm_budget=1e-4/(4*Bbound)
poswidth=int(free.sum())*3
X=np.concatenate([Xpos[:64,free].reshape(64,-1)/prepos_budget,Xnorm[:64].reshape(64,-1)/prenorm_budget],axis=1);mean=X.mean(axis=0);center=X-mean
U,S,Vh=np.linalg.svd(center,full_matrices=False)
for a in range(len(S)):
 idx=int(np.argmax(np.abs(Vh[a])))
 if Vh[a,idx]<0:Vh[a]*=-1;U[:,a]*=-1
curve=[];approx=np.repeat(mean[None],64,axis=0);selected=None
for rank in range(65):
 error=approx-X;pe=float(np.linalg.norm(error[:,:poswidth].reshape(64,-1,3),axis=2).max());ne=float(np.linalg.norm(error[:,poswidth:].reshape(64,-1,3),axis=2).max());curve.append({'rank':rank,'next_singular_value':float(S[rank])if rank<len(S)else 0.,'max_position_error_budget_units':pe,'max_normal_error_budget_units':ne})
 if selected is None and pe<=1 and ne<=1:selected=rank
 if rank<64:approx+=np.outer(U[:,rank]*S[rank],Vh[rank])
assert selected is not None
scales=np.r_[np.full(poswidth,prepos_budget),np.full(X.shape[1]-poswidth,prenorm_budget)]
mean_real=(mean*scales).astype(np.float32);basis_real=((S[:selected,None]*Vh[:selected])*scales[None]).astype(np.float32);coefficient=U[:64,:selected].astype(np.float32)
# Simulate Float32 shader accumulation, including signed morph weights.
reconstructed=np.repeat(mean_real[None],64,axis=0)
for a in range(selected):reconstructed+=(coefficient[:,a,None]*basis_real[a,None])
predpos=np.zeros_like(Xpos);predpos[:64,free]=reconstructed[:,:poswidth].reshape(64,-1,3);predpos[64]=predpos[0]
prednormal=reconstructed[:,poswidth:].reshape(64,len(position),3)+normal[None];prednormal=np.concatenate([prednormal,prednormal[:1]],axis=0)
points=np.einsum('kvij,kvj->kvi',B,position[None]+predpos)+T;nn=np.einsum('kvij,kvj->kvi',B,prednormal);nn/=np.linalg.norm(nn,axis=2)[:,:,None]
edge_min=area_min=1.;edge_max=area_max=1.;negative=0;minimum_y=1e9
for q in points:
 qt=q[tri];edges=np.linalg.norm(qt[:,[1,2,0]]-qt[:,[0,1,2]],axis=2);valid=rest_edges>1e-8;rat=edges[valid]/rest_edges[valid];edge_min=min(edge_min,float(rat.min()));edge_max=max(edge_max,float(rat.max()));cross=np.cross(qt[:,1]-qt[:,0],qt[:,2]-qt[:,0]);area=np.linalg.norm(cross,axis=1);valid=rest_area>1e-12;rat=area[valid]/rest_area[valid];area_min=min(area_min,float(rat.min()));area_max=max(area_max,float(rat.max()));negative=max(negative,int(np.count_nonzero((np.einsum('ij,ij->i',cross,rest_cross)<0)&valid)));minimum_y=min(minimum_y,float(q[:,1].min()))
loop=float(np.max(np.abs(points[0]-points[-1])));nloop=float(np.max(np.abs(nn[0]-nn[-1])));fixed_world=float(np.max(np.abs(points[:,fixed]-Q[:,fixed])));normal_error=float(np.linalg.norm(nn-N,axis=2).max());position_error=float(np.linalg.norm(points-Q,axis=2).max())
passed=edge_min>=.9 and edge_max<=1.1 and area_min>=.8 and area_max<=1.2 and negative==0 and minimum_y>=-1e-5 and loop<=1e-6 and nloop<=1e-6 and fixed_world<=1e-6
count=selected+1;payload=count*len(position)*3*4*2;gpu=[]
for cap in [2048,4096,8192,16384]:
 width=len(position)*2;height=1
 if width>cap:height=math.ceil(width/cap);width=cap
 gpu.append({'maxTextureSize':cap,'texture_width':width,'texture_height':height,'layers':count,'GPU_FloatRGBA_bytes':width*height*4*4*count,'CPU_texture_backing_bytes':width*height*4*4*count})
out={'status':'SELECTED_FLOAT32_BASIS_CPU_KEY_SCREEN_PASS'if passed else'SELECTED_FLOAT32_BASIS_CPU_KEY_SCREEN_FAIL','source_V25_report_sha256':hashlib.sha256(report_path.read_bytes()).hexdigest(),'source_saved_frames_sha256':hashlib.sha256(pose_npz.read_bytes()).hexdigest(),'pose_evaluations':0,'new_corrective_solves':0,'mean_target_count':1,'selected_rank':selected,'total_morph_targets':count,'feature_scaling':{'derived_world_edge_margin_budget_m':edge_budget,'derived_world_area_margin_budget_m':area_budget,'derived_world_normal_orientation_margin_budget_m':normal_budget,'world_position_error_budget_m_with_75percent_reserve':world_budget,'skin_linear_operator_bound':Bbound,'pre_skin_position_budget_m':prepos_budget,'pre_skin_normal_budget':prenorm_budget,'desired_normal_error':1e-4},'singular_values':S.tolist(),'measured_rank_error_curve':curve,'coefficient_range':[float(coefficient.min()),float(coefficient.max())],'negative_weights_require_actual_portable_loader_proof':True,'CPU_key_screen':{'PASS':passed,'edges':[edge_min,edge_max],'areas':[area_min,area_max],'negative_normal_count':negative,'minimum_y_m':minimum_y,'maximum_position_error_vs_V25_m':position_error,'maximum_shader_normal_error_vs_V25':normal_error,'fixed_source_known_hoof_boundary_max_world_error_m':fixed_world,'source_fixed_recomputation_error_m':fixed_error,'loop_position_error_m':loop,'loop_normal_error':nloop},'prospective_bytes':{'body_mesh_vertices':len(position),'additional_dense_POSITION_NORMAL_target_payload':payload,'additional_dense_CPU_GLTF_morph_attribute_arrays':payload,'morph_weight_key_FLOAT_payload':65*count*4,'GPU_texture_by_cap':gpu},'serialized_basis_or_GLB_exports':0,'portable_loader_or_Mixer_qualified':False,'keys_midpoints_shader_browser_visual_or_natural_gait_approval':False,'seconds':time.monotonic()-start}
(d/'ACTUAL-SPECTRUM-RANK-AND-KEY-SCREEN.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','selected_rank','total_morph_targets','feature_scaling','coefficient_range','CPU_key_screen','prospective_bytes','seconds']},indent=2));assert passed
