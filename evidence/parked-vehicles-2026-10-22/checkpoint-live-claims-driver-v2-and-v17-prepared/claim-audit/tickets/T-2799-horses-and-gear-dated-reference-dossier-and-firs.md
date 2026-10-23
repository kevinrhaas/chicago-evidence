---
id: T-2799
title: Horses and gear: dated reference dossier and first master specification
state: done
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2798
opened: 2026-10-18
closed: 2026-10-21
pr: 1174
claimed_by: horse reference and master handoff agent 10/21/2026, 9:57:57 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-22T04:16:26Z
claimed_run: null
claimed_at: 2026-10-22T02:57:58.286Z
decision: null
decision_answer: null
group: T-2792,T-2799
---

## Scope and acceptance

Turn the actual photo audit into a first horse + tack master specification that can be modeled next.

- Inventory any existing horse meshes/rigs, human actor reuse, route affordances, camera-only travel modes and scene depiction gates, with exact code paths. A speed option is not a horse model.
- Build a dated source register for working teams and riding horses, harness versus saddlery, coat/anatomy and seating/reins. Record visible details versus inference, source rights, crop IDs and dates. Do not infer breed, ownership, color or precise team count from unclear pixels.
- Review clear Chrimes carriages, Smith ice team, Harvey-frontage carriage, disputed Glessner-location harness photo and earlier Sauganash drawings. Keep retrospective drawings separate from photographs and later evidence separate from 1835 eligibility.
- Write `horse-master-spec.md` with one bounded horse choice, physically scaled anatomy, source tiers, material detail, portable skeleton/gaits, tack anchors, rider/driver interfaces and matched-view/LOD acceptance. Reconcile axes/metres and hitch interfaces with T-2792.
- Record external archive denials and precise next sources to inspect; provide concrete modeling handoff without calling unvisited references verified.

## Work started

The horse agent has saved the implementation and seven-image audit in `horses.md` and has saved the initial master specification in parallel with T-2792; source/rights clearance and production validation remain outstanding. Viewer survey adds a larger targeted review with exact coverage.

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

**Bounded reference review, 2026-10-21:** Eight candidate families reviewed; recommendation and saved source/license/anatomy evidence in checkpoint-2118/horse-reference-review-pack.tar.gz (6211caeb). BlueMesh draft-horse actual public preview is strongest, CC BY4 declared,200080faces/4Ktextures/0anims; normal asset download HTTP401 so no mesh acquired. HenryS lighter animated candidate also401. No access controls bypassed. Current procedural anatomy remains photographically inadequate; no placement. CC0 living anatomy and public-domain structural plates acquired for original refinement. Modern anatomy references do not attest historical breed/gear/owner.

**Released 2026-10-21** (claim of root parallel people vehicles and horses completion 2026-10-22 10/21/2026, 9:56:46 PM CT): Claims audit: reopen stale inactive work; reference and carriage work immediately reassigned individually for independent parallel completion

## Active parallel completion — 2026-10-22 03:04 UTC

Assigned to horse reference and master handoff agent; reconcile stale no-mesh statements against actual current horse/rig/harness and complete the reference/specification acceptance before anatomical master production. See `WORKPLAN-PEOPLE-TRANSPORT.md` for current owners and dependency order.

## Completed research acceptance — 2026-10-22

All five research/specification clauses have reviewed deliverables: exact current horse/rig/harness/runtime inventory, dated inspected source register, explicit period versus later/modern analogy limits, executable horse-master specification and concrete source/rights/model handoff. The actual current horse is715316bytes/14172triangles/6draws/15joints; harness is602980bytes/8012triangles/36parts. These remain procedural fixtures. Sixteen source frames were actually viewed, including direct Moore1891 light-buggy harness and trace dimensions, separate English-coach collar/hames and riding-saddle engraving. Modern CC0 anatomy does not attest an1835 breed, coat or tack.

App docs horse-master-spec.md/.json, horse-reference-register-20261022.json and source records are integrated in staged treec0b314187a80cbcf8cc115ffeec8f400386b827e for PR1174; full gate retry is running after ordinary Kinzie-derived package repair. Mark review only after successful gate and actual app push. Master geometry/photographic coat/hair, tack fit, animation, world placement and riding remain open. T2800 next source-only draft is outside the app and awaits a fresh exact installed-baseline visual comparison.
