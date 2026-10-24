#!/usr/bin/env bash
# Prepared only. Root must give actual resource handoff before execution.
set -u
source /workspace/.cloud-setup/transport-activate.sh
unset CHICAGO_TICKETS_DIR
export C4D_GATE_REQUIRE_READERS=1
python3 /workspace/.cloud-setup/transport-supervise.py \
  --prefix /workspace/.cloud-setup/logs/transport-recovery/PR1278-PIN70b-canonical-OWNER1 \
  --cwd /workspace/chicago-smoke-infra-t3121/chicago/4d --timeout 1800 \
  -- python3 /workspace/.cloud-setup/logs/transport-recovery/PR1278-a729-plus-PINNED-70b-intake-preparation/canonical-owner-worker.py
task_owner_rc=$?
python3 /workspace/.cloud-setup/logs/transport-recovery/PR1278-a729-plus-PINNED-70b-intake-preparation/canonical-owner-worker.py --snapshot-final-only
task_snapshot_rc=$?
if [ "$task_owner_rc" -ne 0 ]; then exit "$task_owner_rc"; fi
if [ "$task_snapshot_rc" -ne 0 ]; then exit 70; fi
