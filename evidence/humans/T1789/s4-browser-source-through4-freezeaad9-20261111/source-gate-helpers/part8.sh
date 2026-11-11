#!/bin/bash
set -euo pipefail
source /workspace/.cloud-setup/transport-activate.sh
export CHECK_JOBS=4
exec python3 /tmp/t1789-settler-s4-source-full-gate-prep-20261111/part.py 8
