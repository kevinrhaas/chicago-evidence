#!/usr/bin/env bash
# Prepared only. Run after the configured GitHub API/artifact policy permits it.
set -euo pipefail
family=${1:?Usage: dispatch-family.sh dress|teamsters actual-source-sha}
people_source=${2:?actual-source-sha is required}
people_repo=${PEOPLE_REPO:-/tmp/chicago-transport-resume-20261029}
people_out=${PEOPLE_EVIDENCE:?Set PEOPLE_EVIDENCE to a new persistent evidence directory}
people_branch=steward/t1789-people-photoquality-20261026
test "$family" = dress || test "$family" = teamsters
test "$(git -C "$people_repo" branch --show-current)" = "$people_branch"
test "$(git -C "$people_repo" rev-parse HEAD)" = "$people_source"
test -z "$(git -C "$people_repo" status --porcelain)"
if test "$family" = dress; then
  test "$people_source" = a3971c9a638e03216945fc52ce57d7453596187e
fi
PYTHONDONTWRITEBYTECODE=1 python3 - "$people_repo" "$people_source" "$family" <<'PY'
import importlib.util, pathlib, subprocess, sys
r=pathlib.Path(sys.argv[1]); source=sys.argv[2]; family=sys.argv[3]
s=importlib.util.spec_from_file_location('reviewed_human_delivery',r/'chicago/4d/tools/human_delivery.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
assert subprocess.check_output(['git','show',source+':.github/workflows/chicago-4d-humans.yml'],cwd=r)==(r/'.github/workflows/chicago-4d-humans.yml').read_bytes()
m.source_binding({'source':source})
if family=='teamsters':m.require_female_delivery({'source':source})
else:
 assert not (r/'chicago/4d/data/humans/canonical-deliveries/dress.json').exists()
print('Exact reviewed source and native family ancestry guard passed; no generation has run locally.')
PY
test "$(git -C "$people_repo" ls-remote origin "refs/heads/$people_branch")" = "$(printf '%s\trefs/heads/%s' "$people_source" "$people_branch")"
mkdir "$people_out"
date -u +%Y-%m-%dT%H:%M:%SZ > "$people_out/dispatch-not-before.txt"
printf '%s\n' "$people_source" > "$people_out/expected-source-sha.txt"
printf '%s\n' "$family" > "$people_out/family.txt"
if test "$family" = dress; then
  gh workflow run chicago-4d-humans.yml --repo kevinrhaas/chicago --ref "$people_branch" \
    -f build_dress_study=true -f build_teamsters=false -f build_seated_driver_study=false \
    -f deliver_generated_assets=true -f source_ref="$people_source"
else
  # A nonempty source_ref is rejected when build_dress_study is false.
  gh workflow run chicago-4d-humans.yml --repo kevinrhaas/chicago --ref "$people_branch" \
    -f build_dress_study=false -f build_teamsters=true -f build_seated_driver_study=false \
    -f deliver_generated_assets=true -f source_ref=
fi
gh api --method GET repos/kevinrhaas/chicago/actions/workflows/chicago-4d-humans.yml/runs \
  -f event=workflow_dispatch -f branch="$people_branch" -f head_sha="$people_source" -f per_page=100 \
  > "$people_out/run-candidates.json"
printf 'Inspect run-candidates.json for the actual run ID and matching creation time/head SHA; do not redispatch to obtain an ID.\n'
