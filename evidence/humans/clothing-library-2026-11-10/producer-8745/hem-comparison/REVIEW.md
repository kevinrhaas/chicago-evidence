# Native garment hem comparison, 10 November 2026

Joseph and Martin show a visible, bounded improvement: the old coats have triangular notches at their lower edges; the new front, three-quarter and profile renders have continuous hems. I saw no newly visible garment/body clipping in these static idle views. This does not qualify walking, bending, seated fit or hidden layers.

Otis is the control. All three old/new decoded pixel arrays are exactly identical (zero changed pixels). The PNG file hashes and canonical master hashes differ, so this is a statement about the pictured control, not byte-identical assets or preservation of runtime animation clips.

| Collection | Producer source | Renderer source |
| --- | --- | --- |
| Old stills 42730222643, producer 42703941214 | `dc998577d76a09a31a5519b7deb0c0c0f6e1f869` | `a64f26fa2fc3e05dd39cd8e55df5384646786d7b` |
| New stills 42780711312, producer 42774580234 | `8745ab40e39207b90c88b3a3e9823604f091304d` | `8745ab40e39207b90c88b3a3e9823604f091304d` |

The old local 2,806,361-byte ZIP was verified against GitHub artifact 13725250746 and its server SHA256; every local member matches it. No old artifact download was needed. The new 2,801,370-byte ZIP is artifact 13745738181. Both source bindings and all 18 PNG hashes are checked. Original pixels were read directly; no edited images or composites were generated.

Both collections use Blender 4.5.3 LTS, Cycles CPU, 32 samples, seed1789, 512×768, LOD0 and idle frame1. The renderer script itself is the identical Git blob `4ffa586ffdd23e874b0e60a8f98424a392338248` at both renderer commits. Identity/recipe, pose, parts, textures, render and provenance metadata match. Otis and Martin have identical camera, light and framing metadata. Joseph's bounds change the Y target by1.125872mm (the Y maximum changes2.251744mm), shifting the camera and lights by that amount; their rotations, scale and energies remain unchanged. His profile/three-quarter pixel differences therefore include a small framing/light change and are treated qualitatively. The front view still clearly shows the notch removal.

The figures remain stylized/mannequin-like: surfaces are smooth and have little visible cloth fibre/folding detail. Photographic, likeness and complete garment-fit flags remain **false**. Recommendation: retain this demonstrated hem cleanup as a bounded source improvement, then continue the existing T1789 material/posed-fit review. Adopt no assets from this review; preserve Otis's adopted seated-drive and natural-idle clips. T1789 is not done.

Detailed bindings, per-view hashes and raw decoded-pixel differences are in `VERIFIED-OLD-VS-NEW-METADATA-PIXELS.json`; Joseph's exact metadata differences are in `JOSEPH-METADATA-DIFFERENCES.json`; the bounded flags are in `BOUNDED-HEM-REVIEW.json`.
