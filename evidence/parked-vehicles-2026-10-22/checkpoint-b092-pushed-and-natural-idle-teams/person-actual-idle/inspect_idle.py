"""Actual idle channels and CPU LBS; no browser or asset mutation."""
import resource
resource.setrlimit(resource.RLIMIT_CPU, (14, 14))
import sys, pathlib, json, hashlib, time, importlib.util
import numpy as np
started=time.monotonic()
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('/workspace/chicago/chicago/4d')
result=[]

def slerp(a,b,f):
    a=a/np.linalg.norm(a);b=b/np.linalg.norm(b);dot=float(a@b)
    if dot<0:b=-b;dot=-dot
    if dot>.9995:
        q=a*(1-f)+b*f
        return q/np.linalg.norm(q)
    angle=np.arccos(np.clip(dot,-1,1))
    return (a*np.sin((1-f)*angle)+b*np.sin(f*angle))/np.sin(angle)

for lod in range(4):
    path=ROOT/f'assets/humans/web/bardwell_otis_1835.lod{lod}.glb'
    sys.argv=[__file__,str(path)]
    spec=importlib.util.spec_from_file_location(f'decoder{lod}',OUT/'read_gltf.py')
    D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
    G=D.G;idle=next(a for a in G['animations']if a['name']=='idle')
    channels=[];facts=[]
    for ch in idle['channels']:
        s=idle['samplers'][ch['sampler']];ts=D.acc(s['input']).ravel();v=D.acc(s['output'])
        assert s.get('interpolation','LINEAR')in['LINEAR','STEP']
        assert len(ts)==len(v)and np.isfinite(v).all()and np.all(np.diff(ts)>0)
        ni=ch['target']['node'];kind=ch['target']['path']
        channels.append((ni,kind,ts,v,s.get('interpolation','LINEAR')))
        span=np.ptp(v,axis=0)
        angles=[]
        if kind=='rotation':
            for q in v:
                dot=abs(float(q@v[0]/np.linalg.norm(q)/np.linalg.norm(v[0])))
                angles.append(float(np.degrees(2*np.arccos(np.clip(dot,-1,1)))))
        facts.append({'node':ni,'name':G['nodes'][ni]['name'],'property':kind,'interpolation':s.get('interpolation','LINEAR'),'times_s':ts.tolist(),
                      'component_span':span.tolist(),'varying':bool(np.max(span)>1e-9),
                      'max_rotation_from_first_deg':max(angles)if angles else None,
                      'start_end_component_delta':(v[-1]-v[0]).tolist()})
    duration=max(float(c[2][-1])for c in channels)
    times=np.linspace(0,duration,25)
    meshes=[]
    for ni,n in enumerate(G['nodes']):
        if 'mesh'not in n:continue
        skin=G['skins'][n['skin']];ib=D.acc(skin['inverseBindMatrices']).reshape((-1,4,4)).transpose(0,2,1)
        for pr in G['meshes'][n['mesh']]['primitives']:
            a=pr['attributes'];p=D.acc(a['POSITION']).astype(float)
            defaults=n.get('weights',G['meshes'][n['mesh']].get('weights',[]))
            for weight,target in zip(defaults,pr.get('targets',[])):
                if weight and 'POSITION'in target:p+=float(weight)*D.acc(target['POSITION'])
            meshes.append((n['name'],np.c_[p,np.ones(len(p))],D.acc(a['JOINTS_0']).astype(int),D.acc(a['WEIGHTS_0']),skin['joints'],ib))
    snapshots={name:[]for name,*_ in meshes};bonepaths={n['name']:[]for n in G['nodes']if n['name']in['root','pelvis','spine_02','spine_03','neck_01','head','foot_l','foot_r','ball_l','ball_r']}
    for t in times:
        over={}
        for ni,kind,ts,v,mode in channels:
            i=max(0,min(len(ts)-1,int(np.searchsorted(ts,t,side='right')-1)));q=v[i]
            if i+1<len(ts)and mode=='LINEAR':
                f=float((t-ts[i])/(ts[i+1]-ts[i]));q=slerp(q,v[i+1],f)if kind=='rotation'else q*(1-f)+v[i+1]*f
            over.setdefault(ni,{})[kind]=q.tolist()
        world=D.worlds(over)
        for ni,n in enumerate(G['nodes']):
            if n['name']in bonepaths:bonepaths[n['name']].append(world[ni][:3,3].tolist())
        for name,p,j,w,joints,ib in meshes:
            matrices=np.stack([world[x]for x in joints])@ib
            v=np.einsum('nwij,nj->nwi',matrices[j],p)
            v=np.einsum('nw,nwi->ni',w,v)[:,:3]
            assert np.isfinite(v).all();snapshots[name].append(v)
    metrics={}
    for name,poses in snapshots.items():
        poses=np.array(poses);delta=np.linalg.norm(poses-poses[0],axis=2)
        r={'vertices':poses.shape[1],'maximum_vertex_displacement_from_first_m':float(delta.max()),
           'loop_max_vertex_position_seam_m':float(np.linalg.norm(poses[-1]-poses[0],axis=1).max()),
           'loop_finite_difference_velocity_seam_m_s':float(np.linalg.norm((poses[-1]-poses[-2]-poses[1]+poses[0])/(duration/24),axis=1).max()),
           'maximum_per_vertex_axis_span_m':np.ptp(poses,axis=0).max(axis=0).tolist()}
        if 'closed_shoes'in name:
            minimum=float(poses[0,:,1].min());sole=poses[0,:,1]<=minimum+.002
            r.update({'lowest_2mm_band_vertices':int(sole.sum()),'lowest_2mm_band_initial_min_y_m':minimum,
                      'lowest_2mm_band_alltime_y_range_m':[float(poses[:,sole,1].min()),float(poses[:,sole,1].max())],
                      'lowest_2mm_band_max_xyz_displacement_m':float(delta[:,sole].max()),
                      'all_shoe_vertices_minimum_y_m':float(poses[:,:,1].min())})
        metrics[name]=r
    result.append({'lod':lod,'path':str(path),'bytes':len(D.B),'sha256':hashlib.sha256(D.B).hexdigest(),
                   'idle_duration_s':duration,'sample_times_s':times.tolist(),'all_channel_facts':facts,
                   'varying_channels':[x for x in facts if x['varying']],
                   'bone_world_pivot_spans_m':{k:np.ptp(v,axis=0).tolist()for k,v in bonepaths.items()},
                   'mesh_LBS_metrics':metrics})
