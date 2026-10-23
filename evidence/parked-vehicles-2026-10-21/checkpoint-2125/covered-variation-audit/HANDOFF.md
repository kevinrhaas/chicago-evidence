# Covered-wagon variation audit — preparation for T-2980

Read-only source review at app `2aebef95f6a5b6fa1bd8353db936c7674a73c32f`. T-2792, T-2793, T-2979, the newly filed T-2980, QUEUE and current HANDOVER were read. No ticket was claimed or changed. No app/Git writes, browser, network, tests, geometry generation or model acceptance occurred. `inventory.json` contains all 18 covered IDs, exact coordinates/bearings, seed inputs/draws, palette/aging, board/stake factors, geometry and source/ticket SHA256s. `audit.mjs` only reads source/data and evaluates the exact extracted pure hash/PRNG functions.

## Counts and the earlier “80”

The 1835 yard index contains **86 declared vehicle rows**, not a measured runtime population: `town_trade_goods.json` has 80 (25 farm-box, 17 covered, 38 carts), `town_water_cart.json` adds one cart, and `town_trade_yards.json` adds five (four farm-box, one covered). Thus there are **18 declared covered wagons**, 29 farm-box wagons and 39 carts in the index. The older ticket/PR reference to 80 describes the main town_trade_goods group; it must not be silently presented as the complete indexed count.

Actual emitted counts can be lower: createYardGoods skips hostMissing, invalid positions and missing terrain, and increments its census only after the builder succeeds. Its built record/census count is also different from visible on-screen objects: ordinary culling and refined replacement fallback visibility may hide already-built meshes. This audit measured no runtime count. T-2979 reuses three farm-box IDs; it does not add three new rows to these source lists.

## What is already different

All 18 covered wagons currently share a 3.05 × 1.07 × 0.55 m body, 0.95 m bed, 1.37/1.07 m rear/front wheel diameters, 2.35 m wheelbase, 1.21 m wheel-centre track, and 2.75 m tongue. Their canvas uses the same 1.10 m elliptical rise, 0.12 m overhang at each end, 3.29 m total length, 1.07 m width and 2.60 m crown above the builder base. It has eight arch segments, two-sided faces, open ends and no separately drawn bows. There is **no existing randomly varied cover profile, body scale, wheel size or load shape** among these covered rows.

The visible differences come from stable material/color aging and per-board shading/grain; exact locations, bearings and recorded slew; host/shed context; and laid-by gear. Seventeen rows carry an ox-yoke. Only `green_tree_tavern_shed_wagon` has no yoke; it is under the existing Green Tree wagon shed. Yokes use a 1.42 m beam, 0.12 m section, 0.34 m bows and 0.05 m bow section, placed at bodyL/2 + 0.55 m along and 1.35 m across the wagon. No covered row supplies load, cargo, contents, items or identifying marks. These are reconstructions, not attested manufacturers, colors, personal ownership or a named historic load.

`wagonCoat` seeds FNV-1a32 from **`["wagon", originalId, exactE, exactN].join("|")`**. It uses the exact numeric coordinate strings, without centimetre rounding. Bearing, scene, row order and kind are absent from this seed. The extracted source stream adds 0x6d2b79f5 and uses its existing Math.imul/unsigned-shift arithmetic. First draw chooses a weighted scheme; second gives age `0.88 + r*0.18`; third gives gear multiplier `0.92 + r*0.10`, multiplied by age; fourth gives canvas scalar `0.84 + r*0.18`. Next draws shade the floor, eight side/end boards and six stakes. Keep the old ID/seed when assigning a new parked row ID.

Schemes have total weight 13: blue/oxide 3, red/oxide 2, green/oxide 1, blue/greybrown 1, greybrown/greybrown 2, silver/silver 2, oak/darkoak 1, pine/oxide 1. Actual covered allocation is blue/oxide 7, red/oxide 3, pine/oxide 4, greybrown/greybrown 1, oak/darkoak 2 and blue/greybrown 1. Green and silver are possible schemes but are not assigned to any of these 18 covered IDs. Canvas starts at sRGB #bfb49b; material palette hexes are in JSON. A random fresh palette assignment would change the existing deliberate differences.

