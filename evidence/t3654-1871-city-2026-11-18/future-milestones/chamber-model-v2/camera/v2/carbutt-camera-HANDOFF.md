# Carbutt third-camera handoff

`../carbutt-original-candidate.json` is a **preliminary diagnostic camera**, ready for the native renderer. No model render, match record, or image-gate acceptance was created by this camera task. The source was inspected directly as the complete preserved 2737 × 1360 stereo card. Only its **left exposure** supplies observations. The camera retains the original full-card image dimensions and pixel origin; the reference image is neither cropped nor resampled. No right-half landmark is mixed into the solve.

The current fit uses thirteen architectural points: three cornice endpoints, three upper-roof endpoints, two partly visible pavement contacts, and all five north upper inner arch vertices. Five upper sill observations are held out and reported separately. The northeast building-grade intersection is obscured by fence, tree and street objects and is excluded. Every observed point, projected point, uncertainty and residual is preserved in `carbutt-camera-fit-audit.json`; numbered fit points appear in `carbutt-camera-fit-coordinate-plot.png`. The two additional `carbutt-*-coordinate-plot.png` files are original-pixel inspection plots with full-card axes.

The camera fits the unchanged recipe: 93 ft frontage, selected 181 ft depth, reconstructed 24 m cornice and 31.0104 m roof top, 1.9 m roof inset, 11 m upper sill, 9.144 m central opening height and 8.8 m flank opening height. It uses the existing camera helper's fixed 2 m eye height, unit pixel aspect and zero skew. Camera coordinates are east, north, up; the building extends south from its north-facade origin. Reported dimensions remain source claims with the already documented depth and height-datum conflicts.

| Diagnostic | Result |
|---|---:|
| Unweighted RMS distance, 13 fitted points | 14.3767 px |
| Maximum fitted-point residual | 26.3903 px |
| Five held-out sill residuals | 10.04–26.67 px |
| Fixed camera eye height | 2 m |
| Optimized roll | +5° bound reached |
| Principal point, full-card pixels | approximately (1550.72, 555.35) |
| Focal length in pixels | approximately 1637.20 |

The fit is **not an accepted optical calibration**. Its roll reaches the configured bound and its principal point extrapolates beyond the left exposure; that is a warning about model/camera/correspondence degeneracy, not evidence for an unusual historical lens. The archived principal coordinates are full-card coordinates even though their fitted x lies outside the selected photograph. Constraining the principal point to an assumed lens center would introduce another unsupported optical assumption. The native diagnostic lets the reviewer see the unresolved error; it must not be published as an exact historical camera location.

Other limits are material: the camera can absorb errors in the current reconstructed roof rise and window levels; the apparent cornice/coping endpoints have finite projection depth; distant roof detail is soft; two grade points are partly obscured; and the two stereo exposures have unknown baseline and calibration. No stereo triangulation, image aspect correction, terrain datum recovery, or height-datum resolution is claimed. The five held-out sills visibly remain low in the projected model despite fitting the heads, so a fitted upper arch is not proof that its complete aperture matches.

The photograph makes several form distinctions clearer than the drawings: the central roof circle reads as a pale solid/clock-like face rather than dark glazing; the triple portal has slender round shafts and separate upper spandrel decoration; the central upper fan has a three-light group; north basement openings are rectangular; the front roof apron and projecting cornice have substantial profiles. Exact clock-face markings, carved ornament, stone color, tenant continuity in October 1871, and street activity are outside this camera solve. The parent owns all model changes and source-rights records.

To repeat the numerical experiment, run `PYTHONDONTWRITEBYTECODE=1 python camera/v2/carbutt_fit_camera.py` from the candidate root. The helper reads only the candidate recipe, archived full reference, and existing camera math. It writes the Carbutt native camera, fit audit and coordinate plot; it does not render the GLB. Re-running it deliberately changes those camera inputs and requires a fresh native render/review. Do not rerun it over a hash-frozen accepted review. Its output is deterministic within the installed numerical environment, not a proof of a unique global camera solution.

All writes by this task are new Carbutt-named files under `camera/` and `camera/v2/`. Existing camera JSONs, recipe, model, source records, documentation, app files and repository state were left untouched.
