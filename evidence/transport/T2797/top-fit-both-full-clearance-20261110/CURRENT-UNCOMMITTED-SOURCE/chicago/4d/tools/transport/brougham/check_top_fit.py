# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent actual retained-facet/cap/stock checks, never sweep approval."""
import hashlib
import math
import numpy as np

POSITION_TOLERANCE=2e-7
AREA_TOLERANCE=2e-6
_EXPECTED={}


def ceiling(profile,z):
    p=np.asarray(profile,dtype=float)
    assert p[0,0]-POSITION_TOLERANCE<=z<=p[-1,0]+POSITION_TOLERANCE
    return float(np.interp(z,p[:,0],p[:,1]))


def gradient(profile,z):
    p=np.asarray(profile,dtype=float);i=max(0,min(len(p)-2,int(np.searchsorted(p[:,0],z,side='right'))-1))
    return float((p[i+1,1]-p[i,1])/(p[i+1,0]-p[i,0]))


def plane_clip(polygon,normal,bound):
    if not polygon:return []
    output=[];last=polygon[-1];last_sign=float(last@normal-bound)
    for point in polygon:
        sign=float(point@normal-bound)
        if (sign>=0)!=(last_sign>=0):output.append(last+(point-last)*(last_sign/(last_sign-sign)))
        if sign>=0:output.append(point)
        last,last_sign=point,sign
    return output


def polygon_area(polygon):
    return sum(float(np.linalg.norm(np.cross(polygon[i]-polygon[0],polygon[i+1]-polygon[0]))/2)
               for i in range(1,len(polygon)-1))


def expected_areas(source,profile,base_planes):
    key=hashlib.sha256(source.tobytes()+np.asarray(profile).tobytes()+repr(base_planes).encode()).hexdigest()
    if key not in _EXPECTED:
        before=[];after=[]
        for tri in source:
            polygon=list(tri)
            for normal,bound in base_planes:polygon=plane_clip(polygon,np.asarray(normal),bound)
            before.append(polygon_area(polygon));retained=0.
            probes=list(polygon)
            for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                for z,_ in profile:
                    if min(a[2],b[2])<z<max(a[2],b[2]):probes.append(a+(z-a[2])/(b[2]-a[2])*(b-a))
            if not probes or max(p[1]-ceiling(profile,p[2])for p in probes)<=1e-10:
                # A wholly retained source facet is not cut merely because
                # a representational end-Z differs by Float32 roundoff.
                after.append(before[-1]);continue
            for (lo,ly),(hi,hy)in zip(profile,profile[1:]):
                if not polygon:continue
                part=plane_clip(polygon,np.array([0.,0.,1.]),lo)
                part=plane_clip(part,np.array([0.,0.,-1.]),-hi)
                m=(hy-ly)/(hi-lo);b=ly-m*lo
                part=plane_clip(part,np.array([0.,-1.,m]),-b)
                retained+=polygon_area(part)
            after.append(retained)
        _EXPECTED[key]=(np.asarray(before),np.asarray(after))
    return _EXPECTED[key]


def point_triangle_distance(points,triangles):
    """Euclidean WORLD metres to the closed nominated triangle, not barycentric units."""
    points=np.asarray(points,dtype=float);triangles=np.asarray(triangles,dtype=float)
    assert points.shape==(len(triangles),3) and triangles.shape==(len(points),3,3)
    a=triangles[:,0];u=triangles[:,1]-a;v=triangles[:,2]-a;delta=points-a
    uu=np.einsum('ij,ij->i',u,u);uv=np.einsum('ij,ij->i',u,v);vv=np.einsum('ij,ij->i',v,v)
    denom=uu*vv-uv*uv;assert np.all(denom>0)
    du=np.einsum('ij,ij->i',delta,u);dv=np.einsum('ij,ij->i',delta,v)
    s=(vv*du-uv*dv)/denom;t=(uu*dv-uv*du)/denom
    projected=a+s[:,None]*u+t[:,None]*v
    edges=[]
    for i in range(3):
        start=triangles[:,i];edge=triangles[:,(i+1)%3]-start
        fraction=np.einsum('ij,ij->i',points-start,edge)/np.einsum('ij,ij->i',edge,edge)
        nearest=start+np.clip(fraction,0.,1.)[:,None]*edge
        edges.append(np.linalg.norm(points-nearest,axis=1))
    edge_distance=np.min(np.asarray(edges),axis=0)
    return np.where((s>=0)&(t>=0)&(s+t<=1),np.linalg.norm(points-projected,axis=1),edge_distance)


