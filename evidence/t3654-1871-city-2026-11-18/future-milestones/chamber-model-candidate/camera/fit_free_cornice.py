"""Alternative box fit allowing visible cornice rather than imposing roof-rise text."""
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from fit_box_cameras import W,D,OBS,LABELS,SIGMA,basis,project
ROOT=Path(__file__).resolve().parent

def fit(H):
 def points(C):return np.array([[W/2,0,0],[-W/2,0,0],[-W/2,-D,0], [W/2,0,C],[-W/2,0,C],[-W/2,-D,C], [W/2-.8,-.8,H],[-W/2+.8,-.8,H],[-W/2+.8,-D+.8,H]])
 def residual(q):return ((project(points(q[8]),q[:8])-OBS)/SIGMA[:,None]).ravel()
 lo=[-220,8,100,-12,-4,math.log(200),-500,1200,H-10]
 hi=[-15,220,175,12,4,math.log(6000),1800,2600,H-3]
 sols=[]
 for yaw in [120,135,150]:
  for d in [35,70]:sols.append(least_squares(residual,[-d,d,yaw,0,0,math.log(1100),650,2120,H-6],bounds=(lo,hi),max_nfev=5000,xtol=1e-12,ftol=1e-12,gtol=1e-12))
 sol=min(sols,key=lambda s:np.sum(s.fun**2));q=sol.x;p=q[:8];pts=points(q[8]);pred=project(pts,p);r,u,f=basis(p)
 win=project(np.array([[0,0,10.5],[0,0,19.644]]),p)
 return {'roof_edge_height_m':H,'cornice_height_m':float(q[8]),'visible_roof_face_rise_m':float(H-q[8]),'eye_m':[float(p[0]),float(p[1]),2.],'yaw_deg':float(p[2]),'pitch_deg':float(p[3]),'roll_deg':float(p[4]),'focal_px':float(np.exp(p[5])),'principal_px':[float(p[6]),float(p[7])],'basis_right_up_forward':[r.tolist(),u.tolist(),f.tolist()],'rms_px':float(np.sqrt(np.mean(np.sum((pred-OBS)**2,axis=1)))),'max_px':float(np.max(np.linalg.norm(pred-OBS,axis=1))),'points':[{'name':n,'world':w.tolist(),'observed_px':o.tolist(),'predicted_px':a.tolist(),'residual_px':float(np.linalg.norm(a-o))}for n,w,o,a in zip(LABELS,pts,OBS,pred)],'heldout_9_144m_window_height_px':float(np.linalg.norm(win[1]-win[0])),'optimizer_success':bool(sol.success),'boundary_parameters':[name for name,a,l,h in zip(['eyeu','eyev','yaw','pitch','roll','logf','cx','cy','cornice'],q,lo,hi)if min(a-l,h-a)<1e-3]}
j={'scope':'Alternative hand-read boxfit. Thecornice isfree, not silentlyderived by subtracting23ft fromcontradictory99ft height. Visiblerooffrontedge doesnot necessarily equal theunshownhighestroofpoint. Noacceptedcamera orauthoritativeheight. Samefootprint/2m-eye/0.8minset assumptionsasbox-camera-comparison.json.','cases':[fit(H)for H in [30,30.48,32,37]]}
(ROOT/'free-cornice-comparison.json').write_text(json.dumps(j,indent=2)+'\n')
for r in j['cases']:print(r['roof_edge_height_m'],round(r['cornice_height_m'],3),round(r['visible_roof_face_rise_m'],3),round(r['rms_px'],3),round(r['heldout_9_144m_window_height_px'],2),r['boundary_parameters'])
