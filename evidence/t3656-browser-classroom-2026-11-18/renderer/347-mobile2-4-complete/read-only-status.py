#!/usr/bin/env python3
import datetime as dt
import json
from pathlib import Path
import re

root = Path('/tmp/t3658-347-mobile-2-12')
manifest = json.loads((root / 'manifest.json').read_text())
rows = []
failures = []
for row in manifest['stages']:
    item = {key: row.get(key) for key in ['stage', 'status', 'exit_code', 'elapsed_seconds', 'timeout_pid']}
    item['summary'] = row.get('validation', {}).get('summary')
    rows.append(item)
    lines = (root / row['log']).read_text(errors='replace').splitlines()
    failures += [{'stage': row['stage'], 'line': line} for line in lines if re.match(r'^\s*FAIL\s+', line)]
latest = manifest['stages'][-1]
lines = (root / latest['log']).read_text(errors='replace').splitlines()
proc = Path('/proc') / str(latest['supervisor_pid'])
fields = (proc / 'stat').read_text().rsplit(')', 1)[1].split() if proc.exists() else None
print(json.dumps({'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'cohort': manifest['status'],
                  'supervisor_pid': latest['supervisor_pid'], 'supervisor_state': fields[0] if fields else 'absent',
                  'supervisor_pgid': int(fields[2]) if fields else None,
                  'supervisor_session': int(fields[3]) if fields else None,
                  'stages': rows, 'failures': failures, 'latest_tail': lines[-2:],
                  'stop_reason': manifest.get('stop_reason')}, separators=(',', ':')))
