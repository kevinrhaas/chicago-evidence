import json,math,pathlib,hashlib,itertools,struct
HERE=pathlib.Path(__file__).resolve().parent
APP=pathlib.Path('/workspace/chicago-waistcoat/chicago/4d')
receipt=pathlib.Path('/workspace/shared/horse-materials-FIRST-ACTUAL-20261022/receipt.json')
R=json.loads(receipt.read_text());state=R['captures'][0]['state'];bounds=state['world_bounds']
assert R['pass'] and state['indexed_vertices']==11556 and len(state['meshes'])==3
assert all(c['state']['world_bounds']==bounds for c in R['captures'])
rigid=APP/'docs/RESEARCH/standing-horse-development-T-2800/RIGID-SUPPORT-AND-TOPOLOGY-REVIEW.json'
root_y=json.loads(rigid.read_text())['fit']['root_y_m'];shift=root_y-state['receipt']['root_y_m']
meta_file=APP/'data/terrain/epochs/e1834_harbor_cut/heightfield.json';meta=json.loads(meta_file.read_text());bin_file=meta_file.with_name(meta['bin'])
assert meta['encoding']=='int16'
def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def field(e,n):
 gx=(e-meta['origin_e'])/meta['cell_m'];gz=(n-meta['origin_n'])/meta['cell_m'];assert 0<=gx<meta['cols']-1 and 0<=gz<meta['rows']-1
 x,z=math.floor(gx),math.floor(gz);fx,fz=gx-x,gz-z
 with bin_file.open('rb')as f:
  def h(z,x):
   f.seek(2*(z*meta['cols']+x));return f32(struct.unpack('<h',f.read(2))[0]*meta['scale']+meta.get('offset',0))
  return (h(z,x)*(1-fx)+h(z,x+1)*fx)*(1-fz)+(h(z+1,x)*(1-fx)+h(z+1,x+1)*fx)*fz
views={'side':[-127.5,-289.5,180,-7],'quarter':[-123.1,-291.6,225,-7]}
def project(e,n,bearing,pitch):
 eye=field(e,n)+1.68;yaw=math.radians(-bearing);pitch=math.radians(pitch);cy,sy=math.cos(yaw),math.sin(yaw);cp,sp=math.cos(pitch),math.sin(pitch);t=math.tan(math.radians(62/2));values=[]
 for root_delta,eye_delta in itertools.product([-.05,.05],[-.25,.25]):
  for x,y,z in itertools.product(*[[bounds[0][i],bounds[1][i]]for i in range(3)]):
   dx,dy,dz=x-e,y+shift+root_delta-(eye+eye_delta),z+n
   cx,cz=cy*dx-sy*dz,sy*dx+cy*dz
   vy,vz=cp*dy+sp*cz,-sp*dy+cp*cz;depth=-vz
   assert .1<depth<3000
   values.append([cx/(depth*t*.5),vy/(depth*t),depth])
 return {'pose_enu_bearing_pitch':[e,n,bearing,math.degrees(pitch)],'bilinear_walk_ground_nominal_m':field(e,n),'default_eye_y_m':eye,'conservative_ndc_min':[min(v[k]for v in values)for k in range(2)],'conservative_ndc_max':[max(v[k]for v in values)for k in range(2)],'depth_minmax_m':[min(v[2]for v in values),max(v[2]for v in values)],'pass_point97':all(abs(v[0])<=.97 and abs(v[1])<=.97 for v in values)}
results={name:project(*pose)for name,pose in views.items()}
out={'status':'HELD prelaunch camera math only; no browser, no model/yard/photo approval','method':'Conservative 8-corner convex AABB from all11556 actual skinned indexed vertices of all3 unchanged source groups, after approved uniform/support/heading transform. Relative AABB translated by recorded reconstructed yard rootY. Project each corner at all4 combinations of rootheight±50mm and cameraeye±250mm around bilinearfield+default1.68m. Positive depth makes perspective clip halfspaces convex: all corners within .97 contains the whole source AABB. Production YXZ camera orientation, bearingToYaw=−bearing, FOV62deg/aspect.5. Runtime all-indexed-vertex guards unchanged and authoritative.','inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [receipt,rigid,meta_file,bin_file,APP/'renderers/web/js/angles.js',APP/'renderers/web/js/walker.js',APP/'renderers/web/js/travel-settings.js']},'source_sha256':'41acd9bee7bf05fbcdd813fad965027b01b8801d6a21ca1c22eb2178c8842988','actual_flat_source_world_aabb':bounds,'flat_to_yard_y_translation_m':shift,'yard_root_y_nominal_m':root_y,'eyeheight_default_m':1.68,'fov_deg':62,'aspect':.5,'views':results,'limits':['Bilinear ground is nominal cameraheight only; runtimewalker surface/decks/kerbs and actualhorse root remain authoritative. The explicit ±250mm eye and ±50mm root margins are a conservative prelaunch test window, not proof that all runtimeground lies within it.','No visibility/occlusion/budget or visualquality claim from projection math. No viewport/DPR/framing threshold/model/support/material change. No adaptive correction or browser retry.']}
(HERE/'MOBILE-FRAMING.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(results,indent=2));assert all(v['pass_point97']for v in results.values())
