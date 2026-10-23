# T-2792 — vehicle evidence and first-master handoff

Research handoff,22 October 2026. This specifies the next modeling work; it does not certify finished geometry, photographic quality, animation, riding or boarding. [carriages.md](carriages.md), [inspected-image-register.json](inspected-image-register.json) and [existing-vehicle-inventory.json](existing-vehicle-inventory.json) bind the evidence and existing asset bytes. T-2793/T-2794 retain their own actual-model acceptance.

## Build choices and chronological limits

|Choice|Construction basis and identity|Eligible use and remaining gaps|
|---|---|---|
|First static compatibility wagon: W01|Existing project-original farm-box reconstruction; GPL geometry, original CC0 procedural material pixels. Existing3.05×1.07×0.55 m body and running gear; no photograph tracing required.|1835 reconstructed type at existing stands. Maker, owner, specimen, exact timber species/finish and1835 presence at any specific stand are unproved. Never rename it Studebaker, Dearborn or Conestoga.|
|First documented passenger-carriage target: Studebaker1893 Brougham|Actual 1893 first-party color lithograph, IA illustratedsouve00stud leaf 0095; public-domain publication. Source record `studebaker_1893_illustrated_souvenir` explicitly permits geometry derivation within its limits.|1904 type reconstruction from a model documented before 1904. No particular local household owner, survival or unchanged1904 production is established. Pair-team/pole arrangement; not the C02 single-shaft chassis. Opposite side/interior/measured dimensions remain reconstruction.|
|First numbered historical wagon target after W01: Studebaker Farm Wagon No4|Same cleared1893 catalog, leaf 0103. Actual green lined box, red running gear/wheels, sprung driver's seat and paired team viewed.|Separate 1904 master, not a1835 replacement. Carry documented model number and visible design; absolute dimensions, hidden construction and placement remain bounded reconstruction. No independent sales/popularity ranking established.|
|Current C01/C02|Original open/enclosed1904 technical studies, unbranded. C02 is an available static generic parked example, with closed-door/shaft-rest presentation.|Reusable rig/export/picking and technical control; neither is an exact Studebaker, Harvey or Pullman specimen. Retain names/provenance. Refining C02 does not turn it into the catalog brougham without a new actual source comparison.|
|Dearborn passenger wagon|Kinzie1856 pp297/302 describe John Harris Kinzie's1831 purchase of Kercheval's light dearborn wagon and pair of travelling horses.|Distinct light-passenger design follow-up; no identified manufacturer or measured pre1835 appearance comparator yet. This is not1812 evidence. The text alone cannot specify its roof, curtains, springs or photographically correct silhouette.|
|1812 baggage wagon|Kinzie1856 retrospective pp210/221 establish baggage-wagon narrative, maker unknown.|An independently bounded utilitarian reconstruction may be proposed; no imported1831 Dearborn or1893 manufacturer badge. The Smithsonian Conestoga is a type comparator with a replica cover, not proof of local1812 use.|

Rights-pending J.P.Smith ICE, Harvey-frontage and Clarke/Chrimes images remain text citations and reference leads only. No tracing, extracted measurements, livery reproduction or sampled textures from those images is an approved asset input. LoC Pullman-location metadata is freshly verified, but higher-resolution pixels remain unavailable; no maker/type/owner is invented to fill that gap.

## Reuse and current numerical ledger

Retain T-0084's narrow tongue, T-0087's bolsters/reach/hounds/kingbolt and T-2121's individual planks and deterministic coat families. Preserve terrain support, stand-refusal rules, stable instance IDs, bearings, tilt/yoke configuration and per-ID variation. Do not regenerate80 identical clones or replace a freight stand with a passenger coach.

The current committed data holds80 trade wagons:25 farm_box,17 covered,38 cart, plus one separate two-wheel hogshead water cart. These are record counts, not camera-visible counts. Seventy-one are categorized at street verges and six in yards; do not force the remaining three into either category. Current parked data replaces three farm-box stands and two covered stands in 1835 and adds one reconstructed1904 carriage. Exact six placements/bearings/coordinates and all 80 legacy IDs are in the inventory. Water-cart `water_cart_randolph` stays separate at ENU[1220,-262.4], bearing90.5°.

