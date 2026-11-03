---
id: T-2377
title: Match Hogan's store, the first post office to its pictures
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

**Released 2026-10-23** (claim of Codex Hogan picture-match continuation 10/22/2026, 10:18:41 PM CT): Owner requested session wrap. Visible first increment is pushed in resume PR https://github.com/kevinrhaas/chicago/pull/1229 at08f0330eb72129a76690d4379f9cad93c01fba96; actual strict1053/778s, exact source tree and postcommit proof are archived at https://github.com/kevinrhaas/chicago-evidence/blob/8340457/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Fresh all15parts mobile/desktop jobs and required CI remain pending; root PRlap expires17:57:29UTC. Resume existing PR and review exact-head logs/currentdev before merge. Original picture comparison still differs; no accepted image match or closure.

## Remaining effort re-estimate — 2026-10-29

The original October 11 estimate was M. This is a transparent estimate of the concrete work remaining after the already-delivered model work, rather than a change to its historical estimate. The accepted dev baseline 7c5f2109 already contains the pictured store's off-centre door, front sash, gable light and stack. The remaining physical correction is two small default-off controls: horizontal courses on the pictured end gable and a projecting stack cap, plus the credited Cameron card reference and acceptance review. The actual Hogan-only native production retained all 81 other log model pairs byte-exact at that dated increment; Miller’s later correction is accounted for separately. This remaining correction and acceptance unit is sized S.

The group therefore has one M (T-2381, the Miller adjacent-wing/roof/footprint and entrance correction) and three S members, within AGENTS.md’s group budget. Each original retains its full image gate and source qualifications; native app/code checks and an actual merged dev PR still precede completion. Existing claim ownership, group and dates are preserved.
