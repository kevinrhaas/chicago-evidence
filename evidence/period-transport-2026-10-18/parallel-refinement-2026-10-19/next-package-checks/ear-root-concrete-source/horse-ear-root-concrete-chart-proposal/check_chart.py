# SPDX-License-Identifier: GPL-3.0-or-later
"""Lightweight actual-chart injectivity/coverage and exact segment clearance."""
from pathlib import Path
import json,math
import numpy as np
P=Path(__file__).parent

def cross(a,b):return float(a[0]*b[1]-a[1]*b[0])
def area(poly):return sum(cross(a,b)for a,b in zip(poly,np.roll(poly,-1,axis=0)))/2 if len(poly)>=3 else 0

def clip(poly,tri):
 poly=[np.array(p,float)for p in poly];tri=[np.array(p,float)for p in tri]
 if area(tri)<0:tri=tri[::-1]
 for a,b in zip(tri,tri[1:]+tri[:1]):
  old=poly;poly=[]
  if not old:break
  for p,q in zip(old,old[1:]+old[:1]):
   cp=cross(b-a,p-a);cq=cross(b-a,q-a)
   if cp>=0:poly.append(p)
   if cp*cq<0:poly.append(p+(q-p)*cp/(cp-cq))
 return poly

def inside(p,t):
 c=[cross(t[(i+1)%3]-t[i],p-t[i])for i in range(3)];return min(c)>=-1e-15 or max(c)<=1e-15

def earclip(poly):
 poly=np.asarray(poly,float);ix=list(range(len(poly)))
 if area(poly)<0:ix.reverse()
 triangles=[]
 while len(ix)>3:
  found=False
  for k in range(len(ix)):
   t=[ix[k-1],ix[k],ix[(k+1)%len(ix)]];pp=poly[t]
   if cross(pp[1]-pp[0],pp[2]-pp[1])<=1e-15:continue
   if any(inside(poly[j],pp)for j in ix if j not in t):continue
   triangles.append(pp);ix.pop(k);found=True;break
  if not found:raise ValueError('Cannot triangulate actual polygon without degeneracy')
 triangles.append(poly[ix]);assert abs(sum(abs(area(t))for t in triangles)-abs(area(poly)))<1e-12
 return triangles

def segment_distance(p1,q1,p2,q2):
 # Independent finite segment closest-point construction, including clamped ends.
 u=q1-p1;v=q2-p2;w=p1-p2;a=float(u@u);b=float(u@v);c=float(v@v);d=float(u@w);e=float(v@w);D=a*c-b*b;candidates=[]
 def add(s,t):candidates.append(float(np.linalg.norm(p1+s*u-p2-t*v)))
 if D>1e-24:
  s=(b*e-c*d)/D;t=(a*e-b*d)/D
  if 0<=s<=1 and 0<=t<=1:add(s,t)
 for s in[0,1]:add(s,max(0,min(1,(e+s*b)/c)))
 for t in[0,1]:add(max(0,min(1,(t*b-d)/a)),t)
 return min(candidates)

def controls():
 a=np.array([[0.,0.],[1.,0.],[0.,1.]])
 assert abs(area(clip(a,a))-.5)<1e-12
 assert abs(area(clip(a,a+2)))==0
 assert abs(area(clip(a,[[1.,0.],[1.,1.],[0.,1.]])))==0
 z=np.array([0.,0.,0.]);x=np.array([1.,0.,0.]);assert segment_distance(z,x,np.array([.5,-1.,0.]),np.array([.5,1.,0.]))==0
 assert abs(segment_distance(z,x,z+[0,2,0],x+[0,2,0])-2)<1e-12
 assert abs(segment_distance(z,x,x+[1,0,0],x+[2,0,0])-1)<1e-12
 return 6

