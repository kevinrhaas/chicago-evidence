# First portable horse master: bounded reconstruction specification

Status: reviewable design deliverable, 2026-10-18. No horse model, texture, animation, machine-readable contract or runtime implementation has been produced by this document. Proposed targets below are engineering/design choices, not measurements of a historical horse. Source acquisition and rights resolution remain prerequisites to reference-derived production geometry. Companion: `vehicle-master-spec.md` in this directory.

## First master and evidence boundaries

Proposed asset ID: `equine_light_harness_reconstructed_01`. First deliverable is one generic adult light-harness horse in a neutral standing pose, suitable for a single-horse open-carriage fixture. It is not a named Chrimes horse, Pullman horse, particular breed, or attested 1904 individual. Start with a medium light-harness body rather than asserting that the heavier ice-wagon team and carriage horses share identical conformation. A future draft-body variant needs its own anatomy evidence. Riding tack is a separate fitted assembly, not evidence this harness horse was ridden in a particular scene.

Author original anatomy only after acquiring a rights-cleared equine reference set with side/front/rear/head/hoof views and dimensions; alternatively obtain a reusable licensed master and verify all derivative permissions. Until then implementers can make a clearly synthetic dimensional fixture in an unpublished test page, with no geometry or texture derived from unresolved images. Historic photographs listed below are text-cited leads at present. Do not use their pixels as texture, photogrammetry input, direct tracing or derived production asset while rights remain unresolved. No source ID is minted here; registry IDs below refer to existing research catalog records, not necessarily `4d/data/sources` IDs.

A production reconstruction must record its anatomical basis, period gear sources, exact source IDs, license, author, authored-master path and liberty entry. Separate body shape, coat/markings, age/sex, tack and placement confidence. Unknown coat color and unseen surfaces remain reconstructed; sepia values are not RGB evidence.

## Frame and pipeline compatibility

Inspected authorities: `chicago/chicago/4d/docs/GLB-CONTRACT.md`, `docs/HUMAN-ASSET-CONTRACT.md` §§2, 7–10; `tools/human_export.py` and `tools/human_export.sh`. Human exporter uses `export_yup=True`, `export_extras=True`, animations and a checked master/web derivative pair. It validates a humanoid skeleton; it must NOT be run unmodified as if a horse satisfied that contract.

- Canonical master: authored Blender file and original licensed textures; glTF binary 2.0 browser derivatives are rebuilt by command. Future engine exports come from that same master.
- Metres baked into vertices; Y-up, right-handed; forward +Z; horse's anatomical left +X. All scene/armature/bone node scales are 1 in the uncompressed master; outward CCW normals. No world ENU offsets baked into mesh.
- Root origin at ground level below the midpoint between front/hind hoof support centers in rest stance, centered laterally. Root remains fixed during in-place clips. Origin is not the saddle position.
- Scene placement: ENU east → +X, north → −Z, up → +Y; heading clockwise from grid north, actor yaw `π − heading_deg × π/180`, matching portable humans. Heading 0 faces −Z/north after placement. Structure facade yaw differs; never reuse it for this actor.
- Vehicle agent confirmed identical metre/Y-up/+Z-forward and actor yaw conventions; vehicle origin is ground at axle midpoint. Therefore couple by full named socket transforms, not equal root coordinates. Wheel axles are X in the companion spec.
- Proposed equine scene-extra namespace `chicago4d_equine`, versioned independently of `chicago4d_human`; bone and clip names stable across equine LODs. This is a proposal requiring an actual schema/validator ticket before production export.
- Reuse the existing Meshopt derivative pattern and compare decoded derivatives to their uncompressed masters. Do not silently add Draco, unlit material or other untested extensions. Equine texture extensions must be checked against the current renderer rather than copied from the narrower human extension allowlist.

## Dimensional reconstruction targets

