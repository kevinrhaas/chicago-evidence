---
id: T-3041
title: Match the first Fort Dearborn buildings against every reference picture
state: claimed
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: T-2387
opened: 2026-10-22
closed: null
pr: null
claimed_by: run 11/4/2026, 12:08:04 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41782312201
claimed_at: 2026-11-04T06:08:04.715Z
decision: null
decision_answer: null
---

Match the first Fort Dearborn buildings against every reference picture.

Piece 2 of 2 of **T-2387 — Match the first Fort Dearborn (1812) to its pictures, every building in it**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## SPLIT WHILE WORK STOOD ON THE PARENT

When T-2387 was split (2026-10-22T22:45:49.575Z), this was already on it. Read it before you claim this piece, and check the PR list for a branch that has already taken it:

- claim — taken 1m ago, run 10/22/2026, 5:44:36 PM CT — held by the run that split it
- branch `steward/t2387-t2388-fort-reference-groups` — the splitter's own

The run that split it (by hand) may be working one of the pieces now.

**Acceptance:** Meet the full image acceptance retained on parent T-2387: inspect every listed picture, solve cameras for the appropriate dated form, refine all pictured fort components, render before/after comparisons from current assets, and satisfy the Image gate without unresolved visible differences. Include all 21 named records and account for nine additional extant first-fort context records; rendering context alone does not attest it. Preserve surveyed coordinates and document conflicting retrospective evidence.

## Image gate
- first_fort_dearborn_blockhouse_nw

## Picture-review checkpoint — 2026-10-22

Group support is T-3040. First preserve the documented plan and 75 ft staff while reconciling retrospective tower locations. Both blockhouses carry invented separate chimneys absent from panel 1; removing them is a bounded possible refinement after before/after baking. Whistler's 1808 'not yet built' note establishes absence then, not continued absence in 1812. Later completion may be inferred from the retrospective panel with explicit dated provenance; this is not an owner-approval blocker.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of first-fort picture matching agent (frame_final_review) 10/23/2026, 7:19:37 AM CT): Wrap-up handoff: original 21 named records plus 9 context members and every listed picture remain unfinished. Exact 16-export BUILD, nine actually viewed same-camera compound comparisons (all differ, none accepted), independent 1884/1902 PD source proposals and remaining source blockers are archived at https://github.com/kevinrhaas/chicago-evidence/blob/516ab9e/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md ; small tickets pointer a526b46f. Proposed sources remain unapplied, held Getty check_required retained, and Earle unnumbered-plate citation clarification is archived. Resume from closed manifests without moving the surveyed plan or 22.86 m staff. Parent T-2387 remains split; no image-match completion claimed.

## Owner ruling on the Currey 1912 bird's-eye — 2026-11-03 (T-3335)

The bird's-eye (held as library `early-currey-1912-first-fort-birdseye`; camera and match record at `data/reference_views/first_fort_dearborn_pickets_outer/currey_1912_birdseye.*`, PR 1638) was compared building by building. Kevin chose to adopt from it:

