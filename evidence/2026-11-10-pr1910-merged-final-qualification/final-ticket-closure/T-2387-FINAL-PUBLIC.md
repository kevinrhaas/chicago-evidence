---
id: T-2387
title: Match the first Fort Dearborn (1812) to its pictures, every building in it
state: done
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-11-10
pr: 1910
claimed_by: run 10/22/2026, 5:44:36 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-11-10T11:58:50Z
claimed_run: null
claimed_at: 2026-10-22T22:44:38.087Z
decision: null
decision_answer: null
---

Match the first Fort Dearborn (1812) to its pictures, every building in it.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

The fort was built without being checked against its pictures as a whole (inventory of 2026-10-11, T-2368). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

A picture of the fort shows many records at once, so `tools/photo_match.mjs` first learns to render a group: the camera names `also_render` (the other structure ids), each placed by its scene position. Every record of the fort is matched through those views, and the gate is carried by the blockhouse's.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Records: `first_fort_dearborn_blockhouse_nw`, `first_fort_dearborn_blockhouse_se`, `first_fort_dearborn_commanding_officers_barracks`, `first_fort_dearborn_flagstaff`, `first_fort_dearborn_magazine`, `first_fort_dearborn_north_range`, `first_fort_dearborn_officers_barracks`, `first_fort_dearborn_parade`, `first_fort_dearborn_pickets_inner`, `first_fort_dearborn_pickets_outer`, `first_fort_dearborn_small_house_ne`, `first_fort_dearborn_small_house_sw`, `first_fort_dearborn_soldiers_barracks_se`, `first_fort_dearborn_soldiers_barracks_sw`, `first_fort_outer_agents_house`, `first_fort_outer_factory`, `first_fort_outer_officers_garden`, `first_fort_outer_stable_middle`, `first_fort_outer_stable_north`, `first_fort_outer_stable_south`, `first_fort_outer_sutlers_garden`.

Pictures:
  source: `data/sources/kurz_allison_1893.json`
  source: `data/sources/chicagology_prefire274.json`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_birdseye_1812.jpg`
  picture: `chicago/reference/images/chicago/chicago_kinzie_house_fort_dearborn_1812.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1803_getty.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1803_getty_2.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1803_getty_3.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_watercolor_1803_getty.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- first_fort_dearborn_blockhouse_nw

## Qualified-source checkpoint; final closure pending — 2026-11-10 06:26 UTC

[PR1910](https://github.com/kevinrhaas/chicago/pull/1910) is still **DRAFT/OPEN and unmerged** at this checkpoint. This paragraph does not close the ticket, claim a final merge, or turn pending release checks into passed results.

Exact source `af4cc3ff486a90571edb7f3bb48ee1609343ad5f` has completed all eight protected source parts plus required aggregate,1297actual steps, in [run42765887507](https://github.com/kevinrhaas/chicago/actions/runs/42765887507). The actual final fort/GreenTree desktop+phone body/card/source/ground reviews report52directly inspected screenshots; frozen-UI-to-final-source bindings retain the exact relevant model/data/renderer trees. Final stockade smoke190/0 and boot43.82MiB passed. These bounded results do not assert the entire release is finished.

At this observed checkpoint17of18native smoke legs passed; [official desktop13 recovery42765919955](https://github.com/kevinrhaas/chicago/actions/runs/42765919955) remains running at that same source. Balanced release qualification is also still pending. The documented newFullGhost price has strict measured/negative controls; it is not permission to waive an unfinished smoke result. The earlier infrastructure cancellation, external wrong-face UI fixture and every recovery remain recorded.

The existing [public source/native starting checkpoint](https://github.com/kevinrhaas/chicago-evidence/tree/2969e726f1d28c20176174cf0ac517d915041871/evidence/2026-11-10-pr1910-final-three-source/) is a durable **pre-final** checkpoint, not a substitute for the forthcoming full final qualification/readback. Final closure requires actual remaining results, final public evidence, ordinary PR1910 merge and a fresh normal image/liveness/ownership check. No new `--anyway` or fabricated `matches` is authorized or used here.

This parent retains the whole first-fort ask. Its prerequisite childT3040 is alreadyDONE onPR1218; T3041 carries the final21+9/all-listed-pictures acceptance and its inherited parent image gate. The official CLI does not automatically change this split parent's state when its lastchild closes. After T3041 actually settles on the merged release, this parent must receive an explicit normal done/settle receipt so the original17 inventory is genuinely17DONE, not16DONE plus a semantically spent split parent.



## Final qualified resolution — PR1910

The existing original scope is delivered by [PR1910](https://github.com/kevinrhaas/chicago/pull/1910), ordinarily merged at 2026-11-10T11:58:50Z as `b16aece58dd6e51bc5d5f4b16281cdfe15ce9404` from integrated source `fd529eb0915bea1e4b05b181f78a8c67991be56c`. The dated pending checkpoint is superseded by these actual final receipts.

The whole first-fort request is complete. Prerequisite child T-3040 was already DONE on PR #1218; child T-3041 now carries the final 21 original + 9 context, all-listed-pictures acceptance on this actual merged release. Their current image gate and inherited parent gate passed against genuine native assets. The accepted contemporary plan, owner-adopted exceptions, finite retrospective/source-camera disagreements, held-copy restrictions and individually unidentified outside gallery remain explicit. This parent receives its own normal lifecycle receipt after both children are DONE, rather than remaining a spent split parent in the original 17-ticket inventory.

Qualification is tied to its actual source snapshots: final integrated [source CI](https://github.com/kevinrhaas/chicago/actions/runs/42808390389) at `fd529eb0915bea1e4b05b181f78a8c67991be56c`; 18 logical renderer smoke legs for the adopted native model release (16 retained-native legs, mobile stage 5 recovery at `363236c100`, and [desktop stage 13 recovery](https://github.com/kevinrhaas/chicago/actions/runs/42765919955) at `af4cc3ff48`, 158 assertions / 0 failures). On retained source `af4cc3ff48`, published stockade checks passed 190 assertions / 0 failures. Boot measured 45,948,374 bytes against 44.1 MiB; the six-stand Balanced sweep peaked at 2,597,349 triangles / 6,443 calls against 2,675,000 / 7,800. The 52 earlier directly reviewed screenshots retain their frozen visual/native/data/publisher bindings. The subsequent integrated-source review at `fd529eb0915b` accepted 22 actual screenshots and verified real default-phone release behavior. The earlier Green Tree retention claim is withdrawn; its visual acceptance remains valid. Current Full Ghost preserves dev’s 3,760,000 allowance; the retained `af4cc3ff48` runtime qualification passed the stricter 3,750,000 allowance. Durable qualification and integration evidence: [complete retained-model qualification](https://github.com/kevinrhaas/chicago-evidence/tree/0cfc4c1b2054dcecedbddb124fdc4285806688da/evidence/2026-11-10-pr1910-completion-qualification/), [final integrated source and merge](https://github.com/kevinrhaas/chicago/pull/1910). Historical failed/cancelled attempts remain recorded with their successful recoveries.

Every required canonical image gate for this ticket and any last-child ancestor was actually checked against current native assets; no open visitor-visible discrepancy remains under the explicit dated/owner-plan/T-3153 dispositions. No new forced image verdict, source date, rights upgrade, historical metre/camera claim or lifecycle override is introduced. Formal ticket state follows the real merged PR via normal official done and settle, with exact public readback.
