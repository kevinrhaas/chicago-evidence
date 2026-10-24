from pathlib import Path
import runpy,json,struct,hashlib,time,resource,sys
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation
resource.setrlimit(resource.RLIMIT_AS,(1073741824,1073741824))
d=Path(__file__).parent/'V30-PORTABLE-CREEPING-PROTOTYPE';start=time.monotonic();z=runpy.run_path(str(d/'basis.py'));m=z['m'];Model=z['Model'];v=z['v'];r=d.parent
base=Model(Path('/workspace/shared/T2800-V16-PLANTED-STANDING-GLB-EXPORT-ACTUAL-20261023/horse-sevket-v16-planted-standing-v1.glb'));assert hashlib.sha256(base.raw).hexdigest().startswith('b479442c')
for ni in [26,27,28]:
 assert np.array_equal(base.world(ni),m.world(ni))
 for att in ['POSITION','NORMAL','TEXCOORD_0']:
  pa=base.g['meshes'][base.g['nodes'][ni]['mesh']]['primitives'][0];pb=m.g['meshes'][m.g['nodes'][ni]['mesh']]['primitives'][0]
  assert np.array_equal(base.accessor(pa['attributes'][att]),m.accessor(pb['attributes'][att]))
with np.load(z['pins']['v16_arrays']['path'])as saved:
 for mi,ni in enumerate([26,27,28]):
  pr=base.g['meshes'][base.g['nodes'][ni]['mesh']]['primitives'][0]
  assert np.array_equal(base.accessor(pr['attributes']['JOINTS_0']),saved[f'mesh_{mi}_joints'])
  assert np.array_equal(base.accessor(pr['attributes']['WEIGHTS_0']),saved[f'mesh_{mi}_weights'])
assert np.array_equal(base.accessor(base.g['skins'][0]['inverseBindMatrices']),m.accessor(m.g['skins'][0]['inverseBindMatrices']))
g=base.g;binary=bytearray(base.bin)
def ac(a,typ,component=5126,bounds=False):
 a=np.asarray(a,dtype={5126:'<f4'}[component]);a=a.reshape(-1,{'SCALAR':1,'VEC3':3,'VEC4':4}[typ]);assert len(binary)%4==0
 view=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(binary),'byteLength':a.nbytes});binary.extend(a.tobytes());q={'bufferView':view,'componentType':component,'count':len(a),'type':typ}
 if bounds:q.update(min=a.min(axis=0).tolist(),max=a.max(axis=0).tolist())
 idx=len(g['accessors']);g['accessors'].append(q);return idx
count=z['selected']+1;targets=[]
for feature in np.r_[z['mean_real'][None],z['basis_real']]:
 pp=np.zeros((len(z['position']),3),dtype=np.float32);pp[z['free']]=feature[:z['poswidth']].reshape(-1,3);nn=feature[z['poswidth']:].reshape(-1,3)
 targets.append({'POSITION':ac(pp,'VEC3',bounds=True),'NORMAL':ac(nn,'VEC3')})
body=g['meshes'][g['nodes'][27]['mesh']];body['primitives'][0]['targets']=targets;body['weights']=[0.]*count;g['nodes'][27]['weights']=[0.]*count
anim={'name':'RECONSTRUCTED_CREEPING_015MPS_STUDY_NOT_NATURAL_WALK','channels':[],'samplers':[]}
def channel(node,path,times,values,quaternion=False):
 values=np.asarray(values,dtype=float);values[-1]=values[0]
 if quaternion:
  for k in range(1,len(values)):
   if values[k-1]@values[k]<0:values[k]*=-1
  assert np.max(np.abs(values[-1]-values[0]))<1e-12
 spline=CubicSpline(times,values,bc_type='periodic');tangent=spline(times,1);out=np.stack([tangent,values,tangent],axis=1)
 si=len(anim['samplers']);anim['samplers'].append({'input':ac(times,'SCALAR',bounds=True),'output':ac(out,'SCALAR'if path=='weights'else'VEC4'if quaternion else'VEC3'),'interpolation':'CUBICSPLINE'});anim['channels'].append({'sampler':si,'target':{'node':node,'path':path}})
times=np.linspace(0,1.6,129);globals=np.asarray([f['global_body_frame_matrices']for f in z['frames']]);local=[]
for ni in range(26):
 parent=m.parent.get(ni);ll=np.linalg.solve(globals[:,parent],globals[:,ni])if parent is not None else globals[:,ni];local.append(ll)
 old=np.asarray(g['nodes'][ni].get('translation',[0,0,0]));error=float(np.max(np.abs(ll[:,:3,3]-old)))
 if ni==1:channel(ni,'translation',times,ll[:,:3,3])
 else:assert error<1e-12,(ni,error)
 q=Rotation.from_matrix(ll[:,:3,:3]).as_quat();channel(ni,'rotation',times,q,True)
