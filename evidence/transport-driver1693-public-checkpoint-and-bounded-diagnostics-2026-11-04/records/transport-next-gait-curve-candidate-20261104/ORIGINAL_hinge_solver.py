import numpy as np,math

def solve(rest,target):
 offsets=np.diff(rest,axis=0);a=np.zeros(4)
 def evaluate(angles):
  p=[rest[0].copy()];phase=0.
  for j in range(4):
   phase+=angles[j];c=math.cos(phase);s=math.sin(phase);v=offsets[j];p.append(p[-1]+[v[0],c*v[1]-s*v[2],s*v[1]+c*v[2]])
  return np.array(p)
 for _ in range(120):
  points=evaluate(a);error=(target-points[-1])[[1,2]];res=np.linalg.norm(error)
  if res<1e-11:break
  J=np.array([[-(points[-1,2]-points[k,2]),points[-1,1]-points[k,1]]for k in range(4)]).T
  # Minimum-change Gauss-Newton with a null-space regularizer; bounded explicit hinge steps.
  M=J@J.T+np.eye(2)*1e-10;P=J.T@np.linalg.solve(M,np.eye(2));step=P@error-.025*(np.eye(4)-P@J)@a
  a+=np.clip(step,-.06,.06);a=np.clip(a,-.7,.7)
 points=evaluate(a);q={j:np.array([math.sin(v/2),0.,0.,math.cos(v/2)])for j,v in enumerate(a)};v=-a.sum();q[4]=np.array([math.sin(v/2),0.,0.,math.cos(v/2)]);return q,float(np.linalg.norm(points[-1]-target))
