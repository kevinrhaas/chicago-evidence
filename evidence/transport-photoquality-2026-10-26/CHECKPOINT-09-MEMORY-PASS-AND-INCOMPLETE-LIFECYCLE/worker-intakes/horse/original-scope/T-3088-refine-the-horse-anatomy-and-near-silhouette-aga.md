---
id: T-3088
title: Refine the horse anatomy and near silhouette against cleared views
state: claimed
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2800
opened: 2026-10-23
closed: null
pr: null
claimed_by: Codex root horse_resume continuing owned canonical anatomy in this session 10/26/2026, 1:58:09 PM CT
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: null
claimed_at: 2026-10-26T18:58:10.380Z
decision: null
decision_answer: null
---

## Current photo-quality progress — 26 October 2026

Checked safe hoof/body source is pushed at [db71c0c6](https://github.com/kevinrhaas/chicago/commit/db71c0c6d84b17d1bcc3786f872d0b2595a85ce4), in [draft PR1347](https://github.com/kevinrhaas/chicago/pull/1347). Complete native preflight passed1071 checks/384 intentional self-tests in783.358 seconds, with zero-child cleanup; actual committed-HEAD checks and remote hash confirmation pass. The600-second timing target remains exceeded. The geometric upper-eye hood remains open. A separate strip prototype is not adopted: source/topology checks passed, strict crossing qualification failed, and independent diagnosis places all24 body-crossing segments inside the existing embedded eye interface. Its16 matched diagnostic images show less drooping lid bulk but do not establish anatomical/photographic or deformation acceptance. A source-bound interface qualification design is being reviewed; current925 model remains unchanged.

Checked-source receipts, actual diagnostics and retained failures: [transport checkpoint05](https://github.com/kevinrhaas/chicago-evidence/tree/4aafe1f3a2b6000bb59e64d80e3d127c68905d27/evidence/transport-photoquality-2026-10-26/CHECKPOINT-05-CHECKED-PEOPLE-AND-ACTUAL-FAILURES). This progress update does not close the ticket.

Refine the horse anatomy and near silhouette against cleared views.

Piece 3 of 4 of **T-2800 — Build the first anatomically grounded photographic horse master**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## SPLIT WHILE WORK STOOD ON THE PARENT

When T-2800 was split (2026-10-23T23:58:39.740Z), this was already on it. Read it before you claim this piece, and check the PR list for a branch that has already taken it:

- claim — taken 1.2h ago, Codex resumed horse photographic refinement after own merged PR1244 10/23/2026, 5:45:48 PM CT — held by the run that split it
- branch `steward/t2794-t2800-photographic-refinement-20261023-2245` — the splitter's own
- branch `steward/t2800-planted-standing-v16-dev-20261023`
- branch `steward/t2800-standing-idle-dev-20261022`

The run that split it (by hand) may be working one of the pieces now.

## Scope and acceptance

Finish one horse's source-bounded anatomical near master, retaining T-2800's
unmet anatomy/topology and source-comparison requirements. No fleet/breed variants.

- Use cleared anatomical and dated period references to define scale, body
  proportions, head/eyes/ears/muzzle, neck/shoulder, limbs/joints/hooves, mane and
  tail. Keep this a generic working animal, not an identified horse or claimed breed.
- Resolve actual near silhouette/anatomy discrepancies at matched front, profile,
  quarter and detail views. Inspect the actual images and maintain a discrepancy
  register; do not treat the eye-only child as acceptance of the whole head/body.
- Provide a source-bounded canonical master with clean supported topology for
  T-2803. Test metre scale/axes, connected joints and weight-bearing hoof contact;
  every changed geometry/skin must have fresh protected-source and exported proof.
- Retain rights/modern attribution, per-attribute confidence and liberties for
  coat, grooming, unknown dimensions and unpictured features. Do not derive from
  rights-pending references or invent Chicago ownership.
- Use the supported canonical build path, without installing Blender on the
  improve runner. Hand exact accepted master hashes to the surface/LOD sibling.
