# Transport recovery — mobile results and continuing desktop checks

- Draft [PR1279](https://github.com/kevinrhaas/chicago/pull/1279), source `3290195d`, tree `bac89999`. Three child commits remain preserved. T-3083/T-3086/T-3087 are in review, not done.
- Local preflight passed **1,063 steps / 383 negative self-tests** on unchanged source (checkpoint6).
- Mobile stages **1–13 and15 passed**, with zero page errors and complete owned-child cleanup.
- Mobile14 failed **only zero-page-errors**: four real image requests to `kevinrhaas.github.io` were denied by the proxy. Its other139 assertions passed. Actual command1/557.55s and cleanupcomplete are preserved. It is not counted as passed.
- All four local JPEGs match both image manifests by SHA/size and decode successfully. No supported image-origin override exists; no request interception, mocking or error filtering was used.
- Desktop1 is running. Desktop14 is explicitly deferred for the same missing image-host access. Both deferred14 legs remain required; completing the other22legs will not establish the full gate.
- Mobile13 functionally passed160 assertions in22m34, exceeding the600s foreground budget. Keep the actual timing and resource conditions (four CPU quota, software Chromium154); do not claim budget fit.
- Normal PR gate40085901834, report40069749728 and warranted build screen40069749684 succeeded. Moving40085901811 failed InstallPlaywright before any publishing or renderer measurements. Exact installer stderr remains unread.
- The Ubuntu26/Playwright1.56.1 incompatibility path is a hypothesis; no speculative workflow patch, rerun, dispatch or admin merge occurred. Tested gateQ01977/oldbasec968 and newer DEV50a5/candidate7e3a are distinct bindings (checkpoint9).
- Official job-log API authorization succeeds, then proxyCONNECT403 blocks Azure log storage. Direct actual image GET also gets proxyCONNECT403. GitHub API and public DEV preview are reachable.
- Prepared environment draft12 includes `kevinrhaas.github.io`, `productionresultssa14.blob.core.windows.net`, `productionresultssa15.blob.core.windows.net`, existing API/preview hosts and package-manager presets. Saving it did not apply it. Save/apply these settings to unblock required diagnostics and image coverage.
- Follow `/workspace/.cloud-setup/queue-session.json` for the current driver, binding and logfile. All output is redirected; inspect actual processes/receipts before restarting after a runtime disconnect. Historical bindings and failed receipts remain unchanged.

Next: finish unaffected desktop checks; verify actual CDN access after settings apply, then rerun both14 legs with new receipt prefixes; inspect original CI install error and obtain fresh normal green checks; review current head/base/test merge and ordinary lock state before DEV merge and published source/asset verification.

No full browser pass, moving-frame pass, DEV merge, public delivery or production promotion is claimed. Parent photographic/native/world and gait/interaction remainder tickets stay open.
