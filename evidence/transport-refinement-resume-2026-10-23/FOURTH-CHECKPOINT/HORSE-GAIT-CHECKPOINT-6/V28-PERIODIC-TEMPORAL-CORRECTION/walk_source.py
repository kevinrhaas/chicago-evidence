"""HELD reconstructed articulated walk; same original targets/timing/limits."""
from walk_source_ORIGINAL import PARAMETERS,THRESHOLDS
from articulated_chain_PROPOSAL_HELD import pose_articulated
from reconstructed_profiles_HELD import reviewed_orientations

def pose(t,pivots,limbs,hoof_min_y):
    return pose_articulated(t,pivots,limbs,hoof_min_y,reviewed_orientations)
