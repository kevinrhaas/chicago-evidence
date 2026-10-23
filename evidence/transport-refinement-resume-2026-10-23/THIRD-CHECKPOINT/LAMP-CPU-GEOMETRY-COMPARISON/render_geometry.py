"""Render immutable GLB geometry for a bounded form diagnostic, not Three/PBR acceptance."""
from pathlib import Path
import json,hashlib,struct,time,math,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).parent
FIX=Path('/workspace/shared/T2794-LAMP-RESUME-20261023-2245/SOURCE8-V17-V18/fixture/transport')
W,H=1280,800
EXPECTED={'v17':'ec2bfc0da49b570429dbcd8db39250aa6f1bbf55587570f0dafad9a42afc4ee5','v18':'bce1ecc757a7175cb193b1263fc8dbcdf1ce76a263916d3cff5e41dc4a835938'}
COUNTS={'v17':33502,'v18':33374}
SHA=lambda x:hashlib.sha256(x).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def unit(x):return x/np.maximum(np.linalg.norm(x,axis=-1,keepdims=True),1e-30)
def srgb(x):return np.where(x<=.04045,x/12.92,((x+.055)/1.055)**2.4)
def display(x):return np.where(x<=.0031308,12.92*x,1.055*np.maximum(x,0)**(1/2.4)-.055)
def rgbhex(h):return srgb(np.array([(h>>16)&255,(h>>8)&255,h&255],dtype=float)/255)
def local_matrix(n):
 if 'matrix'in n:return np.array(n['matrix'],float).reshape(4,4,order='F')
 x,y,z,w=n.get('rotation',[0,0,0,1]);need(abs(x*x+y*y+z*z+w*w-1)<1e-6,'Nonunit node quaternion')
 r=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
 m=np.eye(4);m[:3,:3]=r@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);return m

def load_model(version):
 raw=(FIX/version/'brougham.glb').read_bytes();need(SHA(raw)==EXPECTED[version],'Frozen GLB drift')
 magic,ver,total=struct.unpack_from('<4sII',raw);need(magic==b'glTF'and ver==2 and total==len(raw),'GLB2 header')
 length,kind=struct.unpack_from('<II',raw,12);need(kind==0x4e4f534a,'JSON chunk');g=json.loads(raw[20:20+length]);b=raw[28+length:];need(struct.unpack_from('<I',raw,24+length)[0]==0x004e4942,'BIN chunk')
 need(not g.get('images')and not g.get('textures'),'Unsupported texture/image map present')
 for mat in g['materials']:
  need(not any('Texture'in k for k in mat),'Unsupported texture map')
  need(not any('Texture'in k for k in mat.get('pbrMetallicRoughness',{})),'Unsupported PBR map')
  need(set(mat.get('extensions',{}))<= {'KHR_materials_clearcoat'},'Unsupported material extension')
  need(mat.get('alphaMode','OPAQUE')in ['OPAQUE','BLEND'],'Unsupported alpha mode')
 need(not g.get('skins') and not g.get('animations'),'Expected static carriage GLB')
 types={5121:np.dtype('u1'),5123:np.dtype('<u2'),5125:np.dtype('<u4'),5126:np.dtype('<f4')};dims={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
 def accessor(i):
  a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];dt=types[a['componentType']];width=dims[a['type']];need(not a.get('normalized')and not a.get('sparse'),'Unsupported accessor');need(v.get('byteStride',dt.itemsize*width)==dt.itemsize*width,'Interleaved accessor refused');at=v.get('byteOffset',0)+a.get('byteOffset',0);return np.frombuffer(b,dtype=dt,count=a['count']*width,offset=at).reshape(a['count'],width).copy()
 coords=[];normals=[];mats=[];lamps=[];doubles=[];parents={child:i for i,n in enumerate(g['nodes'])for child in n.get('children',[])}
 def visit(i,parent):
  n=g['nodes'][i];world=parent@local_matrix(n)
  if'mesh'in n:
   for pr in g['meshes'][n['mesh']]['primitives']:
    need(pr.get('mode',4)==4,'Triangle primitive required');p=accessor(pr['attributes']['POSITION']).astype(float);no=accessor(pr['attributes']['NORMAL']).astype(float);ix=accessor(pr['indices']).reshape(-1).astype(int);need(len(ix)%3==0,'Index alignment');p=p@world[:3,:3].T+world[:3,3];no=unit(no@np.linalg.inv(world[:3,:3]));ids=ix.reshape(-1,3);count=len(ids);mi=pr['material'];mask=np.zeros(count,bool);frame=g['nodes'][parents[i]]['name']
    for part in g['extras']['parts']:
     if part['frame']==frame and part['material']==mi and part['name'].startswith('lamp_'):
      a=part['triangle_start_in_batch'];z=a+part['triangles'];need(0<=a<=z<=count,'Lamp part span');mask[a:z]=True
    coords.append(p[ids]);normals.append(no[ids]);mats.extend([mi]*count);lamps.append(mask);doubles.extend([g['materials'][mi].get('doubleSided',False)]*count)
  for child in n.get('children',[]):visit(child,world)
 for i in g['scenes'][g.get('scene',0)]['nodes']:visit(i,np.eye(4))
 vertices=np.concatenate(coords);norms=np.concatenate(normals);mask=np.concatenate(lamps);material=np.array(mats);double=np.array(doubles)
 need(len(vertices)==COUNTS[version],'Triangle count changed');need(np.isfinite(vertices).all()and np.isfinite(norms).all(),'Nonfinite attributes');need(mask.any(),'No lamp span identified')
 return {'version':version,'vertices':vertices,'normals':norms,'materials':g['materials'],'material_ids':material,'lamps':mask,'double':double,'hash':SHA(raw),'bounds':[vertices.reshape(-1,3).min(0).tolist(),vertices.reshape(-1,3).max(0).tolist()]}

