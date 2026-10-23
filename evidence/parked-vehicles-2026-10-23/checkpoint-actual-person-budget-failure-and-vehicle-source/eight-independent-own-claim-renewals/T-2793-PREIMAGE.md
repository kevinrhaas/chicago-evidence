---
id: T-2793
title: Build one articulated period wagon master from the existing wagon families
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
claimed_by: root continuing delegated people and transport delivery; independent renewal 10/22/2026, 7:49:48 PM CT
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: null
claimed_at: 2026-10-23T00:49:49.039Z
decision: null
decision_answer: null
---

## Checkpoint — 2026-10-23, 02:28 UTC

Root visually accepted finewoodV4B boundedmaterial increment; all4nativeA/BchecksPASS, originalstalepinFAIL retained. ModernCC0texturemaps are opticalanalogy, not historiccapture/species/maker evidence. Freshoriginalpipeline reproductionPASS7.642s. Current6ccombinedvehicle intake in1213 includes acceptedmaterial, awaiting canonicalprep/fullgate/worldqualification; photographic acceptance remains open. See HANDOVER.md and checkpoint-person-ci-green-and-combined-vehicle-intake for exact immutable evidence.


## Depends on

T-2792. Read each dependency before claiming; do not silently skip its proof.

## Scope and acceptance

Build **one** reusable articulated farm-box wagon master, as a bounded reconstruction for the earlier scene, retaining the existing wagon's documented provenance and proportions unless better evidence changes them explicitly. Covered/cart variants remain later follow-ups, not hidden acceptance.

- Read the existing 3.05 x 1.07 x 0.55 m reconstructed body and running gear in yard.js/data before changing it. Separate body, four wheels, front bogie/kingbolt, reach, tongue and hitch nodes; preserve correct axle/track and wheel clearance through a low-speed turn.
- Match a licensed construction reference and reviewed period analogue; wood grain, joinery, iron tires/hardware, paint wear and load attachments survive a close view without pretending colors or dimensions are attested.
- Produce canonical authored master + portable GLB/sidecar, license record and declared liberties. Supply neutral material variants within one bounded specimen, with compressed near/mid/far exports.
- Render close, side, front-three-quarter and distant views with a scale reference; compare against approved evidence and list remaining differences. Export/load it through the actual web path and measure budget.
- Existing 80 static wagons remain placed and operational; do not replace all of them or rebake unrelated buildings for this ticket.

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


## W01 visible refinement checkpoint, 2026-10-19

Reviewed original tapered octagonal spokes and1.2mm board/stave chamfers are integrated in the current combined source WIP, not yet committed. Exact bundle is saved alongside CHECKPOINT.md.9000→10792triangles,22mesh batches/47nodes and wheel bounds/pivots/socket frames unchanged; source wrapper regenerates exact reviewed GLB7749a0199b93bd196ecf6c3482af8ec537f1420a38f6fac88ab79fd8f34d44aa. Two-run determinism and independent Khronos0/0 passed on proposal bytes; controlled close/clay/mobile images were inspected. Full-view gain is modest; geometry cost and eventual LOD decision remain explicit. All dimensions/material variation are reconstructed engineering, no photographic/historical joinery acceptance. Combined full gate/commit pending; production ticket remains open.


## Measured progress — 2026-10-19 08:26 UTC

Combined PR1041 is committed and pushed at `f97ee94970385d35f469c449c6b111b0d8488057`, reconciled with dev c7770e99. Full local preflight passed 1,012 checks, and the remote required gate and canonical human workflow passed. The final 18-leg published desktop/mobile smoke matrix is running at that exact head; merge to dev remains conditional on all remaining checks and strict coverage. No production ticket closure. The separate C02 door/body portable package and actual browser proof remain saved for a later PR; construction/photo acceptance is still open.


## Measured progress — 2026-10-19 10:13 UTC

Saved implementation checkpoint512f4a7e3 is pushed, including reviewed C02 and devfb6a; fullpreflight1015/0 and postcommit checks pass. PR1041 remains draft: earlierf97 desktop13 failed draw331/330 and HUD31.23%/10; current targeted actual512f camera trace passes tint287,rowghost327,XRAY316 twice each, but does not reproduce331 or qualify wholematrix. HUDmeasurement correction is uncommitted under actualdiagnosis; no finalmatrix/merge yet. Wagon photographic/period/production acceptance remains open.


## Progress — 2026-10-19 14:20 UTC

Supported W01 bench and named-driver authoring are committed and pushed at `09a3ad1d4`; full local preflight passed 1,016 steps and the published bench passed desktop/mobile views. PR1041 remains draft while its 19 selected qualification runs complete. No photographic ticket closure.

