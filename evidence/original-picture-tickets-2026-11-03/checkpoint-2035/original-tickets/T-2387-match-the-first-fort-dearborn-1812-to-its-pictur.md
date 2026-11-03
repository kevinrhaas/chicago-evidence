---
id: T-2387
title: Match the first Fort Dearborn (1812) to its pictures, every building in it
state: split
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-10-22
pr: null
claimed_by: run 10/22/2026, 5:44:36 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-22T22:46:12.274Z
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

