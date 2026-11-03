# T-2374 bounded opening-count check — no data-only patch

This is preparation only for the original open T-2374. No source checkout, ticket, camera, model, grade or match verdict was changed. PR1665's credited source link is already merged; its old fallback source edits must not be replayed.

The authenticated earlier private comparison is [864bffef](https://github.com/kevinrhaas/chicago-evidence/blob/864bffef74a9346873fa9285cd3d16164c0e61ae/evidence/cobweb-2026-11-03/private-camera-actual-unsolved-520/RECOVERY.md). It remains UNSOLVED/unreviewed: its central-gable numeric fit is not full-compound acceptance, and the held-out rear ridge differs about20.75px. The root's corrected interpretation is retained: the central gable **faces the camera**. Neither width, metric opening dimensions nor world placement can be recovered reliably from that fit.

## Concrete observed gap

Directly re-read the full unmodified1920×1042 keyed panorama, original source/native equal-pixel8× analysis crop and actual projected-landmark overlay. The Agency-House keyed central white gable visibly contains **two lower dark vertical rectangles and one small dark gable mark**. This establishes a candidate count/appearance difference, not whether both lower marks are doorways, whether the upper mark was glazed, their metric dimensions or July1835 survival. The current public MASTER is byte-identical to the earlier actually rendered MASTER `af1f33c0f5d75fc8c40e6cbb589adfd7d29d551572c2775e236bb260f6ee561f`. Its central face has one centred door and no upper opening; archived native mesh-visibility checks establish that face is visible in the diagnostic.

The source is the existing public-domain keyed Wentworth1881 reproduction credited to Kinzie's Wau-Bun1857 and depicting1831. It remains retrospective tier-5 cross-check material, with same-witness and Hubbard criticism retained. The already existing SourceRecord and current link do not become a measured plan or license to trace dimensions. No source, confidence or grade upgrade follows.

## Actual native control result

Imported only the exact publicly authenticated pure-Python `log_dwelling_params.py`. Existing record resolves successfully. `compound_front_rects` emits one central door at front plane9, plus one window on each recessed wing at plane8; `core_front_rects` confirms **one** central opening.

This five-room path supports one singular `front_opening` value per room (`null`, `door` or `window`). Its existing facade/loft/end-opening controls are expressly forbidden by `_validate_compound`. Actual tiny native probes rejected `front_windows_per_side=2`, an attic `end_openings` light and a list of two central openings. `OPENING-CONTROL-PROOF.json` contains exact errors. The generator's `_compound` uses only those returned front rectangles; it has no gable-light call. The richer elbow opening-list path is restricted to exactly two equal-span L rooms plus a frame addition and cannot substitute for this five-room Agency House.

**No safe existing-control data-only patch is prepared.** Splitting the central room merely to obtain two openings would alter roof/wall topology or duplicate coplanar roofs; switching to the Wolf elbow would replace the five-room composition. Neither is an acceptable count-only change.

## Next bounded implementation, if resumed

Add one opt-in explicit aperture control to the ordinary five-room compound path, retaining current defaults and all existing room/roof/footprint/world coordinates. That control must place neutral exterior dark marks on the central +Y wall/gable without claiming door function, glazing, interiors or a historical metric fit. Keep dimensions/positions reconstructed and the drawing a cross-check; do not derive them from the unresolved camera. First decide whether to implement both lower-count and attic-mark gaps in the same bounded control. This is a producer-plus-data change, not the requested existing-control data-only parcel. No implementation was made in this preparation.

When an authored branch implements that actual control, use the existing pinned bake workflow rather than installing Blender locally:

```sh
gh workflow run chicago-4d-bake.yml --repo kevinrhaas/chicago --ref OWN_SOURCE_BRANCH -f only=cobweb_castle
```

Target only Cobweb's MASTER and WEB; authenticate all untouched assets/records and exact native mesh input changes. Re-render the existing private diagnostic against the genuine baked asset to review the count change without declaring its compound camera solved. Preserve the original open image gate, then run all four native source parts and exact-head desktop/390×780 published app acceptance for any code PR. No new photo follow-up, canonical camera, geometry claim, match verdict or grade promotion is supplied by this packet.
