import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,importlib.util,numpy as np,math
from pathlib import Path
from scipy.optimize import minimize
sys.dont_write_bytecode=True;R=Path(__file__).parent
spec=importlib.util.spec_from_file_location('source_math',R.parent/'BARE-CURRENT26-WALK-SPECIMEN-04-LOCAL-BODY-WEIGHTS/produce_current26_walk.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
spec=importlib.util.spec_from_file_location('hinges',R.parent/'BARE-CURRENT26-WALK-SPECIMEN-05-X-HINGES/hinge_solver.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
p.TRAVEL=.135;p.ROOT_Y=-(.0052360789850354195+.005237669218331575)/2;p.LIFT=.01;FORE_BIAS=p.TRAVEL*p.DUTY/2
class PoseSolver:
 def __init__(self):
  self.raw=p.SOURCE.read_bytes();assert p.sha(self.raw)==p.EXPECTED;self.d,self.b=p.read(self.raw);p.PARENT={i:None for i in range(26)}
  for i,n in enumerate(self.d['nodes'][:26]):
   for child in n.get('children',[]):
    if child<26:p.PARENT[child]=i
  self.rest=p.fk(self.d,{},np.zeros(3))[:,:3,3];self.ibm=p.accessor(self.d,self.b,self.d['skins'][0]['inverseBindMatrices']).reshape(26,4,4).transpose(0,2,1).astype(float);pr=self.d['meshes'][1]['primitives'][0];self.P=p.accessor(self.d,self.b,pr['attributes']['POSITION']).astype(float);J=p.accessor(self.d,self.b,pr['attributes']['JOINTS_0']).astype(int);W=p.accessor(self.d,self.b,pr['attributes']['WEIGHTS_0']).astype(float);W=(W/abs(W).sum(1)[:,None]).astype(np.float32).astype(float);allTri=p.accessor(self.d,self.b,pr['indices']).reshape(-1,3);self.data={}
  for label,(chain,offset)in p.CHAINS.items():
   weights=np.stack([np.where(J==joint,W,0).sum(1)for joint in chain],1);ids=np.flatnonzero(weights.sum(1)>0);faces=allTri[np.isin(allTri,ids).any(1)];v=self.P[faces];N=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);A=np.linalg.norm(N,axis=1);edges=np.unique(np.sort(np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[0,2]]]),axis=1),axis=0);L=np.linalg.norm(self.P[edges[:,1]]-self.P[edges[:,0]],axis=1);edges=edges[L>1e-8];L=L[L>1e-8];sole=float(self.P[weights[:,-1]==1,1].min());self.data[label]=(weights,faces,N,A,edges,L,sole)
 def target(self,label,time):
  chain,offset=p.CHAINS[label];sole=self.data[label][-1];target,phase,stance=p.goal(self.rest[chain[-1]],time,offset,sole)
  if label.startswith('fore'):
   target[2]+=FORE_BIAS
   if not stance:
    u=(phase-p.DUTY)/(1-p.DUTY);lift=(u*u*(1-u)**3)/(.4**2*.6**3);target[1]=self.rest[chain[-1],1]-sole-p.ROOT_Y+p.LIFT*lift
  return target,phase,stance
 def evaluate(self,label,alpha):
  chain,_=p.CHAINS[label];weights,faces,N,A,edges,L,sole=self.data[label];q={chain[i]:np.array([math.sin(alpha[i]/2),0,0,math.cos(alpha[i]/2)])for i in range(4)};q[chain[-1]]=np.array([math.sin(-alpha.sum()/2),0,0,math.cos(-alpha.sum()/2)]);world=p.fk(self.d,q,np.zeros(3));out=self.P.copy()
  for i,joint in enumerate(chain):
   M=world[joint]@self.ibm[joint];out+=(self.P@M[:3,:3].T+M[:3,3]-self.P)*weights[:,i,None]
  ratios=np.linalg.norm(out[edges[:,1]]-out[edges[:,0]],axis=1)/L;v=out[faces];normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);areas=np.linalg.norm(normal,axis=1)[A>1e-12]/A[A>1e-12];return world[chain[-1],:3,3],ratios,areas,int((np.einsum('ij,ij->i',normal,N)<0).sum())
 def solve(self,label,time,seed=None):
  chain,_=p.CHAINS[label];target,phase,stance=self.target(label,time)
  if seed is None:
   init,_=h.solve(self.rest[chain],target);seed=np.array([2*math.atan2(init[i][0],init[i][3])for i in range(4)])
  def eq(x):tip,*_=self.evaluate(label,x[:4]);return(tip-target)[[1,2]]
  def bounds(x):_,r,a,_=self.evaluate(label,x[:4]);return np.r_[x[4]-(r-1),x[4]+(r-1),x[4]-.5*(a-1),x[4]+.5*(a-1)]
  result=minimize(lambda x:x[4]+1e-5*np.dot(x[:4],x[:4]),np.r_[seed,.3],method='SLSQP',bounds=[(-.9,.9)]*4+[(0,1)],constraints=[{'type':'eq','fun':eq},{'type':'ineq','fun':bounds}],options={'maxiter':45,'ftol':1e-10});alpha=result.x[:4];tip,r,a,n=self.evaluate(label,alpha);return alpha,{'limb':label,'time':float(time),'phase':float(phase),'stance':bool(stance),'angles':alpha.tolist(),'angleDegrees':(alpha*180/np.pi).tolist(),'strain':float(result.x[4]),'edgeMin':float(r.min()),'edgeMax':float(r.max()),'areaMin':float(a.min()),'areaMax':float(a.max()),'normalNegative':n,'tipResidual':float(np.linalg.norm(tip-target)),'success':bool(result.success),'message':str(result.message),'iterations':result.nit}
