---
id: T-2383
title: Match the Sauganash Hotel to its pictures
state: open
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: null
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
