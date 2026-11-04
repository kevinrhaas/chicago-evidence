# PR1690 exact resume — the lower-aperture depth repair, with its actual pixels

Companion to the pre-gate checkpoint
[`pr1690-exact-resume-depth-repair-wip-41766`](../pr1690-exact-resume-depth-repair-wip-41766/RECOVERY.md),
which was saved BEFORE any long gate. This folder holds what was produced after it.
**Nothing here claims a camera solve, a match verdict, a grade or a completed image
gate.** T-2374 stays OPEN / PARTIAL / DIFFERS.

## The controlled pair is a genuine reproduction, not a new experiment

Three renders at the SAME retained private camera (`07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977`)
on the SAME source (`624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f`),
with the project's own `tools/photo_match.mjs` and nothing but the GLB changing. All
writes went to a private external fixture; no canonical reference view, grade, verdict or
repo camera was touched.

| mesh | MASTER sha256 | bare render sha256 | 8× fixed crop `[1380,330,1500,420]` |
|---|---|---|---|
| original (one centred door) | `af1f33c0…561f` | `a893bf59105fff73e7d1068192d321666ed98fd6085da9084a9054ef83c4a32d` | `0c215929387d6f80a0679faf5e1a316d7b220c66761124f2987c11acd2b34145` |
| striped (PR1690 as authored) | `4f42207b…5fbea` | `6f8bbb144778fb063ffb40c75c11cbae64b99dc4b68bbe0097904ac321da28f3` | `e2a7020322a4364135ce7305c54b706e589b87941cdd475d147368110726db10` |
| **repaired (this work)** | `1ddf548d…ee82` | `fe496a9fef4df97e6649a0e5a6df0473721e392c5d0507353f6b072c77e7c1c7` | `76920874cce6fc8ee17ba92313ca3aaa6f761df8c045288be6520bcb1c10b9e1` |

The first two rows are **byte-identical to the review's own `before-bare-render.png` /
`after-bare-render.png` and its `before-/after-same-fixed-crop-8x.png`** in
`../pr1690-controlled-pair-local-depth-defect/`, and the source crop reproduces
`955124de…` exactly. That identity is the point: it shows the third render differs from
them because the mesh differs and for no other reason. Those earlier striped images stay
where they are as failed evidence; nothing was renamed or overwritten.

`*-lower-pair-24x.png` is the same two grounded apertures at 24×, from the same
pre-existing crop rectangle family, nearest-neighbour, with no annotation, enhancement or
fit. Read directly: in `striped-` both lower faces are crossed by horizontal log courses
and read as ladders; in `repaired-` both read as uninterrupted dark upright recesses. The
upper gable light, the casings, both wings' single windows, the two stacks, the roofs and
the massing are unchanged between them.

`repaired-private.match.json` is the record photo_match wrote beside the private camera.
It stays `unreviewed` and private. **The camera remains UNSOLVED and unenrolled**; its
earlier front RMS of 1.848 px and held-out rear of 20.751 px do not solve it and are not
restated as a fit here.

## Source gate, run before the first source commit

`tools/check.sh --part k/4`, four bounded foreground calls: 292 / 292 / 291 / 291 steps,
391 s / 315 s / 302 s / 243 s, **all four PASS, none red** (`check-part-*-of-4.tail.log`).
No step stood on a banked reading; the only "not installed" lines are the tagged self-test
proving that warning fires. Preflight's two PR-only questions answered separately:
changelog entry present against merge base `22d624f3e`; id collisions not applicable.

Environment-only: this runner's NumPy 2.5.4 removed `np.cross` on 2-vectors (reproduced
directly), so numpy was pinned to **2.3.5** to align with CI, per T-3368. No source
assertion was bypassed.

## Smoke, and an honest red that is not ours

- `mobile 3-4 --published` — **SMOKE PASS**, 139 passed, 0 failed, 5 m 54 s.
- `desktop 3 --published` — **SMOKE PASS**, 107 passed, 0 failed, 5 m 51 s.
- `mobile 1-2 --published` — 193 passed, **5 failed**, all of them the Green Tree Tavern's
  yard (0 sheds, covered wagon MISSING, 80 frontages refused).

The five were attributed rather than assumed: the identical leg was run on a **pristine
`origin/dev` worktree**, published from that tree, and returned **193 passed, 5 failed
with the identical five names** (`smoke-mobile-1-2.PRISTINE-DEV.tail.log` beside
`smoke-mobile-1-2.branch.tail.log`). This branch touches nothing in that neighbourhood and
`renderers/` not at all. Both readings are filed with `dev-smoke-state.mjs record`. The red
belongs with T-2376 / PR #1684; it is not hidden and it is not a missing-load error.

## What is NOT claimed

No camera solve, no enrolment in `data/reference_views/`, no RMS or metric fit, no
From-this-spot link, no grade change, no `matches` verdict, no completed image gate, no
glass, interior, attic room, white paint or historic function for any of the three marks.
The compound's overall width, the wings and sub-roofs, the roof junctions and valleys, the
text-attested partial clapboarding, and the finish and tone all still differ from the
picture. The source is retrospective 1831 context printed in 1881. No photo follow-up
ticket was filed, no split, no sign-off.