def verify_facets(source,source_normals,actual,actual_normals,origins,profile,base_planes=(),expected_changed=None):
    assert len(origins)==len(actual),'Top-fit source-facet map length changed'
    ids=np.asarray(origins,dtype=int);assert np.all((ids>=0)&(ids<len(source)))
    original=source[ids];normals=source_normals[ids]
    a=original[:,0];u=original[:,1]-a;v=original[:,2]-a
    uu=np.einsum('ij,ij->i',u,u);uv=np.einsum('ij,ij->i',u,v);vv=np.einsum('ij,ij->i',v,v)
    denom=uu*vv-uv*uv;assert np.all(denom>0)
    delta=actual-a[:,None];du=np.einsum('ijk,ik->ij',delta,u);dv=np.einsum('ijk,ik->ij',delta,v)
    s=(vv[:,None]*du-uv[:,None]*dv)/denom[:,None];t=(uu[:,None]*dv-uv[:,None]*du)/denom[:,None]
    closest=a[:,None]+s[:,:,None]*u[:,None]+t[:,:,None]*v[:,None]
    distance=point_triangle_distance(actual.reshape((-1,3)),np.repeat(original,3,axis=0))
    assert np.all(distance<=POSITION_TOLERANCE),'Retained top-fit facet escaped its nominated original triangle'
    assert np.linalg.norm(closest-actual,axis=2).max()<=POSITION_TOLERANCE,'Retained top-fit closed-WORLD surface changed'
    interpolated=(1-s-t)[:,:,None]*normals[:,0,None]+s[:,:,None]*normals[:,1,None]+t[:,:,None]*normals[:,2,None]
    interpolated/=np.linalg.norm(interpolated,axis=2)[:,:,None]
    assert np.abs(interpolated-actual_normals).max()<=POSITION_TOLERANCE,'Retained top-fit original surface NORMAL changed'
    # A same-area wrong-side cut must not pass. Within each Z cell the signed
    # ceiling/base-plane distances are affine, so corners and every original
    # edge/profile-knot intersection cover each actual retained triangle.
    for tri in actual:
        points=list(tri)
        for a,b in zip(tri,np.roll(tri,-1,axis=0)):
            for z,_ in profile:
                if min(a[2],b[2])<z<max(a[2],b[2]):
                    points.append(a+(z-a[2])/(b[2]-a[2])*(b-a))
        for point in points:
            distance=(point[1]-ceiling(profile,point[2]))/math.hypot(1.,gradient(profile,point[2]))
            assert distance<=POSITION_TOLERANCE,'Retained top-fit facet remains above its declared ceiling'
            for normal,bound in base_planes:
                assert np.dot(point,normal)>=bound-POSITION_TOLERANCE,'Retained header escaped original leaf support'
    before,expected=expected_areas(source,profile,base_planes)
    areas=np.linalg.norm(np.cross(actual[:,1]-actual[:,0],actual[:,2]-actual[:,0]),axis=1)/2
    measured=np.zeros(len(source));np.add.at(measured,ids,areas)
    assert np.abs(measured-expected).max()<=AREA_TOLERANCE and abs(measured.sum()-expected.sum())<=AREA_TOLERANCE,'Top-fit per-original-facet area was lost, duplicated or changed'
    changed=np.flatnonzero(before-expected>1e-11).tolist()
    if expected_changed is not None:assert changed==expected_changed,'Top-fit changes escaped the exact declared original frame facets'
    untouched=[]
    for i in range(len(source)):
        if abs(before[i]-polygon_area(list(source[i])))>1e-11 or i in changed:continue
        rows=np.flatnonzero(ids==i)
        assert len(rows)==1,'Unchanged original frame facet was lost or retessellated'
        row=int(rows[0]);assert np.abs(actual[row]-source[i]).max()<=POSITION_TOLERANCE,'Untargeted original frame closed-WORLD POSITION changed'
        if expected_changed is not None:
            # Frame facets were copied whole before this proposal and retain
            # their exact NORMAL bytes. Header fragments already use the
            # original transferred-facet interpolation/roundoff contract above.
            assert np.asarray(actual_normals[row],dtype='<f4').tobytes()==np.asarray(source_normals[i],dtype='<f4').tobytes(),'Untargeted original frame NORMAL bytes changed'
        untouched.append(i)
    return {'actual_source_facet_count':len(source),'changed_original_source_facets':changed,
        'unchanged_original_facets_verified':untouched,'original_baseline_area_m2':float(before.sum()),
        'expected_retained_source_area_m2':float(expected.sum()),'actual_retained_source_area_m2':float(measured.sum()),
        'removed_declared_original_area_m2':float(before.sum()-expected.sum()),'original_facet_map_independently_checked':True}


