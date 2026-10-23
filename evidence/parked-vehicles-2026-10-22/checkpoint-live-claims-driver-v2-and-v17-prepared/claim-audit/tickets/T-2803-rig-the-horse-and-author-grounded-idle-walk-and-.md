---
id: T-2803
title: Rig the horse and author grounded idle, walk and trot clips
state: claimed
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2798
opened: 2026-10-18
closed: null
pr: null
claimed_by: root parallel team circuit: native horse gait agent 10/22/2026, 11:57:00 AM CT
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: null
claimed_at: 2026-10-22T16:57:01.550Z
decision: null
decision_answer: null
---

## Checkpoint — 2026-10-22, 18:34 UTC

Actualnormalizedfilteredidle c255 has385poseactualMixer+shadernorm proofPASS: all4hoofpatches+732lowerlimbvertices0drift, clocks/loop/clone/disposePASS, old6neverplayed. ConsumerpeerCLEAR; actualworldvisual/fullgate next. Separate03a1experimental26jointstaticrig passesformat/staticshape but haszeroanimation and gait/selfcontact/nativevisualOPEN.


## Checkpoint — 2026-10-22, 17:47 UTC

A first filtered head/tail idle derivative2f590ee3 exists outside app. Independent new-curve/structural checks pass; whole glTF validation FAILS with inherited90 errors/15900 warnings. Both complete reports and V2 failure/V3 source correction are preserved. Separate normalization SOURCE is under review, not executed. Actual Mixer/full-surface/visual and four-limb walk remain open.


## Depends on

T-2800. Begin bare-horse rigging independently; the gear-contact subgate waits on T-2801/T-2802 but does not prevent skeleton and gait work. Read each dependency before claiming; do not silently skip its proof.

## Scope and acceptance

Rig the first horse master and provide **idle, walk and trot** clips that work through the actual portable export and browser playback path. Canter/gallop and special tricks are later scope.

- Use a documented portable skeleton with anatomically plausible joint pivots, hoof controls, neck/head, ears and mane/tail solution; preserve skin weights through gait extrema.
- Specify clip names, speed/stride data and in-place versus root-motion contract. Walk/trot transitions match travelled distance, preserve grounded stance and avoid sliding, hyperextended joints or snapping at loop seams.
- Gear follows correct body/bit anchors; hitch mode leaves stable trace/shaft connection points. Demonstrate idle/start/walk/trot/stop and turning with synchronized rein endpoints.
- Export clips and rig through real GLB path, exercise browser AnimationMixer/LOD handling, show near and distance playback and measure update cost. No Blender installation on improve runner; use qualified bake pipeline.

## Shared requirements

Owner request, 2026-10-18: two epics below portable humans; inspect both research viewers and existing wagons; build photographic-quality period models first, then distant movement, riders/drivers, and eventually boarding/riding. Explicitly authorized parallel work. Implementation target is `kevinrhaas/chicago` **dev**; use the existing isolated checkout, no worktree unless requested.

- Keep 1812/1835, pre-fire (through 1871), and Prairie Avenue 1904 eligibility separate. Later images may support a labeled period analogy, never establish earlier Chicago presence. Do not call the Pullman-location carriage Pullman-owned without evidence.
- Resolve every implementation source ID in `data/sources/`; distinguish attested, inferred with reasoning, and bounded reconstruction. Unknown dimensions/color/breed do not block a defensible reconstruction; record bounds and liberties. Never promote a guess to attested.
- Text citation of rights-pending sources is permitted; assets must not be derived from them. Every shipped asset/input carries license provenance. Prefer project-authored or institutionally cleared references and no paid acquisition without owner authorization.
- Photographic quality is an acceptance target, not a status label. Compare actual renders against dated source views at matched cameras, record discrepancies and what is hidden/inferred. Do not close on a placeholder silhouette or unseen screenshot. Keep black-and-white sources distinct from reconstructed color.
- Canonical deliverables follow the existing portable export pipeline: authored masters where supported, glTF/GLB + engine-neutral JSON, metres and explicitly tested axes, licensed materials and near/mid/far LODs. No Blender installation on the improve runner; mark `needs_bake` honestly.
- Preserve existing placed static wagons; route/actor integration is additive. Existing camera horse/wagon paces do not count as a rendered animal/vehicle or a working riding interaction.
- Measure GLB/texture bytes, triangles, draw calls, texture memory and frame cost for the selected desktop/mobile specimen. Reuse materials and population budgets; do not regress the phone memory work above this band.
- Rider/driver work reuses portable humans and follows the owner's current depiction rulings (T-2672); isolated test fixtures can validate attachments before scene release. No invented named likenesses, dialogue or ceremonies.

## Evidence

Read `evidence/period-transport-2026-10-18/carriages.md`, `horses.md`, and `viewer-survey.md`. They distinguish pixel inspection from metadata, record coverage and rights, and explain external archive access blockers. The Prairie visual pass was targeted, not all 944 source records were visually reviewed. Read the master specifications as they are added; they are a first-pass design, not proof of finished models.

## Parallel checkpoint — 2026-10-19

Additive grounded engineering trot integrated into app WIP, exact regeneration and bare-horse browser sole checks pass. Clip dropdown reads actual duration/stride. Transition/stop blend FAILED actual sole -22.9mm; world-foot IK replacement in progress outside app. No riding/hitch-trot acceptance. See evidence/period-transport-2026-10-18/parallel-refinement-2026-10-19/ and CHECKPOINT.md. PR1041 remains draft; conditional dev merge awaits green final-head gates.


## Latest measured checkpoint — 2026-10-19 04:52 UTC

Grounded trot and loop-continuous preview are committed at PR1041 finalcandidate e1b31c070. World-foot IK stop/start/change work is now an OUTSIDE portable20-clip proposal plus exact10-phase stop references. Stable finite-player source archive09de08f and corrected browser evidence53932072 are saved centrally:30 finite cases x101 actual poses passed desktop AND mobile numerical and recovery/lifecycle checks; original first-RAF negative-delta failure is retained, with corrected short actual-RAF/captures passing. Unchanged sole guards remain strict. Starts/gaitchanges route through neutral, not direct constant-speed blends. Arbitrary-phase/turning/occupied/tack/hitch-trot acceptance and app integration remain open.

Durable inputs, failed receipts and current recovery instructions: `evidence/period-transport-2026-10-18/CHECKPOINT.md` and `parallel-refinement-2026-10-19/` beneath that evidence directory. This progress update does not change the ticket state or production acceptance.

**Released 2026-10-21** (claim of parallel horse gait 10/18/2026, 10:07:00 PM CT): Claims audit: reopen stale inactive work; reference and carriage work immediately reassigned individually for independent parallel completion


## Owner priority and parallel checkpoint — 2026-10-22, 17:13 UTC

Owner explicitly expects natural standing shifts rather than frozen figures. Native horse clips fail as walk/rest idle; safe head/tail-only idle and independent-limb rerig/gait work are being prepared, with contact/animation/browser acceptance pending. Recovery: `evidence/parked-vehicles-2026-10-22/checkpoint-b092-pushed-and-natural-idle-teams/`.
