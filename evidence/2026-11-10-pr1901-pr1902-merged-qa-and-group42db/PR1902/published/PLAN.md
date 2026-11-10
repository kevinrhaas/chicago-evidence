# T-3041 actual published-scene review, prepared 2026-11-09

No browser launched. No source edits, publish, installation or GitHub mutation. The source branch remains frozen. Only `node --check review.mjs` has run successfully. This helper is prepared code, not a runtime PASS.

Use after the parent qualifies the actual native15 outputs and grants the serial GPU slot. Serve the already-built published mirror from its real output root; do not point at the source viewer or rewrite asset URLs to source masters. Use the same pinned Playwright1.56.1 already installed for the current work and `/usr/bin/chromium` or the parent's approved browser executable. No npm/pip install or publish happens here.

## Bind actual native bytes first

Write `expected.json` externally, from the retained native run's actual source SHA and web output hashes. No old1704 output, arbitrary hash or empty template may count. Example SHAPE only:

```json
{
  "source_sha": "ACTUAL_BAKED_SOURCE_COMMIT",
  "native_run": "ACTUAL_CURRENT_NATIVE_RUN_ID_OR_URL",
  "build_prefix": "ACTUAL_PUBLISH_CHECKOUT_HEAD_SHORT_SHA",
  "assets": {
    "first_fort_dearborn_pickets_outer": {"sha256": "ACTUAL_NATIVE_WEB_GLB_SHA256"},
    "first_fort_dearborn_pickets_inner": {"sha256": "ACTUAL_NATIVE_WEB_GLB_SHA256"}
  }
}
```

`build_prefix` is optional; where supplied, it must be the build stamp of the actual published checkout, which may be later than the source commit originally baked. The helper independently fetches the two exact `record.assetUrl` addresses the running app loaded and checks byte SHA256 against this manifest. It records actual sidecar URLs, selected asset URLs/detail, source attrs, placement, footprint and native-loaded status. The supplied source/run metadata does not itself prove ancestry; root still verifies the retained branch parent and full15/13controls/1029foreign+6versions before calling this runtime review qualified.

## One viewport per bounded foreground command, serial

Set `CHICAGO_PW_MODULE` to the absolute `index.mjs` file of the already-installed pinned Playwright package. Set `CHICAGO_PUBLISHED_1812_URL` to the actual published local URL, e.g. `http://127.0.0.1:PORT/walk/?year=1812`. The helper uses `new URL`, forces `year=1812`, and refuses source-viewer paths. It starts no server.

```bash
PW_MODULE="$CHICAGO_PW_MODULE" PW_EXECUTABLE=/usr/bin/chromium \
  timeout 570s node /tmp/nov9-west-published-review/review.mjs \
  --url "$CHICAGO_PUBLISHED_1812_URL" --viewport desktop \
  --expected /tmp/nov9-west-published-review/expected.json \
  --out /tmp/nov9-west-published-review/desktop \
  > /tmp/nov9-west-published-review/desktop.log 2>&1
```

Then, after desktop has closed its browser:

```bash
PW_MODULE="$CHICAGO_PW_MODULE" PW_EXECUTABLE=/usr/bin/chromium \
  timeout 570s node /tmp/nov9-west-published-review/review.mjs \
  --url "$CHICAGO_PUBLISHED_1812_URL" --viewport phone \
  --expected /tmp/nov9-west-published-review/expected.json \
  --out /tmp/nov9-west-published-review/phone \
  > /tmp/nov9-west-published-review/phone.log 2>&1
```

Viewport desktop1280x800 at DPR1; phone390x780 at DPR2/hasTouch true/isMobile false, matching `smoke_renderer.mjs`. Fresh browser per viewport, serial, default app detail preserved. SwiftShader launch flag follows the existing smoke. Boot240s and welcome90s match existing bounded waits. The outer570s cap is a hard stop with no green verdict if exceeded; receipt is written incrementally. A launch/import failure may precede the first receipt; keep the command log.

## What is exercised

Existing actual app hooks are sufficient: `__chicago4d.registry`, `fortGates.gates/group`, `interactions.act/update`, `interactKey.current/refresh`, `walker.teleport/update/state/surfaceAt`, the shared `intent`, `walkBudget`, `setFly`, `setAnimationHold`, `setFloraSpread`, `step` and `welcome.enter`. No source instrumentation or new app hook is needed.

The helper verifies booted1812 target1812-08-14; actual native assets loaded; published `/data/gltf/` web URLs and byte hashes; expected original south width1.89 and offsets inner-2.62/outer-2.83; four gates initially shut; zero hard actual app loading problems, with every retained review annotation preserved and verified exactly. It derives camera positions from the actual gate things' world `at`, rather than duplicating the model's UTM-to-local conversion.

It then enters the actual town, docks the Navigator, dismisses help and pauses the existing world clock with the same animation-hold hook the smoke uses. Rendering remains real. Both west leaves are opened through a real R keyboard event on desktop and actual Interact-button tap on phone, with assertions that the current in-reach offer identifies the intended gate, the action actually starts, and its real engine completes to open/swing1. The existing interaction clock is advanced synchronously while held; no gate state or mesh rotation is assigned directly.