qualification=pathlib.Path('/workspace/shared/bardwell-connected-waistcoat-CANONICAL-SUCCESS-39736567239-96c4da4b-20261022/qualification')
prior=json.loads((qualification/'web-inspection.json').read_text())
parity=[]
for r in result:
    old=next(x for x in prior['runs']if x['file']==f"assets/humans/web/bardwell_otis_1835.lod{r['lod']}.glb")
    actual=next(v for k,v in r['mesh_LBS_metrics'].items()if 'closed_shoes'in k)['all_shoe_vertices_minimum_y_m']
    parity.append({'lod':r['lod'],'prior_browser_min_footwear_y_m':min(old['footwear_min_y_m'].values()),'actual_CPU_min_footwear_y_m':actual,'absolute_delta_m':abs(actual-min(old['footwear_min_y_m'].values()))})
receipt={'scope':'Actual exported canonical Bardwell all4LOD idle key data and full LBS vertices at25 inclusive loop times. Lowest2mm shoe band is a numerical sole proxy. Procedural runtime blink is not simulated; no pixel/naturalness/cloth/contact-area acceptance.',
         'canonical_source_head':'96c4da4b1fe68e6dec3b18c15da2f14c596a60c5','canonical_run':'39736567239',
         'qualification_record_path':str(qualification/'QUALIFICATION.json'),'prior_browser_footwear_parity':parity,
         'reader_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         'meshopt_decoder_sha256':hashlib.sha256((ROOT/'renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js').read_bytes()).hexdigest(),
         'elapsed_s':time.monotonic()-started,'LODs':result}
(OUT/'ACTUAL-IDLE-READBACK.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'elapsed_s':receipt['elapsed_s'],'LODs':[{'lod':r['lod'],'sha256':r['sha256'],'idle_duration_s':r['idle_duration_s'],'varying_channels':r['varying_channels'],'bone_world_pivot_spans_m':r['bone_world_pivot_spans_m'],'mesh_LBS_metrics':r['mesh_LBS_metrics']}for r in result]},indent=2))