- blockhouse cupolas (a small square lookout under its own pyramid cap) on both blockhouses — Whistler 1808 also drew them, "not yet built" then;
- a barrel-vaulted roof on the magazine (Whistler's arched front);
- a pyramid roof on the north-east small house;
- the western gateway / wicket gate beside the north-west blockhouse (the drawing's no. 3; Quaife: 'near the northwestern blockhouse'; Whistler index no. 8).

Keep Whistler's measured plan for everything else (owner ruling): blockhouse proportions, the main gate as a gap between the barracks halves (no gate building), range functions and lengths, chimneys. Those rows are `owner ruling` on the match record; do not rebuild toward the drawing there.

## Exact native-worker roof handoff — 2026-11-03

This remains the existing T-3041 piece of original T-2387. The bounded next increment is ONLY the north-east small house's pyramid roof adopted by the owner from Currey on 2026-11-03. It is partial; the full first-fort picture gate stays unfinished. No new photo follow-up, split, done--pr or forced completion is authorized by this handoff.

Read the [closed current-source readiness and native implementation plan](https://github.com/kevinrhaas/chicago-evidence/blob/a16454e4f5425e94e124526624559019bc52ec12/evidence/first-fort-2026-11-03/native-ne-roof-readiness-current42b/RECOVERY.md), its ROOT-REVIEW.md, READINESS-AUDIT.json and actual Currey image before editing. Fresh coordinator source readback at 42b9c601d51d8a93cde2706e1773f0bd00fadfbe confirms the target record, existing producer/parameter files, licensed source and current canonical view/match agree with that packet. Reassess actual current dev when the worker starts.

Keep first_fort_dearborn_small_house_ne an outbuilding. Add an opt-in pyramid branch locally in outbuilding.py and outbuilding_params.py, with supported triangular roof covering and level wall-top handling. Preserve every existing gable/shed default, the complete below-eave body, walls/materials, 0.86 by 1.88m batten front door and existing rear vent. Do not migrate to fort_structure/quarters: its facade machinery changes those features. Keep Whistler's measured fort plan and all seats/bearings unchanged. The current 3.72 by 3.05m footprint, 2.4m wall and 34-degree working roof pitch are retained reconstructed controls, not new measurements from the retrospective plate. Resolve eaves/overhang without sky gaps; refuse unsupported pyramid+loft/chimney/open-side combinations rather than altering old defaults. Keep helper changes local: no shared mesh/emit recipe change.

Changing the outbuilding producer reaches **243 existing outbuilding assets** in the authenticated current manifest. Before the FIRST geometry-source commit, genuinely generate and qualify every affected current MASTER and applicable variant on pinned Ubuntu26.04 / SHA-verified Blender4.5.3 in bounded native batches. Use the actual affected roster; no predicted/manual freshness hashes. Byte-identical regenerated MASTERs may retain genuinely bound existing WEB derivatives; actual changed outputs require encoding. Preserve every foreign registry row, including Green Tree's selected closed shoulder/current 0b53 model and the independent active Jail frame-family work. The Jail run41734994705 owns T-2380/frame_dwelling271 and is not this task; do not modify its run, topic or claim.

Use the existing fourteen-member Currey camera anchored on first_fort_dearborn_pickets_outer, scene1812, for actual before/after native comparisons. Its group already contains the NE house; replacing that GLB invalidates the old group binding and requires a fresh genuine render. Keep the diagnostic fit and surveyed plan fixed. Mark only the adopted NE roof difference fixed after direct visual confirmation; other roofs, cupola, magazine and west-gate gaps remain OPEN. Retain owner-ruling history. If the now-adopted house identity is verified, adding it to this picture's card_members and updating the former exclusion note is an optional credited Images improvement, not blanket attestation of fort context.

Root reviewed [platform draft PR219](https://github.com/kevinrhaas/polecat-platform/pull/219), exact feature commit aa9d7d2322d3abbc78d72526146c018a241c643e on steward/chicago-native-exact-ticket-20261103. Both source CI check runs and the official fifteen-case both-viewport smoke passed; the dedicated native-authoring job is literal Ubuntu26.04,150minutes, using the existing pinned Blender cache. Platform main stays unchanged. Coordinator authorizes only one exact target_ticket=T-3041 feature-definition dispatch after this handoff is synchronized/released and fresh ownership is free; no unrelated queue fallback or second Jail dispatch. No worker has been dispatched by this handoff yet.

All four source-check parts must pass BEFORE the first geometry-source commit. Keep every native command bounded below600seconds, record actual phase/variant rows and parity, preserve assertions/light-tier budgets, and retain checkpoints. After actual builds/owners: normal dev PR, actual published1812 desktop1280x800 AND phone390x780 roof/body/Images/Record/ground/entry checks with zero page errors, appropriate existing smoke, truthful current model/photo/camera bindings, current hosted green gate and ordinary exact-head protected merge. The150minute authoring budget is a budget, not a claimed bake/pass or completion promise.

Ship a checked partial roof improvement and release T-3041 OPEN with remaining differences and recovery links. Parent T-2387 remains split/unfinished. Never direct-push dev/main, weaken assertions, invent dimensions/source/rights, run local-host Blender or call done--anyway.

**Released 2026-11-03** (claim of Codex first-fort NE native handoff 2026-11-03 11/3/2026, 5:21:15 PM CT): Reviewed bounded NE-pyramid native handoff published; OPEN for authorized exact T3041 worker. No geometry applied, worker dispatch or full original completion claimed by this metadata handoff.

**Released 2026-11-03** (claim of run 11/3/2026, 5:38:59 PM CT, by https://github.com/kevinrhaas/polecat-platform/actions/runs/41739288717): Partial increment shipped as PR #1685 (open, labelled resume, green checks on its head, conflicted with a dev that moved under it): the north-east small house's pyramid roof, adopted from the Currey 1912 bird's-eye on the owner's 2026-11-03 ruling, with an opt-in pyramid branch in the outbuilding archetype and all 243 affected outbuilding masters regenerated on pinned Blender 4.5.3. That is ONE of the thirteen differences on data/reference_views/first_fort_dearborn_pickets_outer/currey_1912_birdseye.match.json, now marked fixed. STILL OPEN there: the blockhouse cupolas, the magazine's barrel vault and the western gateway, plus the whole original acceptance (21 named records, 9 context records, every listed picture). Verdict stays differs; parent T-2387 stays split and unfinished. Recovery: PR https://github.com/kevinrhaas/chicago/pull/1685, docs/STATUS.md T-3041, docs/LIBERTIES.md L-first-fort-ne-house-pyramid-3041.

**Released 2026-11-03** (claim of codex fort-parade-presence continuation 11/3/2026, 9:30:52 PM CT): PR1696 merged normally to dev as818be0cb: bounded parade-presence accounting repair, actual1812positiveground/cards both and1835nativeStage3both107/0; original first-fort all-buildings/picture acceptance remains PARTIAL and OPEN, roof body deferred. No new photo ticket or image completion. Source/current8gate/merge proof and runtime recovery: https://github.com/kevinrhaas/chicago/pull/1696 ; https://github.com/kevinrhaas/chicago-evidence/blob/d2d1a4203849bc597338d6a08a1cbd7da0727a6d/evidence/first-fort-2026-11-04/pr1696-runtime-closed-pass/RECOVERY.md . Later Cobweb scene carry is explicit in PR, not a new1835browser execution.


## Native magazine vault handoff — 2026-11-04

PREP ONLY / UNQUALIFIED. Root must review this handoff, external patch and controller before any ticket claim, app edit, dispatch or native job. No host Blender/GPU: Jail currently owns host runtime. This is NEW work on existing T-3041, parent T-2387, not a resume PR and never a new photo ticket.

Deliver ONE visible correction: replace the first-fort magazine's reconstructed gable with the vault form the owner adopted in T-3335/T-3041. Original remains OPEN/PARTIAL. Do not claim the whole fort matches, close the original, split it, or create follow-ups.

### Immutable candidate and upstream dependency

External patch SHA256 `661b69b2c544c73af8745be7f5b55bc142f3e2d338f6abd19a6cf8fddf4f17f5`, three files, 11,985 bytes. Immutable raw patch: https://raw.githubusercontent.com/kevinrhaas/chicago-evidence/55a51a17a1abf95bcfbe7097973d10f0a6c7adb6/evidence/first-fort-2026-11-04/magazine-vault-prep-unqualified-raw/UNQUALIFIED-CANDIDATE.patch . Fetch/hash it; rawsource/images share that commit. No app edits.

The patch COMPOSES with live Cupola PR1687 head `52d6f631df788258a50a6e3271cca9e97ba960ac`, not old dev's pre-cupola producer. Exact producer/params/data/output blob guards are in the controller and manifest. Cupola PR1687 MUST merge and current dev must contain its reviewed producer/data/physical output before native work, unless root explicitly plans a truly combined native build. Do not race or overwrite its live producer. If merged source differs, STOP and rebase/review the external patch; do not use fuzzy context or overwrite a newer producer.

### Picture and chronology, not new metric evidence

Read the actual supplied images, not just this prose. Whistler's January 25, 1808 measured draught shows the magazine's arched front; pinned Gutenberg plate SHA256 `4568caacfde738aa5273411ac27a61a2a350dc78b715ea75ee8eab66af72bfb1`. Currey, The Story of Old Fort Dearborn (1912), p.27, labels the rounded magazine 8; actual 889x588 image SHA256 `2f2b1e60fd78cb91956d16a50af526886b67c0b5fdc0337610ca5ad331360a1f`. Currey is tier5 retrospective form evidence, after an 1899 Tribune sketch of an 1898 model. Existing owner adoption authorizes vault SHAPE for the first-fort 1812 phase. Neither image dates a vault's completion or measures its radius, thickness, rise, colour or material. Do not transfer this change to the separate second-fort magazine.

### Concrete shape and confidence

Unchanged: surveyed seat, bearing, phase/date range, 4.51m front width, 3.05m depth, 2.6m wall, brick wall material, door/window/gate counts and positions, all other buildings and historical camera. Front is local +Y; current rotation180 faces it toward the parade. The vault curves across local X and runs along Y, unlike the old gable's longest-axis choice. Front width is half-measured; depth/height remain reconstructed.

Use opt-in `roof_type: barrel_vault` INFERRED with Whistler+Currey credits. Add explicit `barrel_rise_m: 1.0286254881847008`, RECONSTRUCTED, and REMOVE the obsolete visitor-facing gable `roof_pitch_deg` attribute from this record. Rise is merely old envelope conservation: min(4.51,3.05)/2*tan(34°), giving the unchanged crown3.628625488184701m. The old34° is retained in the derivation note only; the curve has varying tangent, not a uniform34° pitch. Circular-segment radius2.9860699863584146m is reconstructed, not measured from either picture. This is a shallow segment, not a claimed semicircle or a matched curvature.

Keep the existing0.30m roof projection and0.07m covering edge as declared reconstruction. Same-circle extension crosses the unchanged wall tops exactly. Side-eave height becomes2.188061556m rather than oldgable2.397647445m (0.209586m lower); total footprint/overall base-to-crown envelope stays unchanged. This edge change is explicit. Covering/material/colour stay the prior reconstruction: the B&W illustration does not attest painting or roofing fabric. The record's research note now distinguishes inferred form from reconstructed profile and metrics. No structure-grade promotion or camera/placement fit.

Covering has underside/front/rear fascia and two outer side edges; no internal ribs, random strip paint or `_gable_wall` approximation. End infills are proper polygons wound front+Y/rear-Y above unchanged rectangular walls. Roof and infill uncertainty include the reconstructed rise. Validation is magazine-only, one-storey, without chimney/gallery/cupola/lantern/loopholes; invalid rise or nonfinite derived radius is refused, never clamped.

### Actual preparation evidence and limits

R peer read the actual pictures and bound v2 PREP-only PASS to this patch. AST/pure-math probe, not Blender: exact crown/seats, closed oriented covering/ends, continuous tone, invalid profiles including finite1e-320 overflow rejected in params AND producer. All unchanged helper/class bytes, including `_cupola`, match52d. All25 existing default records resolve to their old existing params plus optional newNone; this is not proof of native output or a `matches` verdict.

Real dependency owner: `mesh_inputs._code_shas` includes the per-archetype producer, common geometry modules and emit/pin; params source isn't directly hashed, but resolved dataclass fields are. This producer change affects25 fort_structure defaults, currently0 variants. GENUINELY rebuild every affected fort default plus ACTUAL variants on the pinned native runner BEFORE THE FIRST APP SOURCE COMMIT. Re-inventory current manifests/dependencies. Preserve all243 outbuilding defaults/current0variants, their recipes/registries/physical outputs and the NE pyramid exactly: no outbuilding/common/emit/pin edits, no unrelated243 rebake.

### Native execution after separate root GO

1. Recheck original T-3041 is normally OPEN with null claimed_by/run/at/pr; no matching open PR or live target/lane job. Use normal exact-target claim in the native run. No force, stale-branch deletion, existing-PR hijack or hidden ownership exception. Stop if a new writer owns it. The reviewed7b427 owner-safe feature guards must still match.
2. Controller request: feature7b427, appchicago, target_ticketT-3041, lane`first-fort-magazine-native-20261104`, slice1/1, max_turns400, default model (no model override), NOresume_pr. Default is read-only prepare. Dispatch requires exact-artifact rootGO, fresh merged-cupola/source/claim/PR/job/feature-CI guards and one reserved POST; never retry an uncertain POST. Verify actualrun SHA/lane/Ubuntu26 label and claimed_run equal that run URL.
3. On Ubuntu26.04, verify official pinned Blender4.5.3 binary SHA/version. Derive the complete affected ID/variant list through actual recipe ownership, then run the genuine builder/UV/export/AO-as-declared/web pipeline (`tools/bake.sh --only <all affected IDs>`; build CLI accepts comma-separated IDs and includes their versions). Log bounded foreground commands, <=600s each, regular-file stdout, proper exit/reaping. Partition if needed; no partial-family source commit and no hand-written freshness/manifest hashes.
4. Preserve before/after raw outputs and source hashes. Verify all24 non-target fort physical meshes/materials/normals/colours/UV semantics, the exact cupola data/code/physical output and real parade-ground presence fix. Expect unchanged WEB bytes for unchanged output; classify deltas beyond bounds. All243 outbuilding MASTER/WEB/registry bindings and NE pyramid must stay exact. Native exporter metadata/unusedUV differences require explicit audit, never fake byte equality.
5. Compile owner-generated sidecars/Pictures/SourceUse and current grade. Target remains INFERRED; credit shape without treating tiny component depiction as a whole-building attestation. Add append-only liberty and one T-3041 changelog entry for this increment; update STATUS/ROADMAP with limits. Include final metadata in source qualification. No schema/assertion weakening, grade promotion or camera/footprint/date change.
6. Produce actual same-camera before/after compound picture from current GLBs; keep camera/source hashes. Mark only the vault discrepancy fixed if the native comparison warrants it; cupolas/gates/other differences remain open. Capture actual published1812 magazine/roof/Design/Sources and desktop1280x800 AND mobile390x780, geometry ownership and zero errors. Run current published native Stage3 BOTH viewports for the shared fort-family release, plus the relevant1812 presence/ground checks. No banked/DOM-only/old-head passes.
7. All four `check.sh --part k/4` calls proper/current before first source commit; actual changelog/ID preflight; complete exact-head hosted8+namedaggregate before normal PR merge todev. No production promotion. Push durable UNQUALIFIED source/raw-log/hash checkpoints before long gates. On success ship one bounded PR and normally release originalT3041 OPEN/PARTIAL with evidence; never done the whole fort. On incomplete native output, checkpoint and return its claim normally.


### Magazine handoff execution-stage clarification

The saved PREP/UNQUALIFIED/no-app-edits statements describe the preparation snapshot. After a separate exact root GO, the worker may execute ONLY the bounded native phase above on GitHub Ubuntu26.04/Blender4.5.3. The shared cloud host remains unavailable for Blender/GPU. Prep approval is not a native, matches or release verdict. Final published HANDOFF SHA256 6456396d7528eb9404a2832f7a2dce1827c645981d4209d84f986d259dc47654 uses this explicit stage wording; candidate patch remains661b69b2c544c73af8745be7f5b55bc142f3e2d338f6abd19a6cf8fddf4f17f5 at immutable rawcommit55a51a17a1abf95bcfbe7097973d10f0a6c7adb6. Native dispatch still awaits exact GO.


### EXECUTION GRANTED — native 41782312201

Exact root GO **IS GRANTED**, and the authorized run is already started: https://github.com/kevinrhaas/polecat-platform/actions/runs/41782312201. Earlier "dispatch still awaits GO" wording was a preparation snapshot, superseded here. Proceed with the bounded native phase; no additional design review is pending.

Public exact GO: https://raw.githubusercontent.com/kevinrhaas/chicago-evidence/ab803bc75c3ce0d97ba868c4a4308e25c196a0eb/evidence/first-fort-2026-11-04/magazine-native41782312201-authorized-dispatch/ROOT-GO.json
GO SHA256 `068f834dfccbdac637f54790111fd794a0b8874f5d2af85b7453c749c14179f7`; source base `26f6b8dfe96e9af96d7137b8e7b8a8d4061512c0`; feature `7b427d130a2cca6ed82c183c74605b965aee1d4e`. Bound request SHA256 `2cec77cfa0ad606ef3f6fb9d385188828247f582dd355508cbe6c9d36f14fda2`; patch `661b69b2c544c73af8745be7f5b55bc142f3e2d338f6abd19a6cf8fddf4f17f5`; final handoff `6456396d7528eb9404a2832f7a2dce1827c645981d4209d84f986d259dc47654`; controller `3f63c2ea506d11e4e76479d25e34036aae1c75a78e881a635b8ab9db5e6cbc43`. Actual GO/reservation/response/run/fresh source guard and monitor proof are public in that same evidence directory.

NEW T-3041 / lane `first-fort-magazine-native-20261104` / default model / max400 / no resume_pr. Claim normally for this exact run URL if not already owned; do not force another owner. Only the reviewed first-fort magazine vault, inferred shape and reconstructed profile, is authorized. Native work is on GitHub Ubuntu26.04/Blender4.5.3 only, never the shared cloud host. Genuinely rebuild the affected25 fort defaults plus actual variants before the first source commit; preserve merged cupola and all243 outbuilding outputs/bindings. All current source/runtime/image gates and normal dev PR apply. No unrelated rebake, new photo ticket or original-ticket completion: release T-3041 OPEN/PARTIAL with evidence after the increment.


### Root checkpoint-order clarification — 2026-11-04

The earlier instruction to finish all four source-check parts before the FIRST source commit is superseded. After all genuinely affected native models have been built on the pinned runner, and actual MASTER/WEB bindings and affected owners are verified, promptly push an explicitly UNQUALIFIED source-branch/raw-log/hash checkpoint BEFORE long gates. The owner explicitly requested periodic GitHub checkpoints and visible incremental progress. Do not wait for every check to save valid work.

All four actual source-check parts and normal preflight remain required before opening the release PR under repository policy. Both published runtime viewports, actual controlled picture comparisons, and the current-head eight-part gate plus named aggregate remain required before ordinary dev merge. This changes checkpoint order only: no gate/assertion is waived, no model freshness is fabricated, and no partial fort match becomes complete. Preserve the current cupola and all243 outbuilding assets. Original T3041 remains partial. Actual native execution authorization remains the granted exact ROOTGO068f/run417823 described above.
