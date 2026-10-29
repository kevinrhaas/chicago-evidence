# Focused native context recovery diagnosis

Actual desktop03 remained NONPASS: rc1, 3484.828873 seconds, not timeout. Thirteen pre-context phases and the ordinary reload/restored scene completed. A pageerror said `Cannot read properties of null (reading byteLength)`; that observer did not retain its stack or timestamp. Neither cause nor baseline attribution is established.

## Concrete source findings

- Three WebGLAttributes.createBuffer reads `attribute.array.byteLength` at vendor/three-0.185.1/three.module.js:70; update has another read at line273.
- upload-release.js deliberately makes static `attribute.array = null` after upload. Railway now uses that native path on desktop, as other layers already do on phones.
- Three registers its native context listeners in its constructor. Its restore listener clears `_isContextLost` and recreates GL state including the attribute cache (`initGLContext`), before the app's later crashGuard listener runs.
- crash-guard.js requests `window.location.reload()` on first restore when arrays/images/compressed levels were released. Navigation is asynchronous. Repeated loss deliberately requires visitor Reload.
- The app's main animation loop has no context-loss/reload-pending pause, and still calls tick/confidence.render until navigation. Once Three has cleared the lost flag and attribute cache, a frame can try uploading a null page array.

This is a concrete unguarded restore-to-navigation interval and a plausible cause, not a proven attribution of the actual message. Capture its full stack/order before applying the proposed patch.

## Prepared diagnostic — NOT RUN

`run-focused-native-context-trace.cjs` boots the unchanged published `/1904/` without URL flags, performs the native welcome entry and an actual analytic track pick, proves selected rail arrays were released, induces a real WEBGL_lose_context loss/restore, records ordinary navigation, boot/world/track/pixel-ratio/GL/release states and before/after PNGs. It records full pageerror stacks and UTC/document-relative timestamps, main-frame navigation and native canvas lost/restored events. Strict zero-pageerror/console-error assertions remain; no recovered error is waived.

`run-sealed-focused-context-trace.py` owns a native stdlib server, verifies all 53 frozen source paths, the complete semantic index and all 5630 published mirror files before/after, verifies its prepared payload pins, drains the server thread, and emits a guard closure. The outer transport-supervise must own the entire process tree and enforce its fresh timeout. Use a new name beginning `RAIL-CONTEXT-ONLY-`, e.g. desktop and RAIL-CONTEXT-ONLY-DESKTOP-01; never reuse a prior result name.

Default desktop Full is primary. No Full/Balanced/Full rebuilding sequence or phone/far/fullgate is included. This protocol is a focused diagnostic, never full lifecycle or photographic acceptance. H has priority for the heavy/GPU slot; root must explicitly grant execution after review and actual resource checks. No execution, server or browser has started during preparation.

## UNAPPLIED patch hypothesis

`UNAPPLIED-HYPOTHESIS-stop-loop-on-context-loss.patch` stops the main animation loop on context loss and resumes only if no native upload resource requires reload. First/repeated losses needing reload stay paused until navigation. Existing crashGuard reload cap, step-down/card policy, memory limits, upload release and error propagation remain intact. The named callback is installed after boot only when context is not paused, covering a loss during boot.

This is a proposal against the currently frozen staged main.js, syntax checked in an outside-app scratch file then scratch removed. It has NOT been applied or functionally qualified. Other direct renderer uses (placement work, capture/manual step) are outside its guard, so a different stack would require a different fix. Do not use this patch to claim the current candidate passes. Current app source SHA and all source/index/full-mirror guards remain unchanged.
