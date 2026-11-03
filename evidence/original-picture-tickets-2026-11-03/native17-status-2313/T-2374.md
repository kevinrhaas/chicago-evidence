---
id: T-2374
title: Match Cobweb Castle to its pictures
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

Match Cobweb Castle to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- cobweb_castle


## Picture-review checkpoint — 2026-10-22

The 20-vertex centre/wings/tails footprint is reduced to a bounding box by `log_dwelling_params`. Compound massing is not built; a camera cannot fix it. Implement opt-in compound geometry without changing other cabins.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-11-03** (claim of Codex Cobweb recovered original-panorama increment 11/3/2026, 8:05:03 AM CT): Merged PR1665 to dev as ae54d698c93f0543a233e7127e9ff036efe10506: one credited original-panorama Images link, actual desktop/phone card and native107x2 passed. Partial only; source geometry/camera/grade unchanged, private camera remains unsolved and full compound picture match unfinished. Source proof b1a59536572f005a24344fbfc602a6bc114e6ad6; fresh QA https://github.com/kevinrhaas/chicago-evidence/blob/b6168fa2fb109f505388df61f698949605c8b95c/evidence/cobweb-wolf-2026-11-03/fresh-07b8-card-and-native-stage3/RECOVERY.md. Keep original open with PR null; no completed-match claim.
