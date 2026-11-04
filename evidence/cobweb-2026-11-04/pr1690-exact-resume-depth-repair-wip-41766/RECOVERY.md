# PR1690 exact resume — UNQUALIFIED working source + raw native receipts

**Nothing here is a pass.** This is the raw, pre-gate checkpoint the exact-resume handoff
asks for: the working source of the local depth repair, the actual native logs and the
real before/after hashes, saved BEFORE the four source-check parts and the smoke run, so
the work survives a run that does not finish. No source gate has been run on this tree
yet, no application check has been made, and the corrected pixels have NOT yet been
rendered. Treat every claim below as "this is what was executed", not "this is green".

## Ownership, verified fresh before any write

- PR [kevinrhaas/chicago#1690](https://github.com/kevinrhaas/chicago/pull/1690) — OPEN,
  base `dev`, head branch `steward/t2374-cobweb-front-apertures`, saved head
  `e9d93bf385623353a2134a18a98b959fbd84efb7`, label `resume`, no `hold`.
- T-2374 — `open`, `claimed_by: null`, `pr: null`; `ticket.mjs inflight` shows this
  branch with "no lap lock"; `ticket.mjs claims` holds no lap lock for PR 1690.
- Previous worker, polecat-platform run 41746386858 — `status: completed`,
  `conclusion: failure` (max turns), ended 2026-11-04T02:38:37Z. It is not live.
- Claimed here through the ordinary protocol after those checks.

## The defect, and the repair as written

`generators/archetypes/log_dwelling.py` blob `6698bda4bd92ba2a974b8282aa0df469f59d3595`
at line 1462 passed the bare constant:

    openings.face(b, w, APERTURE_BACK_M, u0, u1, z0, z1, conf, M_DARK)

`openings.face(b, w, n, …)` measures `n` from the wall's PLANE. `openings.surround(…,
back=k)` runs its reveal back to `w.skin + k`. With `APERTURE_BACK_M = 0.004` and the
log wall's `RELIEF_M = 0.022`, the dark face landed at 0.004 m while the log courses
bulge to 0.022 m and the reveal ended at 0.026 m — so the courses crossed both grounded
apertures as stripes. The repair passes the same absolute offset the surround uses:

    openings.face(b, w, w.skin + APERTURE_BACK_M, u0, u1, z0, z1, conf, M_DARK)

0.026 m, just proud of the relief, which is what `APERTURE_BACK_M`'s own comment says it
is for. It is the convention `_opening`'s blind doorway already follows in the same file
(`back = -0.30 - w.skin` beside `face(…, -0.30, …)`). No shared helper
(`common/openings.py`, `logwork.py`, `mesh.py`, `emit.py`, `materials.py`), no schema,
no recipe scheme and no camera, grade or match verdict was touched.

`source-repair.diff` is the whole authored diff. It also extends
`tools/test_log_compound_apertures.py` with a source-read guard on exactly this
invariant (the surround's `back` and the face's offset must be the same absolute
offset, and that offset must exceed `RELIEF_M`). Negative control, actually run:
reverting the one expression makes the new check FAIL ("and the dark face is given that
same absolute offset (APERTURE_BACK_M)", 1 failure); restoring it passes 47 checks.
`test_log_compound_apertures.log` is the passing transcript.

## Current dev, integrated into the same existing branch

Merged `origin/dev` at `22d624f3e` (T-3041, the first fort's north-east small house)
into this branch as `0a1a2341c`. Three authored conflicts, all append-only files:

| file | resolution |
|---|---|
| `docs/LIBERTIES.md` | BOTH entries kept — dev's `L-first-fort-ne-house-pyramid-3041` first, then this branch's `L-cobweb-apertures-2374` |
| `data/liberties.json` | derived, not hand-merged: `tools/compile_liberties.py` re-run (993 liberties; both ids present) |
| `data/sidecars/1835/sources/index.json` | derived: `tools/compile_source_use.py` re-run (559 sources, 229 663 raw bytes, all source IDs resolve) |

No foreign registry row was hand-won. Current head of this branch: `0a1a2341cda9a96a54f4618964889702e2ab3f3f`
(the merge; the repair is still uncommitted working source at the time of writing).

## Native rebuild — actually executed, before any new source commit

Pinned Blender **4.5.3** on **Ubuntu 26.04.1 LTS**; the cached tarball's sha256 was
verified against `generators/blender.pin` (`975c58fc…d845`) before use.

82 `log_dwelling` structure records enumerated from `data/structures/*.json` — the same
roster the handoff names — rebuilt in four bounded foreground batches of 21/21/21/19
(3 s, 2 s, 2 s, 1 s). Then `tools/stale_derivatives.py` → `tools/web_derivatives.sh
--only` (16 s), `tools/compile_scene.py --all` (15 s), `tools/generate_entrances.py`,
`tools/publish.sh` (57 s).

**81 of the 82 masters came back byte-identical** (`masters-before.sha256` vs
`masters-after.sha256`, `comm -12` = 81). Only Cobweb's moved:

| | before this repair (PR1690's striped output) | after this repair |
|---|---|---|
| MASTER `assets/gltf/cobweb_castle__log_1820.glb` | `4f42207be5fcb2391fda58672ce8442b02aba9510f3096db8c2934b695fe7bea` (139 248 B) | `1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82` (139 248 B) |
| WEB `assets/web/cobweb_castle__log_1820.glb` | `1699d7aa1c4b0abb6229bd4cbfaed95013f3ede9323f4945396583fd14b26e23` (30 304 B) | `99997b5f3935ceceddb072286387859a5d9a8dd3dfa112b64978d1213e20890e` (30 304 B) |

The published mirror carries that same WEB byte string at
`site/4d/data/gltf/cobweb_castle__log_1820.glb`.

`assets/manifest.json` changed in exactly 82 lines, all `inputs_sha256` — one per
log_dwelling master, which is what a producer edit does. `assets/manifest.web.json`
changed in exactly ONE line, Cobweb's. The six `versions/…` snapshots
`stale_derivatives.py` listed as unrecorded re-derived byte-identical and are unchanged
in the tree. `data/enclosures/town_entrance_aprons.json` is unchanged: the repair moves
a depth, not a rectangle, so the grounded entrance and its apron keep their ground.

## What has NOT been done at this checkpoint

- No `tools/check.sh` part has been run on this tree. The four parts are next.
- No smoke leg, no application review, at either viewport.
- **No controlled before/after render of the corrected GLB yet**, so the striping is
  not yet shown repaired in pixels. The previous striped images stay as failed
  evidence at `pr1690-controlled-pair-local-depth-defect/`.
- No source commit. Nothing pushed to the code branch beyond the dev merge.
- The panorama's camera stays UNSOLVED, unenrolled and private. No RMS, no
  From-this-spot link, no grade change, no `matches` verdict, no completion.
  T-2374 stays OPEN/PARTIAL/DIFFERS: compound width, wings, sub-roofs, roof junctions,
  the text-attested partial clapboarding, finish and tone all still differ.

## Remaining work, precisely

1. `tools/check.sh --part k/4` for k = 1..4, one bounded foreground call each.
2. Commit the repair, push, publish the integrated head.
3. Controlled before/after at the retained private camera `07f94fa8…` on source
   `624d8f1f…`, and publish those pixels for direct review.
4. `smoke_budget.mjs --for-diff` legs, both viewports, plus the desktop 1280×800 and
   phone 390×780 application check with zero page/console/network/server errors.
5. The named full hosted `gate` on the final head — all eight required parts, not a
   `report`/`warranted`/single shard — then an ordinary protected merge into `dev`.
6. `ticket.mjs release T-2374` back to OPEN with the remaining differences.
