"""Preliminary left-stereo camera in full-card pixels; does not render or accept a match.

Run from any working directory with Python, NumPy, SciPy, Pillow and Matplotlib.
Writes only new carbutt-named files beside this helper and the new native camera.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parent
CAMERA=ROOT.parent
CANDIDATE=CAMERA.parent
sys.path.insert(0,str(CAMERA))
from fit_box_cameras import basis, project

recipe=json.loads((CANDIDATE/'data/chamber_of_commerce_1865.recipe.json').read_text())
f=recipe['form'];front=recipe['front']
W,D,C,I=f['width_m'],f['depth_m'],f['cornice_m'],f['roof_inset_m']
H=C+f['roof_rise_m']+f['roof_deck_rise_m']
# All manually read source positions refer to the unmodified 2737 x 1360 card.
# A cornice coordinate is the apparent upper projecting edge, not its bottom dentils.
landmarks=[
 ('NE cornice',[W/2,0,C],[537,445],6,'Upper projecting edge; projection depth not modeled in box point.'),
 ('NW cornice',[-W/2,0,C],[1093,386],5,'Upper projecting edge at visible north/west corner.'),
 ('SW cornice',[-W/2,-D,C],[1296,551],7,'Rear visible edge; distant fine profile is soft.'),
 ('NE upper roof edge',[W/2-I,-I,H],[577,352],5,'Upper roof/coping endpoint; the precise coping projection is uncertain.'),
 ('NW upper roof edge',[-W/2+I,-I,H],[1064,286],4,'Clear front/side upper roof intersection.'),
 ('SW upper roof edge',[-W/2+I,-D+I,H],[1267,489],9,'Soft distant roof termination; greater reading uncertainty.'),
 ('NW grade',[-W/2,0,0],[1095,868],10,'Building pavement contact partly crossed by cart/wheel; no surveyed datum.'),
 ('SW grade',[-W/2,-D,0],[1299,854],12,'Distant building pavement contact partly obscured by street objects.'),
]
# Opening vertices, not the higher ornamental crowns. Centre values follow the
# current recipe, so a residual may be a geometry error as well as a camera error.
arch_observations=[([1025,496],5),([939,505],5),([799,502],7),([671,527],6),([598,535],6)]
for k,(u,(px,sigma)) in enumerate(zip(front['upper_centres_m'],arch_observations)):
 height=front['central_height_m'] if abs(u)<.001 else front['flank_height_m']
 landmarks.append((f'North upper opening {k+1} inner arch vertex',[u,0,front['upper_sill_m']+height],px,sigma,'Inner opening vertex; central pole overlaps part of the frame; no ornamental crest fitted.'))
pts=np.array([p[1] for p in landmarks],float)
obs=np.array([p[2] for p in landmarks],float)
sigma=np.array([p[3] for p in landmarks],float)
lo=np.array([-180,12,100,-15,-5,math.log(250),-400,300],float)
hi=np.array([-4,250,179,15,5,math.log(7000),1800,1600],float)
def residual(p):
 return ((project(pts,p)-obs)/sigma[:,None]).ravel()
sols=[]
for yaw in [140,155,170]:
 for d in [35,65,110]:
  sols.append(least_squares(residual,[-d*.4,d,yaw,0,0,math.log(1300),820,900],bounds=(lo,hi),max_nfev=5000,xtol=1e-12,ftol=1e-12,gtol=1e-12))
sol=min(sols,key=lambda x:float(np.sum(x.fun**2)))
p=sol.x;pred=project(pts,p);r,up,forward=basis(p)
held=[]
for k,(u,px) in enumerate(zip(front['upper_centres_m'],[[1025,666],[939,672],[800,663],[671,681],[598,687]])):
 world=[u,0,front['upper_sill_m']]
 out=project(np.array([world],float),p)[0]
 held.append({'name':f'North upper opening {k+1} sill (held out)','world':world,'observed_px':px,'predicted_px':out.tolist(),'residual_px':float(np.linalg.norm(out-np.array(px))),'reading_sigma_px':8 if k!=2 else 10,'note':'Apparent glazing/sill junction; central balustrade and flanking tree complicate the edge. Not used by fit.'})
reference=CANDIDATE/'references/carbutt/carbutt-nypl-G90F172_009F.png'
report={
 'schema':'carbutt-left-stereo-preliminary-camera-fit-v1',
 'status':'preliminary_not_rendered_not_accepted',
 'reference':'../../references/carbutt/carbutt-nypl-G90F172_009F.png',
 'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),
 'image_px':[2737,1360],
 'coordinate_system':'Full unmodified card, origin upper left, x right and y down. LEFT stereo exposure only. No crop, resample, rectification, or coordinates from the right exposure are used.',
 'selected_exposure_approx_bounds_px':[250,90,1390,1235],
 'model':{'width_m':W,'depth_m':D,'cornice_m':C,'roof_m':H,'roof_inset_m':I,'upper_sill_m':front['upper_sill_m'],'central_height_m':front['central_height_m'],'flank_height_m':front['flank_height_m']},
 'method':'Uncertainty-weighted nonlinear pinhole fit to 13 hand-read architectural points, with five held-out upper sills. Fixed eye height 2m, pixel aspect 1, zero skew. Fit minimizes source-coordinate error against the current reconstructed model. It cannot independently resolve absolute historical height or the basement/street datum.',
 'eye':[float(p[0]),float(p[1]),2.],
 'yaw_deg':float(p[2]),'pitch_deg':float(p[3]),'roll_deg':float(p[4]),
 'focal_px':float(np.exp(p[5])),'principal_px':[float(p[6]),float(p[7])],
 'basis_right_up_forward':[r.tolist(),up.tolist(),forward.tolist()],
 'rms_px':float(np.sqrt(np.mean(np.sum((pred-obs)**2,axis=1)))),
 'max_px':float(np.max(np.linalg.norm(pred-obs,axis=1))),
 'weighted_sum_squares':float(np.sum(sol.fun**2)),
 'optimizer_success':bool(sol.success),
 'parameter_bounds':dict(zip(['eye_east_m','eye_north_m','yaw_deg','pitch_deg','roll_deg','log_focal_px','principal_x_px','principal_y_px'],[[float(a),float(b)] for a,b in zip(lo,hi)])),
 'boundary_parameters':[name for name,v,a,b in zip(['eye_east','eye_north','yaw','pitch','roll','log_focal','principal_x','principal_y'],p,lo,hi) if min(v-a,b-v)<1e-3],
 'fit_points':[{'name':q[0],'world':q[1],'observed_px':q[2],'reading_sigma_px':q[3],'note':q[4],'predicted_px':v.tolist(),'residual_px':float(np.linalg.norm(v-np.array(q[2])))} for q,v in zip(landmarks,pred)],
 'held_out_points':held,
 'excluded_ambiguous_point':{'name':'NE grade','observed_approx_px':[543,870],'reading_sigma_px':25,'note':'Fence, tree, cart and foreground sidewalk prevent reading the actual building-grade intersection; excluded rather than treating a foreground line as building grade.'},
 'limits':['Only one stereo half is fitted. Stereo baseline and optical calibration are unknown; no stereo triangulation is claimed.','Digitized card may contain mounting/scan distortion; no anisotropic scaling is assumed without an independent measurement.','13 fit points are observations of one image, not 13 independent archival dimensions.','Current shell height, upper opening levels, fixed camera eye height and grade all remain reconstruction assumptions.','Two grade observations remain partly obscured and carry reduced weight. Cornice/roof projections are approximated by the shell coordinates.','No model render or accepted image comparison is generated by this helper.']
}
(ROOT/'carbutt-camera-fit-audit.json').write_text(json.dumps(report,indent=2)+'\n')
cam={
 'structure_id':'chamber_of_commerce_1865',
 'source_id':'carbutt_chamber_nypl_G90F172_009F',
 'photo':'../references/carbutt/carbutt-nypl-G90F172_009F.png',
 'image_px':[2737,1360],
 'principal_px':report['principal_px'],'focal_px':report['focal_px'],
 'eye':report['eye'],'yaw_deg':report['yaw_deg'],
 'basis_right_up_forward':report['basis_right_up_forward'],
 'diagnostic_only':True,
 'sky':'overcast','sun_uvy':[-1,1,3],
 'solve':{
  'status':'preliminary_candidate_not_accepted',
  'method':report['method'],
  'exposure':'LEFT stereo half of full unchanged 2737x1360 card; all landmarks and principal point use full-card pixels. No points from the right exposure, no crop/scale transform.',
  'audit':'v2/carbutt-camera-fit-audit.json',
  'rms_px':report['rms_px'],'max_px':report['max_px'],'fit_point_count':len(landmarks),'held_out_point_count':len(held),
  'model_assumptions':report['model'],
  'limits':'Unknown original lens, stereo baseline and scan distortion. Fixed 2m eye height. Grade partly obscured; northeast grade excluded. Roof/cornice extents approximate projecting details. The fit does not resolve the conflicting archival height datum or establish a historical viewer location. Current model must still be rendered and inspected.',
  'lighting':'Soft geometric review key only. Source shows cornice shadows, but no calibrated sunlight/weather reconstruction is claimed by this preliminary camera.',
  'ground':'Common flat model grade only; no actual terrain or street survey verification.',
  'parameter_boundary_hits':report['boundary_parameters'],
  'optical_degeneracy':'The optimizer reaches its +5 degree roll bound and extrapolates principal x to about1550.72px, beyond the selected left exposure. These are model/camera/correspondence degeneracy warnings, not an accepted lens calibration or historical viewer position. All coordinates still refer to the full unmodified card; no right-exposure observations were fitted.'
 }
}
(CAMERA/'carbutt-original-candidate.json').write_text(json.dumps(cam,indent=2)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
im=np.array(Image.open(reference))
fig,ax=plt.subplots(figsize=(13,10),layout='constrained')
ax.imshow(im);ax.set_xlim(500,1340);ax.set_ylim(920,240)
ax.scatter(obs[:,0],obs[:,1],marker='o',facecolors='none',edgecolors='cyan',s=55,label='Observed fit points')
ax.scatter(pred[:,0],pred[:,1],marker='+',color='red',s=55,label='Projected current-model points')
for i,(o,q) in enumerate(zip(obs,pred),1):
 ax.plot([o[0],q[0]],[o[1],q[1]],color='red',linewidth=.8);ax.text(o[0]+4,o[1]-5,str(i),fontsize=8,color='blue')
hobs=np.array([h['observed_px']for h in held]);hpred=np.array([h['predicted_px']for h in held])
ax.scatter(hobs[:,0],hobs[:,1],marker='s',facecolors='none',edgecolors='lime',s=45,label='Observed held-out sills')
ax.scatter(hpred[:,0],hpred[:,1],marker='x',color='magenta',s=45,label='Projected held-out sills')
ax.grid(alpha=.2);ax.legend(loc='lower left');ax.set_title(f'Carbutt LEFT half, full-card pixels — provisional RMS {report["rms_px"]:.2f}px; not accepted')
fig.savefig(ROOT/'carbutt-camera-fit-coordinate-plot.png',dpi=120)
print(json.dumps({'rms_px':report['rms_px'],'max_px':report['max_px'],'eye':report['eye'],'principal_px':report['principal_px'],'focal_px':report['focal_px'],'bounds':report['boundary_parameters'],'held_out_residuals_px':[h['residual_px']for h in held]},indent=2))
