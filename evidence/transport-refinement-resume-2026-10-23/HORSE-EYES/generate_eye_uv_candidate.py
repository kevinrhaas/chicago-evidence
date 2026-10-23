"""HELD SOURCE ONLY. Do not execute without exact ROOT release.

One external UV-only candidate. No image edit, GLB baseline overwrite, browser,
app write, rig/geometry/material change, command spawn, or automatic retry.
"""
from pathlib import Path
import argparse,copy,hashlib,json,math,struct

D=Path(__file__).parent.resolve()
BASE=Path('/workspace/chicago-waistcoat/chicago/4d/renderers/web/transport/standing-horse/horse-sevket-v16-planted-standing-v1.glb')
BASE_SHA='b479442cb03ac46eb13c19da15a79cdfaf28dbdf356b116f78de7ce7ecdc60be'
DECODER=Path('/workspace/shared/HORSE-B479-EYE-UV-APERTURE-SOURCE-INSPECTION-20261023/ACTUAL-CORRECTED-READER.py')
DECODER_SHA='3f7e06fe4c1e0a91e142e0adc4358a8b277662e9335228269ed5d156e6630729'
RAYS=Path('/workspace/shared/HORSE-B479-OCULAR-FIRST-EXTERIOR-20RAY-SOURCE-20261023/RESULT.json')
RAYS_SHA='d44a04364da6e3a8dcc23f3e67ea5dc00d14cda9c4c2801d7036e44a1da7a6fa'
IMAGE_SHA='1e0382c8ad5d155dc3bf45378a5a37bb10bdcc79ffefee211e69edb3b609a5b3'
sha=lambda b:hashlib.sha256(b).hexdigest()
# Frozen proposed trial values. A different trial needs separate ROOT review.
A,BANG,ALPHA0,ALPHA_I=0.20,0.07,0.01,0.55
RHO_P,RHO_I,RHO_F=0.10,0.36,0.42
SEAM_TARGET=100*math.pi/180
BACK_U,BACK_V,BACK_R=0.78,0.50,0.035
MAX_UV_CENTROID_ERROR=4/256

def need(ok,message):
    if not ok:raise ValueError(message)

