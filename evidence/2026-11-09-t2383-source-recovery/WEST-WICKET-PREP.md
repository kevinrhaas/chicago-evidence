# First-fort west wicket: bounded read-only prep, 2026-11-09

Status: proposal only. No source changes, claims, tickets, API writes, bake, native request or runtime verification performed. Parent is sole source writer. This is a possible next Native15 after Sauganash25, never a dependency of that work.

## Evidence and finite conclusion

Directly viewed the current 1802x588 Currey source/current-model pair at `docs/RESEARCH/photo-match/first_fort_dearborn_pickets_outer/currey_1912_birdseye-side-by-side.jpg`. The drawing labels western gateway 3 immediately south of northwest blockhouse 4, beside the west range. The current model shows continuous west pickets there. Current match has exactly one open discrepancy, that gateway. T3335 owner adoption delegates the fix to existing T3041 under T2387; no new ticket is needed.

Source: `data/sources/currey_1912_first_fort_birdseye.json`: Currey, *The Story of Old Fort Dearborn* (1912), p27, Commons `Birds_eye_view_of_first_Fort_Dearborn.jpg`, also Gutenberg ebook52346 p27. Public domain, verified, retrospective tier5. The source record expressly supplies gateway identity, no dimension/coordinate/bearing. It reports an 1899 Tribune drawing of an 1898 model without independently inspecting those originals. Whistler1808 register expressly says the wicket could not be located on the sheet; Quaife places it near the northwestern blockhouse. Existing source gives a bounded adjacency, not historical meters, completion date, precise make or an independent dimension. Keep the measured Whistler site/plan/bearing, existing component ranges and date qualifications.

## Relative model bound and a conservative working trial

Current fixed records, computed with placement rotation as currently used:

- NW blockhouse base south edge: UTM N4637629.08. Its reconstructed upper-storey overhang is0.45m, projecting south to N4637628.63.
- Officers' west range north end: N4637622.80. Thus6.28m between those base rectangles, already present without moving either.
- Outer west row: E448208.64, origin N4637599.88, depth33.92.
- Inner west row: E448211.23, origin N4637602.90, depth27.80.

A finite reconstructed trial is a1.50m cut in each west row, aligned on model N4637627.33. It extends N4637626.58..4637628.08, leaving1.0m south of the NW base and0.55m below its upper overhang in plan, and3.78m north of the range's base. These are model clearances chosen for the source's near-NW relationship, NOT measurements from the historical drawing. Width1.50 is the existing archetype's accepted minimum and existing wicket kit width, not a discovered historical figure. Placement should be described by those existing model neighbors, not presented as a precise historical UTM claim.

Per-side west offsets toward +v: inner +10.53m, outer +10.49m. Formula: desired common model N minus row origin N minus row depth/2. A later native image must confirm the visual relationship and leaf/frame clearance, not merely reuse this arithmetic as proof.

Preserve south verbatim: gate_width_m1.89; inner gate_offset_m-2.62; outer-2.83. They align E448222.265/E448222.270 in the measured south barracks passage. Merely appending `w` to gate_sides would reuse the negative south offset, place the new opening far from the NW blockhouse, and apply the wrong width/type.

## Minimum engine-neutral control contract

Each named side needs independently resolved offset, width and kind with current scalar fields as fallback. A single graded `gate_overrides` form map is sufficient, e.g. `value:{w:{offset_m:10.53,width_m:1.5,kind:"wicket"}}` on inner (outer10.49), confidence reconstructed, while gate_sides becomes[s,w] at its separately supported occurrence grade. An alternative three side-map attributes is equivalent but not necessary; do not duplicate gate membership in two independent places.

