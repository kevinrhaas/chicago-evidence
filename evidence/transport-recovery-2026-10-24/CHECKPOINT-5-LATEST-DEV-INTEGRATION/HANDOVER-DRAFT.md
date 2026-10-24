# Transport recovery handover draft — 24 October 2026

Captured 2026-10-24T06:23:03.276029+00:00. This is a recovery/local-validation checkpoint, not proof of new GitHub CI, a DEV merge, photographic completion, or production promotion.

The app is `/workspace/chicago`, branch `steward/t3083-t3086-t3087-transport-recovery-20261024`. **Current committed HEAD is `3290195d40cbacf5cbfd0c76f14119d6712aa30c`, tree `bac89999d2afd653e632c52d15b2f50336688deb`.** Root ordinarily merged current DEV `29ea317f30ea110c4477e84a8d34b55f9fc50e55`, preserving all three source commits, with no force push. `latest-dev-integration.json` explicitly requires new validation for this merge.

The preserved child commits are:

- T-3083: `4a14cdf92eaa2eb4286da27e4dbed19ea05b1cab` — rounded Brougham lamps, 30 paths.
- T-3086: `d718a1711fd52c9632d40ff7848aca058cade3d7` — UV-only horse-eye repair and measured isolation entry, 21 paths.
- T-3087: `8c45c899f696eb87da9f818828bed36668bdfa2b` — safe yard viewpoint and shared provenance/status, eight paths.

The remote recovery branch was verified by native Git at current HEAD `3290195d40cbacf5cbfd0c76f14119d6712aa30c`. Evidence checkpoint 4 is pushed as `6a52c4d`, but contains the **old HEAD's** preflight pass. Root owns further app/evidence pushes. Use one grouped PR named for all three children, not three competing PRs.

The original 58-file / 24,030,831-byte snapshot came from `kevinrhaas/chicago-evidence/evidence/transport-refinement-resume-2026-10-23/FINAL-SOURCE-BEFORE-GATE`; every saved file hash was verified. Incoming data/bakes were retained. The append-only liberty correction restores historical V17 text and adds an explicit V18 amendment, without dropping the accepted lamp/eye notes. All original liberty raw lines, all 67 named Glessner Markdown blocks, all 58 Glessner JSON records, and ROADMAP's original non-UTF8 `0xFC` byte remain preserved.

The new committed merge differs from DEV 29ea317f in exactly the expected **59 recovery paths**, with no unexpected path. All three child commits are ancestors. Of the prior 59 source-file hashes, 55 remain identical; four shared files legitimately include incoming DEV additions: `tools/check.sh`, `tools/step_isolation.json`, `docs/LIBERTIES.md`, and generated `data/liberties.json`. All prior gate/liberty raw lines remain, both parents' existing isolation rows are unchanged, and the three transport liberty records remain exact. See the separate pinned-commit `latest-dev-merge-preservation-audit.json` and its read-only reproducer; this audits committed tree bac89999, not transient owner-tail writes.

Historical validation on old HEAD 8c45c899f remains valid evidence for that tree only:

- The post-amendment canonical tail passed in 424.600s: 59 steps, two laps, final lap unchanged (`append-only-derived-owner-tail.*`).
- Complete preflight 1 failed in 657.063s solely because the newly gated UV test lacked its measured isolation row. The normal measurement command genuinely executed it, recorded empty writes, and the normal isolation audit passed; no existing registry row was weakened.
- Complete preflight 2 passed in 667.458s: **1,062 steps, none red**, including 383 negative self-tests. Its precommit changelog question saw unchanged HEAD; the actual committed HEAD then passed the separate changelog and ticket-ID checks (`exact-head-*.log`). `app-commit-receipt.json` binds that validated combined source and final old-HEAD tree to `a954088580272b10145fc9df9d46f4a775dbfa3c`.
- Independent actual lamp near/mid/card/LOD checks, exact UV reproduction/protected-boundary controls, and 19-anchor dry-ground/outside-roof checks passed. Root inspected the fixed-camera CPU lamp/plate and both eye pairs (`root-visual-review.json`). Those are bounded software form/UV/navigation results, not native PBR/world/mobile/photographic acceptance.

**Current validation is unfinished:** `latest-dev-derived-tail.log` is the active canonical tail for the merged current tree; no terminal result receipt existed at draft capture. Fresh complete preflight and the required browser coverage are still needed for the new HEAD. Do not reuse old passing receipts as though they certify 3290195d.

The old-HEAD mobile stages 1–2 run was **intentionally interrupted after 93.211s, return code 130** when DEV advanced. It recorded 36 staged checks, `coverage_verified: false`, and is **NOT PASS** (`smoke-mobile-1-2.*`, `smoke-batch-binding.json`). Its corrected-wrapper cleanup reports `cleanup_complete: true` and zero remaining owned children. Its old batch binding is not reusable across the changed tree.

**Cleanup distinction:** both earlier full-preflight cleanup receipts report **701 remaining owned children each**. Neither is a clean-process receipt; do not relabel them clean. The corrected supervisor's separate 32-child test drained all 32 and reported zero remaining (`supervisor-owned-drain-check.*`), and the interrupted smoke above has its own successful cleanup receipt. These do not retroactively repair older cleanup records. Assess each new command's own receipt; never signal PID1 or unowned processes.

Use `source /workspace/.cloud-setup/transport-activate.sh` for installed Python 3.11/Node 22 and bounded math threads. Keep `CHICAGO_TICKETS_DIR` unset for fixture tests. Run heavy work sequentially through the corrected `/workspace/.cloud-setup/transport-supervise.py` with fresh log prefixes. Preserve the original browser/OCI failures and interrupted original-session preflight as nonpasses. A readiness probe, partial transcript, expected workflow number, or branch push is not a gate or delivery result.

Shipping scope remains exact: T-3083 changes lamp form only, preserving non-lamp geometry/materials/anchors/contacts/proxy/policies; T-3086 changes declared ocular UV mapping/notice only, preserving horse geometry/mechanics/materials and all six images; T-3087 adds the safe camera at E−124/N−292/yaw221.19, preserving the horse and all previous 18 viewpoints.

Remaining acceptance stays open: T-3084/T-3085 own carriage photographic appearance/interfaces/portable and native-published qualification; T-3088/T-3089 own horse anatomy/materials/portable photographic qualification. Parents T-2794/T-2800 stay split and must not be closed for this increment. Gait/drivers/riders/tack/teams/boarding and interaction acceptance remain separate; T-2803/T-2804 were released/open, not newly claimed by this recovery. Never promote the gait study's old eye texture over d454.

Next: let the new owner tail finish and inspect its actual result; obtain fresh complete preflight and bound published smoke coverage on the final tree; recheck current DEV, competing PRs and claims; open the one grouped PR; collect its normal required CI results at the actual current HEAD; merge ordinarily only on fresh green checks; verify published DEV source/asset hashes and the yard viewpoint; then use the normal ticket CLI and real PR number for only T-3083/T-3086/T-3087. Production promotion is not authorized.

Checkpoint5 update: fresh derived owner tail passed59steps in214.547s, one unchanged lap. Fresh complete preflight is running; no pass is claimed yet for that gate or for new-tree browser coverage.
