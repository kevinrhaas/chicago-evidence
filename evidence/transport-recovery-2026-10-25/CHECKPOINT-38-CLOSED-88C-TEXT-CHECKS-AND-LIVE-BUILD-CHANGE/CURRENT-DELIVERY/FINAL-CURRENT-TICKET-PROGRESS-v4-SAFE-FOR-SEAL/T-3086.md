---
id: T-3086
title: Repair planted horse eye UVs while preserving its mechanics
state: done
epic: RENDERING
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-2800
opened: 2026-10-23
closed: 2026-10-25
pr: 1279
claimed_by: Transport recovery continuing saved group after runtime reconnection 10/24/2026, 5:25:25 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-25T15:41:24Z
claimed_run: null
claimed_at: 2026-10-24T10:25:26.697Z
decision: null
decision_answer: null
group: T-3083,T-3086,T-3087
---

Repair planted horse eye UVs while preserving its mechanics.

Piece 1 of 4 of **T-2800 — Build the first anatomically grounded photographic horse master**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## SPLIT WHILE WORK STOOD ON THE PARENT

When T-2800 was split (2026-10-23T23:58:39.740Z), this was already on it. Read it before you claim this piece, and check the PR list for a branch that has already taken it:

- claim — taken 1.2h ago, Codex resumed horse photographic refinement after own merged PR1244 10/23/2026, 5:45:48 PM CT — held by the run that split it
- branch `steward/t2794-t2800-photographic-refinement-20261023-2245` — the splitter's own
- branch `steward/t2800-planted-standing-v16-dev-20261023`
- branch `steward/t2800-standing-idle-dev-20261022`

The run that split it (by hand) may be working one of the pieces now.

## Scope and acceptance

Deliver the bounded dark-eye UV repair to the existing licensed planted-standing
horse, preserving its original body and mechanics. This is not the photographic master.

- Reproduce the versioned d4544c28 derivative from the unchanged b479442c canonical
  baseline using a portable stdlib recipe. Preserve every geometry/normal, rig,
  weight, clip, material and embedded image byte; only the declared ocular UV
  accessor/bounds and explicit derivative notice may change. Reject independent
  non-UV binary/JSON mutations and meaningful destructive controls.
- Root must inspect fixed-camera actual source/candidate textured comparisons on
  both eyes, with all non-eye pixels protected. CPU software-render limitations,
  reconstructed pupil/gaze and the modern model's licence remain explicit.
- Load the exact new SHA through the real GLTFLoader, production clone and Mixer
  at all 65 keys and 64 midpoints with unchanged physical/contact/loop controls.
  Bind the current CPU receipt to its actual fixture; never transfer historical
  b479 browser/world/appearance acceptance to the derivative.
- Update the selected versioned runtime asset and provenance without changing
  placement, natural planted weight shift, budgets or capability/visibility clocks.
  Preserve original assets/receipts and complete integrated app/normal PR gates.

## Saved work

Root reviewed both actual whole-horse quarter comparison pairs. Exact source,
portable recipe, five mutation controls and fresh d454 Mixer129 proof are in
https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence/transport-refinement-resume-2026-10-23
(THIRD-CHECKPOINT and FOURTH-CHECKPOINT). Native/mobile/photographic acceptance
remains open in the sibling master/qualification work.
