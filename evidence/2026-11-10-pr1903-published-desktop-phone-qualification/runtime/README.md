# Bounded actual grouped app QA (external, not yet run)

The helper boots the actual published1835 scene once per viewport, using the existing held-draws policy: no-pixel measurements use the real app while draw submissions are held; each screenshot submits one real scene frame before capture. Desktop1280×800DPR1 and phone390×780DPR2 run serially after the parent grants the GPU slot. No install, publish, source change or GitHub operation is included.

Prepare the explicit expected manifest only **after** the parent has verified and integrated authentic native83 and compiled current sidecars/WEB. Supply the actual40-character source commit baked, actual native workflow run ID and actual published build prefix. These values are intentionally not guessed in the helper. The manifest records that qualified provenance; generating it is not bake authentication.

```bash
source /tmp/chicago-resume-env-20261109.sh
export PW_MODULE=/tmp/chicago-browser-tools/node_modules/playwright/index.mjs
node /tmp/nov10-group-published-review/prepare-expected.mjs \
  --root /tmp/chicago-west-wicket-20261109/chicago/4d \
  --source-sha ACTUAL_40_CHARACTER_BAKED_SOURCE_SHA \
  --native-run ACTUAL_NATIVE_RUN_ID \
  --build-prefix ACTUAL_PUBLISHED_BUILD_PREFIX \
  --out /tmp/nov10-group-published-review/expected.json
node /tmp/nov10-group-published-review/review.mjs \
  --url http://127.0.0.1:4188/walk/ --viewport desktop \
  --expected /tmp/nov10-group-published-review/expected.json \
  --out /tmp/nov10-group-published-review/desktop
node /tmp/nov10-group-published-review/review.mjs \
  --url http://127.0.0.1:4188/walk/ --viewport phone \
  --expected /tmp/nov10-group-published-review/expected.json \
  --out /tmp/nov10-group-published-review/phone
```

Use the parent's actual published server port/base URL if different. The helper forces `year=1835` and `keep-geometry=1`; it rejects the raw renderer path. Both viewport runs perform the same bounded checks:

- Fetch actual loaded published `/data/gltf/` WEB bytes for Cobweb, Green Tree, Jail and the retained keeper control; compare SHA-256 and byte counts to the explicit native pin. Check July 1 target date and published build prefix. Require the current 1.30 m Cobweb band, 4.6 m Green Tree shoulder attachment and 2.44 m reconstructed Jail fence.
- Bind every retained review note to the exact flagged actual registry key, record ID and sidecar ID. Require equality to the pinned compiled review ID list and each exact allowed message once. Preserve raw problems; unrelated, malformed or duplicated problems fail.
- Capture each building at a street pose, recording actual walker and terrain positions. Jail additionally measures actual target-record enclosure vertices after quantization/world transform against actual terrain, checks authored world bounds/origin, and captures elevated compound context. No substitute geometry is used.
- Open each actual card's Sources, Images and new Liberty. Require governing source text, nonempty credited image entries, accurate Images count, actual held thumbnail readiness when one is deferred, no eager Images `src` before opening, and the explicit reconstructed numeric liberty. Save screenshots and full disclosure text.
- Require zero hard app problems, page errors, request failures, HTTP errors and console errors. Raw receipts remain available on failure.

Expect **13 screenshots per viewport**: three street views, one extra Jail elevated view, and Sources/Images/Liberties for each building. Runtime/card checks can pass while visuals still need review. `PASS_FOCUSED_REVIEW_REQUIRES_HUMAN_SCREENSHOT_INSPECTION` explicitly requires viewing the PNGs, especially Cobweb's lower boards, Green Tree's shoulder junction and Jail's roof above the pointed fence. If a pose is obstructed, record and improve the external pose without changing scene/source data or declaring a match.

This bounded review is not the full smoke/photo gate, ticket closure, historical camera match or complete compound/date acceptance. All original tickets remain partial. Source-matching comparisons and native/WEB audit are separate parent-owned checks.

Only helper syntax was checked before handoff. No browser, published server or GPU run occurred while preparing these files.