def radial(alpha,theta,alpha_front):
    """Strictly monotone C1 Hermite radial field; no image modification."""
    ap=A*BANG/math.hypot(BANG*math.cos(theta),A*math.sin(theta))
    k=RHO_P/A
    x=[0.,ALPHA0,ap,ALPHA_I,alpha_front]
    y=[0.,k*ALPHA0,RHO_P,RHO_I,RHO_F]
    need(all(x[i+1]>x[i] and y[i+1]>y[i] for i in range(4)),'Radial knot ordering')
    h=[x[i+1]-x[i] for i in range(4)]
    delta=[(y[i+1]-y[i])/h[i] for i in range(4)]
    m=[delta[0]]
    for i in range(1,4):
        w1=2*h[i]+h[i-1];w2=h[i]+2*h[i-1]
        m.append((w1+w2)/(w1/delta[i-1]+w2/delta[i]))
    m.append(delta[-1])
    # Sufficient slope limiter, followed by exact per-interval derivative minimum.
    for i in range(4):
        q=math.hypot(m[i]/delta[i],m[i+1]/delta[i])
        if q>3:
            factor=3/q;m[i]*=factor;m[i+1]*=factor
    for i in range(4):
        qa=3*(m[i]+m[i+1]-2*delta[i])
        qb=2*(3*delta[i]-2*m[i]-m[i+1]);qc=m[i]
        probes=[0.,1.]
        if qa>0 and 0 < -qb/(2*qa) < 1:probes.append(-qb/(2*qa))
        need(min(qa*t*t+qb*t+qc for t in probes)>1e-8,'Nonpositive radial derivative')
    i=next((i for i in range(4) if alpha<=x[i+1]),3)
    need(x[i]-1e-10<=alpha<=x[i+1]+1e-10,'Front chart outside radial domain')
    t=max(0.,min(1.,(alpha-x[i])/h[i]))
    return ((2*t**3-3*t*t+1)*y[i]+(t**3-2*t*t+t)*h[i]*m[i]
            +(-2*t**3+3*t*t)*y[i+1]+(t**3-t*t)*h[i]*m[i+1])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root-release',required=True,type=Path)
    args=parser.parse_args()
    release=json.loads(args.root_release.read_text())
    need(release.get('released') is True,'HELD: explicit ROOT release absent')
    need(release.get('generator_sha256')==sha(Path(__file__).read_bytes()),'ROOT exact generator hash')
    need(release.get('baseline_sha256')==BASE_SHA,'ROOT exact baseline hash')
    need(D.is_relative_to(Path('/workspace/shared')),'External diagnostic directory only')
    OUT=D/'ACTUAL-ONE-UV-ONLY-CANDIDATE'
    need(not OUT.exists(),'Once-only candidate: no retry/overwrite')
    OUT.mkdir()
    receipt={'state':'RUNNING_EXTERNAL_UV_ONLY','baseline':str(BASE),'baseline_sha256':BASE_SHA,
             'source_sha256':sha(Path(__file__).read_bytes()),'photographic_acceptance':False}
    try:
        raw=BASE.read_bytes();need(sha(raw)==BASE_SHA,'Frozen baseline drift')
        size=struct.unpack_from('<I',raw,12)[0]
        g=json.loads(raw[20:20+size]);original_json=copy.deepcopy(g)
        B=raw[28+size:]
        need(raw[:4]==b'glTF' and struct.unpack_from('<I',raw,4)[0]==2,'GLB2 only')
        need(struct.unpack_from('<I',raw,20+size+4)[0]==0x004E4942,'One normal BIN chunk')
        saved=DECODER.read_bytes();need(sha(saved)==DECODER_SHA,'Pinned source decoder')
        raybytes=RAYS.read_bytes();need(sha(raybytes)==RAYS_SHA,'Pinned exposed-aperture evidence')
        # No prior inspection/report loop is executed, only its frozen decoder block.
        text=saved.decode();fragment=text[text.index('fmt='):text.index('eye=[p for p in prims')]
        env={'g':g,'B':B,'struct':struct,'math':math}
        exec(compile(fragment,str(DECODER)+':decoder-fragment','exec'),env)
        prims=env['prims'];unit=env['unit'];dot=env['dot'];sub=env['sub'];mul=env['mul'];cross=env['cross'];norm=env['norm']
        eye=[p for p in prims if g['materials'][p['material']]['name']=='Eye_brown']
        need(len(eye)==1 and len(prims)==3 and len(g['materials'])==3,'Original three-mesh/material contract')
        eye=eye[0];need(eye['attributes']['TEXCOORD_0']==10 and eye['indices_accessor']==11,'Original eye UV/index mapping')
        accessor=g['accessors'][10];view=g['bufferViews'][accessor['bufferView']]
        need(accessor['componentType']==5126 and accessor['type']=='VEC2' and accessor['count']==3968,'Original float32 UV10')
        need(view.get('byteStride')==8 and not accessor.get('sparse'),'Original dense stride8 eye UVs')
        uvstart=view.get('byteOffset',0)+accessor.get('byteOffset',0);uvlength=accessor['count']*8
        need(uvstart==332984 and uvlength==31744,'Exact protected UV byte range')
        images=[]
        for im in g['images']:
            v=g['bufferViews'][im['bufferView']];at=v.get('byteOffset',0)
            images.append(sha(B[at:at+v['byteLength']]))
        need(images[4]==IMAGE_SHA and len(images)==6,'Unchanged six source images')
        points=eye['points'];indices=eye['indices'];triangles=[indices[i:i+3] for i in range(0,len(indices),3)]
        # Index-connected islands: an existing shared vertex can have only ONE UV.
        parents=list(range(len(points)))
        def find(i):
            while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
            return i
        def union(a,b):
            a,b=find(a),find(b)
            if a!=b:parents[b]=a
        for a,b,c in triangles:union(a,b);union(a,c)
        islands={}
        for i in range(len(points)):islands.setdefault(find(i),[]).append(i)
        rays=json.loads(raybytes)['hits'];UV=[None]*len(points);charts={};frames={};component_receipts={}
        for side,sign in [('positive_X',1),('negative_X',-1)]:
            ids=[i for i,p in enumerate(points) if sign*p[0]>0]
            need(len(ids)==1984,'Original two source-eye components')
            C=tuple(sum(points[i][k] for i in ids)/len(ids) for k in range(3))
            lo=[min(points[i][k] for i in ids) for k in range(3)]
            hi=[max(points[i][k] for i in ids) for k in range(3)]
            R=.5*min(hi[1]-lo[1],hi[2]-lo[2])
            radii=[norm(sub(points[i],C)) for i in ids]
            need(R>0 and max(abs(r-R)/R for r in radii)<=.10,'Source globe too nonspherical for declared UV recipe')
            seed=next(r['first_hit'] for r in rays if r['side']==side and r['view']=='lateral' and r['sample']=='vertical_minus')
            need(seed['material_name']=='Eye_brown','Actual exposed lower-globe seed')
            G=unit(sub(seed['source_rest_position'],C))
            H=unit(sub((0,0,1),mul(G,dot((0,0,1),G))))
            up=sub((0,1,0),mul(G,dot((0,1,0),G)))
            V=unit(sub(up,mul(H,dot(up,H))))
            need(dot(V,(0,1,0))>0 and abs(dot(H,V))<1e-8,'Per-eye anatomical frame')
            def polar(point):
                p=unit(sub(point,C));h=dot(p,H);v=dot(p,V)
                return math.atan2(math.hypot(h,v),dot(p,G)),math.atan2(v,h)
            polar_vertex={i:polar(points[i]) for i in ids}
            side_islands=[]
            for values in islands.values():
                if not any(i in polar_vertex for i in values):continue
                need(all(i in polar_vertex for i in values),'Island crosses anatomical eye sides')
                chart='front' if sum(polar_vertex[i][0] for i in values)/len(values)<=SEAM_TARGET else 'back'
                side_islands.append((values,chart))
                for i in values:charts[i]=chart
            front=[i for i in ids if charts[i]=='front'];back=[i for i in ids if charts[i]=='back']
            need(front and back,'Existing index seams cannot form two charts')
            alpha_front=max(polar_vertex[i][0] for i in front)
            alpha_back=min(polar_vertex[i][0] for i in back)
            need(ALPHA_I<alpha_front<math.pi-.01 and 0<alpha_back<math.pi,'Legal existing-island seam domain')
            for ray in rays:
                if ray['side']==side and ray['first_hit']['material_name']=='Eye_brown':
                    need(all(charts[i]=='front' for i in ray['first_hit']['index_triplet']),'Back seam crosses demonstrated exposed globe')
            def mapped(point,chart):
                alpha,theta=polar(point)
                if chart=='front':
                    rho=radial(alpha,theta,alpha_front)
                    return(.5+rho*math.cos(theta),.5-rho*math.sin(theta))
                rho=BACK_R*(math.pi-alpha)/(math.pi-alpha_back)
                return(BACK_U+rho*math.cos(theta),BACK_V-rho*math.sin(theta))
            for i in ids:UV[i]=mapped(points[i],charts[i])
            frames[side]=(C,G,H,V,alpha_front,alpha_back,mapped)
            component_receipts[side]=dict(center=C,radius_scale_m=R,radius_min_m=min(radii),radius_max_m=max(radii),gaze_reconstructed=G,horizontal=H,vertical=V,front_vertices=len(front),back_vertices=len(back),index_islands=len(side_islands),alpha_front=alpha_front,alpha_back=alpha_back)
            # Evaluate interpolation NOW while this side's mapping closure is bound.
            worst=0.
            for tri in triangles:
                if not all(i in polar_vertex for i in tri):continue
                need(len({charts[i] for i in tri})==1,'Cross-chart triangle')
                centroid=tuple(sum(points[i][k] for i in tri)/3 for k in range(3))
                actual=mapped(centroid,charts[tri[0]])
                linear=tuple(sum(UV[i][k] for i in tri)/3 for k in range(2))
                worst=max(worst,math.hypot(actual[0]-linear[0],actual[1]-linear[1]))
            component_receipts[side]['max_centroid_interpolation_error_uv']=worst
            need(worst<=MAX_UV_CENTROID_ERROR,'Existing tessellation undersamples ocular field')
        need(all(v is not None for v in UV),'Complete existing eye UV stream')
        # Protect actual GPU float32 coordinates, not only unquantized formulas.
        uvbytes=b''.join(struct.pack('<ff',*v) for v in UV)
        quantized=[struct.unpack_from('<ff',uvbytes,i*8) for i in range(len(UV))]
        minimum_area=float('inf');orientation={};welded={};seam_positions=0
        for i,p in enumerate(points):welded.setdefault(tuple(round(x,7) for x in p),[]).append(i)
        for values in welded.values():
            groups={charts[i] for i in values}
            if len(groups)>1:seam_positions+=1
            for chart in groups:
                same=[quantized[i] for i in values if charts[i]==chart]
                need(max(math.hypot(u[0]-same[0][0],u[1]-same[0][1]) for u in same)<1e-6,'Undeclared UV crack within chart')
        for tri in triangles:
            pa,pb,pc=[points[i] for i in tri];geometry_area=norm(cross(sub(pb,pa),sub(pc,pa)))
            ua,ub,uc=[quantized[i] for i in tri]
            area=(ub[0]-ua[0])*(uc[1]-ua[1])-(ub[1]-ua[1])*(uc[0]-ua[0])
            if geometry_area>1e-12:need(abs(area)>1e-12,'New UV-degenerate nondegenerate source triangle')
            minimum_area=min(minimum_area,abs(area))
            side='positive_X' if pa[0]>0 else 'negative_X';chart=charts[tri[0]]
            C,G,H,V,*_=frames[side]
            outward=dot(cross(sub(pb,pa),sub(pc,pa)),sub(tuple((pa[k]+pb[k]+pc[k])/3 for k in range(3)),C))
            need(outward>0,'Source eye triangle winding not outward')
            expected=-1 if dot(cross(H,V),G)>0 else 1
            if chart=='back':expected=-expected
            need(area*expected>0,'Isolated reversed/folded ocular UV triangle')
            orientation[side+':'+chart]=expected
        need(seam_positions>0,'No legal existing duplicate-position chart seam')
        newbin=bytearray(B);newbin[uvstart:uvstart+uvlength]=uvbytes
        need(bytes(newbin[:uvstart])==B[:uvstart] and bytes(newbin[uvstart+uvlength:])==B[uvstart+uvlength:],'Non-UV BIN stream changed')
        g['accessors'][10]['min']=[min(v[k] for v in quantized) for k in range(2)]
        g['accessors'][10]['max']=[max(v[k] for v in quantized) for k in range(2)]
        need('chicago4d_ocular_uv_derivative' not in g.get('asset',{}).get('extras',{}),'Never overwrite baseline derivative notice')
        g.setdefault('asset',{}).setdefault('extras',{})['chicago4d_ocular_uv_derivative']={
            'baseline_sha256':BASE_SHA,'reconstructed_gaze_and_equine_pupil':True,
            'texture_pixels_unchanged':True,'source_credit':'Horse by sevketkabatas, CC BY4.0, via Objaverse',
            'license_url':'https://creativecommons.org/licenses/by/4.0/',
            'changes':'Eye UV10 and accessor bounds only; original planted-standing rig/geometry/materials/images retained; no photographic acceptance'}
        allowed=copy.deepcopy(g);allowed['accessors'][10]=copy.deepcopy(original_json['accessors'][10])
        del allowed['asset']['extras']['chicago4d_ocular_uv_derivative']
        if 'extras' not in original_json['asset']:del allowed['asset']['extras']
        need(allowed==original_json,'Unexpected non-UV/provenance JSON mutation')
        j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
        total=12+8+len(j)+8+len(newbin)
        candidate=struct.pack('<4sII',b'glTF',2,total)+struct.pack('<II',len(j),0x4E4F534A)+j+struct.pack('<II',len(newbin),0x004E4942)+bytes(newbin)
        file=OUT/'horse-sevket-v16-planted-standing-ocular-uv-CANDIDATE.glb';file.write_bytes(candidate)
        for name in ['ATTRIBUTION.md','LICENSE-CC-BY-4.0.txt','PROPOSAL.md']:(OUT/name).write_bytes((D/name).read_bytes())
        need(sha(BASE.read_bytes())==BASE_SHA,'Baseline after-read drift')
        receipt.update(state='SOURCE_CANDIDATE_WRITTEN_NOT_RENDERED_OR_ACCEPTED',candidate_file=str(file),candidate_sha256=sha(candidate),candidate_bytes=len(candidate),changed_uv_accessor=10,uv_start_in_BIN=uvstart,uv_bytes=uvlength,non_uv_BIN_exact=True,materials_exact=True,images_exact_sha256=images,components=component_receipts,minimum_absolute_uv_double_area=minimum_area,chart_orientation=orientation,existing_seam_positions=seam_positions,baseline_after_sha256=BASE_SHA)
    except Exception as error:
        receipt.update(state='SOURCE_GENERATOR_REJECTED_NO_RETRY',error=str(error))
        raise
    finally:
        (OUT/'ACTUAL-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':main()