All values in this table are proposed fixture bounds, not historical claims. Replace with a measured licensed reference before photographic model acceptance. Dimensions describe a relaxed adult stance; head movement changes the overall bounding box.

| Measurement | Proposed first fixture target | Gate and confidence |
|---|---:|---|
| Ground to withers | 1.55 m | reconstructed target ±0.02 m; never label breed/individual attested |
| Point of shoulder to buttock, horizontal | 1.60 m | reconstructed target ±0.04 m; record landmark definitions |
| Trunk breadth at widest measured section | 0.55 m | reconstructed target ±0.04 m; requires front/rear reference |
| Hoof-ground plane in neutral stance | y = 0 | four hoof contact markers within 2 mm of plane |
| Root scale | 1,1,1 | reject centimetre models and unapplied nonuniform scale |
| Saddle/seat/bit/trace heights | measured after modeling | no fabricated universal numeric anchor; store actual transform per fitted gear |

Do not nonuniformly scale one skeleton to turn it into a draft animal. Keep a dimension/landmark table for each body; compare profile, neck-to-shoulder transition, scapular region, withers, barrel, croup, joints, pasterns and hoof angles against the chosen measured source. Hoof soles, eyelid contact and mouth/bit contact need close inspection. Anatomical left/right and fore/hind labels must survive export.

## Materials and close-up quality

Required proposed slots: `equine_coat`, `equine_eyes`, `equine_hooves`, `equine_mane_tail`; optional muzzle/mouth slot only when its separation is justified. Gear: `tack_leather`, `tack_metal`, optional cloth/felt. PBR metallic-roughness, correct color-space handling, physically scaled detail and UV texel-density report. Coat/skin/hoof/leather remain dielectric; buckles/bit material depends on sourced metal, not generic chrome. Model eyelids, eye wetness and hoof edges so they hold up at close range without baked directional highlights. Hair cards or geometry need stable silhouettes, alpha/depth and shadow review on mobile; use a simpler far representation.

Proposed first texture ceilings: coat up to 4096² at lod0; up to 2048² at lod1; up to 1024² at lod2; up to 512² at lod3, with packed normal/roughness/occlusion textures where supported. These are ceilings and must be replaced or ratified by decoded-memory measurements; a 4K texture is not itself evidence of photographic quality. Budget loaded textures separately from shipped compression. Do not ship four duplicate texture sets if they can share/cache suitable maps. Fine texture may not disguise wrong anatomy or silhouette.

## Equine skeleton, clips and root motion

Proposed skeleton name `c4d_equine_v1`; separate contract from the 56-bone humanoid. Minimum semantic chains: ground `root`; pelvis/spine/withers/chest; neck chain/head/jaw; paired eyes/ears; four limbs labeled `fore_l`, `fore_r`, `hind_l`, `hind_r` with anatomically appropriate segments and hoof controls; tail chain. Rigging ticket must pin complete parentage and actual names before authoring reusable clips. Avoid a knee-like hind limb invented from a humanoid rig. Maximum four normalized skin influences per vertex; every LOD retains the complete contract skeleton even where weights simplify.

Clip names lower snake case: required `idle`, `walk`; next `trot`, `start_walk`, `stop_walk`, `turn_left`, `turn_right`; later `canter_left`, `canter_right`, `gallop` only when sourced movement and gameplay needs justify them. Idle variations may use suffixes. They are equine verbs; adding them does not extend the current humanoid verb grammar.

All clips are **in place**, matching human contract policy: no root translation or yaw accumulation. Runtime actor controls world movement and heading. A locomotion clip carries proposed extras `speed_m_s`, `cycle_duration_s`, `stride_m`, `foot_contacts` (named limb plus normalized phase ranges), gait/lead and loop status. Require `speed_m_s × cycle_duration_s` to agree with `stride_m` within 1% as an engineering consistency check; values come from measured motion reference, not travel.js's interface speed. Report authored and runtime playback rate and allowed speed range. Large speed variation needs another clip/blend, not unlimited playback scaling.

