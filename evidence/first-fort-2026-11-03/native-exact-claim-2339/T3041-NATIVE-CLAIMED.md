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
claimed_by: run 11/3/2026, 5:38:59 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41739288717
claimed_at: 2026-11-03T23:39:00.854Z
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
