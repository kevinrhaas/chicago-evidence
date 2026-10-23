# Finite dependency review — prefer stable arithmetic, retain strict raw guards

Read-only review only: no application, index, Git, mirror, browser, CI or generator actions. Existing reviewed ownership capture is SHA256 2fb3709d233e896280c50342618c28f9e340029e52c67b328100e05a125e2c27, with 158 ordered records / 36,312 vertices. The actual CI JSON hash remains unknown from this review. The arithmetic agent reports native3.12 / emulated3.11 proof that replacing floating sum with explicit math.fsum in generate_wagon_hardware.py + hardware_shapes.py preserves the reviewed raw capture and hardware GLB. Native3.11 and complete-chain verification remain that agent/root's responsibility; no new regeneration was duplicated here.

The preferred minimal correction is these arithmetic-source changes, with every existing strict raw-parts and final-GLB assertion retained. It avoids a weaker semantic acceptance rule and avoids a recipe/GLB hash cascade.

## Complete active raw-parts pin and metadata map

| Location within chicago/4d | Field / role |
| --- | --- |
| tools/transport/wagon_parked/apply_materials.py:10 | First strict raw JSON SHA gate, after exact04820fc1 hardware GLB assertion |
| data/transport/parked/wagon-w01.json | base_study.materials.authored_parts_sha256 — consumed by first gate |
| data/transport/parked/wagon-w01.json | finish.tiles.authored_parts_sha256 — duplicate reference passed into finish config; not itself an active raw-parts gate |
| tools/transport/wagon_covered/build.py:174 | Second strict raw JSON SHA gate, after exact274e737b finished-parent assertion |
| data/transport/parked/covered-w01.json | authoredPartsSha256 — consumed by second gate and copied into covered receipts |
| renderers/web/transport/covered-wagon/covered_w01_western_blue/covered-w01.json | authored_parts_sha256 — output provenance copied from covered recipe |
| renderers/web/transport/covered-wagon/covered_w01_wolfpoint_oak/covered-w01.json | authored_parts_sha256 — output provenance copied from covered recipe |

The two recipes and both covered sidecars also have published counterparts under site/4d/data/transport/parked and site/4d/walk/transport/covered-wagon. An exact literal search across the app's transport tools/data/assets/renderers and published counterparts found no other active raw capture pins. Historical shared receipts/capsules are not current producer inputs and must remain immutable lineage.

The covered wrapper rebuilds its parked parent, then separately recaptures hardware and its ownership JSON for covered build. Patching only apply_materials would still leave the second core gate red. The hardware/source sum fix makes both independently recaptured raw files satisfy the original same pin.

## Metadata propagation for the arithmetic-only fix

1. generate_parked_wagon.py:39 hashes every .py/.json file directly in tools/transport/wagon_parked plus its wrapper into the parked sidecar source_sha256 map. Update/regenerate renderers/web/transport/parked-wagon/wagon-w01.json.source_sha256['generate_wagon_hardware.py'] and ['hardware_shapes.py']. This is generated sidecar metadata, outside the GLB.
2. assets/authored/transport/wagon_parked/SOURCE.json.generated_files_sha256['renderers/web/transport/parked-wagon/wagon-w01.json'] must then match the newly generated sidecar. The final parked GLB/texture hashes stay unchanged.
3. Supported publishing mirrors the changed parked sidecar to site/4d/walk/transport/parked-wagon/wagon-w01.json. The SOURCE manifest itself is source provenance, not an additional published runtime product here.
4. With covered core + covered recipe untouched and parent/model bytes exact, BOTH covered sidecars and wagon_covered/SOURCE.json core_source_sha256/sidecar_sha256 pins remain exact. No covered sidecar/source provenance should be rewritten merely because an ancestor source script changed: their receipt hashes identify the actual covered core, its parameters and pinned parent GLB, all unchanged.
5. A new helper/test .py or fixture .json inside wagon_parked is automatically added to the parked sidecar source_sha256 set; placing an independent test outside that directory avoids accidentally broadening its producer provenance list. Any deliberate addition there must be represented in regenerated sidecar + SOURCE manifest.

