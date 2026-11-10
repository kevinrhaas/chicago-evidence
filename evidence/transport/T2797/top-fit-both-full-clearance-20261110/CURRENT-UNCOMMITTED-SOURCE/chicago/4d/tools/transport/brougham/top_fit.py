# SPDX-License-Identifier: GPL-3.0-or-later
"""Unqualified ordinary moving-door fit; no source roof/glass modification.

Only source facets intersecting the declared top profile are clipped. The
analytical swept-envelope certificate is explicitly UNPROVEN; the complete
actual SAT proof remains mandatory, with its original depth and tolerance.
"""
import math
import numpy as np


def height(profile, z):
    p=np.asarray(profile,dtype=float)
    if not p[0,0]-1e-7<=z<=p[-1,0]+1e-7:
        raise ValueError('Top-fit coordinate outside its source-bound profile')
    i=max(0,min(len(p)-2,int(np.searchsorted(p[:,0],z,side='right'))-1))
    a,b=p[i:i+2]
    return float(a[1]+(z-a[0])*(b[1]-a[1])/(b[0]-a[0]))


def slope(profile,z):
    p=np.asarray(profile,dtype=float)
    i=max(0,min(len(p)-2,int(np.searchsorted(p[:,0],z,side='right'))-1))
    a,b=p[i:i+2]
    return float((b[1]-a[1])/(b[0]-a[0]))


def combine_front_planes(profile, support_planes):
    """Minimum of the roof profile and two explicit inset-header halfplanes."""
    stops=[float(p[0])for p in profile]
    for (lo,_),(hi,_)in zip(profile,profile[1:]):
        m=slope(profile,(lo+hi)/2);b=height(profile,lo)-m*lo
        lines=[(m,b)]
        for row in support_planes:
            ny,nz=row['inward_normal_yz'];bound=row['source_bound']+row['moving_inset_m']
            if ny>=0:
                raise ValueError('Expected only the two ordinary front-upper profile planes')
            lines.append((-nz/ny,bound/ny))
        for i,(a,b)in enumerate(lines):
            for c,d in lines[:i]:
                if abs(a-c)>1e-12:
                    z=(d-b)/(a-c)
                    if lo<z<hi:stops.append(z)
    result=[]
    for z in sorted(set(stops)):
        ceilings=[height(profile,z)]
        for row in support_planes:
            ny,nz=row['inward_normal_yz']
            ceilings.append((row['source_bound']+row['moving_inset_m']-nz*z)/ny)
        result.append([z,min(ceilings)])
    return result


def points_for_triangle(triangle,profile):
    """Actual source corners and edge/profile-knot intersections, no sampling."""
    points=list(triangle)
    for a,b in zip(triangle,np.roll(triangle,-1,axis=0)):
        for z,_ in profile:
            if min(a[2],b[2])<z<max(a[2],b[2]):
                t=(z-a[2])/(b[2]-a[2]);points.append(a+t*(b-a))
    return points


def affected(triangle,profile):
    return max(float(p[1])-height(profile,float(p[2]))for p in points_for_triangle(triangle,profile))>1e-10


def clip_polygon(polygon,normal,bound):
    if not polygon:return []
    result=[];previous=polygon[-1];pd=float(normal@previous[:3]-bound)
    for current in polygon:
        cd=float(normal@current[:3]-bound)
        if (pd>=0)!=(cd>=0):result.append(previous+pd/(pd-cd)*(current-previous))
        if cd>=0:result.append(current.copy())
        previous,pd=current,cd
    return result


def triangulate(polygon):
    for i in range(1,len(polygon)-1):
        tri=np.asarray([polygon[0],polygon[i],polygon[i+1]],dtype=float)
        if np.linalg.norm(np.cross(tri[1,:3]-tri[0,:3],tri[2,:3]-tri[0,:3]))<=1e-12:continue
        lengths=np.linalg.norm(tri[:,3:],axis=1)
        if (lengths<1e-10).any():raise ValueError('Undefined retained source normal')
        tri[:,3:]/=lengths[:,None]
        yield tri


