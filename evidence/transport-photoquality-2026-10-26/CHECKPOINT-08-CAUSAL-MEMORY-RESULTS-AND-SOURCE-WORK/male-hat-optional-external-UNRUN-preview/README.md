# Optional male hat finish, external only

`HAT-FINISH.patch` adds `hat.finish = "rounded_felt_v1"` to a copied generator. It rounds the crown shoulder and brim edge, gives the roof a shallow 1.2mm rise, and adds a 0.7mm raised same-material band. Seating and maximum brim extent stay exact. Existing hat material, colors and head-bone weights remain; Joseph's no-hat profile stays untouched. No sculpted crease or named likeness is introduced.

`PROFILE-OPT-IN.json` lists the two external preview hat specs. `INTEGRATION.md` supplies the small optional Non-Color felt-roughness image hook for the people agent's own material block. People retains exclusive app/worker integration.

Actual Wild1835 painting and current Otis/Martin close PNGs were viewed; `SOURCE-BOUNDS.json` states the narrow silhouette support and reconstructed details. No image pixels are reused.

CPU checks passed on actual fitted source hair for both hats/all four LODs: default result arrays exact to original, source/body/hair/recipe untouched, closed oriented positive-volume meshes, valid nonzero UV triangles and unchanged head skin ownership. Finished triangle counts are 2880/1920/1200/720 per hat (old576/384/240/144). This is optional prototype geometry, not a budget or acceptance waiver. Full Blender generation, default emitted-file byte identity, GLB export, fit/deformation and visual acceptance remain UNRUN.

No app, ticket, workflow, generated asset or production flag changed. No Blender/browser job ran.
