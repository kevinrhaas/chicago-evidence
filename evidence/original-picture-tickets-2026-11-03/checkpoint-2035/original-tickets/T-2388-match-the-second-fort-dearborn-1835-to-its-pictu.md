---
id: T-2388
title: Match the second Fort Dearborn (1835) to its pictures, every building in it
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

Match the second Fort Dearborn (1835) to its pictures, every building in it.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

The fort was built without being checked against its pictures as a whole (inventory of 2026-10-11, T-2368). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

A picture of the fort shows many records at once, so `tools/photo_match.mjs` first learns to render a group: the camera names `also_render` (the other structure ids), each placed by its scene position. Every record of the fort is matched through those views, and the gate is carried by the blockhouse's.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Records: `fort_dearborn_artillery_house`, `fort_dearborn_barracks`, `fort_dearborn_big_barn`, `fort_dearborn_blockhouse`, `fort_dearborn_commandants_quarters`, `fort_dearborn_flagstaff`, `fort_dearborn_garrison_garden`, `fort_dearborn_guard_house`, `fort_dearborn_magazine`, `fort_dearborn_officers_quarters`, `fort_dearborn_out_building_a`, `fort_dearborn_out_building_b`, `fort_dearborn_palisade`, `fort_dearborn_parade`, `fort_dearborn_root_house`, `fort_dearborn_root_house_b`, `fort_dearborn_shop`, `fort_dearborn_store_house`, `fort_dearborn_sutlers_store`, `fort_dearborn_us_factors_house`, `fort_dearborn_wash_house`.

Pictures:
  source: `data/sources/kurz_allison_1893.json`
  source: `data/sources/chicagology_prefire276.json`
  source: `data/sources/chicagology_prefire052.json`
  source: `data/sources/wentworth_1881_fort_dearborn.json`
  picture: `chicago/reference/images/chicago/chicago_settlement_1820_2.jpg`
  picture: `chicago/reference/images/chicago/chicago_from_lake_1818_1830_childs.jpg`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_2.jpg`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_river_mouth_1830.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_second_fort_dearborn_1816_getty.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1830_alamy.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1892_peck_hindman.jpg`
  picture: `chicago/reference/images/chicago/chicago_harbor_lighthouse_1838.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- fort_dearborn_blockhouse


## Picture-review checkpoint — 2026-10-22

The unique blockhouse at the right of panel 5 has an absent cupola. Add a consumed cupola option, grade occurrence inferred from this source and dimensions reconstructed, then bake. Do not guess which range carries the pictured gallery. Early 1820 views predate replacement barracks; 1838/1850s views cannot silently govern July 1835.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

## Unapplied next-change handoff — 2026-10-22

A proposed first refinement and its evidence/remaining validation are saved in [T-2388.patch and T-2388.md](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/image-match-2026-10-22/t3040-compound-review-checkpoint/unapplied-next-parcels). `git apply --check` passed against code commit `d3685569c5284946ab400deb0d2ccd0aa17a06be`. This is not an applied change, bake, solved camera or completed match. Claim the ticket before implementation, inspect current source and the handoff, and retain its full image acceptance. Whole-compound review support is [code PR #1218](https://github.com/kevinrhaas/chicago/pull/1218), awaiting GitHub CI at this checkpoint.

**Released 2026-10-23** (claim of run 10/23/2026, 8:49:10 AM CT): Owner requested session wrap. Exact closed prototypes, actual renders and unapplied source patches are saved at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Delegated workers have stopped. Image matching remains unfinished; resume from the case handoff and preserve its evidence limits.
