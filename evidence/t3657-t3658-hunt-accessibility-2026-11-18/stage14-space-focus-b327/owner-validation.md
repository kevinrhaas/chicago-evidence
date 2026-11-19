# T3658 stage 14 Space focus diagnosis

Smoke-only repair: `b3272f5a4ac513dc4cd09819d21f4f5acefbff1d`, backed up at `backup/t3658-smoke-world-focus`. Runtime source and frozen publication: `edc7099032cd6d55d7a7e7f0d66d313b15960f10`. No runtime file changed.

The official failing Space block is inside `stageOn(14)` and runs at both widths. After the smoke helper focuses and clicks `#nav-close`, Navigator intentionally restores focus to `#nav-grip` (phone) or `#nav-collapse` (desktop). Camera-only `goTo/frame` calls retain that UI focus. Space therefore correctly activates the focused UI instead of inspecting.

The patch establishes and asserts BODY/CANVAS focus immediately before world Space checks. It adds the complementary native Space test on the visible Navigator handle, asserting that the drawer opens without movement, flying or inspection. The original Space-inspects/no-flight assertion and Escape/E-to-close assertions remain intact.

Published Light-detail phone probe: 11/11, exit 0, 55 seconds. It reproduced retained `BUTTON#nav-grip` focus and native Guide opening, then passed the exact patched world Space/no-flight and Escape/reopen/E-close block. Zero page/console or HTTP errors. The server and owned browser closed. Four aborted resource requests were retained in the report; this was not a Jump or texture-drain test.

Published desktop attempt 1 reproduced retained `BUTTON#nav-collapse` focus and passed native UI Space. Immediately afterward, its execution context was destroyed by a navigation before the world-focus precondition. Cleanup stalled inside context.close; the final cached page URL was about:blank. A later localStorage error occurred on that null-origin page. This attempt is failed/incomplete (exit 1, 323 seconds); it grants no desktop coverage. Only its owned Chromium group was terminated after confirming the failure. Artifacts are preserved.

The retry adds navigation/warning recording and direct browser cleanup in the scratch probe, preserving the extracted smoke block byte-for-byte. No test assertion or runtime behavior is weakened.

Artifacts:
- `/tmp/t3658-stage14-published-390/report.json`, sibling `.log` and `-exit.json`
- `/tmp/t3658-stage14-published-1280/report.json`, sibling `.log` and `-exit.json` (failed first attempt)
- `/tmp/t3658-stage14-desktop-pending-call.json`, `/tmp/t3658-stage14-desktop-navigation.json`
- `/tmp/t3658-stage14-published-1280-retry/` (retry)
- `/tmp/t3658-stage13-world-focus.patch` (historical filename; actual stage 14)

This is a bounded actual-town check, with ordinary api.step rendering and continuous animation paused. It is not the complete official stage 14 or stages 13–15 release gate. The remaining full official group must run both widths on the final combined source.

Smoke file SHA256: `76624c859b7cb88af17b9f958c66681308b9c35b2a6d86d65fde44036c2976d2`.
Extracted block SHA256: `f7cbdaec0cc1d2050f019035c8ab9182a10d8f5cc59b9427e250e228adb323be`.

Desktop retry: 11/11, exit 0, 77 seconds, zero page/console or HTTP errors. It reproduced BUTTON#nav-collapse ownership and passed the unchanged native UI Space, world focus, Space inspection/no-flight, Escape, reopen and E-close assertions. Both widths tested identical smoke/block hashes and identical runtime module hashes against the frozen publication. The retry recorded only the initial navigation request; later same-URL frame events coincide with Navigator history updates. It does not explain the first attempt's destroyed execution context, which remains retained as failed/incomplete.

Cleanup confirmed after all attempts: every probe server closed, no Playwright Chromium processes remaining, diagnostic Node inspector closed. Receipt: `/tmp/t3658-stage14-published-cleanup.json`. CPU is released.

Probe slice boundaries: from `// Space is mode-scoped:` through immediately before `// And neither fires from inside the Go-to box:`. The later Go-to typing check and full free-fly sequence are outside this focused run and remain for the official final stage group. Desktop retry retained ten ERR_ABORTED resource requests and eight ordinary renderer/performance/deprecation warnings; it recorded no page/console errors or HTTP errors.
