V5 is prepared and awaits independent matrix review. Do not execute until ROOT approves actual launch.

Fresh6ab transport/UI matrix v5 — external preparation, not executed.

The focused helper v5 was independently reviewed and is pinned to SHA7207204b7c95a72a28a82023878252ba920fc6f53bd534c3a9d939cfc40f2d66. Matrix v5 itself awaits independent review; do not launch until root reviews it. Old V2 scripts and old run1 partial receipts remain unchanged. This package imports no results from C4B8 or any other run.

Supported source: accepted BASE6ab39e9a32a8270b96d9ab252cfddc5962a871a3; final committed tree757e30973d8e8b13d167e86fe95aeb5f58c6a41d; APP77cd7218e00cf750ad1cb423fc05ddb0376ba560. Future --head must be the real full committed H2, containing BASE and exactly those tree/app bytes. No H2 SHA or PASS is invented here. Initial actual staged-index entries/modes were compared to the candidate tree without git write-tree; they matched, with no unstaged or untracked source.

Root must supply actual new preflight/publish/focused receipts. Preflight prefix is exactly6ab-transport-ui-refreshed-base-preflight-before-commit. Publish and focused prefix/output must be NEW6ab-transport-ui-* direct children of transport-recovery. They must have real successful, not timed-out result and complete cleanup with no children; reviewed focused report requires both components, both widths, final source/error guards and exact Node report digest/count -> before/after complete manifest -> current manifest. Source and all published bytes are checked again before/after each leg and at final verification. No helper publishes or derives.

Future driver CLI (do not run now):
python3 dev6ab_transport_ui_matrix_driver.py --execute-fresh-matrix --head ACTUAL_FULL40_H2 --out /workspace/.cloud-setup/logs/transport-recovery/6ab-transport-ui-matrix-run2 --preflight-prefix /workspace/.cloud-setup/logs/transport-recovery/6ab-transport-ui-refreshed-base-preflight-before-commit --publish-prefix ACTUAL_NEW6AB_PUBLISH_PREFIX --focused-prefix ACTUAL_NEW6AB_FOCUS_WRAPPER_PREFIX --focused-output ACTUAL_NEW6AB_FOCUS_OUTPUT

Root launches under the actual owned supervisor and preserves its outer result/cleanup. After driver finishes and all browsers/children are gone, run a separate owned read-only verifier to a NEW independent receipt:
python3 dev6ab_transport_ui_matrix_verify.py --head ACTUAL_FULL40_H2 --run-dir /workspace/.cloud-setup/logs/transport-recovery/6ab-transport-ui-matrix-run2 --receipt /workspace/.cloud-setup/logs/transport-recovery/6ab-transport-ui-independent-final-24-ACTUAL.json

Exact unchanged24-leg shape: mobile1-2/3-4/5-6/7-8/9-10/11-12/13/14/15; desktop1..15. Existing strict published command and canonical transcript parser are unchanged. Mobile13/14 and desktop14 are3600s, desktop13 is10800s, desktop9-12 each3600s, others1800s. Actual timing is retained; >600s is not called foreground-budgetPASS. No assertion changes or automatic retries.

Global owned advisory lock intentionally keeps /workspace/.cloud-setup/abb1-transport-ui-matrix.active.lock, excluding the old generation as well as the new. Busy-process checks retain all known old driver basenames and add the new one. Root's external resource pause is checked before source checks/launch; helpers never clear it. Existing output directory/prefix is refused; failures/interruption are retained and stop. A future same-input outage continuation requires a reviewed explicit resume addendum; old C4 legs cannot transfer to changed APP.

This preparation performs external text writes and read-only Git metadata only. No syntax/import/parser fixtures/browser/gate/owner/publish or primary source/index/mirror writes are authorized here.

V4 preserves frozenV3 and adds only exact focused→matrix preflight/publish association: command arguments and report prefixes must match config, report result/cleanup hashes must match the same real receipts. Driver/verifier/parser/caps remain identical. No syntax/import/fixtures/execution occurred.

V5 provenance correction: earlier source preflight succeeded with stale local origin/dev. Root repaired only local tracking/ref, kept source757/app77 unchanged and repeated fullpreflight against actual accepted6ab. Only that actual refreshed-base preflight prefix is accepted byV5. Earlier gate remains historical. No new H2/result invented.
