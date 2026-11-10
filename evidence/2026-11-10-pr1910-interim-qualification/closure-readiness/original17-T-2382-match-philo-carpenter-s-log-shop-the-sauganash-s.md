---
id: T-2382
title: Match Philo Carpenter's log shop (the Sauganash's log wing) to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-10-31
pr: 1512
claimed_by: Codex continuing same four-picture batch; verified existing ownership 10/30/2026, 8:07:21 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-31T11:19:28Z
claimed_run: null
claimed_at: 2026-10-31T01:07:21.938Z
decision: null
decision_answer: null
group: T-2372,T-2375,T-2378,T-2382
---

Match Philo Carpenter's log shop (the Sauganash's log wing) to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  source: `data/sources/andreas_1884_sauganash_hotel_plate.json`
  source: `data/sources/trowbridge_sauganash_hotel.json`
  picture: `chicago/reference/images/chicago/chicago_sauganash_hotel_1831_petford.jpg`
  picture: `chicago/reference/images/chicago/chicago_sauganash_hotel_1831.jpg`
  picture: `chicago/reference/images/chicago/chicago_sauganash_tavern_1835.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- philo_carpenter_log_shop


## Picture-review checkpoint — 2026-10-22

The annex is a separate structure, not a second hotel wing to re-enable. Refine tall multipane sash and brick stack from the rights-cleared Braunhold plate. Preserve the July 1835 function: former shop/school, current use unattested.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

## Post-PR1456 remaining work estimate — 2026-10-30

The original M estimate included refining the roof, chimney and gable and solving the three source views. The accepted native MASTER f3e26f and WEB 281280, all three reviewed canonical MATCHES, hosted credited images and native recipe 498ba51e are now retained; current native recomputation reproduces that recipe exactly. Remaining work is one bounded nineteen-path entrywise adoption, generated owners and shared current app/source/PR qualification; sized S for this remaining unit. The original image gate, source/date/rights qualifications and done-on-merge acceptance remain unchanged. This is the remaining effort estimate, not a completion claim.
