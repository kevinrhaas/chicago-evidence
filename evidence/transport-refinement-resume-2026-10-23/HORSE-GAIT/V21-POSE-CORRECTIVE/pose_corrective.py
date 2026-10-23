"""Explicit posed flesh correction prototype. No base geometry or weight edits.

Uniform relative-edge ARAP energy; exact original protected and shared-seam rows
follow the unmodified LBS result. A 1% local stiffness positional tether bounds
free-surface drift from that posed reference. Parameters are frozen before test,
not acceptance thresholds. No joint/hoof target or physical tolerance changes.
"""
import json
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import splu

class Corrector:
 def __init__(self,parts,rest,piv,ib,here):
  pin=json.loads((here/'INPUT-PINS.json').read_text())['phase_a_arrays']['path']
  with np.load(pin,allow_pickle=False)as a:
   cls=a['vertex_classes_1'];protected=a['source_protected_class_ids'];other=np.unique(np.r_[a['vertex_classes_0'],a['vertex_classes_2']])
  self.ids,self.first,self.reverse=np.unique(cls,return_index=True,return_inverse=True)
  self.p=rest[1][self.first].copy();self.normal=parts[1][1].copy();self.restnormal=rest[1]*0 # unneeded old mesh-space normal is not canonical
  fixed=np.isin(self.ids,protected)|np.isin(self.ids,other)
  self.fixed=np.flatnonzero(fixed);self.free=np.flatnonzero(~fixed)
  assert len(self.fixed)>0 and len(self.free)>0
  tri=self.reverse[parts[1][4]]
  pairs=np.sort(np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]]),axis=1)
  pairs=np.unique(pairs,axis=0);pairs=pairs[pairs[:,0]!=pairs[:,1]]
  self.i,self.j=pairs.T;self.edge=self.p[self.i]-self.p[self.j];l2=np.einsum('ij,ij->i',self.edge,self.edge)
  assert (l2>1e-16).all();self.w=1/l2
  n=len(self.p);self.n=n
  diagonal=np.bincount(np.r_[self.i,self.j],weights=np.r_[self.w,self.w],minlength=n)
  self.tether=.01*diagonal
  L=coo_matrix((np.r_[diagonal,-self.w,-self.w],(np.r_[np.arange(n),self.i,self.j],np.r_[np.arange(n),self.j,self.i])),shape=(n,n)).tocsc()
  K=L+diags(self.tether,format='csc')
  self.cross=K[self.free][:,self.fixed];self.factor=splu(K[self.free][:,self.free],permc_spec='MMD_AT_PLUS_A')
  self.calls=0;self.maxcorrection=0.;self.iterations=25;self.maxstep=0.;self.frames=[]
 def apply(self,out,normals):
  target=out[1][self.first].copy();q=target.copy();R=np.repeat(np.eye(3)[None],self.n,axis=0)
  fixedterm=self.cross@target[self.fixed]
  for iteration in range(self.iterations):
   de=q[self.i]-q[self.j]
   cov=np.zeros((self.n,3,3));outer=self.w[:,None,None]*np.einsum('ni,nj->nij',de,self.edge)
   np.add.at(cov,self.i,outer);np.add.at(cov,self.j,outer)
   U,_,Vh=np.linalg.svd(cov);R=U@Vh;bad=np.linalg.det(R)<0
   if bad.any():U[bad,:,-1]*=-1;R[bad]=U[bad]@Vh[bad]
   edge_rhs=self.w[:,None]*np.einsum('nij,nj->ni',.5*(R[self.i]+R[self.j]),self.edge)
   rhs=np.zeros((self.n,3));np.add.at(rhs,self.i,edge_rhs);np.add.at(rhs,self.j,-edge_rhs)
   rhs+=self.tether[:,None]*target
   nxt=q.copy();nxt[self.free]=self.factor.solve(rhs[self.free]-fixedterm)
   step=float(np.max(np.linalg.norm(nxt-q,axis=1)));q=nxt
  assert np.array_equal(q[self.fixed],target[self.fixed]) and np.isfinite(q).all()
  self.maxstep=max(self.maxstep,step);corr=q-target;self.maxcorrection=max(self.maxcorrection,float(np.linalg.norm(corr,axis=1).max()))
  # Rotate the original canonical rest normals using the local best-fit ARAP
  # rotation. Normals are defined per render vertex, preserving split charts.
  # The physical checker separately computes geometric triangle normals.
  old=out[1];out[1]=q[self.reverse]
  # Tethered original LBS normal is rotated by the small corrective best-fit
  # surface rotation from old LBS edges to corrected edges.
  old_edges=old[self.first][self.i]-old[self.first][self.j];new_edges=q[self.i]-q[self.j]
  C=np.zeros((self.n,3,3));outer=self.w[:,None,None]*np.einsum('ni,nj->nij',new_edges,old_edges)
  np.add.at(C,self.i,outer);np.add.at(C,self.j,outer);U,_,Vh=np.linalg.svd(C);corR=U@Vh;bad=np.linalg.det(corR)<0
  if bad.any():U[bad,:,-1]*=-1;corR[bad]=U[bad]@Vh[bad]
  normals[1]=np.einsum('nij,nj->ni',corR[self.reverse],normals[1]);normals[1]/=np.linalg.norm(normals[1],axis=1)[:,None]
  self.calls+=1;self.frames.append({'positions':out[1].copy(),'normals':normals[1].copy()})
  return out,normals
 def receipt(self):
  return {'kind':'EXPLICIT_POSE_CORRECTIVE_ARAP_PROTOTYPE','base_geometry_weights_unchanged':True,'fixed_classes':len(self.fixed),'free_classes':len(self.free),'unique_mesh_classes':self.n,'edges':len(self.i),'relative_edge_stiffness':'1/rest_length_squared','fidelity_fraction_of_vertex_stiffness':.01,'iterations_per_pose':self.iterations,'calls':self.calls,'maximum_surface_correction_m':self.maxcorrection,'last_iteration_maximum_step_m':self.maxstep,'portable_export_done':False,'GLB_or_browser_acceptance':False}