Wood grain has a separate seed from each primitive centre rounded to centimetres, including terrain-dependent Y, over the existing 4.48 m grain tile; the canvas explicitly disables grain. Per-face endgrain and contact darkening are additional renderer shading. JSON linear colors are nominal uncached sRGB conversions: actual toneOf reuses a cache keyed by hex and scalar rounded to three decimals. This is not a full vertex-color replay or measured framebuffer color.

## Bounded candidates, not a placement selection

These retain different contexts/coats for a later old/new comparison. No actual four-wheel terrain qualification or shed-clearance check was performed, so none is approved for replacement yet.

| Existing ID | EN metres | Bearing | Body / gear | Age scalar | Canvas scalar | Yoke |
|---|---|---:|---|---:|---:|---|
| `green_tree_tavern_shed_wagon` | [-20.93, -86.97] | 90° | blue / oxide | 0.998023416 | 0.995454507 | no |
| `town_wagon_western_hotel_wagon_yard_1` | [-136.05, -291] | 356.2° | blue / oxide | 1.022647512 | 0.867634306 | yes |
| `town_wagon_wolf_point_tavern_yard_1` | [-90.5, -39.5] | 356.2° | oak / darkoak | 0.914639327 | 0.933498787 | yes |
| `town_wagon_wolf_point_tavern_yard_3` | [-92.5, -48.5] | 7.5° | blue / oxide | 0.956152499 | 0.910305285 | yes |
| `inf_teamster_stable_west_yard_wagon_2` | [-170, -228.63] | 180° | blue / oxide | 0.905552439 | 0.969938516 | yes |

## Safe integration boundary

Use an explicit small subset in `placements.json`: a new row points `replaces` to the exact old covered ID and retains original coordinates, bearing, host/context, reconstruction grade and seed lineage. Give it a true covered model/type rather than relabeling the current open W01. Existing source records remain the authority and fallback. Do not alter all 80/86 vehicle rows, regenerate the town, add arbitrary loads/brands or change the current farm-box placements for this follow-up.

Current main creates parkedTransport first, passes its replacementIds to createYardGoods, then connects setFallback to yard.setReplacementVisible. Selected old vehicles get isolated fallback chunks; near refined visibility suppresses that whole chunk and Light/far/failed-load paths retain or restore the old object. **That chunk contains the old covered body, canvas, tongue AND yoke.** A new asset lacking the flagged laid-by yoke silently deletes gear near the replacement; retain equivalent gear in the new covered asset/support, or deliberately isolate/preserve the old accessory with a separately reviewed change. Keep the Green Tree shed independent and avoid duplicating a yoke when fallback returns.

The current parked loader supports row.model → models[key].file and optional support_file; it does not implement a coat/variant field. asset.scene.clone(true) still shares material references. A follow-up must explicitly carry the original per-ID coat/aging/board seed into reproducible material variants (or a narrowly reviewed per-instance material path); retinting one shared material would recolor other instances. Distinct named model variants can use the existing manifest interface, but resource sharing, texture cost and actual visible differences still need measurement. Do not assume one new GLB with one uniform finish preserves the old variety.

Keep unchanged confidence/picking/card ownership limits, disposal, original GLB authority and static batching behavior. Keep the existing four-contact finite/30 mm ground guard and actual tongue-contact solver: the legacy yard builder samples only centre terrain, so an old coordinate is not proof that a new four-wheel placement passes. Qualify a small subset on actual terrain before integration; do not raise the guard to rescue a stand. Existing Full 100 m, Balanced 65 m and Light fallback behavior remain. Static material batches are not an animation/boarding implementation.

Any new canvas/bow/fold geometry, seam construction, wear and shape variation must remain explicitly reconstructed and use cleared/original inputs. Preserve open ends and existing proportions unless the new evidence and liberty record justify a change. Future acceptance requires actual old/new matched views, multiple variants together, source/published desktop/mobile inspection and current canonical api.stats driver/triangle/texture/memory budgets, followed by required project gates. None of those future model/render checks was executed in this audit.

Source anchors: yard.js hashOf/streamOf near635; wagonCoat1433; pushWagonBox1453; buildWagon1486; covered tilt1626; pushYoke1733; readForm2894; replacement selection3343; fallback visibility3473. main.js integration2399. parked-transport.js manifest/load/four-wheel checks143–205. Exact hashes, not these human line hints, bind the inspected bytes.