def camera(view):
 raw=(FIX/'v17/camera-hypothesis.json').read_bytes();need(raw==(FIX/'v18/camera-hypothesis.json').read_bytes(),'Per-version camera drift');fit=json.loads(raw)['fit'];r=np.array(fit['basis']['right']);u=np.array(fit['basis']['up']);t=np.array(fit['basis']['towardCamera']);B=np.stack([r,u,t]);need(np.max(abs(B@B.T-np.eye(3)))<1e-10,'Camera basis orthogonality');need(np.linalg.det(B)>0,'Camera handedness')
 crop=np.array([900,450,1300,875]if view=='detail'else[100,400,1500,1000]);cw,ch=crop[2:]-crop[:2];scale=min(W/cw,H/ch);pad=np.array([(W-cw*scale)/2,(H-ch*scale)/2]);pp=pad+(np.array(fit['principal_px'])-crop[:2])*scale;f=fit['focal_px']*scale;d=fit['distance_m'];P=np.zeros((4,4));P[0,0]=2*f/W;P[1,1]=2*f/H;P[0,2]=1-2*pp[0]/W;P[1,2]=2*pp[1]/H-1;P[2,2]=-(1000+100)/(1000-100);P[2,3]=-2*1000*100/(1000-100);P[3,2]=-1
 def project(points):
  q=points@B.T;depth=d-q[...,2];xy=np.stack([pp[0]+f*q[...,0]/depth,pp[1]-f*q[...,1]/depth],axis=-1);return xy,depth
 checks=[]
 for p in [[0,0,0],[.67,.55,1.15],[.67,.72,-1.15],[0,2,0]]:
  p=np.array(p);q=B@p;q[2]-=d;clip=P@np.r_[q,1];ndc=clip[:3]/clip[3];matrix=np.array([(ndc[0]+1)*W/2,(1-ndc[1])*H/2]);xy,depth=project(p);native=np.array(fit['principal_px'])+fit['focal_px']*np.array([p@r,-p@u])/depth;source=pad+(native-crop[:2])*scale;err=max(float(np.linalg.norm(matrix-xy)),float(np.linalg.norm(xy-source)));need(err<1e-6,'Independent camera projection mismatch');checks.append({'point':p.tolist(),'expected_px':source.tolist(),'matrix_px':matrix.tolist(),'error_px':err})
 return {'view':view,'fit':fit,'basis':B,'camera_position':d*t,'project':project,'crop':crop.tolist(),'scale':float(scale),'padding_px':pad.tolist(),'projection_matrix':P.tolist(),'checks':checks}

