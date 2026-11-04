# T-2388 (partial) — the second fort blockhouse's pictured cupola, as shipped

Code: `kevinrhaas/chicago` PR **#1682**, branch
`steward/t2388-blockhouse-cupola-native-20261103`, commit `f447b68a1fbe332d1b5d4375d49ef021a81a53d0`,
based on `dev` `42b9c601d51d8a93cde2706e1773f0bd00fadfbe`. Authored natively on pinned
**Ubuntu 26.04.1 / Blender 4.5.3** (sha256-verified from `generators/blender.pin`).

**This is a bounded partial increment.** T-2388's all-buildings, all-pictures acceptance is NOT
met. The ticket is released OPEN with its remaining differences recorded. No new photo ticket,
no split, no `done --pr`.

## What changed

Panel 5 of `kurz_allison_1893` ("Fort Dearborn as rebuilt 1835", crop sha256
`80c71433bd66455639b535718b936fa343be5e84a88a509dbe9f79e4f7b1818d`) draws a small square cupola
at the centre of the blockhouse's four-sided cap under a little cap of its own, and draws no
stack on that roof; the two Wau-Bun 1831 reproductions
(`kinzie_1857_chicago_1831_panorama`) draw the same body. The cupola is built, through a new
keyword-only, default-off `cupola` control on `fort_structure` consumed by a local `_cupola`
helper — NOT the lighthouse's `lantern` (only `_tower` reads that), not routed through the tower
builder, no shared geometry changed. The invented centre chimney that stood in exactly its
place is recorded at a count of 0, stated in the record as a **depiction choice and not a
finding about heating, flues or later projections**. The 1856 Kellogg/Blanchard print's louvred
cap and ambiguous projection (about 1836-1849) are left unresolved, not backdated.

Occurrence `inferred`; every dimension reconstructed in the archetype and admitted in
`docs/LIBERTIES.md` § `L-second-fort-blockhouse-cupola-2388`. The body is sunk 0.12 m below the
lowest the main roof reaches under its own footprint, so it meets all four sloping planes.
Everything below the roof is untouched.

## The 25-master family, genuinely rebuilt

All 25 current `fort_structure` MASTERs — the accepted 1832 lighthouse and the Lake House
construction shell included — were rebuilt in two bounded native batches before the first source
commit (`logs/build1.log`, `logs/build2.log`). All 25 `inputs_sha256` in `assets/manifest.json`
are the regenerated ones. **Exactly one master's bytes moved**:

| master | before | after |
|---|---|---|
| `fort_dearborn_blockhouse__log_1816.glb` | 134,632 B · `4b49f0dba271d11ce407e6b407c6e4a766402bce04b93b24ebbcc2862f899e00` | 133,092 B · `96d9fb803cdd3b1639c32b9e0c562d0b3bf2af1b2fe8254abea4d62e8e136b15` |

The other 24 came back byte-identical and keep their genuinely bound existing WEB derivatives;
the blockhouse's WEB derivative was re-encoded (29,564 → 28,388 B). No foreign registry row was
touched and no other job's source, claims or branches were gone near.

## Gate and verification, all bounded foreground runs

| what | result |
|---|---|
| `tools/check.sh --part 1/4` | **PASS** — 287 steps, none red (`logs/c1b.log`; first run red only on source-use backlinks, rebuilt with `compile_source_use.py` and re-run) |
| `tools/check.sh --part 2/4` | **PASS** — 287 steps (`logs/c2.log`) |
| `tools/check.sh --part 3/4` | **PASS** — 288 steps (`logs/c3.log`) |
| `tools/check.sh --part 4/4` | **PASS** — 286 steps (`logs/c4.log`) |
| smoke desktop 1280x800 stage 3 | **SMOKE PASS** — 107 passed, 0 failed, zero page errors, 7m01s (`logs/smoke_d3.log`) |
| smoke mobile 390x780 stage 3-4 | **SMOKE PASS** — 139 passed, 0 failed, zero page errors, 7m22s (`logs/smoke_m34.log`) |

Stages chosen from `tools/smoke_budget.mjs --for-diff`: it names parts 1-15 because a structure
record and the asset manifest changed, which is the whole gate; part 3 is the one that actually
covers this diff (the record's own account on the card, the citation, the liberties). Both
readings are filed with `tools/dev-smoke-state.mjs record`. **The whole 15-part gate was not run
and is not claimed.** No gate step reported a missing module.

## Pixels actually inspected

`app/` — the published mirror, default 1835 entry, both viewports, from
`qa_t2388_blockhouse_cupola.mjs` (`logs/qa_d.log`, `logs/qa_m.log`):

* `blockhouse-normal-1280.jpg` / `-390.jpg` — standing south-west of the blockhouse, outside the
  stockade. The cupola stands at the apex, its body coming up cleanly through all four roof
  planes with **no floating corner, no strip of sky and no stack**, under its own overhanging
  four-sided cap. The jetty, log courses, loopholes and openings below it are unchanged.
* `blockhouse-bygrade-1280.jpg` / `-390.jpg` — the Confidence view's By-grade preset.
* `card-images-1280.jpg` / `-390.jpg` — the card reads **"Attested. Pictured: a picture on the
  Images tab shows it."**, and the Images tab carries 2 credited public-domain pictures: the
  Wentworth 1881 keyed reproduction of the 1831 Wau-Bun view and the Kurz & Allison 1893 sheet,
  each with repository, date and rights, link-only (no new held media).
* `card-record-1280.jpg` / `-390.jpg` — the Record pane and its dossier link. The Evidence tab
  lists `cupola` among the 7 inferred claims, reasoned from Kurz & Allison among others.

The grade derives `attested` from an explicit **pictured ruling** in
`data/structure_grades.json` that states why panel 5 is a reasonable whole picture — not
hand-typed, and not taken as a camera-fit shortcut.

## What is NOT claimed

The compound view's verdict is **`differs`**. Only the roof assembly is `fixed`. The camera is
the T-3040 landmark fit reused unchanged as a before/after control; it reached its imposed 100 m
eye bound, renders the compound aerial and undersized, and is marked `diagnostic_only` so no
invented "from this spot" is offered. Still open: the camera's own fit, the galleried range's
identity, the facade openings, the other roof forms and chimney counts, the compound's
composition, and every other dated picture T-2388 lists. The 15-part smoke gate as a whole was
not run. Production was not moved; merge is to `dev` only.
