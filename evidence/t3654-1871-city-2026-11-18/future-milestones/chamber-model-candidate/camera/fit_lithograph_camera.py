"""Preliminary camera initialization for the cleared full-page lithograph."""
import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from fit_box_cameras import W,D,basis,project
ROOT=Path(__file__).resolve().parent
H,C,I=31.0104,24.,1.9
obs=np.array([[657,752],[915,785],[1264,784],[653,477],[914,402],[1263,564],[673,410],[912,313],[1257,520]],float)
labels=['NEgrade partlyoccluded','NWgrade','SWgrade obscured by streetfigures','NEcornice','NWcornice','SWcornice','NEtoproofedge','NWtoproofedge','SWtoproofedge']
sigma=np.array([10,7,18,5,5,9,7,5,10],float)
pts=np.array([[W/2,0,0],[-W/2,0,0],[-W/2,-D,0],[W/2,0,C],[-W/2,0,C],[-W/2,-D,C],[W/2-I,-I,H],[-W/2+I,-I,H],[-W/2+I,-D+I,H]])
lo=[-220,8,90,-12,-5,math.log(200),-800,-500];hi=[-15,220,175,12,5,math.log(6000),1800,1500]
def residual(p):return ((project(pts,p)-obs)/sigma[:,None]).ravel()
sols=[]
for yaw in [115,130,145]:
 for d in [40,80,140]:sols.append(least_squares(residual,[-d,d,yaw,0,0,math.log(1100),700,740],bounds=(lo,hi),max_nfev=5000,xtol=1e-12,ftol=1e-12,gtol=1e-12))
sol=min(sols,key=lambda x:np.sum(x.fun**2));p=sol.x;pred=project(pts,p);r,u,f=basis(p)
report={'scope':'Preliminary hand-read lithograph box fit; not an accepted photo camera. Tree and people hide several physical edges. Camera and source dimensions do not establish trueheight.','source_file':'../references/illustrated-plate.png','source_sha256':hashlib.sha256((ROOT.parent/'references'/'illustrated-plate.png').read_bytes()).hexdigest(),'image_px':[1400,1082],'model':{'width_m':W,'depth_m':D,'cornice_m':C,'roof_m':H,'inset_m':I},'eye':[float(p[0]),float(p[1]),2.],'yaw_deg':float(p[2]),'pitch_deg':float(p[3]),'roll_deg':float(p[4]),'focal_px':float(np.exp(p[5])),'principal_px':[float(p[6]),float(p[7])],'basis_right_up_forward':[r.tolist(),u.tolist(),f.tolist()],'rms_px':float(np.sqrt(np.mean(np.sum((pred-obs)**2,axis=1)))),'max_px':float(np.max(np.linalg.norm(pred-obs,axis=1))),'points':[{'name':n,'world':w.tolist(),'observed_px':a.tolist(),'predicted_px':b.tolist(),'residual_px':float(np.linalg.norm(b-a)),'reading_sigma_px':float(s)}for n,w,a,b,s in zip(labels,pts,obs,pred,sigma)],'boundary_parameters':[n for n,x,l,h in zip(['eyeu','eyev','yaw','pitch','roll','logf','cx','cy'],p,lo,hi)if min(x-l,h-x)<1e-3]}
(ROOT/'lithograph-shell-camera-fit.json').write_text(json.dumps(report,indent=2)+'\n')
cam={'structure_id':'chamber_of_commerce_1865','source_id':'chicago_illustrated_chamber_1866_67','photo':'../references/illustrated-plate.png','image_px':[1400,1082],'principal_px':report['principal_px'],'focal_px':report['focal_px'],'eye':report['eye'],'yaw_deg':report['yaw_deg'],'basis_right_up_forward':report['basis_right_up_forward'],'sky':'overcast','sun_uvy':[1,1.5,3],'solve':{'status':'preliminary_candidate_not_accepted','method':'Ninehand-read boxcorners onfullunmodified1400×1082 page; fixed2m eyeheight,pixelaspect1 andactualworkingrecipe31.0104mtop/24mcornice/1.9minset/93×181ftplan. Weightedpinholefit; detailedpoints andresiduals inlithograph-shell-camera-fit.json.','rms_px':report['rms_px'],'max_px':report['max_px'],'fit_point_count':9,'limits':'Westfacepartlyhiddenbytree; gradepartlyhiddenbyfigures; printperspectivenotcalibrated. Roofedges includeprojections. Camera is an initialization with visible residuals, not image-gateacceptance or an archivalheightdatum. Full original-building viewinventory remainsincomplete.','lighting':'Soft geometricreview lighting; not a scene-time weatherassertion.','ground':'Common flatgrade only; actualterraincontact untested.'}}
(ROOT/'illustrated-original-candidate.json').write_text(json.dumps(cam,indent=2)+'\n')
print('lithograph',report['rms_px'],report['max_px'],report['boundary_parameters'])
