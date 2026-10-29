#!/bin/bash
set -euo pipefail
source /workspace/.cloud-setup/transport-activate.sh
python tools/human_natural_idle.py --check
python tools/human_contract.py --check
python tools/human_contract.py --self-test
python -m unittest discover -s tools -p test_human_natural_idle.py
node tools/test_human_frame_time.mjs
node tools/test_human_body_ray_grid.mjs
git diff --check
