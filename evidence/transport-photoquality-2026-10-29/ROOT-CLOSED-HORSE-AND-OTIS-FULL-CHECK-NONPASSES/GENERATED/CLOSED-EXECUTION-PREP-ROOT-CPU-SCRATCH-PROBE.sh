#!/usr/bin/env bash
set -euo pipefail
out=${1:-/tmp/TRANSPORT-SHM-NODE-PYTHON-PROBE-20261030-01}
[ ! -e "$out" ] && [ ! -e "$out.driver.log" ] || { echo 'Use a fresh scratch-probe output path.' >&2; exit 2; }
source /workspace/.cloud-setup/transport-activate.sh
exec /workspace/.cloud-setup/venv311/bin/python /tmp/TRANSPORT-WHOLE-GATE-SHM-PREP-20261030/run-guarded-whole-gate.py probe --out "$out" > "$out.driver.log" 2>&1