First acceptance: flat-ground idle/walk/trot without foot skate; correct source-supported footfall order; continuous contact and no obvious hyperextension; start/stop/turn transitions; body/saddle rider motion evaluated together. Proposed gate: a planted hoof drifts ≤20 mm per contact phase in fixture world space; neutral four contacts within 2 mm; loop root difference ≤1 mm and 0.1°; record any gait-specific exceptions. These are target tolerances requiring validation, not existing passing tests. Terrain-aware hoof placement is a subsequent runtime capability, not a GLB promise.

## Gear and coupling sockets

Socket naming proposal uses `socket_equine_*` for horse-side anchors, `socket_vehicle_*` for vehicle-side anchors. Pin position, rotation, parent bone and role in metadata; +Z points in the local travel-forward direction in rest pose, +Y up, +X anatomical left. A moving socket follows its parent bone; role-specific target orientation may additionally be stored. Never infer harness fit from a bounding box.

Required semantic anchors: `socket_equine_bit_l/r` on head; `socket_equine_saddle` on back; `socket_equine_rider_seat` from the fitted saddle; `socket_equine_stirrup_l/r` from riding gear; `socket_equine_trace_l/r`, `socket_equine_breeching_l/r` and `socket_equine_shaft_l/r` from fitted draft harness; optional breastcollar/collar and pole/yoke coupling anchors when the historically sourced configuration needs them. Not every source depicts every anchor or harness type. Do not combine collar, breastcollar, breeching, shafts and pole fittings into a universal unhistorical kit.

Riding and driving gear are independently removable/fitted assets with body compatibility and temporal/provenance records. Fitting records store rest offsets, clearance envelope and allowed adjustments; hide body/gear intersections only with documented masks, not arbitrary deletion. Single-horse shafts and paired-team pole/traces are separate configurations. Verify full harness load path and stops/turns; attachment sockets alone do not simulate tension.

For the first single-horse fixture, assemble the prototype vehicle's coupling socket to the horse's fitted harness frame by composing inverse/forward transforms; retain a measured horse-to-vehicle separation and shaft lateral clearance. Vehicle wheel rotation derives from travel distance. A pair team later needs independent left/right horse transforms, pole clearance, traces and individual gait phase; never substitute a doubled mesh with coincident skeletons. Companion vehicle spec owns axle, wheel and hitch frame details.

## Portable-human rider and driver plan

Preserve humanoid skeleton `c4d_humanoid_v1`; do not parent equine bones into it. Drive a separate human actor from the fitted saddle's rider-seat transform; retain independent humanoid pose/animation and person identity. `socket_hand_l/r` already exist in the human contract. Pose rider hands to rein targets near the bit, feet to fitted stirrup targets, pelvis to seat; the rein curve connects targets with controlled slack/tension. A carriage driver sits on vehicle seat sockets and uses the same rein-end semantics; driver seat is not the horse saddle.

Existing humanoid state `seated`/clip verb `sit` can seed a fixture pose, but rider/driver poses, stirrup reach, reins and gait synchronization need new authored clips or a formally extended human contract. No claim they already exist. Test varied human body sizes against one horse/seat instead of scaling the horse to each rider. Avoid clipping at thigh/saddle, boot/stirrup, hand/rein and torso/vehicle. Proposed close-up target: hand-to-grip and boot-to-stirrup contact error ≤10 mm in seated neutral pose; record dynamic error throughout motion.

Prototype with the existing anonymous CI human fixture on an unpublished page. Scene display remains governed by L1 and review flags independently of engine capability. This spec neither lifts the policy nor assigns an invented historical rider. Later mount/dismount needs approach anchors, state ownership, occupancy, safe ground exit and recovery; camera travel mode alone is not mounting.

## Export, LOD and photographic comparison gates

