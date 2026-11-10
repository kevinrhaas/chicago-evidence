---
id: T-2381
title: Match the Miller House to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-10-30
pr: 1456
claimed_by: Codex Chicago picture group renewal 10/29/2026, 2:27:32 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-30T21:42:36Z
claimed_run: null
claimed_at: 2026-10-29T19:27:38.302Z
decision: null
decision_answer: null
group: T-2381,T-2373,T-2384,T-2377
---

Match the Miller House to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1830.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1830_and_1833_engravings.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1832.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_tavern_miller_house_1832.jpg`
  picture: `chicago/reference/images/chicago/chicago_town_view_1833_colbert.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833_hammon.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833_nypl.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- miller_house


## Picture-review checkpoint — 2026-10-22

Colbert/Blanchard pictures show log lower storey, vertical-board upper storey and a low side annex. `_frame_addition` clads both floors in horizontal clapboard and puts the old cabin behind. Add opt-in split cladding and side-wing composition; preserve unrelated defaults.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-26** (claim of Codex Miller picture correction 10/26/2026, 9:04:59 PM CT): Renew this same active Miller run for the combined Miller/lighthouse/Mary PR; complete source/native WIP is checkpointed, and original image acceptance remains unfinished.
