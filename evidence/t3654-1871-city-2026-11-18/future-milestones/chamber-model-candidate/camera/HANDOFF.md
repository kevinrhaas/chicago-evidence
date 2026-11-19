# Chamber reference and camera handoff

Both inspected exterior candidates **visibly differ** from the cleared original-building views. This is a useful, rendered starting point, not a passed image gate, solved historical camera, recovered survey, or finished photographic model. The main audit below preserves the earlier GLB `e48bc95b903e76a70320efc401553ad83d173bc73a12d1ef1f201a6511df4fee`; the final comparison section records the subsequently adjusted GLB `15c8c236110fe5bdb34f5c8d3269580c2303bb761fbf446b967c776812716e6e`.

## Current review inputs

| View | Native camera | Fit RMS | Maximum residual |
|---|---|---:|---:|
| Andreas engraving, 2306 × 3299 | `andreas-original-candidate.json` | 21.3997 px | 41.5563 px |
| Chicago Illustrated lithograph, 1400 × 1082 | `illustrated-original-candidate.json` | 15.0911 px | 29.1725 px |

The two camera JSON files are frozen to preserve the current native match hashes. Detailed observed/projected points are in `actual-shell-camera-fit.json` and `lithograph-shell-camera-fit.json`. `reference-landmark-audit.json` preserves source hashes, all full-raster pixel landmarks, reading uncertainties, and finite line directions. Pixel origin is upper left; x increases right and y increases down. No crop or resampling is used to define camera coordinates.

Both fits use nine hand-read box corners, fixed pixel aspect 1 and zero skew, a reconstructed 2 m eye height, a 28.3464 × 55.1688 m footprint, cornice 24 m, top 31.0104 m, and 1.9 m top-roof inset. The native frame is `[east, north, height]`; the asset frame is `[east, height, south]`. The north facade midpoint is the grade origin. Grade is a common flat review plane, not terrain validation. Soft review lighting is a modeling aid; it does not recover 1871 weather or print illumination.

The RMS is the unweighted RMS of point distances after an uncertainty-weighted nonlinear fit. These are coarse fits with substantial residuals. The largest Andreas error is the southwest upper roof edge; the largest lithograph error is the partly obscured northeast grade. Trees, figures, projecting ornament, and inconsistent engraving perspective complicate the corner readings. Neither optimizer reaching a solution nor a close roof silhouette establishes facade alignment.

## Observed form and current differences

- Both sources show five north upper arch heads arranged 2 / 1 / 2. The larger central opening has three principal vertical lights and a group of three small circular/arched lights in its head. Four flanking openings show paired vertical lights with a circular upper light. The current candidate expresses this rhythm, but the central hood and crest remain much simpler.
- A triple arched entrance sits below the central upper opening, with two lower arched windows on each flank. Current portal depth, pier/profile proportions, lower openings, basement apertures, and railings are reconstructed approximations requiring further source comparison.
- The north roof has four smaller oculi and a larger framed central circle with an ornamental crest. Both views show an ornamental central finial and tall staff; they do not establish flag continuity on the chosen 1871 date. The current bare staff is bounded reconstruction. The initial oculi clipping was corrected in the current candidate, but the current simple rings and central crest do not reproduce the source dormer casings and sculpted profiles.
- Ten tall west upper arches are readable in the Andreas view. The lithograph tree hides much of the west elevation. The rear terminal details and side entrance placement remain uncertain. Do not treat the repeated generic side rhythm as measured elevation geometry.
- The strongest remaining visual discrepancy is facade vertical alignment. In the lithograph comparison, multiple candidate upper arch heads and the first-story belt sit approximately 25–45 full-image pixels below corresponding source features, despite a relatively close major roof outline. This is a visual range, not a new solved correspondence or metric height. Andreas is closer in some zones but still differs in central ornament, roof/cornice profiles, and opening placement. A next pass should explicitly constrain these features rather than fit only the bounding shell.
- Cornice, modillions, arch hoods, rustication, crestwork, and bay projections remain uniformly simplified. These source-visible profiles are larger than incidental rendering noise and prevent a matches verdict. Current roof and glazing tones are provisional; monochrome engraving does not establish roof color, and lithographic wash is not calibrated material evidence.
- The south/rear and unseen east facade are not verified by these two perspectives. Omitted or repeated details there must retain reconstructed status. Neighboring buildings, street life, tree, vehicles, and ancillary annex are outside this bounded main-exterior candidate and are not evidence of a failed standalone-building silhouette.

## Dimensions and ambiguity retained

The 93 ft frontage is a reported scale constraint. The current depth selects the contemporary 181 ft report while retaining Andreas's 180 ft alternative. Andreas reports a central window 30 ft high by 12 ft wide; the current opening uses 9.144 × 3.6576 m, but its sill and exact aperture definition are reconstructed.

The roof-height prose remains contradictory: Andreas describes a roof 23 ft above the cornice and 99 ft from basement, then describes the cornice as 99 ft from basement. A separate contemporary 100 ft height lacks a clear datum/endpoint. The current 24 m cornice and 31.0104 m top are an explicit working reconstruction; they do not resolve the basement datum or establish exact source height.

Initial alternative-camera diagnostics used a different 0.8 m roof inset. At fixed 7.0104 m roof rise, 30 m top produced 15.93 px RMS and 37 m top 33.77 px RMS; the latter reached a roll bound. Letting cornice vary gave approximately 23.71 m cornice at 30 m top versus 29.06 m at 37 m top, with RMS 15.42 versus 33.11 px. These tests favor the lower working shell under their particular assumptions, but are not a height determination. Their files (`box-camera-comparison.json`, `free-cornice-comparison.json`) must not be substituted for current 1.9 m inset camera evidence. `first-shell-fit-inset-0p8-superseded.json` is explicitly superseded.

