"""Provisional fit of hand-read engraving corners, not an image-gate solve."""
import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parent
W,D=28.3464,55.1688
OBS=np.array([[335.,2162.],[737.,2177.],[1076.,2167.], [326.,1808.],[735.,1696.],[1068.,1913.], [357.,1725.],[728.,1591.],[1049.,1853.]])
LABELS=['NE grade','NW grade','SW grade (partly occluded)','NE cornice','NW cornice','SW cornice','NE top roof edge','NW top roof edge','SW top roof edge']
SIGMA=np.array([6,5,12,5,4,6,6,5,8.])

def basis(p):
 yaw,pitch,roll=np.radians(p[2:5]);r=np.array([np.cos(yaw),-np.sin(yaw),0.]);f=np.array([np.sin(yaw)*np.cos(pitch),np.cos(yaw)*np.cos(pitch),np.sin(pitch)]);u=np.cross(r,f);return r*np.cos(roll)+u*np.sin(roll),-r*np.sin(roll)+u*np.cos(roll),f

def project(pts,p):
 r,u,f=basis(p); delta=pts-np.array([p[0],p[1],2.]); z=delta@f; focal=np.exp(p[5]); return np.column_stack([p[6]+focal*(delta@r)/z,p[7]-focal*(delta@u)/z])

def fit(H, inset=.8):
 C=H-7.0104
 pts=np.array([[W/2,0,0],[-W/2,0,0],[-W/2,-D,0], [W/2,0,C],[-W/2,0,C],[-W/2,-D,C], [W/2-inset,-inset,H],[-W/2+inset,-inset,H],[-W/2+inset,-D+inset,H]])
 def residual(p): return ((project(pts,p)-OBS)/SIGMA[:,None]).ravel()
 bounds=([-220,8,100,-12,-4,math.log(200),-500,1200],[-15,220,175,12,4,math.log(6000),1800,2600])
 candidates=[]
 for yaw in [120,135,150]:
  for dist in [35,70,130]:
   x=np.array([-dist,dist, yaw,0,0,math.log(1100),650,2120.])
   sol=least_squares(residual,x,bounds=bounds,max_nfev=5000,xtol=1e-12,ftol=1e-12,gtol=1e-12)
   candidates.append(sol)
 sol=min(candidates,key=lambda s:np.sum(s.fun**2));p=sol.x;pred=project(pts,p);r,u,f=basis(p)
 # Held-out window geometry: nominal actual report9.144m high with candidate sill10.5m.
 win=np.array([[0,0,10.5],[0,0,19.644]])
 wpx=project(win,p)
 return {'roof_height_m':H,'cornice_height_m':C,'roof_inset_m':inset,'eye_m':[float(p[0]),float(p[1]),2.],'yaw_deg':float(p[2]),'pitch_deg':float(p[3]),'roll_deg':float(p[4]),'focal_px':float(np.exp(p[5])),'principal_px':[float(p[6]),float(p[7])],'basis_right_up_forward':[r.tolist(),u.tolist(),f.tolist()],'weighted_cost':float(np.sum(sol.fun**2)),'rms_px':float(np.sqrt(np.mean(np.sum((pred-OBS)**2,axis=1)))),'max_px':float(np.max(np.linalg.norm(pred-OBS,axis=1))),'points':[{'name':n,'world':w.tolist(),'observed_px':o.tolist(),'predicted_px':q.tolist(),'residual_px':float(np.linalg.norm(q-o)),'reading_sigma_px':float(s)}for n,w,o,q,s in zip(LABELS,pts,OBS,pred,SIGMA)],'held_out_central_window':{'candidate_world_m':win.tolist(),'projected_px':wpx.tolist(),'projected_height_px':float(np.linalg.norm(wpx[1]-wpx[0])),'observed_approx_height_px':152,'note':'This evaluates a9.144m report-constrained height at a separately reconstructed sill10.5m. Sourceprintedheight is not surveyvalidation; exactarchvertex reading and opening definition remainuncertain.'},'optimizer_success':bool(sol.success),'boundary_parameters':[name for name,a,lo,hi in zip(['eyeu','eyev','yaw','pitch','roll','logf','cx','cy'],p,bounds[0],bounds[1])if min(a-lo,hi-a)<1e-3]}
if __name__ == '__main__':
    results={'schema':'chamber-preliminary-box-camera-comparison-v1','scope':'Hand-read full-reference pixelcorners; fixed2m eyeheight, fixed28.3464×55.1688m footprint and0.8m roofinset. Metricheights are deliberately alternative reconstructions. Noacceptedcamera/imagegate/noexactheightclaim.','image':{'path':'../references/andreas-p358.jpg','sha256':hashlib.sha256((ROOT.parent/'references'/'andreas-p358.jpg').read_bytes()).hexdigest(),'image_px':[2306,3299]},'parameter_bounds':{'focal_px':[200,6000],'eyeu_m':[-220,-15],'eyev_m':[8,220],'eyeheight_m':2,'pitch_deg':[-12,12],'roll_deg':[-4,4],'principal_x_px':[-500,1800],'principal_y_px':[1200,2600]},'cases':[fit(h)for h in [30.,30.48,32.,37.]]}
    (ROOT/'box-camera-comparison.json').write_text(json.dumps(results,indent=2)+'\n')
    for x in results['cases']: print(x['roof_height_m'],'rms',round(x['rms_px'],3),'eye',[round(a,2)for a in x['eye_m']],'f',round(x['focal_px'],1),'windowheight',round(x['held_out_central_window']['projected_height_px'],2),'boundaries',x['boundary_parameters'])
