## What

The first fort's north-east small house carries the four-sided pyramid cap the Currey 1912 bird's-eye draws in that angle, instead of a gable. **T-3041 is a partial increment and stays OPEN** — one of the thirteen differences on that picture moves; the view's verdict is still `differs`.

`first_fort_dearborn_small_house_ne.first_fort_1803.form.roof_type`: `gable`/`reconstructed` → `pyramid`/`inferred`, cited to `currey_1912_first_fort_birdseye` and to Whistler's 1808 draught (which identifies the building, his index no. 16, and is silent about its roof).

## Why

Owner ruling of 2026-11-03 (T-3335), recorded on T-3041: of the Currey plate's departures from Whistler, adopt the blockhouse cupolas, the magazine's vault, **this house's pyramid roof** and the western gate, and keep Whistler's measured plan for everything else. This PR builds the third of those four and nothing else.

The plate was opened and read directly before any edit: at the north-east inner angle it draws a point apex, two hips to the eave corners and no ridge, with only the cap clearing the picket row. So the drawing supplies the roof's **topology and nothing else** — it is a 1912 retrospective after an 1899 sketch of an 1898 model, its camera here is `diagnostic_only`, and it is not metric. The 34° pitch stays **reconstructed**, the footprint stays the register's half-measured 12.2 × 10.0 ft, the 2.4 m wall stays unattested, and the surveyed seat, bearing and 75 ft staff are untouched. None of them was moved to fit the plate.

## How

An **opt-in `pyramid` branch** in `outbuilding.py` / `outbuilding_params.py`, never defaulted (`default_roof_type` still answers gable or shed only).

- `roof_run_m` already reads half the **short** span, so `roof_rise_m` (1.0286 m) and `apex_z_m` (3.4286 m) are right for a rectangular pyramid with **no new equation** — audited, not invented.
- `_top_z` returns a level wall head on every elevation; `_top_break` already returned `None`.
- A **triangular covering** was needed: `_roof_plane` sorts a quad into two low and two high corners and walks off the end of a triangle. `_pyramid_face` lays the same jittered boards up the slope and cuts each at the hip, so they tile the face exactly — no pile of them at the apex, no bare wedge beside each hip — and the board the apex stands over is emitted as two quads so the point is not cut off.
- **The eave is the footprint scaled about its centre, not grown by a constant margin.** `fort_structure._hip_roof` does the latter, correctly, over the square plans it serves; on this 3.72 × 3.05 m rectangle it would leave the two long walls standing **23 mm** through their own roof, because the long-span faces must be shallower to reach the same apex. Scaling instead makes all four planes pass through the wall head **exactly — measured 0.000 m** — at the price of an overhang of 0.258 m across the long span against 0.212 m across the short one. This archetype's standing promise is that `_top_z` and the roof agree exactly, so exactness won; the asymmetry is recorded as a liberty.
- A pyramid with an **open side, a loft or a chimney is refused** with a reason, rather than approximated by borrowing machinery that means something else. Every gable and shed path is unchanged, as are this building's walls, materials, 0.86 × 1.88 m batten front door and rear vent.

## The 243-asset cost, and what it actually moved

`outbuilding.py`'s bytes are hashed into every outbuilding's mesh inputs, so one branch stales **all 243 committed outbuilding masters**. Every one was regenerated on the pinned, **sha256-verified** Blender 4.5.3 (`generators/blender.pin`) on Ubuntu 26.04 **before the first source commit**, in bounded foreground batches:

| | |
|---|---|
| masters regenerated | 243 (22.5 s, one Blender start-up) |
| bytes moved | **180** — NE roof geometry plus 179 unused UV repacks; the 179 default meshes have byte-exact positions, normals, colours, indices and materials |
| byte-identical | 63 |
| web derivatives re-encoded | 180, in two batches of 90 (173 s + 166 s) |
| web derivatives that **changed** | **1** — this house's; all 179 other WEB blobs are byte-exact |

**Independent integration audit, 2026-11-04:** the earlier attribution to sub-millimetre hardware float noise was incorrect. Across all 179 changed default MASTERs every POSITION, NORMAL, colour and non-UV accessor is exact, as are indices, nodes, meshes and materials. Only `TEXCOORD_0` was repacked (maximum UV-component delta 0.974573); none of these files binds a texture or image. Their served WEB blobs remain exact. The remaining changed MASTER/WEB pair is the intended NE roof. The failed initial audit assumption and the corrected measurements are preserved in the integration evidence.

No freshness hash was predicted or written by hand. `validate.py`'s staleness gate reports **1034 assets match their inputs, 0 stale**. No foreign registry row was touched, and nothing of the frame_dwelling/Jail work was modified.

## Verification

Run here, in the foreground, each inside the 600 s cap:

- `./tools/check.sh --part 1/4` → **PASS**, 287 steps (423 s)
- `./tools/check.sh --part 2/4` → **PASS**, 287 steps (343 s)
- `./tools/check.sh --part 3/4` → **PASS**, 288 steps (383 s)
- `./tools/check.sh --part 4/4` → one red, `dataset (…)`: L370 and the new entry both claimed a `roof_type` that is no longer invented. Both registers were corrected (L370 stops claiming it; the new entry supersedes L370 for this one value and covers the pitch alone) and **`python3 tools/validate.py` — the step that was red — re-ran green on the final tree: `PASS 0 error(s)`.**
- `node tools/changelog-entries.mjs --check` → OK; `tools/compile_liberties.py --check` → OK; `tools/compile_source_use.py --check` → OK.
- Before/after compound renders through `tools/photo_match.mjs` on the existing 14-member Currey camera (`first_fort_dearborn_pickets_outer`, scene 1812), **inspected directly**: the ridge that used to cross that angle is gone and the cap converges to a point. The group hash was invalidated by the peer GLB and the match record was regenerated and rebound.

**Stated plainly:** parts 3/4 and 4/4 were **not re-run whole** after that last liberties-register edit — the clock ran out — so the authoritative whole-gate run is this PR's own CI, which runs `check.sh` entire. The fifteen-case smoke was not re-run and is not claimed. Do not read this as a whole-gate pass taken here.

## Scope — what is NOT done

T-3041 and its parent T-2387 are **not finished** and T-3041 is released OPEN. Still `open` on the match record: the blockhouse cupolas, the magazine's barrel vault, the western gateway. The full first-fort acceptance — 21 named records, nine context records, every listed picture — is untouched by this increment. The NE house was **not** added to the picture's `card_members`: that would read as the 1912 retrospective attesting the building, which it cannot do, and it is explicitly optional.

Registers updated in this PR: `docs/LIBERTIES.md` (new entry + L370 narrowed), `docs/STATUS.md`, `docs/ROADMAP.md` (reasoning archive), `changelog.d/T-3041.json`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
