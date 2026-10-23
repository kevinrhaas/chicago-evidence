"""One bounded triangle deformation-gradient ADMM constraint study.

Local singular values jointly bounded to .95–1.05 (a stricter modeling envelope
than the unchanged original edge .9–1.1 / area .8–1.2 verification). Global
quadratic reconstruction keeps source-known, hoof, tail and shared-boundary
classes exactly on original LBS. Not a natural-gait or portable-asset acceptance.
"""
import json
import hashlib
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import splu

class Corrector:
 def __init__(self,parts,rest,piv,ib,here):
  pin=json.loads((here/'INPUT-PINS.json').read_text())['phase_a_arrays']['path']
  with np.load(pin,allow_pickle=False)as a:
   cls=a['vertex_classes_1'];protected=a['source_protected_class_ids'];other=np.unique(np.r_[a['vertex_classes_0'],a['vertex_classes_2']])
  self.ids,self.first,self.reverse=np.unique(cls,return_index=True,return_inverse=True)
  self.p=rest[1][self.first].copy();self.n=len(self.p)
  fixed=np.isin(self.ids,protected)|np.isin(self.ids,other)
  self.fixed=np.flatnonzero(fixed);self.free=np.flatnonzero(~fixed)
  assert len(self.fixed)>0 and len(self.free)>0
  tri=self.reverse[parts[1][4]];xyz=self.p[tri];e01=xyz[:,1]-xyz[:,0];e02=xyz[:,2]-xyz[:,0]
  nrm=np.cross(e01,e02);area2=np.linalg.norm(nrm,axis=1)
  valid=area2>1e-12;self.tri=tri[valid];e01=e01[valid];e02=e02[valid];area2=area2[valid]
  e1=e01/np.linalg.norm(e01,axis=1)[:,None];normal=np.cross(e01,e02)/area2[:,None];e2=np.cross(normal,e1)
  Dm=np.zeros((len(e01),2,2));Dm[:,0,0]=np.linalg.norm(e01,axis=1);Dm[:,0,1]=np.einsum('ij,ij->i',e02,e1);Dm[:,1,1]=np.einsum('ij,ij->i',e02,e2)
  self.G=np.einsum('va,tab->tvb',np.array([[-1.,-1.],[1.,0.],[0.,1.]]),np.linalg.inv(Dm))
  self.area=area2*.5
  blocks=self.area[:,None,None]*np.einsum('tva,twa->tvw',self.G,self.G)
  ii=np.repeat(self.tri,3,axis=1).reshape(-1);jj=np.tile(self.tri,(1,3)).reshape(-1)
  L=coo_matrix((blocks.reshape(-1),(ii,jj)),shape=(self.n,self.n)).tocsc()
  diagonal=L.diagonal();assert (diagonal>0).all()
  self.tether=.01*diagonal;K=L+diags(self.tether,format='csc')
  self.cross=K[self.free][:,self.fixed];self.factor=splu(K[self.free][:,self.free],permc_spec='MMD_AT_PLUS_A')
  pairs=np.unique(np.sort(np.concatenate([self.tri[:,[0,1]],self.tri[:,[1,2]],self.tri[:,[2,0]]]),axis=1),axis=0);pairs=pairs[pairs[:,0]!=pairs[:,1]]
  self.i,self.j=pairs.T;edge=self.p[self.i]-self.p[self.j];self.w=1/np.einsum('ij,ij->i',edge,edge)
  self.calls=0;self.maxcorrection=0.;self.iterations=100;self.maxstep=0.;self.frames=[];self.minimum_F_singular=1.;self.maximum_F_singular=1.;self.max_primal_residual=0.;self.max_dual_step=0.
 def apply(self,out,normals):
  target=out[1][self.first].copy();q=target.copy();fixedterm=self.cross@target[self.fixed]
  # Augmented-Lagrangian variable split F(q)=Z. The dual term prevents the
  # fidelity tether silently trading away the proposed triangle strain bound.
  dual=np.zeros((len(self.tri),3,2))
  def project(F):
   U,S,Vh=np.linalg.svd(F,full_matrices=False)
   return (U*np.clip(S,.95,1.05)[:,None,:])@Vh
  F=np.einsum('tvc,tva->tca',q[self.tri],self.G);Z=project(F)
  for iteration in range(self.iterations):
   vertex_rhs=self.area[:,None,None]*np.einsum('tva,tca->tvc',self.G,Z-dual)
   rhs=np.zeros((self.n,3));np.add.at(rhs,self.tri.reshape(-1),vertex_rhs.reshape(-1,3));rhs+=self.tether[:,None]*target
   nxt=q.copy();nxt[self.free]=self.factor.solve(rhs[self.free]-fixedterm)
   step=float(np.max(np.linalg.norm(nxt-q,axis=1)));q=nxt
   F=np.einsum('tvc,tva->tca',q[self.tri],self.G);oldZ=Z;Z=project(F+dual);dual+=F-Z
   primal=float(np.max(np.linalg.norm(F-Z,axis=(1,2))));dualstep=float(np.max(np.linalg.norm(Z-oldZ,axis=(1,2))))
  self.max_primal_residual=max(self.max_primal_residual,primal);self.max_dual_step=max(self.max_dual_step,dualstep)
  assert np.array_equal(q[self.fixed],target[self.fixed]) and np.isfinite(q).all()
  # Meaningful fixed-anchor corruption control, same exact validator.
  if self.calls==0:
   bad=q.copy();bad[self.fixed[0],0]+=.001;rejected=not np.array_equal(bad[self.fixed],target[self.fixed]);assert rejected
  F=np.einsum('tvc,tva->tca',q[self.tri],self.G);S=np.linalg.svd(F,compute_uv=False)
  self.minimum_F_singular=min(self.minimum_F_singular,float(S.min()));self.maximum_F_singular=max(self.maximum_F_singular,float(S.max()))
  self.maxstep=max(self.maxstep,step);corr=q-target;self.maxcorrection=max(self.maxcorrection,float(np.linalg.norm(corr,axis=1).max()))
  old=out[1];out[1]=q[self.reverse]
  old_edges=old[self.first][self.i]-old[self.first][self.j];new_edges=q[self.i]-q[self.j]
  C=np.zeros((self.n,3,3));outer=self.w[:,None,None]*np.einsum('ni,nj->nij',new_edges,old_edges)
  np.add.at(C,self.i,outer);np.add.at(C,self.j,outer);U,_,Vh=np.linalg.svd(C);corR=U@Vh;bad=np.linalg.det(corR)<0
  if bad.any():U[bad,:,-1]*=-1;corR[bad]=U[bad]@Vh[bad]
  normals[1]=np.einsum('nij,nj->ni',corR[self.reverse],normals[1]);normals[1]/=np.linalg.norm(normals[1],axis=1)[:,None]
  self.calls+=1;self.frames.append({'positions':out[1].copy(),'normals':normals[1].copy()})
  return out,normals
 def save_diagnostic_frames(self,path):
  arrays={}
  for i,f in enumerate(self.frames):
   for k,v in f.items():arrays[f'{i:02d}_{k}']=v
  np.savez_compressed(path,**arrays)
 def receipt(self):
  return {'kind':'EXPLICIT_TRIANGLE_ADMM_CORRECTIVE_PROTOTYPE','base_geometry_weights_unchanged':True,'fixed_classes':len(self.fixed),'free_classes':len(self.free),'unique_mesh_classes':self.n,'triangles_in_solver':len(self.tri),'projection_singular_value_bounds':[.95,1.05],'actual_reconstructed_singular_extrema':[self.minimum_F_singular,self.maximum_F_singular],'fidelity_fraction_of_vertex_stiffness':.01,'iterations_per_pose':self.iterations,'maximum_primal_constraint_residual':self.max_primal_residual,'maximum_last_dual_projection_step':self.max_dual_step,'calls':self.calls,'maximum_surface_correction_m':self.maxcorrection,'last_iteration_maximum_step_m':self.maxstep,'corrective_loop_position_error_m':float(np.max(np.abs(self.frames[0]['positions']-self.frames[-1]['positions'])))if self.calls==65 else None,'corrective_loop_normal_error':float(np.max(np.abs(self.frames[0]['normals']-self.frames[-1]['normals'])))if self.calls==65 else None,'portable_export_done':False,'GLB_or_browser_acceptance':False}
