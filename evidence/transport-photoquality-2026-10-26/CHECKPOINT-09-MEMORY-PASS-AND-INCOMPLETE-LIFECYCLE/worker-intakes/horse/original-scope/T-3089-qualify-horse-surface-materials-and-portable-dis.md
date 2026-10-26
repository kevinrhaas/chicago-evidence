---
id: T-3089
title: Qualify horse surface materials and portable distance exports
state: open
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2800
opened: 2026-10-23
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: null
claimed_at: null
decision: null
decision_answer: null
---

Qualify horse surface materials and portable distance exports.

Piece 4 of 4 of **T-2800 — Build the first anatomically grounded photographic horse master**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## SPLIT WHILE WORK STOOD ON THE PARENT

When T-2800 was split (2026-10-23T23:58:39.740Z), this was already on it. Read it before you claim this piece, and check the PR list for a branch that has already taken it:

- claim — taken 1.2h ago, Codex resumed horse photographic refinement after own merged PR1244 10/23/2026, 5:45:48 PM CT — held by the run that split it
- branch `steward/t2794-t2800-photographic-refinement-20261023-2245` — the splitter's own
- branch `steward/t2800-planted-standing-v16-dev-20261023`
- branch `steward/t2800-standing-idle-dev-20261022`

The run that split it (by hand) may be working one of the pieces now.

## Scope and acceptance

Qualify the single accepted anatomical master from the sibling anatomy child as
the full static photographic/portable horse delivery originally required by T-2800.

- Skin/coat, eyes, muzzle, hair and hooves must read at near view. Use browser-suitable
  mane/tail geometry and materials, declared reconstructed colour/grooming, and
  preserve the accepted exact anatomical shape unless a new proof accompanies it.
- Produce compressed near/mid/far GLBs, engine-neutral sidecars, tested metres/axes,
  licence provenance and bounded material/texture reuse through the supported
  export pipeline. A single unqualified near GLB is not complete.
- Compare actual native front/profile/quarter/detail renders with cleared reference
  plates at the same views, inspect the images, resolve the discrepancy register
  and record which surfaces/dimensions/colours remain reconstructed.
- Load the exact published exports in current desktop and phone browsers; measure
  triangles, materials/draws, textures/memory, bytes and frame cost at unchanged
  caps, including near/mid/far transitions and actual placement/support clearance.
- Complete normal source and published desktop/mobile qualification. Do not infer
  walking/trot, tack, riders, teams, driving or boarding from a static-animal pass;
  those remain the existing T-2803/T-2804 and gear/traffic tickets.
