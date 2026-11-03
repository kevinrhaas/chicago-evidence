# Original T-2376: smallest honest next world increment

This is a CLOSED read-only source plan, not implementation, source adoption, new control, bake, render, ticket claim, commit or PR. The current private closed-shoulder comparison is checkpointed at ba86a4b537d47ef4024fe10bace305384b5a960f; original T-2376 remains OPEN/DIFFERS.

## Exactly which yard records conflict

Current public e32 `data/yard/town_trade_goods.json` contains two coupled records at the same reconstructed ENU centre[-34.87,-86.97]:

- `/sheds/0`, id `green_tree_tavern_wagon_shed`: the open roof AND its posts,4.05x3.20m, eaves2.95m/head3.63m. This is one yard record, not a separate hidden model.
- `/wagons/3`, id `green_tree_tavern_shed_wagon`: covered wagon, `under_shed: green_tree_tavern_wagon_shed`, same centre, bearing90degrees.

The two other `green_tree_tavern_yard_wagon_1/2` farm wagons, frontage barrels and front bench are different records. They are not the shoulder conflict and must not be removed as a shortcut. `EXACT-COUPLED-YARD-RECORDS.json` preserves the actual two complete records and positions; no new dimensions are proposed.

Source owner is `tools/generate_yard_goods.py::_green_tree_wagon_shed` (lines1066–1215). It constructs the roof/posts record AND its associated wagon together and returns both. `build_green_tree_yard`/main append both to the town output. The existing native derivative step runs the generator and `--check`; hand-deleting two generated JSON entries alone would not survive its re-derivation. `derived_manifest.json` explicitly runs this producer while leaving `resolves:[]`; that ownership distinction does not make its generated file a valid hand-edit shortcut.

The same wagon id occurs in `data/transport/studies/farm-box-protected.json`, a protected development-study snapshot. It is not a second live yard placement, and this plan does not change that unrelated study. Any later physical/protection check that cites it must be investigated honestly rather than deleting its historical record to make a gate pass.

## Existing versions cannot scope away this yard conflict

`docs/STRUCTURE-VERSIONS.md` says a version swaps one building, never adds one. Current `scene-loader.js:326–334` replaces ONLY the selected structure's sidecar registry row; it expressly leaves the scene's own index canonical. Main passes `VERSION_REQUEST` to `loadScene`, but its `createYardGoods` call at2671passes dataBase/terrain/confidence/problems/hostMissing/lowSpec/replacementIds, not the selected version or a per-version yard record. `yard.js:createYardGoods` has no version/context option and loads the ordinary yard index/records. `hostMissing` only tests whether a host building is missing; a version keeps the same Green Tree id, so that is not a suppression mechanism.

Therefore simply enrolling `andreas-reading` and opening its ordinary in-town version URL retains the canonical open shed/posts/wagon. There is NO existing safe data-only version-specific yard override. Globally deleting the two records for an optional version would damage the unchanged open default. Hiding the whole yard layer is also not a faithful local alternative. Supporting a true in-town alternative with its own yard treatment would require explicit version-aware context semantics; none is implemented or proposed in this bounded packet.

All seven inspected current runtime/producer/data files were fetched through the public e32 API and Git-blob verified. They equal immutable N exactly; PUBLIC-CURRENT-BINDINGS.json records their identities. This is actual code inspection, not a browser claim.

## Concrete smallest source choice

The existing private asset comparison is already valid without changing the world. For an ACTUAL visible world increment using only current geometry controls, the narrow path is a consciously chosen CLOSED canonical working interpretation PLUS its coupled yard relation in the SAME source increment:

1. Retain the prepared one-boolean closed-shoulder geometry. It reuses genuine native MASTER0b53/recipe80d47 under full current-input equality, with all producer/parameter code and every numeric form input unchanged. No new25family native requalification or new model measurement is needed. Derive/register its actual WEB and correct native source-to-master record through the supported native package/adoption path before use; do not relabel the old canonical bytes or a predicted recipe as a bake.
2. Amend current Green Tree research/attribute/Liberty prose to say Andreas's enclosed shoulder is the chosen working reading, while Trowbridge's open bay remains explicit counterevidence/alternative. Do NOT invent a conversion year, assert that either source proves the exact July1835state, or silently change confidence. No full matches verdict follows: the private left-cluster roof silhouette/proportions still differ.
3. Couple `_green_tree_wagon_shed` to the EXISTING canonical `enclosed_left_annex.value.shoulder_enclosed` attribute. For a true value, decline BOTH the open shed/posts AND its under-shed wagon with an explicit source/layout reason; for false/absent, preserve the current function's output exactly. This requires a small yard-derivation relationship change, not a new geometry producer/control or a global suppression switch. The current boolean is already the physical state; do not add an independent flag that can disagree with it. Preserve the other farm wagons/bench/goods unless real native clearance rejects one.
4. Run the ordered current native owners for sidecars, occupied solids, entrances, clearances, yard goods and their downstream layers. Verify the selected closed shoulder takes occupancy, the two competing open-bay entries are absent by their declared relationship, other yard records remain appropriate, and no new collision/access defect appears. Keep current normal phone/desktop app QA, actual WEB/registry checks, all four source-check parts and normal PR/dev integration. The original ticket stays OPEN/DIFFERS while material left-cluster gaps or original picture coverage remain unfinished.

This packet does not choose or apply that canonical interpretation. It identifies the actual finite source choice needed: CLOSED default data plus COUPLED yard derivation, or a future explicit version-aware context path. The supported isolated native comparison alone neither authorizes a blind default flip nor manufactures an in-town version that already handles its context. No new ticket, date, measurement, confidence promotion or user-approval question is introduced.
