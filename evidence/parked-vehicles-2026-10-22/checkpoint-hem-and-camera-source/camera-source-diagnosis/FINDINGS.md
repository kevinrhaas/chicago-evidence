# Finite V3 camera source diagnosis — CLOSED, no browser

The deferred popup-close recenter explains the observed V3 NORMAL orientation exactly. This is a caller observation-order issue relative to an intentional arrival-card behavior; the available evidence does not establish an application camera bug or resolve either CI draw-budget failure.

The saved position stayed `[104.5,1.8381999981403307,79]`. Bearing changed from 163.9866798667308° to 151.3858147453921° (−12.600865121338757°); pitch changed from 3.507684925681695° to 6.930053782918187°. Their combined physical quaternion rotation is 13.05554135869248°, rather than a 13.05554° yaw change. Executing the exact pinned `reaimAfterCard` function body with the recorded Hogan aim, then pinned Three's `Euler(...,'YXZ')`/`Quaternion`, produces every actual NORMAL quaternion component exactly: `[0.014935690049529538,-0.9672137232896036,0.05856475578111403,0.246667200947562]`. Maximum component error is zero. The offline control also confirms moved/flying arrivals refuse reaim. It uses an explicitly disclosed framing stub returning the recorded aim; it does not execute the full framing function or a browser.

## Source chain

- `main.js:3358–3391` documents the intended behavior: close an arrival card at the same position and center the building. `reaimAfterCard()` consumes `lastArrival`, obtains `framing(id,{card:false}).aim`, and calls `walker.teleport` at unchanged e/n with recomputed yaw/pitch. A popup `hidden` attribute MutationObserver invokes it.
- `main.js:3796` records `lastArrival` when a ride arrives and `pick(id)` opens its card. V3's successful person ride reaches idle with Hogan's card open.
- `compare.cjs:54–60` closes that card, clears intent, runs two `a.step()` calls, and returns the saved camera in the same synchronous part of `page.evaluate`. MutationObserver callbacks run at a microtask checkpoint after that work, so those two synchronous steps cannot flush the pending observer. The subsequent mode evaluate awaits Navigator selection and timers, allowing the card-close callback to run before NORMAL is read.
- `walker.js:375–403,513–532` applies the teleport yaw/pitch through the sole camera-transform writer, `apply()`, using Euler YXZ. That reproduces the observed quaternion exactly.

The actual callback invocation/timestamp was not recorded. Its source arithmetic and the recorded aim predict the exact actual result; this is strong source attribution, not an invented event trace.

## Other requested paths

Travel's arrival easing writes look intent only while a ride exists. `travel.js:550–558` returns at idle; `simulate():579–599` consumes the same steering/walker/afterWalk path until idle. `walker.update()` consumes and clears look. There is no surviving independent travel aim writer required to explain this sample.

Navigator's `navigator.js:162–238` opening changes app/level, queues change notifications, updates DOM/focus/listeners and evaluates app state. The examined resize callback (`main.js:4830–4845`) changes renderer size, aspect, FOV and projection, without authoring yaw/quaternion. Its source does not account for this exact orientation change. The production loop still calls backend update, travel update and walker update before rendering; desktop pointerlock contributes rig deltas to intent (`controls/pointerlock.js:169–184`). No actual input-event trace was saved, so absolute absence of input cannot be proven retrospectively. The popup recenter arithmetic already matches all four observed components without needing an input hypothesis.

## Measurement limits retained

V3 stopped on its first NORMAL sample, with no Xray, Ghost40 or parent sample. NORMAL alone measured primary GL3695, shipped primary3695, picking GL0, picking extra0, reported3695, residual0; reconciliation passed. The three parked groups were not visible. The actual sample cannot establish parked cost at a failing CI pose, compare parent/new, demonstrate coalescing savings or characterize the primary/pick counter issue on a pick frame. CI Xray8223/Ghost408469 remain unreproduced and their historic pose is unavailable.

## Possible later protocol, explicitly controlled and nonhistoric

No caller is prepared or released by this recommendation. If root later requests a diagnostic pair, retain the existing finite guards (one ≤600s process group, each boot≤240s, entry≤30s) and use a predeclared static Hogan pose, rather than an asynchronous travel/card prefix. A concrete pose already supported by this sample is e104.5, n−79, bearing151.3858147453921°, pitch6.930053782918187°, walking eye1.68, with the same declared viewport/detail/quality/season and published assets. This is an observed settled V3 pose chosen before new measurements; it is not the historic CI pose and must never be labeled a CI reproduction.

For each arm and raw NORMAL/Xray/Ghost40 mode: enter world, require travel idle, close existing cards, select/configure the requested Navigator confidence controls, and allow those awaited UI tasks/microtasks to finish. Only then place the same literal walker pose. Placement is an explicit experimental intervention; clear caller-owned movement intent at placement, without disabling target/gaze, production backend, governor, picking, or actual post-production stats. Run the ordinary production step and retain its actual cadence/target timing and passive per-pass/driver/pick/extra attribution. Record before/after position, physical quaternion, projection and render state; stop on drift, reconciliation failure, unmatched arm state, or deadline rather than adjusting pose or retrying to seek a pass. Any mode-specific animation hold must remain explicitly declared and identical between arms. Do not add warmup or private target resets to force a desired counter result.

Root may decide whether such a controlled experiment is useful. This finite diagnosis needs no current checkout/index guard and does not block the covered source preflight/commit/push. No source fix, budget change, assertion change, browser launch, dispatch or rerun is proposed as part of this completed task.

## Existing actual capsule

`/workspace/shared/parked-2979-paired-overlay-ACTUAL-v3-STOPPED-CAPSULE.tar.gz`, bytes4532314, SHA256 `10803525ddd802d4c3f3fd9bc4ba3f6a74b7dba74bc078733f85561e6551657f`, contains the closed actual V3 evidence and compact prepared support, with the documented runtime/mirror omissions. It remains unchanged. This directory adds only finite source excerpts, hashes, and the offline control; no full caller/package is frozen anew.