Passability uses the actual loaded app's `walker.update` and shared `intent`, with its real terrain, heightfield, current scene footprints and dynamic gate walls. It attempts a fixed distance at1/60s steps and records positions, blocking, groundY, actual gate states and speeds. There is no flat-ground fixture and no replacement collider. It proves four west states: both shut and inner-only open stop at the outer leaf; outer-only open reaches and stops at the inner leaf; both open enter at least3m beyond the inner row and finish inside the actual inner footprint. Cross-axis drift is held below0.08m so sliding elsewhere cannot masquerade as passage entry. A bound requires a shut-case walk to reach within1.2m of the leaf, so an unrelated earlier terrain obstruction cannot masquerade as gate collision. South both-shut and both-open are also rechecked through the real scene.

This movement is deliberately a synchronous drive of the actual app's shared intent/walker; it is not a claim that the touch joystick or keyboard movement backend was manually exercised. The button tap and R-event checks separately exercise actual gate UI. The parent still runs the required broader published smoke for input/chrome/renderer qualification. Native-image fit likewise remains separate.

## Seven actual screenshots per viewport

1. `01-west-context-closed.png`: aerial oblique view includes the northwest tower, west range and chosen gateway context.
2. `02-west-outer-closed.png`: eye-level west approach, outer leaf shut.
3. `03-west-outer-open-inner-closed.png`: outside, outer leaf open and inner leaf still shut.
4. `04-west-both-open.png`: same approach, both leaves open.
5. `05-west-through-looking-back.png`: after the actual successful walk, looking back at both rows.
6. `06-south-preserved-closed.png`: unchanged south entrance, shut.
7. `07-south-through-looking-back.png`: after the actual south walk, looking back through the main passage.

Inspect every screenshot using view_image. Check visible holes in both native curtains, posts/leaf fit at reconstructed stockade height, no immutable baked leaf blocking the runtime leaf, enough head/body clearance, no collision or overlap with the northwest tower/west range, and preserved south lintels/jambs and two-leaf shapes. Compare each closed/open pair for the actual change; do not infer visible geometry from gate state strings alone. Read phone at CSS390x780 despite its780x1560 DPR2 PNG pixels. If a view is obscured or the light/camera is unhelpful, record that and adjust only the temporary browser camera; do not edit the authored Currey diagnostic camera or historical placement.

Each viewport's `receipt.json` contains hashes, loading errors, real interaction/movement samples and screenshot names. Success is named `PASS_FOCUSED_REVIEW_REQUIRES_HUMAN_SCREENSHOT_INSPECTION`. It is never the full smoke or image-match verdict. Failures leave a partial receipt and best-effort `FAIL.png`; do not weaken an assertion to hide a real terrain, mesh, interaction or loading problem. The helper closes its own browser in finally and restores animation hold where the page remains available.

## Review scope still outside this helper

Actual native15/13controls/foreign-row audit; full check gate; the required existing full/diff-selected published smoke; actual fixed Currey picture composition; source/provenance qualification; human screenshot judgment and the original finite discrepancy decision. No automatic image `matches` or ticket closure occurs.

## Review-annotation correction before the first west browser run

Native dispatch metadata currently identifies exactly one west request: run42715284565, source b079b1479e2bb0abaf6c6f341db29925f7832796. This preparation does not inspect target asset hashes or qualify outputs before they arrive. Root supplies actual retained asset hashes/run/source in expected.json once audited, then grants the serial GPU slot. No west browser has launched.

The external helper now follows the retained-review-note policy in smoke_renderer.mjs1892–1906 and the successful Sauganash review. Every raw problem remains in the receipt. An allowed annotation must match the entire exact scene-loader sentence, including "this flag does not block scene release", and bind an actual registry key equal to its record.id and sidecar.id with review_required===true. Every flagged registry record must have exactly one note. Unknown IDs, false/malformed flags, changed sentence, omitted/duplicate notes, or any other message fail; no broad regex exception or provisional/placeholder exemption is used. The hard list must be empty at boot and after all gates/walks; declared record IDs must stay unchanged. Optional expected.json review_ids pins the set independently to the qualified native-manifest records; omission still enforces the actual registry/message equality used by the existing smoke. This handles zero or several legitimately flagged records without borrowing Sauganash's scene-specific14IDs.

Only node--check has run after this correction. review-before-annotation-policy.mjs preserves the prior external helper, and ANNOTATION-CORRECTION.json records hashes. No source edits, browser, publish/install, asset-hash reads or GitHub mutation occurred.

## Actual first desktop cap and draw-only optimization

First actual desktop attempt hit outer570s cap after six screenshots and both actual R opens plus all four west walking states had passed. It did not finish south checks; raw receipt/log/screenshots preserved under desktop-attempt1-cap570, never relabeled green. Browser closed.

The external helper then adopted the existing smoke_renderer holdDraws mechanism: preserve renderer.render in the same temporary __smokeHeldDraw slot and let animation ticks update matrices without submitting the full town while measurements read no pixels. Actual loaded registry, interactions, shared intent, walker, terrain and native-scene colliders are unchanged; no state, movement, assertion or terrain substitute is introduced. For each screenshot it restores the actual render method, forces exactly one real app step/draw, and reinstates the hold in the same page evaluation before the next RAF, then captures the actual composited canvas. This removes redundant full-frame draws from every state/camera/walk read. The finalizer restores the original render method and animation clock before closing. These are existing QA techniques, no source hooks or source edits. No bars loosened and incomplete first attempt remains RED. Human image inspection must confirm the optimized captures show their real poses/states.