SUN=unit(np.array([4.,8.,5.]));SKY=rgbhex(0xe5f1ff);GROUND=rgbhex(0x8d7b57);SUNC=rgbhex(0xfff3d7)
def shade(normal,world,mat,cam):
 n=unit(normal);v=unit(cam-world);ndotl=np.maximum(n@SUN,0);hemi=(n[...,1,None]*.5+.5)*SKY+(1-(n[...,1,None]*.5+.5))*GROUND;p=mat.get('pbrMetallicRoughness',{});base=np.array(p.get('baseColorFactor',[1,1,1,1])[:3]);metal=p.get('metallicFactor',1);rough=max(.04,p.get('roughnessFactor',1));F0=.04*(1-metal)+base*metal;half=unit(v+SUN);power=min(128,max(2,2/(rough*rough)-2));spec=np.maximum(np.sum(n*half,axis=-1),0)**power;irradiance=2.6*hemi;diffuse=base*(irradiance*(.65+.35*(1-metal))+3.8*SUNC*ndotl[...,None]*(1-metal)*.45);reflective=F0*(irradiance*.18+3.8*SUNC*spec[...,None]*.4);clear=mat.get('extensions',{}).get('KHR_materials_clearcoat',{}).get('clearcoatFactor',0)*.04*spec[...,None]*SUNC;return np.maximum(diffuse+reflective+clear,0)

