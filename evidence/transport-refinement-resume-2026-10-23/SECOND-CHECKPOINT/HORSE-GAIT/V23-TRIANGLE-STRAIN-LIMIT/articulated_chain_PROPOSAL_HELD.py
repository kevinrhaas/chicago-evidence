"""One constrained short-walk diagnostic; longer proximal closure, coherent distal chain.

Unchanged root/foot targets and original authored pastern profile.  The former
prescribed proximal profile is explicitly replaced by IK.  This constrained study
is not a claim of normal fetlock load transfer or a certified natural gait.
"""
import math
import numpy as np
from walk_source_ORIGINAL import PARAMETERS, THRESHOLDS, path, unit, arc


def pose_articulated(t,pivots,limbs,hoof_min_y,reviewed_orientations):
    xyz=pivots.copy();xyz[1:,1]-=PARAMETERS['body_lowering_m']
    rot=np.repeat(np.eye(3)[None],len(pivots),axis=0)
    states={}
    for label,row in limbs.items():
        a,b,c,d,e=row['joints']
        _,rd=reviewed_orientations(t,label)
        assert rd.shape==(3,3) and np.isfinite(rd).all()
        assert np.max(np.abs(rd.T@rd-np.eye(3)))<=1e-12
        assert abs(np.linalg.det(rd)-1)<=1e-12
        delta,stance,phase=path(t,PARAMETERS['phase_offsets'][label])
        delta[1]-=hoof_min_y[label];target=pivots[e]+delta
        # Keep distal cannon and pastern coherent to avoid a new relative
        # rotation across the short, thick original fetlock skin transition.
        distal=rd
        fetlock=target-distal@(pivots[e]-pivots[d])
        carpus=fetlock-distal@(pivots[d]-pivots[c])
        old_a=pivots[b]-pivots[a];old_b=pivots[c]-pivots[b]
        l1,l2=np.linalg.norm(old_a),np.linalg.norm(old_b)
        line=carpus-xyz[a];distance=np.linalg.norm(line)
        if not abs(l1-l2)<distance<l1+l2:
            raise ValueError(f'Unreachable proximal closure {label}; no clamp/fallback')
        direction=unit(line)
        # Both existing proximal rest bends have positive anterior component;
        # select that canonical sagittal hemisphere, rather than a near-straight
        # fore section-centre lateral offset.  Choice is reconstructed.
        anterior=np.array([0.,0.,1.])
        projected=anterior-direction*(anterior@direction)
        if np.linalg.norm(projected)<=1e-8:
            raise ValueError('Undefined proximal sagittal pole; no fallback')
        pole=unit(projected)
        along=(l1*l1-l2*l2+distance*distance)/(2*distance)
        height=math.sqrt(max(0,l1*l1-along*along))
        elbow=xyz[a]+along*direction+height*pole
        xyz[b],xyz[c],xyz[d],xyz[e]=elbow,carpus,fetlock,target
        rot[a],rot[b],rot[c],rot[d]=arc(old_a,elbow-xyz[a]),arc(old_b,carpus-elbow),distal,distal
        states[label]={'stance':stance,'phase':phase,'target_local_m':target.tolist(),
                       'reach_margin_m':float(l1+l2-distance)}
    matrices=np.repeat(np.eye(4)[None],len(pivots),axis=0)
    matrices[:,:3,:3]=rot;matrices[:,:3,3]=xyz
    return matrices,states
