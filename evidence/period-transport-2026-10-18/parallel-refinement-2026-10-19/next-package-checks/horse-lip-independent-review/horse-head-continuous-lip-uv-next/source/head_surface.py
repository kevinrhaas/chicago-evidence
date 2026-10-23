# SPDX-License-Identifier: CC0-1.0
"""Original connected craniofacial skin with actual orbital/nostril/lip recess cuts."""
import math

def require(c,m):
 if not c:raise ValueError(m)
def sub(a,b):return [a[i]-b[i]for i in range(3)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(dot(a,a))
def polygon_inside(y,z,loop,vertices):
 inside=False
 for i,a in enumerate(loop):
  b=loop[(i+1)%len(loop)];ya,za=vertices[a][1:];yb,zb=vertices[b][1:]
  if (ya>y)!=(yb>y)and z<(zb-za)*(y-ya)/(yb-ya)+za:inside=not inside
 return inside

def audit(verts,faces,portal,records,tags):
 require(len(tags)==len(faces),'Face owner count mismatch')
 expected_names={'eye_l','eye_r','nostril_1','nostril_-1','lip_l','lip_r'};require(len(records)==6 and{r['name']for r in records}==expected_names,'Missing/duplicate feature records');require(set(tags)=={'skin'}|expected_names|{'skin:'+n for n in expected_names},'Missing/foreign face owners')
 edges={};areas=[]
 for i,f in enumerate(faces):
  require(len(set(f))==3,'Degenerate IDs');a,b,c=[verts[k]for k in f];area=norm(cross(sub(b,a),sub(c,a)))/2;require(math.isfinite(area)and area>1e-12,'Nonfinite/zero-area face');areas.append(area)
  for a,b in zip(f,f[1:]+f[:1]):edges.setdefault((min(a,b),max(a,b)),[]).append((a,b,i))
 expected={tuple(sorted((portal[i],portal[(i+1)%len(portal)])))for i in range(len(portal))};boundary=set()
 for key,use in edges.items():
  if len(use)==1:boundary.add(key)
  else:require(len(use)==2 and use[0][:2]==use[1][:2][::-1],'Nonmanifold/inconsistent edge')
 require(boundary==expected,'Unexpected hole or missing portal boundary')
 for record in records:
  for role in ['outer','aperture']:
   loop=record[role];require(len(loop)==len(set(loop))and len(loop)>=3,'Invalid feature boundary')
   for i,a in enumerate(loop):
    use=edges[tuple(sorted((a,loop[(i+1)%len(loop)])))];require(len(use)==2,'Missing shared feature edge');actual={tags[x[2]]for x in use};expected={'skin','skin:'+record['name']}if role=='outer'else{'skin:'+record['name'],record['name']};require(actual==expected,'Feature boundary owner mismatch')
 active={i for f in faces for i in f};neighbors={i:set()for i in active}
 for a,b in edges:neighbors[a].add(b);neighbors[b].add(a)
 seen=set();pending=[next(iter(active))]
 while pending:
  i=pending.pop()
  if i in seen:continue
  seen.add(i);pending.extend(neighbors[i]-seen)
 require(seen==active,'Detached closed overlay component')
 require(len(active)-len(edges)+len(faces)==1,'Unexpected head surface genus/closure')
 return {'connected_components':1,'euler_characteristic':1,'triangles':len(faces),'source_vertices':len(verts),'active_vertices':len({i for f in faces for i in f}),'portal_boundary_edges':len(boundary),'minimum_area_m2':min(areas),'features':len(records)}

def build(recipe):
 v=[];f=[];tags=[];rings=[];grid={};records=[];source_uv={}
 def tri(a,b,c,tag):f.append((a,b,c));tags.append(tag)
 for x,y,z,rx,ry,rz in recipe['protected_portal_rings']:
  ring=[]
  for k in range(24):
   t=k*2*math.pi/24;ring.append(len(v));v.append([x+rx*math.cos(t),y+ry*math.sin(t),z+rz*math.sin(t)])
  rings.append(ring)
 stations=recipe['stations']
 for s in stations:
  ring=[];cy=(s['top_y']+s['bottom_y'])/2;r=(s['top_y']-s['bottom_y'])/2
  for k in range(48):
   t=k*2*math.pi/48;sn=math.sin(t);cs=math.cos(t);bulge=s['cheek_lateral_bulge']*max(0,-sn)*abs(cs);source_uv[len(v)]=(s['z'],k);ring.append(len(v));v.append([s['half_width']*cs*(1+bulge),cy+r*sn,s['z']])
  rings.append(ring)
 for row,(a,b)in enumerate(zip(rings,rings[1:])):
  if len(a)==len(b):
   for k in range(len(a)):
    j=(k+1)%len(a);start=len(f);tri(a[k],a[j],b[j],'skin');tri(a[k],b[j],b[k],'skin')
    if len(a)==48:grid[(row-3,k)]=[start,start+1]
  else:
   require((len(a),len(b))==(24,48),'Bad interface')
   for k in range(24):
    j=(k+1)%24;t=2*k;tri(a[k],a[j],b[(t+2)%48],'skin');tri(a[k],b[(t+2)%48],b[(t+1)%48],'skin');tri(a[k],b[(t+1)%48],b[t],'skin')
 center=[sum(v[i][k]for i in rings[-1])/48 for k in range(3)];tip=len(v);v.append(center)
 for k in range(48):tri(tip,rings[-1][k],rings[-1][(k+1)%48],'skin')
 removed=set()
 def sx(y,z):
  points=[{'z':.08,'half_width':.111,'top_y':.144,'bottom_y':-.134,'cheek_lateral_bulge':0}]+stations
  for a,b in zip(points,points[1:]):
   if a['z']-1e-10<=z<=b['z']+1e-10:
    t=(z-a['z'])/(b['z']-a['z']);s={k:a[k]*(1-t)+b[k]*t for k in ['half_width','top_y','bottom_y','cheek_lateral_bulge']};cy=(s['top_y']+s['bottom_y'])/2;r=(s['top_y']-s['bottom_y'])/2;sn=(y-cy)/r;require(abs(sn)<1,'Feature outside head section');cs=math.sqrt(max(0,1-sn*sn));return s['half_width']*cs*(1+s['cheek_lateral_bulge']*max(0,-sn)*cs)
  raise ValueError('Feature outside longitudinal surface')
 def patch(name,side,z0,z1,k0,k1,cy,cz,w,upper,lower,depth,kind):
  selected={i for zi in range(z0,z1)for k in range(k0,k1)for i in grid[(zi,k)]};require(not selected&removed,'Overlapping feature patches');removed.update(selected);uses={}
  for i in selected:
   face=f[i]
   for a,b in zip(face,face[1:]+face[:1]):uses.setdefault(tuple(sorted((a,b))),[]).append((a,b))
  boundary=[e[0]for e in uses.values()if len(e)==1];out={a:b for a,b in boundary};require(len(out)==len(boundary),'Branched patch boundary');start=min(out);loop=[start]
  while out[loop[-1]]!=start:
   loop.append(out[loop[-1]]);require(len(loop)<=len(out),'Open boundary')
  require(len(loop)==len(out),'Multiple patch boundary loops');inner=[]
  for index in loop:
   p=v[index]
   if kind=='lip':
    # Preserve ordered longitudinal/theta correspondence. Polar projection about
    # the slit centre folds the rising anterior jaw boundary back onto itself.
    source_z,k=source_uv[index];u=(source_z-stations[z0]['z'])/(stations[z1]['z']-stations[z0]['z']);q=(k-k0)/(k1-k0)
    if side<0:q=1-q
    radius=upper;zmin=cz-w;zmax=cz+w
    if abs(u)<1e-10 or abs(u-1)<1e-10:
     t=math.pi*(q-.5);y=cy+radius*math.sin(t)
     z=zmin+radius*(1-math.cos(t)) if u<.5 else zmax-radius*(1-math.cos(t))
    else:
     require(abs(q)<1e-10 or abs(q-1)<1e-10,'Lip source not on rectangle boundary')
     y=cy+radius*(2*q-1);z=zmin+radius+(zmax-zmin-2*radius)*u
   else:
    angle=math.atan2((p[1]-cy)/(upper if p[1]>=cy else lower),(p[2]-cz)/w);sn=math.sin(angle);h=upper if sn>=0 else lower;y=cy+h*math.copysign(abs(sn)**1.25,sn);z=cz+w*math.cos(angle)
   require(polygon_inside(y,z,loop,v),'Inner feature outside cut polygon');inner.append([side*(sx(y,z)-(.0015 if kind=='eye'else .001)),y,z])
  previous=loop
  for alpha in [.40,.75,1.0]:
   current=[]
   for old,p in zip(loop,inner):
    y=v[old][1]*(1-alpha)+p[1]*alpha;z=v[old][2]*(1-alpha)+p[2]*alpha;x=side*(sx(y,z)+.0005*math.sin(math.pi*alpha)-(.0015 if kind=='eye'else .001)*alpha**3);current.append(len(v));v.append([x,y,z])
   for i,a in enumerate(previous):j=(i+1)%len(loop);tri(a,previous[j],current[j],'skin:'+name);tri(a,current[j],current[i],'skin:'+name)
   previous=current
  aperture=previous;inside=[]
  for i in aperture:
   y=cy+(v[i][1]-cy)*.5;z=cz+(v[i][2]-cz)*.5
   x=side*(sx(y,z)-.0015+.00075)if kind=='eye'else side*(sx(y,z)-depth*.8)
   inside.append(len(v));v.append([x,y,z])
  for i,a in enumerate(aperture):j=(i+1)%len(loop);tri(a,aperture[j],inside[j],name);tri(a,inside[j],inside[i],name)
  x=side*(sx(cy,cz)-.0015+.001)if kind=='eye'else side*(sx(cy,cz)-depth);center=len(v);v.append([x,cy,cz])
  for i,a in enumerate(inside):tri(center,a,inside[(i+1)%len(inside)],name)
  records.append({'name':name,'outer':loop,'aperture':aperture,'inner':inside,'closure_center':center,'removed_original_faces':sorted(selected),'kind':kind})
 # Actual disjoint rectangular cuts in longitudinal/theta grid; matching loop counts.
 for side in [1,-1]:
  key='l'if side>0 else'r'
  patch('eye_'+key,side,0,3,0 if side>0 else 18,6 if side>0 else 24,.025,.150,.018,.011,.007,.001,'eye')
  patch('nostril_'+str(side),side,7,9,0 if side>0 else 18,6 if side>0 else 24,-.176,.475,.021,.012,.012,.017,'recess')
  patch('lip_'+key,side,6,10,41 if side>0 else 27,45 if side>0 else 31,-.222,.470,.035,.0015,.0015,.006,'lip')
 f=[face for i,face in enumerate(f)if i not in removed];tags=[tag for i,tag in enumerate(tags)if i not in removed];stats=audit(v,f,rings[0],records,tags)
 normals=[[0.,0.,0.]for _ in v]
 for a,b,c in f:
  n=cross(sub(v[b],v[a]),sub(v[c],v[a]))
  for i in[a,b,c]:normals[i]=[normals[i][k]+n[k]for k in range(3)]
 normals=[[x/(norm(n)or 1)for x in n]for n in normals]
 return {'positions':v,'faces':f,'tags':tags,'normals':normals,'portal':rings[0],'band':rings[1],'records':records,'topology':stats,'status':'original closed recessed features; only rear neckportal open; anatomy/fit/visual acceptance pending'}
