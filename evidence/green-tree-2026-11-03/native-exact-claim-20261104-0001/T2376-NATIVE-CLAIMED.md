---
id: T-2376
title: Match the Green Tree Tavern to its pictures
state: claimed
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: null
pr: null
claimed_by: run 11/3/2026, 6:01:18 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41742893188
claimed_at: 2026-11-04T00:01:18.671Z
decision: null
decision_answer: null
---

Match the Green Tree Tavern to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  source: `data/sources/andreas_1884_green_tree_hotel_plate.json`
  source: `data/sources/trowbridge_green_tree_1902.json`
  source: `data/sources/chm_green_tree_1859.json`
  source: `data/sources/kurz_allison_1893.json`
  picture: `chicago/reference/images/chicago/chicago_green_tree_tavern_1835.jpg`
  picture: `chicago/reference/images/chicago/chicago_green_tree_inn_1838.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- green_tree_tavern


## Picture-review checkpoint — 2026-10-22

Both pictures show seven long-elevation bays; `_fenestration_gable_front` derives six and ignores `upper_windows`. Add an explicit optional eaves-bay count. Gable windows differ between Braunhold and Trowbridge; the off-centre entrance and low additions also need comparison.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of Codex frame picture-match integration 10/23/2026, 12:28:11 AM CT): First picture-led frame refinements and source corrections are saved in the GitHub recovery checkpoint aaeac5b0. Full image matches remain open. Shared generator and source prerequisites will be tracked separately; continue the original cases from the recorded previews.

**Released 2026-10-25** (claim of Codex Green Tree visible image-match continuation 10/25/2026, 5:38:41 PM CT): The bounded visible front correction is in PR #1328 (https://github.com/kevinrhaas/chicago/pull/1328), under final combined validation: two viewer-left sash, rightmost doorway, and matching native entrance/apron. T-2376 remains unfinished: the committed Andreas1838 discrepancy register still has visitor-visible annex massing and long-wall opening-pattern gaps. Conflicting upper/attic drawings and camera residuals are within tolerance under T-3153. No photo follow-up or false whole-case completion is filed.

**Released 2026-10-29** (claim of Codex Tremont pictured-form and Green Tree continuation 2026-10-29 10/29/2026, 9:35:31 AM CT): Finite seventh-sash and front wagon-bay corrections are qualified in PR #1448. The substantial enclosed-annex discrepancy remains OPEN on original T-2376; continue this original image case without a new photo ticket.

## Prepared next geometry increment — 2026-11-03

The Green Tree open wagon bay, connector and farther-range orientation have a genuine regenerated MASTER (`f447aa45…`) plus native occupied-solid handling for collision, routes, framing, ground and entrances. The prepared controls retain the other 24 default MASTER files, including the Sauganash correction. The already-landed front door/sash layout is not claimed as new work.

[Durable source package, exact manifest and recovery](https://github.com/kevinrhaas/chicago-evidence/blob/dda6ee9414ddcfd5f67cfd3bc3815f436c8f792b/evidence/green-tree-2026-11-03/eae-compatible-consumers/RECOVERY.md). Focused geometry, Fort-gate and resource-lifecycle fixtures pass. A private successor also preserves the newer Fort ground renderer changes; it awaits rebinding to the final combined Sauganash/Wolf head.

This is a source checkpoint, not a merged app change or picture signoff. Remaining adoption work: native WEB/scene/yard/entrance refresh, source gates, actual published desktop/phone review and refreshed picture bindings where changed. T-2376 remains unfinished; no follow-up ticket is created. Apply only guarded source deltas and the separate liberty appendix, never replace the current full liberty book with a package snapshot.

**Combined `0e838b35` checkpoint:** [23 guarded source changes and recovery](https://github.com/kevinrhaas/chicago-evidence/blob/e1c2de29d477bb2441b7b699f82886c82046426a/evidence/green-tree-2026-11-03/combined-0e838b35-consumers/RECOVERY.md). All per-file preimages now bind to the pushed Sauganash/Wolf/Fort integration. The 23 postimages and complete 2,119-file private execution input set are byte-identical to the recorded passing Fort-compatible fixtures; no tests were rerun or relabelled as a new run. The separate liberty appendix avoids replacing the current book. App adoption and full image signoff remain unrun.

**Released 2026-11-03** (claim of Codex combined Green Tree range and Wolf Point credit integration 11/3/2026, 4:48:56 AM CT): Partial Green Tree increment merged normally in PR #1652 (squash738f0f81566693980a09f20175a90c5602ec042f; reviewedhead ebf7befa1afba05947578a5ee08e0cbc8655d98a). The low connector and turned farther gabled range now use authenticated native geometry and occupied-solid consumers, with the existing procedural open wagon bay retained. Combined source/native gates, desktop/phone published checks and official107x2 passed. The historical Andreas comparison remains differs with one compound OPEN for the remaining closed shoulder/openings/source alternatives; the original image gate is unfinished. Keep this original ticket open/partial and PR field null; no done or automatic close. https://github.com/kevinrhaas/chicago/pull/1652

**Released 2026-11-03** (claim of Codex original T2376 closed shoulder and coupled yard increment 2026-11-03 11/3/2026, 2:10:37 PM CT): Partial progress merged in https://github.com/kevinrhaas/chicago/pull/1677 at dev7b2e956d38c7a35d2b8964cff4f6f7163f3e8665: choose the documented closed Andreas shoulder with sash/dormer; remove its competing shed/posts/covered wagon and occupied cordwood rick, retaining two separate farm wagons. Exact source four parts, accepted desktop/phone plus native107 both, current owners and full hosted gate passed. ORIGINAL REMAINS PARTIAL/DIFFERS: visible roof/proportion gaps remain in data/reference_views/green_tree_tavern/andreas_1838.match.json; Trowbridge open-bay counterevidence and unknown conversion date remain explicit. No original-ticket signoff, done override, new photo follow-up or exact July1835 claim. Complete proof https://github.com/kevinrhaas/chicago-evidence/blob/8825e2556e9af799052efad6a5414116ca41b1c5/evidence/green-tree-2026-11-03/final749-accepted-both-native107/RECOVERY.md . Resume the remaining visible discrepancies from the merged source.


## Exact native-worker small dormer-peak trial handoff — 2026-11-03

This is one bounded visible trial within existing T-2376, NOT full original picture matching. PR1677's accepted closed shoulder, lower sash, raised upper light, yard cleanup and current0b53MASTER/0154WEB are already merged and publicly delivered; do not replay/revert them. Root directly viewed the current comparison and authorized only the following data-only trial.

Read [current-source/native-parameter/actual-picture readiness](https://github.com/kevinrhaas/chicago-evidence/blob/094485bf376bd33cac9ff087eeef76b041ff672b/evidence/green-tree-2026-11-03/native-dormer-peak-readiness-current42b/RECOVERY.md), CURRENT-SOURCE.json, PARAMETER-TRIAL-AUDIT.json, PICTURE-AND-ASSET-BINDINGS.json and actual CURRENT-0b53-ANDREAS.jpg. Reassess actual current dev at worker start.

The ONLY proposed geometric data change is phases.frame_1833.form.enclosed_left_annex.value.shoulder.front_gable_peak_m:4.50→4.85m. Keep this value reconstructed, not a measurement from the retrospective plate. Actual current pure params80d47 validate the candidate already; no producer, parameter-validator, schema or recipe-scheme edit is authorized. The candidate raises the little cap0.35m from about25.6degrees to about46.1degrees while staying below unchanged mainwall5.0m and actualglobalmax8.722m. Those are working controls/candidate calculations, NOT a promised output or source measurement.

On pinnedUbuntu26.04/Blender4.5.3 genuinely build the affected targetMASTER and discover actual variants/staleness (currentframe_tavern roster23, expectedONLYthisone target stale; do not rebake a historical25family). Genuinely encode the changed WEB; never relabel old0154 as new. Record actual complete normalized inputs and actual outputs BEFORE the FIRST source commit. No predicted/manual freshness rewrite. Preserve all foreign registry entries and producer families: activeJail41734994705/frame_dwelling271, firstfortNE41739288717/outbuilding243, secondfortcupola41740271907/fort_structure25. Their runs/topics/claims are independent and must remain untouched.

Capture genuine controlled BEFORE/AFTER through native photo_match.mjs using the unchanged9439f5camera and bfaa184fsource, with current0b53 as before. Preserve old comparison history. Inspect whether this sharper cap actually improves the pictured shoulder dormer without roof seam, hole or penetration. Confirm actual triangles/regions confine change to this small dormer roof and associated gable-course infill, fullbbox remains exact, mainbuilding/occupiedrings/doorfaces/nativeground/entry/phase/materials unchanged. Keep closed shoulder, lower and upper light, two independent uncovered farm wagons and no shed/posts/coveredwagon.

One primary candidate and at most one justified adjustment are authorized. If no useful visible improvement results, retain honest recovery and LEAVE THE APPLICATION UNCHANGED; do not ship a number merely because it validates or run an unbounded pixel-fit loop. If useful, mark only this sharper roof detail fixed and keep remaining shoulder/compound proportions OPEN. No full view/original matches conclusion follows from having one old OPEN compound row.

Entire original coverage remains incomplete: Andreas1884, Trowbridge/Gale1902, CHMc1859, Kurz/Allison1893, plus both named reproduced images. Andreas verifiedPD1884 is retrospective; INN1838 caption is not an independently established date/dimension/camera. Trowbridge/Gale1902 retrospectivelycaptioned1835 shows an OPEN post/roof bay, against the accepted enclosed shoulder; source disagreement and unknown conversion date remain explicit. CHMc1859 stays CHECK_REQUIRED/link-only/cross-check: NOderivative or geometry from it and no falsefrom-spot. Keep all four native credited picture rows, legitimate existingAndreas comparisonspot,1859noheld/nospot, date/paint/sourceconflict explanations. Upper/atticcount and retainedcamera/pixel residuals stay WITHINTOLERANCE underT3153; no newcalibration barrier/photo followups.

Root reviewed platform draftPR219 exactfeatureaa9d7d2322d3abbc78d72526146c018a241c643e on steward/chicago-native-exact-ticket-20261103; local11CIgroups/official15case bothviewport smoke/bothhostedchecks passed. Dedicated exactjob literalUbuntu26.04/150min uses SHA-verifiedBlender4.5.3 cache; platform main unchanged. After this preserved nativehandoff is synchronized/released and freshownership is free, one exacttargetT-2376 featuredispatch appchicago/slice1/slices1/lanegreen-tree-dormer-native-20261103/unspecifieddefaultmodel-effort is authorized. No worker dispatch is claimed by metadatahandoff alone.

All four complete source-check parts must PASS BEFORE firstsourcecommit, each command bounded600s with truthful properreaping/verdicts. Ask actualcommittedhead PRchangelog/ID questions and push draftdevPR promptly only for useful qualified increment. Publish the exacthead and verify shippedbytecontract. Actual desktop1280x800 AND phone390x780 must show smallgable/body Normal/ByGrade, currentImagescredit/Record, nativearrival/drygroundedoutsideentry with zero page/console/network/server errors, plus appropriate existing smoke/nativeStage3both107 as applicable. Split customQA into bounded<=600s legs (setup/card/body/entry) rather than exceedingcapture/process ceilings or weakeningassertions. Keep coarseALL15 smoke-budget request distinct from actual scopedverification. Root must directly review actualpixelresults before exactfinalhead hostedgreen/ordinaryprotecteddevmerge.

Append bounded research/liberty/STATUS/ROADMAP explanations without replacing foreign suffixes; one visitor-facing changelogentry. Save actualgeometry/source4/PR/merge/delivery checkpoints. Then release T2376 OPEN/PARTIAL/DIFFERS with remaining discrepancy and recovery link. NOdone--pr,done--anyway,newphoto tickets,resplit,directdev/mainpush,admin/forcemerge,hostBlender or fabricatedrights/measurement.


Known native branch guard, checked before this metadata handoff: steward/t2376-closed-shoulder-coupled-yard-20261103 is still EXACT74992e8, the finished/mergedPR1677 head, not another active run. Three other listed verification/picture branches are127–213hours old and have no open PR. Recheck fresh ticket claim, every matching openPR and branch tip before the worker acts. If the guard names only these finished/stale branches while T2376 is OPEN/free and no live PR/owner exists, native ticket.mjs claim T-2376 --force is authorized ONLY to pass that branch guard. It is NOT Git force, branch deletion, a live claim takeover or permission to override a new matching PR. Preserve any refusal and actual audit; stop if new live ownership appears.

**Released 2026-11-03** (claim of Codex Green Tree dormer native handoff 2026-11-03 11/3/2026, 5:54:30 PM CT): Reviewed bounded data-only dormer trial native handoff saved; OPEN for authorized exact T2376 worker. No geometry, dispatch or full-original completion claimed by metadata handoff.