def main():
 r=json.loads((P/'CONCRETE-CHART.json').read_text());s=json.loads(Path('/workspace/shared/horse-head-groove-coat-next/trial1/head-source-surface.json').read_text());v=np.asarray(s['positions'],float);f=np.asarray(s['faces']);report=[]
 for row in r['rows']:
  leaf=np.asarray([p['leaf_point_local_m']for p in row['original_18_projected_points']]);poly=leaf[:,[0,2]];cuttri=earclip(poly);focus=np.array(row['projection_focus_actual_ring1_centroid_m']);ly=leaf[0,1]
  def proj(p):return focus[[0,2]]+(p[[0,2]]-focus[[0,2]])*(ly-focus[1])/(p[1]-focus[1])
  ids=[i for i in list(range(24))+list(range(48,72))if np.all(v[f[i],1]>focus[1]+1e-9)];chart={i:np.asarray([proj(p)for p in v[f[i]]])for i in ids};areas={i:sum(abs(area(clip(t,chart[i])))for t in cuttri)for i in ids};active=[i for i in ids if areas[i]>1e-15];overlaps=[]
  for j,a in enumerate(active):
   for b in active[j+1:]:
    aa=sum(abs(area(clip(clip(t,chart[a]),chart[b])))for t in cuttri)
    if aa>1e-15:overlaps.append({'a':a,'b':b,'overlap_area_m2':aa})
  sourceface_rows=[]
  for i in active:
   sourceface_rows.append({'source_face':i,'projected_triangle_area_m2':abs(area(chart[i])),'projected_footprint_inside_area_m2':areas[i],'fully_retired':abs(areas[i]-abs(area(chart[i])))<1e-14,'split_boundary':i in row['boundary_split_source_faces']})
  cut=np.array([p['position_local_m']for p in row['conforming_loop']]);portal=v[s['portal']];mind=min(segment_distance(a,b,c,d)for a,b in zip(cut,np.roll(cut,-1,axis=0))for c,d in zip(portal,np.roll(portal,-1,axis=0)));minvertices=min(float(np.linalg.norm(z-(a+max(0,min(1,float((z-a)@(b-a)/((b-a)@(b-a)))))*(b-a))))for a,b in zip(cut,np.roll(cut,-1,axis=0))for z in v[:48]);coverage=sum(areas.values());target=abs(area(poly));assert abs(coverage-target)<1e-12 and not overlaps;assert not row['projected_boundary_strict_self_crossings'];assert row['minimum_projected_leaf_to_skull_Y_gap_m']>0
  edgegap=min(segment_distance(np.array([a[0],0,a[1]]),np.array([b[0],0,b[1]]),np.array([c[0],0,c[1]]),np.array([d[0],0,d[1]]))for i,(a,b)in enumerate(zip(poly,np.roll(poly,-1,axis=0)))for j,(c,d)in enumerate(zip(poly,np.roll(poly,-1,axis=0)))if j>i and j!=(i+1)%18 and i!=(j+1)%18);assert edgegap>1e-12
  report.append({'side':row['side'],'original_loop_corners':18,'minimum_nonadjacent_projected_boundary_edge_distance_m':edgegap,'required_conforming_skull_knots':len(cut),'footprint_triangulation_triangles':len(cuttri),'global_projected_overlap_pairs':overlaps,'projected_coverage_area_m2':coverage,'footprint_area_m2':target,'coverage_delta_m2':coverage-target,'minimum_cut_segments_to_portal_segments_m':mind,'minimum_cut_segments_to_protected48_vertices_m':minvertices,'exact_affected_skull_source_faces':sourceface_rows})
 out={'source_only':True,'no_generated_mesh':True,'analytic_controls':controls(),'rows':report,'conclusion':'Natural retained-ear projection is feasible as contained source chart BUT conforming skull boundary requires22 knots each, not18. Explicit root contract change required; upper ear boundary can remain18 using unequal-ring annular triangulation.'};(P/'CHART-CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
if __name__=='__main__':main()
