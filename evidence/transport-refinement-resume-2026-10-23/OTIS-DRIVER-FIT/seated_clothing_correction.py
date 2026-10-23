# SPDX-License-Identifier: GPL-3.0-or-later
"""Opt-in static seated pelvis raise with fixed complete foot frames.

Original source-Y-up two-bone math, following human_standing_idle's shortest-arc
and law-of-cosines construction. No mesh, rest bone, weights, scale or bench edit.
The source root datum translates with the trunk; the asset wrapper stays identity,
and both foot/ball rigid world frames stay exactly original through leg IK.
"""
import copy,math
def add(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def mul(a,s):return [x*s for x in a]
def dot(a,b):return math.fsum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(dot(a,a))
def unit(a):
 n=norm(a)
 if n<1e-10:raise ValueError('degenerate seated direction')
 return mul(a,1/n)
def mm(a,b):return [[math.fsum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def shortest_arc(a,b):
 a,b=unit(a),unit(b);c=dot(a,b)
 if c<-.999999:raise ValueError('antiparallel seated frame')
 x,y,z=a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0];k=[[0,-z,y],[z,0,-x],[-y,x,0]];kk=mm(k,k)
 return [[float(i==j)+k[i][j]+kk[i][j]/(1+c)for j in range(3)]for i in range(3)]
def correct(pose,raise_m):
 if not math.isfinite(raise_m)or not 0<=raise_m<=.020:raise ValueError('bounded positive seated pelvis raise required')
 out=copy.deepcopy(pose);delta=[0,raise_m,0];fixed={f'{bone}_{s}'for bone in ['calf','foot','ball']for s in ['l','r']};witness={}
 for name,e in out.items():
  if name not in fixed:e['head_m']=add(e['head_m'],delta)
 for side in ['l','r']:
  hip,knee,ankle=[pose[f'{n}_{side}']['head_m']for n in ['thigh','calf','foot']];newhip=add(hip,delta);l1=norm(sub(knee,hip));l2=norm(sub(ankle,knee));direction=sub(ankle,newhip);d=norm(direction)
  if not abs(l1-l2)<d<l1+l2:raise ValueError('unreachable fixed seated foot')
  e=unit(direction);prior=sub(knee,newhip);pole=unit(sub(prior,mul(e,dot(prior,e))));along=(l1*l1-l2*l2+d*d)/(2*d);h=math.sqrt(max(0,l1*l1-along*along));newknee=add(add(newhip,mul(e,along)),mul(pole,h))
  for name,oldsegment,newsegment in [(f'thigh_{side}',sub(knee,hip),sub(newknee,newhip)),(f'calf_{side}',sub(ankle,knee),sub(ankle,newknee))]:out[name]['rotation_3x3']=mm(shortest_arc(oldsegment,newsegment),pose[name]['rotation_3x3'])
  out[f'calf_{side}']['head_m']=newknee
  witness[side]={'hip_m':newhip,'knee_m':newknee,'fixed_ankle_m':ankle,'segment_lengths_m':[norm(sub(newknee,newhip)),norm(sub(ankle,newknee))],'original_segment_lengths_m':[l1,l2]}
 return out,witness
if __name__=='__main__':
 import json
 from pathlib import Path
 p=Path(__file__).resolve().parent;source=Path('/workspace/chicago/chicago/4d/data/humans/poses/w01/bardwell_otis_1835-triangle-corrected-pose.json');base=json.loads(source.read_text());poses=[]
 for dy in [0,.008,.009,.010,.012,.016]:
  pose,witness=correct(base['bone_global_head_rotation'],dy);poses.append({'raise_m':dy,'bone_global_head_rotation':pose,'IK_witnesses':witness})
 (p/'CANDIDATE-POSES.json').write_text(json.dumps({'baseline':base['bone_global_head_rotation'],'candidates':poses},indent=2)+'\n')