Outside-app timber A/B candidate `9af2109f…` passed common-camera framing and geometry checks; root inspected actual desktop bench comparisons. Grain improves the flat baseline but remains broad/soft, and the full wagon still needs coherent wood, paint and iron detail. Eight actual captures are saved in `evidence/period-transport-2026-10-18/next-visible-parcels-2026-10-19/material-review-1420/`; the browser helper lacked a console listener, so console-error absence is unproven. Existing procedural maps have cleared project provenance; they are not photographic scans. A whole-wagon finish candidate is being developed outside the frozen release.


## Whole-wagon finish result — 2026-10-19 14:38 UTC

Outside-app filtered candidate `464e430d…` passed12actual desktop/mobile matched A/B captures, keeping23draw batches and an estimated6MiB decoded mapped texture memory with mipmaps. Root inspected the actual bench image: finer irregular grain improves the flat baseline, while photographic timber, cut ends/hubs and optical calibration remain open. Earlier48MiB and regular-comb candidates are preserved as unaccepted. An original bounded fastener refinement is now under development, with no changes to current release09a.


## Progress — 2026-10-19 15:42 UTC

Frozen09a is already pushed. PR1041 merge still blocked on remaining mandatory workflows plus contradictory required-step metadata in two otherwise successful jobs39266459095/39266463876. Aggregate, single refresh and direct immutable job details all retain published-test in_progress/postpending. Preserved evidence in github-backup-1542. No finalv6/merge/waiver. A source-only exacttwo-attempt2 freshqualification plan is being reviewed; no rerunPOST yet.


## Merge recovery — 2026-10-19 16:20 UTC

PR1041 is already pushed. Fresh GitHub reconciliation found 16 old-head workflows successful, one cancelled after90m22s, and two running. Meanwhile dev advanced to28c53 and introduced a real smoke HUD conflict. Root merged dev locally, preserving both navigatorDock and confLegend. Independent index review confirms no assets or liberties were lost. Existing dev also carries its150-minute smoke policy. Local preflight is running after restoring three stale ignored Glessner files from dev's verified package; no new application commit yet. Fresh checks must qualify the eventual updated SHA. Old two-rerun recovery authority is invalidated; no bypass/merge occurred. Durable evidence is pushed in backup commits8a066c58 and855e0378. Photographic acceptance remains open.


## Checked merge pushed — 2026-10-19 16:53 UTC

Resolved dev conflict is committed and pushed at `aedc80126c6178376d3fb60f40297bec5c7c9ec7` in PR1041. Full local preflight passed1,017checks/377 deliberate selftests; postcommit changelog/ID and104.28MB published mirror checks pass. Fresh remote SHA/tree and26code pins match; PR is mergeable with CI pending. One canonicalboth-flags run and18 smoke runs were dispatched once at this exact head; normal automatic CI remains required. One durable observer tracks them. No merge until actualgreen/final verifier; no source or assertion waiver. Photographic finish/LOD/period acceptance still open.


## Progress — 2026-10-19: pushed aedc branch, CI setup failure

PR1041 remains open and unmerged at pushed, clean aedc80126. Local full preflight passed 1,017 checks and 377 refusal self-tests. Canonical human build and auxiliary attempt2 passed. One selected smoke job failed Playwright installation before publication or application assertions; annotations establish exit1 but not its cause. Original failure is retained, no test waived, and a source-only once-only diagnostic recovery plan awaits review. Merge remains conditional on actual green checks and fresh exact-head/dev verification.


## Measured progress — 2026-10-19 20:55 UTC

Transport source f2f607b0 passed all18 selected published renderer workflows and5 normal workflows; final V10 source/job audit passed. A subsequent real conflict with dev a139 is resolved and independently audited across all15,933 index paths. Full local preflight is still running; the resolved merge is not committed or merged yet. Fresh full renderer qualification is planned for the changed runtime. No photographic or ticket acceptance is claimed.

Recovery: `evidence/period-transport-2026-10-18/CHECKPOINT.md`, current backup `github-backup-204639`. Ticket remains open; no status/claim/PR association changed by this evidence note.


## Final handover — 2026-10-19 22:40 UTC

Foundation landed: PR1041 actually merged into DEV at22:05:13UTC as cc79b6b19f5c87febb8199453ed0f1d4326dbd15. All18 selected desktop/mobile smoke workflows and4 automatic workflows passed on qualified25b9; final V11 PASS. Ordinary merge, no protection bypass or production promotion. This does not close photographic acceptance or wagon boarding/driving. W01/C02 study and portable human infrastructure are available in DEV; remaining optional refinements and limitations are listed in root HANDOVER.md.

Photographic/interaction acceptance remains open; this evidence note changes no ticket state or claim.

## Owner's covered-wagon follow-up — 2026-10-21

