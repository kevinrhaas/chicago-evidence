#!/usr/bin/env bash
# PREPARED ONLY. Do not run until root authorizes this exact fresh checked HEAD.
# Native gh workflow_dispatch calls only; no checkout, source edit, rerun or merge.
set -euo pipefail
: "${T3173_ROOT_GO:?Set to DISPATCH-FRESH-CHECKED-HEAD only after root GO}"
test "$T3173_ROOT_GO" = DISPATCH-FRESH-CHECKED-HEAD
: "${T3173_CHECKED_HEAD:?Full new checked and pushed 40-hex commit required}"
[[ "$T3173_CHECKED_HEAD" =~ ^[0-9a-f]{40}$ ]]
test "$T3173_CHECKED_HEAD" != a96607b40eaa12f0d94b9438973afb74b2bf6aca
test "$T3173_CHECKED_HEAD" != 6c103072dae94ed58cc8fc06462aef2638be736f
repo=kevinrhaas/chicago
branch=steward/t2793-wagon-photoquality-20261026
assert_remote_head() {
  test "$(gh api "repos/$repo/git/ref/heads/$branch" --jq '.object.sha')" = "$T3173_CHECKED_HEAD"
  test "$(gh api "repos/$repo/pulls/1340" --jq '.head.sha')" = "$T3173_CHECKED_HEAD"
  test "$(gh api "repos/$repo/pulls/1340" --jq '.base.ref')" = dev
}
assert_workflow() {
  local workflow_path=$1 expected_workflow_sha=$2 actual_workflow_sha
  actual_workflow_sha=$(gh api "repos/$repo/contents/$workflow_path?ref=$T3173_CHECKED_HEAD" --jq '.content' | base64 --decode | sha256sum)
  test "${actual_workflow_sha%% *}" = "$expected_workflow_sha"
}
assert_remote_head
# Fail closed if the exact new HEAD changed native workflow semantics.
assert_workflow .github/workflows/chicago-4d-frame-time.yml 380caa3be97ab0383b073118271f6a2a1385adc551b5be17153bf42009acae1c
assert_workflow .github/workflows/chicago-4d-smoke.yml f0f6c6f5cf942af4e49609b7854bdd1472bd98e06159e687ed76893138e7a73c
assert_workflow .github/workflows/chicago-4d-bake.yml 9d8b658e2a7efa4eb553d35cdafefa5fc239c39fe10a5733bb996c1d271ac854
# Capture existing dispatch IDs/time in an external ledger BEFORE invoking this file.
gh workflow run chicago-4d-frame-time.yml --repo "$repo" --ref "$branch"
for viewport in mobile desktop; do
  for stage in 1-2 3-4 5 6-7 8 9-12 13 14 15; do
    assert_remote_head
    printf 'Dispatching head=%s viewport=%s stage=%s UTC=%s\n' "$T3173_CHECKED_HEAD" "$viewport" "$stage" "$(date -u +%FT%TZ)"
    gh workflow run chicago-4d-smoke.yml --repo "$repo" --ref "$branch" -f "viewport=$viewport" -f "stage=$stage"
  done
done
assert_remote_head
# Dispatch submission is not success. See PLAN.md for exact SHA/input/log mapping.