def verify_stock(source,retained,actual_caps,profile,minimum_stock,minimum_cover):
    # Independent NEXT-ring extraction, actual four/eight-sided source topology.
    assert len(source)%14==0;sides=len(source)//14;assert sides in [4,8]
    flat=source.reshape((-1,3));rings=[];covered=set();centres=[]
    for i in range(7):
        previous=(i-1)%7;ring=np.array([flat[previous*sides*6+j*6+5]for j in range(sides)])
        assert len(np.unique(ring,axis=0))==sides
        for point in ring:assert tuple(point)not in covered;covered.add(tuple(point))
        centre=ring.mean(axis=0);centres.append(centre)
        for point in ring:
            if point[1]<=centre[1]+POSITION_TOLERANCE:
                assert np.linalg.norm(retained.reshape((-1,3))-point,axis=1).min()<=POSITION_TOLERANCE,'Top-fit removed protected lower/midline frame stock'
        low_z,high_z=float(ring[:,2].min()),float(ring[:,2].max())
        if not any(point[1]>ceiling(profile,point[2])+POSITION_TOLERANCE for point in ring):continue
        candidates=[]
        for tri in actual_caps:
            polygon=plane_clip(list(tri),np.array([0.,0.,1.]),low_z)
            polygon=plane_clip(polygon,np.array([0.,0.,-1.]),-high_z)
            candidates.extend(polygon)
        assert candidates,'Actual top-fit cap missing from original crest section'
        cap_min=float(np.asarray(candidates)[:,1].min())
        stock=cap_min-float(ring[:,1].min());cover=cap_min-float(centre[1])
        assert stock>=minimum_stock-POSITION_TOLERANCE and cover>=minimum_cover-POSITION_TOLERANCE,'Top-fit actual crest stock or glass-edge cover is too thin'
        rings.append({'source_ring':i,'source_sides':sides,'actual_cap_min_y_m':cap_min,
            'retained_vertical_stock_m':stock,'glass_edge_centre_cover_m':cover,
            'source_transverse_stock_m':float(np.ptp(ring[:,0]))})
    assert covered==set(tuple(p)for p in flat) and rings
    for a,b in zip(centres,centres[1:]+centres[:1]):
        probes=[a,b]
        for z,_ in profile:
            if min(a[2],b[2])<z<max(a[2],b[2]):probes.append(a+(z-a[2])/(b[2]-a[2])*(b-a))
        assert min(ceiling(profile,p[2])-p[1]for p in probes)>=minimum_cover-POSITION_TOLERANCE,'Top-fit leaves a thin rail/glass joint between source sections'
    return rings


def verify_caps(retained,cap,cap_normals,profile):
    edges=[]
    for tri in retained:
        points=[]
        for point in tri:
            d=abs(point[1]-ceiling(profile,point[2]))/math.hypot(1.,gradient(profile,point[2]))
            if d<=POSITION_TOLERANCE:points.append(point)
        assert len(points)<3,'Source facet unexpectedly replaces a new top-fit cap'
        if len(points)==2 and abs(points[0][2]-points[1][2])>1e-10:edges.append(points)
    assert edges,'Actual retained top-fit cut edges missing'
    for point in cap.reshape((-1,3)):
        distances=[]
        for a,b in edges:
            d=b-a;fraction=np.clip(np.dot(point-a,d)/np.dot(d,d),0,1)
            distances.append(np.linalg.norm(point-a-fraction*d))
        assert min(distances)<=POSITION_TOLERANCE,'Top-fit cap detached from actual retained source skins'
        assert abs(point[1]-ceiling(profile,point[2]))/math.hypot(1.,gradient(profile,point[2]))<=POSITION_TOLERANCE,'Top-fit cap escaped declared source ceiling'
    cross=np.cross(cap[:,1]-cap[:,0],cap[:,2]-cap[:,0]);length=np.linalg.norm(cross,axis=1)
    assert np.all(length>1e-12) and np.all(cross[:,1]>0),'Top-fit cap winding/area changed'
    normal=cross/length[:,None]
    assert np.abs(cap_normals-normal[:,None]).max()<=POSITION_TOLERANCE,'Top-fit cap NORMAL differs from actual triangle'
    stops=sorted(set([float(p[2])for edge in edges for p in edge]+cap[:,:,2].reshape(-1).tolist()+[p[0]for p in profile]))
    checks=0
    for lo,hi in zip(stops,stops[1:]):
        if hi-lo<=1e-10:continue
        for fraction in [.25,.75]:
            z=lo+fraction*(hi-lo)
            xs=[a[0]+(b[0]-a[0])*(z-a[2])/(b[2]-a[2])for a,b in edges
                if min(a[2],b[2])<z<max(a[2],b[2])]
            intervals=[]
            for tri in cap:
                points=[]
                for a,b in zip(tri,np.roll(tri,-1,axis=0)):
                    if min(a[2],b[2])<z<max(a[2],b[2]):points.append(a[0]+(b[0]-a[0])*(z-a[2])/(b[2]-a[2]))
                if points:assert len(points)==2;intervals.append((min(points),max(points)))
            if not xs:assert not intervals,'Top-fit cap bridges absent source material';continue
            assert len(xs)>=2 and intervals,'Top-fit actual cut was left uncapped'
            cursor=min(xs)
            for left,right in sorted(intervals):
                assert abs(left-cursor)<=POSITION_TOLERANCE,'Top-fit cap has an actual gap/overlap'
                cursor=right
            assert abs(cursor-max(xs))<=POSITION_TOLERANCE,'Top-fit cap misses original source thickness'
            checks+=1
    assert checks
    return {'actual_cut_edge_count':len(edges),'actual_cap_triangles':len(cap),'actual_cross_section_coverage_checks':checks,
        'normal_true_to_actual_triangles':True,'closed_occlusion_verified':False,'analytic_sweep_certificate':False}


