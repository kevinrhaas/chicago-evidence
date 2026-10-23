"""Pinned authored candidate Ra/Rd; unexecuted, not measured motion/acceptance."""
from pathlib import Path
import json, math
import numpy as np
from walk_source_ORIGINAL import path, PARAMETERS

SPEC=json.loads((Path(__file__).parent/'RECONSTRUCTED-ANATOMY-AND-PROFILE-INPUTS.json').read_text())['profile']


def rx(theta):
    c,s=math.cos(theta),math.sin(theta)
    return np.array([[1.,0.,0.],[0.,c,-s],[0.,s,c]])


def reviewed_orientations(t,label):
    # "reviewed" here means source-authored coefficients explicitly documented;
    # it does not mean measured anatomy, reachable poses or qualified motion.
    delta,stance,phase=path(t,PARAMETERS['phase_offsets'][label])
    amplitude=math.radians(SPEC['nominal_proximal_excursion_deg'][label])
    theta_a=-amplitude*delta[2]/(PARAMETERS['stride_m']*PARAMETERS['stance_fraction']/2)
    assert abs(theta_a)<=amplitude*SPEC['proximal_guard_multiple_of_nominal'], 'No proximal amplitude clamp/fallback'
    if stance:
        u=phase/PARAMETERS['stance_fraction']
        angle=SPEC['stance_extension_deg'][label]
    else:
        u=(phase-PARAMETERS['stance_fraction'])/(1-PARAMETERS['stance_fraction'])
        angle=SPEC['unloaded_flexion_deg'][label]
    theta_d=math.radians(angle)*64*u**3*(1-u)**3
    return rx(theta_a),rx(theta_d)