def render(model,cam):
 verts=model['vertices'];norms=model['normals'];mi=model['material_ids'];is_lamp=model['lamps'];doubles=model['double'];materials=model['materials']
 # The original100m plane is geometry, not a fitted background or per-version framing.
 floor=np.array([[[-50,-.004,-50],[-50,-.004,50],[50,-.004,-50]],[[-50,-.004,50],[50,-.004,50],[50,-.004,-50]]],float)
 vertices=np.concatenate([verts,floor]);normals=np.concatenate([norms,np.tile([0.,1.,0.],(2,3,1))]);mids=np.r_[mi,[len(materials)]*2];lamp=np.r_[is_lamp,[False]*2];ds=np.r_[doubles,[False]*2];materials=materials+[{'name':'original100m_floor','pbrMetallicRoughness':{'baseColorFactor':list(rgbhex(0xc9c7b9))+[1.],'metallicFactor':0,'roughnessFactor':1}}]
 xy,depth=cam['project'](vertices);need(np.min(depth)>100 and np.max(depth)<1000,'Source depth interval clips geometry');geon=np.cross(vertices[:,1]-vertices[:,0],vertices[:,2]-vertices[:,0]);toward=np.einsum('ij,ij->i',geon,cam['camera_position']-vertices[:,0]);front=toward>1e-12;valid=front|ds
 areas=(xy[:,1,0]-xy[:,0,0])*(xy[:,2,1]-xy[:,0,1])-(xy[:,1,1]-xy[:,0,1])*(xy[:,2,0]-xy[:,0,0]);valid&=abs(areas)>1e-12
 lo=np.floor(xy.min(1)).astype(int);hi=np.ceil(xy.max(1)).astype(int);valid&=(hi[:,0]>=0)&(lo[:,0]<W)&(hi[:,1]>=0)&(lo[:,1]<H);lo=np.maximum(lo,[0,0]);hi=np.minimum(hi,[W-1,H-1]);lo=np.minimum(lo,[W,H]);hi=np.maximum(hi,[-1,-1]);
 zbuffer=np.full((H,W),np.inf);color=np.tile(rgbhex(0xe9e7df),(H,W,1));lamp_union=np.zeros((H,W),bool);winning_lamp=np.zeros((H,W),bool);triangle_id=np.full((H,W),-1,np.int32);opaque=[];transparent=[]
 for i in np.flatnonzero(valid):
  alpha=materials[mids[i]].get('alphaMode','OPAQUE')
  (transparent if alpha=='BLEND'else opaque).append(i)
 transparent.sort(key=lambda i:(-float(depth[i].mean()),i))
 counts={'source_model_triangles':len(verts),'with_original_floor_triangles':len(vertices),'model_frontfacing_triangles':int(np.count_nonzero(front[:len(verts)])),'projected_in_view_triangles':int(np.count_nonzero(valid[:len(verts)])),'projected_lamp_triangles':int(np.count_nonzero(valid[:len(verts)]&is_lamp)),'opaque_raster_triangles':len(opaque),'transparent_raster_triangles':len(transparent),'fragment_updates':0}
 for i in opaque+transparent:
  x0,y0=lo[i];x1,y1=hi[i];
  if x1<x0 or y1<y0:continue
  xs=np.arange(x0,x1+1,dtype=float)+.5;ys=np.arange(y0,y1+1,dtype=float)+.5;X,Y=np.meshgrid(xs,ys);a,b,c=xy[i];area=areas[i];l0=((b[0]-X)*(c[1]-Y)-(b[1]-Y)*(c[0]-X))/area;l1=((c[0]-X)*(a[1]-Y)-(c[1]-Y)*(a[0]-X))/area;l2=1-l0-l1;inside=(l0>=-1e-9)&(l1>=-1e-9)&(l2>=-1e-9)
  if lamp[i]:lamp_union[y0:y1+1,x0:x1+1]|=inside
  inv=l0/depth[i,0]+l1/depth[i,1]+l2/depth[i,2];pixelz=1/inv;oldz=zbuffer[y0:y1+1,x0:x1+1];keep=inside&(pixelz<oldz)
  if not keep.any():continue
  lam=np.stack([l0[keep]/depth[i,0],l1[keep]/depth[i,1],l2[keep]/depth[i,2]],axis=1);lam/=lam.sum(1)[:,None];normal=lam@normals[i];
  if not front[i]:normal=-normal
  world=lam@vertices[i];values=shade(normal,world,materials[mids[i]],cam['camera_position']);patch=color[y0:y1+1,x0:x1+1];mat=materials[mids[i]];alpha=mat.get('pbrMetallicRoughness',{}).get('baseColorFactor',[1,1,1,1])[3]
  if mat.get('alphaMode')=='BLEND':patch[keep]=values*alpha+patch[keep]*(1-alpha)
  else:
   patch[keep]=values;oldz[keep]=pixelz[keep];winning_lamp[y0:y1+1,x0:x1+1][keep]=lamp[i];triangle_id[y0:y1+1,x0:x1+1][keep]=i
  counts['fragment_updates']+=int(keep.sum())
 # A deterministic ACES-curve approximation and sRGB output; not Three's full PBR pipeline.
 exposed=color*1.3;mapped=np.clip((exposed*(2.51*exposed+.03))/(exposed*(2.43*exposed+.59)+.14),0,1);rgb=np.clip(np.rint(display(mapped)*255),0,255).astype('uint8')
 counts.update({'visible_lamp_opaque_pixels':int(winning_lamp.sum()),'all_projected_lamp_coverage_pixels':int(lamp_union.sum()),'camera_depth_range_m':[float(depth.min()),float(depth.max())],'projected_model_bbox_px':[xy[:len(verts)].reshape(-1,2).min(0).tolist(),xy[:len(verts)].reshape(-1,2).max(0).tolist()],'material_inventory':[{'name':m['name'],'alphaMode':m.get('alphaMode','OPAQUE'),'texture_maps':False}for m in model['materials']]})
 return rgb,lamp_union,counts

def controls():
 # Perspective depth/attribute interpolation is independently exercised on a synthetic triangle.
 z=np.array([2.,4.,8.]);lam=np.array([.2,.3,.5]);w=lam/z;w/=w.sum();depth=1/(lam/z).sum();need(abs(depth-1/(.1+.075+.0625))<1e-12,'Perspective depth control');need(np.max(abs(w-lam))>.1,'Perspective attribute control must differ from affine');n=np.array([[1,0,0],[0,1,0],[0,0,1]],float);need(abs(np.linalg.norm(unit(w@n))-1)<1e-12,'Interpolated normal control');need(np.dot(np.cross([1,0,0],[0,1,0]),[0,0,1])>0,'Backface orientation control');return {'perspective_depth_and_non_affine_attribute_control':True,'normal_renormalization':True,'front_back_orientation':True}

