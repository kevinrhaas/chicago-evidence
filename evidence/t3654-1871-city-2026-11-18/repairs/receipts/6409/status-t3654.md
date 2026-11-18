## T-3654 — A citywide pre-fire baseline for 1871 (2026-11-18)

The owner asked for the whole city as context before detailed properties: varied generic
buildings appropriate to each district, streets and walks, bridges and other structures.
`data/scenes/1871.json` opens 8 October at 16:00 local mean solar time on its own pre-fire
terrain. An explicit empty named-structure allowlist keeps broad phases authored for other
years out. The 1869 boundary, corrected 1870 Mitchell map registration, period
panorama and public-works record guide `data/context/1871/plan.json`. Context footprints,
facades, grades, district density and infrastructure detail remain reconstructed. The
Saturday Night Fire has an uncertainty mask excluding intact buildings.

The registration now uses 28 fitting intersections and eight reserved checks. Correcting
misread street intersections reduced fitting RMS from 37.73 m to 18.67 m; on the same
eight independent checks, the original transform's 49.97 m RMS falls to 15.62 m
(maximum 25.65 m). Flexible warps performed worse in geographically withheld districts,
so the shipped transform remains affine. Raw map pixels, projected features, original
registration, model comparisons and compact versioned OSM control primitives are retained
under `data/traces/`. These are intersection-registration results, not measured accuracy
for banks, parcels or vertical grades. A newly inspected August 1869 federal harbor chart
provides finer relative shoreline geometry; its absolute placement and changes before
October 1871 remain separate research questions.

The existing Today/Google Maps navigation alignment supplies a second modern-data
cross-check: nine shared City-centreline and OSM intersections agree within 2.023 m
RMS (3.854 m maximum), and fourteen inherited control targets match exactly. Both
paths use the same local EPSG:26916 frame. The older years’ display shifts belong to
their own reconstructed grids and are not transplanted into 1871. See
`docs/measurements/t-3654-today-registration-audit.json` for source hashes, exact
coordinates and reproduction instructions. This downtown comparison does not reduce
the historical-map residuals or establish that street centres stayed unchanged.

An independent overlay review also corrected river/fork identities and bends, the
Goose Island canal, six road or railway routes, shoreline and cemetery boundaries.
The research viewer retains a reproducible original-pixel overlay. The resulting
baseline contains 33,580 generic buildings, 3,627 trees, 22 road crossings (21 in
the public-works inventory and one separately map-attested canal crossing), 597
quay bays and five rail corridors. These are generated scene counts, not a census.
The 10 m heightfield preserves the modeled banks with a separate resampling audit;
its finer numerical agreement does not reduce historical feature uncertainty.

The portable kit supplies sixteen building families and original embedded procedural
surface maps; deterministic placements vary form and colour by district. The scene adds
city/district viewpoints and navigation, with its own arrival deck. Nearby spatial queries
make context buildings solid without scanning the entire city on each footstep; bridge
decks, quay floors, roads and plank walks use the same walk surfaces as their visible
geometry. The full width of streets and walks stays on supported ground. Distant tile batches keep the
whole city present while reducing draw calls. See L-1871-city-baseline and the generated
asset inventories for scope, inputs and rights.

The afternoon uses a declared sky exposure grade shared by the visible sky, reflected
light and sampled haze. This corrects the night-like backdrop at the dated low sun;
it changes neither the solar position nor the earlier years' default calibration.
Atmosphere remains a presentation reconstruction, not a recorded weather observation.

Published-app acceptance passes at 390×780 and 1280×800 across all three detail
levels: every bridge in both directions, all 597 quay approaches, road/plank-walk
transitions, building collision, source cards and confidence filtering, with no
application, page or resource errors. The measured maxima are 460/548 driver draws
and 682,504/796,657 submitted triangles (mobile/desktop). These are headless
SwiftShader readings, not physical-device frame-rate or GPU-memory claims;
`docs/measurements/t-3654-city-baseline.json` retains the inputs and conditions.
The portal plate is an actual canvas capture of this final dated city.
Year doors share one renderer page while retaining their clean URLs, deep links and
offline packs; native 1835/1871 entry and nine browser fixtures pass. See
`docs/measurements/t-3654-entry-pages.json` for the dated evidence.

