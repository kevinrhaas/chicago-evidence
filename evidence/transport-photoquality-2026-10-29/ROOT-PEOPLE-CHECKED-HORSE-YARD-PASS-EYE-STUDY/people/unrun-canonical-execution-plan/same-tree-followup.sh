#!/usr/bin/env bash
# Run only after root has reviewed the collected actual native evidence.
set -euo pipefail
people_review=${1:?Usage: same-tree-followup.sh actual-evidence-directory}
people_repo=${PEOPLE_REPO:-/tmp/chicago-transport-resume-20261029}
test "${GITHUB_ACTIONS:-}" != true
test -f "$people_review/REVIEW.json"
people_bot=$(python3 -c 'import json,sys; j=json.load(open(sys.argv[1])); assert j["result"].startswith("PASS"); print(j["bot_HEAD"])' "$people_review/REVIEW.json")
people_tree=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["TREE"])' "$people_review/REVIEW.json")
people_family=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["family"])' "$people_review/REVIEW.json")
people_branch=steward/t1789-people-photoquality-20261026
test "$(git -C "$people_repo" branch --show-current)" = "$people_branch"
test "$(git -C "$people_repo" rev-parse HEAD)" = "$people_bot"
test "$(git -C "$people_repo" write-tree)" = "$people_tree"
test -z "$(git -C "$people_repo" status --porcelain)"
test "$(git -C "$people_repo" ls-remote origin "refs/heads/$people_branch")" = "$(printf '%s\trefs/heads/%s' "$people_bot" "$people_branch")"
git -C "$people_repo" commit --allow-empty -m "ci: request ordinary checks for $people_family canonical delivery (T-1789)"
people_head=$(git -C "$people_repo" rev-parse HEAD)
test "$(git -C "$people_repo" rev-parse HEAD^)" = "$people_bot"
test "$(git -C "$people_repo" rev-parse 'HEAD^{tree}')" = "$people_tree"
(
  cd "$people_repo/chicago/4d"
  export C4D_GATE_REQUIRE_BASE=1
  node tools/check-changelog-entry.mjs 9e14c138848ef854a535271fbd3feaae52dd4aa2 "$people_head"
  node tools/resolve_id_collisions.mjs --base 9e14c138848ef854a535271fbd3feaae52dd4aa2 --check
  node tools/check-changelog.mjs
  node tools/changelog-history.mjs --base 9e14c138848ef854a535271fbd3feaae52dd4aa2
) > "$people_review/SAME-TREE-NEWHEAD-CHECKS.log" 2>&1
test -z "$(git -C "$people_repo" status --porcelain)"
test "$(git -C "$people_repo" ls-remote origin "refs/heads/$people_branch")" = "$(printf '%s\trefs/heads/%s' "$people_bot" "$people_branch")"
git -C "$people_repo" push origin "HEAD:refs/heads/$people_branch"
test "$(git -C "$people_repo" ls-remote origin "refs/heads/$people_branch")" = "$(printf '%s\trefs/heads/%s' "$people_head" "$people_branch")"
test -z "$(git -C "$people_repo" status --porcelain)"
printf '%s\n' "$people_head" > "$people_review/SAME-TREE-FOLLOWUP-SHA.txt"
printf 'Normal-auth same-tree followup pushed: %s. Observe actual PR CI for this exact SHA before the next family.\n' "$people_head"