def retain_source(data,profile):
    kept=[];origins=[];changed=[];ranges=[]
    for source_id,tri in enumerate(data):
        begin=len(kept)
        if not affected(tri[:,:3],profile):
            kept.append(tri.copy());origins.append(source_id)
        else:
            changed.append(source_id)
            for (lo,_),(hi,_)in zip(profile,profile[1:]):
                if tri[:,2].max()<lo or tri[:,2].min()>hi:continue
                polygon=clip_polygon(list(tri),np.array([0.,0.,1.]),lo)
                polygon=clip_polygon(polygon,np.array([0.,0.,-1.]),-hi)
                m=slope(profile,(lo+hi)/2);b=height(profile,lo)-m*lo
                polygon=clip_polygon(polygon,np.array([0.,-1.,m]),-b)
                pieces=list(triangulate(polygon));kept.extend(pieces);origins.extend([source_id]*len(pieces))
        ranges.append({'source_triangle':source_id,'first_retained_triangle':begin,'retained_triangles':len(kept)-begin})
    return np.asarray(kept).reshape((-1,3,6)),{'source_triangle_for_retained':origins,
        'changed_source_triangles':changed,'source_ranges':ranges,'not_independent_geometry_proof':True}


def encoded_local(data,pivot):
    result=data.copy();result[:,:,:3]-=pivot
    return np.asarray(result,dtype='<f4').astype(float)


def edge_caps(encoded,pivot,profile):
    """Close only actual encoded cut skins; no invented backing across a hole."""
    world=encoded[:,:,:3]+pivot
    edges=[]
    for tri in world:
        boundary=[]
        for p in tri:
            distance=abs(p[1]-height(profile,p[2]))/math.hypot(1.,slope(profile,p[2]))
            if distance<=2e-7:boundary.append(p)
        if len(boundary)==3:
            raise ValueError('Original source facet unexpectedly coplanar with proposed cut')
        if len(boundary)==2 and abs(boundary[0][2]-boundary[1][2])>1e-10:
            edges.append(tuple(sorted(boundary,key=lambda p:p[2])))
    if not edges:raise ValueError('No actual top-fit cut skins')
    stops=sorted(set(float(p[2])for edge in edges for p in edge));caps=[]
    for lo,hi in zip(stops,stops[1:]):
        if hi-lo<=1e-10:continue
        active=[(a,b)for a,b in edges if a[2]<=(lo+hi)/2<=b[2]]
        if not active:continue
        if len(active)<2:raise ValueError('Unpaired actual top-fit cut skin')
        def ends(z):
            points=[a+(z-a[2])/(b[2]-a[2])*(b-a)for a,b in active]
            return min(points,key=lambda p:p[0]),max(points,key=lambda p:p[0])
        a,b=ends(lo);d,c=ends(hi);quad=np.array([a,b,c,d])
        outward=np.array([0.,1.,-slope(profile,(lo+hi)/2)])
        if np.dot(np.cross(quad[1]-quad[0],quad[2]-quad[0]),outward)<0:quad=quad[::-1]
        for ids in [[0,1,2],[0,2,3]]:
            # Normals belong to the actual serialized triangle, including any
            # tiny nonplanarity introduced by source Float32 cut intersections.
            positions=np.asarray(quad[ids]-pivot,dtype='<f4').astype(float)
            normal=np.cross(positions[1]-positions[0],positions[2]-positions[0]);length=np.linalg.norm(normal)
            if length<=1e-12:continue
            # A strip can narrow to one point, making the first quad cross
            # zero. Orient each surviving encoded ceiling triangle itself.
            if normal[1]<0:
                positions=positions[[0,2,1]]
                normal=np.cross(positions[1]-positions[0],positions[2]-positions[0])
                length=np.linalg.norm(normal)
            normal/=length
            caps.append(np.concatenate([positions,np.tile(normal,(3,1))],axis=1))
    if not caps:raise ValueError('No nondegenerate top-fit closure')
    return np.asarray(caps),{'source_cut_edges':len(edges),'cut_z_partitions':len(stops)-1,'cap_triangles':len(caps),
        'actual_sweep_qualified':False,'closed_occlusion_verified':False}
