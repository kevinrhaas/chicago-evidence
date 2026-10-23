# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit Bardwell/W01 seated trouser-envelope retention; no default LOD change.

The source opt-in retains the already authored LOD1 trouser reduction at LOD2/3.
Existing measured engineering derivatives establish a useful candidate, never a
canonical Blender regeneration or GPU/visual/occupied driver acceptance claim.
"""
import hashlib,json,math
from pathlib import Path

def load_policy(profile_path,variant,recipe):
    profile_path=Path(profile_path)
    profile=json.loads(profile_path.read_text())
    rows=[r for r in profile.get('resident_bindings',[]) if r.get('asset_id')==variant.get('id')]
    if len(rows)!=1:raise ValueError('exactly one seated resident binding required')
    row=rows[0];policy=row.get('driver_contact_lod')
    if policy is None:return None
    if (profile.get('scene')!='1835' or profile.get('vehicle_variant')!='wagon_w01_driver_bench_study'
        or variant.get('id')!='bardwell_otis_1835' or variant.get('person_reference_scene')!='1835'
        or variant.get('person_reference_id')!='rc_bardwell_otis' or row.get('person_reference_id')!='rc_bardwell_otis'):
        raise ValueError('contact LOD retention is only the existing reconstructed1835 Bardwell/W01 study')
    if (policy.get('id')!='bardwell_w01_seated_trouser_lod1_floor_v1' or policy.get('enabled') is not True
        or policy.get('mesh_kind')!='trousers' or policy.get('source_lod')!=1 or policy.get('target_lods')!=[2,3]
        or policy.get('requires_pose_correction')!='bardwell_w01_seated_clothing_clearance_v1'
        or policy.get('live_driver_qualified') is not False):
        raise ValueError('unreviewed seated contact LOD policy')
    relative=Path(row['pose_draft_file'])
    if relative.name!=str(relative):raise ValueError('pose must be a sibling filename')
    pose_path=profile_path.parent/relative;raw=pose_path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row['pose_draft_sha256']:raise ValueError('contact LOD pose hash stale')
    correction=json.loads(raw).get('clothing_correction',{})
    if correction.get('id')!=policy['requires_pose_correction'] or correction.get('raise_pelvis_and_trunk_m')!=.01408:
        raise ValueError('retained envelope requires the measured fixed-foot source correction')
    ratios=recipe.get('lod_ratios')
    if ratios!=[1.0,.6,.28,.12]:raise ValueError('LOD ratios changed; repeat contact/cost qualification')
    return {'id':policy['id'],'asset_id':variant['id'],'person_reference_id':'rc_bardwell_otis','scene':'1835',
            'mesh_kind':'trousers','source_lod':1,'target_lods':[2,3],'minimum_ratio':ratios[1],
            'pose_sha256':row['pose_draft_sha256'],'live_driver_qualified':False,
            'status':'Explicit canonical-source candidate; Blender export, appearance and GPU/world costs require actual qualification'}

def garment_ratio(kind,lod,ordinary,policy):
    if policy is None or kind!='trousers' or lod not in policy['target_lods']:return ordinary
    if not isinstance(ordinary,(int,float)) or not math.isfinite(ordinary) or not 0<ordinary<=1:
        raise ValueError('finite positive existing garment reduction required')
    return max(ordinary,policy['minimum_ratio'])
