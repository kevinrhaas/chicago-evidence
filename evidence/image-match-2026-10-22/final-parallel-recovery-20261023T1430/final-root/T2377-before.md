---
id: T-2377
title: Match Hogan's store, the first post office to its pictures
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
claimed_by: Codex Hogan picture-match continuation 10/22/2026, 10:18:41 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: 2026-10-23T03:18:42.354Z
decision: null
decision_answer: null
---

Match Hogan's store, the first post office to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_first_post_office_1833.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- hogan_store


## Picture-review checkpoint — 2026-10-22

Current generic cabin lacks the depicted off-centre door, single front sash and gable loft light. Existing consumed `front_set_out`, opening dimensions and `end_openings` can refine it without a new archetype. Proposed resolver-valid initial values: door at 4.6 m, window at 10.2 m, sash 0.55×0.95 m, door 0.85×1.95 m, +x gable light at 0.5 and z 3.35 m, ridge chimney at 0.6. These are inferred starting values, not verified measurements. Register the Cameron illustration's own source, then bake and fit (initial wallpoint RMS 13.1 px).

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

## Unapplied next-change handoff — 2026-10-22

A proposed first refinement and its evidence/remaining validation are saved in [T-2377.patch and T-2377.md](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/image-match-2026-10-22/t3040-compound-review-checkpoint/unapplied-next-parcels). `git apply --check` passed against code commit `d3685569c5284946ab400deb0d2ccd0aa17a06be`. This is not an applied change, bake, solved camera or completed match. Claim the ticket before implementation, inspect current source and the handoff, and retain its full image acceptance. Whole-compound review support is [code PR #1218](https://github.com/kevinrhaas/chicago/pull/1218), awaiting GitHub CI at this checkpoint.