This implementation is checkpointed while final repository and legacy-scene verification
continues. `docs/measurements/t-3654-validation-checkpoint.json` records completed checks,
remaining CI coverage and resumption commands. A checkpoint is not a completed release gate. Source part 7 exposed missing 1871 benchmark poses,
aerial-anchor measurement handling and a stale shared source catalog. These are repaired
with focused positive and negative checks, preserving the city geometry and historical
claims; `docs/measurements/t-3654-integration-repairs.json` records their exact scope. Full
source verification precedes the next browser regression run.

Final review also found that the new context casters used default shadow materials,
so Confidence-mode dither or hiding did not reach their shadows. Near buildings,
trees and bridge batches now own confidence-patched depth materials per color
material, including the existing texture/alpha state and disposal. The focused test
passes on the repair and fails on the original casters; the existing confidence
suite also passes. A native desktop Full probe confirms unchanged normal shadow
coverage, reduced dither coverage and zero hidden coverage at building, bridge and
tree viewpoints, with no errors. Exact runtime bindings and sampling limits are in
`docs/measurements/t-3654-confidence-shadows.json`.

The source library now collects the actual context records and kit citations, so
Edwards' 1871 Directory appears in the scene's source-use map. The initial native
probe reproduced its omission from the default list while all eleven new source
details resolved correctly. Sixteen compiler fixtures and the strict confidence
audit pass. The startup packer also handles 1871's empty named-structure index with
a valid empty shared table, retaining strict missing-record and rehydration checks.
The full published `c0c235` build passes mirror checks and rehydrates all 1,119 named
records across the scenes. Native 1871 startup succeeds with 33,580 context buildings
and the empty named-structure pack; Edwards appears by default, and actual building/tree
cards plus all eleven new source details resolve with zero errors. This focused desktop
Light check is recorded in `docs/measurements/t-3654-source-and-boot.json`.
The latest dev roof corrections and changelog fold are integrated. Local source part 12
then identified two gate issues: rounded bare sums in the harbor trace and missing
step-isolation measurements for seven new tools. The trace uses precise summation and
its derived coordinates remain byte-identical. All seven tools now pass actual write
probes without modifying the repository; the complete isolation census and its self-tests
pass. Full combined-tree source and browser gates remain required before the authorized
dev merge.

The saved `871698` checkpoint has complete source-assertion coverage across the
successful hosted parts and their verified local counterparts: all 1,379 declarations
were exercised successfully. Its hosted aggregate is not claimed green: one section
hit the unchanged 600-second limit, and that timeout contributes no coverage. Both
supporting browser workflows passed. Before fresh legacy browser runs began, `dev`
advanced with the corrected 1893 monument and its changelog fold. Those changes are
integrated through `150fb1d3`; all 201 audited 1871/pre-fire/runtime paths are unchanged,
and the upstream assets/photo proofs are preserved. Full-checkout freshness, derived
records, source-use and changelog checks pass. The new combined version still needs
publication and its complete source/browser verification; dated prior-tree results are
kept as evidence rather than silently credited to the new tree.

Regenerate with `python3 generators/city_context_emit.py`, then
`python3 generators/city_1871_emit.py`, `python3 tools/compile_scene.py --scene 1871`
and `python3 tools/compile_jaunts.py`. Register the terrain entries from
`data/context/1871/generated-assets.json` in `assets/manifest.json`, then run
`tools/web_derivatives.sh --only terrain__e1871_prefire.glb,water__e1871_prefire.glb`.
The map-fit and both deterministic generator checks are in `tools/check.sh`; the
published scene has a dedicated `tools/smoke_city_1871.mjs` browser check. This is the
complete context baseline, not a claim of individually surveyed buildings, populated
daily activity or photographic finish.

