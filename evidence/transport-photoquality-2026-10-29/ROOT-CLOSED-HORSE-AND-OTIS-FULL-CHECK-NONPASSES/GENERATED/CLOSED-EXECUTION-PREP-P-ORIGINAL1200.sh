#!/usr/bin/env bash
set -euo pipefail
out=${1:-/tmp/OTIS-WHOLE-GATE-SHM-20261030-01}
[ ! -e "$out" ] && [ ! -e "$out.driver.log" ] || { echo 'Use a fresh whole-gate output path.' >&2; exit 2; }
source /workspace/.cloud-setup/transport-activate.sh
exec /workspace/.cloud-setup/venv311/bin/python /tmp/TRANSPORT-WHOLE-GATE-SHM-PREP-20261030/run-guarded-whole-gate.py run --worker P --out "$out" --root-slot-go > "$out.driver.log" 2>&1
