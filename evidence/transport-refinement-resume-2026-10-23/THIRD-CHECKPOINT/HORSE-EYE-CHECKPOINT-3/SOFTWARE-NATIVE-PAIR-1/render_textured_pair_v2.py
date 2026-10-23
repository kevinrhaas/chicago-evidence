"""Actual mesh/UV/image CPU diagnostic. No browser/PBR/photographic acceptance."""
from pathlib import Path
import json,hashlib,time,math
import numpy as np
from PIL import Image,ImageDraw
from software_geometry_reference import unit,srgb,display,controls,need
ROOT=Path(__file__).parent;DATA=ROOT/'EXPORTED-ACTUAL';W,H=1280,800;SHA=lambda b:hashlib.sha256(b).hexdigest();E=json.loads((DATA/'EXPORT-RECEIPT.json').read_text());need(E['status']=='PASS_ACTUAL_CLONED_REST_INPUT_EXPORT_ONLY'and E['exact_actual_protected_streams'],'Actual protected loader export required')
TEXTURES={};TEXTURE_ROWS={};SAMPLES={'map':0,'roughnessMap':0,'metalnessMap':0}
for row in E['textures']:
 p=DATA/row['file'];need(SHA(p.read_bytes())==row['sha256'],'Embedded image drift');im=Image.open(p);need(im.size==(row['width'],row['height']),'Actual Pillow dimensions disagree with source shim');a=np.asarray(im.convert('RGB'),dtype=float)/255;TEXTURES[row['sha256']]={'raw':a,'linear':srgb(a)};TEXTURE_ROWS[row['sha256']]={**row,'actual_Pillow_mode':im.mode,'RGB_channel_min':np.min(a,axis=(0,1)).tolist(),'RGB_channel_max':np.max(a,axis=(0,1)).tolist(),'pixels_decoded_here_not_in_loader_shim':True}

def sample(texture,UV,color):
 need(texture['channel']==0,'Unsupported UV channel');M=np.asarray(texture['uv_transform_matrix']).reshape(3,3,order='F');v=UV@M[:2,:2].T+M[:2,2];v=v.copy()
 if texture['flipY']:v[:,1]=1-v[:,1]
 a=TEXTURES[texture['sha256']]['linear'if color else'raw'];h,w=a.shape[:2];q=v*np.array([w,h])-.5;x=np.floor(q[:,0]).astype(int);y=np.floor(q[:,1]).astype(int);f=q-np.stack([x,y],axis=1)
 def ix(i,size,mode):
  if mode==1000:return i%size
  if mode==1001:return np.clip(i,0,size-1)
  if mode==1002:
   j=i%(2*size);return np.where(j<size,j,2*size-1-j)
  raise ValueError('Unsupported texture wrap')
 x0=ix(x,w,texture['wrapS']);x1=ix(x+1,w,texture['wrapS']);y0=ix(y,h,texture['wrapT']);y1=ix(y+1,h,texture['wrapT']);fx,fy=f[:,0,None],f[:,1,None];return((1-fx)*(1-fy)*a[y0,x0]+fx*(1-fy)*a[y0,x1]+(1-fx)*fy*a[y1,x0]+fx*fy*a[y1,x1])

scale=.36440688373115426;native_origin=np.array([.0013648444640481372,-.09537431257051576,-.0034172495824063565]);SUN=(np.array([6.,12.,8.])-native_origin)*scale;SUN_TARGET=-native_origin*scale;SUN_DIR=unit(SUN-SUN_TARGET);SKY=np.ones(3);HEMI_GROUND=srgb(np.full(3,0x88/255));

