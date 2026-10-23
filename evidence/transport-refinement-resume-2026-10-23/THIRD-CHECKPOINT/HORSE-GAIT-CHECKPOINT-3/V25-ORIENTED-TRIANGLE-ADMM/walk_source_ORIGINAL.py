"""Reconstructed short straight walk proposal, no source animation borrowed.

Actual five-joint chains retain all four segment lengths. Upper and lower links
use rigid two-bone IK; carpus/hock, fetlock and hoof retain world orientation.
No start, stop, turning, load transfer, anatomy or live gait qualification.
"""
import math
import numpy as np
PARAMETERS={'period_s':1.6,'stride_m':.24,'nominal_speed_m_s':.15,'stance_fraction':.75,'unloaded_hoof_peak_clearance_m':.03,'body_lowering_m':.03,'phase_offsets':{'hind_l':0.,'fore_l':.25,'hind_r':.5,'fore_r':.75},'forward':'+Z','up':'+Y','source':'Explicit authored lateral-sequence four-beat schedule, not measured donor motion or anatomical certification.'}
THRESHOLDS={'stance_patch_drift_m':1e-5,'segment_length_error_m':1e-9,'loop_position_m':1e-9,'loop_rotation_matrix_abs':1e-9,'negative_control_min_detected_m':.001,'minimum_triangle_edge_ratio':.9,'maximum_triangle_edge_ratio':1.1,'minimum_triangle_area_ratio':.8,'maximum_triangle_area_ratio':1.2,'allowed_rest_relative_triangle_normal_dot_negative':0,'minimum_all_surface_y_m':-1e-5,'minimum_seam_gap_tolerance_m':1e-6}
def unit(v):
 n=np.linalg.norm(v)
 if n<1e-12:raise ValueError('Degenerate IK vector')
 return v/n
def arc(a,b):
 a,b=unit(a),unit(b);c=float(a@b)
 if c<-.999999:raise ValueError('Antiparallel segment')
 x,y,z=np.cross(a,b);k=np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
 return np.eye(3)+k+k@k/(1+c)
def path(t,offset):
 p=PARAMETERS;phase=(t/p['period_s']+offset)%1;d=p['stance_fraction'];sweep=p['stride_m']*d
 if phase<d:return np.array([0.,0.,sweep/2-p['stride_m']*phase]),True,phase
 u=(phase-d)/(1-d);duration=p['period_s']*(1-d)
 # Quintic position interpolates rear->front with local endpoint velocity -v
 # and zero acceleration, matching stationary world stance at each boundary.
 h=10*u**3-15*u**4+6*u**5
 z=-sweep/2-p['nominal_speed_m_s']*duration*u+(sweep+p['nominal_speed_m_s']*duration)*h
 y=p['unloaded_hoof_peak_clearance_m']*64*u**3*(1-u)**3
 return np.array([0.,y,z]),False,phase
def pose(t,pivots,limbs,hoof_min_y):
 p=PARAMETERS;xyz=pivots.copy();xyz[1:,1]-=p['body_lowering_m'];rot=np.repeat(np.eye(3)[None],len(pivots),axis=0);states={}
 for label,row in limbs.items():
  a,b,c,d,e=row['joints'];target_delta,stance,phase=path(t,p['phase_offsets'][label]);target_delta[1]-=hoof_min_y[label]
  target=pivots[e]+target_delta;carpus=target-(pivots[e]-pivots[c]);hip=xyz[a];old_a=pivots[b]-pivots[a];old_b=pivots[c]-pivots[b];l1,l2=np.linalg.norm(old_a),np.linalg.norm(old_b);line=carpus-hip;distance=np.linalg.norm(line)
  if not abs(l1-l2)<distance<l1+l2:raise ValueError(f'Unreachable {label}: {distance} not ({abs(l1-l2)},{l1+l2})')
  direction=unit(line);prior=pivots[b]-hip;pole=unit(prior-direction*(prior@direction));along=(l1*l1-l2*l2+distance*distance)/(2*distance);height=math.sqrt(max(0,l1*l1-along*along));knee=hip+along*direction+height*pole
  xyz[b],xyz[c],xyz[d],xyz[e]=knee,carpus,target-(pivots[e]-pivots[d]),target
  rot[a]=arc(old_a,knee-hip);rot[b]=arc(old_b,carpus-knee)
  states[label]={'stance':stance,'phase':phase,'target_local_m':target.tolist(),'reach_margin_m':float(l1+l2-distance)}
 matrices=np.repeat(np.eye(4)[None],len(pivots),axis=0);matrices[:,:3,:3]=rot;matrices[:,:3,3]=xyz
 return matrices,states
