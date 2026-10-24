A feature branch that merges DEV after a full-smoke workflow edit starts another unfiltered measurement. Those runs reach the 150-minute limit and prevent otherwise green PRs from merging (#1277 and #1278).

Restrict the workflow’s automatic own-file push self-test to `dev`. Branch and path filters both apply. Automatic measurements also stop on `main` and tags; explicit dispatch, the nightly bake’s smoke, both viewport defaults, all 15 parts, the 150-minute measurement limit and every renderer assertion remain unchanged. This changes one workflow file and no merge-policy code.

This is an invisible CI repair that unblocks the visible work in #1277/#1278. T-3121’s integration acceptance still requires those PRs to merge through ordinary green checks without a blind override.

Validation:

- Full preflight: **1,064 steps / 384 self-tests**, none red, 673.643s. Cleanup reaped 721 owned descendants with none remaining. Committed tree `534ff7c9` equals the validated input.
- Seven trigger/YAML cases passed; the only semantic change is `push.branches: [dev]`.
- App/reference content is identical to accepted DEV `33a99a55`. Existing exact-source renderer evidence and the inherited release-note fold are being checked separately; the focused published news probe and fresh normal PR CI are pending. No new whole-renderer pass is claimed by the static test.

This owner-visible PR remains draft while those final checks run.