def shade(normal,world,mat,camera,UV=None):
 n=unit(normal);maps=mat['textures'];base=np.broadcast_to(np.array(mat['color_linear'],dtype=float),n.shape).copy();rough=np.full(len(n),mat['roughness'],dtype=float);metal=np.full(len(n),mat['metalness'],dtype=float)
 for key in ['normalMap','aoMap','emissiveMap','alphaMap']:need(maps[key]is None,'Unsupported non-null map '+key)
 if maps['map']is not None:SAMPLES['map']+=len(n);base*=sample(maps['map'],UV,True)
 if maps['roughnessMap']is not None:SAMPLES['roughnessMap']+=len(n);rough*=sample(maps['roughnessMap'],UV,False)[:,1]
 if maps['metalnessMap']is not None:SAMPLES['metalnessMap']+=len(n);metal*=sample(maps['metalnessMap'],UV,False)[:,2]
 hemi=(n[:,1,None]*.5+.5)*SKY+(1-(n[:,1,None]*.5+.5))*HEMI_GROUND;ndotl=np.maximum(n@SUN_DIR,0);diffuse=base*(2*hemi+2.5*ndotl[:,None])/math.pi*(1-metal[:,None]);view=unit(camera-world);half=unit(view+SUN_DIR);power=np.minimum(128,np.maximum(2,2/np.maximum(.04,rough)**2-2));spec=np.maximum(np.sum(n*half,axis=1),0)**power;F0=.04*(1-metal[:,None])+base*metal[:,None];reflection=F0*spec[:,None]*2.5*.08;return np.maximum(diffuse+reflection,0)

def model(version):
 row=E['variants'][version];verts=[];norms=[];uvs=[];mids=[]
 for i,o in enumerate(row['objects']):
  arrays={}
  for k,dtype,width in [('positions','<f8',3),('normals','<f8',3),('uv','<f4',2),('indices','<u4',1)]:
   pin=o['attributes'][k];b=(DATA/pin['file']).read_bytes();need(SHA(b)==pin['sha256'],'Exported stream drift');arrays[k]=np.frombuffer(b,dtype=dtype).reshape(-1,width)
  ids=arrays['indices'].reshape(-1,3).astype(int);verts.append(arrays['positions'][ids]);norms.append(arrays['normals'][ids]);uvs.append(arrays['uv'][ids].astype(float));mids.extend([i]*len(ids))
 return{'version':version,'vertices':np.concatenate(verts),'normals':np.concatenate(norms),'uv':np.concatenate(uvs),'material_ids':np.array(mids),'materials':row['materials'],'eye':np.array(mids)==2}

def camera(row,points):
 V=np.asarray(row['view']).reshape(4,4,order='F');P=np.asarray(row['projection']).reshape(4,4,order='F');M=np.asarray(row['world']).reshape(4,4,order='F');need(np.max(abs(V@M-np.eye(4)))<1e-12,'View/world inverse')
 def project(ps):
  q=ps@V[:3,:3].T+V[:3,3];clip=np.concatenate([q,np.ones(q.shape[:-1]+(1,))],axis=-1)@P.T;ndc=clip[...,:3]/clip[...,3,None];return np.stack([(ndc[...,0]+1)*W/2,(1-ndc[...,1])*H/2],axis=-1),-q[...,2]
 xy,depth=project(points);q=points@V[:3,:3].T+V[:3,3];f=H/(2*math.tan(math.radians(38)/2));ind=np.stack([W/2+f*q[...,0]/(-q[...,2]),H/2-f*q[...,1]/(-q[...,2])],axis=-1);err=float(np.max(abs(xy-ind)));need(err<1e-9,'Independent native FOV matrix projection');need(depth.min()>row['near']and depth.max()<row['far'],'Whole horse depth clipping');need((xy[...,0]>W*.0075).all()and(xy[...,0]<W*.9925).all()and(xy[...,1]>H*.0075).all()and(xy[...,1]<H*.9925).all(),'Fixed whole horse viewport clipping')
 return{'project':project,'position':np.array(row['position']),'world':M,'projection':P,'row':row,'max_independent_projection_error_px':err}

def background(cam):
 # Exact native rectangular floor is intersected analytically per ray; no near-plane triangle shortcut.
 x,y=np.meshgrid(np.arange(W)+.5,np.arange(H)+.5);inv=np.linalg.inv(cam['projection']);clip=np.stack([2*x/W-1,1-2*y/H,np.ones_like(x),np.ones_like(x)],axis=-1);v=clip@inv.T;v=v[...,:3]/v[...,3,None];worlddir=v@cam['world'][:3,:3].T;origin=cam['position'];floor_y=-.0001*scale;distance=(floor_y-origin[1])/np.where(abs(worlddir[...,1])>1e-15,worlddir[...,1],np.nan);wp=origin+worlddir*distance[...,None];viewdir=v*distance[...,None];depth=-viewdir[...,2];hit=(distance>0)&(depth>cam['row']['near'])&(depth<cam['row']['far'])&(np.abs(wp[...,0])<=50*scale)&(np.abs(wp[...,2])<=50*scale);z=np.where(hit,depth,np.inf);color=np.tile(srgb(np.full(3,0xd5/255)),(H,W,1));floor={'textures':{k:None for k in ['map','normalMap','aoMap','emissiveMap','alphaMap','roughnessMap','metalnessMap']},'color_linear':srgb(np.full(3,0xaa/255)).tolist(),'roughness':1.,'metalness':0.};color[hit]=shade(np.tile([0.,1.,0.],(int(hit.sum()),1)),wp[hit],floor,origin);return color,z

