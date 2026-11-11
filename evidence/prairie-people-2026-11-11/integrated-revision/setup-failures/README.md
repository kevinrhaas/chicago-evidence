# Browser setup failures, retained

On application commit b5cc48c08, the code gate passed (run 43058287448). All twelve browser workflows failed before running browser assertions: Ubuntu archive DNS failed during Playwright dependency installation. An unchanged retry reproduced the failure; the desktop stage 13 attempt-2 log is included.

Commit bf9db83f8 changes only CI setup. When default Ubuntu mirror DNS fails, it verifies all four Noble suite InRelease signatures with the runner's installed Ubuntu archive keyring before adding Kernel.org's mirror at explicit priority 0. The existing fallback URLs, package verification, pinned runner/Playwright and test assertions are preserved. Ten isolated self-tests pass. Fresh full-suite results are pending, not claimed green.

These logs document setup failures, not application test results. The whole application subtree is identical to locally validated b5cc48c08: 20cf29d39ee118ed0993a0d3f90f5038f7d5e702.
