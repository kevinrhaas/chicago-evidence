# SPDX-License-Identifier: GPL-3.0-or-later
"""Frozen-source engineering pose controls; no app or canonical master mutation."""
import copy,json
from pathlib import Path
from seated_clothing_correction import correct
D=Path(__file__).resolve().parent
old=json.loads((D/'inputs/original-pose.json').read_text())['bone_global_head_rotation']
new=json.loads((D/'inputs/corrected-source-pose.json').read_text())['bone_global_head_rotation']
positive,_=correct(old,.01408)
assert positive==new
under,_=correct(old,.0138)
lift=copy.deepcopy(old)
for p in lift.values():p['head_m'][1]+=.01408
(D/'POSE-CONTROLS.json').write_text(json.dumps({'baseline':old,'corrected':new,'under_raise':under,'whole_asset_lift':lift},indent=2)+'\n')
print('Exact saved positive source pose reproduced; under-raise and whole-lift controls generated')
