# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded articulated-seat search: source foot/ball frames fixed, no scale/stretch."""
import json,math,copy
from pathlib import Path
from seated_clothing_correction import add,sub,mul,dot,norm,unit,mm,shortest_arc
D=Path(__file__).resolve().parent
old=json.loads((D/'inputs/original-pose.json').read_text())['bone_global_head_rotation']
def pose(rise,theta):
 out=copy.deepcopy(old);delta=[0,rise,0];fixed={f'{n}_{s}'for n in ['calf','foot','ball']for s in ['l','r']}
 for n,e in out.items():
  if n not in fixed:e['head_m']=add(e['head_m'],delta)
 for side,sign in [('l',1),('r',-1)]:
  hip,knee,ankle=[old[f'{n}_{side}']['head_m']for n in ['thigh','calf','foot']];newhip=add(hip,delta);a=norm(sub(knee,hip));b=norm(sub(ankle,knee));axis=unit(sub(ankle,newhip));d=norm(sub(ankle,newhip));p=sub(knee,newhip);pole=unit(sub(p,mul(axis,dot(p,axis))));t=math.radians(theta*sign);cross=[axis[1]*pole[2]-axis[2]*pole[1],axis[2]*pole[0]-axis[0]*pole[2],axis[0]*pole[1]-axis[1]*pole[0]];pole=add(mul(pole,math.cos(t)),mul(cross,math.sin(t)));along=(a*a-b*b+d*d)/(2*d);h=math.sqrt(a*a-along*along);newknee=add(add(newhip,mul(axis,along)),mul(pole,h))
  for n,v,w in [(f'thigh_{side}',sub(knee,hip),sub(newknee,newhip)),(f'calf_{side}',sub(ankle,knee),sub(ankle,newknee))]:out[n]['rotation_3x3']=mm(shortest_arc(v,w),old[n]['rotation_3x3'])
  out[f'calf_{side}']['head_m']=newknee
  assert abs(norm(sub(newknee,newhip))-a)<1e-12 and abs(norm(sub(ankle,newknee))-b)<1e-12
  for n in ['foot','ball']:assert out[f'{n}_{side}']==old[f'{n}_{side}']
 return out
rows=[{'rise_m':dy,'mirrored_knee_pole_angle_deg':t,'pose':pose(dy,t)}for dy in [.010,.012,.01408,.016,.018,.020]for t in [-12,-8,-4,0,4,8,12]]
(D/'BOUNDED-KNEE-SEARCH-POSES.json').write_text(json.dumps(rows)+'\n');print(len(rows),'fixed-foot, fixed-segment articulated poses')
