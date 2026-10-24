A feature branch that merges DEV after a full-smoke workflow edit starts another unfiltered measurement. Those runs reach the 150-minute limit and obstruct otherwise green PRs (#1277 and #1278).

Restrict the workflow's automatic own-file push self-test to `dev`. Branch and path filters both apply. Automatic measurements also stop on `main` and tags. Explicit dispatch, nightly smoke, both viewports, all 15 parts, the 150-minute measurement limit and every renderer assertion remain unchanged. This changes one workflow file and no merge-policy code.

This invisible CI repair unblocks visible work in #1277/#1278. Its integration acceptance requires ordinary green-check merges without a blind override; #1278 currently has a real gate failure and is not eligible for a merge.

Validation:

- Latest-base full preflight on accepted DEV `abb1dd407a96`: 1,065 steps / 384 self-tests, none red, 639.020s; cleanup reaped 721 owned descendants with none remaining. Tested tree `4a2c75629c545d8be63dcd0ab8f328603539994b` equals newly committed/pushed HEAD `84272d6e0`.
- Seven trigger/YAML cases pass; the sole semantic change is `push.branches: [dev]`.
- App and reference bytes are exactly identical to accepted DEV `abb1dd4`. Fresh normal hosted gate40121257436, report and content checks passed. The original gate log confirms checkoutQ2158db01731a6b3c7c12f53c7bd7b3a7ed0703b3, tree4a2c7562, 1,065 steps /384self-tests and the workflow-only changelog exemption. No feature-head full smoke was started; the earlier d04/Qf842 green tested the previous base33 and is retained only as historical evidence.
- No new whole-renderer PASS is claimed by a static test or by accepted-base identity. The inherited release-note layout failure is retained and being fixed as T-3125 in #1279, with fresh combined browser coverage required there. Prior focused news-flow passes and overall presentation FAIL remain bound to their actual older source.

Saved evidence: https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence/transport-recovery-2026-10-24/CHECKPOINT-27-CURRENT-DEV-GATE-AND-SAVED-WRAPPING-FIX

Fresh hosted verification complete; ordinary SHA-pinned DEV merge next. No manual rerun/dispatch, assertion change, status filtering or blind override was used.
