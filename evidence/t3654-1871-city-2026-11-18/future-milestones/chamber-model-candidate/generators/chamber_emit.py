#!/usr/bin/env python3
"""Deterministic exterior candidate from a standalone, engine-neutral recipe.

Coordinates: glTF x east, y up, z south; north facade z=0. No city placement.
No repository state is read or written; neutral flat-face/GLB assembly follows
existing project emitters, without adopting their 1904 residential contracts.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, random, struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
ROOT=Path(__file__).resolve().parent.parent
RECIPE=ROOT/'data/chamber_of_commerce_1865.recipe.json'

def canon(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,s): return tuple(x*s for x in a)
def dot(a,b): return math.fsum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):
 d=math.sqrt(dot(a,a)); return tuple(x/d for x in a)

class Mesh:
 def __init__(self,name): self.name=name; self.p=[];self.n=[];self.uv=[];self.c=[];self.idx=[]
 def face(self,pts,hint=None,uv=None,confidence=.35):
  n=cross(sub(pts[1],pts[0]),sub(pts[2],pts[0])); q=dot(n,n)
  if q<1e-16:return
  n=unit(n)
  if hint is not None and dot(n,hint)<0: pts=list(reversed(pts));n=mul(n,-1);uv=list(reversed(uv)) if uv else None
  base=len(self.p)
  for i,p in enumerate(pts):
   self.p.append(p);self.n.append(n);self.c.append(confidence)
   self.uv.append(uv[i] if uv else (p[0]/4.2+p[2]/4.2,-p[1]/1.68))
  for i in range(1,len(pts)-1):self.idx.extend((base,base+i,base+i+1))
 def box(self,a,b,omit=None,confidence=.35):
  x0,y0,z0=a;x1,y1,z1=b
  for name,pts,n in [('north',[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],(0,0,-1)),('south',[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],(0,0,1)),('west',[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)],(-1,0,0)),('east',[(x1,y0,z0),(x1,y0,z1),(x1,y1,z1),(x1,y1,z0)],(1,0,0)),('top',[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],(0,1,0)),('bottom',[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],(0,-1,0))]:
   if name!=omit:self.face(pts,n,confidence=confidence)

class Face:
 def __init__(self,name,length,origin,along,out): self.name=name;self.length=length;self.origin=origin;self.along=along;self.out=out
 def p(self,s,y,d=0):return add(add(self.origin,mul(self.along,s)),add((0,y,0),mul(self.out,d)))
 def poly(self,mesh,pts,d=0,confidence=.35):mesh.face([self.p(s,y,d)for s,y in pts],self.out,[(s/4.2,-y/1.68)for s,y in pts],confidence)
 def rect(self,mesh,a,b,d=0,confidence=.35):self.poly(mesh,[(a[0],a[1]),(b[0],a[1]),b,(a[0],b[1])],d,confidence)
 def block(self,mesh,s0,s1,y0,y1,depth,back=0,confidence=.35):
  points=[self.p(s,y,d)for d in [back,depth]for y in [y0,y1]for s in [s0,s1]]
  # Outer face and four reveals only: no coplanar back against the wall.
  for ix,hint in [((4,5,7,6),self.out),((0,4,6,2),mul(self.along,-1)),((1,3,7,5),self.along),((0,1,5,4),(0,-1,0)),((2,6,7,3),(0,1,0))]:mesh.face([points[i]for i in ix],hint,confidence=confidence)

def arch(cx,width,sill,head,name='',kind='window'):
 return {'s':cx,'w':width,'sill':sill,'head':head,'r':width/2,'spring':head-width/2,'name':name,'kind':kind}
def top(o,s):return o['spring']+math.sqrt(max(0,o['r']**2-(s-o['s'])**2))
def outline(o,segments=24):
 return [(o['s']-o['r'],o['sill']),(o['s']+o['r'],o['sill'])]+[(o['s']+o['r']*math.cos(a),o['spring']+o['r']*math.sin(a))for a in [i*math.pi/segments for i in range(segments+1)]]
def ring(face,mesh,cx,cy,rx,ry,thick,depth,segments=32,partial=False):
 n=segments//2 if partial else segments
 for i in range(n):
  a=i*(math.pi if partial else 2*math.pi)/n;b=(i+1)*(math.pi if partial else 2*math.pi)/n
  pts=[(cx+rx*math.cos(a),cy+ry*math.sin(a)),(cx+rx*math.cos(b),cy+ry*math.sin(b)),(cx+(rx-thick)*math.cos(b),cy+(ry-thick)*math.sin(b)),(cx+(rx-thick)*math.cos(a),cy+(ry-thick)*math.sin(a))]
  face.poly(mesh,pts,depth)
  # Outer/inner edges make relief read in an oblique view.
  for j,k in [(0,1),(2,3)]: mesh.face([face.p(*pts[j],depth),face.p(*pts[k],depth),face.p(*pts[k],depth-.12),face.p(*pts[j],depth-.12)])

def wall(face,mesh,holes,height):
 xs=[0,face.length]
 for o in holes:
  xs.extend(o['s']+o['r']*math.cos(i*math.pi/24)for i in range(25))
 xs=sorted(set(round(max(0,min(face.length,x)),9)for x in xs))
 for a,b in zip(xs,xs[1:]):
  if b-a<1e-7:continue
  hs=sorted([o for o in holes if o['s']-o['r']<(a+b)/2<o['s']+o['r']],key=lambda o:o['sill'])
  low=(0,0)
  for o in hs:
   if o['sill']>max(low)+1e-7:face.poly(mesh,[(a,low[0]),(b,low[1]),(b,o['sill']),(a,o['sill'])])
   low=(top(o,a),top(o,b))
  if height>max(low)+1e-7:face.poly(mesh,[(a,low[0]),(b,low[1]),(b,height),(a,height)])

def fit_rect(face,mesh,cx,width,sill,head,depth):
 face.rect(mesh,(cx-width/2,sill),(cx+width/2,head),depth)

def opening(face,o,meshes):
 trim,glass,sash,dark=meshes['stone_trim'],meshes['glass'],meshes['sash'],meshes['recess']
 pts=outline(o);recess=.7 if o['kind']=='portal' else .22
 face.poly(dark,pts,-recess-.03)
 face.poly(glass,pts,-recess)
 for a,b in zip(pts,pts[1:]+pts[:1]):
  trim.face([face.p(*a),face.p(*b),face.p(*b,-recess),face.p(*a,-recess)])
 band=.19 if o['kind']=='upper' else .15
 face.block(trim,o['s']-o['r']-band,o['s']-o['r'],o['sill'],o['spring'],.13)
 face.block(trim,o['s']+o['r'],o['s']+o['r']+band,o['sill'],o['spring'],.13)
 ring(face,trim,o['s'],o['spring'],o['r']+band,o['r']+band,band,.13,partial=True)
 face.block(trim,o['s']-o['r']-.25,o['s']+o['r']+.25,o['sill']-.20,o['sill'],.33)
 # Hood, keystone and restrained scroll-like crown are visible forms, detail is reconstructed.
 ring(face,trim,o['s'],o['spring'],o['r']+.38,o['r']+.38,.11,.24,partial=True)
 face.block(trim,o['s']-.15,o['s']+.15,o['head']+.10,o['head']+.72,.30)
 if o['kind']=='upper':
  lights=3 if o.get('central') else 2
  oc_r=.55 if o.get('central') else .39
  oc_y=o['head']-.85
  if o.get('central'):
   for dx,dy,rr in [(0,.32,.32),(-.50,-.47,.38),(.50,-.47,.38)]:ring(face,sash,o['s']+dx,oc_y+dy,rr,rr,.065,-.05,24)
  else:ring(face,sash,o['s'],oc_y,oc_r,oc_r,.07,-.05,24)
  shaft_top=o['spring']-.35
  for i in range(1,lights):
   x=o['s']-o['r']+o['w']*i/lights
   face.block(sash,x-.045,x+.045,o['sill']+.08,shaft_top,-.075,back=-recess)
  for k in [1,2,3]:
   y=o['sill']+(shaft_top-o['sill'])*k/4
   face.block(sash,o['s']-o['r']+.05,o['s']+o['r']-.05,y-.04,y+.04,-.075,back=-recess)
  # Small subarch heads beneath the fanlight follow the pictured divided sash.
  for i in range(lights):
   cx=o['s']-o['r']+o['w']*(i+.5)/lights
   ring(face,sash,cx,shaft_top-o['w']/lights/2,o['w']/lights/2-.04,o['w']/lights/2-.04,.065,-.075,20,True)
 else:
  face.block(sash,o['s']-.045,o['s']+.045,o['sill']+.1,o['spring'],-.08,back=-recess)
  for y in [o['sill']+(o['spring']-o['sill'])*.42,o['spring']-.06]:face.block(sash,o['s']-o['r']+.04,o['s']+o['r']-.04,y-.05,y+.05,-.08,back=-recess)
  if o['kind']=='portal':
   face.rect(meshes['door'],(o['s']-o['r']+.06,o['sill']+.05),(o['s']+o['r']-.06,o['sill']+3.05),-recess+.015)
   for dx in [-.5,.5]:face.block(sash,o['s']+dx-.35,o['s']+dx+.35,o['sill']+.45,o['sill']+2.6,-recess+.05,back=-recess+.02)

def texture(kind):
 rng=random.Random(18650830+len(kind));n=512;im=Image.new('RGB',(n,n)); pix=im.load()
 base={'stone':(186,178,159),'roof':(61,66,64),'brick':(133,82,63)}[kind]
 for y in range(n):
  for x in range(n):
   noise=rng.randint(-5,5);pix[x,y]=tuple(max(0,min(255,c+noise))for c in base)
 d=ImageDraw.Draw(im)
 if kind=='stone':
  for row,y in enumerate(range(0,n,128)):
   d.line((0,y,n,y),fill=(138,132,117),width=2)
   for x in range(-128,n+128,128):d.line((x+(64 if row%2 else 0),y,x+(64 if row%2 else 0),y+128),fill=(151,145,130),width=2)
 elif kind=='brick':
  for row,y in enumerate(range(0,n,32)):
   d.line((0,y,n,y),fill=(143,135,117),width=3)
   for x in range(-64,n+64,64):d.line((x+(32 if row%2 else 0),y,x+(32 if row%2 else 0),y+32),fill=(143,135,117),width=2)
 else:
  for row,y in enumerate(range(0,n,64)):
   d.line((0,y,n,y),fill=(40,44,43),width=2)
   for x in range(-64,n+64,64):d.line((x+(32 if row%2 else 0),y,x+(32 if row%2 else 0),y+64),fill=(45,49,47),width=1)
 b=io.BytesIO();im.save(b,format='PNG',compress_level=9);return b.getvalue()

def build(r):
 names=['stone_wall','stone_trim','roof','brick','glass','sash','door','recess','iron']
 ms={n:Mesh(n)for n in names};f=r['form'];W,D,H=f['width_m'],f['depth_m'],f['cornice_m'];fr=r['front'];side=r['side']
 faces=[Face('north',W,(-W/2,0,0),(1,0,0),(0,0,-1)),Face('west',D,(-W/2,0,0),(0,0,1),(-1,0,0)),Face('east',D,(W/2,0,0),(0,0,1),(1,0,0)),Face('south',W,(-W/2,0,D),(1,0,0),(0,0,1))]
 records=[]
 for face in faces:
  holes=[]
  if face.name=='north':
   for x in fr['upper_centres_m']:
    central=x==0;o=arch(x+W/2,fr['central_width_m']if central else fr['flank_width_m'],fr['upper_sill_m'],fr['upper_sill_m']+(fr['central_height_m']if central else fr['flank_height_m']),f'north_upper_{x}', 'upper');o['central']=central;holes.append(o)
    if not central:holes.append(arch(x+W/2,2.45,2.55,7.0,f'north_lower_{x}'))
   for x in fr['portal_centres_m']:holes.append(arch(x+W/2,fr['portal_width_m'],fr['portal_sill_m'],fr['portal_head_m'],f'north_portal_{x}','portal'))
   for x in [-11.15,-7,7,11.15]:holes.append(arch(x+W/2,1.65,.38,1.7,f'north_basement_{x}'))
  elif face.name in ('west','east'):
   for i in range(side['upper_bay_count']):
    s=side['first_centre_m']+(side['last_centre_m']-side['first_centre_m'])*i/(side['upper_bay_count']-1)
    holes.append(arch(s,side['upper_width_m'],fr['upper_sill_m'],fr['upper_sill_m']+side['upper_height_m'],f'{face.name}_upper_{i}','upper'))
    entry=i==side['side_entry_bay'];holes.append(arch(s,2.55 if entry else side['ground_width_m'],.32 if entry else side['ground_sill_m'],7.4 if entry else side['ground_head_m'],f'{face.name}_lower_{i}','portal'if entry else'window'))
    if not entry:holes.append(arch(s,1.6,.38,1.7,f'{face.name}_basement_{i}'))
  else:
   for x in [3.5,8.8,14.17,19.5,24.8]:
    for sill,head in [(2.5,6.8),(10.5,15),(17,21.5)]:holes.append(arch(x,1.9,sill,head,f'south_{x}_{sill}'))
  wall(face,ms['brick']if face.name=='south'else ms['stone_wall'],holes,H)
  for o in holes:opening(face,o,ms)
  records.extend({'face':face.name,**o,'grade':'reconstructed'if face.name in ('east','south')else'inferred'}for o in holes)
  # Basement cap, continuous first-storey cornice and four-part deep main entablature.
  B=f['first_story_belt_m'];bt=f['basement_top_m']
  for y,depth,height in [(bt-.08,.18,.20),(B-.8,.24,.18),(B-.52,.34,.30),(B-.1,.22,.18),(H-2.0,.25,.22),(H-1.65,.32,.28),(H-.90,.62,.25),(H-.48,.78,.22),(H-.12,.86,.24)]:face.block(ms['stone_trim'],-.18,face.length+.18,y,y+height,depth)
  # Raised ashlar quoins divide front into three bays; side/end corners are repeated cautiously.
  div=[x+W/2 for x in fr['division_centres_m']]if face.name=='north'else[.28,face.length-.28]
  for x in div:
   y=0
   while y<H-2.0:
    width=.74 if round(y/.45)%2 else 1.03
    face.block(ms['stone_trim'],x-width/2,x+width/2,y+.025,min(y+.425,H-2.0),.30)
    y+=.45
  # Dentils and brackets keep their own source-visible rhythm; individual spacing reconstructed.
  count=round(face.length/.72)
  for i in range(count):
   s=(i+.5)*face.length/count
   face.block(ms['stone_trim'],s-.13,s+.13,H-1.50,H-.95,.52)
   face.block(ms['stone_trim'],s-.085,s+.085,H-.65,H-.45,.72)
 # Mansard shell, no residential kit priors. Broad roofplanes use the explicit recipe.
 inset=f['roof_inset_m'];rh=H+f['roof_rise_m'];deck=rh+f['roof_deck_rise_m']
 lower=[(-W/2-.30,H,-.30),(W/2+.30,H,-.30),(W/2+.30,H,D+.30),(-W/2-.30,H,D+.30)]
 upper=[(-W/2+inset,rh,inset),(W/2-inset,rh,inset),(W/2-inset,rh,D-inset),(-W/2+inset,rh,D-inset)]
 for i in range(4):ms['roof'].face([lower[i],lower[(i+1)%4],upper[(i+1)%4],upper[i]],[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][i])
 ms['roof'].face([(x,deck,z)for x,y,z in upper],(0,1,0))
 for face in faces:
  face.block(ms['stone_trim'],-.3,face.length+.3,H+.12,H+.35,.40)
  # Upper crest band kept near the roof's actual inset at this height.
  for y in [rh-.40,rh-.15]:face.block(ms['stone_trim'],inset,face.length-inset,y,y+.16,-inset+.12,back=-inset-.08)
  centres=[x+W/2 for x in r['roof']['north_oculi_centres_m']]if face.name=='north'else([3.0+(D-6)*i/9 for i in range(10)]if face.name in ('east','west')else[W*.25,W*.5,W*.75])
  for i,s in enumerate(centres):
   central=face.name=='north'and i==2;rad=r['roof']['central_radius_m']if central else r['roof']['oculus_radius_m'];cy=H+r['roof']['oculus_above_cornice_m'];d=.30-(inset+.30)*(cy-rad-.28-H)/f['roof_rise_m']+.20
   ring(face,ms['stone_trim'],s,cy,rad+.23,rad+.28,.20,d,40)
   face.poly(ms['glass'],[(s+rad*math.cos(i*2*math.pi/40),cy+rad*math.sin(i*2*math.pi/40))for i in range(40)],d-.10)
   face.block(ms['sash'],s-.035,s+.035,cy-rad,cy+rad,d-.04,back=d-.12)
   face.block(ms['sash'],s-rad,s+rad,cy-.035,cy+.035,d-.04,back=d-.12)
   if central:
    ring(face,ms['stone_trim'],s,cy,rad+.65,rad+.95,.16,d+.06,40,True)
    face.block(ms['stone_trim'],s-.22,s+.22,cy+rad+.80,cy+rad+1.50,d+.03)
 # Finials instead of claiming an October flag. North shoulder urn silhouettes are bounded reconstructions.
 for x in [-W/2+.5,-4.6,4.6,W/2-.5]:
  ms['stone_trim'].box((x-.20,H+.1,-.45),(x+.20,H+1.2,-.02),omit='south')
  ms['stone_trim'].box((x-.28,H+1.2,-.50),(x+.28,H+1.38,.03),omit='south')
 # Bare source-visible central staff, not an asserted October flag.
 if r['roof']['flagstaff']:
  staff=faces[0];s0=W/2;d=-.05;start=H+r['roof']['oculus_above_cornice_m']+2.3
  staff.block(ms['stone_trim'],s0-.16,s0+.16,start-.6,start+.35,d+.08,back=d-.18)
  staff.block(ms['iron'],s0-.045,s0+.045,start+.25,start+r['roof']['staff_length_m'],d,back=d-.09)
 # Basement-area railings pictured at north/west. Exact run depth/picket spacing reconstructed.
 for face in faces[:2]:
  if face.name=='north':runs=[(.5,W/2-4.65),(W/2+4.65,W-.5)]
  else:
   ent=side['first_centre_m']+(side['last_centre_m']-side['first_centre_m'])*side['side_entry_bay']/(side['upper_bay_count']-1)
   runs=[(.5,ent-1.6),(ent+1.6,D-.5)]
  for a,b in runs:
   for y in [.20,1.05]:face.block(ms['iron'],a,b,y,y+.055,.93,back=.875)
   n=math.ceil((b-a)/.25)
   for i in range(n+1):
    q=a+(b-a)*i/n;wide=.045 if i%5==0 else .018
    face.block(ms['iron'],q-wide,q+wide,.1,1.16 if i%5==0 else 1.08,.935,back=.885)
 # Rear chimneys are reconstructed from the visible side-roof stacks, never a measured count.
 for i in range(r['roof']['rear_chimneys']):
  z=8+(D-16)*i/max(1,r['roof']['rear_chimneys']-1)
  ms['brick'].box((-W/2+inset+.5,rh-.6,z-.30),(-W/2+inset+1.15,deck+1.65,z+.30))
  ms['stone_trim'].box((-W/2+inset+.42,deck+1.58,z-.38),(-W/2+inset+1.23,deck+1.83,z+.38))
 # Three shallow front stair risers, localized under the three portals.
 for i in range(3):ms['stone_trim'].box((-4.5,i*.105,-1.05+i*.25),(4.5,(i+1)*.105,.0),omit='south')
 return ms,records

def glb(meshes,recipe):
 data=bytearray();views=[];acc=[];images=[];textures=[]
 def put(b,target=None):
  o=len(data);data.extend(b);data.extend(b'\0'*((-len(data))%4));v={'buffer':0,'byteOffset':o,'byteLength':len(b)}
  if target:v['target']=target
  views.append(v);return len(views)-1
 def accessor(v,ct,typ,n,target,mm=False):
  flat=[z for item in v for z in(item if n>1 else[item])];fmt={5126:'f',5125:'I'}[ct];a={'bufferView':put(struct.pack('<'+fmt*len(flat),*flat),target),'componentType':ct,'type':typ,'count':len(v)}
  if mm:
   a['min']=[struct.unpack('<f',struct.pack('<f',min(p[k]for p in v)))[0]for k in range(n)];a['max']=[struct.unpack('<f',struct.pack('<f',max(p[k]for p in v)))[0]for k in range(n)]
  acc.append(a);return len(acc)-1
 for kind in ['stone','roof','brick']:
  images.append({'name':'original_'+kind,'mimeType':'image/png','bufferView':put(texture(kind))});textures.append({'source':len(images)-1,'sampler':0})
 specs={'stone_wall':([1,1,1,1],.92,0),'stone_trim':([.65,.60,.49,1],.82,None),'roof':([1,1,1,1],.88,1),'brick':([1,1,1,1],.92,2),'glass':([.055,.075,.075,1],.32,None),'sash':([.17,.14,.105,1],.76,None),'door':([.10,.072,.045,1],.78,None),'recess':([.012,.014,.014,1],1,None),'iron':([.035,.04,.04,1],.75,None)}
 mats=[];prims=[]
 for name,m in meshes.items():
  if not m.idx:continue
  color,rough,tex=specs[name];pbr={'baseColorFactor':color,'roughnessFactor':rough,'metallicFactor':.1 if name=='iron'else 0}
  if tex is not None:pbr['baseColorTexture']={'index':tex}
  mats.append({'name':name,'pbrMetallicRoughness':pbr})
  prims.append({'attributes':{'POSITION':accessor(m.p,5126,'VEC3',3,34962,True),'NORMAL':accessor(m.n,5126,'VEC3',3,34962),'TEXCOORD_0':accessor(m.uv,5126,'VEC2',2,34962),'_CONFIDENCE':accessor(m.c,5126,'SCALAR',1,34962)},'indices':accessor(m.idx,5125,'SCALAR',1,34963),'material':len(mats)-1})
 j={'asset':{'version':'2.0','generator':'chamber_emit.py isolated original1865candidate'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':recipe['id'],'mesh':0}],'meshes':[{'name':recipe['id'],'primitives':prims}],'buffers':[{'byteLength':len(data)}],'bufferViews':views,'accessors':acc,'materials':mats,'images':images,'textures':textures,'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}],'extras':{'source_status':recipe['status'],'recipe_sha256':sha(RECIPE.read_bytes()),'grade':'candidate_geometry_confidence_reconstructed','frame':recipe['frame']}}
 jb=json.dumps(j,separators=(',',':'),ensure_ascii=False).encode();jb+=b' '*((-len(jb))%4);length=12+8+len(jb)+8+len(data)
 return struct.pack('<4sII',b'glTF',2,length)+struct.pack('<I4s',len(jb),b'JSON')+jb+struct.pack('<I4s',len(data),b'BIN\0')+data

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();r=json.loads(RECIPE.read_text());meshes,openings=build(r);blob=glb(meshes,r)
 target=ROOT/'assets/chamber_of_commerce_1865__original_1865.glb'
 info={'structure_id':r['id'],'phase':r['phase'],'status':r['status'],'recipe_sha256':sha(RECIPE.read_bytes()),'generator_sha256':sha(Path(__file__).read_bytes()),'glb_sha256':sha(blob),'bytes':len(blob),'triangles':sum(len(m.idx)//3 for m in meshes.values()),'vertices':sum(len(m.p)for m in meshes.values()),'draw_primitives':sum(bool(m.idx)for m in meshes.values()),'openings':openings,'bounds_m':{'min':[min(p[k]for m in meshes.values()for p in m.p)for k in range(3)],'max':[max(p[k]for m in meshes.values()for p in m.p)for k in range(3)]},'unresolved':['Absoluteheight/grade datum and camera fit','Full source-visible ornament/sideentrance placement','October1871tenant/signcontinuity','East/rear faces reconstructed','No cityparcelplacement/contextreplacement or appintegration yet']}
 assert sum(o['face']=='north'and o['kind']=='upper'for o in openings)==5
 assert sum(o['face']=='north'and o['kind']=='portal'for o in openings)==3
 assert sum(o['face']=='west'and o['kind']=='upper'for o in openings)==10
 assert all(math.isfinite(v)for m in meshes.values()for p in m.p for v in p)
 if a.check:
  assert target.read_bytes()==blob,'GLB differs from reproducible candidate'
  assert (ROOT/'assets/chamber_of_commerce_1865.json').read_bytes()==canon(info),'Sidecar differs'
  print('Candidate byte reproduction PASS;5northupper/3northportal/10westupper; finitegeometry')
 else:
  target.write_bytes(blob);(ROOT/'assets/chamber_of_commerce_1865.json').write_bytes(canon(info));print(json.dumps({k:info[k]for k in ['bytes','triangles','vertices','draw_primitives','glb_sha256']}))
if __name__=='__main__':main()
