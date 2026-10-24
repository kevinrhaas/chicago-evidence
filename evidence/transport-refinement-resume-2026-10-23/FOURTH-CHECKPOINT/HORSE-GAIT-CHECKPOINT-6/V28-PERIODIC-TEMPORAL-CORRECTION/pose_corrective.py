"""One jointly periodic material correction study; no foot/gait parameter changes."""
from pathlib import Path
import json,hashlib,time
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import splu
from scipy.interpolate import CubicSpline
from walk_source import pose,PARAMETERS

class Corrector:
 def __init__(self,parts,rest,piv,ib,here,limbs,hoof_min):
  started=time.monotonic();self.spec=json.loads((here/'PERIODIC-MATERIAL-SMOOTHING.json').read_text());pins=json.loads((here/'INPUT-PINS.json').read_text());warm=json.loads((here/'TEMPORAL-WARMSTART-PINS.json').read_text())
  for row in warm.values():assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
  j=json.loads(Path(warm['V25_report']['path']).read_text());assert j['mechanics_pass']and j['deformation_screen_pass']
  with np.load(pins['phase_a_arrays']['path'],allow_pickle=False)as a:
   cls=a['vertex_classes_1'];protected=a['source_protected_class_ids'];other=np.unique(np.r_[a['vertex_classes_0'],a['vertex_classes_2']])
  self.ids,self.first,self.reverse=np.unique(cls,return_index=True,return_inverse=True);self.p=rest[1][self.first].copy();self.n=len(self.p)
  fixed=np.isin(self.ids,protected)|np.isin(self.ids,other);self.fixed=np.flatnonzero(fixed);self.free=np.flatnonzero(~fixed)
  tri=self.reverse[parts[1][4]];self.alltri=tri
  xyz=self.p[tri];e01=xyz[:,1]-xyz[:,0];e02=xyz[:,2]-xyz[:,0];cross=np.cross(e01,e02);area2=np.linalg.norm(cross,axis=1);valid=area2>1e-12
  self.tri=tri[valid];e01=e01[valid];e02=e02[valid];area2=area2[valid];e1=e01/np.linalg.norm(e01,axis=1)[:,None];normal=np.cross(e01,e02)/area2[:,None];e2=np.cross(normal,e1)
  Dm=np.zeros((len(e01),2,2));Dm[:,0,0]=np.linalg.norm(e01,axis=1);Dm[:,0,1]=np.einsum('ij,ij->i',e02,e1);Dm[:,1,1]=np.einsum('ij,ij->i',e02,e2)
  self.G=np.einsum('va,tab->tvb',np.array([[-1.,-1.],[1.,0.],[0.,1.]]),np.linalg.inv(Dm));self.area=area2*.5;self.rest_normal=normal;self.rest_tangent=e1
  blocks=self.area[:,None,None]*np.einsum('tva,twa->tvw',self.G,self.G);ii=np.repeat(self.tri,3,axis=1).reshape(-1);jj=np.tile(self.tri,(1,3)).reshape(-1)
  L=coo_matrix((blocks.reshape(-1),(ii,jj)),shape=(self.n,self.n)).tocsc();diag=L.diagonal();assert(diag>0).all();self.diag=diag
  phase_count=self.spec['phase_count'];assert phase_count==64;self.period=PARAMETERS['period_s'];times=np.arange(phase_count)*self.period/phase_count
  pos,nor,joint,weight,_=parts[1];targets=[]
  for t in times:
   matrices,_=pose(float(t),piv,limbs,hoof_min);transforms=matrices@ib;blend=np.einsum('nw,nwij->nij',weight,transforms[joint]);target=np.einsum('nij,nj->ni',blend,np.c_[pos,np.ones(len(pos))])[:,:3];targets.append(target[self.first])
  target=np.asarray(targets);q=[]
  with np.load(warm['V25_frames']['path'],allow_pickle=False)as a:
   for k in range(phase_count):q.append(a[f'{k:02d}_positions'][self.first])
  q=np.asarray(q);assert np.max(np.abs(q[:,self.fixed]-target[:,self.fixed]))<1e-12;q[:,self.fixed]=target[:,self.fixed]
  fid=self.spec['fidelity_fraction'];h=self.spec['cutoff_harmonic'];cut_eigen=16*np.sin(np.pi*h/phase_count)**4;self.tau=fid/cut_eigen
  factors=[];factor_nnz=[]
  for f in range(phase_count//2+1):
   eigen=16*np.sin(np.pi*f/phase_count)**4;K=L[self.free][:,self.free]+diags((fid+self.tau*eigen)*diag[self.free],format='csc');factor=splu(K,permc_spec='MMD_AT_PLUS_A');factors.append(factor);factor_nnz.append(int(factor.L.nnz+factor.U.nnz))
  # The target already satisfies exact fixed rows. Solve only displacement,
  # so the spatial RHS subtracts the full L*target and fixed displacement=0.
  Ltarget=np.asarray([(L@p)[self.free]for p in target]);F=self.gradient(q);Z=self.project(F);dual=np.zeros_like(Z);history=[]
  for iteration in range(self.spec['iterations']):
   vertex_rhs=self.area[None,:,None,None]*np.einsum('tva,ktca->ktvc',self.G,Z-dual);rhs=np.zeros((phase_count,self.n,3))
   for k in range(phase_count):np.add.at(rhs[k],self.tri.reshape(-1),vertex_rhs[k].reshape(-1,3))
   rhs=rhs[:,self.free]-Ltarget;freq=np.fft.rfft(rhs,axis=0,norm='ortho');solution=np.empty_like(freq)
   for f,factor in enumerate(factors):solution[f]=factor.solve(freq[f].real)+1j*factor.solve(freq[f].imag)
   delta=np.fft.irfft(solution,n=phase_count,axis=0,norm='ortho');nxt=target.copy();nxt[:,self.free]+=delta;step=float(np.linalg.norm(nxt-q,axis=2).max());q=nxt
   F=self.gradient(q);oldZ=Z;Z=self.project(F+dual);dual+=F-Z
   if iteration in [0,9,24,49,74,99]:history.append({'iteration':iteration+1,'maximum_primal_residual':float(np.linalg.norm(F-Z,axis=(2,3)).max()),'maximum_dual_projection_step':float(np.linalg.norm(Z-oldZ,axis=(2,3)).max()),'maximum_position_iteration_step_m':step})
  assert np.array_equal(q[:,self.fixed],target[:,self.fixed])and np.isfinite(q).all()
  deltas=q-target;assert np.max(np.abs(deltas[:,self.fixed]))==0
  cyclic_times=np.r_[times,self.period];cyclic_delta=np.concatenate([deltas,deltas[:1]],axis=0);self.spline=CubicSpline(cyclic_times,cyclic_delta,axis=0,bc_type='periodic');self.fields=deltas;self.target=target
  self.solver_receipt={'phase_count':phase_count,'source_pose_evaluations_before_screen':phase_count,'iterations':self.spec['iterations'],'cutoff_harmonic':h,'temporal_tau':float(self.tau),'fidelity_fraction':fid,'shifted_spatial_factorizations':len(factors),'free_factor_size':len(self.free),'factor_LU_nnz_total':sum(factor_nnz),'history':history,'elapsed_s':time.monotonic()-started,'interpolation':'Periodic cubic world-displacement spline; original analytic skeleton/footprofile at queried times. Not GLTF/Mixer interpolation.'}
  self.calls=0;self.maxcorrection=0.;self.frames=[];self.geonormals=[];self.max_undefined_fixed=0
 def gradient(self,q):return np.einsum('ktvc,tva->ktca',q[:,self.tri],self.G)
 def project(self,F):
  U,S,Vh=np.linalg.svd(F,full_matrices=False);Z=(U*np.clip(S,*self.spec['local_singular_bounds'])[:,:,None,:])@Vh
  normal=np.cross(Z[:,:,:,0],Z[:,:,:,1]);normal/=np.linalg.norm(normal,axis=2)[:,:,None];dot=np.einsum('kti,ti->kt',normal,self.rest_normal);cosmin=self.spec['local_normal_cone_minimum_rest_dot'];bad=dot<cosmin
  if bad.any():
   n=normal[bad];ref=np.broadcast_to(self.rest_normal,normal.shape)[bad];tan=n-dot[bad,None]*ref;length=np.linalg.norm(tan,axis=1);degenerate=length<1e-12;tan[degenerate]=np.broadcast_to(self.rest_tangent,normal.shape)[bad][degenerate];length[degenerate]=1.;tan/=length[:,None]
   desired=cosmin*ref+np.sqrt(1-cosmin*cosmin)*tan;cross=np.cross(n,desired);c=np.einsum('ij,ij->i',n,desired);K=np.zeros((len(n),3,3));K[:,0,1]=-cross[:,2];K[:,0,2]=cross[:,1];K[:,1,0]=cross[:,2];K[:,1,2]=-cross[:,0];K[:,2,0]=-cross[:,1];K[:,2,1]=cross[:,0];rotation=np.eye(3)[None]+K+np.einsum('tij,tjk->tik',K,K)/(1+c[:,None,None]);assert np.max(np.abs(np.linalg.det(rotation)-1))<1e-10;Z[bad]=rotation@Z[bad]
  return Z
 def smooth_normals(self,points):
  tri=points[self.alltri];cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);out=np.zeros((self.n,3))
  for k in range(3):np.add.at(out,self.alltri[:,k],cross)
  length=np.linalg.norm(out,axis=1);good=length>1e-15;out[good]/=length[good,None]
  return out,good
 def apply(self,out,normals,t):
  assert t is not None
  time=float(t)%self.period;delta=self.spline(time);assert np.max(np.abs(delta[self.fixed]))==0
  old=out[1];new=old+delta[self.reverse];self.maxcorrection=max(self.maxcorrection,float(np.linalg.norm(delta,axis=1).max()));before,bgood=self.smooth_normals(old[self.first]);after,agood=self.smooth_normals(new[self.first]);good=bgood&agood;bad=np.flatnonzero(~good);assert not np.isin(bad,self.free).any(),'Undefined geometric normal on a corrected free class';self.max_undefined_fixed=max(self.max_undefined_fixed,len(bad))
  a=before[good];b=after[good];cross=np.cross(a,b);dot=np.einsum('ij,ij->i',a,b);assert(dot>-1+1e-8).all(),'Antipodal normal correction; no fallback';K=np.zeros((len(a),3,3));K[:,0,1]=-cross[:,2];K[:,0,2]=cross[:,1];K[:,1,0]=cross[:,2];K[:,1,2]=-cross[:,0];K[:,2,0]=-cross[:,1];K[:,2,1]=cross[:,0];rotation=np.repeat(np.eye(3)[None],self.n,axis=0);rotation[good]=np.eye(3)[None]+K+np.einsum('tij,tjk->tik',K,K)/(1+dot[:,None,None]);nn=np.einsum('nij,nj->ni',rotation[self.reverse],normals[1]);nn/=np.linalg.norm(nn,axis=1)[:,None]
  out[1]=new;normals[1]=nn;self.calls+=1;self.frames.append({'time_s':float(t),'positions':new.copy(),'normals':nn.copy()});self.geonormals.append((after.copy(),good.copy()));return out,normals
 def save_diagnostic_frames(self,path):
  arrays={}
  for i,f in enumerate(self.frames):
   for k in ['positions','normals']:arrays[f'{i:03d}_{k}']=f[k]
  arrays['time_s']=np.array([f['time_s']for f in self.frames]);np.savez_compressed(path,**arrays)
 def receipt(self):
  normals=np.array([f['normals']for f in self.frames]);keys=normals[::2];dot=np.sum(keys[1:]*keys[:-1],axis=2);angle=float(np.degrees(np.arccos(np.clip(dot,-1,1))).max());dot=np.sum(normals[1:]*normals[:-1],axis=2);midangle=float(np.degrees(np.arccos(np.clip(dot,-1,1))).max());g=np.array([q[0]for q in self.geonormals])[::2];good=np.array([q[1]for q in self.geonormals])[::2];mask=good[1:]&good[:-1];geodot=np.sum(g[1:]*g[:-1],axis=2);geoangle=float(np.degrees(np.arccos(np.clip(geodot[mask],-1,1))).max())
  return {'kind':'JOINT_PERIODIC_TEMPORAL_CORRECTION_PROTOTYPE','fixed_classes':len(self.fixed),'free_classes':len(self.free),'original_base_geometry_skin_fields_unchanged':True,'solver':self.solver_receipt,'maximum_surface_correction_m':self.maxcorrection,'calls_keys_and_midpoints':self.calls,'maximum_shader_normal_step_at_25ms_keys_deg':angle,'maximum_shader_normal_step_at_12p5ms_midpoint_grid_deg':midangle,'maximum_defined_geometric_normal_key_step_deg':geoangle,'undefined_fixed_geometric_normal_classes_kept_original':self.max_undefined_fixed,'corrective_loop_position_error_m':float(np.abs(self.frames[0]['positions']-self.frames[-1]['positions']).max()),'corrective_loop_normal_error':float(np.abs(self.frames[0]['normals']-self.frames[-1]['normals']).max()),'portable_export_done':False,'natural_gait_approved':False}