- New PalisadeParams field must be keyword-only/default empty. Existing positional constructors must remain compatible. Add to CONSUMED/from_phase. Reject unknown sides/keys, overrides for absent sides, nonfinite numbers, unknown kinds, invalid width or offset on each resolved wall. Reuse current1.5..8m, at-most-half-wall and jamb margin constraints per side.
- Producer `_stockade` cut width, `_gate_shift` sign and `_gate` center/frame/leaf must all consume the same resolved side settings. +u for n/s, +v for e/w; n/w reversed walks keep the sign inversion.
- Preserve unchanged gates' grades. West gate vertices and runtime leaf use worst applicable side/override confidence, reconstructed; do not downgrade the source-supported south gate solely because an unrelated west override exists.
- Runtime stockadePlan must mirror side resolution for BOTH curtain cuts and gate plans. Add w display names to FORT_GATES for BOTH first-fort rows. Without those names it cuts a wall but skips the interactive leaf/span. Existing drawsLeaves drops baked dark leaves only for mapped stockades; a wicket builds posts without a baked leaf, so the current renderer can own its one leaf without duplication.
- Existing kind wicket is a generic physical kit currently documented as a garden paling: two posts in the cut and one pale/rail/braced leaf, full picket height minus0.06, foot0.07, inward100degree swing. Reusing at a3.7m fort curtain is reconstructed make, not proof the historical fort gate was a garden wicket. At cut1.50, actual leaf span is1.18 between post inner faces. State this in liberty notes and review native silhouette. No need for a new historical gate kind unless actual image shows a specific incompatible form.
- Source/map sidecar attrs must derive from records, not renderer-only literals or engine-specific geometry. No new dates, dimensions claimed from Currey or relocation of measured plan elements.

## Current family and exact scope

Current registries contain1044 default assets,1044 web master receipts,6 version assets. Palisade has15 default phase bindings, zero variants. Inventory with input/master/web SHA256 is in `palisade-inventory.json`.

Two intentional geometry changes are first_fort_dearborn_pickets_inner/outer, both first_fort_1803. Thirteen controls: coursoll_field_1812; first_fort_covered_way_bank_lower/middle/upper; first_fort_covered_way_terrace; first_fort_outer_officers_garden; first_fort_outer_sutlers_garden; forks_company_cornfield_1812; fort_dearborn_garrison_garden; fort_dearborn_palisade; kinzie_garden_1812; kinzie_house_1812_green; lees_place_field_fence_1812. Shared palisade.py bytes affect all15 input hashes; cannot honestly request/adopt just2. Any no-op native outputs must be measured; do not hand-stamp registry hashes. Unrelated defaults/versions must retain their actual identity. Parent may have newer source changes; rebind count/identities before request.

Only one current reference composition explicitly contains either picket row: first_fort_dearborn_pickets_outer/currey_1912_birdseye. Camera diagnostic_onlytrue, eye65.92/56.2/49.69, focal1000, principal444.5/294, RMS8.4px/max12.9 from reconstructed picket corners; do not refit it to manufacture agreement. Refresh actual pair/overlay/reports after final native assets.

## Finite checks and completion

1. Pure params + current check gate: fallback/override errors, position-preserving old positional constructor, invalid per-side overrides; existing15 records resolve; no unrelated drift. Do not change geometry assertions to accommodate a failure.
2. Runtime: independent west and south side plans; both west cuts/centers aligned; wicket one leaf; south and second fort still double leaves at existing positions. Add real west route/walk cases: both shut stops outside, outer-only opens between rows, both open reaches fort interior, inner-only still stops at outer. Open leaves, jambs and near-blockhouse/range obstacles remain solid.
3. Existing `tools/test_fort_gates.mjs` assumes exactly2 first-fort gates and loops all gates as if south in two blocks. Update those selectors to explicit south ids while preserving every existing south assertion; add west assertions. Its ride route block also loops all gates expecting the south route visits each, so scope that to the gates actually crossed and assert the separate west route. Avoid falsely claiming old assertions pass unchanged.
4. Native15, actual registry/sidecar/master/web ownership/freshness, evidence pair and full source checks. `tools/measure_fort_gates.py` currently defaults to the second fort and scalar fields; it is not by itself evidence for mixed first-fort wicket controls. Any new mixed-gate readback must inspect actual emitted positions/materials/opening, not merely re-run parameter arithmetic.
5. Published desktop+phone inspection including1812 interaction. The single open Currey item may close only after an actual visible opening beside the NW blockhouse with working leaves/walkway, preserved south entrance and qualified source notes. Keep T3041/T2387 partial if any other current view still has a finite visible difference. Retain outcome honestly if native/source/browser fails.

No new broad research, no new ticket, no camera fit, no blockhouse/range/site changes, no global gate_offset replacement, no main promotion.
