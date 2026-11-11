#!/bin/bash
set -euo pipefail
source /workspace/.cloud-setup/transport-activate.sh
export PYTHONDONTWRITEBYTECODE=1
exec python3 -B /tmp/T1789-NEXT-CLOTHING-C999-CONTROLS-PREP-20261111/run.py
