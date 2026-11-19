# Original 1865 Chamber of Commerce — isolated exterior candidate

This package contains actual geometry, parameters, independently acquired reference
pages and two comparisons rendered with the project's existing photo tool. It is a
first implementation candidate, not a passed image gate or a cinematic completion.
It has not been installed in the city or registered in the application's manifests.

The exterior includes five tall north archheads, the wider tripartite central window,
three front portals, ten west upper bays, a high basement, masonry bands and quoins,
cornice, mansard, circular roof openings, bare staff, chimneys and bounded railings.
The east elevation repeats the west rhythm as a reconstruction; the brick rear and
its openings are reconstructed. There are no interiors, crowds or ancillary annex.

## Build and verify

Requirements: Python 3 with Pillow. NumPy/SciPy are needed only to repeat the optional
camera experiments. The mesh generator has no dependency on the repository, Blender,
Shapely, downloaded materials or a running service.

```sh
cd /tmp/t3654-chamber-model-candidate
python3 generators/chamber_emit.py
python3 generators/chamber_emit.py --check
python3 tools/validate_candidate.py
```

The output is `assets/chamber_of_commerce_1865__original_1865.glb` plus its JSON build
record. Embedded textures are three original procedural 512px PNGs. glTF coordinates
are x east, y up and z south, in metres. The north facade midpoint at candidate street
grade is the origin. No georeferenced world position is claimed.

## Actual comparisons

- `review/andreas/andreas-original-candidate-side-by-side.jpg`
- `review/illustrated/illustrated-original-candidate-side-by-side.jpg`

Each compares the complete cleared source page to this actual GLB with a fitted
pinhole camera. Both `camera/*.match.json` verdicts are `differs`. Their hashes tie the
camera, model and source bytes to the images. The initial Andreas comparison is retained
as `review/andreas/iteration1-side-by-side.jpg` to show the roof-occlusion defect that
was found and repaired. Stable bare renders are beside each current comparison.

The existing tool is invoked from this package's directory with explicit GLB paths:

```sh
TMPDIR="$PWD/review/tmp" node /workspace/chicago/chicago/4d/tools/photo_match.mjs \
  camera/andreas-original-candidate.json \
  --glb assets/chamber_of_commerce_1865__original_1865.glb --out review/andreas
TMPDIR="$PWD/review/tmp" node /workspace/chicago/chicago/4d/tools/photo_match.mjs \
  camera/illustrated-original-candidate.json \
  --glb assets/chamber_of_commerce_1865__original_1865.glb --out review/illustrated
```

These commands require the project's Three vendor directory and `keith-stone.js`
reachable at the same relative web paths, plus Playwright and Chromium. This session
used read-only symlinks in this candidate to those installed dependencies; they are
not archived. `review/native-tool-provenance.json` records exact hashes and runtime
paths. Recreate equivalent dependency links when restoring elsewhere. Set
`PW_EXECUTABLE` to the installed Chromium path. `review/tmp` keeps browser temporary
writes inside the candidate. The neutral photo tool does not render actual terrain,
neighbors or street life, and its light is not an October weather reconstruction.

## Bounded dimensions

The width is the reported 93ft (28.3464m). Working depth is the contemporary 181ft
(55.1688m), with Andreas's 180ft alternative retained. The candidate uses a reconstructed
24m cornice above candidate street grade and a reported 23ft mansard rise, with a
flush roof deck. This is not an exact source height: Andreas gives contradictory 99ft
cornice/roof claims from basement floor, while the contemporary 100ft claim names no
datum or endpoint. The central opening uses the reported 30ft by 12ft dimensions.
Following actual comparison, upper sills and the first-story band were raised by0.8m
to11.0m and9.7m respectively; the two pictures still disagree in detail. Fine spacing,
wall thickness, roof inset, materials and hidden faces remain declared
reconstructions. The camera experiments document why approximately 30–31m overall
roof height was a useful starting hypothesis, not a resolution of the source conflict.

## Sources, rights and continuation

`data/sources/` and `assets/LICENSES.md` document the two public-domain-original image
routes. Reference pages retain their full margins and attribution. No restricted CHM
poster bytes or source-image texture pixels occur in this package. The original
source packets remain separately archived by the parent task.

The next city PR needs the source/native-record registrations, remaining image work,
map-based parcel placement, terrain contact and deterministic generic-context
replacement described by `data/integration-candidate.json`. That file supplies the
actual local footprint but deliberately leaves world placement null. The current
research/terrain baseline and its CI were not changed by this candidate work.