co=np.c_[np.ones(65),np.r_[z['U'][:,:z['selected']],z['U'][:1,:z['selected']]]];channel(27,'weights',np.linspace(0,1.6,65),co)
g.setdefault('animations',[]).append(anim);g['buffers'][0]['byteLength']=len(binary);g.setdefault('extras',{})['V30_study']={'status':'SOURCE_ONLY_PORTABLE_CREEPING_PROTOTYPE_NO_APP_OR_GAIT_ACCEPTANCE','speed_m_s':.15,'profile_unchanged':True,'phase_label_error_documented':True,'maximum_world_flesh_correction_m':.033719906232,'convergence_certified':False,'base_sha256':hashlib.sha256(base.raw).hexdigest(),'morph_order':'bind_local_morph_then_existing_LBS_skin','morph_targets':count}
js=json.dumps(g,separators=(',',':')).encode();js+=b' '*((-len(js))%4);out=struct.pack('<III',0x46546c67,2,28+len(js)+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary;assert len(out)<6*1024*1024
path=d/'creeping-015mps-PORTABLE-STUDY-NOT-APP.glb';path.write_bytes(out)
report={'status':'EXPORTED_SOURCE_ONLY_NOT_ACCEPTED','sha256':hashlib.sha256(out).hexdigest(),'bytes':len(out),'baseline_sha256':hashlib.sha256(base.raw).hexdigest(),'original_BIN_prefix_exact':out[28+len(js):28+len(js)+len(base.bin)]==base.bin,'targets':count,'bone_keys':129,'coefficient_keys':65,'readback_times':257,'maximum_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'seconds':time.monotonic()-start}
(d/'ENCODE-ACTUAL.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert report['maximum_RSS_bytes']<=536870912
controls=json.loads((v/'RERIG-CONTROLS-PROPOSAL-V2.json').read_text());side=json.loads(Path('/workspace/shared/horse-standing-intake-proposal-V2-20261022/proposed/data/transport/parked/horse-sevket-sidecar.json').read_text());piv=np.asarray([m.world(i)[:3,3]for i in range(26)]);reach=[]
for label,row in controls['limbs'].items():
 a,b,c,dd,e=row['joints'];ll=np.linalg.norm(piv[b]-piv[a])+np.linalg.norm(piv[c]-piv[b]);patch=np.unique(z['tri'][side['contacts'][label]['source_triangle_ids']].ravel());hm=float(z['rest'][patch,1].min());delta=piv[c]-piv[a];delta[1]+=.03-hm;transverse=float(delta[0]**2+delta[1]**2);horizontal=float(np.sqrt(max(0,ll*ll-transverse)));bound=2*(horizontal-abs(delta[2]))/.75
 distances=[float(np.linalg.norm(delta+np.array([0,0,sign*1.32*.75/2])))for sign in[-1,1]]
 reach.append({'limb':label,'proximal_two_link_total_m':float(ll),'body_fixed_flat_distal_stance_endpoint_stride_upper_bound_m':bound,'illustrative_1p32m_stride_endpoint_reach_required_m':distances,'illustrative_endpoint_unreachable':max(distances)>=ll})
gait={'status':'ACTUAL_SOURCE_PROFILE_AND_RIG_COMPARISON_NOT_ORDINARY_WALK_ATTESTATION','source':{'stride_m':.24,'cycle_s':1.6,'speed_m_s':.15,'stance_fraction':.75,'stance_s':1.2,'swing_s':.4,'swing_clearance_m':.03,'constant_body_lowering_m':.03,'body_control_height_m':1.02,'fore_a_height_m':1.01,'hind_a_height_m':1.05,'local_stance_sweep_m':.18,'touchdown_time_order_s':[['hind_l',0],['fore_r',.4],['hind_r',.8],['fore_l',1.2]],'inherited_lateral_sequence_label_correct':False,'cyclic_body_vertical_pitch_roll_sway_head_motion':False},'illustrative_reconstructed_engineering_target_ONLY':{'speed_m_s':1.2,'cycle_s':1.1,'stride_m':1.32,'speed_multiple':8,'stride_multiple':5.5,'source_attested_ordinary_horse_gait':False},'unchanged_profile_rig_stance_endpoint_necessary_reach_bounds':reach,'concrete_required_changes':['Select documented ordinary-walk contact time-order; current positive phase offset sign reverses advertised order.','Obtain cleared actual walk measurements/video before choosing ordinary speed/cadence/duty; existing Cuyer anatomy plates and Muybridge gallop do not attest walk timing.','Replace coherent cannon/pastern constraint with anatomically qualified independent carpus/hock/fetlock/hoof articulation and heel/toe roll; current flat-distal fixed-height chain cannot merely scale to illustrative stride.','Author sourced periodic body/COM/scapular/head movement, and continuous entry/exit from30mm walking lowering.','Requalify complete sole loading/contact, triangle strain, selfcollision, naturalness and portable interpolation at new stride/speed, before turning/hitch/driver/traffic.']}
(d/'SOURCE-PHASE-HEIGHT-STRIDE-REACH-COMPARISON.json').write_text(json.dumps(gait,indent=2)+'\n')