def render(m,cam,bg):
 verts=m['vertices'];norms=m['normals'];uv=m['uv'];mi=m['material_ids'];xy,depth=cam['project'](verts);geon=np.cross(verts[:,1]-verts[:,0],verts[:,2]-verts[:,0]);front=np.einsum('ij,ij->i',geon,cam['position']-verts[:,0])>1e-15;double=np.array([m['materials'][i]['side']==2 for i in mi]);valid=front|double;areas=(xy[:,1,0]-xy[:,0,0])*(xy[:,2,1]-xy[:,0,1])-(xy[:,1,1]-xy[:,0,1])*(xy[:,2,0]-xy[:,0,0]);valid&=abs(areas)>1e-12;lo=np.maximum(np.floor(xy.min(1)).astype(int),[0,0]);hi=np.minimum(np.ceil(xy.max(1)).astype(int),[W-1,H-1]);valid&=(hi[:,0]>=0)&(lo[:,0]<W)&(hi[:,1]>=0)&(lo[:,1]<H);color=bg[0].copy();zbuffer=bg[1].copy();eye_union=np.zeros((H,W),bool);winner=np.full((H,W),-1,np.int32);fragments=0
 for i in np.flatnonzero(valid):
  mat=m['materials'][mi[i]];need(not mat['transparent']and mat['opacity']==1 and mat['alphaTest']==0,'Source opaque policy only');x0,y0=lo[i];x1,y1=hi[i]
  if x1<x0 or y1<y0:continue
  X,Y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5);a,b,c=xy[i];area=areas[i];l0=((b[0]-X)*(c[1]-Y)-(b[1]-Y)*(c[0]-X))/area;l1=((c[0]-X)*(a[1]-Y)-(c[1]-Y)*(a[0]-X))/area;l2=1-l0-l1;inside=(l0>=-1e-9)&(l1>=-1e-9)&(l2>=-1e-9)
  if m['eye'][i]:eye_union[y0:y1+1,x0:x1+1]|=inside
  inv=l0/depth[i,0]+l1/depth[i,1]+l2/depth[i,2];pixelz=1/inv;oldz=zbuffer[y0:y1+1,x0:x1+1];keep=inside&(pixelz<oldz)
  if not keep.any():continue
  lam=np.stack([l0[keep]/depth[i,0],l1[keep]/depth[i,1],l2[keep]/depth[i,2]],axis=1);lam/=lam.sum(1)[:,None];normal=lam@norms[i]
  if not front[i]:normal=-normal
  world=lam@verts[i];texUV=lam@uv[i];values=shade(normal,world,mat,cam['position'],texUV);color[y0:y1+1,x0:x1+1][keep]=values;oldz[keep]=pixelz[keep];winner[y0:y1+1,x0:x1+1][keep]=mi[i];fragments+=int(keep.sum())
 rgb=np.clip(np.rint(display(np.clip(color,0,1))*255),0,255).astype('uint8');return rgb,eye_union,{'triangles':len(verts),'projected_triangles':int(valid.sum()),'fragments':fragments,'visible_eye_pixels':int((winner==2).sum()),'visible_body_hair_pixels':int(((winner==0)|(winner==1)).sum()),'eye_visible_mask':winner==2}

