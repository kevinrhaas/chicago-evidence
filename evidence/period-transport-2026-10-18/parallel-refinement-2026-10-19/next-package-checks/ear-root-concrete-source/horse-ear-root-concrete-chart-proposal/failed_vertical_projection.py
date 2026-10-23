# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only vertical projection of actual retained ear cross sections to skull."""
from pathlib import Path
import json,math,hashlib
import numpy as np
P=Path(__file__).parent;B=Path('/workspace/shared/horse-head-groove-coat-next');s=json.loads((B/'trial1/head-source-surface.json').read_text());prior=json.loads(Path('/workspace/shared/horse-ear-root-shared-proposal/SOURCE-MAP.json').read_text());v=np.asarray(s['positions'],float);faces=np.asarray(s['faces']);candidate=list(range(24))+list(range(48,72));chart=v[faces[candidate]][:,:,[0,2]]
def cross(a,b):return float(a[0]*b[1]-a[1]*b[0])
def bary(q,t):
 a,b,c=t;D=cross(b-a,c-a)
 if abs(D)<1e-15:return None
 u=cross(q-a,c-a)/D;w=cross(b-a,q-a)/D;return np.array([1-u-w,u,w])
def hit(q):
 found=[]
 for fi,t in zip(candidate,chart):
  bc=bary(q,t)
  if bc is not None and min(bc)>=-1e-10:found.append((float(bc@v[faces[fi],1]),fi,bc))
 if not found:raise ValueError('Projection outside bounded original upper skull chart')
 y,fi,bc=max(found,key=lambda a:(a[0],-a[1]));return {'source_face':fi,'source_vertices':faces[fi].tolist(),'barycentric':bc.tolist(),'position_local_m':[float(q[0]),y,float(q[1])]}
def seg_distance(p,a,b):
 d=b-a;t=max(0,min(1,float((p-a)@d/(d@d))));return float(np.linalg.norm(p-(a+t*d)))
portal=v[np.asarray(s['portal'])];protected=v[:48];edges={(min(a,b),max(a,b))for fi in candidate for a,b in zip(faces[fi],np.roll(faces[fi],-1))};rows=[]
for ear in prior['ear_root_cohorts']:
 loop=np.asarray([r['position_local_m']for r in ear['ordered_root_boundary']],float);xz=loop[:,[0,2]];points=[{**hit(q),'ear_boundary_corner':i,'leaf_point_local_m':loop[i].tolist(),'vertical_gap_m':float(loop[i,1]-hit(q)['position_local_m'][1])}for i,q in enumerate(xz)];crossings=[];splits=[];conforming=[]
 for i,a in enumerate(xz):
  b=xz[(i+1)%18];found=[]
  for e0,e1 in edges:
   c,d=v[e0,[0,2]],v[e1,[0,2]];den=cross(b-a,d-c)
   if abs(den)<1e-15:continue
   t=cross(c-a,d-c)/den;u=cross(c-a,b-a)/den
   if 1e-9<t<1-1e-9 and -1e-10<=u<=1+1e-10:
    if any(abs(t-r['ear_edge_fraction'])<1e-8 for r in found):continue
    h=hit(a+t*(b-a));found.append({**h,'ear_edge':i,'ear_edge_fraction':t,'crossed_source_edge':[int(e0),int(e1)]})
  found.sort(key=lambda a:a['ear_edge_fraction']);conforming.append(points[i]);conforming.extend(found);crossings.extend(found)
 # Actual exact source-owner sequence along each projected cut segment.
 segments=[]
 for i,a in enumerate(xz):
  ts=[0]+[r['ear_edge_fraction']for r in crossings if r['ear_edge']==i]+[1];ts=sorted(ts)
  for lo,hi in zip(ts,ts[1:]):segments.append({'ear_edge':i,'s0':lo,'s1':hi,'source_face':hit(a+(lo+hi)/2*(xz[(i+1)%18]-a))['source_face']})
 # Proper polygon-edge intersections, including nonadjacent non-neighbour edges.
 selfhits=[]
 for i,a in enumerate(xz):
  b=xz[(i+1)%18]
  for j in range(i+1,18):
   if j==(i+1)%18 or i==(j+1)%18:continue
   c,d=xz[j],xz[(j+1)%18];den=cross(b-a,d-c)
   if abs(den)<1e-15:continue
   t=cross(c-a,d-c)/den;u=cross(c-a,b-a)/den
   if 1e-10<t<1-1e-10 and 1e-10<u<1-1e-10:selfhits.append([i,j])
 minportal=min(seg_distance(np.asarray(q['position_local_m']),portal[j],portal[(j+1)%24])for q in conforming for j in range(24));minprotected=min(float(np.linalg.norm(np.asarray(q['position_local_m'])-z))for q in conforming for z in protected)
 rows.append({'side':ear['side'],'original_18_projected_points':points,'extra_source_edge_crossings':crossings,'conforming_piecewise_planar_cut_point_count':len(conforming),'conforming_loop':conforming,'source_segment_ownership':segments,'boundary_split_source_faces':sorted({r['source_face']for r in segments}),'projected_boundary_strict_self_crossings':selfhits,'minimum_projected_leaf_to_skull_Y_gap_m':min(r['vertical_gap_m']for r in points),'minimum_vertex_sample_to_neckportal_edge_m':minportal,'minimum_vertex_sample_to_protected48vertices_m':minprotected,'clearance_scope':'Boundary vertices to portal segments/protected vertices only; exact segment-segment minimum still required','correspondence':'s=i+t on actual oriented18edge leaf boundary; projected skull cuts share identical XZ at s. Extra skull knots derive ONLY original source-edge intersections; upper leaf root ring remains18edges.'})
r={'status':'SOURCE ONLY; no horse geometry emitted or changed','input090_sha256':hashlib.sha256((B/'trial1/equine_light_harness_skinned_prototype_01.glb').read_bytes()).hexdigest(),'rows':rows};(P/'CONCRETE-CHART.json').write_text(json.dumps(r,indent=2)+'\n');print([(r['side'],r['conforming_piecewise_planar_cut_point_count'],r['boundary_split_source_faces'],r['minimum_projected_leaf_to_skull_Y_gap_m'],r['minimum_vertex_sample_to_neckportal_edge_m'],r['minimum_vertex_sample_to_protected48vertices_m'])for r in rows])
