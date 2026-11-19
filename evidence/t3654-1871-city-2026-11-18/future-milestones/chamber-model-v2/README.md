# Original 1865 Chamber of Commerce — exterior candidate v2

This isolated second version develops the source-visible exterior from the preserved
v1 checkpoint. It is not installed in the city and does not claim a photographic match.
The two drawn references retain their original camera parameters so geometry changes
can be assessed directly. A newly acquired Carbutt stereograph supplies a third view;
its original-building phase is visually identified, while its exact date is unresolved.

The first v2 pass built the broad central mansard apron, curved shoulders, urns,
molded arch crowns, larger fanlights, round portal columns and capitals, recessed
entrance, spandrel relief and projecting central balustrade. Actual comparison exposed
incorrectly facing entrance reveals and an overly plain stone surface. The next pass
corrects aperture-facing normals, bounds a dark exterior passage proxy, cuts horizontal
beveled stone courses around actual openings, strengthens roof dormer casings and
layers the apron moldings. Rectangular basement apertures replace unsupported arches;
lower office openings rise 0.7m while portal height and grade remain unchanged because
the drawings disagree. Direct inspection of both Carbutt stereo halves replaces the
central roof circle’s unsupported black glazing with a pale face; exact dial markings
and time are unresolved. Upper fanlight glazing is retained. Exact carving, color and
dimensions remain reconstructions.

## Regeneration

Requirements: Python3 with Pillow. The generator reads only this package; it does not
read the app, run Blender or download external assets. The ornament helper contains
original parametric geometry. Both generator source hashes are in the build sidecar.

```sh
cd /tmp/t3654-chamber-model-v2-candidate
python3 generators/chamber_emit.py
python3 generators/chamber_emit.py --check
python3 tools/validate_candidate.py
```

The engine-neutral recipe is `data/chamber_of_commerce_1865.recipe.json`. The output is
`assets/chamber_of_commerce_1865__original_1865.glb` plus its JSON build record. Three
original procedural PNG textures are embedded. Geometry uses metres, x east, y up and
z south; origin is the north facade midpoint at reconstructed street grade. No city
position is assigned. Duplicate vertices are shared only where every final float32
attribute is identical; source silhouette and material boundaries are preserved.

This is a detailed master candidate. Scene/web registration and a suitable derivative
belong to the later integration milestone, alongside actual terrain contact and named
footprint replacement of the generic context city.

## References and review

The full public-domain source pages and their rights/provenance records are in
`references/` and `data/sources/`. The two drawn-view camera JSONs in `camera/` are unchanged
from v1. Their coarse box-fit residuals remain21.40px RMS for Andreas and15.09px for
Chicago Illustrated; neither is an accepted camera solve. `camera/v2/FORM-AUDIT.md`
and its coordinate plot document the source-visible forms used for this revision.
No source-image pixels are used as model textures, and no restricted CHM bytes occur.

Current v2 comparisons belong under `review/v2/andreas/` and `review/v2/illustrated/`.
The third photographic comparison belongs under `review/v2/carbutt/`. Native match
records hash the actual model, camera and image bytes. Earlier v2 comparisons and
recipe snapshots are preserved under `review/v2/iteration1/` and `iteration2/`; these
images are historical evidence, not independently replayable old generator snapshots. Historical v1 analysis in
this working directory is clearly labelled and is not evidence for changed geometry.
The compact v2 archive deliberately leaves bulky superseded v1 plots in the separately
preserved v1 archive, while retaining current sources, cameras, exact fit reports,
source-form audit and actual v2 comparisons.

The native tool runs read-only from the repository, with explicit candidate paths:

```sh
TMPDIR="$PWD/review/tmp" node /workspace/chicago/chicago/4d/tools/photo_match.mjs \
  camera/andreas-original-candidate.json \
  --glb assets/chamber_of_commerce_1865__original_1865.glb --out review/v2/andreas
TMPDIR="$PWD/review/tmp" node /workspace/chicago/chicago/4d/tools/photo_match.mjs \
  camera/illustrated-original-candidate.json \
  --glb assets/chamber_of_commerce_1865__original_1865.glb --out review/v2/illustrated
TMPDIR="$PWD/review/tmp" node /workspace/chicago/chicago/4d/tools/photo_match.mjs \
  camera/carbutt-original-candidate.json \
  --glb assets/chamber_of_commerce_1865__original_1865.glb --out review/v2/carbutt
```

Playwright, Chromium and the project's Three vendor files must be available. This
session uses read-only dependency symlinks; the archive excludes those dependencies.
`PW_EXECUTABLE` selects Chromium. All temporary browser files stay in `review/tmp`.
The photo tool renders a neutral flat-grade review, without city terrain or neighbors;
its light does not reconstruct October1871weather.

## Historical limits retained

Both sources report93ft frontage. Working depth follows the contemporary181ft report;
Andreas's180ft alternative remains explicit. The roof remains a reconstructed24m
cornice plus the reported23ft mansard rise. Andreas's contradictory99ft statements and
the contemporary undatumed100ft report are not resolved. The central window retains
the reported30ft by12ft opening, with a reconstructed11m sill. Ornament, staff, railings,
colors, east and south faces are reconstructed. No image alone proves1871tenancy,
flags, signage or an individual's October8presence. No interior or ancillary annex is
modeled; a dark closed backing limits the entrance to an exterior view.

The frozen v1 package remains at `/tmp/t3654-chamber-model-candidate`, unchanged.
Its archive SHA256 is `d6f4c2d23b27292410dc6792e96d93e97ac823dff1d2151da7f597ffb8a49f51`.

## Frozen v2 checkpoint

All three current native comparisons were directly inspected and remain **differs**.
Byte-for-byte reproduction and independent geometry validation pass. The Carbutt fit
has 14.38px RMS and 26.39px maximum residual over 13 fitted points, plus five held-out
sills; it reaches a 5-degree roll bound and places its principal point outside the left
exposure. It is a diagnostic camera, not accepted optical calibration. Actual photo
comparison exposes lower-facade/grade, roof/cornice, apron, sash and material gaps.
See `HANDOFF.txt` and the current match records for precise limits.

Generate the raw public file/hash whitelist with
`python3 tools/archive_candidate.py --manifest-only`; copy only listed regular files
and the manifest/checkpoint record. No duplicate tar is needed. The reference card,
printed attribution, source metadata and broad catalog date are preserved intact.
