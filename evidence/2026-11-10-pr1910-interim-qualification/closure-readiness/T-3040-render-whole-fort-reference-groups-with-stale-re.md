---
id: T-3040
title: Render whole-fort reference groups with stale-review protection
state: done
epic: TOWN
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-2387
opened: 2026-10-22
closed: 2026-10-22
pr: 1218
claimed_by: run 10/22/2026, 5:47:36 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-23T00:35:18Z
claimed_run: null
claimed_at: 2026-10-22T22:47:37.490Z
decision: null
decision_answer: null
---

Render whole-fort reference groups with stale-review protection.

Piece 1 of 2 of **T-2387 — Match the first Fort Dearborn (1812) to its pictures, every building in it**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## SPLIT WHILE WORK STOOD ON THE PARENT

When T-2387 was split (2026-10-22T22:45:49.575Z), this was already on it. Read it before you claim this piece, and check the PR list for a branch that has already taken it:

- claim — taken 1m ago, run 10/22/2026, 5:44:36 PM CT — held by the run that split it
- branch `steward/t2387-t2388-fort-reference-groups` — the splitter's own

The run that split it (by hand) may be working one of the pieces now.

**Acceptance:** Demonstrate one camera rendering all requested scene members, including both complete fort inventories, with correct relative bearings/origins; regression tests refuse missing or wrong-scene members and invalidate review after a peer mesh or placement changes. Save actual compound baseline renders and document calibration limits. This is the tool prerequisite for T-3041 and T-2388, not completion of their image gates; no geometry or matches verdict is claimed.