Minimal dependent tracked products for the two-script arithmetic change are the parked source sidecar + parked SOURCE manifest + published parked sidecar; application and model GLB bytes need no change. Added tests/check registration/changelog are root-owned and outside this dependency minimum.

## Why metadata-only recipe changes are not necessarily GLB-neutral

refine_materials.py:45 embeds sha256(exact finish config bytes) in the final parked GLB at extras.finish_variant.recipe_sha256. Changing even the otherwise-unused finish.tiles.authored_parts_sha256 changes that embedded digest and hence the final274e737b GLB. The covered core refuses that parent hash. Preserve the finish subrecipe and its emitted formatting exactly for a source-only fix.

Changing the overall parked recipe outside finish changes only the parked sidecar top-level recipe_sha256, but changing finish changes both that sidecar's embedded finish recipe field and the GLB. Changing covered parameters changes both covered sidecars' parameters_sha256. Changing covered core changes SOURCE.core_source_sha256 and both covered sidecars.source_sha256. Any such covered-sidecar change requires both SOURCE.variants[].sidecar_sha256 pins and both published covered sidecars. These cascades are unnecessary for the stable-arithmetic approach.

## Semantic-guard risks if that approach is reconsidered

A float32 fingerprint must bind ordered part records, complete exact field/schema set, name, frame, integer material, vector counts/shapes, and all FOUR arrays: local_positions/local_normals/positions/normals. Names are not unique: this actual capture has multiple parts named band, so reducing records to a name-keyed dictionary loses ownership information. Order/duplicate names must remain preserved.

Float32 equality does not imply equal producer inputs: apply_materials consumes the raw JSON values as NumPy float64 in PCA, normal classification, UV/tangent construction and linear solves. Two Float64 inputs with identical Float32 projection can still change final UVs/tangents. The existing mapping check only compares merged Float32 positions, not names, local coordinates or normal ownership. A fingerprint of positions alone would miss those changes. Keep exact downstream GLB hash checks even if introducing a semantic source guard; do not quantize the consumed arrays just to make the fingerprint agree. Reject malformed/nonfinite arrays and avoid JSON duplicate-key/NaN acceptance, ambiguous framing, host-endian packing, or tolerance-based equality. Explicit domain version + field tags + length framing + little-endian Float32 bytes would be necessary. Signed zero needs an explicit policy; raw guards already distinguish it.

Because arithmetic stability restores the reviewed raw capture, no semantic relaxation is necessary. It retains stronger ownership/provenance identity without imposing new canonicalization conventions.

## Bounded negative-control evidence and preserved output pins

NEGATIVE-CONTROLS.json evaluates the actual extracted pre-generation raw-hash predicates from both checked-in consumers. The reviewed baseline passes both; eight independent in-memory alterations (name, frame, material, positions, normals, local_positions, local_normals, record order) are refused by BOTH predicates. No generator, texture producer, application state or filesystem fixture was mutated. This is guard-level evidence only, not a full actual-CLI or cross-version generation proof.

Expected final bytes remain hardware04820fc15b16c6f1b9b12487c2d6ceb3500d03c94094d84c73554f2b2d1f5709; material0138ad2565f3e8b08029ef788c5196c65c80c79643313e944c726b993ff31ee4; parked274e737b51872983df792d0b24de8e75de8631890a8d586a32d9c6f0066484fb; Western9b6575d1702ca288b5a66487ef089cc51dd0b86d14a47574f94b6fe6eaf23d23; WolfPointc6f69830d4ad690125ed703353d429bb8f68d67d29d6f6161b383b8b2d78f191. Read-pins snapshot preserves current source/product identities; fullchain actual generation is intentionally not repeated in this review.

GPL-3.0-or-later geometry/source and CC0-1.0 original procedural-pixel/descriptive-data licensing remain unchanged. Existing assets/LICENSES.md and renderer transport LICENSES.md describe the same original generated chain and contain no per-script hash that requires editing. No new imported geometry/pixels or provenance claim is introduced.
