# Confidence-shadow repair: focused native proof

The application repair is committed at `3f81ece88f0d57d26063d786e6bccd9658ab89c3`. Near buildings, trees and bridge batches now use confidence-patched depth materials so their shadows follow the color pass when confidence is off, dithered or hidden. Geometry, lighting, historical registration and the existing detail-tier shadow policy are unchanged.

`native-proof/` is the frozen 30-file result bundle released by the test owner after the browser closed. All 29 hashes in its `artifacts.sha256.json` were verified before copying, along with all 16 selected candidate inputs and five runtime-module hashes against the committed 3f81 source. The archive retains the exact patch, regression test, positive log, expected-failing old-renderer negative control, 17-case confidence appearance test log, and 178-fixture check-harness log.

The native candidate was a copy of the published **92ac** mirror with **only `walk/js/city-context.js` replaced**. Five relevant runtime modules match 3f81 exactly, as recorded in `native-proof-summary.json`. This was not a freshly generated complete 3f81 publication.

One 1280×800 Full-detail session exercised commercial buildings, a bridge and trees in three confidence states. Each state also ran the old-depth fallback as a negative control: 18 actual native render states, nine candidate screenshots and eight actual GPU shader sources. Off-state occupied-shadow coverage matched the fallback; dither reduced coverage; hidden coverage was zero for each pose. Zero page, shader, network or application errors were recorded. The 512×512 PCF comparison readback measures occupied-shadow coverage at a stated reference depth, not recovered floating-point depth values.

This is software-rendered functional shadow acceptance, not hardware performance, photographic reconstruction or complete current-tree validation. The earlier ae259 city reports separately cover unchanged geometry and walking behavior. The new regression check changes source-partition allocation; old partial passes retain their original source scope. Full source and fresh legacy-browser gates remain required.

The portable `../receipts/confidence-shadows-3f81.json` and revision-7 checkpoint were committed before the native probe completed, so their pending-native entries are historical. The released native summary/report in this folder records the later PASS without changing those original receipts.
