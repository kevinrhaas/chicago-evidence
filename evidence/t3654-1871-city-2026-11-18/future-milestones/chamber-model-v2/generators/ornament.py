"""Original, parameterized exterior relief inferred from the two cleared drawings.

No external meshes, image textures, or claims of exact carving profiles. Coordinate
operations use the host emitter's facade frame and explicitly reconstructed depths.
"""
import math


def _area(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def extrude(face,mesh,points,depth,thickness=.18):
    """Ear-clip a simple concave silhouette, then emit its depth edges."""
    pts=list(points)
    signed=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1]))
    if signed<0:pts.reverse()
    remaining=list(range(len(pts)))
    while len(remaining)>3:
        for j,b in enumerate(remaining):
            a=remaining[j-1];c=remaining[(j+1)%len(remaining)]
            if _area(pts[a],pts[b],pts[c])<=1e-9:continue
            inside=False
            for k in remaining:
                if k in (a,b,c):continue
                if min(_area(pts[a],pts[b],pts[k]),_area(pts[b],pts[c],pts[k]),_area(pts[c],pts[a],pts[k]))>=-1e-9:
                    inside=True;break
            if not inside:
                face.poly(mesh,[pts[a],pts[b],pts[c]],depth);remaining.pop(j);break
        else:raise ValueError('Non-simple or degenerate ornament silhouette')
    face.poly(mesh,[pts[k]for k in remaining],depth)
    for a,b in zip(pts,pts[1:]+pts[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1]
        hint=tuple(face.along[i]*dy+(0,-dx,0)[i] for i in range(3))
        mesh.face([face.p(*a,depth),face.p(*a,depth-thickness),face.p(*b,depth-thickness),face.p(*b,depth)],hint)


def turned(face,mesh,s,depth,profile,segments=24):
    """Turn a positive-radius vertical profile: columns, balusters and urns."""
    for (y0,r0),(y1,r1) in zip(profile,profile[1:]):
        for i in range(segments):
            a=2*math.pi*i/segments;b=2*math.pi*(i+1)/segments
            points=[face.p(s+r*math.cos(t),y,depth+r*math.sin(t)) for y,r,t in [(y0,r0,a),(y0,r0,b),(y1,r1,b),(y1,r1,a)]]
            mid=(a+b)/2
            hint=tuple(face.along[k]*math.cos(mid)+face.out[k]*math.sin(mid)+(0,-(r1-r0)/(y1-y0),0)[k] if y1!=y0 else (0,1 if r1<r0 else -1,0)[k] for k in range(3))
            mesh.face(points,hint)
    for y,rad,normal in [(profile[0][0],profile[0][1],(0,-1,0)),(profile[-1][0],profile[-1][1],(0,1,0))]:
        mesh.face([face.p(s+rad*math.cos(i*2*math.pi/segments),y,depth+rad*math.sin(i*2*math.pi/segments)) for i in range(segments)],normal)


def urn(face,mesh,s,base,depth,scale=1):
    profile=[(0,.23),(.12,.23),(.15,.16),(.28,.14),(.44,.24),(.64,.29),(.82,.24),(.91,.14),(1.00,.13),(1.05,.20),(1.14,.20),(1.22,.11),(1.32,.035)]
    turned(face,mesh,s,depth,[(base+y*scale,r*scale)for y,r in profile],20)


def crown(face,mesh,s,head,rise,depth):
    # Broad foot, tapered carved shaft and projecting cap. Flanking scrolls are
    # bounded silhouette reconstruction, not a claimed recovered carving.
    outline=[(-.36,.13),(.36,.13),(.43,.42),(.30,.66),(.19,rise-.33),(.29,rise-.20),(.24,rise),(-.24,rise),(-.29,rise-.20),(-.19,rise-.33),(-.30,.66),(-.43,.42)]
    extrude(face,mesh,[(s+x,head+y)for x,y in outline],depth,.26)
    for sign in [-1,1]:
        scroll=[(.26,.40),(.57,.43),(.91,.14),(.91,.49),(.71,.81),(.50,1.02),(.32,.87)]
        extrude(face,mesh,[(s+sign*x,head+y*min(1,rise/1.6))for x,y in scroll],depth-.07,.16)
    face.block(mesh,s-.31,s+.31,head+rise-.20,head+rise-.07,depth+.07,back=depth-.10)
    face.block(mesh,s-.14,s+.14,head+.53,head+rise-.32,depth+.065,back=depth-.08)


def shaped_panel(face,mesh,profile,base,depth,hole,thickness=.28):
    """Vertical strips follow the apron top and leave a real elliptical opening."""
    cx,cy,rx,ry=hole
    xs=sorted(set([p[0]for p in profile]+[cx+rx*math.cos(i*math.pi/40)for i in range(41)]))
    def roof(x):
        for a,b in zip(profile,profile[1:]):
            if a[0]-1e-8<=x<=b[0]+1e-8:return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
        raise ValueError('Panel sample outside profile')
    def cut(x):return ry*math.sqrt(max(0,1-((x-cx)/rx)**2))
    for a,b in zip(xs,xs[1:]):
        if b-a<1e-8:continue
        ta,tb=roof(a),roof(b)
        if abs((a+b)/2-cx)<rx:
            la,lb=cy-cut(a),cy-cut(b);ua,ub=cy+cut(a),cy+cut(b)
            face.poly(mesh,[(a,base),(b,base),(b,lb),(a,la)],depth)
            face.poly(mesh,[(a,ua),(b,ub),(b,tb),(a,ta)],depth)
        else:face.poly(mesh,[(a,base),(b,base),(b,tb),(a,ta)],depth)
    outline=[(profile[0][0],base),(profile[-1][0],base)]+list(reversed(profile))
    for a,b in zip(outline,outline[1:]+outline[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];hint=tuple(face.along[k]*dy+(0,-dx,0)[k]for k in range(3))
        mesh.face([face.p(*a,depth),face.p(*a,depth-thickness),face.p(*b,depth-thickness),face.p(*b,depth)],hint)
    circle=[(cx+rx*math.cos(i*2*math.pi/64),cy+ry*math.sin(i*2*math.pi/64))for i in range(64)]
    for a,b in zip(circle,circle[1:]+circle[:1]):
        mid=((a[0]+b[0])/2,(a[1]+b[1])/2);hint=tuple(face.along[k]*(cx-mid[0])+(0,cy-mid[1],0)[k]for k in range(3))
        mesh.face([face.p(*a,depth),face.p(*b,depth),face.p(*b,depth-thickness),face.p(*a,depth-thickness)],hint)
