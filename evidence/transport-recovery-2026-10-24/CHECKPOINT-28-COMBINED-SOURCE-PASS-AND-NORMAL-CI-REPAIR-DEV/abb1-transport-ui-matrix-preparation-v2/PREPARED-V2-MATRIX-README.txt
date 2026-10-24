Fresh transport/UI 24-leg matrix — version 2, prepared only

No new matrix, browser, supervisor, publisher, owner, gate or application command has run during this preparation. Syntax checks, historical-log parser fixtures and explicitly synthetic prerequisite fixtures are the only validation performed. Historical smoke results are never imported as matrix completions. Version 1 is preserved in the adjacent abb1-transport-ui-matrix-preparation directory.

The new driver requires an explicit complete future HEAD whose committed tree is 4b2a7066a039936ddcc65d8c1c891fcf25dd7e5f and app subtree is 43838a949e02a01de4ad064aa859c2d11995524d. The normal combined preflight must have passed on its recorded matching input tree with zero owned children. The actual fresh publish and completed guarded focused wrapping proof are supplied as explicit receipt prefixes; no attempt-1 prefix is assumed. The focused helper must be the reviewed 07a051… version, with both required viewport identities, successful final guards/components and complete supervisor cleanup.

The focused BEFORE manifest must first match its reviewed report’s original Node digest and file count. The focused BEFORE and AFTER manifests must agree. Their complete normalized bytes/hash census and raw manifest file hashes are retained in prerequisites. The matrix's initial, per-leg and final complete published file hashes must equal that focused census. A ticket-mirror write, republish, build-stamp change, extra file or changed byte stops the matrix. Do not run ticket CLI mutations, publishers or source writers on this checkout until all browser work finishes.

All results start empty in a NEW output directory. Mobile stages are 1-2, 3-4, 5-6, 7-8, 9-10, 11-12, 13, 14, 15; desktop stages are 1 through 15 separately. Each width covers each part exactly once. Every actual leg must return zero, have a positive staged-check count, an unambiguous successful footer, actual completion/zero-page-error pass lines, no failure lines and zero owned descendants. Wrong viewport, stage, cwd, command or timeout fails verification. Source HEAD/tree/app/index/worktree and complete published bytes are checked before and after each leg. Every failure is retained and stops execution; no automatic retry or inherited resume exists.

Bounds: mobile 13/14 and desktop 14 use 3,600 seconds. Desktop 13 explicitly uses 10,800 seconds because the verified accepted reference took 7,767 seconds. Desktop 9-12 each use 3,600 because their accepted grouped cost was 2,216 seconds with no trustworthy individual distribution. Other legs use 1,800, above measured containing groups/parts up to 1,373 seconds. These are operational bounds. Any actual duration above 600 seconds is explicitly reported as not fitting the foreground budget, even when its functional smoke passes. No assertion or repository budget is changed.

The driver owns a separate external advisory lock, checks for live Chromium/smoke/focused/known old continuation processes, and waits for the existing resource-pause file before checking source or requesting launch. It never signals unowned processes or changes the global pause file. The unchanged supervisor owns browser cleanup. Results and state are saved after each leg for the root agent to checkpoint.

Root launch, after the fresh focused proof and all prerequisite receipts complete:

source /workspace/.cloud-setup/transport-activate.sh
python3 /workspace/.cloud-setup/logs/transport-recovery/abb1-transport-ui-matrix-preparation-v2/abb1_transport_ui_matrix_driver.py --execute-fresh-matrix --head ACTUAL_FULL_HEAD --out /workspace/.cloud-setup/logs/transport-recovery/abb1-transport-ui-matrix-NEW_ATTEMPT --preflight-prefix /workspace/.cloud-setup/logs/transport-recovery/abb1-transport-ui-combined-preflight --publish-prefix ACTUAL_AFTER_TICKET_REVIEW_PUBLISH_PREFIX --focused-prefix ACTUAL_FOCUSED_ATTEMPT2_PREFIX --focused-output ACTUAL_FOCUSED_ATTEMPT2_OUTPUT

The root agent should supervise the driver externally and preserve its receipts. No local preview URL is a user-facing deliverable.

After all 24 legs complete, the driver rereads the actual logs/results/cleanup and source bindings before producing FINAL-24-LEG-VERIFICATION.json. Independently rerun the read-only verifier before claiming full coverage:

python3 /workspace/.cloud-setup/logs/transport-recovery/abb1-transport-ui-matrix-preparation-v2/abb1_transport_ui_matrix_verify.py --head ACTUAL_FULL_HEAD --run-dir ACTUAL_MATRIX_DIRECTORY --receipt /workspace/.cloud-setup/logs/transport-recovery/abb1-transport-ui-matrix-FINAL-VERIFY-NEW.json

The verifier checks all 24 unique legs, exact part coverage, receipt/log hashes, per-leg source and mirror bindings, unchanged prerequisite/helper receipts and the current source/mirror. It refuses while a browser or matrix driver remains active. Totals come only from actual completed footers. A matrix PASS does not promote production, close photographic/gait remainders or transfer to a later source tree.
