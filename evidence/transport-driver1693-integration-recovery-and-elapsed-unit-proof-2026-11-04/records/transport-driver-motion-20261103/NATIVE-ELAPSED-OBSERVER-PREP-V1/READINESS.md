# Prepared native transport pace observer — false GO

Nothing here has been executed. APP, source, assets and the owned native gate
remain untouched. ROOT-GO-UNBOUND-TEMPLATE.json is false and contains deliberately
unbound future source/runtime pins. The wrapper refuses it before launching any
browser. The canonical lock is mandatory and nonblocking.

This is a finite extension of REAL-LOOK-RENDERED-FIXTURE-V1's server/browser/
supervisor scaffold. It reuses that fixture's exact source verifier by import,
its original resource guard and supervisor, browser version and browser arguments.
It serves the actual source app directly. The prior flat-ground scene fixture
is not used: actual mounted world ground, clearance, horse support, vehicle,
horses, driver, hitch, native world camera and native render budgets all remain.

## Scope and admission

- One actual app load per viewport, with sequential requested 1, 2 and 4FPS
  windows, each containing two seconds of requested active time. Desktop is
  1280x800, 1835 Full; narrow viewport is 390x780, 1904 Balanced. These are two
  explicit eligible transport cases, not a claim about default phone Light.
- Every viewport's complete load, native assembly admission, camera, motion,
  controls, screenshots and cleanup must fit the original 120 seconds. The outer
  supervisor retains its original 600 seconds with no override. There are no
  per-scene retries, added app reloads, extended boot allowances or cadence
  fallback. A native boot that cannot fit the remaining viewport budget is
  NONPASS. A slow renderer cannot be made to support 4FPS by this observer.
- The runner stops the normal loop with the existing renderer.setAnimationLoop
  API, then calls the unchanged native api.step on actual browser timers. No
  getDelta, performance.now, requestAnimationFrame, renderer method or runtime
  module is replaced. No virtual-time or artificial-delta clock is used.
- The rendered-frame cost must fit each requested cadence's period. Otherwise
  the report states cadence unavailable and remains NONPASS; it never presents
  a slower actual cadence as a forced4FPS result.

The practical minimum is six seconds of scheduled active waits per viewport,
plus actual native rendering, model loading, control frames, six screenshots
and cleanup. The absolute deadline governs all of them. Root should inspect
the latest real boot/frame costs before authorizing; this preparation does not
establish that the full native world can admit that matrix within 120 seconds.

## What is measured

The loaded seated driver's native mixer time is an independent visible-time
readback. Each active frame brackets api.step with actual performance.now reads,
checks that admitted native mixer time falls inside those wall-clock brackets,
then compares native travelled metres with min(configured speed * admitted time,
.25m). This checks the actual clock wiring as well as the physical advance cap.
The old test's speed1 ten-second .25m limit remains in the separate V2 Node patch.

Snapshots record native path distance, four wheel angles, both horses' actual
distance-driven gait counters and support readings, actual horse bone locals,
protected seated-driver body transforms, original world budgets and camera.
Wheel deltas are bounded by the actual route curvature/geometry; the existing
integrator tests remain authoritative for exact wheel arcs. Horse phase is
reported as actual travelled distance / unchanged .135m stride, with actual
loaded bone-pose change away from whole-cycle sampling aliases. The configured
speed remains .084375m/s. Nothing asserts a natural stride or ordinary walking
speed.

Sequential windows start at different positions on the same real journey.
There is no rewind, initial-distance edit, assembly reset, fake phase equality
or equal-origin wheel claim. Each window reports its own actual admitted wall
time and configured speed. This supports comparing observed pace across
cadences without pretending unequal timing windows have identical endpoints.

## Actual transitions and independent clocks

Eight finite control readings per viewport cover:

1. Public native Stop/Continue with no intervening stopped tick.
2. Public native Stop/Continue with a stopped tick.
3. Native animation hold/release.
4. Browser reduced-motion preference hold/resume.
5. Reduced-motion toggles without a held tick.
6. A genuinely hidden/shown native browser tab.
7. Native HUD reconstructed hide/show without a held tick.
8. Actual draw-range return with the native same-tier setTier/lastUpdate
   synthetic visibility replay before the first actual returned frame.

The first actual resumed journey frame moves zero, then the next real interval
advances at the configured pace. The independent look keeps running during a
journey-only Stop, and pauses/rebases across held/hidden/reduced/range periods.
The range synthetic refresh must prime neither production elapsed clock; this
specifically detects the V1 visual-priming edge fixed by the V2 conditional
visual guard. Native hidden state must actually become document.hidden=true;
an unavailable headless browser visibility transition produces NONPASS, never
a document.hidden property replacement.

## Pictures and honest visual scope

Each requested cadence has a before/after PNG from the same fixed native camera
and viewport: six pairs / twelve PNGs total. The camera recipe and exact matrix,
drawing buffer, native measurements and PNG hashes are saved. No pixel ROI or
arbitrary changed-pixel threshold is used. Root must inspect the actual PNGs to
confirm that the horse/team is visibly rendered and that the small configured
advance is useful. The numerical observer does not convert a background pixel
change into a horse-motion acceptance claim.

No photographic quality, natural gait, trusted DOM interaction, consumer FPS,
all-scene release or visual-owner signoff is inferred from an observer PASS.

## Root's future concrete admission

After PR1693 merges, the current upstream merge closes, the accepted V2 patch is
applied/reviewed, and the existing canonical owner releases the lane:

1. Recheck provider readiness and the same current resource epoch.
2. Bind actual HEAD/TREE/APP/semantic-index and all required runtime hashes into
   a new ROOT GO file. Verify all thirteen unchanged asset/config/certificate
   pins and fixture/helper pins. Current merge-owned source is deliberately
   inadmissible: the reused source verifier refuses MERGE_HEAD.
3. Review the exact two-case schedule and original120/600 deadlines; set the
   explicit approval/lane-release/candidate-reviewed fields true only then.
4. Run this wrapper once with an outside-APP output directory. It requires the
   original canonical lock and writes only observer evidence outside APP.
5. Read CLOSED.json plus the final browser report. Require original deadlines,
   current resource acceptance, all owned descendants reaped, native browser/
   server contexts closed, empty native TMPDIR ownership and exact source/pins
   before/after. Preserve any partial NONPASS evidence; no automatic retry.

The wrapper uses a private outside-APP TMPDIR and deletes it only after native
supervisor cleanup is complete. Missing cleanup, source drift, resource failure,
budget breach, unavailable native hidden state or unavailable cadence cannot
produce PASS. The GO template is still false; no permission or execution is
requested while the current four-part gate owns the lane.