As better covered wagons become ready, replace the existing covered wagons with better covered-wagon models. Preserve the deliberate visual variety already present: upgraded vehicles must not read as clones. Inventory each selected original stand's identity, dimensions, orientation, material/wood/canvas variation and load details before replacement; carry distinct, stable variants into the new family rather than applying one identical mesh/finish everywhere. Keep type/date/source limits explicit. Unmeasured differences remain declared reconstruction, never invented manufacturer/model claims.

This is the owner's next-family direction. Covered variants remain a separate follow-up to this farm-box master's acceptance. Current T-2979/PR1174 replaces only three farm-box stands and retains the old covered wagons; it is not a covered-family completion. Future replacements should retain Light/far/load-failure fallback and earn actual photographic comparison and desktop/mobile scene acceptance.

**Released 2026-10-21** (claim of wagon-model agent 10/18/2026, 1:45:25 PM CT): Claims audit: reopen stale inactive work; reference and carriage work immediately reassigned individually for independent parallel completion

## Actual richer source-base inspection — 2026-10-22

One original licensed OldCart13600b73 source-native inspection passed7.96s with three fixed front/quarter/side PNGs,0clipped/0errors, original root/materials/geometry/hierarchy unchanged, caller/browser closed. Root personally viewed richer timbergrain/joinery/rims/hubs/steeredaxle. Compact proof ea4ecbea is GitHub-backed in evidence/parked-vehicles-2026-10-22/checkpoint-779-final-ci-and-rendering-followups/. It is a development base only: originalauthor provides NO maker/date/region/prototype, so no1835/Dearborn/Studebaker attribution or actual replacement accepted. Metriccalibration/periodanalogue/clearance/optimizedLOD/actualtown acceptance remain open. No broadwagon closure.


## Licensed close-view timber source candidate — 2026-10-22 23:40 UTC

External candidate atlasV2 is saved in `evidence/parked-vehicles-2026-10-22/checkpoint-wagon-atlas-and-active-horse-gate/`, archive SHA256 `18df56c8dd9b3eafc86b199da071819aee7b64fd0ba06b5789544dd86eb4cd23`. Actual bounded build and independent geometry/material readback pass:12,104triangles/23meshes/23primitives/6materialdefinitions, exact original position/normal/index/pivots/paint/iron/covered-variant pins.16,176 serialized UV samples retain the previous candidate's native surface values. Prior crop/gamut failures and the higher-draw V1 remain preserved in the previous checkpoint.

Only licensed modern timber pixels are transferred from Lyskilde/longtail's Old Cart, CC BY4.0; no donor geometry or purported historical maker/date is transferred. W01 remains a bounded reconstructed farm-box wagon, not an identified Dearborn. Original cut ends are disclosed project-authored material. Native donor crop145x40pixels does not establish photographic resolution. Atlas needs2576px texture support and dimension-estimated12,976,992bytes RGBA8+mips; GPU cost, coarser mip appearance, actual town near/far views and period/photo acceptance remain open. No active app replacement or broad ticket closure.


## Saved concrete delivery — 2026-10-22 23:54 UTC

Minimal external atlas intake patch41cfd8b5 is saved. ActualWebGL2renderer supportsNPOT/mipmaps but resizes oversizedimages, so patch passesactualmaxTextureSize and selects ORIGINAL fallback BEFOREcandidatefetch for missing/nonfinite/<2576caps. High/exact2576cap usescandidate;Lightfetchesneither;negativecontrol rejectsdisabledguard. ActualGLBsourcefixture merges5batches/9textures (not23appdrawcalls). Exactfresh-baseline appendbinder reproducesd65a4c and rejects3mutations; fullfreshproducerchain remainsunrun. EstimatedactiveRGBA8+mips12,976,992B,+6,685,308overbaseline, outsidebuildingresidencypool. NativeA/B/coarsemips/deviceGPU/photo acceptance remainOPEN; sourcepatchnotapplied.

Recovery: `evidence/parked-vehicles-2026-10-22/checkpoint-pushed-horse-and-concrete-model-intake/`. No broad ticket closure.


## Delivery checkpoint — 2026-10-23, 01:00 UTC

Root reviewed all four V4B native images and accepted a bounded finer timber material improvement over the flat tan baseline. Corrected capture passed5.46s with zero browser/GL errors and closed cleanup; stale source-pin attempt remains failed and saved. Fresh original wagon generation reproduces the candidate. Normal intake is assigned to the existing parked-vehicle PR1213; preserve GPL geometry/charts and CC0 modern PolyHaven pixel attribution. Repeated grain and faceted paint/iron remain; photographic master acceptance stays open. Recovery c33ae02d is in the newest evidence checkpoint.
