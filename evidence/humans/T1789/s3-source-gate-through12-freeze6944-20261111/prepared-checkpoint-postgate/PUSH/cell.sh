#!/bin/bash
set -euo pipefail
source /workspace/.cloud-setup/transport-activate.sh
cd /dev/shm/chicago-t1789-charles-gate-20261110/chicago/4d
exec python3 /tmp/ROOT-T1789-LINEN-S3-CHECKPOINT-POSTGATE-PREP-20261111/chain.py PUSH