The `held_out_central_window` diagnostic in `actual-shell-camera-fit.json` uses a 10.5 m sill, whereas the current recipe uses 10.2 m. Its approximately 151 px span versus approximately 152 px hand-read source height is only a reported-length sanity check; it is neither a feature fit to the current sill nor independent survey validation.

## Files and replay

- Native review cameras: the two `*-original-candidate.json` files above. Native `.match.json` files and final verdicts are managed by the parent candidate author; this audit does not overwrite them.
- Exact corner fits: `actual-shell-camera-fit.json`, `lithograph-shell-camera-fit.json`.
- Exploratory solvers: `fit_box_cameras.py`, `fit_free_cornice.py`, `fit_lithograph_camera.py`. Python requires NumPy and SciPy. The current Andreas parameters are reproducible by importing `fit_box_cameras.fit` and calling `fit(31.0104, inset=1.9)`. The lithograph script runs its fixed current-shell fit and writes its camera/report; do not rerun it against the frozen review without deliberately regenerating and reviewing the comparison.
- Solver source-file reads resolve through `ROOT.parent / 'references'` to the verbatim archived originals, so the scripts can run after this candidate directory is moved. Original acquisition paths remain in the archived earlier fit reports and source records as provenance. Only the solver lookup paths were made portable; neither the native camera JSONs nor the numerical fit reports were rewritten, and no solver was rerun after this edit. The numeric `fit()` function itself has no source-path dependency.
- `andreas-coordinate-viewport.png`, `lithograph-coordinate-viewport.png`, and `front-arch-measurement-viewport.png` are analysis coordinate plots of original source pixels. `andreas-actual-comparison-inspection.png` and `illustrated-actual-comparison-inspection.png` are coordinate plots of the actual current side-by-side comparison, retaining full-source axes. They are review aids, not new historical reference assets.
- `reference-landmark-audit.json` and this handoff are new audit files. No root repository or app data was mutated by this camera task.

## Remaining work

Inventory and assess every available original-building view, including the outstanding Carbutt photographic lead, before claiming a comprehensive image gate. Acquire only rights-cleared originals. Refine correspondence definitions for grade, cornice edges, upper sills, arch vertices, portals, and roof projections; fit camera and reconstructed feature heights without silently changing attested plan dimensions. Render each resulting current GLB with each current camera, inspect the actual outputs, and keep every visible substantive discrepancy open until resolved. Preserve conflicting height claims as claims rather than promoting a working reconstruction to an archival measurement.

The two reference files are verbatim cleared public-domain original publications provided by the parent source packet. Source/scan licensing and provenance remain governed by that packet's records. No Chicago History Museum poster bytes or third-party photo textures were used in this task. The candidate materials are procedural and outside this camera task's authorship.

## Central feature follow-up on the same e48bc95b candidate

A closer full-coordinate comparison (`central-window-current-alignment-inspection.png`) was made after the broad audit above. The ranges below distinguish the inner glazing vertex from the much taller decorative arch hood; they are approximate manual readings, not new fit inputs. Horizontal coordinates differ slightly between the source and candidate because the camera is still preliminary.

| Mid-north-facade feature | Andreas source y | Andreas candidate y | Lithograph source y | Lithograph candidate y |
|---|---:|---:|---:|---:|
| Central inner arch vertex | 1840–1845 | about 1845 | 488–493 | 510–515 |
| Central glazed sill | 1977–1980 | 1993–1996 | 611–616 | 637–643 |
| Major first-story belt zone | 2005–2015 | 2017–2027 | 633–645 | 660–672 |

Both sources support lifting the belt modestly. A roughly 0.8 m increase would improve the direction of the visible error, but cannot be treated as an attested floor height. A 0.7–1 m lift of the upper windows would improve both sill positions and the lithograph head; it would move the Andreas central head above its present reading. A 1.5 m blanket lift is not consistently supported. The differently sized offsets should remain unresolved until feature correspondence/camera and sill/head geometry are fitted together. The earlier rough 152 px central-opening diagnostic used a less precise aperture reading; this closer inspection reinforces why it must not be used as an accepted metrology result.


## Final comparison: 15c8c236

Both native comparisons were inspected again after the parent raised the upper sill from 10.2 to 11.0 m and first-story belt from 8.9 to 9.7 m. The reported 9.144 m central opening height, shell, and both frozen camera files were retained. Final GLB SHA-256: `15c8c236110fe5bdb34f5c8d3269580c2303bb761fbf446b967c776812716e6e`.

The modest rise improves the Andreas central sill to approximately y1980 and brings the first-story belt closer to its source position. As anticipated, the central inner arch vertex is now approximately y1832, somewhat above the source reading of y1840–1845. In the lithograph, the candidate inner arch vertex is now about y500–505 and sill about y627–632, reducing but not eliminating their previous downward offsets from the source. The belt also moves closer. These are visual readings from the actual final render, not refitted-camera residuals. The fixed bounding-shell camera RMS/max values remain unchanged because those fitted geometry points did not move.

The final verdict remains **differs** for both views. The improved opening/belt placement does not resolve ornamental arch and dormer profiles, cornice detail, side entrance and basement rhythm, exact opening definitions, terrain contact, or competing source perspective/height interpretations. The final comparison is preserved in `final-both-comparisons-inspection.png` and `final-central-window-alignment-inspection.png`; the earlier inspection plots were not overwritten. `final-review-audit.json` binds this inspection to the final GLB, both camera files, both references, and both actual native side-by-side output hashes.