|Existing output|GLB bytes|Triangles|glTF primitives*|Estimated RGBA8+mips|
|---|---:|---:|---:|---:|
|W01 portable study|793932|10792|22|0|
|W01 driver-bench study|817220|11032|23|0|
|C01 open study|770892|10416|27|0|
|C02 enclosed study|860956|11512|31|0|
|Parked W01|1926852|12104|23|6291456 B|
|Parked C02|1844804|12228|31|3145728 B|
|C02 shaft rest, separate|6960|60|1|0|
|Covered W01 blue / oak|2970424 /2970420|17292 each|26 each|8388608 B each|

*Primitive counts are source inventory, not measured driver draws. Shadows, confidence passes, instancing/batching and transparency can change actual work. Texture figures are dimension-based estimates, not GPU allocations. Current files do not provide accepted separate near/mid/far LODs. Full/Balanced/Light parked reach100/65/0 m and legacy fallback are distance/tier policy, not proof of a completed LOD set. The 22 October CI source-reproduction failure and repair are tracked separately; these inspected existing bytes do not establish cross-machine regeneration or qualify any later CI run.

All following dimensions are metres. W01 values are reconstructed legacy choices: body3.05×1.07×0.55; bed top0.95; wheelbase2.35; track1.21; front/rear radii0.535/0.685; tongue2.75. Cart body1.98×1.07×0.50, wheel diameter1.42, bed0.86, shafts2.44; hogshead1.22×0.84×0.70. No source measures these particular Chicago vehicles.

C02 reconstructed reference envelope is cabin(width,length,height)[1.32,1.70,1.44], wheelbase1.90, track1.40, radii0.45/0.55, shafts2.20 with0.773 inner tip spacing, supported study steering8°. Its generator validates wheelbase1.6–2.2, track1.25–1.6, front radius0.4–0.55, rear0.5–0.65 and shafts1.8–2.6. These are engineering bounds, not historical confidence intervals.

The saved Studebaker Brougham v10 proposal has reconstructed wheelbase2.30, track1.34, radii0.528/0.650, body half-width0.585, driver bench width/depth1.08/0.39 and pole2.65. They are reproducible proposal inputs, not a catalog's measured metres or accepted geometry. Its roof revision is explicitly UNRENDERED; reuse its source controls and parameter history rather than claiming another completed master. Whole-body dimensional scale remains nonunique from one lithograph. Resolve scale with eligible measurements or retain a stated reconstruction interval before a scene release. Farm No4 may initially reuse the W01 engineering envelope as a declared scale hypothesis; change its source-visible body/seat/gear design and preserve uncertainty rather than infer exact scale from the printed art.

## Components, mechanics and material work order

1. Build separate body/floor/plank or cabin panels, rear axle/bolster, reach, front hounds/kingpin/forecarriage, individual wheels/hubs/felloes/tyres, drawgear and seats. Body must have a physical support path through the gear. Distinct translucent glazing stays separate from opaque painted panels; no double surfaces or fake opaque windows hiding an open cabin.
2. Place each wheel pivot at the axle center, axle localX, roll aboutX with explicitly tested forward sign. Front forecarriage pivots aboutY at its kingpin. Test wheel/body/pole swept clearance to the stated limit; preserve actual C02's8° limit rather than the obsolete generic±25° proposal. Whole-axle steering is not automobile Ackermann steering.
3. W01 uses a team tongue; C02 uses two shafts for one horse. The documented Studebaker Brougham/No4 plates show a pair/pole. Separate configurations, hitch-ready angles and force/clearance envelopes must be represented explicitly. Do not attach a horse to a tongue resting on the ground.
4. W01 original procedural wood/paint/iron can be reused within its license. Species, pigment, wear and gloss are reconstructed. The Brougham plate documents depicted dark green/black panels, thin dark wheel elements, lamps/glazing and brown driver upholstery/lap robe; it does not identify actual pigments or every empty-seat surface hidden by people. No sepia/monochrome local photograph establishes color. Farm No4's illustrated green box/red running gear/lining are a distinct catalog appearance, not a paint instruction for 1835.
5. Door/lamp/spring/joinery details visible in the selected plate get individual source-attribute entries. Hidden mechanical geometry receives bounded reconstruction notes. Occupant-facing seats, footboards, boarding steps and door clearances need a later portable-human fit pass before any capability is advertised.

