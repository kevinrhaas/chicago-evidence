---
id: T-3108
title: 1801 Prairie's south-west corner from HABS photograph 1: the two-storey round corner bay under its pierced balcony south of the gabled pavilion, the pavilion's face narrowed to the print's paired lights and its gable re-centred, then HABS 1's camera re-solved on the rebuilt front (its cornice reads up to 85 px over the build's at the corner) and the Taylor match record re-read
state: done
epic: SOUTH_TIME
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-3003
opened: 2026-10-24
closed: 2026-10-25
pr: 1314
claimed_by: run 10/25/2026, 11:44:54 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-25T20:36:44Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/40212074067
claimed_at: 2026-10-25T16:44:55.366Z
decision: null
decision_answer: null
---

1801 Prairie's south-west corner from HABS photograph 1: the two-storey round corner bay under its pierced balcony south of the gabled pavilion, the pavilion's face narrowed to the print's paired lights and its gable re-centred, then HABS 1's camera re-solved on the rebuilt front (its cornice reads up to 85 px over the build's at the corner) and the Taylor match record re-read.

Piece 2 of 4 of **T-3003 — 1801 Prairie's south and east sides and its rear from the 1929 and HABS photographs: find each picture, solve its camera into data/reference_views/kimball_house_1801_prairie/, and bring the faces the Taylor camera cannot see to them**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## SPLIT WHILE WORK STOOD ON THE PARENT

When T-3003 was split (2026-10-24T09:14:09.287Z), this was already on it. Read it before you claim this piece, and check the PR list for a branch that has already taken it:

- claim — taken 21m ago, run 10/24/2026, 3:53:05 AM CT (https://github.com/kevinrhaas/polecat-platform/actions/runs/40079431083) — held by the run that split it

The run that split it (https://github.com/kevinrhaas/polecat-platform/actions/runs/40079431083) may be working one of the pieces now.

**Acceptance:** One source-bound before/after demonstration of the exact title: two-storey ROUND southwest corner bay under its pierced balcony south of the gabled pavilion; narrower paired-light pavilion with gable re-centered on its face; HABS1 camera re-solved on that rebuilt front and its prior85pxcornice discrepancy explicitly remeasured, then Taylor match re-read. Preserve valid control bearings and otherhouses/accepted placement, record every inferred/reconstructed dimension and phase exclusion, and keep unexplained differences open. Native photo/image-gate code has no generic numericalpixelPASS threshold: prior~10pxHABS and1–3pxTaylor fits are retained comparison controls, not new pass tolerances or substitutes for visual review. Only actual final source-bound render/comparison review may mark a scoped difference fixed; no wholeview MATCH while other visible differences remain. Preserve T-3107's unresolved height/phase issue until the demonstration resolves it; T-3109/10 and fullT-1890 remain OPEN. Require actual final-source canonical outputs, normal preflight/ordinary CI, published all15parts bothwidths, and actual390px HABSphoto/credit/screenshot review. No image-gate or test weakening.


**Grouped resume 2026-10-25T00:40:43.447290+00:00:** Normal replacement draft [#1290](https://github.com/kevinrhaas/chicago/pull/1290) preserves closed/unmerged1278/H747 and carries T-3107+T-3108 together. Implementation and qualification remain PENDING; no MATCH/closure claim.

**Released 2026-10-25** (claim of codex-api-diagnosis-kimball-group-20261025T002647Z 10/24/2026, 7:40:27 PM CT, by https://github.com/kevinrhaas/polecat-platform/actions/runs/40200128019): Resume PR #1290 ships T-3107 alone on the owner's 2026-10-25 handoff ('finish T-3108, or ship T-3107 alone and leave T-3108 to its ticket'); none of T-3108's round bay, pavilion or HABS1 re-solve was built on the branch.

## Finding — slice 5/5, 2026-10-25 (built, measured and reverted; nothing shipped)

**The three sources, read against each other.**
- **The 1911 sheet's trace** (`s28fp-1801-b1`, data/traces/prairie_1904_footprints_s28.json, local x east / y north, the 18th Street wall at y ≈ -3217.4): the front line (u ≈ 20.6) runs x 1418.6-1418.7; the bow's bulge peaks at x 1418.32 (v 6.9); the pavilion's face holds the line to (1418.66, -3226.66) = **v 9.26**, then the line turns back to (1419.59, -3227.65) = v 10.25 (0.93 m behind), (1419.55, -3228.26) v 10.86, and meets the south wall at (1420.02, -3228.70), u ≈ 19.2, v 11.3. So the sheet cuts the corner back about 1.0-1.4 m over about 2 m, where T-3059 read a 0.44 m chamfer.
- **HABS photograph 1** (1800 px copy): the gabled face at **x 455-625**, its pairs at x 480-600, the finial top at (543, 152); the round bay from x 625 to about 750, one window a storey (storey 2 at y 610-690), its pierced balcony at y 520-560 on a cornice at about y 575; the bow's balcony peeks out at x 440-460, y 540-570, so the bow stands mostly hidden behind the pavilion. Pavilion pair rows: y 345-445, 560-700, 780-900.
- **The Taylor print**: the face runs from about x 1240 to 1340 (about 100 px; the current build renders 109 px), the main cornice carried on just past the face's south edge to about x 1345, then the dark neighbour; no bay visible.

**What was tried.** p_south narrowed to the sheet's face (v 6.85-9.4, 2.55 m, pairs centred 1.5 m clear, gable pitch 2.64 to hold the rise), the chamfer dropped, and K01's `round_corner` (its `north` end, radius 1.5 m, the kit's ceiling) laid at the corner; it bakes clean (the south wall's front-corner downpipe has to come off: K01 refuses a pipe on that wall past s 0.5 m). **Reverted because it regresses the Taylor view**: the face renders about 70 px against the print's ~100, and because K01's round is corbelled out to the square under the wall head, the main eave and the mansard's square corner stand about 50 px past the pavilion's south cheek where the print shows the neighbour. Through HABS 1 the narrowed face renders about 100 px against the photograph's 170 (the trial side-by-side was not kept).

**HABS 1's camera cannot be re-solved on the build as it stands.** A least-squares fit (eye, heading, focal, principal point; roll held at -0.93°) on the arch crown (20.5, 1.6, 3.9 m) → (395, 945), the face's edges, the pavilion's three sill/head rows (5.6 / 7.8 / 9.6 / 11.45 m) and the south-east cornice goes unphysical (eye below grade, rms 25-35 px). Read on its own, the pavilion's rows give about 61 px a metre at the face and put the photograph's gable finial near **14.6 m**, where the Taylor-matched build has 16.82 m. So the camera's re-solve is a question about the pavilion's storey heights between the two pictures, not about its corner.

**What the ticket needs, and why it is not an S.** (1) A round corner bay that K01/K08 can build: openings on the round, a pierced stone balcony on its cornice, the main eave and the mansard set back over it (today's `round_corner` takes no openings and squares itself under the wall head; a K08 corner tower stands only on a rear wing). (2) The pavilion's width settled between the sheet's ~2.4 m and Taylor's apparent ~3.7 m: the difference may be the round's near part read as face from the north-west, which only a build carrying the round can show through the Taylor camera. (3) Then HABS 1's camera re-solved with the storey-height question above in view. One kit extension plus a two-camera re-read is about M, not S.

**Released 2026-10-25** (claim of run 10/25/2026, 10:43:38 AM CT, by https://github.com/kevinrhaas/polecat-platform/actions/runs/40207960171): Built the narrowed pavilion and K01 round corner off the 1911 trace and HABS 1, and reverted it: it regresses the Taylor view (the face 70 px against the print's ~100, the squared eave 50 px past the cheek). The round bay needs a kit extension (openings and a balcony on a round corner, the mansard set back over it), and HABS 1's camera re-solve is a storey-height question; measurements are in the ticket's Finding section. About M, not S.