def main():
 started=time.monotonic();out=ROOT/'ACTUAL';need(not out.exists(),'Once-only output');out.mkdir();pins={}
 for p in [FIX/'v17/brougham.glb',FIX/'v18/brougham.glb',FIX/'v17/camera-hypothesis.json',FIX/'v18/camera-hypothesis.json',FIX/'v17/plate0095.jpg',FIX/'v18/plate0095.jpg',FIX/'v17/demo-prefix.js',FIX.parent.parent/'source-extension.js']:
  pins[str(p)]={'sha256':SHA(p.read_bytes()),'bytes':p.stat().st_size}
 need(pins[str(FIX/'v17/plate0095.jpg')]['sha256']=='b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe','Untouched source plate pin')
 report={'status':'CPU_GEOMETRY_DIAGNOSTIC_RUNNING','scope':'Actual immutable meshes and fixed source8 camera; software form diagnostic only. No browser/GPU/PBR/performance/photographic acceptance.','resolution_per_panel':[W,H],'input_pins':pins,'controls':controls(),'renders':[],'comparisons':[],'approximations':['Lambert/hemisphere plus bounded roughness-Phong reflection/clearcoat approximation, not Three GGX/DFG/PMREM.','Exact original light directions/colors/intensities/exposure; approximate ACES curve.','No cast shadows, contact shadows, environment raytracing, refraction, depth quantization, antialiasing or pixel-matched browser claim.','Transparent BLEND triangles sorted deterministically back-to-front by mean camera depth, opaque depth-test/no transparent depthwrite.','Original crop/projective formula evaluated at1280x800 per render panel; this is not a claim about the browser DOM panel size.']}
 try:
  models={v:load_model(v)for v in ['v17','v18']};a,b=models['v17'],models['v18'];need(a['materials']==b['materials'],'Material delta not permitted');need(a['bounds']==b['bounds'],'Full-model bounds changed')
  for key in ['vertices','normals','material_ids']:
   need(np.array_equal(a[key][~a['lamps']],b[key][~b['lamps']]),'Protected nonlamp stream changed: '+key)
  report['protected_nonlamp_geometry_normals_materials_exact']=True;report['model_bounds_m']=a['bounds'];report['source_materials']=a['materials'];
  for view in ['fullquarter','detail']:
   cam=camera(view);images={};masks={};
   for version in ['v17','v18']:
    im,mask,stats=render(models[version],cam);name=f'{version}-{view}-software-geometry.png';Image.fromarray(im).save(out/name);images[version]=im;masks[version]=mask;report['renders'].append({'version':version,'view':view,'png':name,'sha256':SHA((out/name).read_bytes()),'projection_checks':cam['checks'],'crop':cam['crop'],'scale':cam['scale'],'padding_px':cam['padding_px'],'projection_matrix':cam['projection_matrix'],**stats});print(version,view,stats['projected_in_view_triangles'],'triangles;',stats['all_projected_lamp_coverage_pixels'],'lamp pixels',flush=True)
   diff=np.any(images['v17']!=images['v18'],axis=2);allowed=masks['v17']|masks['v18'];outside=diff&~allowed;need(not outside.any(),'Difference outside projected lamp-only coverage');need(diff.any(),'No visible lamp geometry difference');ys,xs=np.where(diff);report['comparisons'].append({'view':view,'changed_pixels':int(diff.sum()),'changed_bbox_px':[[int(xs.min()),int(ys.min())],[int(xs.max()),int(ys.max())]],'outside_projected_lamp_union_changed_pixels':int(outside.sum()),'protected_nonlamp_image_pixels_exact':True});Image.fromarray(np.concatenate([images['v17'],images['v18']],axis=1)).save(out/f'{view}-v17-v18-software-comparison.png');Image.fromarray((diff*255).astype('uint8')).save(out/f'{view}-lamp-only-difference-mask.png')
  shutil.copy2(FIX/'v17/plate0095.jpg',out/'plate0095-untouched.jpg');need(SHA((out/'plate0095-untouched.jpg').read_bytes())==pins[str(FIX/'v17/plate0095.jpg')]['sha256'],'Plate copy drift');report['inputs_unchanged']=all(SHA(Path(p).read_bytes())==v['sha256']for p,v in pins.items());need(report['inputs_unchanged'],'Final input drift');report['status']='CPU_GEOMETRY_FORM_COMPARISON_RENDERED_ONLY';report['photographic_or_ThreePBR_or_browser_acceptance']=False
 except Exception as e:report.update(status='CPU_GEOMETRY_DIAGNOSTIC_FAIL',error=repr(e));raise
 finally:
  report['elapsed_seconds']=time.monotonic()-started;(out/'RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
