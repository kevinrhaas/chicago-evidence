---
id: T-2373
title: Match the 1832 lighthouse to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: S
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

Match the 1832 lighthouse to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  source: `data/sources/andreas_1884_dearborn_drawbridge_plate.json`
  source: `data/sources/dearborn_street_bridge_1834_engraving.json`
  source: `data/sources/eliza_chappel_school_shore_view.json`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_river_mouth_1830.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1892_peck_hindman.jpg`
  picture: `chicago/reference/images/chicago/chicago_harbor_lighthouse_1838.jpg`
  picture: `chicago/reference/images/chicago/chicago_flood_engraving_1849.jpg`
  picture: `chicago/reference/images/chicago/chicago_dearborn_drawbridge_1834.png`
  picture: `chicago/reference/images/chicago/chicago_dearborn_street_bridge_1834.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- chicago_lighthouse_1832


## Picture-review checkpoint — 2026-10-22

The public-domain Andreas bridge plate shows a domed lantern, cage mullions, finial and gallery rail. `_tower` currently builds an opaque drum, pyramid cap and gallery disk. Add consumed optional details, document reconstructed dimensions, then bake and compare. Do not infer paint from monochrome.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of Codex lighthouse picture matching; parallel Chicago 4D 10/23/2026, 7:00:17 AM CT): Owner requested session wrap. Exact closed prototypes, actual renders and unapplied source patches are saved at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Delegated workers have stopped. Image matching remains unfinished; resume from the case handoff and preserve its evidence limits.

## Remaining effort re-estimate — 2026-10-29

The original October 11 estimate was M. This is a transparent estimate of the concrete work remaining after the already-delivered model work, rather than a change to its historical estimate. The accepted dev baseline 7c5f2109 already contains the lighthouse's physical tower (master ae855793), placement and form. The remaining unit uses that exact model: enroll the credited Castelnau camera/card reference, review the seven held files with their source/date/rights limits, and qualify the unchanged physical consumers. This is a bounded camera/card and acceptance unit, sized S.

The group therefore has one M (T-2381, the Miller adjacent-wing/roof/footprint and entrance correction) and three S members, within AGENTS.md’s group budget. Each original retains its full image gate and source qualifications; native app/code checks and an actual merged dev PR still precede completion. Existing claim ownership, group and dates are preserved.