def verify_connection(retained,cap,closed):
    """Actual positive-length shared edges, including clipped T junctions."""
    triangles=np.concatenate([retained,cap]);points=np.unique(triangles.reshape((-1,3)),axis=0)
    # Canonicalize only the existing Float32 position tolerance, never a broad
    # nearest-neighbour merge or a physical collision/contact epsilon.
    vertices=[];canonical=[]
    for point in points:
        matches=[i for i,p in enumerate(vertices)if np.linalg.norm(p-point)<=POSITION_TOLERANCE]
        if matches:canonical.append(matches[0])
        else:canonical.append(len(vertices));vertices.append(point)
    vertices=np.asarray(vertices);canonical=np.asarray(canonical)
    owners={};parent=list(range(len(triangles)))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for face,triangle in enumerate(triangles):
        for a,b in zip(triangle,np.roll(triangle,-1,axis=0)):
            d=b-a;length=float(np.linalg.norm(d));assert length>POSITION_TOLERANCE,'Top-fit created a sub-tolerance collapsed edge'
            t=(points-a)@d/np.dot(d,d)
            distances=np.linalg.norm(points-a-t[:,None]*d,axis=1)
            ids=np.flatnonzero((t>=-POSITION_TOLERANCE/length)&(t<=1+POSITION_TOLERANCE/length)&(distances<=POSITION_TOLERANCE))
            ordered=[]
            for i in ids[np.argsort(t[ids])]:
                value=int(canonical[i])
                if not ordered or value!=ordered[-1]:ordered.append(value)
            assert len(ordered)>=2
            for i,j in zip(ordered,ordered[1:]):
                if i==j:continue
                key=tuple(sorted((i,j)));owners.setdefault(key,[]).append((face,1 if i<j else -1))
    for rows in owners.values():
        if closed:assert len(rows)==2 and rows[0][1]!=rows[1][1],'Top-fit frame/cap is not closed with coherent shared edges'
        for face,_ in rows[1:]:parent[root(face)]=root(rows[0][0])
    assert len(set(root(i)for i in range(len(triangles))))==1,'Top-fit retained material/cap joint disconnected'
    return {'actual_connected_surface_components':1,'closed_shared_edges_required':closed,
            'actual_atomic_shared_edges':len(owners),'position_roundoff_tolerance_m':POSITION_TOLERANCE,
            'not_a_strength_or_occupant_proof':True}


def maximum_roof_removal(source,roof_profile,base_planes):
    maximum=0.
    for tri in source:
        polygon=list(tri)
        for normal,bound in base_planes:polygon=plane_clip(polygon,np.asarray(normal),bound)
        points=list(polygon)
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            for z,_ in roof_profile:
                if min(a[2],b[2])<z<max(a[2],b[2]):points.append(a+(z-a[2])/(b[2]-a[2])*(b-a))
        for point in points:maximum=max(maximum,float(point[1]-ceiling(roof_profile,point[2])))
    return maximum


def check_profile_scope(combined,roof,front_planes):
    # This only verifies the explicitly reviewed construction profile, NOT its
    # unproven swept-roof theorem. The actual complete SAT proof is mandatory.
    probes=sorted(set([p[0]for p in combined]+[p[0]for p in roof]))
    for z in probes:
        if z<combined[0][0]or z>combined[-1][0]:continue
        choices=[(ceiling(roof,z),gradient(roof,z))]
        for normal,bound in front_planes:
            ny,nz=normal[1],normal[2];assert ny<0
            choices.append(((bound-nz*z)/ny,-nz/ny))
        expected,m=min(choices,key=lambda row:row[0])
        delta=abs(ceiling(combined,z)-expected)/math.hypot(1.,m)
        assert delta<=POSITION_TOLERANCE,'Top-fit profile exceeds the reviewed roof/5mm-front scope'
    return {'reviewed_profile_scope_checked':True,'whole_domain_swept_ceiling_certificate':False}
