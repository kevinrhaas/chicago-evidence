#!/bin/bash
set -euo pipefail
source /workspace/.cloud-setup/transport-activate.sh
export PYTHONDONTWRITEBYTECODE=1
cd /dev/shm/chicago-t1789-charles-gate-20261110/chicago/4d
exec python3 -B /tmp/T1789-NEXT-CLOTHING-C999-CONTROLS-PREP-20261111/execute.py
