# SPDX-License-Identifier: GPL-3.0-or-later
"""Original convex clipping diagnostic for actual closed lip chart projection."""
import json,math
from pathlib import Path
P=Path(__file__).resolve().parent.parent

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def signed_area(poly):return sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(poly,poly[1:]+poly[:1]))/2

def overlap_area(a,b):
 if signed_area(b)<0:b=b[::-1]
 poly=[list(p)for p in a]
 for c,d in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for p,q in zip(old,old[1:]+old[:1]):
   cp=cross(c,d,p);cq=cross(c,d,q)
   if cp>=0:poly.append(p)
   if (cp<0 and cq>0)or(cp>0 and cq<0):
    t=cp/(cp-cq);poly.append([p[k]+t*(q[k]-p[k])for k in range(2)])
 return abs(signed_area(poly))if len(poly)>=3 else 0

def controls():
 a=[[0.,0.],[1.,0.],[0.,1.]]
 assert abs(overlap_area(a,a)-.5)<1e-12
 assert overlap_area(a,[[1.,0.],[1.,1.],[0.,1.]])==0
 assert overlap_area(a,[[2.,0.],[3.,0.],[2.,1.]])==0
 assert overlap_area(a,[[.1,.1],[.8,.1],[.1,.8]])>.2
 assert abs(overlap_area(a,a[::-1])-.5)<1e-12
 return 5

def main():
 s=json.loads((P/'trial1/head-source-surface.json').read_text());rows=[]
 for r in s['records']:
  if r['kind']!='continuous_closed_lip_groove':continue
  faces=r['source_faces'];pos=s['positions'];tri=[[[pos[i][1],pos[i][2]]for i in f]for f in faces];areas=[signed_area(t)for t in tri];pairs=[];maximum=0
  for i,a in enumerate(tri):
   for j in range(i+1,len(tri)):
    area=overlap_area(a,tri[j]);maximum=max(maximum,area)
    if area>1e-15:pairs.append({'a':i,'b':j,'intersection_area_m2':area,'shared_source_vertices':len(set(faces[i])&set(faces[j]))})
  chart_exact=all(pos[i][1:]==old[1:]for i,old in zip(r['chart_vertices'],r['source_positions']))
  rows.append({'name':r['name'],'triangles':len(tri),'all_unordered_pairs_checked':len(tri)*(len(tri)-1)//2,'nonzero_projected_area':all(abs(a)>1e-12 for a in areas),'consistent_orientation':all(a*areas[0]>0 for a in areas),'YZ_source_exact':chart_exact,'positive_area_overlap_pairs':pairs,'maximum_overlap_area_m2':maximum})
 report={'pass':all(not r['positive_area_overlap_pairs']and r['YZ_source_exact']and r['nonzero_projected_area']and r['consistent_orientation']for r in rows),'analytic_controls':controls(),'area_detection_threshold_m2':1e-15,'rows':rows,'scope':'Actual ordered lips globally nonoverlapping projected interiors, including adjacent pairs; shared chart boundaries permitted. Finite numerical diagnostic, not photographic/anatomical acceptance.'};(P/'qualification/projected-chart.json').write_text(json.dumps(report,indent=2)+'\n');print(report);assert report['pass']
if __name__=='__main__':main()
