# Next visible carriage parcel: clear cabin glazing

Read-only review of actual V17 desktop/mobile detail and full-quarter images. This is a proposed follow-up after PR1213 lands unchanged. No candidate, producer run, browser, app edit or acceptance claim is included.

## Why this parcel

The existing front and door panes read as broad pale-grey panels, especially in the desktop near detail. The 1893 Studebaker catalogue plate0095 depicts the door as glazed, with people/background visible through it. Improving that large visible surface should contribute more than another small hardware detail.

Primary reference: `data/sources/studebaker_1893_illustrated_souvenir.json`, Studebaker Brothers, Illustrated Souvenir (1893), Library of Congress copy, https://archive.org/details/illustratedsouve00stud . Plate identity/hash is pinned in `tools/transport/brougham/parameters.json`: scan0095, SHA256 b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe. This is a period lithograph, not a calibrated photograph or an optical-material measurement.

Reviewed evidence: `/workspace/shared/brougham-v15-v17-rear-quarter-native-source8-HELD-20261022/actual/{desktop,mobile}-v17-source-{detail,fullquarter}-near100.png`. The unaltered full plate is `/workspace/shared/brougham-v11-v12-largeforms-preview8-HELD-20261022/fixture/transport/v12/plate0095.jpg`.

## Exact bounded ownership

Producer root: `/tmp/chicago-covered-sag/chicago/4d`.

* `tools/transport/brougham/generate.py`: two `side_door_glass` instances (around line182), one `front_glass` (around line255), current material5 (around line413), and document `extensionsUsed` declaration.
* Existing material5 is blue-grey `[.38,.49,.50,.25]`, roughness .10, alpha BLEND. It is shared with `lamp_glass`; do not silently change the lamps.
* Preserve all part POSITION/NORMAL streams and shapes, including the current9mm pane solids, window profiles/divisions, body affine, roof, door and interior. Preserve transforms, sockets, silhouette, wheel/step/pole contacts and all placement data.
* Preserve `rear-quarter.json`, `quarter_surface.py` and opaque quarter material6 exactly. The plate does not adjudicate that quarter as glass, curtain or lining.

## One predeclared physical-glass candidate

Add a separate recipe block in `tools/transport/brougham/parameters.json` for the three cabin panes only, and consume it in `generate.py`; clone a distinct material rather than editing shared lamp material5. Proposed optical reconstruction, not historical measurements:

* Name `reconstructed_cabin_clear_glass`; white baseColor `[1,1,1,1]`; metallic0; roughness .04.
* `KHR_materials_transmission.transmissionFactor: 1`; `KHR_materials_ior.ior: 1.52`; alpha OPAQUE, rather than pigment-like alpha BLEND. Register both used extensions.
* No tint, absorption, dirt, invented waviness, image decal or added volume thickness. The current geometric pane thickness remains an explicitly unmeasured reconstruction. Do not claim restoration of attested1893 optical properties.

Physical transmission preserves Fresnel surface reflection while allowing the empty cabin/background to read through the windows. These values are one bounded starting proposal, not a tuning loop or accepted result. Lamps retain material5; quarter remains material6. A new cabin material creates one additional body material batch; account for its actual mesh/node/draw and transmission-resource cost rather than pretending counts are unchanged.

## Shadow behavior that belongs to the same parcel

`renderers/web/js/parked-transport.js:55` currently makes every static material batch cast and receive shadows. The isolated source fixture's `demo.js` likewise sets every mesh to castShadow=true. Untextured alpha glass therefore participates as an opaque shadow caster with the default depth material; current source code supplies no glass-specific transmission shadow solution.

For this pane-only material, disable opaque shadow casting in both the source comparison and eventual app integration. Do not disable shadows on the cabin frame/body or lamp material. This is an explicit approximation to light through clear glass, not simulated refracted caustics. Keep receiving behavior initially unchanged. No lighting, exposure, background or camera change belongs to this parcel.

## Acceptance after PR1213, not a condition of that PR

1. Produce one fresh source-only candidate outside the app, preserving V17 baseline and all original evidence. Confirm exact per-part POSITION/NORMAL and transform equality, unchanged contacts, lamp material and opaque quarter; only the three pane material assignments and their optical recipe may differ.
2. Compare the same desktop/mobile source-detail and full-quarter near100 views at the existing native indexed-near stream, fixed camera hypothesis, original floor/lights/exposure and source crop. The panes should read clear with retained frames and subtle surface reflection; no pale diffuse slab, missing cabin wall, lost window or false see-through quarter. Do not add the catalogue occupants to make the comparison resemble the plate.
3. Inspect a front-oblique and side view of the empty cabin to catch transmission ordering, duplicate faces and inside-view failures. In the eventual1904 parked app view, check windows against actual street/background geometry and preserve the parking contacts. Fixed-source fixtures alone cannot establish app appearance.
4. Record actual before/after images and material/resource costs. Run the normal relevant checks only when integration is authorized; transmission's extra render target/pass must fit the real budget. Reject or hold the candidate if it does not visibly improve the carriage. No photographic-completion claim before actual reviewed images.

No geometry, source, application, workflow or ticket files were changed during this review.