Four proposed files `<asset_id>.lod0.glb` through `.lod3.glb`, complete compatible skeleton, material semantic slots and gear anchors at all levels. Full uses lod0–3; balanced lod1–3; light lod2–3, following existing detail-tier convention. Proposed initial triangle ceilings for horse body excluding separate tack: 60k / 25k / 8k / 2k. These are unmeasured starting budgets; record actual triangles, vertices, draws, bones, texture decoded bytes, shipped bytes and GPU/CPU/frame timings for horse alone, hitched unit and rider combination. Do not weaken a quality gate by quietly changing the ceiling; justify measured revisions. Measure LOD distance thresholds rather than inheriting human thresholds blindly for larger silhouettes.

Required export review: parse all GLBs; no missing buffers/textures, skin joints or animations; stable names and provenance; all source IDs resolve; asset license entry; no `check_required` source used for derived assets. Compare decoded web derivative to uncompressed master: rest frame within 2 mm, socket positions within 2 mm and same hierarchy/metadata; compare sampled animation at contact/transition times, not rest only. All gate results currently **not run**.

Photographic review starts only with an eligible reference source. Record exact source image/crop, rights decision, camera intrinsics/extrinsics, pose, illumination, and masks for known/unknown/occluded regions. Use side/front/three-quarter render pairs at fixed camera, with neutral-light material turntables separately; source color unknown stays unknown. Proposed review targets: annotated visible landmark reprojection RMS ≤1% of horse image height, maximum ≤2%; visible silhouette intersection-over-union ≥0.95 after camera/pose registration, with mask and measured values saved. These targets do not establish quality on their own: reviewer must inspect side-by-side for joint shapes, head/muzzle/eyes, mane/tail, hoof contact, tack thickness/fittings and implausible highlights. Never tune camera to conceal a mismatch or claim unseen surfaces match a source. A model remains open when visible mismatches remain despite numeric scores.

Browser fixture must run at 1280×800 and 390×780 with zero page errors, source/derivative parity and detail switching. Include standing, moving, stop/turn, close-up tack, distant street and seat/rein-contact captures. Explicitly measure moving actors with animation throttled at distance: holding a frozen walk pose while translating is not acceptable distant movement. Frame-time/heap results and population limits are outstanding implementation measurements, not certified here.

## Unresolved reference registry

| Existing research record | What it offers | Unresolved limitation and next action |
|---|---|---|
| `a19-gh-clarke-wabash-chrimes` | closest clear local side-view horse/harness and occupied open-carriage photograph inspected | after June 1872, exact date unresolved; rights unknown/link-only; original courtesy Clarke House Museum. Left turnout team count disputed by initial readers. Obtain primary high-resolution record/terms, then annotate independent silhouettes; do not claim pair count yet. |
| `a16-ghm-blog-1736-mcbirney-c1890` | c1890 J. P. Smith & Co. ICE wagon and visibly two horses | bounds 1885–1895, holder unknown, rights unknown/link-only. Find original and company/catalog evidence; suited to separate draft-body research, not proof of light-harness anatomy. |
| `a20-glessner-2100-block-east-side-1890s` | enclosed carriage/horse street silhouette | 1890s caption only, original/rights unknown; too small for close anatomy. Seek original. |
| `a19-chm-ichi66015-west-side-north-from-allerton` | c1905 distant horse-drawn traffic context | CHM no-known-restrictions wording accompanied by reproduction licensing request; existing registry keeps link-only. Confirm terms and precise location before reuse. |
| `trowbridge_sauganash_hotel` in 4D source registry | retrospective saddled horse at post; pre-fire subject | undated plate, no direct 1835 observation; `check_required`, cross-check only. Text-cite; resolve original/date/rights and avoid treating as independent photographic anatomy. |

Exact local paths, catalog URLs, visible observations and date fields are in `horses.md`. No rights-cleared anatomical/motion reference has yet been acquired by this agent. No historical named individual or breed has been established. No production horse master may be marked reference-matched from this specification alone.