def main():
 start=time.monotonic();out=ROOT/'SOFTWARE-V2-ACTUAL';need(not out.exists(),'Once-only software output');out.mkdir();pins={str(p):SHA(p.read_bytes())for p in [Path(__file__),ROOT/'software_geometry_reference.py',DATA/'EXPORT-RECEIPT.json']};report={'status':'CPU_TEXTURED_DIAGNOSTIC_RUNNING','scope':'Actual production-cloned canonical-rest geometry, exact native camera matrices and unchanged embedded image pixels; software diagnostic only. No native browser, ThreePBR, GPU, performance, world, or photographic acceptance.','resolution':[W,H],'controls':controls(),'input_pins':pins,'texture_pixel_reads':TEXTURE_ROWS,'renders':[],'comparisons':[],'approximations':['Source native neutral hemisphere2 and directional2.5 positions/colors are retained; diffuseLambert plus small roughness-Phong lobe approximates material response, not ThreeGGX/DFG/PMREM/physicalspecular.','Basecolor JPEG/PNG pixels decoded with Pillow then sRGB-linearized before perspective-correct UV/bilinear sampling. Original normalized UV transforms/wrap/flipY apply. RoughnessG andmetalnessB textures sampled on same actual UVs; all roughness/metalness map channels are separately inventoried, never silently ignored.','All6 embedded images remain bit-identical; source texture/filter declarations retained as metadata. Software uses base-level bilinear filtering, no mipmaps/aniso/derivative-based filtering.','Source has no normal/AO/emissive/alpha maps; non-null unsupported maps are rejected. Imported skinned normals use actual Float32 palettes and CPU shader-order evaluation.','No cast/contact shadows, antialiasing, environment refraction or GPU depthquantization; opaque source hair remains opaque. Exact floor geometry is analytically ray-intersected.','Native source renderer uses NoToneMapping/exposure1; software clamps linear then sRGB output, no ACES substitution. No automatic camera/model/light changes.']}
 try:
  models={v:model(v)for v in ['baseline','candidate']};a,b=models.values();need(np.array_equal(a['vertices'],b['vertices'])and np.array_equal(a['normals'],b['normals'])and np.array_equal(a['material_ids'],b['material_ids']),'Protected actual cloned geometry differs');need(a['materials']==b['materials'],'Source material differs');need(np.array_equal(a['uv'][~a['eye']],b['uv'][~b['eye']]),'Non-eye UV differs');report['protected_actual_geometry_normals_materials_body_hair_UVs_exact']=True
  for row in E['cameras']:
   cam=camera(row,a['vertices']);bg=background(cam);images={};masks={};stats={}
   for version in ['baseline','candidate']:
    im,mask,s=render(models[version],cam,bg);name=version+'-'+row['name']+'-software-textured.png';Image.fromarray(im).save(out/name);images[version]=im;masks[version]=mask;stats[version]=s;report['renders'].append({'version':version,'view':row['name'],'file':name,'sha256':SHA((out/name).read_bytes()),'native_projection_matrix':row['projection'],'native_view_matrix':row['view'],'max_independent_projection_error_px':cam['max_independent_projection_error_px'],**{k:v for k,v in s.items()if k!='eye_visible_mask'}});print(version,row['name'],s['visible_eye_pixels'],'visible eye pixels',flush=True)
   diff=np.any(images['baseline']!=images['candidate'],axis=2);allowed=masks['baseline']|masks['candidate'];need(not(diff&~allowed).any(),'Difference outside projected original eye geometry');ys,xs=np.where(diff);report['comparisons'].append({'view':row['name'],'changed_pixels':int(diff.sum()),'changed_bbox_px':None if not len(xs)else[[int(xs.min()),int(ys.min())],[int(xs.max()),int(ys.max())]],'outside_projected_eye_changed_pixels':int((diff&~allowed).sum()),'protected_non_eye_image_pixels_exact':True});Image.fromarray(np.concatenate([images['baseline'],images['candidate']],axis=1)).save(out/('comparison-'+row['name']+'-baseline-candidate-software.png'));Image.fromarray((diff*255).astype('uint8')).save(out/('difference-'+row['name']+'.png'))
  need(any(r['changed_pixels']>0 for r in report['comparisons']),'No visible sourceUV diagnostic difference');report['texture_samples']=SAMPLES;need(all(n>0 for n in SAMPLES.values()),'Runtime basecolor/ORM maps not sampled');report['inputs_unchanged']=all(SHA(Path(p).read_bytes())==h for p,h in pins.items());need(report['inputs_unchanged'],'Source input drift');report['status']='CPU_TEXTURED_NATIVE_PAIR_DIAGNOSTIC_RENDERED_ONLY';report['photographic_browser_PBR_performance_acceptance']=False
 except Exception as e:report.update(status='CPU_TEXTURED_DIAGNOSTIC_FAIL',error=repr(e));raise
 finally:report['elapsed_seconds']=time.monotonic()-start;(out/'RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
