---
id: T-2384
title: Match St Mary's church to its pictures
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

Match St Mary's church to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_st_marys_church_1843.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- st_marys_church


## Picture-review checkpoint — 2026-10-22

The later image's open belfry must not be backdated into the July 1835 phase; the original-location phase ends June 1837. Resolve the depicted phase before matching it.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of Codex frame picture-match integration 10/23/2026, 12:28:11 AM CT): First picture-led frame refinements and source corrections are saved in the GitHub recovery checkpoint aaeac5b0. Full image matches remain open. Shared generator and source prerequisites will be tracked separately; continue the original cases from the recorded previews.

**Released 2026-10-23** (claim of Codex St Mary picture matching continuation 10/23/2026, 9:08:19 AM CT): Exact continuation archived at https://github.com/kevinrhaas/chicago-evidence/blob/64fd5de/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Positive1835 chapel actual Moss/Gale previews remain differs; narrower belfry next study is UNRUN, not canonically adopted. Preserve25x35plan, dates, placement and uncertain tower installation; Gale1902 original-site attribution is retrospective, Quarter May1844 dates presence only. Official271-family rebuild and all-picture/app validation still owed. Original T-2384 remains open and unaccepted; normal own-claim release for wrap handoff, no done.

## Remaining effort re-estimate — 2026-10-29

The original October 11 estimate was M. This is a transparent estimate of the concrete work remaining after the already-delivered model work, rather than a change to its historical estimate. The accepted dev baseline 7c5f2109 already contains the chapel form, belfry, footprint, solved Moss camera and held credited reference. The remaining physical correction is one nullable front-sill control: raise the five front sash 0.45 m, preserve their sizes and every other opening, and qualify the selected master/WEB and card. Actual native production retains all 270 other frame model pairs byte-exact. This remaining correction and acceptance unit is sized S.

The group therefore has one M (T-2381, the Miller adjacent-wing/roof/footprint and entrance correction) and three S members, within AGENTS.md’s group budget. Each original retains its full image gate and source qualifications; native app/code checks and an actual merged dev PR still precede completion. Existing claim ownership, group and dates are preserved.
