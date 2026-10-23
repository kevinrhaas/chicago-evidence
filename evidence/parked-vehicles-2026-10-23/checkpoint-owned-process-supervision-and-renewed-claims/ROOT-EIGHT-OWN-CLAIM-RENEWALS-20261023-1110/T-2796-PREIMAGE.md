---
id: T-2796
title: Move horse-drawn traffic through distant streets with measured LOD budgets
state: claimed
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2791
opened: 2026-10-18
closed: null
pr: null
claimed_by: root continuing delegated people and transport delivery; independent renewal 10/23/2026, 3:32:57 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: 2026-10-23T08:32:57.904Z
decision: null
decision_answer: null
---

## Delivery progress — 2026-10-23 10:14 UTC

PR #1175 merged to DEV (fffae74c7); its resident, timber wagons, distinct canvas and Brougham are delivered. PR #1213 closed as superseded after full63-path containment. Standing horse is applied on currentDEV e4745b3 in a separate branch; actual canonical owners, measured unit and isolation checks pass; fullpreflight and actual published app verification are next. Broad photographic, gait, complete gear, occupied teams and riding acceptance remain open. Full current source and actual merge/owner receipts are GitHub-checkpointed; see HANDOVER.md.


## Current delivery checkpoint — 2026-10-23 09:39 UTC

503m circuit/controller remains saved and inactive. Combined parked resident/vehicle PR1175pushed7d98638 with freshCI active. Accepted standing horse loaded129PASS now available for app integration; walking teams,fullgear,driver,swept clearance and traffic qualification remain open.

## Current delivery checkpoint — 2026-10-23, 08:19 UTC

The saved 503 m route and controller remain inactive. Work now supplies the prerequisite standing-horse asset and actual trace geometry, while walking skin, complete tack and driver fit remain unqualified. No circuit, boarding or riding activation is claimed.

[Full recovery and next steps](../HANDOVER.md). The existing root claim remains active.


## Checkpoint — 2026-10-22, 17:47 UTC

Frozen route source/capsule backed:503.190m/667.787s Randolph east→Clark north→Lake west→LaSalle south,17m corners within8-degree steering. Worked-earth/ROW/dry/obstacle coarse checks pass; worn7m core mask FAIL−3.600m is preserved. Explicit reconstructed-shoulder/corridor ruling and actual animated swept-bound/world/mobile proof still required.


## Depends on

T-2795, T-1792. Read each dependency before claiming; do not silently skip its proof.

## Scope and acceptance

Add a bounded first route with **one** period-correct horse-drawn vehicle in the distance, then a small capped population using the same path. It must visibly move in the actual selected scene, not just in a fixture.

- Use road masks/route affordances rather than sidewalk pedestrian paths; respect scene date, stopped/turning behavior, street crossings, building and static-wagon collision proxies.
- Distance LOD and animation update tiers share mobile budgets with portable humans; do not spawn new full-resolution textures per animal/vehicle. Test culling, return to near view, pause and reduced-motion choice without popping into collisions.
- Keep stable selection/dossier identity and source/liberty metadata; no unsupported daily schedule, owner or named driver is invented.
- Show the same street view before/after with moving vehicle, screenshots/video and measured phone/desktop p95, bytes and memory. A real browser functional test must demonstrate route progress and correct hitch motion.

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


## Current traffic pricing constraint — 2026-10-19

The complete split fresh diagnostic covers 36 unique rows: six stands, three tiers and two viewports. Light's worst readings are 1,154,091 triangles and 89 draw calls. Its strict limits remain 1,190,000 triangles and 90 calls; the general 330-call budget does not override Light's separate floor. Only one call and 35,909 triangles remain at the sampled worst.

These measurements contain no new town humans or moving traffic. Full/balanced repricing buys no unmeasured future actors. Before adding traffic, measure shared materials, instancing, LOD costs and actual savings, then qualify complete published desktop/mobile coverage. Existing placed static wagons remain intact. See [the complete pricing receipt](../evidence/period-transport-2026-10-18/ci379-and-transport-repairs/combined36.md).

## Parallel checkpoint — 2026-10-19

Outside-app deterministic distant-transport prototype prepared with route/LOD/admission tests. Actual asset draw cost exceeds current Light headroom; no main-scene placement/production acceptance. See evidence/period-transport-2026-10-18/parallel-refinement-2026-10-19/ and CHECKPOINT.md. PR1041 remains draft; conditional dev merge awaits green final-head gates.


## Paired street study result — 2026-10-19 14:55 UTC

Corrected responsive source passed actual desktop/mobile study checks: both horses and wagon visible, actual canvas/aspect/disclaimer and projected framing checked. Each enabled batch adds one draw and39,136triangles; all12off/on/restored counter rows pass. Actual GPU transform-feedback comparison against independent source checks all46,880vertices at six times, maximum world-component difference0.0000568m. Local finished-frame timings are study measurements, not phone/main-scene capacity proof. Root inspected actual mobile and route images.

The earlier mobile crop failure remains preserved. Archive `79b82d0c…` is saved in actual-progress-1455. No fitted harness, yoke, traces or driver; Full/Balanced rebudget is a proposal only, Light refuses, and no main-scene admission or photographic completion is claimed.

**Released 2026-10-21** (claim of continuing parallel period transport team 10/19/2026, 1:49:28 PM CT): Claims audit: reopen stale inactive work; reference and carriage work immediately reassigned individually for independent parallel completion


## Owner priority and parallel checkpoint — 2026-10-22, 17:13 UTC

Owner prioritizes first repeating team circuit before population expansion/player riding. Actual finite route/controller work is underway with fixed steering, road/ROW/terrain/static-obstacle bounds; no live moving-team or phone acceptance yet. Recovery: `evidence/parked-vehicles-2026-10-22/checkpoint-b092-pushed-and-natural-idle-teams/`.


## Checkpoint — 2026-10-22, 19:44 UTC

Active source extension is checking continuous provisional rigid-team clearance and dry worked-earth shoulders within correct ROW; no widened wear mask or moved historic geometry. Existing worn7mcore failure remains visible. Full actual animated horse/harness sweep and world/phone proof remain open.
