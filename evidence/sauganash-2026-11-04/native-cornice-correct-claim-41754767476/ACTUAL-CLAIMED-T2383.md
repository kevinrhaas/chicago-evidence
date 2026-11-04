---
id: T-2383
title: Match the Sauganash Hotel to its pictures
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
claimed_by: run 11/3/2026, 8:01:31 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41754767476
claimed_at: 2026-11-04T02:01:31.986Z
decision: null
decision_answer: null
---

Match the Sauganash Hotel to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  source: `data/sources/andreas_1884_sauganash_hotel_plate.json`
  source: `data/sources/trowbridge_sauganash_hotel.json`
  source: `data/sources/kurz_allison_1893.json`
  picture: `chicago/reference/images/chicago/chicago_sauganash_hotel_1831_petford.jpg`
  picture: `chicago/reference/images/chicago/chicago_sauganash_hotel_1831.jpg`
  picture: `chicago/reference/images/chicago/chicago_sauganash_tavern_1835.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- sauganash_hotel


## Picture-review checkpoint — 2026-10-22

Group with Carpenter. `sauganash_plate_baseline.json` supplies measured vanishing points (−1467.2, 6462.5), focal 3664.7 px and horizon 917.5 on 2017×1296. Fit translation against the render. Measured 2.392 m doorcase/1.923 m opening and 45 px transom are not fully consumed by `_frontispiece`. Braunhold/Petford/Trowbridge are related compositions, not independent witnesses.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of Codex frame picture-match integration 10/23/2026, 12:28:11 AM CT): First picture-led frame refinements and source corrections are saved in the GitHub recovery checkpoint aaeac5b0. Full image matches remain open. Shared generator and source prerequisites will be tracked separately; continue the original cases from the recorded previews.

## Incremental entrance and lower-window correction — 2026-11-03

[PR #1631](https://github.com/kevinrhaas/chicago/pull/1631) adds the Sauganash entrance case, transom and sidelights, plus four taller, narrower lower front sash and shutters. The working sash dimensions are reconstructed 0.70 × 1.85 m with a 0.90 m sill, bounded by the Andreas/Braunhold engraving; they are not historical measurements. The selected door leaf also drives its entrance clearance. Existing upper/rear openings, body/roof massing and geographic placement stay unchanged. Liberty `L-sauganash-entrance-lower-sash-2383` records these choices.

The genuine native MASTER is `a369598a…` and WEB is `5f7d8a54…`. Candidate checks reproduced 25 default controls and kept the other 24 MASTER/WEB files unchanged. Three Carpenter-group comparisons were genuinely refreshed for the changed hotel context and directly reviewed: the already-accepted Carpenter target remains accepted, while the whole hotel is not signed off by those annex cameras. Native dependent owners updated the entrance/apron and yard-goods outputs; the other checked doorway consumers stayed unchanged.

This is partial progress; T-2383 is not done. Its own full hotel/compound picture coverage and signoff remain. No new follow-up ticket or claim of a historical camera, door traversal, or complete photographic match is made.

Pushed application revision: `e51af51e7723b1f39586e204f29b64f15263b920`. Fresh published desktop and 390×780 phone checks pass with default geometry release enabled, no page/console/network/server errors, all six captures directly reviewed and source/publication/metadata guards unchanged. [Durable actual runtime proof and recovery](https://github.com/kevinrhaas/chicago-evidence/blob/fd7b25a3f6d3470da24d5071dbfbe4ab6818864d/evidence/wolf-sauganash-2026-11-03/e51af51e7723-default-visitor/RECOVERY.md). Native stage 3 was not rerun on e51; the earlier qualified feature head has both native stage-3 passes. Newer Fort/Pullman changes on dev are being integrated before merge. No final integration, merge or full-ticket completion is claimed by this checkpoint.

## Merged incremental progress — 2026-11-03

[PR #1631](https://github.com/kevinrhaas/chicago/pull/1631) merged into dev at 2026-11-03 04:03:42 UTC as `18c037e9f756a5190787ef1bd77bacce78331ad1`. The checked source head is `0e838b35b5ba32b61ccd01499310520e160ab4a2`; GitHub gate passed before merge. [Final screenshots, source transcripts and native regression proof](https://github.com/kevinrhaas/chicago-evidence/blob/121eaee6e28f74696131cfd71850e26c8cc259b1/evidence/wolf-sauganash-2026-11-03/0e838b35b5ba-final-default-visitor/RECOVERY.md). Actual published desktop and phone checks pass with default geometry release, all six captures directly reviewed and no page/console/network/server errors. Native stage 3 passes 107 checks at each viewport with zero failures/page errors; all source/publication/Git guards stay unchanged.

The four lower front sash and entrance case/leaf correction are landed. The three Carpenter contextual comparisons are genuinely refreshed. The original full hotel/compound picture coverage and signoff remain unfinished; the contextual annex views do not close this ticket.

This original ticket remains open for its remaining work. No follow-up ticket or whole-ticket completion is filed. The published dev deployment was still pending at the first post-merge read; the merge itself is verified.

**Released 2026-11-02** (claim of run 11/2/2026, 5:29:33 PM CT): Merged scoped facade and credited-picture progress in PR #1631 (18c037e9); original picture coverage and signoff remain. Final 107+107 viewport proof is linked in each ticket.

**Released 2026-11-03** (claim of Codex Sauganash current Andreas comparison 2026-11-03 11/3/2026, 3:13:15 PM CT): PR1680 merged to dev at 6953d4131bf741a1d56a141a83b0bc852b8cb56b: Andreas's credited 1884 retrospective engraving is now held on the hotel's Images card (3 rows, 1 held and 2 links), and the actual current two-building comparison records DIFFERS. All four source parts, current integration owners, whole hosted1139 gate, actual desktop/phone custom review and official Stage3both107 passed; root directly reviewed12 screenshots. This is a partial visible increment with no geometry/phase/placement/paint change. The main/rear-wing roof silhouette and left-gable differences remain OPEN under the original image gate; camera uncertainty is within tolerance. Do not mark the original done or create photo followups. Exact source/recovery: https://github.com/kevinrhaas/chicago-evidence/blob/a817d15ed334e4f20d3fe3ab6d2249996a6ea730/evidence/sauganash-2026-11-03/pr1680-integrated27-source4-published-qa-active/RECOVERY.md ; final both-viewport/merge receipts are linked from https://github.com/kevinrhaas/chicago/pull/1680 .

## Owner-targeted native increment: boxed main-gable cornice — 2026-11-04

Work only original T-2383, one visible partial increment: add the missing boxed rake cornice and short horizontal returns pictured on the hotel's visible main +x gable. The original remains OPEN/PARTIAL; no full image match, done override, new photo ticket, split sign-off or grouping. Prior PR1680 already merged6953 and its claim was released. [Root-reviewed picture/source/baseline readiness](https://github.com/kevinrhaas/chicago-evidence/blob/5107b810f803a7baeeb43acef55eb32b82c47c7a/evidence/sauganash-2026-11-04/next-boxed-gable-cornice-readiness-current8e64/RECOVERY.md); the source is the credited public-domain1884 Andreas/Braunhold plate, not a newly recovered period photograph. Read the original pictures and current dossier/match records directly before authoring.

READINESS BASELINE: current dev `96d0612d940e3652af24875674a2e17feeb38184` has Hotel MASTER a369598aafec6a868b0ec3e04ba591a821e4518174a1e75ac2bdba790ffbe5ec, WEB5f7d8a54f1c805d53bdb558506dc18ce237c9c0fb180a7cd274dec7d64ad480e, unchanged producer/params and Hotel structure from the root-reviewed picture. Ticket was open/unclaimed/prnull at the audit, but that is not a lock: before any application write, re-read fresh ticket, live native/ordinary workers, open PRs and inflight; claim normally. Stop on a genuine live claim/PR refusal, never force takeover or select another ticket. The surviving steward/t2383-sauganash-andreas-current-20261103@27ab2f3 branch is the CLOSED/MERGED PR1680, not an unmerged rescue. Verify rather than infer from its age.

LOCAL FEATURE: one explicit optional, default-off main-gable-cornice control in local generators/archetypes/frame_tavern.py and frame_tavern_params.py, selected only on Hotel frame_1831 +x. Do not change common geometry/emit/material helpers, repurpose the entrance cornice or annex fascia, or activate it for other houses. Initial reconstructed trial: 0.55m horizontal returns, 0.18m section/depth and0.18m projection, adjusted only for real native joins/intersections. Occurrence/form is inferred from the retrospective picture; ALL numeric geometry stays RECONSTRUCTED with the reasoning and bounds in the existing dossier, data/liberties and append-only LIBERTIES. The source's whole-picture attested grade does not upgrade metric dimensions or establish July1835 occurrence. Use the existing white-wall material. Strict params must reject invalid/incompatible roof, scheme/end and nonfinite/out-of-bound controls; default-off existing buildings must keep their designed shapes.

PROTECT: main footprint9.92x8m; actual wall5.5m (6.1m is the attic opening's z, not wall height); working pitch25.2deg; UTM447174.1/4637265.2, bearing0; all openings/bays, four existing lower sash, entrance case/leaf, blue louvred shutters, two stacks, rear/cross wing8m, grades/paint and separate Carpenter Shop. Do not cut cross-wing depth to4m, remove pictured gable windows or move the building. Roof/wing/other image discrepancies remain OPEN. Measure real bbox and cornice joins, avoid floating boards/holes/window/roof overlaps and protect dry, grounded native entry. Do not assume bbox or doorway-consumer identity; invoke actual affected owners if measurements require them. Make the missing element visible from a sensible outside visitor stand.

NATIVE SCOPE AND CONCURRENT GT: pinned Ubuntu26.04/Blender4.5.3 worker only; no cloud-host Blender. Changing this producer/resolver stales ALL current23 frame_tavern defaults, plus every variant native staleness actually reports. GENUINELY build and qualify them BEFORE the first application source commit; a new recipe hash on old bytes is not a bake. Reuse WEB only if it is truly bound to the actual unchanged MASTER; changed outputs require real encoding. Preserve every foreign manifest and manifest.web row. No hash-only proof renewal or weakening a gate. New source inputs must match actual emitted bytes.

Green Tree PR1684 is currently OPEN at `a5df5f8d0256de921762fa5a47b44c4326e1bb6f` and overlaps this family. Its exact geometry delta is enclosed_left_annex.value.shoulder.front_gable_peak_m4.50->4.85m; closed-shoulder, wagon/yard decisions, placement and other dimensions stay intact. Recheck current PR/dev status at start and before integration; continue concurrently without taking its claim. When that work lands, merge currentdev normally and perform a TRUE combined Green Tree bake using BOTH its peak data and this new producer, even if the default-off cornice itself does not change GT geometry. Never attach a new combined-input digest to pre-combination GT bytes. Qualify changed GT WEB and actual source views if its MASTER changes; inherited green images are not combined-output acceptance. Native both-sides model conflicts require actual combined regeneration, never hand-winning one registry side. Current Shop source and all foreign producers are read from current combineddev.

TRUTHFUL GT PROVENANCE: root independently checked PR1684: eight other meshes keep exact geometry/normals/colors/indices and materials, while UV0 was repacked across all ten meshes; those UVs are unused and no texture/material samples them. The existing GT match-note phrase “every other primitive byte-identical” is too broad. When the current GT canonical owner is actually refreshed after the new family producer, narrow this to geometry/material identity with the explicit unused-UV exception. Preserve the accepted pointed-cap increment and the remaining DIFFERS state. Do not promote that historical reading into whole-primitive identity or assert future combined-output identity without measuring the actual output. This is the same family/canonical provenance work, not a new ticket.

CANONICAL IMAGE COVERAGE: four real Hotel-dependent groups need ACTUAL controlled before/after renders and freshly bound records: ownHotel Andreas1884 remains DIFFERS; Carpenter Shop Andreas1884, Trowbridge1902 and Kurz/Allison1893panel14 are currently MATCHES. Read each camera, source and actual current model. Render all four from their controlled cameras, preserve meaningful before images, and publish actual output pairs. Root must directly review the new image pairs/Shop anchor before retaining its three MATCHES verdicts; do not merely rewrite groupSHA, inherit a previous acceptance, mark Hotel MATCHES, or reopen the already-DONE Shop original. Publish the review packet early enough for root inspection before merge. Any changed actualGTMASTER adds its relevant source views to this controlled review.

SAVE EARLY: publish a public UNQUALIFIED raw-working-source checkpoint every15-20minutes and immediately after the actual build, BEFORE full gates finish. Include exact authored source postimages/diff, input/output hashes, native logs/receipts, current head/base and precise remaining work in chicago-evidence; link it from the existing ticket/PR when available. These are durable WIP evidence, not claims of gate passes or qualified application commits. Preserve all earlier failed/WIP receipts. Every application source commit still needs genuine affected native outputs and all four source-gate parts; no stale data-only app commit to create apparent progress.

FINISH ONE INCREMENT: commands bounded600s foreground, proper exact-source/output guards and closed native receipts. Resolve known bounded local reds and rerun affected checks while budget remains. All four sourceparts1/4..4/4 must genuinely pass before each application source commit, plus actual PR-only preflight questions. Publish from the committed final currentdev-integrated head; run actual desktop1280x800 and phone390x780 UI/card Images/Reader/body/entry checks with no pageerrors, and the required measured native published smoke subset at BOTH viewports. Keep actual subset evidence distinct from conservative ALL15 requests. Measure light-tier headroom; do not weaken assertions. The final exact head needs the ACTUAL whole hosted source `gate`, not only `report`/`warranted` or skipped CI. Request the supported full-gate path if necessary and wait for green. Only after actual current-source, both UI, native checks, root pixel review and required hosted green: ordinary feature PR into dev and ordinary protected merge. No direct dev/main pushes or auto-merge before those proofs. Concise visitor-visible changelog, honest STATUS/dossier and partial release of T-2383 after merged progress; do not mark it done. If150minutes/400calls cannot finish safely, preserve a resumable PR/public raw-source checkpoint and exact remaining work instead of inventing completion.

[Immutable root-approved handoff and source/ownership review packet](https://github.com/kevinrhaas/chicago-evidence/blob/b2fdf42d877436189ae4e9df818b2799c7faa1ee/evidence/sauganash-2026-11-04/cornice-native-dispatch-review-dev96d061/RECOVERY.md).

**Released 2026-11-03** (claim of Codex Sauganash cornice handoff 2026-11-04 11/3/2026, 7:30:25 PM CT): Prepared root-reviewed boxed-gable-cornice exact native handoff and source audit; original image work remains open/partial. No application edit or geometry completion. Next authorized worker must claim normally; preserve genuine all23+variants builds, combined Green Tree and four canonical/root pixel gates.
