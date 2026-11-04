#!/usr/bin/env bash
set -euo pipefail
source /workspace/shared/resume-chicago-env.sh
P=/tmp/cobweb-ee1690-private-pair-20261104
exec python /workspace/shared/run-with-reaping.py "$P/OUTER-REAPER.json" -- timeout --signal=TERM --kill-after=15s 600s nice -n 19 taskset -c 0-4 python "$P/run.py"
