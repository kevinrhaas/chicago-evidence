# Navigator rail keyboard fixture

Tested commit: 15ebfe4ce2ba26ec30ee4cef850ba655301675fe.

All 36 checks passed: 390x780 and 1280x800, with normal motion and reduced motion. Actual createNavigator, createRail, Navigator markup and Navigator CSS were served from /workspace/chicago-rail. Small fixture app bodies replaced the world-dependent app contents. The year chip used the same navigator.select('jump') listener as main.js.

Real Tab, Shift+Tab, arrows, Home, End, Enter, Escape and N covered Home -> Move, year chip -> Jump, a single surviving visible Tab stop, truthful aria-selected values, manual activation, close/reopen, conditional tab disappearance and unregistration. No canvas, WebGL scene, world asset, remote request, page error or HTTP error occurred. One browser and one local server were used; both closed at completion.

Source hashes match the committed files (commit-verification.json). The two normal-motion screenshots were visually inspected: phone and desktop both show Jump remaining open while Map has a clear keyboard focus outline. Reduced-motion screenshots are retained too.

Read-only source review of syncTabStop and its registration/selection/evaluation/unregistration calls found no blocker. The helper preserves eligibility during delayed hiding and does not alter app selection or loading.

This is a DOM keyboard fixture, not a complete application, physical-phone test, assistive-technology certification or complete release gate. The initial Playwright bundled-browser lookup failed before any page opened; its report and log are retained. The successful run uses installed /usr/bin/chromium. No app files were edited by this review.
