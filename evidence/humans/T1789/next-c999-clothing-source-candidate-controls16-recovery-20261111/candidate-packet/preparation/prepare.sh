#!/bin/bash
set -euo pipefail
source /workspace/.cloud-setup/transport-activate.sh
export PYTHONDONTWRITEBYTECODE=1
exec /tmp/ROOT-GATE-BIND-PREP-V2-20261110/with-cache.sh -- python3 -B /tmp/T1789-NEXT-CLOTHING-C999-SOURCE-PREP-20261111/prepare.py