## Portable frames and coupling handoff

Metres; glTF right-handed,+Yup,+Zforward,+Xtravel/anatomical left; scale[1,1,1]. Root is ground at midpoint between axle stations. Geographic ENU(E,N) maps to world(X,Z)=(E,−N), yaw=π−bearingRadians. Treat every socket as a transform relative to its declared parent, never an unexplained world-space vector. Actor controls root motion; clips do not translate the world root.

Actual existing W01 hierarchy and straight-pose local frames:

```text
vehicle_root
  vehicle_body
    vehicle_seat_driver                [0,1.58,0.65]
    vehicle_driver_foot_left/right      [±0.18,1.12,1.19]
    vehicle_seat_passenger_01           [0,1.15,-0.45]
    vehicle_board_left/right           [±0.85,0,0.50]
    vehicle_camera_ride                 [0,1.80,0.20]
  vehicle_running_gear_rear             [0,0.685,-1.175]
    vehicle_wheel_rear_left/right       [±0.605,0,0]
  vehicle_steer_front                   [0,0.535,1.175]
    vehicle_wheel_front_left/right      [±0.605,0,0]
    vehicle_tongue                     [0,0,0.35]
      vehicle_hitch_team               [0,0,2.75]
    vehicle_hitch_single               [0,0,0.35] RESERVED, unsupported
  vehicle_collision                    metadata only until validated
```

W01 team socket is[0,0.535,4.275] in root space only with straight/unpitched tongue. Parked loader rotationX=+0.18578444683082146 lowers it near the ground; that display pose is not a hitch-ready coupling. W01 passenger/boarding/camera sockets do not prove occupied interfaces have been released.

C02 forecarriage[0,0.45,0.95] contains identity `vehicle_drawgear`; its single hitch local[0,0.30,2.20] is root[0,0.75,3.15] in the straight pose. Driver seat root[0,1.32,0.86], passenger seats[±0.24,1.155,−0.68], boarding[±0.85,0.38,−0.12]. Its closed parked presentation does not enable boarding. Covered W01 descendants retain inherited socket names but explicitly mark hitch/driver/passenger/boarding/camera/collision/driver feet `covered_empty_interface_supported:false`; bench and footboard donor geometry were removed. Never infer capability from those names.

A coupling sidecar must name `vehicle_asset_id`, vehicle/harness revisions and hashes, selected `profile_id`, vehicle socket and parent, horse named root/frame mapping, hitch-ready local pose, team lateral offsets, collar/trace/shaft/pole clearances, `seats` with pelvis/foot/hand/rein frames, collision envelopes and explicit capabilities. Horse rig names remain in its own namespace. T-2799 owns the anatomical fit; no horse/vehicle scaling to conceal mismatch. Team traces/evener/breastcollar/full collar and single-shaft tugs/breeching are distinct profiles; a photograph showing one is not a complete force diagram. Driver/rider reuse attested/inferred/reconstructed people under current depiction rulings; no invented named likenesses.

`vehicle-master-handoff.json` is the concrete engine-neutral input/receipt checklist. Required sidecar fields are asset/revision, source attributes/rights/liberties, scene bounds, units/axes/root datum, wheel centers/radii/roll signs, steer pivot/limits, hitch profiles, material slots, LOD records, collisions, seat/boarding capabilities. `false`/unvalidated capabilities remain unavailable in the visitor UI.

## Executable next-ticket acceptance

Authoring commands run from `chicago/4d`; use a new external output directory and the supported interpreter/dependencies, never overwrite accepted outputs while investigating. Existing interfaces:

```sh
python tools/transport/generate_wagon.py --parameters data/transport/studies/wagon.json --output-dir "$VEHICLE_OUTPUT/wagon"
python tools/transport/generate_carriage_c02.py --parameters data/transport/studies/carriage-c02.json --output-dir "$VEHICLE_OUTPUT/carriage-c02" --door-angle-deg 0
python tools/transport/generate_parked_wagon.py --parameters data/transport/parked/wagon-w01.json --output-dir "$VEHICLE_OUTPUT/parked-wagon"
```

