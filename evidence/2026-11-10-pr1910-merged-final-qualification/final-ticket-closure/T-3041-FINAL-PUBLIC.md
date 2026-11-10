---
id: T-3041
title: Match the first Fort Dearborn buildings against every reference picture
state: done
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: T-2387
opened: 2026-10-22
closed: 2026-11-10
pr: 1910
claimed_by: Chicago final three completion 2026-11-10 11/9/2026, 10:28:16 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-11-10T11:58:50Z
claimed_run: null
claimed_at: 2026-11-10T04:28:18.664Z
decision: null
decision_answer: null
group: T-2376,T-3041,T-2388
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

**Released 2026-11-04** (claim of run 11/4/2026, 12:08:04 AM CT, by https://github.com/kevinrhaas/polecat-platform/actions/runs/41782312201): Partial increment MERGED to dev as a92e7c3d0 (PR https://github.com/kevinrhaas/chicago/pull/1698): the first fort's powder magazine now carries the barrel vault the owner adopted from Whistler's 1808 arched front and Currey's 1912 bird's-eye on 2026-11-03 (T-3335), built by an opt-in barrel_vault branch of the fort_structure archetype. All 25 affected fort_structure masters were genuinely rebuilt before the first source commit on pinned sha256-verified Blender 4.5.3 under Ubuntu 26.04; exactly one moved a byte, 24 came back byte-identical (the second fort's magazine and the cupola blockhouse among them), and all 243 outbuilding masters, their derivatives, registries and the T-3041 NE pyramid are untouched. THE SHAPE ALONE IS ADOPTED: the rise 1.0286254881847008 m is envelope conservation holding the old gable crown at 3.628625488184701 m, making a shallow segment where Whistler draws near a semicircle, and that gap is stated, not closed. That is the second of thirteen differences on data/reference_views/first_fort_dearborn_pickets_outer/currey_1912_birdseye.match.json marked fixed; verdict stays differs. STILL OPEN there: the blockhouse cupolas and the western gateway, plus the whole original acceptance (21 named records, 9 context records, every listed picture). Parent T-2387 stays split and unfinished; no image-match completion, photo follow-up or split is claimed. Verification: check.sh parts 1-3 green, part 4 one pre-existing environmental red (NumPy 2 removed 2-D np.cross in tools/transport/horse_socket_interface_v1/socket_controls.py, nothing that step reads is in the diff), smoke stage 3 PASS at both 390x780 and 1280x800 with zero page errors, and the hosted 8-part dev gate green on the exact merged head. Recovery: PR 1698, docs/STATUS.md T-3041 (2026-11-04), docs/LIBERTIES.md L-first-fort-magazine-barrel-vault-3041.

**Released 2026-11-04** (claim of Codex magazine current 1812 acceptance followup 11/4/2026, 1:41:13 AM CT): PR #1699 merged to dev as 0a14eb07bc6630ace4ce8bec12b87e9fa1a4b0d4: delivered magazine current1812 exterior/real GPU roof and ground/Inspect Design+Sources desktop+phone accepted; saved evidence https://github.com/kevinrhaas/chicago-evidence/blob/38e7792be383556ed9506f3047e6fa2c041b7ea0/evidence/first-fort-2026-11-04/pr1699-current1812-magazine-body-design-sources/runtime-d5-v2/FINAL-CLOSURE.json. Documentation-only finalhead 880036af3d6355799968fea9a77b92d85f95deec preserves exact runtime inputs; final current8+gate passed. This is partial T3041/T2387: Currey remains DIFFERS, first-fort blockhouse cupolas, western gateway and remaining original picture coverage still open. Give back the original claim; do not close or split/create a photo ticket.

**Released 2026-11-07** (claim of run 11/7/2026, 9:54:32 AM CT): Partial increment MERGED to dev as 18d5204a (PR https://github.com/kevinrhaas/chicago/pull/1831, owner-reported 2026-11-07): both first-fort blockhouses (NW, SE) now carry the cupola the owner adopted from Currey 1912 (T-3335) — occurrence inferred, kit dimensions reconstructed (L-first-fort-blockhouse-cupolas-3041); the Currey match row is fixed, verdict stays differs. Draft PR 1704 (same feature, stalled) closed as superseded. STILL OPEN: the western gateway / wicket by the NW blockhouse, plus the original all-pictures acceptance. Parent T-2387 stays split; no completion claimed.

**Released 2026-11-07** (claim of Kevin thread: log, lower cupolas 11/7/2026, 12:37:40 PM CT): Follow-up MERGED to dev as 2ed7d761 (PR https://github.com/kevinrhaas/chicago/pull/1840): on the owner's reading of the drawings (2026-11-07) the first-fort cupolas are now log (opt-in cupola_construction) and 1.6 m bodies instead of 2.1 m (opt-in cupola_height_m), about 20% lower overall. STILL OPEN: the western gateway / wicket by the NW blockhouse, plus the original all-pictures acceptance.

**Released 2026-11-07** (claim of claude (thread: cupola lookouts and shingle roofs) 11/7/2026, 2:41:23 PM CT): partial: cupola lookout ports and riven shingle roofs in PR 1850; the western gateway/wicket by the NW blockhouse is still open

**Landed incremental progress, 2026-11-10 — PR #1902**

Merged to dev as d07704f13a5c20491c3453065f653c8cfe59064c: https://github.com/kevinrhaas/chicago/pull/1902 . Both first-fort stockades now have aligned reconstructed western wickets beside the NW blockhouse; unchanged south entrances remain usable. Pinned native run42715284565 produced the15 family outputs. Thirteen control WEBs are byte-identical; MASTER differences are unused untextured UVs only, with geometry/materials/confidence/layout preserved. Final source head4f0878a0f1d4b185dc01c9e8525e18bf6d3030bb passes all8 CI parts and the required gate. Actual desktop and phone gate interactions and all12 terrain walk cases pass, with14 screenshots inspected. Fresh Currey comparison supports this bounded increment under the explicit owner rulings.

The whole original T-2387/T-3041 all-pictures request remains partial. The northwest blockhouse lacks its own enrolled canonical comparison, and the remaining original/context picture coverage has not been individually accepted. Broader published smoke has known baseline failures disclosed in the PR; this note does not claim it passed. Recovery and source checkpoint: https://github.com/kevinrhaas/chicago-evidence/tree/3c9b3da860d21ba480a97735c753727a5a315def/evidence/2026-11-09-parallel-three-picture-source-group/ .

**Released 2026-11-09** (claim of Chicago original-picture west-gateway resume 2026-11-09 11/9/2026, 4:07:58 PM CT): Native increments merged to dev as PR1901 and PR1902 with final source gates green and actual target desktop/phone checks. Original wider image coverage remains partial in landed notes; this run continues the separate three-ticket PR1903 group. No forced closure or new photo follow-up.

**Released 2026-11-09** (claim of Chicago first-fort canonical picture coverage 2026-11-10 11/9/2026, 6:48:48 PM CT): Bounded northwest coverage MERGED to dev in PR1905 as 1880ca90fc21ee4f8c00e2af71720fa69b0e4ca0. Two actual canonical comparison groups retained (Currey14 bounded MATCHES under existing T3335 crop/context limits; Kurz30 DIFFERS on2 finite composition/identity questions). Authoritative pictured badge reflects2 alreadycredited depictions under rule12; geometry, perattributeconfidence, Images list and native meshes/placements unchanged. Final8ef source all8+requiredgate green (1290steps); actual currentdesktop+phone badge/Sources/Images pass,6 screenshots inspected,0errors. OriginalT3041/T2387 allotherdatedpictures and21record+9context inventory remain PARTIAL, notDONE. No new photo followup.

## Existing final three-ticket continuation — 2026-11-10

Continue **T-2376, T-3041 and T-2388 as one existing-ticket group** under actor Chicago final three completion2026-11-10, on `steward/t2376-t3041-t2388-final-pictures-20261110`. PR1907 has actually merged; its four qualified originals T-2374/T-2379/T-2380/T-2383 are publicly done. Green Tree's third upper-front window remains its explicit categorical remainder; the two forts retain their full original picture/date/coverage scope. No photo follow-up, replacement ticket or reduced acceptance is created.

Fresh public ownership review found T-2376 open and T-3041/T-2388 held by this same coordinator's Chicago two-fort completion group, with no matching open PR and only historical related source refs. The official claim force option is used solely to renew these own active claim timestamps and replace the old two-ticket grouping with this three-ticket continuation under the coordinator's explicit authorization. No foreign live claim, branch or writer is displaced. The previous source/date/rights rulings and partial handoffs remain in force until genuinely qualified completion; no ticket is closed by this claim.

## Qualified-source checkpoint; final closure pending — 2026-11-10 06:26 UTC

[PR1910](https://github.com/kevinrhaas/chicago/pull/1910) is still **DRAFT/OPEN and unmerged** at this checkpoint. This paragraph does not close the ticket, claim a final merge, or turn pending release checks into passed results.

Exact source `af4cc3ff486a90571edb7f3bb48ee1609343ad5f` has completed all eight protected source parts plus required aggregate,1297actual steps, in [run42765887507](https://github.com/kevinrhaas/chicago/actions/runs/42765887507). The actual final fort/GreenTree desktop+phone body/card/source/ground reviews report52directly inspected screenshots; frozen-UI-to-final-source bindings retain the exact relevant model/data/renderer trees. Final stockade smoke190/0 and boot43.82MiB passed. These bounded results do not assert the entire release is finished.

At this observed checkpoint17of18native smoke legs passed; [official desktop13 recovery42765919955](https://github.com/kevinrhaas/chicago/actions/runs/42765919955) remains running at that same source. Balanced release qualification is also still pending. The documented newFullGhost price has strict measured/negative controls; it is not permission to waive an unfinished smoke result. The earlier infrastructure cancellation, external wrong-face UI fixture and every recovery remain recorded.

The existing [public source/native starting checkpoint](https://github.com/kevinrhaas/chicago-evidence/tree/2969e726f1d28c20176174cf0ac517d915041871/evidence/2026-11-10-pr1910-final-three-source/) is a durable **pre-final** checkpoint, not a substitute for the forthcoming full final qualification/readback. Final closure requires actual remaining results, final public evidence, ordinary PR1910 merge and a fresh normal image/liveness/ownership check. No new `--anyway` or fabricated `matches` is authorized or used here.

The complete first-fort21original+9context inventory has a separate dated/rights/identity disposition for every listed picture. Current NWCurrey, outer-picketCurrey, Kurz panel1 and independent Lossing fort-only comparisons are accepted after actual native review. T3335 retains Whistler's measured plan, corner blockhouses, range functions/lengths, main-gate gap and documented75ftstaff, with the already adopted cupolas, magazine vault,NEpyramid and west wickets. Conflicting retrospective composition/camera scale is withinT3153; an unidentified outside gallery is not arbitrarily assigned to a named context record. Four heldGetty copies and the Chicagology container remain read-only, with no new rights or held-copy geometry derivation.



## Final qualified resolution — PR1910

The existing original scope is delivered by [PR1910](https://github.com/kevinrhaas/chicago/pull/1910), ordinarily merged at 2026-11-10T11:58:50Z as `b16aece58dd6e51bc5d5f4b16281cdfe15ce9404` from integrated source `fd529eb0915bea1e4b05b181f78a8c67991be56c`. The dated pending checkpoint is superseded by these actual final receipts.

The complete first-fort 21 original + 9 context inventory has a separate dated/rights/identity disposition for every listed picture. Current NW Currey, outer-picket Currey, Kurz panel 1 and independent Lossing fort-only comparisons are accepted after actual native review. T-3335 retains Whistler's measured plan, corner blockhouses, range functions/lengths, main-gate gap and documented 75 ft staff, with the already adopted cupolas, magazine vault, NE pyramid and west wickets. Conflicting retrospective composition/camera scale is within T-3153; an unidentified outside gallery is not arbitrarily assigned to a named context record. Four held Getty copies and the Chicagology container remain read-only, with no new rights or held-copy geometry derivation.

Qualification is tied to its actual source snapshots: final integrated [source CI](https://github.com/kevinrhaas/chicago/actions/runs/42808390389) at `fd529eb0915bea1e4b05b181f78a8c67991be56c`; 18 logical renderer smoke legs for the adopted native model release (16 retained-native legs, mobile stage 5 recovery at `363236c100`, and [desktop stage 13 recovery](https://github.com/kevinrhaas/chicago/actions/runs/42765919955) at `af4cc3ff48`, 158 assertions / 0 failures). On retained source `af4cc3ff48`, published stockade checks passed 190 assertions / 0 failures. Boot measured 45,948,374 bytes against 44.1 MiB; the six-stand Balanced sweep peaked at 2,597,349 triangles / 6,443 calls against 2,675,000 / 7,800. The 52 earlier directly reviewed screenshots retain their frozen visual/native/data/publisher bindings. The subsequent integrated-source review at `fd529eb0915b` accepted 22 actual screenshots and verified real default-phone release behavior. The earlier Green Tree retention claim is withdrawn; its visual acceptance remains valid. Current Full Ghost preserves dev’s 3,760,000 allowance; the retained `af4cc3ff48` runtime qualification passed the stricter 3,750,000 allowance. Durable qualification and integration evidence: [complete retained-model qualification](https://github.com/kevinrhaas/chicago-evidence/tree/0cfc4c1b2054dcecedbddb124fdc4285806688da/evidence/2026-11-10-pr1910-completion-qualification/), [final integrated source and merge](https://github.com/kevinrhaas/chicago/pull/1910). Historical failed/cancelled attempts remain recorded with their successful recoveries.

Every required canonical image gate for this ticket and any last-child ancestor was actually checked against current native assets; no open visitor-visible discrepancy remains under the explicit dated/owner-plan/T-3153 dispositions. No new forced image verdict, source date, rights upgrade, historical metre/camera claim or lifecycle override is introduced. Formal ticket state follows the real merged PR via normal official done and settle, with exact public readback.
