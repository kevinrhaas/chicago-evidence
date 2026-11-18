#!/bin/bash
source /tmp/t3654-runtime.sh
c4d_gate_started_ns=$(date +%s%N)
timeout --kill-after=5s 590s env CHECK_PART=2/16 CHECK_JOBS=4 CHECK_TIMINGS=/tmp/t3654-source-fallback-2of16-attempt1-timings.tsv bash tools/check.sh > /tmp/t3654-source-fallback-2of16-attempt1.log 2>&1
c4d_gate_rc=$?
c4d_gate_ended_ns=$(date +%s%N)
python3 - /tmp/t3654-source-fallback-2of16-attempt1.process.json "$c4d_gate_rc" "$c4d_gate_started_ns" "$c4d_gate_ended_ns" <<'PY'
import json,sys
from pathlib import Path
Path(sys.argv[1]).write_text(json.dumps({'part':'2/16','exit_code':int(sys.argv[2]),'start_epoch_ns':int(sys.argv[3]),'end_epoch_ns':int(sys.argv[4])},indent=2)+'\n')
PY
exit "$c4d_gate_rc"
