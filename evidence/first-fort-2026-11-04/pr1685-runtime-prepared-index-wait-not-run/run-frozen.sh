#!/usr/bin/env bash
set -euo pipefail
source /workspace/shared/resume-chicago-env.sh
fort_runtime_head=${1:?Final qualified head is required}
fort_runtime_tree=${2:?Final qualified tree is required}
fort_runtime_root=/tmp/first-fort-runtime-1685-20261104
test ! -e "$fort_runtime_root/OUTER-REAPER.json"
# The caller must first obtain the exclusive source/publication writer freeze and GPU lease.
# Keep controller stdout on a regular file so reconnects cannot break a proven child leg.
setsid --fork --wait python /workspace/shared/run-with-reaping.py "$fort_runtime_root/OUTER-REAPER.json" -- python "$fort_runtime_root/run.py" --head "$fort_runtime_head" --tree "$fort_runtime_tree" --run > "$fort_runtime_root/CONTROLLER.log" 2>&1