These are documented handoff commands, not runs performed or certified here. The last chain exposed the 22 October machine-dependent source-reproduction failure; use the separately reviewed repair and preserve all original exact-byte guards. Named Studebaker work has its saved external producer/parameters and requires normal reviewed integration before a canonical app command is claimed.

Next two modeling tickets deliver portable source/master and glTF/JSON, original-material license entries, per-attribute source/liberty records and exact input/output SHA receipts. Verify units, dimensions, pivots and sockets within1mm of chosen parameters, unloaded wheel contact within2mm, actual steering swept clearance, solid hubs/joinery/support paths, normals/tangents and no unintended overlaps. Actual later rolling test is ten circumferences/ten turns within0.1%; no animation completion is inferred from empty joints.

For each cleared source view, record full image/plate ID+SHA, visibility/occlusion masks, source camera model, crop/rotation and whether solved or only approximate. Render source-aligned side/quarter view plus unobscured front/rear/overhead controls. Brougham's original is a lithograph with potentially inconsistent perspective: retain residuals and any camera ambiguity rather than distorting the chassis to fit an impossible camera. Record wheel-center/radius ratios, roof/cabin/door lower-U contour, body-to-wheel clearances, lamp/bench/spring positions and every visible discrepancy. Compare actual pixels; no predicted projection or unrendered v10 closes a match. Inspect near~3 m, mid15 m and distant60 m at recorded FOV/distance on1280×800 and390×780. No photographically accepted label before the source-guided and independent material/detail review passes.

Near/mid/far masters keep all sockets and pivots identical. LOD simplification first removes unseen bevels/fasteners and reduces circular tessellation; never collapses open spokes into a solid wheel at a distance where the gaps remain visible, changes roof/door silhouette, or removes boarding/collision contracts. Draft planning targets are mid≤4000 tri/12 primitives and far≤800 tri/4 primitives per vehicle, subject to actual image/aliasing checks. Near quality begins from the measured existing family cost, not an arbitrary new global cap. These are proposed planning envelopes, not measurements or permission to weaken any shipped budget.

The receipt names source/mirror/GLB hashes, viewport/detail/confidence modes, near/mid/far thresholds and simultaneous instance count; GLB and texture bytes/dimensions; index-derived triangles; source primitive count; actual visitor-frame driver draws/triangles including shadows/confidence; GPU texture allocation where available or explicitly labeled estimate; frame median/p95/max and boot/residency peak. Measure single-object deltas and representative street populations. Normal, Tint, active Ghost, Full/Balanced/Light and mobile fallback retain existing policy and picking. No counter substitution, hidden duplicate, permanent observer or ceiling change can stand in for that receipt.

## Outstanding work precisely retained

Research deliverable is ready for review with its cleared initial choices and bounded modeling instructions. It does not assert the broader collection is exhausted. Current 947 Prairie records include83 contact-screened IDs plus one separate Taylor full-size image:84 known unique,863 without recorded visual coverage; historical83/944 left861. Pre-fire24/24 screening found no dependable contemporary vehicle construction photograph; archive-resolution map magnification remains open. LoC catalog access now works but20.9 MB higher-resolution retrieval failed/timed out and166.6 MB master was not fetched. Smith/Harvey/Clarke original-holder rights, dates and additional elevations remain prerequisites for those particular replicas. Dearborn pre1835 appearance,1812 military construction comparator, exact1904 local owner/specimen and independent maker popularity data remain open. These gaps constrain follow-up models; they are not silently converted into facts or a claim of completed deep research.

## Root validation update — 2026-10-22

The retained V10 Brougham is no longer unrendered: the corrected isolated fixture produced 12 normal desktop/mobile V9/V10 quarter/front/profile captures with identical paired cameras/lights and zero errors. Actual cleanup identifies and releases the owned Three DFG lookup texture; every arm returns to zero geometry/textures. Root inspected the paired desktop quarters: V10 reduces the excessive front roof curl, while fine materials, exact reference-camera match, photographic and main-world acceptance remain open. The generic parked C02 is unchanged and remains unbranded. Actual image/proof capsule SHA25669e78de54548ac296038b7a16ac57b3ade9b7bc191488d20e6633521ce208671.
